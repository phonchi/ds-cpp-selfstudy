#!/usr/bin/env python3
"""recursion.html：第六章各節內容、圖、程式與附加互動。冪等，可重跑。

每一節在 h2 之後有一對 <!-- gen:recursion-* --> 標記，內容由 content/recursion_depth.py 產生
（程式在 recursion_programs.py、講義圖在 recursion_figures.py、互動元件在 recursion_widgets.py）。
toStr 呼叫堆疊與迷宮播放器分別由 recursion-extra-js、recursion-maze-js 重建；其餘動畫保留在原主 script。
"""
import json
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib import ensure_style, _replace_gen

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "recursion.html"
s = PAGE.read_text()
s = ensure_style(s)

# Keep the opening's navigation and heading aligned with its conceptual role.
s = re.sub(r'(<a href="#prologue" data-target="prologue"><span class="fn-num">P00</span><span class="fn-name">).*?(</span></a>)', r'\1遞迴用途與策略\2', s, count=1)
s = re.sub(r'(<a href="#prologue"><span class="toc-num">P00</span>).*?(</a>)', r'\1遞迴用途與策略\2', s, count=1)
s = re.sub(r'(<section id="prologue">.*?<h2>).*?( <span class="sec-badge">)', r'\1為什麼要使用遞迴？\2', s, count=1, flags=re.S)
s = s.replace('三法則｜call stack｜toStr｜河內塔｜迷宮回溯｜動態規劃', '遞迴用途｜解題策略｜呼叫堆疊｜河內塔｜迷宮｜找零')
s = s.replace('<span class="fn-name">動態規劃</span>', '<span class="fn-name">貪婪與動態規劃</span>')
s = s.replace('<a href="#dp"><span class="toc-num">P08</span>動態規劃</a>', '<a href="#dp"><span class="toc-num">P08</span>貪婪與動態規劃</a>')

from content.recursion_depth import sections, STYLE
from content.recursion_figures import STYLE as FIG_STYLE
from content.recursion_widgets import EXTRA_JS
from content.recursion_maze import MAZE_JS, MAZE_STYLE

for name, block in sections().items():
    s, ok = _replace_gen(s, name, block)
    if not ok:
        raise SystemExit(f"missing <!-- gen:{name} --> markers in {PAGE.name}")

for sid, css in (('recursion-depth-style', STYLE), ('recursion-figures-style', FIG_STYLE), ('recursion-maze-style', MAZE_STYLE)):
    if f'id="{sid}"' in s:
        s = re.sub(rf'<style id="{sid}">.*?</style>', lambda m: css, s, count=1, flags=re.S)
    else:
        s = s.replace('</head>', css + '\n</head>', 1)

# Extra player JS: after the main script (it uses Player, renderBoxStack, setStatus, hlLine).
extra = f'<script id="recursion-extra-js">\n{EXTRA_JS}\n</script>\n'
if 'id="recursion-extra-js"' in s:
    s = re.sub(r'<script id="recursion-extra-js">.*?</script>\n', lambda m: extra, s, count=1, flags=re.S)
else:
    anchor = '<script>\nconst FLASHCARDS'
    if s.count(anchor) != 1:
        raise SystemExit("FLASHCARDS script not found")
    s = s.replace(anchor, extra + anchor, 1)

# Replace the former inline maze implementation once, then keep its source in
# recursion_maze.py so rebuilding cannot restore different search semantics.
legacy = r'/\* ---------- P05 maze ---------- \*/.*?(?=/\* ---------- P08 DP make change)'
s, removed = re.subn(legacy, '/* Maze player is generated in recursion-maze-js. */\n\n', s, count=1, flags=re.S)
maze = f'<script id="recursion-maze-js">\n{MAZE_JS}\n</script>\n'
if 'id="recursion-maze-js"' in s:
    s = re.sub(r'<script id="recursion-maze-js">.*?</script>\n', lambda m: maze, s, count=1, flags=re.S)
else:
    if removed != 1:
        raise SystemExit('Expected the original maze player before its first migration')
    anchor = '<script>\nconst FLASHCARDS'
    if s.count(anchor) != 1:
        raise SystemExit('FLASHCARDS script not found')
    s = s.replace(anchor, maze + anchor, 1)

# Flashcard count shown in the table of contents and the cards heading.
n_cards = len(json.loads((ROOT / "data/flashcards_zh/ch6.json").read_text()))
s, n1 = re.subn(r'關鍵詞彙卡（\d+ 張）', f'關鍵詞彙卡（{n_cards} 張）', s)
s, n2 = re.subn(r'sec-badge">\d+ 張', f'sec-badge">{n_cards} 張', s)
if (n1, n2) != (2, 1):
    raise SystemExit(f"flashcard count labels not found: {n1}, {n2}")

# Preserve output spaces as HTML entities without source trailing whitespace.
s = re.sub(r'<pre>.*?</pre>', lambda m: re.sub(r' +(?=\n)', lambda w: '&#32;' * len(w.group()), m.group()), s, flags=re.S)
s = re.sub(r'(?m)^[ \t]+$', '', s)
from content.teaching_copy import polish_preserved
s = polish_preserved("recursion", s)
from content.course_recordings import apply_recording
s = apply_recording(s, "recursion")
PAGE.write_text(s)
print("updated:", ", ".join(sections()))
