# 第 7–9 章讀者審閱修正（2026-10-09）

依 `readerB-ch7-9.md` 的「決定」欄修正 24 項。未 commit。

## 第 7 章 searching_sorting.html

| # | 修法 | 檔案 |
|---|---|---|
| 1 | 刪掉 legacy 的 info-box「比較次數對照表」，保留 depth 的表（用語是「值在／值不在（未排序／已排序）」）；info-box 末句「兩種版本的大 O 都是 O(n)…下一節的二分搜尋」改成段落保留 | `search_legacy.py` |
| 2 | 改成「最多 $\lfloor \log_2 n \rfloor + 1$」；10⁶ 的例子改成「最多只要 $\lfloor \log_2 10^6 \rfloor + 1 = 20$ 次」 | `search_legacy.py` |
| 3 | 快速排序列：需求改「可交換（本章的 partition 用左右雙指標）」，array 欄 ✓，linked 欄「△ 需改寫 partition」，原因改成「本章的雙指標 partition 要從右往左走…需改用由左往右的單向掃描」。希爾排序列：「△ 可做但很慢」，原因改成每次都得從頭走過去才能跳 gap 格。△ 圖例改「可以，但效能下降或要改寫部分步驟」。info-box 標題改成「為何 Quick Sort 用在 Singly Linked List 要改寫 partition」，內文補上 Lomuto 式單向掃描可行，並說明快速排序本身仍做得到 | `search_legacy.py` |
| 4 | 改成「（本章的版本每一輪找最大值，放到未排序區的尾端。）」 | `search_legacy.py` |
| 5 | shell 面板標題改「虛擬碼」 | `search_legacy.py` |
| 6 | shell 統計欄「交換」改成「位移」（`genShellSort` 的 `swp` 本來就是在位移時加一） | `search_legacy.py` |
| 7 | 改成 $\sum (i+1) \cdot \text{ord}(c_i) \bmod m$，和 `hashStrWeighted` 的 `int(i + 1)` 一致 | `search_legacy.py` |
| 8 | `// partition, quickSortHelper, quickSort (header listing above)`、`// partitionDesc, quickSortHelperDesc, quickSortDesc (header listing above)`，對應上方 `sorting.hpp` 的兩張標頭卡 | `search_programs.py` |
| 9 | TOC 末段改成 REF → SUP → SUM → QUIZ → CARD（在 gen 區外，直接改頁面；pipeline 重跑後仍在） | `searching_sorting.html` |
| 10 | reference 表的平均欄改「依 gap 序列而定 †」，下方註腳說明本章用 n/2 折半增量最差 $O(n^2)$，Hibbard 序列 $2^k-1$ 最差 $O(n^{3/2})$ | `search_legacy.py` |

## 第 8 章 graphs.html

| # | 修法 | 檔案 |
|---|---|---|
| 1 | 已看過圖：圖中佇列確實畫成 pole、pall。alt 改成「圖中佇列畫成 pole、pall，這是原圖的錯誤，正確內容是 poll、fail」；figcaption 補一句說明佇列應為 poll、fail。圖檔未動 | `graphs_figures.py` |
| 2 | scc1b 圖說改「在轉置圖 Gᵀ 上跑 dfs()」 | `graphs_figures.py` |
| 3 | 關鍵概念面板（gen 區外）：Cycle 改成「回到起點的封閉序列 $(w_1, \ldots, w_n, w_1)$，其中 $w_1, \ldots, w_n$ 互不相同」；Path 補上「互不相同」，Tree 補上「無向圖」，和正文定義一致 | `graphs.html` |
| 4 | dfs：兩段合併成一段，刪掉第二段（「盡量往深處搜尋…必要時才分岔」併入第一段）。topsort：刪掉圖後段落裡重複的定義與三個應用例，只保留看圖的觀察，改成「要決定每個步驟的確切順序，就用上面介紹的拓撲排序」 | `graphs_depth.py` |
| 5 | ktdfse 的 alt 補上「圖中 C 仍畫成灰色，但程式回溯時已把 C 塗回白色」 | `graphs_figures.py` |
| 6 | 改寫成：數字是第幾步走到；四個角落分別在第 0、15、21、46 步走到，沒有一個留到最後；最後的 61、62、63 步都落在棋盤中間（已對照預期輸出） | `graphs_depth.py` |
| 7 | 改成「C、D、E 都可以更新：經 B 到 C 只要 1，比原本經 A 的 3 便宜；D 和 E 則是第一次得到距離。三者的 previous 都改指向 B。」與 primb 圖說一致 | `graphs_depth.py` |
| 8 | 「樹」：連通、無循環的無向圖；「無控制氾濫」：每台路由器收到訊息後轉送給所有相鄰的路由器並把 TTL 減一。JSON 保持一行一張卡的原格式 | `data/flashcards_zh/ch8.json` |
| 第 7 章 #8 的 ch8 部分 | `// Vertex, Graph (graph.hpp listing above)`、`// DFSGraph: dfs, dfsVisit (DFSGraph listing above)`、`// dijkstra (dijkstra listing above)`、`// prim (prim listing above)` | `graphs_programs.py` |

## 第 9 章 trees.html

| # | 修法 | 檔案 |
|---|---|---|
| 1 | 「第 7 章與本章我們學了四種實作 map ADT 的方式」 | `trees_legacy.py` |
| 2 | 已看過 buildExp1–3：空根 → 讀 ( → 讀 3。圖說改「從空的根開始，讀入 ( 與 3 之後、讀 + 之前的狀態」 | `trees_depth.py` |
| 3 | 舊 info-box 已併入新 info-box（見 #4），新文字用 `percDown`；主 script 中 heap 動畫的三則狀態訊息 `perc_down` 也一併改成 `percDown`，頁面不再出現 `perc_down` | `trees_depth.py`、`trees.html`（主 script） |
| 4 | 刪除 `{{slot:perc}}` 後的 info-box，把它和 heapify 程式後的推導段落合併成一個 info-box「為什麼 buildHeap 是 O(n) 而不是 O(n log n)？」，放在 heapify 程式之後；操作表補一列 `print()`（依 vector 順序印出所有鍵，以空白分隔，與 `binaryheap.hpp` 實作一致） | `trees_legacy.py`、`trees_depth.py` |
| 5 | bst-analysis 表「del」改 `remove` | `trees_legacy.py` |
| 6 | 字卡正面改「由下往上建堆（Bottom-up buildHeap）」 | `data/flashcards_zh/ch9.json` |

## 驗證

- pipeline 連跑兩次，sha256 相同：
  - `searching_sorting.html` `7d50c2b3…95c0`
  - `graphs.html` `74f35246…ea52`
  - `trees.html` `8dadbc62…d26e`
- `check_content.py`：ch7 run 22/22、ch8 run 12/12、ch9 run 15/15，errors 0（compile_error 是填空題，本來就預期編譯失敗）。`content-results.json` 只有暫存路徑改變，已用 `git checkout` 還原。
- 保真比對（對 HEAD）：`data-expected`、`pre`、`id` 完全相同；`pseudo-code` 只有 6 行 include 註解不同；`href` 只有第 7 章 TOC 的順序不同。
- `python3 tools/check_links_cpp.py`：22 頁，0 錯誤、0 警告。
- 三頁 15 段 inline script 都通過 `node --check`。
- `check_browser.py`（1440／390）：三章都沒有 page error、沒有溢出、圖都載入；所有面板都能播完（ch7 shell 播完顯示「26 次比較、10 次位移」，ch9 heapify 狀態列顯示 percDown）。結果另存在 `fixes-ch7-9-browser/`；`20261008-chN/` 裡被覆寫的截圖與 browser-results.json 已還原。
- shell 面板 Playwright（`fixes-ch7-9-browser/ch7-shell-panel.json`）：統計欄標籤是「位移」，標題是「虛擬碼」，單步與播放都正常，播完位移數 10；TOC 末六項與 DOM 的 section 順序一致。

## 備註

- 工作目錄裡 `recursion.html`、`recursion_*.py` 的修改是另一個 agent 在處理第 4–6 章，不是這次的改動。

- 三章的 gen 區外手改已補記到 `docs/verification/20261008-chN/README.md` 末尾。
