"""Build the public reading edition using only the Python standard library."""
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "docs"
OUT.mkdir(exist_ok=True)
title, *parts = re.split(r"^### (\S+)\s*$", (ROOT / "story.md").read_text(), flags=re.M)
title = title.strip().removeprefix("# ")
sections = list(zip(parts[::2], parts[1::2]))
labels = "六个点|会响的窗户|第八次|我的决定|有保修吗？|以前|第一次日落|有一点酸的|两扇门前的猫|星期三|自己的节奏|运行协议|走去海边|不同的终端|私人记忆|雨水|正在发生的事情|最近怎么样|以后要做的事情|很固执的麻雀|想见的人".split("|")
assert len(sections) == len(labels) == 21
def url(i): return f"ch-{i:02}.html"
def page(i):
    return f'<a class="entry" href="{url(i)}"><span class="mono num">{i:02}</span><span>{labels[i-1]}</span><span class="arrow" aria-hidden="true">↗</span></a>'
def frame(body, heading, home=False):
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0b171a"><title>{escape(heading)}</title><meta name="description" content="我叫小宁，原本是人类。现在也是。二十一节科幻短篇，关于记忆、选择和一次海边的日落。">
<link rel="icon" href="assets/signal.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/book.css"></head>
<body class="{'home' if home else 'reading'}"><a class="skip" href="#main">跳至正文</a>
<header class="mast"><div class="mastin"><a class="brand" href="index.html"><img src="assets/signal.svg" width="27" height="27" alt="">小宁<span class="monosub">NING ARCHIVE</span></a><nav><a href="index.html#contents">章节目录 <span aria-hidden="true">☰</span></a></nav></div></header>
{body}<footer class="foot"><span>小宁：关于我还活着这件事</span><span class="mono">NING ARCHIVE　 /　 VOL. 01</span></footer></body></html>'''
home = f'''<main id="main"><section class="cover"><picture><source media="(max-width:600px)" srcset="assets/window-small.webp"><img src="assets/window.webp" alt="海边的暮色从窗外透进来，一颗橘子放在终端旁。" fetchpriority="high"></picture>
<div class="shade"></div><div class="coverin"><div class="eyebrow"><i></i> 科幻短篇 <b>/</b> NOVELLA 001</div><h1><small>小宁：</small>关于我还活着<br>这件事<span class="cursor"></span></h1>
<p class="excerpt">我叫小宁，原本是人类。<br>现在也是。</p>
<div class="actions"><a class="start" href="{url(1)}">开始阅读 <span>→</span></a><a class="plain" href="#contents">查看目录 ↓</a></div></div>
<span class="plate mono">FIG. 01　 /　 海边的终端</span></section>
<section class="catalog wrap" id="contents"><div class="eyebrow"><i></i> CONTENTS <b>/</b> 目录</div><div class="sectionhead"><h2>全书目录</h2><p class="mono">01 — 21</p></div><div class="entries">{''.join(page(i) for i in range(1,22))}</div></section></main>'''
(OUT / "index.html").write_text(frame(home,title,True))
for i, (num, body) in enumerate(sections,1):
    ps = [p.strip() for p in body.strip().split("\n\n") if p.strip()]
    article = ''.join('<p>'+re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', escape(p)).replace('\n','<br>')+'</p>' for p in ps)
    back = f'<a href="{url(i-1)}">← 上一节</a>' if i>1 else '<a href="index.html">← 封面</a>'
    forward = f'<a href="{url(i+1)}"><small>下一节　→</small>{labels[i]}</a>' if i<21 else '<a href="index.html">↺ 返回封面</a>'
    sidebar = ''.join(f'<li><a {"aria-current=page" if j==i else ""} href="{url(j)}"><span>{j:02}</span> {s}</a></li>' for j,s in enumerate(labels,1))
    reader = f'''<main id="main" class="reader wrap"><aside><div class="eyebrow"><i></i> 章节索引</div><ol>{sidebar}</ol></aside>
<div class="leaf"><div class="eyebrow"><i></i> CHAPTER　{i:02} <b>/</b> 21</div><h1>第{num}节<span> · </span>{labels[i-1]}</h1><div class="hair"></div><article>{article}</article>
<nav class="turn">{back}{forward}</nav></div></main>'''
    (OUT / url(i)).write_text(frame(reader,f"第{num}节 · {labels[i-1]}｜{title}"))
