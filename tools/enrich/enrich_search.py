#!/usr/bin/env python3
"""searching_sorting.html：第七章各節內容、講義圖、程式與練習。冪等，可重跑。

每一節在 h2 之後有一對 <!-- gen:search-* --> 標記，內容由 content/search_depth.py 產生：
手寫的說明與動畫面板在 search_legacy.py，講義程式在 search_programs.py（課程標頭的函式本體在
search_headers.py），講義圖在 search_figures.py，講義 quiz 在 search_quizzes.py。
動畫引擎（Animator）是頁面原有的主 <script>，本腳本不改動。
"""
import json
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib import ensure_style, _replace_gen

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "searching_sorting.html"
s = PAGE.read_text()
s = ensure_style(s)

from content.search_depth import sections, STYLE
from content.search_figures import STYLE as FIG_STYLE

for name, block in sections().items():
    s, ok = _replace_gen(s, name, block)
    if not ok:
        raise SystemExit(f"missing <!-- gen:{name} --> markers in {PAGE.name}")

for sid, css in (('search-depth-style', STYLE), ('search-figures-style', FIG_STYLE)):
    if f'id="{sid}"' in s:
        s = re.sub(rf'<style id="{sid}">.*?</style>', lambda m: css, s, count=1, flags=re.S)
    else:
        s = s.replace('</head>', css + '\n</head>', 1)

# Counts shown in the table of contents, float navigation and study guide.
n_cards = len(json.loads((ROOT / "data/flashcards_zh/ch7.json").read_text()))
n_qs = len(json.loads((ROOT / "data/questions_zh/ch7.json").read_text()))
s, n1 = re.subn(r'關鍵詞彙卡（\d+ 張）', f'關鍵詞彙卡（{n_cards} 張）', s)
s, n2 = re.subn(r'題庫 ch7\.json · \d+ 張', f'題庫 ch7.json · {n_cards} 張', s)
s, n3 = re.subn(r'自我檢測（\d+ 題）', f'自我檢測（{n_qs} 題）', s)
if (n1, n2, n3) != (2, 1, 2):
    raise SystemExit(f"count labels not found: {n1}, {n2}, {n3}")

# Preserve output spaces as HTML entities without source trailing whitespace.
s = re.sub(r'<pre>.*?</pre>', lambda m: re.sub(r' +(?=\n)', lambda w: '&#32;' * len(w.group()), m.group()), s, flags=re.S)
s = re.sub(r'(?m)^[ \t]+$', '', s)
from content.teaching_copy import polish_preserved
s = polish_preserved("searching_sorting", s)
PAGE.write_text(s)
print("updated:", ", ".join(sections()))
