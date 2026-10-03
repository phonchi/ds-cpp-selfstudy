#!/usr/bin/env python3
"""linked_lists.html：第四章各節內容、動畫與樣式。冪等，可重跑。

每一節在 section 標題之後有一對 <!-- gen:linked-* --> 標記，內容由
content/linked_depth.py 產生；動畫 JS 取自 content/linked_interactions.js，
放在 /* ---------- helpers: linked list DOM ---------- */ 與 /* /linked-interactions */ 之間。
"""
import sys
import re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib import ensure_style, _replace_gen

PAGE = Path(__file__).resolve().parents[2] / "linked_lists.html"
s = PAGE.read_text()
s = ensure_style(s)

from content.linked_depth import sections, STYLE
for name, block in sections().items():
    s, ok = _replace_gen(s, name, block)
    if not ok:
        raise SystemExit(f"missing <!-- gen:{name} --> markers in {PAGE.name}")

if 'id="linked-depth-style"' in s:
    s = re.sub(r'<style id="linked-depth-style">.*?</style>', lambda m: STYLE, s, flags=re.S)
else:
    s = s.replace('</head>', STYLE + '\n</head>', 1)

interactions = (Path(__file__).parent / 'content' / 'linked_interactions.js').read_text().rstrip('\n') + '\n'
s, n = re.subn(r'/\* ---------- helpers: linked list DOM ---------- \*/.*?/\* /linked-interactions \*/\n',
               lambda m: interactions, s, flags=re.S)
if n != 1:
    raise SystemExit("linked-interactions JS block not found")

# Preserve output spaces as HTML entities without source trailing whitespace.
s = re.sub(r'<pre>.*?</pre>', lambda m: re.sub(r' +(?=\n)', lambda w: '&#32;' * len(w.group()), m.group()), s, flags=re.S)
s = re.sub(r'(?m)^[ \t]+$', '', s)
from content.teaching_copy import polish_preserved
s = polish_preserved("linked_lists", s)
from content.linked_figures import apply_figures
s = apply_figures(s)
from content.chapter_math import render_math
s = render_math(s)
PAGE.write_text(s)
print("updated:", ", ".join(sections()))
