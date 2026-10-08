#!/usr/bin/env python3
"""linear_structures.html：第五章各節內容、講義圖與樣式。冪等，可重跑。

每一節在需要的位置有成對的 <!-- gen:linear-* --> 標記，內容由 content/linear_depth.py 產生；
完整程式與輸出在 content/linear_programs.py，講義圖在 content/linear_figures.py。
手寫的 h2、播放器與 widget 在 gen 區之外，不由這支腳本產生。
"""
import sys
import re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib import ensure_style, _replace_gen

PAGE = Path(__file__).resolve().parents[2] / "linear_structures.html"
s = PAGE.read_text()
s = ensure_style(s)

from content.linear_depth import sections, STYLE
for name, block in sections().items():
    s, ok = _replace_gen(s, name, block)
    if not ok:
        raise SystemExit(f"missing <!-- gen:{name} --> markers in {PAGE.name}")

from content.linear_figures import STYLE as FIGURE_STYLE
for sid, css in (('linear-depth-style', STYLE), ('linear-figures-style', FIGURE_STYLE)):
    if f'id="{sid}"' in s:
        s = re.sub(rf'<style id="{sid}">.*?</style>', lambda m: css, s, flags=re.S)
    else:
        s = s.replace('</head>', css + '\n</head>', 1)

# Preserve output spaces as HTML entities without source trailing whitespace.
s = re.sub(r'<pre>.*?</pre>', lambda m: re.sub(r' +(?=\n)', lambda w: '&#32;' * len(w.group()), m.group()), s, flags=re.S)
s = re.sub(r'(?m)^[ \t]+$', '', s)
from content.teaching_copy import polish_preserved
s = polish_preserved("linear_structures", s)
# chapter_math.render_math is not applied here: on this page it rewrites postfix examples such as
# "7 8 + 3 2 + /" into broken inline math. Formulas in the generated text are written as $...$ directly.
PAGE.write_text(s)
print("updated:", ", ".join(sections()))
