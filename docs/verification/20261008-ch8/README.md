# 第 8 章 graphs 依講義擴充驗收（2026-10-08）

## 範圍

來源：`/home/phonchi/ds_cpp/Slides/08_Graphs and Graphing Algorithms.ipynb`、`questions/ch8/*.json`、`pythonds3/cppds/{graph,graph_algos}.hpp`、講義圖 `nsysu-math208/static_files/presentations/imgs/`。

修改／新增：

- `graphs.html`
- `tools/enrich/enrich_graphs.py`：改寫為 gen 驅動、冪等的 driver（舊的 `insert_end_of_section` 注入全部移除）
- `tools/enrich/content/graphs_depth.py`（新，19 個 gen 區）、`graphs_programs.py`（新，講義程式由 notebook 逐字取出、標頭片段、OUT）、`graphs_figures.py`（新，58 張圖的 figure spec）
- `assets/figures/ch8/`：58 張講義圖
- `data/flashcards_zh/ch8.json`：29 → 35 張（原 29 張已對應講義 Key terms 29 個詞；新增回溯、轉置圖、邊鬆弛、過期項目、安全邊、TTL；「搜尋樹」定義改為本章的 BFS/DFS 搜尋樹）
- `data/questions_zh/ch8.json`：講義的 6 題已放進正文對應的節，章末 bankquiz 換成另出的 8 題（不重複）

一次性腳本（各只執行一次，內含防重跑保護）：

1. `reorder_sections.py`：節次改為講義順序 prologue → representation → word-ladder → bfs → knight → dfs → topsort → scc → dijkstra → prim（exercises、reference 在後）。每塊從 banner 註解到 `</section>` 整塊搬移，id、DOM、widget 不變；PART 編號、banner、float-nav、目錄、BFS 框內「回頭讀 PART 08」同步改號。scratch 複本的排序後 diff（`reorder-sorted-diff.txt`）只有重新編號的行。
2. `place_markers.py`（gen 區外的一次性手改，逐項）：
   - 放置 19 對 `<!-- gen:graphs-* -->`。
   - 移除舊 enrich 注入的 dx-rep／dx-bfs／dx-dfs／dx-dij／dx-prm 卡（id `dx-rep`、`dx-bfs`、`dx-dfs`、`dx-dij`、`dx-prm` 由 gen 區重建）。
   - 由 gen 重寫並移除的手寫段落：representation 開頭段與 C++ 實作小節、word ladder 開頭到 bucket 框、BFS 的複雜度框與兩性質框、knight 開頭四段與「為什麼選鄰居最少」框（內容併入 gen）、DFS 開頭段與欄位框（原寫 `discovery_time/closing_time`，改用標頭的 `discovery/closing`）、Dijkstra 開頭段與負權重框（Bellman-Ford 改為（補充）收合）、Prim 開頭段與三個框、REF 的兩張對照表（改為（補充）收合）、三色圖例（改為（補充）收合）。
   - 原地小改：prologue h3 改「互動：標出路徑與循環」；DFS 框「(line 4)」刪除、`for v : graph`→`for (auto& p : vertices)`、`queue.enqueue(neighbor)`/`dfsVisit(neighbor)`→`vertQueue.push(n.first)`/`dfsVisit(n.first)`；拓撲排序 `dfs(g)`→`g.dfs()`；Dijkstra「第 9–13 行」改為描述、「PDF 上的標準範例」→「講義的路由範例圖」；exercises 的 h2 改「練習：Prim 加入的最後一條邊」，目錄與 float-nav 的 EX 標籤同步。
   - 五個動畫程式面板改用講義／標頭名稱：`bfs`、`dfs`/`dfsVisit`（DFSGraph 成員）、`knightTourWarnsdorff`、`dijkstra`、`prim`，內容照標頭；JS 用到的 `data-l` 值（bfs 6/8/10/11/15、dfs 2/6/9/12/13/16、dij 4/6/7/10/11、prim 5/8/10/11/13）放在對應行，JS 未改。
   - `ts1`、`scc1` 兩題由三選一補成四選一，每個選項有 `data-fb`；`quizCheck` 改為通用寫法（讀 `data-fb`），原本寫死在 JS 裡的四題回饋移到選項上。
   - 練習 1 移到 Dijkstra 節末（講義位置），練習 2 留在 exercises 節；兩題改用講義原圖 Dij.png、primq.png，刪除重繪用的 `ex1Config/ex2Config/ex1R/ex2R` 與 `canvas-ex1/2`。
   - 新增 `<section id="recap">`（gen `graphs-recap`）與 float-nav、目錄的 SUM 連結；使用方式 ② 改寫（原句要學生回講義看完整程式）、④ 加回顧連結。
3. driver 每次執行另外更新詞彙卡張數與自我檢測題數標籤，並在 `graphs-depth-style` 加 `.slider-row{flex-wrap:wrap}`（騎士動畫在 390 寬、5×5 狀態下原本會溢出 2px）。

未呼叫 `chapter_math.render_math`、`course_recordings.apply_recording`；`teaching_copy.EDITS['graphs']` 仍為空清單。

## 結果（全部實際執行，紀錄見 `run.log`）

| 項目 | 結果 |
|---|---|
| C++（`g++ -std=c++17 -Wall -Wextra -pedantic -I/home/phonchi/ds_cpp/Slides`） | 12 個 `data-cpp="run"`（講義 10 個程式＋拓撲排序、練習 1 兩個（補充））全部無警告編譯，輸出與 `data-expected` 及頁面顯示逐字相同（`content-results.json`）。本章沒有 compile-error 區塊；其餘 18 個為 fragment／header |
| 冪等：`pipeline.sh`（enrich_graphs → `apply_zh.py --pages graphs` → `shuffle_quiz.ensure`）連跑兩次 | sha256 相同（最終 e1966e58…）。已用主控更新後的 apply_zh（隨堂自測徽章）。瀏覽器檢查跑在前一版（497e40a2…），之後只改了騎士節一句文字，已重跑冪等與 C++ 檢查 |
| 重複 id／懸空錨點／img 屬性與檔案／inline script `node --check`／每節有 h3（cards、bankquiz 除外）／quiz 四選一且每選項有回饋 | 0 錯誤 |
| `tools/check_links_cpp.py`、`tools/check_contrast.py` | 0 錯誤／0 警告；0 失敗 |
| Chromium 1440、390（`check_browser.py`） | 48 個 details 全展開；58 張圖 naturalWidth>0；intro／相鄰表示高亮可用；bfs、word ladder、dfs、dijkstra、prim 五個控制器從頭單步到底，每步檢查程式面板高亮行的 data-l 與 codeLine 相同，再以最快速度播放到結束；騎士 5×5 Warnsdorff 播放到 SUCCESS，關閉 Warnsdorff 時播放 20 步後跳到最後一步（共 9,996 步）也 SUCCESS；拓撲排序與 SCC（player-v2）三個階段播完，單步、暫停可用；10 題頁內 quiz 答錯／答對皆有回饋；8 題 bankquiz、35 張字卡（翻面、全翻、洗牌）可用；無水平溢出、無 page error。截圖 `graphs-{knight,dijkstra}-{1440,390}.png` |

## 密度（`density.py`）

| 指標 | 前 | 後 | 第 1–3 章 |
|---|---|---|---|
| 可見文字 | 18,681 | 46,499（收合區外 28,933） | 22k–34k |
| h2／h3 | 14／11 | 15／49 | — |
| img | 0 | 58 | 0–6 |
| details | 0 | 48 | 0–28 |
| .pseudo-code | 12 | 37 | 19–42 |
| 收合區外的預期輸出 | 5 | 10 | 10–21 |
| data-cpp 區塊 | 0 | 30 | — |
| quiz | 4 | 10 | — |
| 字卡 | 29 | 35 | — |

總文字超出基準，主要是收合的講義程式；收合區外約 29k。可見輸出 10 段就是講義全部 10 個可執行程式，未另加湊數。圖多是因為逐步序列（gendfs 12 張、prim 7 張、dijkstra 6 張、ktdfs 6 張）各只放 1–2 張可見，其餘收進「逐步圖」。

## speak-human-tw 潤稿摘要（非互動，事後摘要）

這次找到並修改 6 處：「原圖的大結構一目了然」→「比較容易看出原圖的整體結構」；「這張圖其實是用有向邊」刪「其實」；「BFS 不只解決了…還順便解決了…」→「跑完這次 BFS，除了…，其他單字的問題也一起解決了」；「正是我們要的」→「適合這個問題」；「其實更簡單」→「反而更簡單」；「關鍵在 Prim…」→「原因是 Prim…」。程式碼、輸出、數字與連結未動。

## 限制與講義端不一致

- 瀏覽器測試封鎖外部請求，MathJax 與字型未載入，未驗證公式排版。
- 講義投影片的 `Vertex`/`Graph`（含 `getNeighbor/setNeighbor/contains`）與實際 include 的 `graph.hpp` 不同；頁面兩者都列，並說明程式用的是標頭版。
- 講義 Warnsdorff 版的投影片仍叫 `knightTour`，執行的程式呼叫標頭的 `knightTourWarnsdorff`；頁面列標頭版並說明。
- 講義 bfs 投影片沒有重設與起點塗灰，標頭版有；頁面兩者都列。
- 講義 Key terms 的 Search Tree 定義是 BST 式的，不符本章用法；字卡已改寫，講義端可考慮修正。
- 講義圖 bfs1–3、pancakesDFS 依課本的鄰居順序，與 C++ map 的字母順序不同；圖說與輸出說明有交代。ktdfse 圖中 C 仍為灰色，與程式（回溯時塗回白色）不符，圖說已註明。
- 頁面 SCC 動畫用自有的 8 頂點圖，講義 scc1 是 9 頂點圖；講義圖另外放在動畫前。
- 騎士動畫沒有單步鍵（既有設計，未改）；暴力 8×8 的 C++ 程式不放在頁面（實際執行一分鐘內跑不完，本頁只放 5×5）。
- 動畫 JS 註解中的「PART 0x」舊編號未改（不影響顯示）。

## 2026-10-09 潤稿

speak-human-tw 潤稿有 26 處直接改在 `graphs.html` 的 gen 區外（資訊框、目錄、導覽、節標、頁內 quiz 標題、比較表表頭），逐條見 `docs/verification/20261009-polish/ch8-polish.md`。這些文字不會被產生器覆蓋。

## 2026-10-09 讀者審閱修正（gen 區外）

- PART 00 關鍵概念面板：Path 補「互不相同」，Cycle 改成封閉序列 $(w_1, \ldots, w_n, w_1)$ 的定義，Tree 補「無向圖」。其餘修正都在產生器來源，見 `docs/verification/20261009-reading/fixes-ch7-9.md`。
