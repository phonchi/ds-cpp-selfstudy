# 第 4–6 章第二輪讀者審閱修正（2026-10-09）

依 `readerC-ch4-6.md` 的「決定」欄修正，共 20 項；第 4 章第 3 項依決定維持不改。能改來源的都改來源，再用各章 `docs/verification/20261008-chN/pipeline.sh` 重建。gen 區外的部分直接改頁面：主 `<script>`、使用方式框、h2 徽章、手寫的 info-box 與 EXERCISE。重建後已確認這些修改仍在。各章 README 的 gen 區外手改清單已補上本輪條目。上一輪（`fixes-ch4-6.md`）的修正都保留。未 commit。

## 第 6 章 recursion

| # | 修法 | 檔案 |
|---|---|---|
| 1 | `MAZE_ROWS` 照決定改兩列：row4 `'+ + +++ + ++'`、row5 `'+S      +  E'`，打通 (5,2) 與 (4,9)。`mazeFrames` 保存 `search(sr, sc)` 的回傳值 `found`，結尾訊息依它決定：true 時是「searchFrom 回傳 true：綠色 ＋ 連成從 S 到 E 的路徑 ✓」，false 時是「searchFrom 回傳 false：這個迷宮從 S 走不到出口」。第 0 格訊息補上「目標是右邊的出口 E」，取代原本載入時顯示的「S=起點、E=出口」。正文只寫「較小的迷宮」，沒有描述格子配置，所以不必改。 | `recursion.html`（主 script） |
| 2 | 兩頁主 script 都加入 `freshPlayer(old, opts, play)`：暫停舊實例、沿用 ⏸ 按鈕，再 `reset()` 顯示第 0 格。`play` 為 false 時設 `i = 0`，和 ch4 `llRun` 相同。每個播放器拆成 `xMake(play)` 與 `xStart()`，載入時呼叫 `xMake(false)`。會影響 frames 的輸入改變時也重建播放器：`tostrN`、`tostrB`、`hanoiN`。toStr(10, 2) 呼叫堆疊的播放器在 `EXTRA_JS` 裡，改法相同。 | `recursion.html`（主 script）、`tools/enrich/content/recursion_widgets.py` |
| 3 | `hanoiRender` 在每根柱子下方顯示兩行：柱名，以及角色 `fromPole`／`toPole`／`withPole`，對應 `moveTower(n, "A", "B", "C")`。第 0 格訊息也附上角色名。內文「第一根／第二根／第三根」改用角色名：圖前一句定義起始柱（fromPole）、目標柱（toPole）、中間柱（withPole），「由下往上想」兩段改用 fromPole／withPole／toPole。動畫前加一句說明：動畫依講義呼叫擺放柱子，目標柱 B 在中間，和上圖不同。 | `recursion.html`（主 script）、`recursion_depth.py` |
| 4 | 完成格的 `line` 改為 `null`，不高亮任何一行。 | `recursion.html`（主 script） |
| 5 | 刪掉 `used` 陣列與 coinsUsed 回溯。最後一格改為「表填完了：makeChange3 回傳 minCoins[23] = 3，23 分最少要 3 枚。」，仍高亮第 11 行 `return minCoins[change];`。第 0 格補上硬幣與目標金額。 | `recursion.html`（主 script） |
| 6 | 「講義程式：印出遞迴深度（上課略過）」改為「（課堂略過・自學）」。 | `recursion_depth.py` |
| 7 | 「第 5 步就是上圖的狀態」改為「堆疊頂端顯示 toStr(2, 2) 得到 "10"、下面兩格還在等待的那一格，就是上圖的狀態。」，對應 tsfFrames 的第 5 格。 | `recursion_depth.py` |
| 8 | 對照 `OUT['maze']`：出口 O 在第 2 列（row 2，輸出的第 3 行）、第 0 欄，位在左邊界。本頁一律用「列＝row」，所以改寫成「最後在左邊界、第 2 列（從第 0 列算起，也就是輸出的第 3 行）找到出口」。 | `recursion_depth.py` |
| 9 | `colors` 改成講義 `colors[]` 的順序：blue `#2f5fd0`、red `#d0352b`、green `#2e9e4f`、white 用淺灰 `#d9d9d9`、yellow `#f2c80f`、violet `#9b59d0`、orange `#f08a24`。索引仍是 `deg % 7`，與講義的 `colors[degree]` 相同。圖說沒有提到顏色。 | `recursion.html`（主 script） |

## 第 5 章 linear_structures

| # | 修法 | 檔案 |
|---|---|---|
| 1 | 開場 info-box 改為「課程標頭的 `Stack`、`Queue`、`Deque` 是作業用介面」。#queue 改為「`enqueue/dequeue/isEmpty` 是課程實作 `Queue<T>` 的作業用介面」，#deque 改為「`addFront/removeFront` 是課程實作 `Deque<T>` 的作業用介面」，「課程實作補充：」改為「課程實作：」。頁面上的「補充」只剩（補充）收合區的標題與使用方式的定義；字卡與題庫裡沒有其他「補充」。 | `linear_structures.html` |
| 2 | 頁面上沒有 `(a)` 按鈕，現有的兩個按鈕 `(()`、`())(` 都只有括號。問題出在 `parFrames` 的「忽略非括號字元」分支，它和程式行為不符：程式會把非開符號一律當成閉符號。這次刪掉該分支，`parMake` 把輸入框裡的非括號字元去掉。若真的去掉了字元，第 0 格會說明「parChecker 假設字串只有括號，其他字元會被當成閉符號」。 | `linear_structures.html`（主 script） |
| 3 | 「（`())(` 的第 3 步）」改為「（`())(` 讀到第 3 個符號時）」。 | `linear_structures.html` |
| 4 | 題幹改為「若用 int 運算（整數除法）做後序求值，答案是？」。另寫 int 版後序求值驗算（`fixes-ch4-6-round2/ex2-int-postfix.cpp`，輸出存在 `.txt`）：3*5=15、16−4=12、15/12=1、10+1=11。正解 11 與四個選項的回饋都和這個結果一致，未改。 | `linear_structures.html` |
| 5 | 「三節各附一張兩者的對照表」改為「三節各附一張 API 對照表」。 | `tools/enrich/content/linear_depth.py` |
| 6 | 刪掉 gen 區外手寫的「機器轉換用 stack…演算法四步」段落，連同重複的反轉句與 `<ol>`。四步依講義 cell 134–136 改寫後，移到 `infix_convert()`。順序照講義：動機（反轉句只留講義的粗體句）→ (A + B) * C → 「假設中序式…」加上「stack 頂端是最近存入的運算子，拿新運算子和它比較優先權」（cell 132–133）→ 四步 → 追蹤圖 → 核心迴圈 → 文字追蹤表。 | `linear_structures.html`、`linear_depth.py` |
| 2（共通） | 七個播放器（intro、par、base、i2p、peval、hp、pal）都改用 `freshPlayer`，載入時顯示第 0 格。`parInput`、`baseInput`、`baseSel`、`i2pSel`、`hpNum`、`palInput` 改變時重建播放器。 | `linear_structures.html`（主 script） |

## 第 4 章 linked_lists

| # | 修法 | 檔案 |
|---|---|---|
| 1 | 使用方式框的標記說明加入：「標『課堂略過・自學』的是講義內容，只是上課沒有細講，請自己讀完」。講義的 skip cell 中，只有 85–87（append 練習）是整段跳過、頁面也有對應段落，所以只把 `<h3>練習：實作 append()</h3>` 加標為「（課堂略過・自學）」。其餘 skip cell（48、57、80、81、105、118、124、152、156）只是一兩句說明或一行過渡，不標。 | `linked_lists.html`（使用方式框）、`tools/enrich/content/linked_depth.py` |
| 2 | 原本的收合區「所有權與深層複製（補充）」拆成兩部分。講義內容改為可見的 h3「所有權與深層複製」：remove 之後要 delete 節點、解構子釋放剩下的節點（cell 69），以及 deep copy 的定義（cell 161）。複製建構子與複製指派的示範程式講義沒有，收成「複製建構子與複製指派（補充）」。 | `linked_depth.py` |
| 3 | 依決定維持不改。 | — |
| 4 | 刪掉 ordered add 圖後那段「和無序串列的 remove 一樣…previous 與 current…」，保留圖說與講義 add 的說明段。 | `linked_depth.py` |
| 5 | 改為「之後的 size、search、remove 都會沿 next 前進，最遲走到 NULL 時停下；」。 | `linked_depth.py` |
| 6 | #stl 徽章「講義 04 延伸」改為「講義 04」。 | `linked_lists.html` |

## 驗證

- `pipeline.sh` 各連跑兩次，sha256 相同：
  - ch4 `1cb4789b44d04a7d24449ca726df809d56e776fa10ec433f24ac62b6a2cb9ecc`
  - ch5 `db0068fa5f0be3375b406fd834dc6624588116fd0e9b8869ccd45fb578fdf111`
  - ch6 `4abff0e37f2acbab44280bdd9cec04a5b0f6b0c533ac5c4f8f29c410ca50850f`
- `DSCPP_PAGES=linked_lists python3 docs/verification/20261003-ch3-ch4/check_content.py`：23 examples passed，generators stable，IDs／anchors／JS syntax passed。
- `20261008-ch{4,5,6}/check_content.py`：ch4 22/22、ch5 17/17、ch6 13/13，errors 0。
- 三份 `content-results.json`（20261003-ch3-ch4、20261008-ch4、20261008-ch6）只被暫存路徑或單頁結果覆寫，已用 `git checkout -- <路徑>` 還原。
- `python3 tools/check_links_cpp.py`：22 頁，0 錯誤／0 警告。
- 三頁所有 inline script 都通過 `node --check`（5／4／5 段）。
- 改前改後比對：三頁的 `pre`、`data-expected`、`href`、`id`、`.pseudo-code` 完全相同。
- `20261008-ch{4,5,6}/check_browser.py`（1440、390）：無 page error、無水平溢出。
  - ch4：12 個播放器、34 個案例、315 格。
  - ch5：15 個播放案例。
  - ch6：7 個播放器，maze 105 格、hanoi 9 格；三個 canvas 都有像素，sierCv 有 80510 個。
  - browser-results.json 與截圖已更新。
- Playwright（`fixes-ch4-6-round2/step2.py`，結果在 `step2.json`）：
  - **單步不必先按 ▶**：ch6 七個、ch5 七個播放器各自重新載入頁面，未按 ▶ 就點三次「→ 單步」。`i` 依序是 0→1→2→3，每次狀態列都會改變，高亮行等於該格的 `line`。之後按 ▶ 都能播完。14 個全部 ok，無 page error。
  - **迷宮**：從載入狀態點「→ 單步」105 次播完。最後一格訊息為「searchFrom 回傳 true」。標成路徑 P 的 19 格從 S (5,1) 連到 E (5,11)，中間不斷開。每一格的高亮行都和訊息相符：牆→2、出口→5、標記走過→8、成功路徑→13、死路→14。截圖 `maze-final.png`。
    - 因為搜尋順序是北、南、西、東，會先探完 S 上方的死巷，再經 (5,2)、(4,3)、(3,3)…(1,5)–(1,7)…(3,9)、(4,9) 走到 E。
  - **河內塔**：改成 4 盤，柱下標示為「A fromPole」「B toPole」「C withPole」。完成格的 `line` 是 null，沒有任何高亮行；狀態列為「完成！4 個盤子都到了 B，共 15 步」。截圖 `hanoi-labels.png`。
  - **Sierpinski**：degree 3 畫出 80510 個非透明像素，截圖 `sierpinski.png`。顏色由外到內依序是淺灰（white）、綠、紅、藍。
  - **括號**：輸入 `(a)` 後輸入框變成 `()`，第 0 格出現說明，結果是平衡。

## 讀者清單以外的連帶修改

- 換掉播放器前先 `pause()` 舊實例。以前連按 ▶ 時，舊實例的 timer 會繼續寫畫面，只有 intro 有處理這件事。
- 輸入改變時重建播放器。否則先改輸入、直接按單步，會看到舊輸入的 frames。
- 第 0 格取代了原本靜態的提示文字，所以迷宮、填表、河內塔的第 0 格訊息補上必要的說明：出口 E、硬幣與金額、柱子角色。
- ch6 README「限制」裡「單步需先按開始」那條，改為描述目前的行為。

## 未做／注意

- 第 5 章第 2 項：頁面上找不到 `(a)` 案例或按鈕。這次改的是與程式不符的 JS 分支，並限制輸入只能有括號；按鈕不必更新。
- 第 4 章第 1 項只標了 append 練習。講義 cell 105 是一大段 ordered search 的逐步說明，頁面上對應的是正文的一段，沒有整節獨立，所以沒加標示。
