# 資料結構 × C++ 互動自學網站

NSYSU 資料結構課程（MATH208）的互動自學配套網站：兩章課前準備 ＋ 九章互動教材，
每一節都能動手操作、預測、驗證，配上每節 quiz、關鍵詞彙卡（flashcards）與 REF 速查表。

- 線上閱讀：https://phonchi.github.io/ds-cpp-selfstudy/
- 教科書：[cppds — Problem Solving with Algorithms and Data Structures using C++](https://github.com/pearcej/cppds)
- 課程講義：[nsysu-math208](https://github.com/phonchi/nsysu-math208)（各頁「講義 PDF」連結來源）

## 課前準備（先讀）

| # | 頁面 | 內容 |
|---|------|------|
| 00A | [AI 時代，為什麼還要學資料結構？](00a_why_code.html) | 能編譯 ≠ 跑得動、選錯容器兩端的代價、記憶體是你的責任 |
| 00B | [課前準備與環境安裝](00b_setup.html) | Jupyter + C++ kernel／VS Code／線上編譯器三路線、kernel 踩坑 FAQ |

課程 notebook 需要打過 `-I.` patch 的 C++ kernel（[phonchi/jupyter-cpp-kernel @ nsysu-math208](https://github.com/phonchi/jupyter-cpp-kernel/tree/nsysu-math208)，
fork 自 shiroinekotfs，MIT）；PyPI 上的原版缺這一行，`#include "dscpp/…"` 會找不到檔案。安裝方式見 00B。

## 章節（授課順序）

| # | 頁面 | 對應 |
|---|------|------|
| 01 | [C++ 導論](introduction.html) | cppds Ch.1 |
| 02 | [演算法分析](analysis.html) | cppds Ch.2 |
| 03 | [陣列與稀疏矩陣](arrays.html) | 附錄 A（講義 03） |
| 04 | [鏈結串列](linked_lists.html) | cppds Ch.4 |
| 05 | [堆疊、佇列與 Deque](linear_structures.html) | cppds Ch.3 |
| 06 | [遞迴](recursion.html) | cppds Ch.5 |
| 07 | [搜尋與排序](searching_sorting.html) | cppds Ch.6–7 |
| 08 | [圖與圖演算法](graphs.html) | cppds Ch.9 |
| 09 | [樹與樹演算法](trees.html) | cppds Ch.8 |

每頁皆為單檔自足 HTML（互動元件為原生 JS，僅外連 MathJax 與 Google Fonts CDN）。
詞彙卡與自測題取自課程題庫並譯為繁體中文（母檔在 `data/flashcards_zh/`、`data/questions_zh/`，
詞彙卡正面採「中文（English）」格式；改內容請改母檔後跑 `tools/apply_zh.py`）。

## 維護

| 腳本 | 用途 |
|------|------|
| `tools/apply_zh.py` | 從 `data/` 重新灌入各頁的詞彙卡與題庫自測區（冪等） |
| `tools/inject_prereq_cpp.py` | 課前章與先備頁的尾段注入（導讀框、詞彙卡區、上下頁導覽），冪等 |
| `tools/check_links_cpp.py` | 全站錨點、頁面連結與注入前置條件檢查 |
| `tools/enrich/enrich_lib.py` | 頁面同格式 C++ 上色、講義範例卡、插入器，以及 `run_cpp()`（編譯執行取真實輸出） |
| `tools/enrich/enrich_*.py` | 九章正課頁的一次性充實腳本，靠 `dx-*` 標記冪等 |

新增一頁的流程：撰寫頁面本體 → 在 `inject_prereq_cpp.py` 的 `PPAGES` 登記 → 跑該腳本 →
在 `apply_zh.py` 的 `FC`／`BQ` 登記並補上 `data/` 母檔 → 跑 `apply_zh.py` → 跑 `check_links_cpp.py`。
`FC`／`BQ` 的條目要跟頁面同批進 commit，先加會讓 `apply_zh.py` 找不到頁面而中斷。
