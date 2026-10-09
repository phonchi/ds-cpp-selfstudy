# 第 4–6 章讀者審閱修正（2026-10-09）

依 `readerA-ch4-6.md` 的 15 項決定修正。能改來源的都改來源，再用各章 `docs/verification/20261008-chN/pipeline.sh` 重建；gen 區外的 h2 徽章、使用方式框與主 `<script>` 直接改頁面，重建後已確認仍在。未 commit。

## 逐項

| # | 頁 | 修法 | 檔案 |
|---|---|---|---|
| 1 | recursion | 先編譯加計數的 makeChange2（`makechange2-trace.cpp`／`.txt`）：2、3、4 分分別被進入 9、6、3 次，`knownResults` 仍為 0。FAQ 改寫為真正原因：`minCoins` 初值是 `change`（全用 1 分），2、3、4 分的最佳解正好等於初值，`candidate < minCoins` 不成立，所以不寫表、下次還要重算。正文 #dp 只說「2、3、4 分始終沒有填」，沒有錯誤歸因，未改。 | `tools/enrich/content/recursion_depth.py` |
| 2 | recursion | 「才移到下方中間」改為「才移到上方角落，最後才是右下角；每一層裡的三個小三角形都照這個順序」。 | `recursion_depth.py` |
| 3 | recursion | 主 `<script>` 的 spiral 改成真正的遞迴函式，參數 `spiral(…, 100)`、每次減 5，畫布放大 2.5 倍；呼叫次數由程式實算（21 次）。tree 改 `tree(75)`、`branchLen - 15`，放大 1.3 倍；講義參數只有 75、60、45、30、15 五層，滑桿改為 1–5、預設 5（呼叫 3／7／15／31／63 次，實算）。正文說明句與滑桿標籤同步改。 | `recursion.html`（主 script）、`recursion_widgets.py`、`recursion_depth.py` |
| 4 | recursion | `hanoiFrames` 改 `move(n, 0, 1, 2)`，即 `moveTower(n, "A", "B", "C")`：A→B、借 C。開始訊息、每步訊息（附上該層 `moveTower(h, from, to, with)`）與完成訊息同步；初始狀態列改為「A 是 fromPole、B 是 toPole、C 是 withPole」。每步高亮第 4 行 moveDisk。 | `recursion.html`（主 script）、`recursion_widgets.py` |
| 5 | recursion | reverse 解答 summary 改「參考解答（補充）」。 | `recursion_depth.py` |
| 6 | recursion | 字卡「基底情況（Base Case）」→「base case（基底情況）」、「堆疊框（Stack Frame）」→「stack frame（堆疊框）」、「碎形的深度（Degree of a Fractal）」→「碎形的 degree（深度）」（正文用「degree（深度）」）。背面的「基底情況／堆疊框」改用 base case／stack frame。其餘卡（呼叫堆疊、碎形、動態規劃、記憶化、貪婪法、累加變數、回溯、短路求值）正文以中文為主，維持原樣。使用方式第 ④ 點的「中文為主、術語附英文」改為「用語與正文一致，附中英對照」。 | `data/flashcards_zh/ch6.json`、`recursion.html`（使用方式框） |
| 7 | linear_structures | 依面板 `data-l` 修正 line：parFrames push→4、空 stack→6、閉符號先多一格 top/pop→7、配對結果→8；baseFrames 商的更新→5；i2pFrames 運算元→4、`(`→5、`)` 的 pop 與丟棄 `(`→6、shouldPop→8、`ops.push`→9；pevalFrames 數字→4。palFrames 也一併修：起始→2（建立 deque）、比較成功→6（原為第 7 行的 `}`）。 | `linear_structures.html`（主 script） |
| 8 | 兩頁 | #parens、#printer、#viz、#sierpinski、#dp 的徽章「講義補充」→「課堂略過・自學」。兩頁使用方式第 ④ 點改為：「標『課堂略過・自學』的節是講義內容，只是上課沒有細講，請自己讀完；標『（補充）』的收合區是網站另加、講義沒有的延伸，第一輪可略過。」 | `linear_structures.html`、`recursion.html` |
| 9 | linear_structures | 迴文動畫訊息改用 `push_back`／`pop_front`／`pop_back`。 | `linear_structures.html`（主 script） |
| 10 | linear_structures | deque.png 圖說補「圖中 rear 在左、front 在右；後面的操作表與動畫依 STL 的習慣，把 front 畫在左邊。」 | `tools/enrich/content/linear_figures.py` |
| 11 | linear_structures | stack 互動提示改為：預設已放入 4、dog、true，top 是 true；push／pop／top 的作用；連按 pop 到清空就是 `empty()` 為 true、`size()` 為 0。 | `linear_structures.html` |
| 12 | linear_structures | 「各節都會列出兩者的對照」→「stack、queue、deque 三節各附一張兩者的對照表」（三節確實各有一張）。 | `tools/enrich/content/linear_depth.py` |
| 13 | linked_lists | REF 列改「讀第 k 項（k 從 0 起算）」，串列欄 $O(k)$，備註「要從 head 走 k 步（k = 0 時直接讀 head）」；EX1 題幹補「（k 從 0 起算）」，選項與答案不變。 | `tools/enrich/content/linked_depth.py` |
| 14 | linked_lists | dIns 的 mid 案例改為在 54 ↔ 26 ↔ 93 中把 77 插在 26 與 93 之間，與圖一致；按鈕改「77 插在 26 與 93 之間」。front、empty 案例不變。 | `tools/enrich/content/linked_interactions.js`、`linked_depth.py` |
| 15 | linked_lists | #stl 徽章「cppds §4.7」→「講義 04 延伸」。 | `linked_lists.html` |

各章驗證 README（`docs/verification/20261008-ch{4,5,6}/README.md`）的 gen 區外手改清單已補上這次的條目。

## 驗證

- 三章 `pipeline.sh` 各連跑兩次：sha256 相同。
- `DSCPP_PAGES=linked_lists python3 docs/verification/20261003-ch3-ch4/check_content.py`：23 examples passed，generators stable，IDs／anchors／JS syntax 通過（跑完已 `git checkout` 還原 content-results.json）。
- `20261008-ch{4,5,6}/check_content.py`：ch4 22/22、ch5 17/17、ch6 13/13，errors 0；ch4、ch6 的 content-results.json 只有暫存路徑變動，已還原。
- `python3 tools/check_links_cpp.py`：22 頁，0 錯誤／0 警告。
- 三頁所有 inline script `node --check` 通過。
- 改前改後比對：三頁的 `pre`、`data-expected`、`href`、`id`、`.pseudo-code` 完全相同。
- `20261008-ch{4,5,6}/check_browser.py`（1440、390）：無 page error、無水平溢出；ch4 12 個播放器、34 案例、315 格單步完成；ch5 15 個播放案例完成；ch6 7 個播放器完成，3 個 canvas 有像素（spiral 5856、tree 4654、sierpinski 80510 個非透明像素）。browser-results.json 與截圖已更新。
- Playwright 單步（`fixes-ch4-6-steps/step.py`、結果 `step.json`）：
  - #3：spiral 狀態「總共呼叫了 21 次」；tree 第 1–5 層為 3／7／15／31／63 次；截圖 `spiral.png`、`tree.png`。
  - #4：n = 3、4、5 時分別 7、15、31 步（2^n − 1），最後盤子全在 B（pegs = `[[], [n…1], []]`）；每步高亮 `moveDisk(fromPole, toPole);`。
  - #7、#9：parens 四種輸入、233→base 2、兩個中序式、後序求值、radar／lsdkjfskf，每格的高亮行文字都與訊息對應（例：運算元→`if (isOperand(token)) output.push_back(token);`，數字→`if (isNumber(token)) operandStack.push(stod(token));`）。
  - #14：mid 案例第 0 格「newNode 是新配置的節點 77，要插在相鄰的 26 與 93 之間」，四步依序高亮第 2–5 行，結果 `header ↔ 54 ↔ 26 ↔ 77 ↔ 93 ↔ trailer`；front、empty 案例訊息不變。

## 讀者清單以外的連帶修改

- palFrames 行號（起始→2、比較成功→6）與迴文訊息一起修，讓高亮行和訊息一致。
- tree 滑桿由 1–9（預設 7）改為 1–5（預設 5）：講義參數下只有五層，超過 5 不會再變。
- recursion 使用方式第 ④ 點的字卡說明改為「用語與正文一致，附中英對照」，因為部分字卡改成原文在前。

## 未做

- 第 8 項只改了五個 H2 徽章與兩頁頁首定義，沒有逐一對照講義 ipynb，核對現有「（補充）」收合區是否真的都不在講義裡。
