# 第 8 章 graphs.html：讀者 D 第二輪修正（2026-10-09）

依 `readerD-findings.md` 第 8 章 #1–#24 與 `readerD-ch7-9.md` 的決定修正。未 commit。

改動檔案：`graphs.html`（gen 區外的 HTML 與主 `<script>`）、`tools/enrich/content/graphs_depth.py`、`tools/enrich/content/graphs_figures.py`、`data/flashcards_zh/ch8.json`。

| # | 修法 | 檔案 |
|---|---|---|
| 1 | SCC：新增 `sccDfsComplete()`（所有頂點都有 closing time）。`sccStep2()` 在 ① 未播完時擋下並提示「① 的 DFS 還沒播完…」；`sccStep3()` 在未轉置時擋下，① 未播完時另給提示；已轉置後再按 ② 提示接著按 ③ | `graphs.html` script |
| 2 | 拓撲排序：新增 `tsDfsComplete()`，`tsOrder()` 在 ① 未播完時擋下並提示 | `graphs.html` script |
| 3 | 單步鍵改呼叫 `tsStep()`／`sccStep()`：還沒有 player 時建立 ① 並只前進一格（`tsRunDFS(false)`／`sccStep1(false)`）；SCC 在 ② 轉置後、③ 還沒開始時，單步會建立 ③ 並前進一格 | `graphs.html` |
| 4 | 起點選單：奇數邊長只列 (r+c) 為偶數的起點；7×7 的 (0,3) 換成 (0,2)，選單為 (0,0)、(0,2)、(3,3)、(6,6)。節點模擬顯示這 4 個起點 Warnsdorff 都走得完 | `graphs.html` script |
| 5 | 預設 5×5（`<select>` 與 `this.size`）。上限訊息依原因分三種：奇數邊長深色起點（沒有巡遊）、不用 Warnsdorff（大棋盤超過上限，比較請用 5×5）、其他；不再叫學生改用 Warnsdorff。窮舉失敗的訊息改為「這個起點沒有巡遊」。互動說明補上 5×5 最適合比較、6×6 以上不用 Warnsdorff 的情況、奇數邊長只給淺色起點的原因 | `graphs.html` script、`graphs_depth.py` |
| 6 | 改成「看完再回頭對照 PART 08 的 Dijkstra：它依已走成本決定搜尋順序；A* 是在這個優先順序上，再加上到終點的估計」 | `graphs.html` |
| 7 | 複雜度框拆成「放入 bucket $O(n\cdot L)$」與「同 bucket 兩兩連邊 $O(\sum_b\|b\|^2)$，最壞 $\Theta(n^2)$」，註腳補 $\|b\|$ 的意義 | `graphs.html` |
| 8 | 改寫成「核心差別在排程」：BFS 在 if 裡設 color／distance／previous 再放進佇列；DFS 只設 previous 就遞迴，著色與計時在 `dfsVisit` 開頭；另提 discovery／closing 與外層迴圈 | `graphs.html` |
| 9 | 「❌ 查特定邊是 $O(\log\deg(v))$，不是 $O(1)$」 | `graphs.html` |
| 10 | `#primCode` 的 `continue; // stale entry` 一行加 `data-l="9"`，`kind:'stale'` 的 codeLine 改 9 | `graphs.html` |
| 11 | 狀態列「標記為 visited」→「展開它的鄰居」；表格欄名 visited →「已展開」 | `graphs.html` script |
| 12 | 格內步數從 0 起算（成功畫面起點顯示 0）；統計改名「已走格數」；`#knightCode` 20 行加 `data-l`，start→3、move→10、back→14、success→19、fail→17，重置時清除 | `graphs.html` |
| 13 | 保留選單：標籤改「第一棵樹的根」，下方加一句說明 `dfs()` 一律依 key 順序挑根、這裡只改第一棵樹的根、選 A 與 `dfs()` 相同 | `graphs.html` |
| 14 | 側欄改「`d/f` 是 DFS 的 discovery／closing time」；初始與完成的狀態訊息同步改 discovery/closing | `graphs.html` |
| 15 | 互動前一段改「走一遍同樣的四個步驟」並說明按鈕對應；h3 改「互動：四個步驟走一遍」 | `graphs_depth.py` |
| 16 | 改寫成「這個式子的量級約是 $k^N$」，三個數字明寫為 $3.8^{25}$、$4.4^{36}$、$5.25^{64}$ 的值（已重算：3.12e14、1.46e23、1.23e46） | `graphs_depth.py` |
| 17 | 已看原圖：只有 14 個頂點、沒有 fall、sage 為灰色。alt 與圖說補上；fall 在程式的 BFS 樹裡掛在 fail 下（距離 3），所以輸出有 fall(3) | `graphs_figures.py` |
| 18 | 「後面的 BFS 與 DFS 會用…」 | `graphs_depth.py` |
| 19 | 刪除重複的收合區「一次 BFS 得到的兩樣東西（補充）」與 recap FAQ「為什麼 BFS 的路徑和題目開頭的解法不一樣？（補充）」（內容已在正文與 traverse 輸出說明中）。details 由 48 個變 46 個 | `graphs_depth.py` |
| 20 | 頁首使用方式 ② 補「標（補充）的內容是講義以外的延伸說明，跳過不影響主線」；練習 2 的「看完整的追蹤」改用 `fold`，標（補充） | `graphs.html`、`graphs_depth.py` |
| 21 | 補「佇列裡只剩 w 的兩筆過期項目 (4, w) 與 (5, w)，取出時一一略過，佇列空了」 | `graphs_depth.py` |
| 22 | 「C 的鄰居中還不在樹裡的只有 F」 | `graphs_depth.py` |
| 23 | footer「Chapter 9」→「第 8 章」；字卡徽章依決定不改；hero 副標「cppds Chapter 9」是課本章號，未動 | `graphs.html` |
| 24 | 「路徑（Path）」字卡補「序列中的頂點互不相同」 | `data/flashcards_zh/ch8.json` |

## 驗證

- `pipeline.sh` 連跑兩次 sha256 相同：`6a93edb7d809b26259a658b7236db01c824ae8722bb8c86caa1f0ca569908a1b`。重跑後 gen 區外的改動（`tsStep()`、`sccStep()`、knight `data-l`、Prim `data-l="9"`、已走格數、已展開、footer 等）都還在。
- `check_content.py`：run 12/12、errors 0；`content-results.json` 沒有變動。
- 保真比對（對 HEAD）：`data-expected`、`pre`、`id`、`href` 完全相同。
- `python3 tools/check_links_cpp.py`：22 頁，0 錯誤、0 警告。
- 5 段 inline script 都通過 `node --check`。
- `check_browser.py`（1440、390）：無 page error、無溢出；58 張圖正常；五個控制器逐步高亮相符；騎士 5×5 兩種模式都 SUCCESS（Warnsdorff 26 格、不用 9,996 格）；拓撲排序、SCC 三段播完，SCC 得 3 個。結果與截圖存到 `fixes-ch8-round2-browser/`，`20261008-ch8/` 原檔已用 `git checkout` 還原。
- `fixes-ch8-round2-browser/check_round2.py`（結果 `round2-results.json`），從剛載入的狀態測：
  - 拓撲排序：第一次按單步 i=0、沒有自動播放；走 3 格後按 ② 被擋（輸出空白、i 不變）；逐格單步共 18 格走完 ①，再按 ② 排出 9 項。
  - SCC：第一次單步 i=0；走 5 格後按 ②、③ 都被擋下，`sccOnGT` 仍是 false；單步共 16 格走完 ①，按 ② 轉置，再按單步建立 ③（i=0），逐格到結束得到 SCC1 {A,E,B}、SCC2 {C,G,F}、SCC3 {H,I}，狀態寫「3 個強連通元件」。
  - 騎士：預設 5×5；5×5、7×7 選單沒有奇色起點；5×5 兩種模式都 SUCCESS，格內數字恰為 0–24，起點顯示 0，已走格數 25，播放中高亮第 10 行、成功時第 19 行；不用 Warnsdorff 時回溯 4,985 次。6×6 (3,3) 不用 Warnsdorff 時出現上限訊息，內容不叫學生改用 Warnsdorff。
  - Prim：3 個略過格（35–37）都高亮 `if (inTree.count(currentKey)) continue;`。
  - Dijkstra：狀態列寫「展開它的鄰居」，欄名「已展開」，所有步驟訊息都沒有 visited。
  - DFS：標籤「第一棵樹的根」，說明文字可見。
- 起點模擬：`fixes-ch8-round2-browser/knight_starts_sim.{js,txt}` 用和頁面相同的走法順序與 80 萬步上限，模擬 5–8 各起點。5×5、7×7 的奇色起點兩種模式都會超過上限；7×7 的 (2,2)、(2,4)、(3,5) 用 Warnsdorff 也會超過上限，所以這些格子不放進選單。

## 限制

- 騎士動畫仍然沒有單步鍵（既有設計）。關閉 Warnsdorff 時，程式面板顯示的仍是 `knightTourWarnsdorff`（`orderByAvail` 那一行），只有走訪順序不同。
- 瀏覽器測試封鎖外部請求，沒有實際驗證 MathJax 排版；新增的公式只有 `$O(\sum_b |b|^2)$`、`$\Theta(n^2)$`、`$O(\log\deg(v))$`、`$k^N$` 這類簡單寫法。
