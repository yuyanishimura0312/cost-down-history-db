#!/usr/bin/env python3
"""
Cost-Down History DB (CDH-DB) v1.0 — Validation Script
======================================================

Validates schema integrity, numerical sanity, genealogy structure,
mechanism axis distribution, URL liveness, and hallucination signals.

Outputs:
  - VALIDATION_REPORT.md (markdown, textbook style)
  - Stdout summary

Standard library only. URL liveness uses urllib + ThreadPoolExecutor.
"""

from __future__ import annotations

import sqlite3
import sys
import re
import json
import time
import socket
import ssl
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, Counter
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "cdh.sqlite"
REPORT_PATH = PROJECT_ROOT / "VALIDATION_REPORT.md"

# Thresholds / config
URL_TIMEOUT = 10           # seconds
URL_PARALLELISM = 24
ERA_YEAR_MIN = 1700
ERA_YEAR_MAX = 2030
ERA_END_OPEN_SENTINEL = 9999
FUZZY_NAME_THRESHOLD = 0.90  # SequenceMatcher ratio for "near-duplicate name" flag
EXPECTED_AXES = {"M1", "M2", "M3", "M4", "M5", "M6"}


# ---------- Severity helpers ----------

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"


def conn():
    return sqlite3.connect(DB_PATH)


# ---------- 1. Schema integrity ----------

def check_schema_integrity(c) -> dict:
    findings = []

    # method_id uniqueness already enforced by PRIMARY KEY; verify in case
    rows = c.execute("SELECT method_id, COUNT(*) FROM methods GROUP BY method_id HAVING COUNT(*) > 1").fetchall()
    if rows:
        findings.append((FAIL, f"methods.method_id duplicates: {rows}"))
    else:
        findings.append((PASS, "methods.method_id is unique (PK constraint holds)"))

    # method_id null check
    rows = c.execute("SELECT COUNT(*) FROM methods WHERE method_id IS NULL OR method_id = ''").fetchone()[0]
    if rows:
        findings.append((FAIL, f"methods.method_id NULL/empty: {rows} row(s)"))
    else:
        findings.append((PASS, "methods.method_id has no NULL/empty values"))

    method_ids = {r[0] for r in c.execute("SELECT method_id FROM methods").fetchall()}

    # FK: evidence.method_id
    orphans = c.execute(
        "SELECT evidence_id, method_id FROM evidence "
        "WHERE method_id IS NOT NULL AND method_id NOT IN (SELECT method_id FROM methods)"
    ).fetchall()
    if orphans:
        findings.append((FAIL, f"evidence.method_id orphans ({len(orphans)}): {orphans[:5]}{'…' if len(orphans) > 5 else ''}"))
    else:
        findings.append((PASS, "evidence.method_id → methods FK valid"))

    null_method = c.execute("SELECT COUNT(*) FROM evidence WHERE method_id IS NULL").fetchone()[0]
    if null_method:
        findings.append((WARN, f"evidence.method_id NULL: {null_method} row(s) (orphan-by-null)"))

    # FK: genealogy.parent / child
    parent_orphans = c.execute(
        "SELECT rel_id, parent_method_id FROM genealogy "
        "WHERE parent_method_id IS NOT NULL AND parent_method_id NOT IN (SELECT method_id FROM methods)"
    ).fetchall()
    child_orphans = c.execute(
        "SELECT rel_id, child_method_id FROM genealogy "
        "WHERE child_method_id IS NOT NULL AND child_method_id NOT IN (SELECT method_id FROM methods)"
    ).fetchall()
    if parent_orphans:
        findings.append((FAIL, f"genealogy.parent_method_id orphans ({len(parent_orphans)}): {parent_orphans}"))
    else:
        findings.append((PASS, "genealogy.parent_method_id → methods FK valid"))
    if child_orphans:
        findings.append((FAIL, f"genealogy.child_method_id orphans ({len(child_orphans)}): {child_orphans}"))
    else:
        findings.append((PASS, "genealogy.child_method_id → methods FK valid"))

    # FK: critiques.method_id
    crit_orphans = c.execute(
        "SELECT critique_id, method_id FROM critiques "
        "WHERE method_id IS NOT NULL AND method_id NOT IN (SELECT method_id FROM methods)"
    ).fetchall()
    if crit_orphans:
        findings.append((FAIL, f"critiques.method_id orphans ({len(crit_orphans)}): {crit_orphans}"))
    else:
        findings.append((PASS, "critiques.method_id → methods FK valid"))

    # Required NOT NULL: name_ja, primary_source_url, mechanism
    null_name = c.execute("SELECT method_id FROM methods WHERE name_ja IS NULL OR name_ja = ''").fetchall()
    null_url = c.execute("SELECT method_id FROM methods WHERE primary_source_url IS NULL OR primary_source_url = ''").fetchall()
    null_mech = c.execute("SELECT method_id FROM methods WHERE mechanism IS NULL OR mechanism = ''").fetchall()
    if null_name:
        findings.append((FAIL, f"methods.name_ja NULL/empty: {len(null_name)} — {[r[0] for r in null_name]}"))
    else:
        findings.append((PASS, "methods.name_ja: no NULL/empty"))
    if null_url:
        findings.append((WARN, f"methods.primary_source_url NULL/empty: {len(null_url)} — {[r[0] for r in null_url]}"))
    else:
        findings.append((PASS, "methods.primary_source_url: no NULL/empty"))
    if null_mech:
        findings.append((WARN, f"methods.mechanism NULL/empty: {len(null_mech)} — {[r[0] for r in null_mech]}"))
    else:
        findings.append((PASS, "methods.mechanism: no NULL/empty"))

    # domain_code FK into domains
    domains = {r[0] for r in c.execute("SELECT code FROM domains").fetchall()}
    bad_dom = c.execute("SELECT method_id, domain_code FROM methods WHERE domain_code IS NOT NULL AND domain_code NOT IN (SELECT code FROM domains)").fetchall()
    if bad_dom:
        findings.append((FAIL, f"methods.domain_code not in domains: {bad_dom}"))
    else:
        findings.append((PASS, "methods.domain_code → domains FK valid"))

    null_dom = c.execute("SELECT method_id FROM methods WHERE domain_code IS NULL OR domain_code = ''").fetchall()
    if null_dom:
        findings.append((WARN, f"methods.domain_code NULL/empty: {len(null_dom)}"))

    return {"findings": findings, "method_ids": method_ids, "domains": domains}


# ---------- 2. Numerical sanity ----------

def check_numerical_sanity(c) -> dict:
    findings = []

    # era_start range
    bad_start = c.execute(
        "SELECT method_id, era_start FROM methods "
        "WHERE era_start IS NOT NULL AND (era_start < ? OR era_start > ?)",
        (ERA_YEAR_MIN, ERA_YEAR_MAX),
    ).fetchall()
    if bad_start:
        findings.append((FAIL, f"era_start outside [{ERA_YEAR_MIN}, {ERA_YEAR_MAX}]: {bad_start}"))
    else:
        findings.append((PASS, f"era_start values within [{ERA_YEAR_MIN}, {ERA_YEAR_MAX}]"))

    # era_start < era_end (or era_end == 9999)
    bad_order = c.execute(
        "SELECT method_id, era_start, era_end FROM methods "
        "WHERE era_start IS NOT NULL AND era_end IS NOT NULL "
        "AND era_end != ? AND era_end < era_start",
        (ERA_END_OPEN_SENTINEL,),
    ).fetchall()
    if bad_order:
        findings.append((FAIL, f"era_end < era_start (and era_end != 9999): {bad_order}"))
    else:
        findings.append((PASS, "era_start < era_end (or era_end == 9999)"))

    # era_end weird values: not 9999 but > 2030
    weird_end = c.execute(
        "SELECT method_id, era_end FROM methods "
        "WHERE era_end IS NOT NULL AND era_end != ? AND era_end > ?",
        (ERA_END_OPEN_SENTINEL, ERA_YEAR_MAX),
    ).fetchall()
    if weird_end:
        findings.append((WARN, f"era_end > {ERA_YEAR_MAX} and != 9999: {weird_end}"))
    else:
        findings.append((PASS, f"era_end either ≤ {ERA_YEAR_MAX} or == 9999 sentinel"))

    # evidence.value: extreme / negative
    neg_val = c.execute("SELECT evidence_id, value, metric_type FROM evidence WHERE value < 0").fetchall()
    if neg_val:
        findings.append((WARN, f"evidence.value negative: {neg_val}"))
    else:
        findings.append((PASS, "evidence.value has no negatives"))

    # absurd magnitudes: |value| > 1e7 (rough sanity)
    huge_val = c.execute("SELECT evidence_id, value, unit, metric_type FROM evidence WHERE ABS(value) > 1e7").fetchall()
    if huge_val:
        findings.append((WARN, f"evidence.value magnitude > 1e7: {huge_val}"))
    else:
        findings.append((PASS, "evidence.value within reasonable magnitude (|x| ≤ 1e7)"))

    # percent-type > 100 (informational, not necessarily wrong, e.g. cost up)
    pct_over_100 = c.execute(
        "SELECT evidence_id, metric_type, value, unit FROM evidence "
        "WHERE unit = '%' AND value > 100"
    ).fetchall()
    if pct_over_100:
        findings.append((WARN, f"% unit but value > 100 (review whether intended): {pct_over_100}"))

    # evidence.year sanity
    bad_year = c.execute(
        "SELECT evidence_id, year FROM evidence WHERE year IS NOT NULL AND (year < ? OR year > ?)",
        (ERA_YEAR_MIN, ERA_YEAR_MAX),
    ).fetchall()
    if bad_year:
        findings.append((WARN, f"evidence.year outside [{ERA_YEAR_MIN}, {ERA_YEAR_MAX}]: {bad_year}"))
    else:
        findings.append((PASS, f"evidence.year within [{ERA_YEAR_MIN}, {ERA_YEAR_MAX}]"))

    return {"findings": findings}


# ---------- 3. Genealogy structure ----------

def check_genealogy(c) -> dict:
    findings = []

    # self loop
    self_loops = c.execute(
        "SELECT rel_id, parent_method_id, child_method_id FROM genealogy "
        "WHERE parent_method_id = child_method_id"
    ).fetchall()
    if self_loops:
        findings.append((FAIL, f"self-loop in genealogy: {self_loops}"))
    else:
        findings.append((PASS, "no self-loops in genealogy"))

    # cycle detection (directed graph)
    edges = c.execute(
        "SELECT parent_method_id, child_method_id FROM genealogy "
        "WHERE parent_method_id IS NOT NULL AND child_method_id IS NOT NULL"
    ).fetchall()
    g = defaultdict(list)
    for p, ch in edges:
        g[p].append(ch)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(int)
    cycles = []

    def dfs(node, stack):
        color[node] = GRAY
        stack.append(node)
        for nb in g.get(node, []):
            if color[nb] == GRAY:
                # cycle: extract from stack
                idx = stack.index(nb)
                cycles.append(stack[idx:] + [nb])
            elif color[nb] == WHITE:
                dfs(nb, stack)
        stack.pop()
        color[node] = BLACK

    for n in list(g.keys()):
        if color[n] == WHITE:
            dfs(n, [])

    if cycles:
        # dedupe identical cycles
        unique_cycles = {tuple(c[:-1]) for c in cycles}
        findings.append((FAIL, f"genealogy cycles detected ({len(unique_cycles)}): {list(unique_cycles)[:5]}"))
    else:
        findings.append((PASS, "no cycles detected in genealogy DAG"))

    # year_transition within both eras
    rows = c.execute("""
        SELECT g.rel_id, g.parent_method_id, g.child_method_id, g.year_transition,
               mp.era_start, mp.era_end, mc.era_start, mc.era_end
        FROM genealogy g
        LEFT JOIN methods mp ON mp.method_id = g.parent_method_id
        LEFT JOIN methods mc ON mc.method_id = g.child_method_id
    """).fetchall()
    year_anomalies = []
    for rel_id, pid, cid, yt, pst, pen, cst, cen in rows:
        if yt is None:
            continue
        # year_transition should be >= parent.era_start (idea must exist before it can derive)
        # and >= child.era_start - small allowance
        # and <= max(parent.era_end_resolved, current year)
        if pst is not None and yt < pst:
            year_anomalies.append((rel_id, "year_transition before parent.era_start", yt, pst))
        if cst is not None and yt > cst + 5:
            # tolerate ±5 yr for derivation announcement vs concept emergence
            year_anomalies.append((rel_id, "year_transition >> child.era_start (+5y tolerance)", yt, cst))
    if year_anomalies:
        findings.append((WARN, f"year_transition era misalignment ({len(year_anomalies)}): {year_anomalies[:5]}"))
    else:
        findings.append((PASS, "year_transition consistent with parent/child era ranges"))

    return {"findings": findings}


# ---------- 4. Mechanism axis distribution ----------

def check_axes(c) -> dict:
    findings = []
    rows = c.execute(
        "SELECT mechanism_axis, COUNT(*) FROM methods GROUP BY mechanism_axis ORDER BY mechanism_axis"
    ).fetchall()
    dist = {axis: cnt for axis, cnt in rows}

    missing_axis = c.execute(
        "SELECT method_id, name_ja FROM methods WHERE mechanism_axis IS NULL OR mechanism_axis = ''"
    ).fetchall()
    if missing_axis:
        findings.append((WARN, f"methods missing mechanism_axis: {len(missing_axis)} — {[r[0] for r in missing_axis[:10]]}"))
    else:
        findings.append((PASS, "every method has a mechanism_axis assigned"))

    unexpected = [a for a in dist.keys() if a is not None and a not in EXPECTED_AXES]
    if unexpected:
        findings.append((FAIL, f"unexpected axis labels (outside M1-M6): {unexpected}"))
    else:
        findings.append((PASS, "all axes ∈ {M1, M2, M3, M4, M5, M6}"))

    missing_keys = EXPECTED_AXES - set(dist.keys())
    if missing_keys:
        findings.append((WARN, f"axes with zero methods: {sorted(missing_keys)}"))

    return {"findings": findings, "dist": dist}


# ---------- 5. URL liveness ----------

def collect_urls(c) -> list:
    urls = set()
    for q in [
        "SELECT primary_source_url FROM methods WHERE primary_source_url IS NOT NULL AND primary_source_url != ''",
        "SELECT source_url FROM evidence WHERE source_url IS NOT NULL AND source_url != ''",
        "SELECT source_url FROM critiques WHERE source_url IS NOT NULL AND source_url != ''",
    ]:
        for (u,) in c.execute(q).fetchall():
            urls.add(u.strip())
    return sorted(urls)


def check_url(url: str) -> tuple:
    """Return (url, status_code, ok, error_msg)."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept": "*/*",
    }
    # Try HEAD first; if 405 or no useful response, fallback to GET (read 0 bytes).
    try:
        req = urllib.request.Request(url, method="HEAD", headers=headers)
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=URL_TIMEOUT, context=ctx) as resp:
            code = resp.getcode()
            return (url, code, 200 <= code < 400, "")
    except urllib.error.HTTPError as e:
        if e.code in (400, 403, 405, 501):
            # retry with GET — many servers reject HEAD
            try:
                req = urllib.request.Request(url, method="GET", headers=headers)
                with urllib.request.urlopen(req, timeout=URL_TIMEOUT) as resp:
                    code = resp.getcode()
                    return (url, code, 200 <= code < 400, "")
            except urllib.error.HTTPError as e2:
                return (url, e2.code, False, f"HTTPError {e2.code}")
            except Exception as e2:
                return (url, None, False, f"GET failed: {type(e2).__name__}: {e2}")
        return (url, e.code, False, f"HTTPError {e.code}")
    except urllib.error.URLError as e:
        return (url, None, False, f"URLError: {e.reason}")
    except (socket.timeout, TimeoutError):
        return (url, None, False, "timeout")
    except Exception as e:
        return (url, None, False, f"{type(e).__name__}: {e}")


def check_url_liveness(c) -> dict:
    findings = []
    urls = collect_urls(c)
    results = []
    started = time.time()
    with ThreadPoolExecutor(max_workers=URL_PARALLELISM) as ex:
        futures = {ex.submit(check_url, u): u for u in urls}
        for fut in as_completed(futures):
            results.append(fut.result())
    duration = time.time() - started

    success = [r for r in results if r[2]]
    failure = [r for r in results if not r[2]]

    findings.append(
        (PASS if not failure else WARN,
         f"URL liveness: {len(success)}/{len(results)} OK "
         f"({len(failure)} failure, {duration:.1f}s @ {URL_PARALLELISM} parallel)")
    )

    return {"findings": findings, "results": results, "success": success, "failure": failure}


# ---------- 6. Hallucination signals ----------

_norm_re = re.compile(r"[\s　　・/／\-_,，。\.]+")


def _norm(s: str) -> str:
    if not s:
        return ""
    return _norm_re.sub("", s.lower())


def check_hallucinations(c) -> dict:
    findings = []

    # originator with multiple distinct era_starts (potentially conflicting facts)
    rows = c.execute("""
        SELECT originator, GROUP_CONCAT(DISTINCT era_start), COUNT(DISTINCT era_start), GROUP_CONCAT(method_id)
        FROM methods
        WHERE originator IS NOT NULL AND originator != '' AND originator != '-'
        GROUP BY originator
        HAVING COUNT(DISTINCT era_start) > 1
    """).fetchall()
    conflicting = []
    for orig, years, ndist, mids in rows:
        ys = sorted({int(y) for y in years.split(",") if y and y.lstrip("-").isdigit()})
        if not ys:
            continue
        # span > 30 years for the same originator is suspicious
        if ys[-1] - ys[0] > 30:
            conflicting.append((orig, ys, mids))
    if conflicting:
        findings.append((WARN, f"originators with era_start span > 30 years across multiple methods ({len(conflicting)}): {conflicting[:8]}"))
    else:
        findings.append((PASS, "no originator with era_start span > 30 years across multiple methods"))

    # fuzzy near-duplicate method names (ja/en)
    methods = c.execute("SELECT method_id, name_ja, name_en FROM methods").fetchall()
    near_dups = []
    n = len(methods)
    for i in range(n):
        mid_i, ja_i, en_i = methods[i]
        norm_ja_i = _norm(ja_i)
        norm_en_i = _norm(en_i or "")
        for j in range(i + 1, n):
            mid_j, ja_j, en_j = methods[j]
            ratio_ja = SequenceMatcher(None, norm_ja_i, _norm(ja_j)).ratio() if norm_ja_i and ja_j else 0
            ratio_en = SequenceMatcher(None, norm_en_i, _norm(en_j or "")).ratio() if norm_en_i and en_j else 0
            best = max(ratio_ja, ratio_en)
            if best >= FUZZY_NAME_THRESHOLD:
                near_dups.append((mid_i, mid_j, ja_i, ja_j, en_i, en_j, round(best, 3)))
    if near_dups:
        findings.append((WARN, f"potential near-duplicate method names (ratio ≥ {FUZZY_NAME_THRESHOLD}): {len(near_dups)} pair(s)"))
    else:
        findings.append((PASS, f"no near-duplicate method names (threshold {FUZZY_NAME_THRESHOLD})"))

    return {"findings": findings, "conflicting": conflicting, "near_dups": near_dups}


# ---------- Aggregator ----------

def aggregate(all_findings) -> tuple:
    p = sum(1 for s, _ in all_findings if s == PASS)
    w = sum(1 for s, _ in all_findings if s == WARN)
    f = sum(1 for s, _ in all_findings if s == FAIL)
    return p, w, f


# ---------- Markdown report ----------

def render_markdown(results: dict) -> str:
    schema = results["schema"]
    num = results["numerical"]
    gen = results["genealogy"]
    axes = results["axes"]
    urls = results["urls"]
    halu = results["hallucinations"]
    counts = results["counts"]

    all_findings = (
        schema["findings"] + num["findings"] + gen["findings"]
        + axes["findings"] + urls["findings"] + halu["findings"]
    )
    p, w, f = aggregate(all_findings)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def fmt_findings(findings):
        out = []
        for sev, msg in findings:
            out.append(f"| {sev} | {msg} |")
        return "\n".join(out)

    md = []
    md.append("# Cost-Down History DB (CDH-DB) v1.0 — 検証レポート")
    md.append("")
    md.append(f"_検証実施日時: {now}_  ")
    md.append(f"_対象DB: `{DB_PATH}`_  ")
    md.append(f"_検証スクリプト: `scripts/validate_db.py`_  ")
    md.append("")
    md.append("## 0. はじめに")
    md.append("")
    md.append(
        "本レポートは Cost-Down History DB v1.0 に対して、スキーマ整合性・数値妥当性・"
        "系譜構造・メカニズム軸分布・出典 URL 生存性・ハルシネーション疑いの 6 観点で実施した自動検証の結果である。"
        "検証は標準ライブラリのみで構成された `validate_db.py` により再現可能であり、URL 生存確認は "
        "`concurrent.futures.ThreadPoolExecutor` を用いて 24 並列で実行した。"
        "判定は PASS（合格）・WARN（要確認）・FAIL（要修正）の 3 段階で示し、"
        "数値の根拠はすべて SQLite クエリの結果として提示する。推測によるラベル付けは行わない。"
    )
    md.append("")

    md.append("## 1. サマリー")
    md.append("")
    md.append("検証は合計 " + f"{p + w + f}" + " 項目について行われ、その分布は以下の通りである。"
              " FAIL がゼロまたは少数であれば DB の構造的健全性は確保されており、"
              " WARN 群は今後のメンテナンスで優先的に確認すべき箇所として位置づけられる。")
    md.append("")
    md.append("| 区分 | 件数 |")
    md.append("|---|---|")
    md.append(f"| PASS | {p} |")
    md.append(f"| WARN | {w} |")
    md.append(f"| FAIL | {f} |")
    md.append("")

    md.append("テーブル別レコード数は以下の通りである。スキーマ定義どおりに "
              f"methods {counts['methods']} 件 / evidence {counts['evidence']} 件 / "
              f"genealogy {counts['genealogy']} 件 / critiques {counts['critiques']} 件 / "
              f"domains {counts['domains']} 件が格納されている。")
    md.append("")
    md.append("| テーブル | 行数 |")
    md.append("|---|---|")
    for k in ("methods", "evidence", "genealogy", "critiques", "domains"):
        md.append(f"| {k} | {counts[k]} |")
    md.append("")

    md.append("## 2. スキーマ整合性")
    md.append("")
    md.append(
        "method_id の一意性、外部キー参照（evidence・genealogy・critiques から methods への参照、"
        "methods から domains への参照）、必須フィールド（name_ja / primary_source_url / mechanism）の NULL チェックを実施した。"
        "PRIMARY KEY 制約によって ID 重複は構造的に防がれている一方、NOT NULL 制約が宣言されていない "
        "primary_source_url・mechanism は WARN 扱いとして個別レコード単位で確認している。"
    )
    md.append("")
    md.append("| 区分 | 内容 |")
    md.append("|---|---|")
    md.append(fmt_findings(schema["findings"]))
    md.append("")

    md.append("## 3. 数値妥当性")
    md.append("")
    md.append(
        "era_start が 1700–2030 の西暦範囲に収まること、era_start < era_end（era_end == 9999 は "
        "「現在まで継続」を表す sentinel として許容）、evidence.value に負値や非現実的な桁外れ "
        "（|x| > 1e7）が含まれないこと、% 単位で 100 を超える値の確認、evidence.year の範囲を検証した。"
    )
    md.append("")
    md.append("| 区分 | 内容 |")
    md.append("|---|---|")
    md.append(fmt_findings(num["findings"]))
    md.append("")

    md.append("## 4. 系譜構造（genealogy）")
    md.append("")
    md.append(
        "自己ループ（parent == child）と有向グラフ上の循環参照（A→B→A）を深さ優先探索で検出した。"
        "また year_transition（派生年）が parent の era_start 以降、かつ child の era_start を概ね超えない"
        "（±5 年の許容）ことを確認している。理論の派生は常に発祥より後に起こるはずであり、"
        "この時系列の単調性は系譜データの最低限の整合条件である。"
    )
    md.append("")
    md.append("| 区分 | 内容 |")
    md.append("|---|---|")
    md.append(fmt_findings(gen["findings"]))
    md.append("")

    md.append("## 5. メカニズム軸の分布")
    md.append("")
    md.append(
        "本 DB は 6 つのメカニズム軸（M1: 標準化と分業 / M2: 自動化と機械化 / M3: 規模・経験曲線 / "
        "M4: 情報・最適化 / M5: 外部化・市場化 / M6: 制度・会計）を備える。"
        "各軸の手法数を以下に示し、軸が未割当のレコードや想定外の軸ラベルの混入を検出した。"
    )
    md.append("")
    md.append("| 軸 | 手法数 |")
    md.append("|---|---|")
    for axis in sorted(axes["dist"].keys(), key=lambda x: (x is None, x)):
        md.append(f"| {axis if axis is not None else '(NULL)'} | {axes['dist'][axis]} |")
    md.append("")
    md.append("| 区分 | 内容 |")
    md.append("|---|---|")
    md.append(fmt_findings(axes["findings"]))
    md.append("")

    md.append("## 6. 出典 URL 生存確認")
    md.append("")
    md.append(
        "methods.primary_source_url / evidence.source_url / critiques.source_url を重複排除した URL 集合に対して、"
        "Mozilla 互換 User-Agent で HTTP HEAD を発行し、HEAD が拒否される場合は GET で再試行している。"
        "200 / 301 / 302 などの 2xx・3xx を success、404 / 5xx ほかの 4xx・5xx および接続エラーを failure と判定する。"
        "瞬間的なネットワーク状態に左右されるため、failure 群は手動再確認の対象として記載する。"
    )
    md.append("")
    md.append("| 区分 | 内容 |")
    md.append("|---|---|")
    md.append(fmt_findings(urls["findings"]))
    md.append("")
    if urls["failure"]:
        md.append("### 6.1. 失敗 URL 一覧")
        md.append("")
        md.append("| URL | ステータス | エラー |")
        md.append("|---|---|---|")
        for u, code, _ok, err in sorted(urls["failure"], key=lambda r: (str(r[1]), r[0])):
            md.append(f"| {u} | {code if code is not None else '-'} | {err} |")
        md.append("")

    md.append("## 7. ハルシネーション疑い")
    md.append("")
    md.append(
        "1 人の originator が異なる era_start で複数登場し、その範囲が 30 年を超えるケースは、"
        "発祥年の取り違えあるいは人名同定エラーの兆候として WARN 扱いとする。"
        "また method 名の正規化文字列に対する SequenceMatcher 比率 0.90 以上のペアを近似重複として抽出した。"
        "いずれも自動判定にとどめ、人手による発祥年・名称の最終確認を前提とする。"
    )
    md.append("")
    md.append("| 区分 | 内容 |")
    md.append("|---|---|")
    md.append(fmt_findings(halu["findings"]))
    md.append("")
    if halu["conflicting"]:
        md.append("### 7.1. era_start が広く分散した originator")
        md.append("")
        md.append("| originator | era_start 群 | 関連 method_id |")
        md.append("|---|---|---|")
        for orig, years, mids in halu["conflicting"]:
            md.append(f"| {orig} | {years} | {mids} |")
        md.append("")
    if halu["near_dups"]:
        md.append("### 7.2. 類似名 method ペア（ratio ≥ 0.90）")
        md.append("")
        md.append("| method_id (A) | method_id (B) | name_ja (A) | name_ja (B) | name_en (A) | name_en (B) | ratio |")
        md.append("|---|---|---|---|---|---|---|")
        for a, b, ja, jb, ea, eb, r in halu["near_dups"]:
            md.append(f"| {a} | {b} | {ja} | {jb} | {ea or ''} | {eb or ''} | {r} |")
        md.append("")

    md.append("## 8. 修正提案")
    md.append("")
    proposals = []
    # NULL primary_source_url
    null_url_count = sum(1 for s, m in schema["findings"] if "primary_source_url NULL/empty" in m and s == WARN)
    null_mech_count = sum(1 for s, m in schema["findings"] if "mechanism NULL/empty" in m and s == WARN)
    if null_url_count:
        proposals.append(
            "primary_source_url が空のレコードについては、`build_db.py` の該当手法に一次資料 URL を補完するか、"
            "URL が確定しない場合は備考欄に「未確認」と明示することを推奨する。"
        )
    if null_mech_count:
        proposals.append(
            "mechanism が空のレコードについては、当該手法の「なぜコストが下がるのか」を 1 文で記述することを推奨する。"
        )
    if urls["failure"]:
        proposals.append(
            "URL 失敗群は Wayback Machine（https://web.archive.org/）の保存版に差し替えるか、"
            "一次資料（書籍・学術論文 DOI）への置換を検討する。"
        )
    if any(s == FAIL for s, _ in gen["findings"]):
        proposals.append(
            "genealogy の構造的エラーは optimizing inference の前提を崩すため、最優先で修正する。"
        )
    if halu["conflicting"]:
        proposals.append(
            "同一 originator の era_start 大幅乖離は、同名異人の混同または初出文献の取り違えの可能性があるため、"
            "原典への突き合わせを行う。"
        )
    if halu["near_dups"]:
        proposals.append(
            "類似名ペアは（a）同義表記揺れの統合、または（b）意図的な区別を明示するための name_en 補強を検討する。"
        )
    if not proposals:
        proposals.append("特筆すべき修正提案は検出されなかった。次回バージョンアップ時の差分検証で継続観察する。")
    for i, p in enumerate(proposals, 1):
        md.append(f"{i}. {p}")
    md.append("")

    md.append("## 9. 再現方法")
    md.append("")
    md.append(
        "本検証は以下の単一コマンドで完全に再現可能である。標準ライブラリのみを使用しているため、"
        "追加の pip インストールは不要である。"
    )
    md.append("")
    md.append("```bash")
    md.append("python3 scripts/validate_db.py")
    md.append("```")
    md.append("")
    md.append("---")
    md.append("")
    md.append("_本レポートは `scripts/validate_db.py` により自動生成された。設定値は同スクリプト冒頭の定数で調整可能である。_")
    md.append("")
    return "\n".join(md)


# ---------- Main ----------

def main():
    if not DB_PATH.exists():
        print(f"ERROR: DB not found at {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    print(f"[CDH-DB validator] target = {DB_PATH}")
    c = conn().cursor()

    counts = {
        "methods": c.execute("SELECT COUNT(*) FROM methods").fetchone()[0],
        "evidence": c.execute("SELECT COUNT(*) FROM evidence").fetchone()[0],
        "genealogy": c.execute("SELECT COUNT(*) FROM genealogy").fetchone()[0],
        "critiques": c.execute("SELECT COUNT(*) FROM critiques").fetchone()[0],
        "domains": c.execute("SELECT COUNT(*) FROM domains").fetchone()[0],
    }
    print(f"  counts: {counts}")

    print("[1/6] schema integrity ...")
    schema = check_schema_integrity(c)
    print("[2/6] numerical sanity ...")
    numerical = check_numerical_sanity(c)
    print("[3/6] genealogy ...")
    genealogy = check_genealogy(c)
    print("[4/6] mechanism axes ...")
    axes = check_axes(c)
    print("[5/6] URL liveness ...")
    urls = check_url_liveness(c)
    print("[6/6] hallucination signals ...")
    hallucinations = check_hallucinations(c)

    results = {
        "counts": counts,
        "schema": schema,
        "numerical": numerical,
        "genealogy": genealogy,
        "axes": axes,
        "urls": urls,
        "hallucinations": hallucinations,
    }

    all_findings = (
        schema["findings"] + numerical["findings"] + genealogy["findings"]
        + axes["findings"] + urls["findings"] + hallucinations["findings"]
    )
    p, w, f = aggregate(all_findings)
    print(f"\nSummary: PASS={p}  WARN={w}  FAIL={f}")
    print(f"  URL success={len(urls['success'])} / total={len(urls['success']) + len(urls['failure'])}")

    md = render_markdown(results)
    REPORT_PATH.write_text(md, encoding="utf-8")
    print(f"\nReport written to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
