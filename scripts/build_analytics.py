#!/usr/bin/env python3
"""Generate analytics dashboard with charts + cross-cuts."""

import sqlite3
import html
import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "cdh.sqlite"
OUT = ROOT / "docs" / "analytics.html"

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
c = conn.cursor()

methods = [dict(r) for r in c.execute("SELECT * FROM methods")]
evidence = [dict(r) for r in c.execute("SELECT * FROM evidence")]
genealogy = [dict(r) for r in c.execute("SELECT * FROM genealogy")]
critiques = [dict(r) for r in c.execute("SELECT * FROM critiques")]
domains = {r["code"]: dict(r) for r in c.execute("SELECT * FROM domains")}

MECH = {"M1": "労働分解", "M2": "学習効果", "M3": "品質組込", "M4": "設計コスト織込", "M5": "境界解体", "M6": "情報知能化"}

# Statistics
total = len(methods)
by_domain = Counter(m["domain_code"] for m in methods)
by_axis = Counter(m["mechanism_axis"] for m in methods)
by_status = Counter(m["status"] for m in methods)
by_country = Counter(m["origin_country"] for m in methods)
by_decade = Counter((m["era_start"] // 10) * 10 for m in methods if m.get("era_start"))

decades_sorted = sorted(by_decade.keys())
min_dec, max_dec = min(decades_sorted), max(decades_sorted)

# Axis × Domain heatmap
heatmap = defaultdict(lambda: defaultdict(int))
for m in methods:
    if m.get("mechanism_axis") and m.get("domain_code"):
        heatmap[m["mechanism_axis"]][m["domain_code"]] += 1

# Evidence by metric type
ev_by_metric = Counter(e["metric_type"] for e in evidence)

# Genealogy by rel_type
gen_by_type = Counter(g["rel_type"] for g in genealogy)

# Top critiques (by date)
crt_sorted = sorted(critiques, key=lambda x: x["year"] or 0)

# Top-evidence cost reductions
big_savings = sorted(
    [e for e in evidence if e["metric_type"] and "cost" in e["metric_type"]],
    key=lambda e: e["value"] or 0, reverse=True
)[:10]


def esc(s):
    return html.escape(str(s)) if s is not None else ""


def bar(label, value, max_value, color="var(--accent-warm)"):
    pct = (value / max_value * 100) if max_value else 0
    return f'''
    <div class="bar-row">
        <div class="bar-label">{esc(label)}</div>
        <div class="bar-track"><div class="bar-fill" style="width:{pct:.1f}%; background:{color}"></div></div>
        <div class="bar-value">{value}</div>
    </div>'''


# Build sections
max_domain = max(by_domain.values())
domain_section = "".join(
    bar(f"{code} {domains[code]['name_ja']}", v, max_domain)
    for code, v in sorted(by_domain.items(), key=lambda x: -x[1])
)

max_axis = max(by_axis.values()) if by_axis else 1
axis_section = "".join(
    bar(f"{code} {MECH.get(code, '?')}", v, max_axis)
    for code, v in sorted(by_axis.items(), key=lambda x: x[0] if x[0] else "")
    if code
)

# Decade timeline
decade_max = max(by_decade.values())
decade_section = "".join(
    bar(f"{d}年代" if d >= 1900 else f"{d}年代（18-19c）", by_decade[d], decade_max)
    for d in decades_sorted
)

# Country distribution
max_country = max(by_country.values())
country_section = "".join(
    bar(esc(code), v, max_country)
    for code, v in sorted(by_country.items(), key=lambda x: -x[1])[:15]
    if code
)

# Heatmap
heatmap_rows = ""
all_domains = list(domains.keys())
heatmap_rows += "<tr><th></th>" + "".join(f'<th class="hcol">{d}</th>' for d in all_domains) + "</tr>"
heatmap_max = max(
    (heatmap[a][d] for a in MECH for d in all_domains),
    default=1
)
for axis_code in MECH:
    cells = ""
    for d in all_domains:
        v = heatmap[axis_code][d]
        intensity = (v / heatmap_max) if heatmap_max else 0
        cells += f'<td class="hcell" style="background:rgba(204,20,0,{intensity:.2f})" title="{axis_code}×{d}: {v}">{v if v else ""}</td>'
    heatmap_rows += f'<tr><th class="hrow">{axis_code} {MECH[axis_code]}</th>{cells}</tr>'

# Big savings table
savings_rows = ""
method_map = {m["method_id"]: m for m in methods}
for e in big_savings:
    m = method_map.get(e["method_id"], {})
    savings_rows += f'''
    <tr>
        <td>{esc(m.get("name_ja", "?"))}</td>
        <td class="num">{e["value"]:.1f}</td>
        <td>{esc(e["unit"])}</td>
        <td>{esc(e["company_case"])}</td>
        <td>{e["year"] or "?"}</td>
        <td><a href="{esc(e["source_url"])}" target="_blank">出典</a></td>
    </tr>'''

# Critiques table
critique_rows = ""
for cr in crt_sorted:
    m = method_map.get(cr["method_id"], {})
    critique_rows += f'''
    <tr>
        <td>{esc(m.get("name_ja", "?"))}</td>
        <td>{esc(cr["critic"])}</td>
        <td>{cr["year"] or "?"}</td>
        <td>{esc(cr["critique_type"])}</td>
        <td>{esc(cr["description"])}</td>
    </tr>'''

# Genealogy network (simplified as a list)
gen_chain_rows = ""
for g in genealogy[:30]:
    p = method_map.get(g["parent_method_id"], {})
    ch = method_map.get(g["child_method_id"], {})
    gen_chain_rows += f'''
    <tr>
        <td>{esc(p.get("name_ja", "?"))} <span class="met-id-sm">{esc(g["parent_method_id"])}</span></td>
        <td class="rel-arrow">→ {esc(g["rel_type"])} →</td>
        <td>{esc(ch.get("name_ja", "?"))} <span class="met-id-sm">{esc(g["child_method_id"])}</span></td>
        <td>{g["year_transition"] or "?"}</td>
    </tr>'''

# Verification status
verify_status = Counter(m["verification"] for m in methods)
verify_section = "".join(
    bar(esc(k), v, total) for k, v in verify_status.items()
)

CSS = '''
:root {
    --bg: #FFFFFF; --card: #FFFFFF; --card-hover: #F7F7F5;
    --accent: #121212; --accent-soft: #555;
    --accent-warm: #CC1400; --accent-warm-soft: #B01200; --accent-muted: rgba(204,20,0,0.06);
    --text: #121212; --text-secondary: #555; --text-muted: #6B6B6B;
    --border: #D9D9D9; --border-light: #EEE;
    --surface: #F7F7F5;
    --font: "Noto Sans JP", "Hiragino Sans", -apple-system, sans-serif;
    --font-serif: "Noto Serif JP", "Hiragino Mincho ProN", Georgia, serif;
}
[data-theme="dark"] {
    --bg: #121212; --card: #1A1A1A; --card-hover: #222;
    --accent: #E0E0E0; --accent-warm: #FF4030;
    --accent-muted: rgba(255,64,48,0.10);
    --text: #E0E0E0; --text-secondary: #AAA; --text-muted: #8A8A8A;
    --border: #333; --border-light: #2A2A2A;
    --surface: #1A1A1A;
}
* { box-sizing: border-box; }
body {
    margin: 0; padding: 0; background: var(--bg); color: var(--text);
    font-family: var(--font); font-feature-settings: "palt";
    line-height: 1.7; letter-spacing: 0.025em;
}
.top-bar {
    position: fixed; top: 0; left: 0; right: 0;
    height: 48px; z-index: 100;
    background: var(--bg);
    border-top: 3px solid #121212;
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 20px;
}
[data-theme="dark"] .top-bar { border-top: 3px solid var(--accent-warm); }
.brand {
    font-size: 14px; font-weight: 700;
    color: var(--accent-warm); letter-spacing: 0.05em;
}
.brand-sub { color: var(--text-secondary); font-weight: 400; margin-left: 8px; font-size: 12px; }
.nav-link {
    color: var(--text-secondary); text-decoration: none; margin-right: 16px;
    font-size: 13px;
}
.nav-link:hover { color: var(--accent-warm); }
.theme-toggle {
    background: transparent; border: 1px solid var(--border);
    color: var(--text); padding: 4px 12px; cursor: pointer;
    font-size: 12px; border-radius: 2px;
}
.layout { padding-top: 72px; padding-bottom: 96px; }
.main { max-width: 1100px; margin: 0 auto; padding: 0 32px; }
.hero { margin-bottom: 48px; }
.hero h1 {
    font-family: var(--font-serif);
    font-size: 30px; font-weight: 700; margin: 0 0 12px;
}
.hero .subtitle { font-size: 15px; color: var(--text-secondary); }
.stats-row {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px; margin-bottom: 40px;
}
.stat-card {
    padding: 16px; background: var(--surface);
    border-left: 3px solid var(--accent-warm); border-radius: 2px;
}
.stat-label { font-size: 11px; color: var(--text-secondary); letter-spacing: 0.1em; text-transform: uppercase; }
.stat-value { font-size: 28px; font-weight: 700; color: var(--accent-warm); margin-top: 4px; }
.section {
    margin-bottom: 56px; padding-bottom: 32px;
    border-bottom: 1px solid var(--border-light);
}
.section h2 {
    font-family: var(--font-serif);
    font-size: 22px; margin: 0 0 20px;
    padding-bottom: 8px; border-bottom: 2px solid var(--accent-warm);
}
.section h3 { font-size: 16px; margin: 28px 0 12px; }
.section p { font-family: var(--font-serif); margin: 0 0 16px; }
.bar-row {
    display: grid; grid-template-columns: 200px 1fr 50px;
    gap: 12px; align-items: center; padding: 4px 0;
    font-size: 13px;
}
.bar-track {
    height: 18px; background: var(--surface);
    border-radius: 2px; overflow: hidden;
}
.bar-fill { height: 100%; transition: width 0.3s; }
.bar-label { color: var(--text-secondary); }
.bar-value { text-align: right; font-family: "SF Mono", monospace; font-size: 13px; }
.heatmap {
    border-collapse: collapse; margin-top: 16px; font-size: 12px;
}
.heatmap th, .heatmap td {
    padding: 8px 10px; text-align: center;
    border: 1px solid var(--border-light);
}
.heatmap .hrow {
    text-align: left; background: var(--surface);
    font-size: 12px; padding: 8px 12px;
    white-space: nowrap;
}
.heatmap .hcol { background: var(--surface); }
.heatmap .hcell {
    min-width: 36px; color: var(--accent-warm); font-weight: 700;
}
table.data {
    width: 100%; border-collapse: collapse;
    font-size: 13px; margin-top: 12px;
}
table.data th, table.data td {
    padding: 8px 12px; text-align: left;
    border-bottom: 1px solid var(--border-light);
}
table.data th {
    background: var(--surface); font-weight: 700;
    font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase;
}
table.data .num { text-align: right; font-family: "SF Mono", monospace; }
.met-id-sm {
    font-family: "SF Mono", monospace; font-size: 10px;
    color: var(--text-muted); margin-left: 6px;
}
.rel-arrow { text-align: center; color: var(--accent-warm); font-size: 11px; }
.legend { font-size: 12px; color: var(--text-secondary); margin-top: 8px; }
a { color: var(--accent-warm); }
@media (max-width: 800px) {
    .bar-row { grid-template-columns: 140px 1fr 40px; }
    .main { padding: 0 16px; }
}
'''

JS = '''
const root = document.documentElement;
const saved = localStorage.getItem("cdh-theme");
if (saved) root.setAttribute("data-theme", saved);
document.getElementById("themeBtn").addEventListener("click", () => {
    const cur = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", cur);
    localStorage.setItem("cdh-theme", cur);
});
'''

HTML_TPL = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CDH Analytics — 分析ダッシュボード</title>
<link rel="icon" href="https://esse-sense.com/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&family=Noto+Serif+JP:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<nav class="top-bar">
    <div>
        <span class="brand">CDH-DB</span>
        <span class="brand-sub">Analytics</span>
    </div>
    <div>
        <a href="index.html" class="nav-link">← 一覧へ</a>
        <button id="themeBtn" class="theme-toggle">ダーク／ライト</button>
    </div>
</nav>
<div class="layout">
<main class="main">
    <header class="hero">
        <h1>CDH 分析ダッシュボード</h1>
        <p class="subtitle">15領域・158手法・26実証・27系譜・9批判を多角的に可視化。Wattの遠心調速機(1788)から生成AI自動化(2022)までの230年史。</p>
    </header>

    <div class="stats-row">
        <div class="stat-card"><div class="stat-label">手法</div><div class="stat-value">{total}</div></div>
        <div class="stat-card"><div class="stat-label">実証データ</div><div class="stat-value">{len(evidence)}</div></div>
        <div class="stat-card"><div class="stat-label">系譜関係</div><div class="stat-value">{len(genealogy)}</div></div>
        <div class="stat-card"><div class="stat-label">批判・限界</div><div class="stat-value">{len(critiques)}</div></div>
        <div class="stat-card"><div class="stat-label">領域</div><div class="stat-value">{len(domains)}</div></div>
        <div class="stat-card"><div class="stat-label">期間</div><div class="stat-value">{max_dec - min_dec + 10}年</div></div>
    </div>

    <section class="section">
        <h2>1. ドメイン別分布</h2>
        <p>11ドメインそれぞれの手法登録数。製造業（MFG）・ソフトウェア（SW）・エンジニアリング設計（ENG）が三大領域。</p>
        {domain_section}
    </section>

    <section class="section">
        <h2>2. メカニズム軸別分布</h2>
        <p>6つのメカニズム軸（M1-M6）への帰属分布。コストダウンの原理を「労働分解／学習効果／品質組込／設計コスト織込／境界解体／情報知能化」の6軸で整理。</p>
        {axis_section}
    </section>

    <section class="section">
        <h2>3. 時代別分布</h2>
        <p>10年区切りでの手法発祥年分布。20世紀後半（1950-2000年代）に集中。21世紀（特に2010s-2020s）のAI/クラウド手法の比重が増加。</p>
        {decade_section}
    </section>

    <section class="section">
        <h2>4. 発祥国別分布</h2>
        <p>上位15国（地域）の手法数。USA・JPN が二大プレイヤー。次いで欧州・台湾・中国・北欧。インド・新興国の比重は Phase 2 で増強予定。</p>
        {country_section}
    </section>

    <section class="section">
        <h2>5. ヒートマップ — 軸×ドメイン</h2>
        <p>どのメカニズム軸がどのドメインに集中しているかの俯瞰。色が濃いほど手法数が多い。M1労働分解は製造業、M2学習効果はエネルギー・半導体、M5境界解体はソフトウェアに集中する傾向。</p>
        <table class="heatmap">
            {heatmap_rows}
        </table>
        <p class="legend">数値=手法数。空白セルは未登録（カバーすべき領域）。</p>
    </section>

    <section class="section">
        <h2>6. コスト削減実証 TOP10</h2>
        <p>登録済み実証データから削減効果の大きい順。倍率や%は出典の単位に依存（700倍=Swanson's Law、99%=Li-ion、65%=Ford等）。</p>
        <table class="data">
            <thead><tr><th>手法</th><th class="num">削減値</th><th>単位</th><th>事例</th><th>年</th><th>出典</th></tr></thead>
            <tbody>{savings_rows}</tbody>
        </table>
    </section>

    <section class="section">
        <h2>7. 批判・限界マッピング</h2>
        <p>9件の登録批判は、年代順に並べると「労働疎外（1974 Braverman）→ コア能力喪失（2012 Kodak）→ イノベーション阻害（2007 3M）→ 学習しない技術（2024 CCS）→ AI品質劣化（2025 GitClear）」と展開。コストダウンの代償が時代ごとに変化している。</p>
        <table class="data">
            <thead><tr><th>手法</th><th>批判者</th><th>年</th><th>類型</th><th>内容</th></tr></thead>
            <tbody>{critique_rows}</tbody>
        </table>
    </section>

    <section class="section">
        <h2>8. 派生系譜（抜粋）</h2>
        <p>27件の系譜関係から代表30件。Taylor→Ford→TPS→Lean→Agile→Lean Startup の流れ、Wright→Moore→Swanson→Li-ion の学習曲線系譜、GNU→Linux→AWS→Docker→Kubernetes のOSS進化系譜が確認できる。</p>
        <table class="data">
            <thead><tr><th>派生元</th><th>関係</th><th>派生先</th><th>年</th></tr></thead>
            <tbody>{gen_chain_rows}</tbody>
        </table>
    </section>

    <section class="section">
        <h2>9. 検証ステータス</h2>
        <p>各手法の検証ステータス（verified / unverified / requires_review）の分布。一次資料URLの生存確認は別途 validate_db.py で実施。</p>
        {verify_section}
    </section>

    <section class="section">
        <h2>10. 横断的発見</h2>
        <h3>10.1 学習曲線は媒体を越えて成立</h3>
        <p>航空機（Wright 1936）、半導体（Moore 1965）、太陽光（Swanson 2012）、DNA（Carlson 2003）、リチウムイオン電池（2010s）—— 媒体が異なっても累積生産倍増あたり10-30%減という規則性が成立する。Lafond et al. 2018 では51製品で実証。</p>
        <h3>10.2 失敗例がメカニズム理解の鍵</h3>
        <p>GM Saturn $45B 投資→市場シェア 1%増加→破産（2009）／3M Six Sigma→特許申請数低下／CCS 40年で学習率ゼロ／Kodak IT外部委託→コア能力喪失→破産（2012）。「コストを下げた結果、競争力を失った」事例の体系化が重要。</p>
        <h3>10.3 リバウンド（揺り戻し）の周期性</h3>
        <p>大量生産 ↔ 多品種少量（セル生産）／グローバル化 ↔ リショアリング・フレンドショアリング／モノリス → マイクロサービス → モノリス回帰（42%）／集中DC ↔ 分散ラストワンマイル／標準化 ↔ マスカスタマイゼーション。コストダウン手法には周期的な「逆転」が観察される。</p>
        <h3>10.4 90年史の累積効果</h3>
        <p>1900年代の馬車製造から2024年のスマートフォン1台が世界全体の計算機を凌駕する性能まで、複数領域で7桁以上のコスト低減が累積している。これは単一手法ではなく、6メカニズム軸が並行作用した結果である。</p>
    </section>

    <section class="section">
        <h2>11. 次工程</h2>
        <p>Phase 2 拡張計画は <code>COVERAGE_AND_EXPANSION.md</code> 参照（カバー率推論と未網羅領域リスト、優先度順の追加候補50-200手法）。検証結果は <code>VALIDATION_REPORT.md</code> 参照（一次URL生存確認・スキーマ整合性・ハルシネーション疑い検査）。</p>
    </section>

</main>
</div>
<script>{JS}</script>
</body>
</html>
'''

OUT.write_text(HTML_TPL, encoding="utf-8")
print(f"Analytics generated: {OUT}")
print(f"Size: {OUT.stat().st_size} bytes")
conn.close()
