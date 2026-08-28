#!/usr/bin/env python3
"""ds-cpp-selfstudy 課前章（00A/00B）與先備頁（P1–P9）的尾段注入。

分工與既有腳本一致：本檔負責「結構」（導讀框、float-nav/TOC 補項、bankquiz 錨點、
詞彙卡區、上下頁導覽、CSS/JS 引擎），內容則交給 tools/apply_zh.py 從 data/ 灌入。

冪等：頁面出現 <!-- prereq-injected --> 即跳過。

注意：本 repo 沒有保存當初網站化用的 inject 腳本，所以 CSS/JS 常數直接從既有頁面
的 HTML 抽出來（已驗證與 Python 版姊妹站的同名常數位元組相容）。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = "<!-- prereq-injected -->"

# 與九章正課頁完全相同的 MathJax 設定（保險用；從 recursion.html 的 head 組頁本來就有）
MATHJAX = """<script>
  MathJax = { tex: { inlineMath: [['$','$']], displayMath: [['$$','$$']] }, svg: { fontCache: 'global' } };
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
"""

# 課前／先備頁專用的少量補充樣式（本 repo 完全沒有這三個 class）
PRE_CSS = """
.hero .chapter-tag{font-family:'JetBrains Mono',monospace;font-size:.85rem;color:#f5b82e;letter-spacing:.3em;margin-bottom:.8rem;}
.cmp-table-wrap{overflow-x:auto;margin-bottom:1rem;}
.ds-hook{background:var(--card);border:1px solid var(--card-border);border-left:5px solid var(--accent3);border-radius:10px;padding:.8rem 1.1rem;margin:1rem 0;font-size:.9rem;}
.ds-hook .dh-title{font-family:'JetBrains Mono',monospace;font-size:.72rem;font-weight:700;letter-spacing:1.2px;color:var(--accent3);margin-bottom:.3rem;}
"""

# apply_zh.py 會把題目的 code 欄位包成 <pre class="sq-code">
CODE_CSS = """
.sq-code{background:var(--code-bg);color:var(--code-fg);font-family:'JetBrains Mono',monospace;font-size:.82rem;line-height:1.55;padding:.7rem .9rem;border-radius:8px;margin:.2rem 0 .8rem;overflow-x:auto;white-space:pre;}
"""


def _slice(fname, start, end):
    """從既有頁面抽出 start 與 end 之間的區段（含 start）。"""
    s = (ROOT / fname).read_text()
    i = s.find(start)
    assert i >= 0, f"{fname}: 找不到 {start[:40]}"
    j = s.find(end, i + len(start))
    assert j >= 0, f"{fname}: 找不到結束標記 {end[:20]}"
    return s[i:j]


# 網站化樣式（study-guide / flashcards / chapter-nav）—— recursion.html 的第二個 style 區塊
SITE_CSS = _slice("recursion.html",
                  "/* ===== 網站化附加樣式（study-guide / flashcards / chapter-nav）===== */",
                  "</style>")
# 題庫自測區樣式 —— 只有 searching_sorting/graphs/trees 三頁有
QUIZ_CSS = _slice("searching_sorting.html",
                  "/* ===== 題庫自測區 ===== */",
                  "\n\n/* =====")
# 字卡引擎
SITE_JS = _slice("recursion.html", "/* ===== Flashcards engine ===== */", "</script>")
# .sq-item 點選判定引擎
QUIZ_JS = _slice("searching_sorting.html",
                 "(function(){\n  document.querySelectorAll('.sq-item')", "</script>")

# file, 短標題, 詞彙卡母檔, 題庫母檔(None=用頁內 .quiz-box), 類型, prev, next, next 標籤
PRE, PQ = "pre", "prereq"
PPAGES = [
    ("00a_why_code",        "為什麼還要學資料結構",   "00a", None, PRE, None,                   "00b_setup",           "課前準備與環境安裝"),
    ("00b_setup",           "課前準備與環境安裝",     "00b", None, PRE, "00a_why_code",         "introduction",        "C++ 導論"),
    ("p1_cpp_basics",       "C++ 基礎與編譯流程",     "p1",  "p1", PQ,  None,                   "p2_flow_control",     "流程控制"),
    ("p2_flow_control",     "流程控制",               "p2",  "p2", PQ,  "p1_cpp_basics",        "p3_functions",        "函式"),
    ("p3_functions",        "函式",                   "p3",  "p3", PQ,  "p2_flow_control",      "p4_pointers_memory",  "陣列、指標與動態記憶體"),
    ("p4_pointers_memory",  "陣列、指標與動態記憶體", "p4",  "p4", PQ,  "p3_functions",         "p5_vector_string",    "vector 與 string"),
    ("p5_vector_string",    "vector 與 string",       "p5",  "p5", PQ,  "p4_pointers_memory",   "p6_map_set",          "map、set 與迭代器"),
    ("p6_map_set",          "map、set 與迭代器",      "p6",  "p6", PQ,  "p5_vector_string",     "p7_files_exceptions", "檔案與例外"),
    ("p7_files_exceptions", "檔案與例外",             "p7",  "p7", PQ,  "p6_map_set",           "p8_oop_basics",       "物件導向（基礎）"),
    ("p8_oop_basics",       "物件導向（基礎）",       "p8",  "p8", PQ,  "p7_files_exceptions",  "p9_oop_advanced",     "物件導向（進階）"),
    ("p9_oop_advanced",     "物件導向（進階）",       "p9",  "p9", PQ,  "p8_oop_basics",        "introduction",        "回到主線：C++ 導論"),
]

PREV_LABEL = {p[0]: p[1] for p in PPAGES}

SG_PRE = """<div class="study-guide">
  <div class="sg-title">📌 本頁使用方式（課前準備 · 讀完再進第 01 章）</div>
  <p>① <strong>照節次讀</strong>：每一節都短，不要跳著看。
  ② <strong>動手驗證</strong>：有互動元件的地方先自己預測答案，再按按鈕對照。
  ③ <strong>做完自我檢核</strong>再往下：答錯就回頭重讀該節。
  ④ 最後翻 <a href="#cards">關鍵詞彙卡</a>，能不看答案講出定義才算過關。</p>
  <div class="sg-links">{links}</div>
</div>
"""

SG_PQ = """<div class="study-guide">
  <div class="sg-title">📌 本頁使用方式（先備複習 · 選讀，不列入評分）</div>
  <p>① 這頁複習資料結構課程<strong>預設你已經會</strong>的 C++。已經熟的可以直接跳過。
  ② 每節都附一個<strong>「這在資料結構課哪裡會用到」</strong>的小方框——那才是你該記住的部分。
  ③ 讀完做 <a href="#bankquiz">自我檢測</a>，再翻 <a href="#cards">關鍵詞彙卡</a>。
  <br><strong>本頁屬補充先備知識，不列入作業與考試範圍。</strong></p>
  <div class="sg-links">{links}</div>
</div>
"""

LINKS_COMMON = ('<a href="index.html">🏠 章節總覽</a>'
                '<a href="index.html#prereq">📚 先備頁總覽</a>'
                '<a href="https://pythontutor.com/cpp.html" target="_blank" rel="noopener">🔬 C++ Tutor</a>'
                '<a href="https://cppreference.com/" target="_blank" rel="noopener">📖 cppreference</a>')


def inject(entry):
    fname, short, fc, bq, kind, prev, nxt, nxt_label = entry
    path = ROOT / f"{fname}.html"
    if not path.exists():
        print(f"miss {fname}.html（尚未撰寫，略過）")
        return
    s = path.read_text()

    # MathJax：本 repo 的頁面都有，但移植進來的頁面若缺就補上（冪等，放在 MARKER 之前）
    if "MathJax" not in s:
        assert s.count("</head>") == 1, fname
        s = s.replace("</head>", MATHJAX + "</head>", 1)
        path.write_text(s)
        print(f"    + MathJax -> {fname}")

    if MARKER in s:
        print(f"skip {fname}")
        return

    # 1. CSS
    css = PRE_CSS
    if ".study-guide{" not in s:
        css += SITE_CSS
    if bq and ".sq-item{" not in s:
        css += QUIZ_CSS + CODE_CSS
    assert s.count("</head>") == 1, fname
    s = s.replace("</head>", MARKER + "\n" + f"<style>{css}</style>\n" + "</head>", 1)

    # 2. float-nav 補 QUIZ / CARD（插在 ↑TOP 之前）
    m = re.search(r'  <a href="#top" class="fn-top"', s)
    assert m, f"{fname}: fn-top not found"
    nav_add = ""
    if bq:
        nav_add += ('  <a href="#bankquiz" data-target="bankquiz"><span class="fn-num">QUIZ</span>'
                    '<span class="fn-name">自我檢測</span></a>\n')
    nav_add += ('  <a href="#cards" data-target="cards"><span class="fn-num">CARD</span>'
                '<span class="fn-name">關鍵詞彙卡</span></a>\n')
    s = s[:m.start()] + nav_add + s[m.start():]

    # 3. TOC 補 QUIZ / CARD（接在 REF 之後）
    tocm = re.search(r'(<a href="#(?:reference|summary)"><span class="toc-num">REF</span>[^\n]*</a>)', s)
    if tocm:
        toc_add = ""
        if bq:
            toc_add += '\n    <a href="#bankquiz"><span class="toc-num">QUIZ</span>自我檢測</a>'
        toc_add += '\n    <a href="#cards"><span class="toc-num">CARD</span>關鍵詞彙卡</a>'
        s = s[:tocm.end()] + toc_add + s[tocm.end():]

    # 4. 導讀框
    tpl = SG_PRE if kind == PRE else SG_PQ
    guide = tpl.format(links=LINKS_COMMON)
    assert s.count('<div class="container">') == 1, fname
    s = s.replace('<div class="container">', '<div class="container">\n' + guide, 1)

    # 5. bankquiz 錨點 + 詞彙卡區 + 上下頁導覽
    tail = ""
    if bq:
        tail += '<section id="bankquiz"></section>\n'
    tail += """<section id="cards">
  <div class="section-number">CARDS · 關鍵詞彙卡</div>
  <h2>關鍵詞彙卡：點卡片翻面</h2>
  <p>先看正面術語，心中默想定義再翻面對答案；洗牌後再過一輪，直到每張都能不假思索說出來。</p>
  <div class="fc-controls">
    <button id="fcShuffle">🔀 洗牌</button>
    <button id="fcFlipAll">全部翻面</button>
    <button id="fcUnflip">全部翻回</button>
  </div>
  <div class="fc-grid" id="fcGrid"></div>
</section>
"""
    nav_items = []
    if prev:
        nav_items.append(f'<a class="prev" href="{prev}.html"><div class="nav-dir">◂ 上一頁</div>'
                         f'<div class="nav-title">{PREV_LABEL[prev]}</div></a>')
    else:
        nav_items.append("<span></span>")
    nav_items.append('<a class="home" href="index.html"><div class="nav-dir">INDEX</div>'
                     '<div class="nav-title">章節總覽</div></a>')
    if nxt:
        nav_items.append(f'<a class="next" href="{nxt}.html"><div class="nav-dir">下一頁 ▸</div>'
                         f'<div class="nav-title">{nxt_label}</div></a>')
    else:
        nav_items.append("<span></span>")
    tail += f'<div class="chapter-nav">{"".join(nav_items)}</div>\n'

    m2 = re.search(r"</div>(?:\s*<!--[^>]*-->)?\s*<footer>", s)
    assert m2, f"{fname}: container/footer boundary not found"
    s = s[:m2.start()] + tail + s[m2.start():]

    # 6. JS 引擎（詞彙卡陣列留空，由 apply_zh.py 灌資料）
    js = "\nconst FLASHCARDS = [];\n" + SITE_JS
    if bq:
        js += QUIZ_JS
    assert s.count("</body>") == 1, fname
    s = s.replace("</body>", f"<script>{js}</script>\n</body>")

    path.write_text(s)
    print(f"ok {fname}: fc={fc} bq={bq or '-'} prev={prev or '-'} next={nxt or '-'}")


if __name__ == "__main__":
    for e in PPAGES:
        inject(e)
