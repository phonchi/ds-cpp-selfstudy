# 第 9 章 trees 依講義擴充驗收（2026-10-08）

## 範圍

來源：`/home/phonchi/ds_cpp/Slides/09_Trees and Tree Algorithms.ipynb`、`pythonds3/cppds/{binarytree,binaryheap,bst}.hpp`、`questions/ch9/*.json`、講義圖 `nsysu-math208/static_files/presentations/imgs/`。

修改／新增：

- `trees.html`
  - 一次性 `place_markers.py`：11 個 section 的 h2 之後內容移進 `<!-- gen:trees-<sid> -->`，手寫部分存到 `tools/enrich/content/trees_legacy.py`；舊 enrich 注入的三張卡（`dx-voc` 兩個程式、heap 卡、BST 卡，共 12,288 字元）移除，改由 gen 重建並帶 `data-cpp`。
  - 一次性 `hand_edits.py`（gen 區之外）：新增 `<section id="tree-adt">`（PART 02）與 `<section id="recap">`（SUM）；PART 編號 02–09 改為 03–10；float-nav 與目錄加 `#tree-adt`、`#recap` 並重編號；使用方式第 ④ 點改為指向重點回顧與（補充）收合區；主 `<script>` 的 heap 初值改為講義圖的 heap、加上 `data-heapdemo` 預設按鈕的處理；走訪的 `trees` 加上講義書本樹 `book`，程式面板改成講義 C++ 函式（原為 Python 式虛擬碼）。
  - 一次性 `hand_edits_delete.py`（gen 區之外）：BST 刪除面板「→ 單步」原本會直接自動播放、「↺ 重建」後單步失效，改為單步從第一格開始、重建後可再單步。
  - 一次性 `legacy_edits.py`（改 `trees_legacy.py`）：放 `{{slot:…}}`；nodes-refs 的 list-of-lists 拆成 `LEGACY['lol']`（收合「（補充）」，刪掉「課堂投影片跳過（RISE skip）」製作說明，Python 註解 `//` 改 `#`）；側欄 `BinaryTree` 類別、heap 的 `percUp`、走訪初始程式面板改為講義寫法；`` `C++` `` 反引號、「完全不需要指標！」、heap demo 說明（原說 insert，實際是 heapify）、AVL 選讀標示的製作用語；真實系統一節拆成 `LEGACY['real']` 收合「（補充）」；summary 補一個 h3。之後手動把 heap 的「完整的 BinaryHeap 類別」三欄程式拆成 `LEGACY['heapclass']`（收合，與分段程式重複）。舊 id `dx-hp`、`dx-bst` 改放在 heap 操作表與 BST 中序走訪的 h3。
- `tools/enrich/enrich_trees.py`：改寫為 gen 驅動、冪等的 driver（不再注入舊內容）；同步字卡數、題數標籤。
- `tools/enrich/content/trees_depth.py`、`trees_legacy.py`、`trees_programs.py`、`trees_figures.py`、`trees_quizzes.py`（新）。
- `assets/figures/ch9/`：41 張講義圖，全部被引用。
- `data/flashcards_zh/ch9.json`：33 → 37 張，補講義 Key terms 缺的 BST Property、Recursive Inorder Traversal，另加 percUp／percDown、Rotation。List of Lists 保留（對應收合的補充）。
- `data/questions_zh/ch9.json`：原 8 題即講義五個 quiz 檔，已改放正文（tree→術語、traversal→printExp 後、heap×2→buildHeap 後、bst×2→BST 分析、avl×2→AVL 選讀段）；題庫改為 8 題新自我檢測（四選一、每選項有回饋）。

講義 cell 54、282 文字寫的 `trees/binary_tree.cpp` 路徑頁面未提，一律寫實際 include 的 `.hpp`。成員函式版 `preorder()` 不在 `binarytree.hpp`，以 `fragment` 呈現並註明。未呼叫 `chapter_math.render_math` 與 `course_recordings.apply_recording`；`teaching_copy.EDITS['trees']` 維持空清單。

## 結果（全部實際執行，紀錄見 `run.log`）

| 項目 | 結果 |
|---|---|
| C++（`g++ -std=c++17 -Wall -Wextra -pedantic -I/home/phonchi/ds_cpp/Slides`） | 15 個 `data-cpp="run"` 無警告編譯，stdout 與 `data-expected`、頁面可見輸出逐字相同；2 個 `exercise`（練習 2、3 填空）確實編譯失敗。`content-results.json` |
| 標頭對照 | 7 張標示「（binarytree.hpp）」的程式卡，去掉註解與空白後逐字出現在 `binarytree.hpp` |
| 冪等：`pipeline.sh` 跑兩次 | sha256 相同（c8feccb0…） |
| 重複 id／懸空錨點／img 屬性／5 段 inline script `node --check`／每節有 h3／16 個 sq-item 四選一且各有回饋／圖檔全部被引用 | 0 錯誤 |
| `tools/check_links_cpp.py`、`tools/check_contrast.py` | 0 錯誤／0 警告；0 失敗 |
| Chromium 1440、390（`check_browser.py`） | 25 個 details 全展開；41 張圖 naturalWidth>0；術語點選、nodes-refs 單步與自動播放、解析樹單步／播放／求值、走訪（書本樹）單步與播放、heap 三個講義預設單步後播完（結果 `5 7 11 14 9 19 21 33 17 27 18`、`9 14 11 17 18 19 21 33 27`、`2 3 5 6 9`，與講義圖及編譯輸出一致）、BST put/get、刪除四個預設與單步、BST 分析、AVL 四種旋轉單步與播放；16 題 quiz 答錯答對都有回饋；37 張字卡翻面／全翻／洗牌可用；無水平溢出、無 page error。截圖 `trees-{heap,traversals}-{1440,390}.png` |

## 密度（`density.py`）

| 指標 | 前 | 後 | 第 1–3 章 |
|---|---|---|---|
| 文字（含收合區） | 19,000 | 47,336 | 22k–34k |
| 文字（收合區外） | 19,000 | 38,797 | 16.9k–27.6k |
| h2／h3 | 13／9 | 15／49 | — |
| img | 0 | 41 | 0–6 |
| details | 0 | 25 | 0–28 |
| .pseudo-code | 19 | 59 | 19–42 |
| 收合區外的預期輸出 | 4 | 12 | 10–21 |
| data-cpp 區塊 | 0 | 44 | — |
| quiz（sq-item） | 8 | 16 | — |
| 字卡 | 33 | 37 | — |

收合區外文字偏高：其中約 12k 是可見的講義程式片段（slide 上的 C++ listing），散文約 26.6k；heap 的「完整 BinaryHeap 類別」三欄程式與前面的分段程式重複，已收合。可見輸出 12 段，低於 15 的目標；講義可執行的程式只有這些，練習解答的輸出放在收合區內，沒有為了湊數另加程式。

## speak-human-tw 潤稿摘要

非互動模式（跳過確認、事後摘要），檢查 `trees_depth.py` 新增文字，修改 3 處：

1. 「注意 getLeftChild() 回傳的不只是一個值，而是一整棵子樹」→「getLeftChild() 回傳的是一整棵子樹」（「不只是…而是」句型，刪導引詞「注意」）。
2. 「這裡關心的不是元素在樹中的確切位置，而是利用二元樹的結構讓搜尋有效率」→「這裡要利用二元樹的結構讓搜尋有效率，元素放在樹中的哪個確切位置並不重要」（「不是 A，而是 B」整頁只留一次）。
3. 「前序走訪給的正好是這個順序」→「前序走訪的順序就是閱讀順序」。

新增文字無破折號；全形標點已檢查。

## 限制

- 瀏覽器測試封鎖外部請求，MathJax 與 Google Fonts 未載入，公式排版（含 bfderive 推導的 `aligned`）未實際驗證。
- AVL 旋轉面板（補充）與 BST 面板的既有 JS 文字未逐字檢查講義一致性。
- 一次性腳本 `place_markers.py`、`legacy_edits.py`、`hand_edits.py`、`hand_edits_delete.py` 內含防重跑保護。
- 字卡區導語「詞彙卡取自本章課程題庫，已譯為繁體中文」由 `tools/apply_zh.py`（第 59 行）產生；ch9 新加的 4 張字卡不是課程題庫的，這句已不精確，需主控決定是否調整（共用檔，未修改）。

## 2026-10-09 讀者審閱修正（gen 區外）

- 主 script 中 heap 動畫的三則狀態訊息 `perc_down` 改成 `percDown`。其餘修正都在產生器來源，見 `docs/verification/20261009-reading/fixes-ch7-9.md`。

## 2026-10-09 第二輪讀者審閱修正（gen 區外）

- 使用方式框：「選讀」「（補充）」的說明改為涵蓋 AVL 高度上界、段落與互動示範。
- 主 script：nodes-refs 狀態列改用 C++ 寫法；走訪動畫逐格高亮；heap 依操作切換程式面板並逐格高亮、單步到最後一格停住；BST put/get 可從剛載入就單步；刪除動畫 target 欄、Case 3 先 splice 再搬 key、`#delCode` 高亮；AVL 每格文字描述當格的樹，bf 欄由樹算出。細節見 `docs/verification/20261009-reading/fixes-ch7-9-round2.md`。
