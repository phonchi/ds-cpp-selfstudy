# 資料結構 × C++ 互動自學網站

NSYSU 資料結構課程（MATH208）的互動自學配套網站：三章課前準備 ＋ 九章互動教材 ＋ 九頁選讀先備知識，
透過範例與互動練習預測、驗證程式行為，各頁提供自測、關鍵詞彙卡（flashcards）與 REF 速查表。

- 線上閱讀：https://phonchi.github.io/ds-cpp-selfstudy/
- 教科書：[cppds — Problem Solving with Algorithms and Data Structures using C++](https://runestone.academy/ns/books/published/cppds/index.html)（[原始碼](https://github.com/pearcej/cppds)）
- 課程講義：[nsysu-math208](https://github.com/phonchi/nsysu-math208)（各章提供 GitHub Pages 講義 HTML／PDF 線上閱讀與 PDF 下載）

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

最新語氣、課程殘留與先備銜接複查見[讀者審查紀錄](docs/prereq-language-reader-review.md)。

給學過程式、初學 C++ 的讀者，不要求 Python 或課本前提。以改寫前完整先備教材為範圍，
保留重要 C++ 主題與說明深度，依先備關係重排並換成獨立例子。每節包含用途、語法拆解、
逐步推理、完整程式、錯誤對照與帶理由的練習；主要說明直接展開。

| 頁面 | 主題 |
|---|---|
| P1 基礎與編譯 | 程式骨架、四階段、型別與初始化、I/O、運算、轉型、溢位與錯誤診斷 |
| P2 流程控制 | 短路、分支與 switch、while/do-while/for、跳躍、巢狀迴圈與成本 |
| P3 函式與參考 | 引數/參數、回傳、作用域、宣告、傳值與參考、回傳生命週期、多載、遞迴 |
| P4 陣列、指標與記憶體 | 指標與目標、算術與退化、三種參數傳遞、stack/heap、配置釋放與所有權 |
| P5 vector 與 string | 初始化、增刪成本、容量與攤還、三種走訪、失效、二維資料、序列容器與文字 |
| P6 map、set 與迭代器 | pair、查詢副作用、有序/無序、structured binding、安全 erase、計數去重分組 |
| P7 檔案與例外 | 路徑與模式、逐行解析、stream state、RAII、例外傳遞、at/[] 與處理邊界 |
| P8 類別與物件 | ctor、封裝與 const、this/物件連結、複製解構、operator<</friend、組合與多檔 |
| P9 類別延伸與模板 | 繼承多型、抽象介面、模板、運算子、比較/雜湊、priority_queue、資源複製與自訂例外 |

本版以 `b97fe81` 的九頁 HTML 與題卡母檔重新開始，保留原版圖表與互動。修正與獨立審查見[原版恢復紀錄](docs/prereq-original-restoration.md)。

頁面以單檔 HTML 與原生 JS 為主；00C 另引用三張有來源標註的本地官方介面截圖。
先備頁的自測題與詞彙卡依新正文編寫，正課頁維持課程題庫來源。
兩者的母檔均在 `data/flashcards_zh/`、`data/questions_zh/`。先備與正課字卡正面均使用「中文（English term／C++ identifier）」格式，不能只有單語。先備選擇題一律四個選項、唯一正解與逐項理由。
改內容時同步更新母檔，再用 `tools/apply_zh.py --pages p1 p2` 指定重生對應頁面。

## 維護

最近的全站修正：[三類錯誤、繁體用字與語法銜接](docs/error-teaching-review-20260913.md)，包含程式實跑與桌面／手機驗證紀錄。

| 腳本 | 用途 |
|------|------|
| `tools/apply_zh.py` | 從 `data/` 重生詞彙卡與題庫自測區（冪等）；`--pages p1,p2` 限定頁面，省略則全站 |
| `tools/inject_prereq_cpp.py` | 課前章與先備頁的尾段注入（導讀框、詞彙卡區、上下頁導覽），冪等 |
| `tools/check_links_cpp.py` | 全站錨點、頁面連結與注入前置條件檢查 |
| `tools/check_prereq_fidelity.py` | 直接對照 b97fe81 的章節順序、表格結構、SVG 幾何及重要概念；不能取代原稿閱讀 |
| `tools/check_prereq.py` | 編譯執行先備頁完整範例、核對輸出與 JSON、檢查 inline JS 及指向先備頁的跨頁錨點 |
| `tools/check_prereq_runtime.py` | 在暫存目錄實跑原版完整 C++ 程式，區分危險反例與預期失敗，支援 JSON 報告 |
| `tools/check_prereq_browser.py` | 驗證原版播放器各步驟、滑桿、每題四個選項、詞卡與桌面手機版面 |
| `tools/prereq_authoring.py` | 舊改寫的輔助程式；不得用來覆蓋目前恢復的 P1–P9 原版互動 |
| `tools/check_00c.py` | 解析 00C 三份 JSON、核對圖片與範圍，並編譯三種匿名專案模式 |
| `tools/enrich/enrich_lib.py` | 頁面同格式 C++ 上色、講義範例卡、插入器，以及 `run_cpp()`（編譯執行取真實輸出） |
| `tools/enrich/enrich_*.py` | 九章正課頁的充實腳本，靠 `dx-*` 標記冪等（已注入完畢，**不要重跑**）。例外：`enrich_analysis.py` 自 2026-09-19 起改為可重跑，區塊包在 `<!-- gen:name -->` 註解之間，重跑只替換註解內的內容 |
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
python3 tools/check_prereq_runtime.py
python3 tools/check_links_cpp.py
python3 tools/check_contrast.py
```

`check_prereq.py` 需要 Python 3、g++ 與 Node.js，不改動網站；程式範例在獨立暫存目錄執行，
讀寫檔範例不會產生檔案到 repo。原版 `.pseudo-code` DIV 的完整程式也會檢查，刻意錯誤與多檔範例由 contract 明列；新增可執行 `<pre>` 可使用 `data-cpp="run"`、`data-expected`，
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

本版的獨立閱讀審查與驗證範圍見[原版恢復紀錄](docs/prereq-original-restoration.md)。較早的改寫紀錄只保留歷史用途。

多檔程式的每個 `<pre>` 標成 `data-cpp="file"`，用相同 `data-example` 分組，
`data-filename` 指定實際檔名；其中一檔提供 `data-expected`（及需要時的 `data-stdin`）。
檢查器建立真實檔案，將同組 `.cpp` 一起編譯，不以合併成單檔代替多檔驗證。

本次直接從原 commit 恢復；先前 fidelity/coverage 紀錄描述的是已被取代的版本。

```sh
python3 tools/check_prereq_fidelity.py
python3 -m unittest discover -s tests -v
```

`write_page` 如需編寫新頁，必須明確提供該頁 `hero_svg`，不允許再默默生成缺圖章首。
本次先還原原稿，再替換課本案例與必要的錯誤敘述。`data/prereq_fidelity_contract.json` 指定原 commit、
允許的搬移與程式檢查分類；不得改成只對照重寫後的新快照，也不得為了通過檢查而任意新增例外。
計時等非固定輸出可使用 `data-expected-pattern` 作完整匹配，另以 `data-output-example` 顯示清楚標示的示例，
不能把某次時間或跨平台亂數序列當保證。
