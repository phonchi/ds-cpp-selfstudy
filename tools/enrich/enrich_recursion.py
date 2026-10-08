#!/usr/bin/env python3
"""recursion.html：第六章各節內容、圖、程式與附加互動。冪等，可重跑。

每一節在 h2 之後有一對 <!-- gen:recursion-* --> 標記，內容由 content/recursion_depth.py 產生
（程式在 recursion_programs.py、講義圖在 recursion_figures.py、互動元件在 recursion_widgets.py）。
toStr(10, 2) 呼叫堆疊動畫的 JS 放在 <script id="recursion-extra-js">，其餘動畫 JS 是頁面原有的主 <script>。
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

from content.recursion_depth import sections, STYLE
from content.recursion_figures import STYLE as FIG_STYLE
from content.recursion_widgets import EXTRA_JS

for name, block in sections().items():
    s, ok = _replace_gen(s, name, block)
    if not ok:
        raise SystemExit(f"missing <!-- gen:{name} --> markers in {PAGE.name}")

for sid, css in (('recursion-depth-style', STYLE), ('recursion-figures-style', FIG_STYLE)):
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

# Flashcard count shown in the table of contents and the cards heading.
n_cards = len(json.loads((ROOT / "data/flashcards_zh/ch6.json").read_text()))
s, n1 = re.subn(r'關鍵詞彙卡（\d+ 張）', f'關鍵詞彙卡（{n_cards} 張）', s)
s, n2 = re.subn(r'題庫 ch6\.json · \d+ 張', f'題庫 ch6.json · {n_cards} 張', s)
if (n1, n2) != (2, 1):
    raise SystemExit(f"flashcard count labels not found: {n1}, {n2}")

# Preserve output spaces as HTML entities without source trailing whitespace.
s = re.sub(r'<pre>.*?</pre>', lambda m: re.sub(r' +(?=\n)', lambda w: '&#32;' * len(w.group()), m.group()), s, flags=re.S)
s = re.sub(r'(?m)^[ \t]+$', '', s)
from content.teaching_copy import polish_preserved
s = polish_preserved("recursion", s)
PAGE.write_text(s)
print("updated:", ", ".join(sections()))
