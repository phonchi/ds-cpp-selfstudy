# 第 7 章加強與第 7–9 章 quiz 統一（2026-11-13）

內部紀錄，不連到學生頁面。

## 來源與範圍

- 來源：使用者在 ChatGPT 上對第 7 章的 14 輪追問（分享頁以 React Router stream 內嵌，解出的全文：`source-dialog.md`）。對話中的說法逐項重算或對照講義後才採用；對話裡把「起點相同 → 路線相同」稱為 primary clustering 是錯的，頁面改用課本定義。
- 講義範圍依據：`~/ds_cpp/Slides/07_Searching and Sorting.ipynb`。
- 位置規則（使用者定案）：
  - 核心概念放在可見正文：解釋或修正講義既有說法、兩種群聚、gcd 條件、平方探查 (m+1)/2、二分搜尋停止條件、`static_cast` 理由、開放定址與鏈結法對照。
  - 講義沒教的方法與 API 放（補充）收合區：雙重雜湊（使用者明示要收合）、操作比較表與找最小值／範圍查詢（使用者指出 $O(\log n + k)$ 超出講義，開頭的表與相關段落全部收合，Map ADT 後與重點回顧中的同類句子刪除）、刪除與 tombstone、命名混淆、STL 搜尋工具、平方取中推導、加 3 探查與線性探查的等價。
- quiz：第 7 章正文與章末、第 8 章章末、第 9 章正文與章末，從 `sq-item` 改為第 3–6 章的 `quiz-box`。p1–p9 不動。

## 修改

| 檔案 | 內容 |
|---|---|
| `tools/enrich/quizbox.py`（新） | 共用 `quiz_box`、`lecture_quiz`、`QUIZ_CSS`、`QUIZ_CHECK_JS`、`ensure_quiz_check`。回饋先 HTML 跳脫再做屬性跳脫，因為 `quizCheck` 用 innerHTML；開頭的「正確。」「不對。」會去掉，改由 `quizCheck` 印出「正確 ✓」「不對 ✗」。 |
| `tools/enrich/content/search_depth.py`、`trees_depth.py` | `quiz()` 改用 `lecture_quiz`；STYLE 加入 quiz-box CSS。第 7 章另外接上 `search_more` 的新段落、移動線性探查程式的位置、FAQ「為什麼表的大小常選質數？」改為講義內（不標補充），並更新重點回顧。 |
| `tools/enrich/enrich_search.py`、`enrich_trees.py` | 冪等地確保 `<script id="quiz-check">` 存在。 |
| `tools/apply_zh.py` | ch7–ch9 的章末題庫輸出 quiz-box（label「自我檢測 · Qn」，qid `qBankN`）；p 頁維持 sq-item。 |
| `tools/enrich/content/search_more.py`（新） | 新增的教學段落、探查週期小工具（HTML 與自足的 script 都在 gen 區內）。 |
| `tools/enrich/content/search_quizzes.py` | `SITE_QUIZ` 5 題：二分搜尋停止條件、探查週期、表的大小與質數、平方探查走得到幾格、開放定址與鏈結法。 |
| `tools/enrich/content/search_programs.py` | 新程式 `stl_search`、`size_cast`、`probe_cycle`、`double_hash`；練習 1 的呼叫改用 `static_cast<int>(a.size()) - 1`。 |
| `tools/enrich/content/search_legacy.py` | 雜湊元件改為四個策略按鈕；側欄「建議用質數」改為「是質數」；rehash 方塊限定為固定跳格，並寫明平方探查從 h 起算。 |
| `tools/enrich/content/search_figures.py` | 群聚圖說改為 9、10、0、1、2 一整段。 |
| `tools/enrich/content/search_headers.py` | 6 個排序函式同步課程標頭（ds_cpp `bdbf3df` 加入 `sortingTrace`，預設照舊印出，輸出不變）；正文補一句 `sortingTrace` 的說明。 |
| `data/questions_zh/ch7.json` | 8 → 11 題（`find` 用在已排序資料、空 vector 與 `static_cast`、餘數法碰撞條件）。 |
| `data/flashcards_zh/ch7.json` | 35 → 36 張（探查序列）；「群聚」的說明改為連成一段的定義。 |
| `searching_sorting.html`、`graphs.html`、`trees.html` | 由 pipeline 重建。 |

### gen 區外的手改

- `hand_edits_widget.py` 會整段替換 `searching_sorting.html` 的 `initHashing()`，可以重複執行。改了這些地方：
  - 加入加 3 與平方探查；開放定址共用一張表，判斷改用 `isOpen()`。
  - 探查耗盡時回報實際碰到的 slot 數，平方探查不會說成「已掃過整個表」。
  - 新增 `epoch`：清空或切換策略時，播到一半的動畫與批次插入會停止，不會把舊的表寫回來。這是 astra 審查抓到的既有競態。
  - 狀態列第二次以後的探查改說「雜湊值 h 那一格已被佔用，第 k 次試 slot p」。
- `hand_edits_animator.py`：修 Animator 的 `setPointers()`，可以重複執行。
  - 原本隱藏指標的 `setTimeout` 回呼在 200 ms 後讀 `this.pointers[name]`。如果這段時間內按了重置，`buildBars()` 已把它換成 `{}`，回呼就會丟出 `Cannot read properties of undefined (reading 'el')`。
  - 這是既有的時序問題，最終驗收時偶發出現兩次。現在回呼保留自己的參照，不再讀 `this.pointers`。

## 結果

| 項目 | 結果 |
|---|---|
| 基線 | 修改前三章 pipeline 重跑，sha256 不變（`sha-before.txt`） |
| 冪等 | 第 7 章 pipeline 連跑兩次 sha256 相同；第 8、9 章也重建過 |
| C++（`ch7/check_content.py`，`g++ -std=c++17 -Wall -Wextra -pedantic`） | 26 個 run 區塊無警告，輸出與 `data-expected`、可見輸出逐字相同；2 個填空練習確實無法編譯；標頭複本 17 個函式都在課程標頭內；0 錯誤 |
| quiz-box 靜態檢查（ch7/8/9 `check_content.py`） | 沒有殘留 sq-item；每題四選一、一個正解、有字母與 handler、回饋無多餘標籤、qid 不重複；0 錯誤 |
| 瀏覽器（ch7/8/9 `check_browser.py`，1440 與 390） | details 全展開、圖片載入、動畫面板、雜湊四種策略的批次結果（加 3：`77 55 — 44 26 93 17 20 — 31 54`；平方：`77 44 20 55 26 93 17 — — 31 54`）、平方探查搜尋命中與失敗、插入 11 時耗盡（6 個 slot）、切換到一半的競態、探查週期工具 5 組；三章 quiz 答錯與答對都顯示「不對 ✗」與「正確 ✓」；無水平溢出、無 page error |
| MathJax（`check_mathjax.py`，真實網路） | 第 7–9 章都載入完成，0 個 merror，0 個殘留 `$…$` |
| `tools/check_links_cpp.py` | 0 錯誤 / 0 警告 |
| 對比 | 0 失敗（`tools/check_contrast.py` 遇到 `tools/template/` 會誤走 statlearning 分支而崩潰；改用它的手寫站分支逐頁呼叫 `check()`。這是既有問題） |
| `tools/inject_prereq_cpp.py` | import 成功，仍能從本頁抽出 sq-item CSS/JS；p1、p4、p9 重套 `apply_zh` 後 diff 為空 |
| 可見字數（`density.py`） | 收合區外 24.6k → 29.0k（預算 ≤ 30k）；quiz 15 → 23；details 35 → 42 |

## 跨模型審查

- **astra（Codex gpt-6-astra，唯讀）**
  - 計畫審查 job `e40a3f29-fc9b-4556-a7de-ab6c9941a308`：數學全部正確；9 項 should-fix／nit 併入計畫。
  - 成品審查 job `8dbe6df6-2021-4d3d-9db1-bd83d6ca6f2d`：
    - 策略切換競態（已修，並加入瀏覽器重現測試）；
    - 章末 Q9 平均次數的說法（已改為「大約 n / 2」並寫出假設）；
    - Q11 缺絕對值（已改為 `0 < |k1 − k2| < m`）。
  - 紀錄存在 `~/.local/share/claude-codex-collab/runs/<job>/`。
- **Fable（原生 subagent，學生視角順讀）**
  - 重算所有數字無誤；回報 24 項閱讀問題。
  - 已處理：rehash 通式與平方探查的矛盾、練習 1 的轉型、平方探查 (m+1)/2 的理由、gcd 全名與推理、STL 全名位置、FAQ 補充標示、線性探查程式位置、群聚圖說與詞彙卡、「與質數無關」的措辭、兩題 quiz 選項、比較表停止條件、`static_cast` 適用兩個版本、函式物件例子、中點兩種寫法、符號與「加 3 探查」名稱、最多比較次數、狀態列文字、重複句。
  - 未處理，屬既有內容的結構問題，留待之後整理：
    - 雜湊元件出現在碰撞解決之前，「小實驗」離元件太遠；
    - PART 03 開頭重複定義 slot 與雜湊函數；
    - 全頁「鍵／key」「槽／slot」等中英用語混用；
    - 折疊法反轉版的例子和講義的數字不同（總和相同）；
    - ADT 沒有全名（前面章節已定義）。

## speak-human-tw

非互動模式（跳過確認、事後摘要）。這次找到並修改了 3 處：

1. STL 收合區重複「`find` 只透過迭代器一格一格往後走，所以任何容器都能用」：刪除，正文已經說過。
2. 「所以線性探查會連成一串的情形……」：刪掉「所以」，這一段的「所以」用得太密。
3. 「所以『最小的 key 是哪個』……都得把整張表看一遍」：改成「要找『最小的 key 是哪個』或……，都得把整張表看一遍」。

新增文字沒有半形中文標點、中國用語或破折號（表格中的「—」是空值）。

## 未做

- `tools/island_meta.py` 的群島說明仍寫「選線性探查或鏈結法」。這句仍然成立，而改它需要重建 `island/index.html`，該檔有其他工作的未提交修改，所以沒有動。代表圖 `island/figs/searching_sorting.webp` 已重新產生。

## 第二輪：講義範圍與推導（同日）

使用者要求：
- 超出講義的內容一律收合；
- 全章不明顯的結論都要附簡短推導；
- 完成後在 Herdr pane 審閱。

收合（正文只留講義範圍內的說明）：
- 操作比較表與 $O(\log n + k)$：移到「不同存法擅長的操作」，並附推導；Map ADT 後與重點回顧中的同類句子已刪除。
- gcd 條件、探查週期工具與相關兩題 quiz：移到「為什麼質數走得遍」，正文只留講義的質數建議與 12 格／11 格的例子。
- 平方探查的兩個限制（次要群聚、只碰得到 $(m+1)/2$ 格）連同推導與 quiz：移到收合區。
- 負載因子的平均比較次數公式：寫明假設、計數單位與近似，並附推導；Knuth 的線性探查失敗搜尋公式標為引用。側欄的公式列已移除。
- 合併排序側欄的 $\Omega(n\log n)$、`std::stable_sort`、C++20 的轉換規則：移出正文。

新增推導（都在收合區）：
- 有序循序搜尋找不到時的平均；
- 二分搜尋最多 $\lfloor\log_2 n\rfloor+1$ 次；
- 選擇排序的比較與交換次數；
- 插入排序的最佳、最差與平均（逆序對）；
- 希爾排序：最佳 $n\log_2 n - n + 1$、折半增量 $\Theta(n^2)$ 的上下界、$2^k-1$ 的 $O(n^{3/2})$ 概要；
- 合併排序：寫回次數、最差比較次數、$O(n)$ 額外空間、決策樹下界；
- 快速排序：最差加總、理想模型下的平均遞迴式，以及本章實作與模型的差異。

審閱後修正的既有問題：
- 完美雜湊函數的說法；
- 鏈結串列上的二分搜尋與 merge 的空間；
- 快速排序的「就地」與空間；
- `put()` 補充區的兩句；
- 分割點改成「不大於／不小於」；
- 三數取中動畫補記 3 次比較（`hand_edits_animator.py`）；
- 詞彙卡的 Split Point 與 Median of Three；
- 「實務通用、最快」改為附條件的建議；
- 有序循序搜尋表的平均改為 $\frac{n+1}{2}$ 與「約 $\frac{n}{2}$」。

Herdr pane 審閱（astra，唯讀）：
- 第一輪 job `c62bf1bc-21bb-4818-a1a0-79be06982691`：意見全文見 `pane-review-1.txt`，都已核實並處理。其中快速排序的模型差異與三數取中漏算，都先用程式重現過。
- 第二輪 job `45391494-0daf-4ca5-a55b-1454252ef544`：逐條核對第一輪意見（全文見 `pane-review-2.txt`）。已確認修好的有：快速排序模型、負載因子、gcd 可達性、合併排序、二分搜尋、平方探查、選擇與插入排序。殘留項目隨後處理：
  - 希爾排序「gap 小時陣列已接近排好」改為「通常」；
  - partition 三段與 Quick Sort 詞彙卡改用「不大於／不小於」；
  - 有序循序搜尋補上「落在各空隙機率相同」的假設；
  - 雜湊表成本補上「雜湊與 key 比較為 $O(1)$」；
  - `unordered_map` 的實作說明與嵌入式用途移出正文；
  - 完美雜湊改成「對事先知道的固定資料集合可以另外建構」；
  - 鏈結串列二分搜尋改為「可以，但總時間 $O(n)$」；
  - 「就地」明定不計遞迴堆疊；
  - `put()` 補充區末段改正；
  - 拿掉 quicksort「常數比 merge sort 小」；
  - 前言改為「以比較次數為主，另標探查、移動與寫回」；
  - 三數取中改成明確的比較交換並逐次計數，6 種排列都選到中位數，實際比較 2 或 3 次。
- 仍為引用、未推導：線性探查失敗搜尋的 $\frac{1}{2}\left(1 + \frac{1}{(1-\lambda)^2}\right)$（Knuth）。頁面上明確標為引用的結果，並用簡化模型說明分母從哪裡來。
