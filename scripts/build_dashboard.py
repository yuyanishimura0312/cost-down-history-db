#!/usr/bin/env python3
"""Generate Cost-Down History DB dashboard HTML (textbook.html style + 赤白CI)."""

import sqlite3
import html
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "cdh.sqlite"
OUT = ROOT / "docs" / "index.html"
OUT.parent.mkdir(exist_ok=True)

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
c = conn.cursor()

methods = [dict(r) for r in c.execute("SELECT * FROM methods ORDER BY era_start, method_id")]
evidence_by_m = defaultdict(list)
for r in c.execute("SELECT * FROM evidence"):
    evidence_by_m[r["method_id"]].append(dict(r))
critiques_by_m = defaultdict(list)
for r in c.execute("SELECT * FROM critiques"):
    critiques_by_m[r["method_id"]].append(dict(r))
genealogy = [dict(r) for r in c.execute("SELECT * FROM genealogy")]
domains = {r["code"]: dict(r) for r in c.execute("SELECT * FROM domains")}

# Group methods by region (using era + domain heuristic for chapter mapping)
REGIONS = [
    ("R01", "科学的管理法・フォーディズム（1900-1950）", ["CDH-MET-0001", "CDH-MET-0002", "CDH-MET-0003", "CDH-MET-0004", "CDH-MET-0005", "CDH-MET-0006"]),
    ("R02", "TPS・リーン・JIT（1950-1990）", ["CDH-MET-0010", "CDH-MET-0011", "CDH-MET-0012", "CDH-MET-0013", "CDH-MET-0014", "CDH-MET-0015", "CDH-MET-0016", "CDH-MET-0017", "CDH-MET-0018", "CDH-MET-0019"]),
    ("R03", "TQM・カイゼン・シックスシグマ", ["CDH-MET-0020", "CDH-MET-0021", "CDH-MET-0022", "CDH-MET-0023", "CDH-MET-0024", "CDH-MET-0025", "CDH-MET-0026", "CDH-MET-0027", "CDH-MET-0028", "CDH-MET-0029", "CDH-MET-0030", "CDH-MET-0031"]),
    ("R04", "価値工学・原価企画", ["CDH-MET-0040", "CDH-MET-0041", "CDH-MET-0042", "CDH-MET-0043", "CDH-MET-0044", "CDH-MET-0045", "CDH-MET-0046", "CDH-MET-0047", "CDH-MET-0048", "CDH-MET-0049", "CDH-MET-0050"]),
    ("R05", "管理会計・原価計算", ["CDH-MET-0060", "CDH-MET-0061", "CDH-MET-0062", "CDH-MET-0063", "CDH-MET-0064", "CDH-MET-0065", "CDH-MET-0066", "CDH-MET-0067", "CDH-MET-0068"]),
    ("R06", "アウトソーシング・SCM", ["CDH-MET-0080", "CDH-MET-0081", "CDH-MET-0082", "CDH-MET-0083", "CDH-MET-0084", "CDH-MET-0085", "CDH-MET-0086"]),
    ("R07", "ムーア則・学習曲線", ["CDH-MET-0090", "CDH-MET-0091", "CDH-MET-0092", "CDH-MET-0093", "CDH-MET-0094", "CDH-MET-0095", "CDH-MET-0096", "CDH-MET-0097", "CDH-MET-0098", "CDH-MET-0099"]),
    ("R08", "モジュラー設計・プラットフォーム", ["CDH-MET-0110", "CDH-MET-0111", "CDH-MET-0112", "CDH-MET-0113", "CDH-MET-0114", "CDH-MET-0115", "CDH-MET-0116", "CDH-MET-0117", "CDH-MET-0118", "CDH-MET-0119", "CDH-MET-0120", "CDH-MET-0121", "CDH-MET-0122"]),
    ("R09", "ソフトウェア開発手法", ["CDH-MET-0140", "CDH-MET-0141", "CDH-MET-0142", "CDH-MET-0143", "CDH-MET-0144", "CDH-MET-0145", "CDH-MET-0146", "CDH-MET-0147", "CDH-MET-0148", "CDH-MET-0149", "CDH-MET-0150", "CDH-MET-0151", "CDH-MET-0152", "CDH-MET-0153", "CDH-MET-0154"]),
    ("R10", "OSS・クラウド", ["CDH-MET-0170", "CDH-MET-0171", "CDH-MET-0172", "CDH-MET-0173", "CDH-MET-0174", "CDH-MET-0175", "CDH-MET-0176", "CDH-MET-0177", "CDH-MET-0178", "CDH-MET-0179", "CDH-MET-0180", "CDH-MET-0181", "CDH-MET-0182"]),
    ("R11", "エネルギー学習曲線", ["CDH-MET-0200", "CDH-MET-0201", "CDH-MET-0202", "CDH-MET-0203", "CDH-MET-0204", "CDH-MET-0205", "CDH-MET-0206", "CDH-MET-0207"]),
    ("R12", "建設プレハブ・モジュラー", ["CDH-MET-0220", "CDH-MET-0221", "CDH-MET-0222", "CDH-MET-0223", "CDH-MET-0224", "CDH-MET-0225", "CDH-MET-0226", "CDH-MET-0227", "CDH-MET-0228", "CDH-MET-0229", "CDH-MET-0230"]),
    ("R13", "R&D効率化", ["CDH-MET-0240", "CDH-MET-0241", "CDH-MET-0242", "CDH-MET-0243", "CDH-MET-0244", "CDH-MET-0245", "CDH-MET-0246", "CDH-MET-0247"]),
    ("R14", "物流・コンテナ化", ["CDH-MET-0260", "CDH-MET-0261", "CDH-MET-0262", "CDH-MET-0263", "CDH-MET-0264", "CDH-MET-0265", "CDH-MET-0266", "CDH-MET-0267", "CDH-MET-0268", "CDH-MET-0269"]),
    ("R15", "自動化・ロボティクス", ["CDH-MET-0280", "CDH-MET-0281", "CDH-MET-0282", "CDH-MET-0283", "CDH-MET-0284", "CDH-MET-0285", "CDH-MET-0286", "CDH-MET-0287", "CDH-MET-0288", "CDH-MET-0289", "CDH-MET-0290", "CDH-MET-0291", "CDH-MET-0292", "CDH-MET-0293", "CDH-MET-0294"]),
]

methods_by_id = {m["method_id"]: m for m in methods}

MECHANISM_AXES = {
    "M1": "労働の分解と再構成",
    "M2": "学習効果と規模効果",
    "M3": "品質の事前組込み",
    "M4": "設計時のコスト織込み",
    "M5": "境界の解体と再結合",
    "M6": "情報の自動化と知能化",
}


def esc(s):
    return html.escape(str(s)) if s else ""


def fmt_year(y):
    if not y or y == 9999:
        return "現在"
    return str(y)


def method_card(m):
    evs = evidence_by_m.get(m["method_id"], [])
    crts = critiques_by_m.get(m["method_id"], [])
    ev_html = ""
    if evs:
        rows = "".join(
            f'<li><span class="metric">{esc(e["metric_type"])}</span>: <strong>{esc(e["value"])} {esc(e["unit"])}</strong> '
            f'<span class="case">（{esc(e["company_case"])}, {fmt_year(e["year"])}）</span> '
            f'<a href="{esc(e["source_url"])}" target="_blank" rel="noopener">出典</a></li>'
            for e in evs
        )
        ev_html = f'<div class="evidence"><div class="ev-label">数値実証</div><ul>{rows}</ul></div>'
    crt_html = ""
    if crts:
        rows = "".join(
            f'<li><strong>{esc(cr["critic"])}（{fmt_year(cr["year"])}）</strong>: {esc(cr["description"])} '
            f'<a href="{esc(cr["source_url"])}" target="_blank" rel="noopener">出典</a></li>'
            for cr in crts
        )
        crt_html = f'<div class="critique"><div class="ev-label">批判・限界</div><ul>{rows}</ul></div>'

    axis = m.get("mechanism_axis", "")
    axis_label = MECHANISM_AXES.get(axis, "")
    axis_html = f'<span class="axis-tag" data-axis="{axis}">{axis} {axis_label}</span>' if axis else ""

    return f'''
    <article class="method" id="{esc(m["method_id"])}">
        <header>
            <h3><span class="met-id">{esc(m["method_id"])}</span> {esc(m["name_ja"])}</h3>
            <div class="meta">
                <span class="name-en">{esc(m["name_en"])}</span>
                <span class="era">{fmt_year(m["era_start"])}–{fmt_year(m["era_end"])}</span>
                <span class="originator">{esc(m["originator"])}</span>
                <span class="org">{esc(m["origin_org"])} / {esc(m["origin_country"])}</span>
                {axis_html}
            </div>
        </header>
        <p class="mechanism">{esc(m["mechanism"])}</p>
        {ev_html}
        {crt_html}
        <footer>
            <a href="{esc(m["primary_source_url"])}" target="_blank" rel="noopener">一次資料 ↗</a>
            <span class="status">status: {esc(m["status"])} / {esc(m["verification"])}</span>
        </footer>
    </article>
    '''


def region_section(rid, title, ids):
    cards = "\n".join(method_card(methods_by_id[mid]) for mid in ids if mid in methods_by_id)
    return f'''
    <section class="chapter-section" id="{rid}">
        <h2>{esc(title)}</h2>
        <div class="methods-grid">
            {cards}
        </div>
    </section>
    '''


# Build TOC
toc_items = "".join(
    f'<li><a href="#{rid}">{i+1:02d}. {esc(title)}</a></li>'
    for i, (rid, title, _) in enumerate(REGIONS)
)
toc_extra = '''
<li class="toc-divider"></li>
<li><a href="#mechanism-axes">統合: 6メカニズム軸</a></li>
<li><a href="#stats">統計</a></li>
<li><a href="#about">DB概要</a></li>
'''

# Mechanism axes section
axis_html_parts = []
for code, label in MECHANISM_AXES.items():
    items = [m for m in methods if m.get("mechanism_axis") == code]
    sample = ", ".join(m["name_ja"] for m in items[:6])
    axis_html_parts.append(
        f'<div class="axis-card"><h4>{code} {label}</h4>'
        f'<p>{len(items)}手法。代表例: {esc(sample)} ...</p></div>'
    )
axis_section = f'''
<section class="chapter-section" id="mechanism-axes">
    <h2>統合: 6メカニズム軸</h2>
    <p>15領域・158手法を横断分析すると、コストダウンは6つのメカニズム軸の累積的・複合的作用として整理できる。各手法は1つ以上の軸に属する。</p>
    <div class="axes-grid">
        {"".join(axis_html_parts)}
    </div>
</section>
'''

# Stats section
total_methods = len(methods)
total_evidence = sum(len(v) for v in evidence_by_m.values())
total_genealogy = len(genealogy)
total_critiques = sum(len(v) for v in critiques_by_m.values())
stats_section = f'''
<section class="chapter-section" id="stats">
    <h2>統計</h2>
    <table class="stats-table">
        <tr><th>項目</th><th>件数</th></tr>
        <tr><td>手法（methods）</td><td>{total_methods}</td></tr>
        <tr><td>数値実証（evidence）</td><td>{total_evidence}</td></tr>
        <tr><td>系譜関係（genealogy）</td><td>{total_genealogy}</td></tr>
        <tr><td>批判・限界（critiques）</td><td>{total_critiques}</td></tr>
        <tr><td>領域（regions）</td><td>15</td></tr>
        <tr><td>ドメイン（domains）</td><td>{len(domains)}</td></tr>
        <tr><td>メカニズム軸</td><td>6</td></tr>
    </table>
</section>
'''

about_section = '''
<section class="chapter-section" id="about">
    <h2>DB概要</h2>
    <p>Cost-Down History DB (CDH-DB) は、技術・開発のコストダウンに関する230年史を15領域に分割して並列リサーチ（researcher エージェント x15体、バックグラウンド同時実行）で網羅した知識基盤である。一次資料URL必須、ハルシネーション排除を品質基準とし、未検証項目には requires_review フラグを付ける運用とする。</p>
    <h3>スキーマ</h3>
    <p>5テーブル構造（methods / evidence / genealogy / critiques / domains）。SQLite 形式で公開し、HTML ダッシュボードは textbook.html スタイル（赤白CI #CC1400、Noto Sans/Serif JP、サイドバー目次、ダークモード対応）に準拠する。</p>
    <h3>収集メタ</h3>
    <ul>
        <li>着手日: 2026-05-13</li>
        <li>方法: researcher エージェント x15体 並列バックグラウンド</li>
        <li>主要ソース: Wikipedia / 一次論文 / 企業年史 / 学術DB</li>
        <li>リポジトリ: <a href="https://github.com/yuyanishimura0312/cost-down-history-db" target="_blank">github.com/yuyanishimura0312/cost-down-history-db</a></li>
    </ul>
    <h3>引用</h3>
    <pre>西村勇也 (2026). Cost-Down History DB v1.0. NPO法人ミラツク. https://yuyanishimura0312.github.io/cost-down-history-db/</pre>
</section>
'''

# CSS — 赤白CI + textbook style
CSS = '''
:root {
    --bg: #FFFFFF;
    --card: #FFFFFF;
    --card-hover: #F7F7F5;
    --accent: #121212;
    --accent-soft: #555555;
    --accent-warm: #CC1400;
    --accent-warm-soft: #B01200;
    --accent-muted: rgba(204,20,0,0.06);
    --text: #121212;
    --text-secondary: #555555;
    --text-muted: #6B6B6B;
    --border: #D9D9D9;
    --border-light: #EEEEEE;
    --highlight: #CC1400;
    --surface: #F7F7F5;
    --font: "Noto Sans JP", "Hiragino Sans", -apple-system, sans-serif;
    --font-serif: "Noto Serif JP", "Hiragino Mincho ProN", Georgia, serif;
}
[data-theme="dark"] {
    --bg: #121212;
    --card: #1A1A1A;
    --card-hover: #222222;
    --accent: #E0E0E0;
    --accent-warm: #FF4030;
    --accent-light: #1A1A1A;
    --accent-muted: rgba(255,64,48,0.10);
    --text: #E0E0E0;
    --text-secondary: #AAAAAA;
    --text-muted: #8A8A8A;
    --border: #333333;
    --border-light: #2A2A2A;
    --highlight: #FF4030;
    --surface: #1A1A1A;
}
* { box-sizing: border-box; }
body {
    margin: 0; padding: 0;
    background: var(--bg); color: var(--text);
    font-family: var(--font);
    font-feature-settings: "palt";
    line-height: 1.85;
    letter-spacing: 0.025em;
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
.theme-toggle {
    background: transparent; border: 1px solid var(--border);
    color: var(--text); padding: 4px 12px; cursor: pointer;
    font-size: 12px; border-radius: 2px;
}
.theme-toggle:hover { background: var(--accent-muted); border-color: var(--accent-warm); }
.layout { display: flex; padding-top: 48px; min-height: 100vh; }
.toc-sidebar {
    position: fixed; top: 48px; left: 0; bottom: 0;
    width: 280px; padding: 32px 20px; overflow-y: auto;
    border-right: 1px solid var(--border);
    background: var(--surface);
    font-size: 13px;
}
.toc-sidebar h4 {
    font-size: 11px; letter-spacing: 0.1em; color: var(--text-secondary);
    margin: 0 0 12px; text-transform: uppercase;
}
.toc-sidebar ul { list-style: none; padding: 0; margin: 0; }
.toc-sidebar li { margin: 6px 0; }
.toc-divider { border-top: 1px solid var(--border); margin: 12px 0; height: 0; }
.toc-sidebar a {
    color: var(--text-secondary); text-decoration: none;
    display: block; padding: 4px 8px; border-radius: 2px;
    transition: color 0.15s, background 0.15s;
}
.toc-sidebar a:hover {
    color: var(--accent-warm); background: var(--accent-muted);
}
.main {
    margin-left: 280px; flex: 1;
    padding: 48px 60px 96px;
    max-width: 880px;
}
.hero { margin-bottom: 64px; }
.hero h1 {
    font-family: var(--font-serif);
    font-size: 36px; font-weight: 700;
    margin: 0 0 16px; line-height: 1.3;
    color: var(--text);
}
.hero .subtitle {
    font-size: 16px; color: var(--text-secondary);
    margin: 0 0 24px;
}
.hero .badges { display: flex; gap: 12px; flex-wrap: wrap; }
.hero .badge {
    font-size: 12px; padding: 4px 10px;
    background: var(--accent-muted); color: var(--accent-warm);
    border-radius: 2px;
}
.chapter-section {
    margin-bottom: 80px;
    padding-bottom: 32px;
    border-bottom: 1px solid var(--border-light);
}
.chapter-section h2 {
    font-family: var(--font-serif);
    font-size: 24px; font-weight: 700;
    margin: 0 0 24px;
    padding-bottom: 12px;
    border-bottom: 2px solid var(--accent-warm);
    color: var(--text);
}
.chapter-section h3 {
    font-size: 18px; margin: 32px 0 12px;
    color: var(--text);
}
.chapter-section > p {
    font-family: var(--font-serif);
    text-indent: 1em;
    margin: 0 0 16px;
}
.chapter-section > p:first-of-type { text-indent: 0; }
.methods-grid { display: flex; flex-direction: column; gap: 20px; }
.method {
    background: var(--card);
    border: 1px solid var(--border-light);
    border-left: 3px solid var(--accent-warm);
    padding: 20px 24px;
    border-radius: 2px;
}
.method:hover {
    background: var(--card-hover);
    border-left-color: var(--accent-warm-soft);
}
.method header h3 {
    font-size: 16px; margin: 0 0 8px;
    color: var(--text); font-weight: 700;
}
.met-id {
    font-family: "SF Mono", "Fira Code", monospace;
    font-size: 11px; color: var(--text-muted);
    margin-right: 8px;
}
.meta {
    display: flex; flex-wrap: wrap; gap: 12px;
    font-size: 12px; color: var(--text-secondary);
    margin-bottom: 12px;
}
.meta .era { font-weight: 700; color: var(--accent-warm); }
.meta .name-en { font-style: italic; }
.axis-tag {
    background: var(--accent-muted); color: var(--accent-warm);
    padding: 2px 8px; border-radius: 2px;
    font-size: 11px;
}
.mechanism {
    font-family: var(--font-serif);
    font-size: 14px; line-height: 1.85;
    margin: 12px 0; color: var(--text);
}
.evidence, .critique {
    margin: 12px 0; padding: 12px 16px;
    background: var(--surface); border-radius: 2px;
    font-size: 13px;
}
.critique { border-left: 2px solid var(--text-muted); }
.ev-label {
    font-size: 11px; letter-spacing: 0.1em;
    color: var(--text-secondary); margin-bottom: 6px;
    text-transform: uppercase; font-weight: 700;
}
.evidence ul, .critique ul { margin: 0; padding-left: 20px; }
.evidence li, .critique li { margin: 4px 0; }
.metric { color: var(--text-muted); font-family: "SF Mono", monospace; font-size: 11px; }
.case { color: var(--text-muted); font-size: 12px; }
.method footer {
    display: flex; justify-content: space-between; align-items: center;
    margin-top: 12px; padding-top: 12px;
    border-top: 1px solid var(--border-light);
    font-size: 12px;
}
.method a {
    color: var(--accent-warm); text-decoration: none;
}
.method a:hover { text-decoration: underline; }
.status {
    font-family: "SF Mono", monospace; font-size: 11px;
    color: var(--text-muted);
}
.axes-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
}
.axis-card {
    background: var(--surface);
    border: 1px solid var(--border-light);
    padding: 16px 20px; border-radius: 2px;
}
.axis-card h4 {
    color: var(--accent-warm); margin: 0 0 8px;
    font-size: 14px;
}
.axis-card p { font-size: 13px; margin: 0; color: var(--text-secondary); }
.stats-table {
    border-collapse: collapse; width: 100%; max-width: 480px;
    font-size: 14px;
}
.stats-table th, .stats-table td {
    border-bottom: 1px solid var(--border-light);
    padding: 10px 16px; text-align: left;
}
.stats-table th {
    background: var(--surface); font-weight: 700;
    color: var(--text);
}
pre {
    background: var(--surface);
    padding: 12px 16px; border-radius: 2px;
    font-size: 13px; overflow-x: auto;
}
@media (max-width: 1000px) {
    .toc-sidebar {
        position: relative; top: 0; width: 100%;
        height: auto; border-right: none;
        border-bottom: 1px solid var(--border);
    }
    .main { margin-left: 0; padding: 32px 20px 80px; }
}
@media print {
    .toc-sidebar, .top-bar, .theme-toggle { display: none; }
    .main { margin-left: 0; padding: 20px; }
    .method { break-inside: avoid; }
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

HTML = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cost-Down History DB — 技術・開発のコストダウン歴史的手法DB</title>
<link rel="icon" href="https://esse-sense.com/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&family=Noto+Serif+JP:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<nav class="top-bar">
    <div class="brand">CDH-DB <span class="brand-sub">Cost-Down History Database v1.0</span></div>
    <button id="themeBtn" class="theme-toggle">ダーク／ライト</button>
</nav>
<div class="layout">
    <aside class="toc-sidebar">
        <h4>目次</h4>
        <ul>
            {toc_items}
            {toc_extra}
        </ul>
    </aside>
    <main class="main">
        <header class="hero">
            <h1>技術・開発のコストダウン歴史的手法DB</h1>
            <p class="subtitle">230年史を15領域に分割した網羅的知識基盤 — Wattの遠心調速機（1788）から生成AI（2022）まで</p>
            <div class="badges">
                <span class="badge">{total_methods} methods</span>
                <span class="badge">{total_evidence} evidence</span>
                <span class="badge">{total_genealogy} genealogy</span>
                <span class="badge">{total_critiques} critiques</span>
                <span class="badge">15 regions</span>
                <span class="badge">6 mechanism axes</span>
            </div>
        </header>
        {"".join(region_section(rid, title, ids) for rid, title, ids in REGIONS)}
        {axis_section}
        {stats_section}
        {about_section}
    </main>
</div>
<script>{JS}</script>
</body>
</html>
'''

OUT.write_text(HTML, encoding="utf-8")
print(f"Dashboard generated: {OUT}")
print(f"Size: {OUT.stat().st_size} bytes")

conn.close()
