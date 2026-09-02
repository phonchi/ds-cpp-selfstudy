# 資料結構 × C++ 互動自學網站

NSYSU 資料結構課程（MATH208）的互動自學配套網站：三章課前準備 ＋ 九章互動教材 ＋ 九頁選讀先備知識，
每一節都能動手操作、預測、驗證，配上每節 quiz、關鍵詞彙卡（flashcards）與 REF 速查表。

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

複習課程「預設你已經會」的 C++。全部程式碼範例都以 `g++ -std=c++17` 實際編譯執行過，
並直接引用課程的 `pythonds3/cppds/` 標頭檔（[phonchi/pythonds3](https://github.com/phonchi/pythonds3)）。

| # | 頁面 | 內容 |
|---|------|------|
| P1 | [C++ 基礎與編譯流程](p1_cpp_basics.html) | 編譯四階段、靜態型別、整數除法、讀懂 g++ 錯誤訊息 |
| P2 | [流程控制](p2_flow_control.html) | 短路求值、if／switch、while／for、範圍 for 的 `&` |
| P3 | [函式](p3_functions.html) | 傳值 vs 傳參考 vs 傳指標、`const T&`、遞迴與呼叫堆疊 |
| P4 | [陣列、指標與動態記憶體](p4_pointers_memory.html) | `&x`、`*p`、`NULL`、`a[i]` 就是 `*(a+i)`、`new`／`delete`、三種災難 |
| P5 | [vector 與 string](p5_vector_string.html) | 增刪成本、容量與攤還、iterator 失效、二維 vector |
| P6 | [map、set 與迭代器](p6_map_set.html) | `m[k]` 的陷阱、紅黑樹 vs 雜湊表、迭代器 |
| P7 | [檔案與例外](p7_files_exceptions.html) | `ifstream`／`ofstream`、`try`／`catch`、`at()` vs `[]` |
| P8 | [物件導向（基礎）](p8_oop_basics.html) | class、建構式與 `this`、封裝、`operator<<`、組合 |
| P9 | [物件導向（進階）](p9_oop_advanced.html) | 繼承、`virtual` 與多型、`operator<`、組合 vs 繼承、template |

課程全程用了 218 次 `new`、114 次 `NULL`，光第 09 章一章就有 102 個 `new`，
所以 **P4 是最該讀的一頁**；其次是 P8／P9，第 04 章之後每個資料結構都是一個 `class`。

頁面以單檔 HTML 與原生 JS 為主；00C 另引用三張有來源標註的本地官方介面截圖。
詞彙卡與自測題取自課程題庫並譯為繁體中文（母檔在 `data/flashcards_zh/`、`data/questions_zh/`，
詞彙卡正面採「中文（English）」格式；改內容請改母檔後跑 `tools/apply_zh.py`）。

## 維護

| 腳本 | 用途 |
|------|------|
| `tools/apply_zh.py` | 從 `data/` 重新灌入各頁的詞彙卡與題庫自測區（冪等） |
| `tools/inject_prereq_cpp.py` | 課前章與先備頁的尾段注入（導讀框、詞彙卡區、上下頁導覽），冪等 |
| `tools/check_links_cpp.py` | 全站錨點、頁面連結與注入前置條件檢查 |
| `tools/check_00c.py` | 解析 00C 三份 JSON、核對圖片與範圍，並編譯三種匿名專案模式 |
| `tools/enrich/enrich_lib.py` | 頁面同格式 C++ 上色、講義範例卡、插入器，以及 `run_cpp()`（編譯執行取真實輸出） |
| `tools/enrich/enrich_*.py` | 九章正課頁的一次性充實腳本，靠 `dx-*` 標記冪等 |

新增一頁的流程：撰寫頁面本體 → 在 `inject_prereq_cpp.py` 的 `PPAGES` 登記 → 跑該腳本 →
在 `apply_zh.py` 的 `FC`／`BQ` 登記並補上 `data/` 母檔 → 跑 `apply_zh.py` → 跑 `check_links_cpp.py`。
`FC`／`BQ` 的條目要跟頁面同批進 commit，先加會讓 `apply_zh.py` 找不到頁面而中斷。

00C 另有 Windows CI：`check-00c-windows.yml` 會在 MSYS2 UCRT64 安裝 GCC/GDB，執行
`tools/check_00c.py --require-gdb`，並額外驗證 GDB batch session 與 `-lgdi32` 連結。
