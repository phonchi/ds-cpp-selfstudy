# 子任務：修正講義第 6–9 章並重建發布（2026-10-10，使用者已授權）

## 背景
自學網站 `/home/phonchi/ds-cpp-selfstudy` 的讀者審閱發現講義本身有錯。網站已先更正或在圖說註明，現在要回頭修講義。

使用者已決定：
- 修正文字、程式、Key terms 與題庫；
- 重繪三張有誤的課本原圖；
- 依既有流程重建第 6–9 章的 HTML、投影片與 PDF；
- 同步到 `nsysu-math208` 並 push（push 已授權）。

## 必讀
動手前先讀完以下文件：
- `~/ds_cpp/Slides/CLAUDE.md`：conda env `rise`、nbconvert、build 規則。
- `~/ds_cpp/Slides/figure_refresh_20261003_ch1-9/README.md`：重繪圖與發布流程、各項檢查、圖片 width% 調整。最重要的是：建 PDF 前，要先從 Windows 端用 `curl.exe` 確認線上 raw 圖片 URL 已經是新版。
- `~/ds_cpp/Slides/figure_refresh_20261003_ch1-9/` 裡的 `figkit.py`、`generate.py`、`shoot_slides.py`。
- `~/.claude/projects/-home-phonchi-ds-cpp-selfstudy/memory/slides-print-pdf.md`，以及 skill `jupyter-rise-pdf`（用 Skill 工具載入）：print PDF 的做法。
- `~/ds_cpp/Slides/build_all.sh`、`tools/print_pdf_paper.sh`、`inject_pdf_outline.py`。
- 若 `nsysu-math208` 有 STATUS.md 或發布說明，也要讀，並照它的同步方式（哪些檔要放上站）操作。

## 安全限制
- `~/ds_cpp` 裡有使用者尚未 commit 的修改：`.claude/settings.local.json`、`Slides/analysis.html`、`Slides/graphs.html`、`Slides/tools/selfstudy_builders/build_analysis.py`，以及未追蹤的 `Algorithm/`、`HW*/`。**這些一律不碰、不 commit。** 只 commit 你自己改的檔案，逐檔 `git add`，不要用 `-A`。
- 先確認 `~/ds_cpp` 與 `~/nsysu-math208` 各自的 git root 與遠端；push 前用 `git status` 與 `git diff --stat` 確認範圍。
- **math208 是基準**：本機檔案和 math208 版本不同時，以 math208 為準。先比對講義 05–09 的 ipynb 與 math208 是否相同；若不同，先停下來回報，不要覆蓋。
- 不改第 1–5 章；第 1、2 章依既有決定留在本機。

## 要修正的項目（每項先到 notebook 找到確切 cell，再修）
1. **第 6 章 quiz `recursive1.json`**：題目問 `{2,4,6,8,10}` 會有幾次遞迴呼叫，標的答案「4」是舊版 base case 的算法。照現行 `listSumFrom`（以空範圍為 base case），初始呼叫 1 次加遞迴呼叫 5 次，共 6 次。
   - 正解改成 5（遞迴呼叫次數），四個選項的回饋都要配合重寫；必要時可把題目改成問總呼叫次數。
   - 兩份都要改：`~/ds_cpp/Slides/questions/ch6/recursive1.json` 與 `~/nsysu-math208/extra/questions/ch6/recursive1.json`。
   - 確認 notebook 載入題目的路徑。
2. **第 7 章 cell 84 附近，折疊法反轉版**：寫成「34 + 56 + 55 + 64 + 10 = 219」，正確應為「43 + 56 + 55 + 64 + 01 = 219」（每隔一片反轉）。
3. **第 8 章 Key terms 的 Search Tree**：定義寫成二元搜尋樹的意思，改成本章的意思：BFS／DFS 走訪時，由 predecessor 連結形成的樹。
4. **第 8 章 Warnsdorff 那張投影片**：程式名稱仍叫 `knightTour`，但執行的程式呼叫的是 `knightTourWarnsdorff`，名稱改成一致。
5. **第 8 章投影片上的 `bfs`**：沒有重設頂點，也沒有先把起點塗灰，和 `graph_algos.hpp` 不同。依標頭補上，若該 cell 有輸出，要確認輸出不變。
   - 投影片的 `Vertex`／`Graph` 和實際 `#include` 的 `graph.hpp` 不同：概念相同的名稱改成與標頭一致；若投影片刻意簡化，就在旁邊加一句說明。
6. **第 8 章騎士巡遊的分析**：寫「約為 $3.8^{25}-1$，也就是 $3.12\times10^{14}$」，和上一行的公式 $\frac{k^{N+1}-1}{k-1}$ 不符。
   - 改成「約為 $k^N$ 的量級」並重算數字。
   - 6×6 與 8×8 的數字也一起核對。
7. **第 9 章 cell 380 附近**：「往上更新平衡因子最多 $\log_2 n$ 次」改成「最多走過樹高 $h=O(\log n)$ 層」（AVL 樹高約 1.44 log₂n）。
8. **第 9 章 cell 54、282 附近**：文字說完整類別在 `pythonds3/cppds/trees/binary_tree.cpp`、`.../binary_search_tree.cpp`，但實際 include 的是 `binarytree.hpp`、`bst.hpp`。改成實際存在的檔名，先到 `~/ds_cpp/Slides/pythonds3/cppds/` 確認。
9. **第 9 章 BST 的 TreeNode listing**（cell 231、249 附近）：列了 `isRoot()`，但 `bst.hpp` 沒有這個函式，反而有 Case 3 用到的 `hasBothChildren()`。依 `bst.hpp` 修正。另外，`_get()` 在 `bst.hpp` 是 public，若講義寫「私有」就改成「輔助」。
10. **重繪三張課本原圖**：沿用 figkit 的風格與檢查流程，在新目錄 `figure_refresh_20261010_ch8/` 寫 `generate.py`。
    - `bfs3.png`：佇列應為 poll、fail，原圖畫成 pole、pall。
    - `ktdfse.png`：程式回溯後 C 應已塗回白色，原圖仍是灰色。
    - `bfsDone.png`：原圖缺 fall 這個頂點，fall 接在 fail 底下、距離 3；sage 要依實際狀態上色。

    重繪的依據是 `graph_algos.hpp` 實際的執行結果：寫一支 C++ 程式印出 BFS 樹（predecessor 與 distance）以及 DFS 回溯的狀態，用來決定圖的內容。注意鄰居順序：C++ 的 `map` 依字母序。原圖是依課本的鄰居順序畫的，新圖要和講義程式的輸出一致；如果和原本逐步圖序列（bfs1–3）的順序衝突，回報並說明採用的依據。

    各項檢查都要跑：沒有文字超出 SVG、沒有圖形超出 SVG、文字不重疊、diagram-design 的 `self_check.py`。另外：
    - 產出新舊對照的 montage；
    - 每張圖都實際看過；
    - 用 `shoot_slides.py` 確認放進投影片後沒有溢出；
    - 必要時調整 width%。

## 重建與發布（依既有流程）
1. 修改 notebook 時，對照備份確認只動到預期的 cell；並用 nbformat 驗證。
2. 第 8 章的圖先推到 math208 的 `static_files/presentations/imgs/`（commit + push），再從 Windows 端用 `curl.exe` 確認三張圖的 raw URL 已經是新版。之後才建 PDF。
3. 重建第 6–9 章，照 `build_all.sh` 與各章的 build 流程，以及 print PDF 的做法：
   - `--execute --allow-errors`；
   - 驗證動畫與圖片都存在；
   - PDF 有書籤；
   - print 版的頁數等於投影片張數。
4. 依 math208 既有的放置方式同步：
   - 更新 ipynb、html、pdf，以及上一步推過的圖與題庫 json；
   - commit 並 push 到 math208；
   - `~/ds_cpp` 中你改過的檔案也逐檔 commit（若有 remote 就 push）。
5. 用 `gh run list` 確認 GitHub Pages 部署成功。

## 回到自學網站（`/home/phonchi/ds-cpp-selfstudy`）
- 用重繪後的圖取代 `assets/figures/ch8/bfs3.png`、`ktdfse.png`、`bfsDone.png`。
- 刪掉 `tools/enrich/content/graphs_figures.py`（以及任何引用這幾張圖的地方）裡「原圖有誤／原圖沒有畫出 fall／圖中 C 仍畫成灰色」這類更正說明，改成直接描述新圖。
- 執行 `docs/verification/20261008-ch8/pipeline.sh` 兩次，確認冪等。
- 跑 `check_links_cpp.py`，再跑 ch8 的 `check_browser.py`，確認圖片都載入、沒有錯誤；跑完把它改寫的結果檔還原。
- 這個 repo 只 commit 不 push：主控核對後再 push。

## 驗證紀錄
寫在 `~/ds_cpp/Slides/figure_refresh_20261010_ch8/README.md`，內容包括：
- 修了哪些 cell；
- 圖的依據與各項檢查結果；
- build log；
- PDF 頁數與書籤；
- curl 檢查結果；
- 兩個 repo 的 commit 與 push 結果。

## 回報
逐項說明改了什麼、兩個 repo 各自的 commit 與 push、部署狀態、自學網站的 commit，以及有疑慮或沒做到的地方。不要宣稱沒有實際執行過的驗證已經通過。若遇到流程卡住，例如 Windows Chrome 無法執行或 curl 失敗，停下來回報，不要繞過檢查。
