#!/usr/bin/env python3
"""Merge 6 chapters into textbook.html with sidebar TOC + 赤白CI."""

import re
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "textbook"
OUT = ROOT / "docs" / "textbook.html"

CHAPTERS = [
    ("ch01_overview.md", "ch01", "第1章 230年史の概観"),
    ("ch02_axes.md", "ch02", "第2章 6メカニズム軸"),
    ("ch03_domains.md", "ch03", "第3章 15ドメインの俯瞰"),
    ("ch04_genealogy.md", "ch04", "第4章 主要系譜の物語"),
    ("ch05_failures.md", "ch05", "第5章 失敗事例とトレードオフ"),
    ("ch06_outlook.md", "ch06", "第6章 2025-2050年の展望"),
]


def md_to_html(md_text):
    """Minimal Markdown→HTML converter (headings, bold, italic, links, code, lists, paragraphs)."""
    lines = md_text.split("\n")
    out = []
    in_list = False
    in_code = False
    in_para = False

    def close_para():
        nonlocal in_para
        if in_para:
            out.append("</p>")
            in_para = False

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for line in lines:
        s = line.rstrip()

        # Code block
        if s.startswith("```"):
            close_para()
            close_list()
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                out.append("<pre><code>")
                in_code = True
            continue
        if in_code:
            out.append(html.escape(s))
            continue

        # Headings (skip the per-chapter # H1; we add our own)
        m = re.match(r"^(#{1,6})\s+(.+)", s)
        if m:
            close_para()
            close_list()
            level = len(m.group(1))
            text = inline(m.group(2))
            if level == 1:
                # convert to h2 (the chapter container already provides h1)
                out.append(f"<h2>{text}</h2>")
            elif level == 2:
                out.append(f"<h3>{text}</h3>")
            elif level == 3:
                out.append(f"<h4>{text}</h4>")
            else:
                out.append(f"<h5>{text}</h5>")
            continue

        # Horizontal rule
        if re.match(r"^---+$", s):
            close_para()
            close_list()
            out.append("<hr>")
            continue

        # Bullet list
        bm = re.match(r"^[-*]\s+(.+)", s)
        if bm:
            close_para()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(bm.group(1))}</li>")
            continue

        # Numbered list (treat as <ol> alternative; here we keep <ul> for simplicity)
        nm = re.match(r"^\d+\.\s+(.+)", s)
        if nm:
            close_para()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(nm.group(1))}</li>")
            continue

        # Empty
        if not s.strip():
            close_para()
            close_list()
            continue

        # Paragraph
        close_list()
        if not in_para:
            out.append("<p>")
            in_para = True
        out.append(inline(s))

    close_para()
    close_list()
    if in_code:
        out.append("</code></pre>")
    return "\n".join(out)


def inline(s):
    # Bold **x**
    s = re.sub(r"\*\*([^\*]+)\*\*", r"<strong>\1</strong>", s)
    # Italic *x* (only when not part of **)
    s = re.sub(r"(?<!\*)\*([^\*]+)\*(?!\*)", r"<em>\1</em>", s)
    # Inline code `x`
    s = re.sub(r"`([^`]+)`", lambda m: f"<code>{html.escape(m.group(1))}</code>", s)
    # Links [text](url)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    return s


# Build TOC and chapter HTML
toc_html = []
chapters_html = []
for fn, cid, title in CHAPTERS:
    text = (SRC / fn).read_text(encoding="utf-8")
    # Strip first H1 if present (assume the chapter file starts with "# Chapter Title")
    text = re.sub(r"^#\s+.*\n", "", text, count=1)
    body = md_to_html(text)
    chapters_html.append(f'<section class="chapter-section" id="{cid}"><h1>{html.escape(title)}</h1>{body}</section>')
    # Extract subheadings for TOC
    subheads = re.findall(r"^##\s+(.+)$", text, re.MULTILINE)
    sub_html = ""
    if subheads[:6]:
        sub_html = "<ul class='sub'>" + "".join(f"<li><a href='#{cid}'>{html.escape(s.strip())}</a></li>" for s in subheads[:6]) + "</ul>"
    toc_html.append(f"<li><a href='#{cid}'>{html.escape(title)}</a>{sub_html}</li>")

toc_html_str = "<ul>" + "".join(toc_html) + "</ul>"

CSS = """
:root {
    --bg:#FFFFFF;--card:#FFFFFF;--card-hover:#F7F7F5;
    --accent:#121212;--accent-soft:#555;
    --accent-warm:#CC1400;--accent-warm-soft:#B01200;--accent-muted:rgba(204,20,0,0.06);
    --text:#121212;--text-secondary:#555;--text-muted:#6B6B6B;
    --border:#D9D9D9;--border-light:#EEEEEE;
    --surface:#F7F7F5;
    --font:"Noto Sans JP","Hiragino Sans",-apple-system,sans-serif;
    --font-serif:"Noto Serif JP","Hiragino Mincho ProN",Georgia,serif;
}
[data-theme="dark"]{
    --bg:#121212;--card:#1A1A1A;--card-hover:#222;
    --accent:#E0E0E0;--accent-warm:#FF4030;
    --accent-muted:rgba(255,64,48,0.10);
    --text:#E0E0E0;--text-secondary:#AAA;--text-muted:#8A8A8A;
    --border:#333;--border-light:#2A2A2A;
    --surface:#1A1A1A;
}
*{box-sizing:border-box}
body{
    margin:0;padding:0;background:var(--bg);color:var(--text);
    font-family:var(--font);font-feature-settings:"palt";
    line-height:1.95;letter-spacing:0.025em;
}
.top-bar{
    position:fixed;top:0;left:0;right:0;height:48px;z-index:100;
    background:var(--bg);border-top:3px solid #121212;
    border-bottom:1px solid var(--border);
    display:flex;align-items:center;justify-content:space-between;
    padding:0 20px;
}
[data-theme="dark"] .top-bar{border-top:3px solid var(--accent-warm)}
.brand{font-size:14px;font-weight:700;color:var(--accent-warm);letter-spacing:0.05em}
.brand-sub{color:var(--text-secondary);font-weight:400;margin-left:8px;font-size:12px}
.nav-link{color:var(--text-secondary);text-decoration:none;margin-right:16px;font-size:13px}
.nav-link:hover{color:var(--accent-warm)}
.theme-toggle{
    background:transparent;border:1px solid var(--border);
    color:var(--text);padding:4px 12px;cursor:pointer;font-size:12px;border-radius:2px;
}
.layout{display:flex;padding-top:48px}
.toc-sidebar{
    position:fixed;top:48px;left:0;bottom:0;width:280px;
    padding:32px 20px;overflow-y:auto;
    border-right:1px solid var(--border);
    background:var(--surface);font-size:12.5px;
}
.toc-sidebar h4{
    font-size:11px;letter-spacing:0.1em;color:var(--text-secondary);
    margin:0 0 12px;text-transform:uppercase;
}
.toc-sidebar ul{list-style:none;padding:0;margin:0}
.toc-sidebar .sub{padding-left:14px;margin-top:4px}
.toc-sidebar .sub li{margin:2px 0;font-size:11.5px}
.toc-sidebar li{margin:6px 0}
.toc-sidebar a{color:var(--text-secondary);text-decoration:none;display:block;padding:3px 6px;border-radius:2px}
.toc-sidebar a:hover{color:var(--accent-warm);background:var(--accent-muted)}
.main{margin-left:280px;flex:1;padding:48px 60px 120px;max-width:840px}
.hero{margin-bottom:64px;padding-bottom:32px;border-bottom:2px solid var(--accent-warm)}
.hero h1{font-family:var(--font-serif);font-size:36px;font-weight:700;margin:0 0 12px;line-height:1.3}
.hero .subtitle{font-size:15px;color:var(--text-secondary);margin:0 0 16px}
.hero .badges{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.hero .badge{font-size:11px;padding:3px 8px;background:var(--accent-muted);color:var(--accent-warm);border-radius:2px}
.chapter-section{margin-bottom:80px;padding-bottom:32px;border-bottom:1px solid var(--border-light)}
.chapter-section h1{
    font-family:var(--font-serif);font-size:28px;font-weight:700;
    margin:0 0 32px;padding:0 0 12px;
    border-bottom:3px solid var(--accent-warm);color:var(--text);
}
.chapter-section h2{
    font-family:var(--font-serif);font-size:22px;font-weight:700;
    margin:48px 0 16px;color:var(--text);
    padding-bottom:6px;border-bottom:1px solid var(--border-light);
}
.chapter-section h3{
    font-size:17px;font-weight:700;margin:32px 0 12px;color:var(--text);
}
.chapter-section h4{font-size:15px;margin:20px 0 8px;color:var(--text-secondary)}
.chapter-section h5{font-size:13px;margin:16px 0 6px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em}
.chapter-section p{
    font-family:var(--font-serif);font-size:15px;
    text-indent:1em;margin:0 0 18px;
}
.chapter-section p:first-of-type{text-indent:0}
.chapter-section ul,.chapter-section ol{margin:0 0 18px 0;padding-left:24px;font-size:14px}
.chapter-section li{margin:4px 0;line-height:1.75}
.chapter-section a{color:var(--accent-warm);text-decoration:none}
.chapter-section a:hover{text-decoration:underline}
.chapter-section code{font-family:"SF Mono","Fira Code",monospace;font-size:13px;background:var(--surface);padding:1px 5px;border-radius:2px}
.chapter-section pre{background:var(--surface);padding:14px 18px;border-radius:2px;overflow-x:auto;margin:16px 0;font-size:12px;line-height:1.6}
.chapter-section pre code{background:transparent;padding:0}
.chapter-section hr{border:none;border-top:1px solid var(--border-light);margin:32px 0}
.chapter-section strong{color:var(--accent-warm);font-weight:700}
.chapter-section em{font-style:italic;color:var(--text-secondary)}
@media (max-width:1000px){
    .toc-sidebar{position:relative;top:0;width:100%;height:auto;border-right:none;border-bottom:1px solid var(--border)}
    .main{margin-left:0;padding:32px 20px 80px}
}
@media print{
    .toc-sidebar,.top-bar,.theme-toggle{display:none}
    .main{margin-left:0;padding:20px;max-width:none}
    .chapter-section{page-break-after:always}
}
"""

JS = """
const root = document.documentElement;
if (localStorage.getItem("cdh-theme")) root.setAttribute("data-theme", localStorage.getItem("cdh-theme"));
document.getElementById("themeBtn").addEventListener("click", () => {
    const cur = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", cur);
    localStorage.setItem("cdh-theme", cur);
});
"""

HTML = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CDH 教科書 — 技術・開発のコストダウン230年史</title>
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
        <span class="brand-sub">Textbook v1.3 — 230年史</span>
    </div>
    <div>
        <a href="index.html" class="nav-link">一覧</a>
        <a href="analytics.html" class="nav-link">分析</a>
        <a href="app.html" class="nav-link">アプリ</a>
        <a href="https://github.com/yuyanishimura0312/cost-down-history-db" class="nav-link">GitHub</a>
        <button id="themeBtn" class="theme-toggle">ダーク／ライト</button>
    </div>
</nav>
<div class="layout">
    <aside class="toc-sidebar">
        <h4>目次</h4>
        {toc_html_str}
    </aside>
    <main class="main">
        <header class="hero">
            <h1>技術・開発のコストダウン 230年史</h1>
            <p class="subtitle">Wattの遠心調速機（1788）から生成AI（2024）まで、6章の地の文で読む。Cost-Down History DB v1.3 の346手法・190実証・107系譜・47批判を編集したテキストブック。</p>
            <div class="badges">
                <span class="badge">346 methods</span>
                <span class="badge">190 evidence</span>
                <span class="badge">107 genealogy</span>
                <span class="badge">47 critiques</span>
                <span class="badge">15 domains</span>
                <span class="badge">6 chapters</span>
                <span class="badge">~50,000字</span>
            </div>
        </header>
        {"".join(chapters_html)}
    </main>
</div>
<script>{JS}</script>
</body>
</html>
"""

OUT.write_text(HTML, encoding="utf-8")
print(f"Textbook generated: {OUT}")
print(f"Size: {OUT.stat().st_size:,} bytes")
