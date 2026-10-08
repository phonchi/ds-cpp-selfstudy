#!/usr/bin/env python3
"""graphs.html：第八章各節內容、圖與程式。冪等，可重跑。

每一節有一或多對 <!-- gen:graphs-* --> 標記，內容由 content/graphs_depth.py 產生
（程式在 graphs_programs.py、講義圖在 graphs_figures.py）。手寫的 h2、動畫面板與其 JS 原地保留。
"""
import json
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib import ensure_style, _replace_gen

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "graphs.html"
s = PAGE.read_text()
s = ensure_style(s)

from content.graphs_depth import sections, STYLE
from content.graphs_figures import STYLE as FIG_STYLE

for name, block in sections().items():
    s, ok = _replace_gen(s, name, block)
    if not ok:
        raise SystemExit(f"missing <!-- gen:{name} --> markers in {PAGE.name}")

for sid, css in (('graphs-depth-style', STYLE), ('graphs-figures-style', FIG_STYLE)):
    if f'id="{sid}"' in s:
        s = re.sub(rf'<style id="{sid}">.*?</style>', lambda m: css, s, count=1, flags=re.S)
    else:
        s = s.replace('</head>', css + '\n</head>', 1)

# Flashcard and bank-quiz counts shown in the study guide, the table of contents and the cards heading.
n_cards = len(json.loads((ROOT / "data/flashcards_zh/ch8.json").read_text()))
s, n1 = re.subn(r'關鍵詞彙卡（\d+ 張）', f'關鍵詞彙卡（{n_cards} 張）', s)
s, n2 = re.subn(r'題庫 ch8\.json · \d+ 張', f'題庫 ch8.json · {n_cards} 張', s)
if (n1, n2) != (2, 1):
    raise SystemExit(f"flashcard count labels not found: {n1}, {n2}")
n_bank = len(json.loads((ROOT / "data/questions_zh/ch8.json").read_text()))
s, n3 = re.subn(r'自我檢測（\d+ 題）', f'自我檢測（{n_bank} 題）', s)
if n3 != 2:
    raise SystemExit(f"bank quiz count labels not found: {n3}")

# Preserve output spaces as HTML entities without source trailing whitespace.
s = re.sub(r'<pre>.*?</pre>', lambda m: re.sub(r' +(?=\n)', lambda w: '&#32;' * len(w.group()), m.group()), s, flags=re.S)
s = re.sub(r'(?m)^[ \t]+$', '', s)
from content.teaching_copy import polish_preserved
s = polish_preserved("graphs", s)
PAGE.write_text(s)
print("updated:", ", ".join(sections()))
