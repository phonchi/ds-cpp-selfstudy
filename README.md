# 資料結構 × C++ 互動自學網站

NSYSU 資料結構課程（MATH208）的互動自學配套網站：三章課前準備 ＋ 九章互動教材 ＋ 九頁選讀先備知識，
透過範例與互動練習預測、驗證程式行為，各頁提供自測、關鍵詞彙卡（flashcards）與 REF 速查表。

- 線上閱讀：https://phonchi.github.io/ds-cpp-selfstudy/
- 教科書：[cppds — Problem Solving with Algorithms and Data Structures using C++](https://github.com/pearcej/cppds)
- 課程講義：[nsysu-math208](https://github.com/phonchi/nsysu-math208)（各頁「講義 PDF」連結來源）

## 課前準備（先讀）

| # | 頁面 | 內容 |
|---|------|------|
| 00A | [AI 時代，為什麼還要學資料結構？](00a_why_code.html) | 能編譯 ≠ 跑得動、選錯容器兩端的代價、記憶體是你的責任 |
| 00B | [課前準備與環境安裝](00b_setup.html) | Windows 安裝 GCC/GDB、Jupyter + C++ kernel 完整流程與 kernel 踩坑 FAQ |
| 00C | [Windows VS Code 作業實戰](00c_vscode_windows.html) | C/C++ extension、三份 JSON、多檔編譯、執行參數與基本除錯 |

課程 notebook 需要打過 `-I.` patch 的 C++ kernel（[phonchi/jupyter-cpp-kernel @ nsysu-math208](https://github.com/phonchi/jupyter-cpp-kernel/tree/nsysu-math208)，
fork 自 shiroinekotfs，MIT）；PyPI 上的原版缺這一行，`#include "pythonds3/cppds/…"` 會找不到檔案。安裝方式見 00B。

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

## 先備知識（選讀，不列入評分）

給學過程式、初學 C++ 的讀者。先看這九頁再讀課本，不要求 Python 背景。
各節依「用途 → 語法拆解 → 小範例與結果 → 操作或練習」編排，完整範例只用標準 C++17，
不依賴課程標頭。P3 的函式與參考、P4 的指標、P8 的類別是重要基礎。

| # | 頁面 | 內容 |
|---|------|------|
| P1 | [C++ 基礎與編譯流程](p1_cpp_basics.html) | 最小程式、變數與初始化、型別、輸入輸出、運算與轉型、編譯錯誤 |
| P2 | [流程控制](p2_flow_control.html) | 比較與布林、if／switch、短路求值、while／for、break／continue |
| P3 | [函式與參考](p3_functions.html) | 定義與呼叫、參數與回傳、作用域、傳值、參考、const 參考、多載與預設引數 |
| P4 | [陣列、指標與動態記憶體](p4_pointers_memory.html) | 陣列、位址、指標、nullptr、指標與陣列參數、生命週期、new／delete |
| P5 | [vector 與 string](p5_vector_string.html) | 宣告與初始化、索引與增刪、範圍 for、auto、字串輸入與操作 |
| P6 | [map 與 set](p6_map_set.html) | 鍵值查詢與修改、缺鍵新增、去重、走訪與 pair |
| P7 | [檔案與例外](p7_files_exceptions.html) | 讀寫檔、getline、狀態檢查、try／catch／throw、at() |
| P8 | [類別與物件](p8_oop_basics.html) | class、成員、存取權限、建構式、const 成員函式、this、解構式 |
| P9 | [類別延伸與模板入門](p9_oop_advanced.html) | 基本繼承、virtual／override、基底參考、函式模板與類別模板 |

頁面以單檔 HTML 與原生 JS 為主；00C 另引用三張有來源標註的本地官方介面截圖。
先備頁的自測題與詞彙卡依新正文編寫，正課頁維持課程題庫來源。
兩者的母檔均在 `data/flashcards_zh/`、`data/questions_zh/`。先備頁以中文解釋術語、保留 C++ 關鍵字；
正課詞彙卡沿用「中文（English）」格式。
改內容時同步更新母檔，再用 `tools/apply_zh.py --pages p1 p2` 指定重生對應頁面。

## 維護

| 腳本 | 用途 |
|------|------|
| `tools/apply_zh.py` | 從 `data/` 重生詞彙卡與題庫自測區（冪等）；`--pages p1,p2` 限定頁面，省略則全站 |
| `tools/inject_prereq_cpp.py` | 課前章與先備頁的尾段注入（導讀框、詞彙卡區、上下頁導覽），冪等 |
| `tools/check_links_cpp.py` | 全站錨點、頁面連結與注入前置條件檢查 |
| `tools/check_prereq.py` | 編譯執行先備頁完整範例、核對輸出與 JSON、檢查 inline JS 及指向先備頁的跨頁錨點 |
| `tools/check_prereq_browser.py` | 用 Chromium 驗證九頁播放控制、題目回饋、詞彙卡、導覽及桌面／手機版面 |
| `tools/check_00c.py` | 解析 00C 三份 JSON、核對圖片與範圍，並編譯三種匿名專案模式 |
| `tools/enrich/enrich_lib.py` | 頁面同格式 C++ 上色、講義範例卡、插入器，以及 `run_cpp()`（編譯執行取真實輸出） |
| `tools/enrich/enrich_*.py` | 九章正課頁的一次性充實腳本，靠 `dx-*` 標記冪等（已注入完畢，不要重跑） |
| `tools/fix_bare_include.py` | 講義範例卡裸檔名 include 補 `pythonds3/cppds/` 前綴（冪等） |
| `tools/shuffle_quiz.py` | 頁內自測題選項固定種子洗牌 JS 注入（冪等，`inject_prereq_cpp.py` 會呼叫） |

新增一頁的流程：撰寫頁面本體 → 在 `inject_prereq_cpp.py` 的 `PPAGES` 登記 → 跑該腳本 →
在 `apply_zh.py` 的 `FC`／`BQ` 登記並補上 `data/` 母檔 → 跑 `apply_zh.py` → 跑 `check_links_cpp.py`。
`FC`／`BQ` 的條目要跟頁面同批進 commit，先加會讓 `apply_zh.py` 找不到頁面而中斷。

00C 另有 Windows CI：`check-00c-windows.yml` 會在 MSYS2 UCRT64 安裝 GCC/GDB，執行
`tools/check_00c.py --require-gdb`，並額外驗證 GDB batch session 與 `-lgdi32` 連結。

### 先備頁驗證

```sh
python3 tools/apply_zh.py --pages p1 p2 p3 p4 p5 p6 p7 p8 p9
python3 tools/check_prereq.py
python3 tools/check_links_cpp.py
python3 tools/check_contrast.py
```

`check_prereq.py` 需要 Python 3、g++ 與 Node.js，不改動網站；程式範例在獨立暫存目錄執行，
讀寫檔範例不會產生檔案到 repo。完整範例的 `<pre>` 使用 `data-cpp="run"`、`data-expected`，
需要輸入時加 `data-stdin`。預期編譯失敗的示例用 `data-cpp="compile-error"`；
語法骨架與片段用 `data-cpp="fragment"`，並在正文交代上下文，不將未定義行為當作固定輸出。

已注入頁面不會因修改 `SG_PQ` 自動更新導讀；修改既有頁面時應直接同步 HTML 與模板，
不要刪掉 `prereq-injected` 後重跑注入器。

瀏覽器驗收另需 Playwright 與已安裝的 Chromium：

```sh
python3 tools/check_prereq_browser.py
# 可選：只測指定頁面，並將截圖保存在指定目錄
python3 tools/check_prereq_browser.py --pages p3 p4 --screenshots /tmp/prereq-screenshots
```

瀏覽器檢查直接開啟本地頁面，阻擋外部請求，不需啟動網站伺服器。
它會加快互動計時器以驗證暫停、單步、重設、完成與重播，並檢查 1440px／390px 寬度的溢出。

本次全面改寫的獨立閱讀審查、問題修正與驗證範圍見[審查紀錄](docs/prereq-reader-review-20260906.md)。
