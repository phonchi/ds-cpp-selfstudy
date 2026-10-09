# 第 7、9 章第二輪讀者審閱修正（2026-10-09）

依 `readerD-findings.md`（第 7 章 #1–#13、第 9 章 #1–#16）與 `readerD-ch7-9.md` 的決定修正。ch7 #14、ch9 #17（字卡徽章）依決定不改。未 commit，未動 `graphs.html`。

## 第 7 章 searching_sorting.html

| # | 修法 | 檔案 |
|---|---|---|
| 1 | `#quickCode` 改列 `partition`（`pivotVal`／`leftMark`／`rightMark`，與 `sorting.hpp` 同名）＋ `quickSortHelper`，21 行都有 `data-l`。`genQuickSort` 的 pcLine 重新對齊：初始呼叫→helper 標頭，三者取中→註解行，`pivotVal`、`leftMark/rightMark` 拆成兩格各指一行，左右掃描→兩個 while，`done = true`→if，交換→else swap，pivot 歸位→`swap(a[first], a[rightMark])`；完成格不高亮。訊息改用 leftMark／rightMark／pivotVal | `search_legacy.py`、主 script |
| 2 | Hibbard 模式：第一格訊息「gap = 不超過 n=9 的最大 2^k−1 = 7」，同時把面板第 2 行換成 `int gap = largestHibbardGap(a.size()); // 最大的 2^k−1 ≤ n`（切回 n/2 時還原）。`gap /= 2` 對 2^k−1 用整數除法正好得到 2^(k−1)−1，訊息寫成「gap /= 2 → 7 / 2 = 3」 | 主 script（`genShellSort`、`initShell`） |
| 3 | 選擇排序面板加上 `if (maxPos != fill)`；交換格指 swap 行，「無需交換」格指 if 行；一輪結束格指 for 行（`--fill`） | `search_legacy.py`、主 script |
| 4 | shell 狀態列改用面板的 `a`、`gap`、`start`、`curVal`、`curPos`，例如 `gapInsertionSort(a, 0, 4)`、`a[8] = a[4] = 77（位移）` | 主 script |
| 5 | 「midpoint = 0 + (9 - 0) / 2 = 4」 | 主 script |
| 6 | 兩則 FAQ 不加（補充）（`IN_NOTES` 集合） | `search_depth.py` |
| 7 | `43 + 56 + 55 + 64 + 01 = 219` | `search_legacy.py` |
| 8 | 改成「`put()` 會遇到的 4 種情況」，相關標題、表頭、說明的「分支」都改「情況」；同一區上方 collision 對照表原本的「情況一／二／三」改「狀況一／二／三」，避免兩套「情況」 | `search_legacy.py`、`search_depth.py`（fold 標題） |
| 9 | `#hashBatch` 預設改成 9 個數 `54, 26, 93, 17, 77, 31, 44, 55, 20` | `search_legacy.py` |
| 10 | 複雜度欄改「線性探查成功搜尋」「鏈結法成功搜尋」 | `search_legacy.py` |
| 11 | 刪掉 `opCount = Math.max(opCount, 1)`；空鏈訊息「slot 2 的鏈結串列是空的，找不到 13（比較 0 次）」 | 主 script |
| 12 | 兩行「複製剩餘」的 while 給 `data-l` 15、16，結尾 `}` 改 17；`genMergeSort` 為每個尾端複製加一格（「R 已用完，複製 L 剩下的元素：寫入 a[k] = …」），合併完成格指 17 | `search_legacy.py`、主 script |
| 13 | 參考表快速排序空間「$O(\log n)$ 期望，最差 $O(n)$」 | `search_legacy.py` |

## 第 9 章 trees.html

| # | 修法 | 檔案 |
|---|---|---|
| 1 | `genDeleteSteps` 節點改名 `targetNode`，`target` 一律是使用者要刪的鍵；`applyStep` 的 commit 與 `render` 的 hl 都改用 `targetNode` | 主 script |
| 2 | `startOp(op, key, autoplay)`；剛載入或換了 key 時按單步，會用最近一次的 put／get（預設 put）建立操作、停在第一格不自動播放；到最後一格再按不動作；`rebuild()` 清掉 player。另外修正比較格的高亮：鍵相等時指 `==` 那一行（原本指 else） | 主 script |
| 3 | `heapStep`：沒有操作時建立並顯示第一格；到最後一格就停住。重置、切換操作、套用陣列都會清掉 player，下一次單步才會開始新操作。**保留**：最後一格時按「開始」仍會在目前的 heap 上重新執行同一操作（reader 未點名） | 主 script |
| 4 | LR／RL 改成 4 格：BEFORE→第一次旋轉後（mid 樹）→第二次旋轉後→完成，每格文字描述當格的樹；bf 欄由畫出來的樹算 z、y、x 的實際平衡因子（例如 LR 初始「z: +2，y: -1，x: 0」）。LL／RR 同樣改用實際 bf；側欄標籤改「平衡因子 bf」 | 主 script、`trees_legacy.py` |
| 5 | Q4 干擾選項 `1.4` 改 `-4`，回饋「由左往右計算、不管括號：10 / 2 - 6 - 3 = 5 - 6 - 3 = -4」 | `data/questions_zh/ch9.json` |
| 6 | 改成「<a>BST 的限制</a>一節會分析這種退化，<a>AVL Tree</a> 一節再說明怎麼避免」（連到 `#bst-analysis`、`#avl`） | `trees_legacy.py` |
| 7 | 狀態列改 `BinaryTree aTree("a")`、`aTree.insertLeft("b")`、`aTree.insertRight("c")`、`aTree.getLeftChild()->insertRight("d")` 等，與高亮行一致 | 主 script |
| 8 | Case 3 先 `spliceOut`（commit `splice-succ`）再搬 key（`copy-key`），畫面不再出現兩個 35 | 主 script |
| 9 | 四個標題改「完整程式：以 BinaryTree 建立書本樹並做前序走訪」「完整程式：對解析樹做三種走訪與 postordereval」「完整程式：在圖中的 heap 插入 7，以及執行 delMin」「完整程式：buildHeap({9, 6, 5, 2, 3})」 | `trees_depth.py` |
| 10 | 走訪：每格帶 `line`（根的呼叫→函式標頭；左右子呼叫→父層對應的遞迴行；印出→cout 行；結束→結尾 `}`），`applyFrame` 呼叫 `hlLine`，程式面板改在 `player.reset()` 之前設定。heap：三組程式面板（insert＋percUp、delMin＋percDown、heapify＋percDown，percDown 共用 `data-l` 1–11），依操作切換，逐格高亮；訊息改寫成對應的程式動作。刪除：側欄改成可見的 `#delCode`（`_get`、三種情況、findSuccessor、findMin，20 行），搜尋、分類、找 successor、splice、搬 key 各格高亮 | 主 script、`trees_legacy.py` |
| 11 | percUp 面板的 `else`／`break` 有行號；停止格指 `break`；已到根時另有一格指 while | `trees_legacy.py`、主 script |
| 12 | 使用方式框：「標『選讀』的 AVL 高度上界與內部實作，以及標『（補充）』的收合區、段落與互動示範，都是課堂沒細講的延伸，第一輪可略過。」（gen 區外，直接改頁面） | `trees.html` |
| 13 | TreeNode listing 拿掉 `isRoot()`、補 `hasBothChildren()`（與 `bst.hpp` 一致）；「私有輔助函式 `_get()`」改「輔助函式」 | `trees_depth.py` |
| 14 | 「往上更新平衡因子最多走過樹高 $h = O(\log n)$ 層，每層一次（AVL 樹的高度最多約 $1.44\log_2 n$）」 | `trees_depth.py` |
| 15 | 重點回顧第 5 點統一用 $i$ | `trees_depth.py` |
| 16 | 在 heap_basic 之後補講義 cell 151 的 main：`buildHeap({10,4,9,8,12,15,3,5,14,18})` 後 `findMin()`、`size()` 與 delMin 迴圈。實際編譯執行（g++ -std=c++17 -Wall -Wextra -pedantic，課程標頭）輸出 `3 10` / `3 4 5 8 9 10 12 14 15 18 `，帶 `data-cpp="run"`／`data-expected` | `trees_programs.py`（`HEAP_OPS`、RUN／OUT）、`trees_depth.py` |

## 驗證

- pipeline 連跑兩次 sha256 相同：`searching_sorting.html` `681076a0…1cc7`、`trees.html` `ab7006f6…1361`。
- check_content：ch7 run 22/22、ch9 run 16/16（多了 cell 151），errors 0。ch7 的 `content-results.json` 只有暫存路徑差異，已 `git checkout`；ch9 的有新增一筆，保留。
- `python3 tools/check_links_cpp.py`：22 頁，0 錯誤、0 警告。
- 兩頁各 5 段 inline script 通過 `node --check`。
- check_browser（1440／390）：兩章都沒有 page error、沒有水平溢出、圖都載入、所有播放器能播完。結果存在 `fixes-ch7-9-round2-browser/`；`20261008-ch7/`、`20261008-ch9/` 被覆寫的截圖與 `browser-results.json` 已還原。
- 逐格單步（Playwright，每個案例都從剛載入的頁面開始；腳本 `step_ch7.py`、`step_ch9.py`，逐格紀錄在 `ch7-step-frames.json`、`ch9-step-frames.json`）。每格比對「訊息 → 高亮行」規則，結束後多按一次單步確認畫面不變：
  - ch7：quick（first 49 格、median 52 格）、shell（n/2 152 格、Hibbard 140 格，第 2 行已換）、selection 68 格（含 2 次「不用交換」）、binary（命中 3 格、未命中 8 格）、merge 64 格（含 7 格尾端複製），全部 0 不符、結束停住。雜湊鏈結法：空鏈搜尋比較 0 次，非空鏈未命中 1 次；批次預設 9 個數。
  - ch9：BST delete 20／80／30／50（建立樹後逐格單步）0 不符，target 欄全程是原鍵，任何一格都沒有重複鍵，結束後鍵已刪除；BST put（剛載入就單步）與 get（換 key 後單步）都不自動播放、高亮 0 不符、結束停住；heap 三個講義示範單步到底再按兩次，陣列與輸入框不變，高亮 0 不符；AVL LL／RR／LR／RL 的階段、bf、訊息與樹一致；走訪三種順序高亮 0 不符；nodes-refs 狀態列的 C++ 敘述與高亮行一致。

## 備註

- quick 面板改成 21 行 partition＋helper，側欄較窄時長行在面板內捲動，頁面沒有溢出。
- `largestHibbardGap()` 不是 `sorting.hpp` 的函式，只出現在標題為「虛擬碼」的面板，註解寫明「最大的 2^k−1 ≤ n」。
