# 第 6 章 recursion 依講義擴充驗收（2026-10-08）

## 範圍

來源：`/home/phonchi/ds_cpp/Slides/06_Recursion.ipynb`、`pythonds3/cppds/maze.hpp`、講義圖 `nsysu-math208/static_files/presentations/imgs/`。

修改／新增：

- `recursion.html`：12 個 gen 區由產生器重建。gen 區外的一次性手改：
  - 各 section 的 h2 之後原有內容全部移入 `<!-- gen:recursion-<sid> -->`（prologue、laws、tostr、frames、viz、sierpinski、hanoi、maze、dp、exercises、reference）；原本由舊 enrich 插入的三張 deck-extra 卡（`dx-fr`／`dx-hn`／`dx-mz`）一併由 gen 重建並帶 `data-cpp`。
  - 新增 `<section id="recap">`（gen `recursion-recap`），float-nav 與目錄加 `#recap`（SUM），使用方式第 ④ 點加回顧連結。
  - 主 `<script>` 的行號與文字：listSum 播放器改用 `numList`，高亮行改 3/5/9；迷宮播放器高亮行改 5/8/13/14/15（對應 maze.hpp 的 searchFrom）；DP 播放器高亮行改 9/11（對應 makeChange3），並刪除錯誤的「貪婪法會拿 5 枚：10+10+1+1+1」（有 21 分硬幣時貪婪法找 23 分正是 3 枚）。
- `tools/enrich/enrich_recursion.py`：改寫為 gen 驅動、冪等的 driver（取代舊的一次性插入）。
- `tools/enrich/content/recursion_depth.py`（新）、`recursion_programs.py`（新）、`recursion_figures.py`（新）、`recursion_widgets.py`（新，含 toStr(10, 2) 呼叫堆疊播放器的 JS，放在 `<script id="recursion-extra-js">`）。
- `assets/figures/ch6/`：18 張講義圖。
- `data/flashcards_zh/ch6.json`：7 → 12 張（原 7 張已對應講義 Key terms；新增呼叫堆疊、累加變數、碎形深度、回溯、短路求值）。

未呼叫 `chapter_math.render_math`（公式直接寫成 MathJax）與 `course_recordings.apply_recording`（無第 6 章條目）。`teaching_copy.EDITS['recursion']` 維持空清單。
  - 2026-10-09 讀者審閱修正（詳見 `docs/verification/20261009-reading/fixes-ch4-6.md`）：#viz、#sierpinski、#dp 徽章「講義補充」改「課堂略過・自學」，使用方式第 ④ 點重寫兩種標示的定義與字卡說明；主 `<script>` 的 spiral／tree 改用講義參數 `spiral(turtle, 100)`、`tree(75)`／`branchLen - 15` 並按比例放大；`hanoiFrames` 改為 `moveTower(n, "A", "B", "C")`（A→B、借 C）。

## 結果（全部實際執行，紀錄見 `run.log`）

| 項目 | 結果 |
|---|---|
| C++（`g++ -std=c++17 -Wall -Wextra -pedantic -I/home/phonchi/ds_cpp/Slides`，執行目錄為 Slides 以讀到 maze2.txt） | 13 個 `data-cpp="run"` 全部無警告編譯，輸出與 `data-expected` 及頁面顯示逐字相同（reverse 解答為 assert 程式，預期無輸出）；1 個 `exercise`（reverse 填空）確實編譯失敗。`content-results.json` |
| 呼叫次數 | 另以計數版程式（`call_counts.cpp`，輸出 `call_counts.txt`）確認：makeChange1 26 分 377 次、15 分 52 次、63 分 67,716,925 次；makeChange2 63 分 221 次，knownResults[2..4] 為 0（頁面的 MC_COUNT 補充程式也在上列 run 檢查內，63 分版因太慢未放入頁面） |
| 冪等：`pipeline.sh` 跑兩次 | sha256 相同 |
| 重複 id／懸空錨點／img 屬性／inline script `node --check`／每節有 h3／quiz 四選一 | 0 錯誤 |
| `tools/check_links_cpp.py`、`tools/check_contrast.py` | 0 錯誤／0 警告；0 失敗 |
| Chromium 1440、390（`check_browser.py`） | 21 個 details 全展開；18 張圖 naturalWidth>0；7 個播放器（sum、tostr、tsf、frame、hanoi、maze、dp）從頭單步到底，每格檢查程式高亮行存在，再以最快速度播放到結束；暫停鍵可停；3 個 canvas 重畫後有像素；10 題 quiz 四選一、答錯答對都有回饋；12 張字卡翻面／全翻／洗牌可用；無水平溢出、無 page error。截圖 `recursion-{frames,dp}-{1440,390}.png` |

## 密度（`density.py`）

| 指標 | 前 | 後 | 第 1–3 章 |
|---|---|---|---|
| 可見文字 | 9,762 | 30,457 | 22k–34k |
| h2／h3 | 12／2 | 13／44 | — |
| img | 0 | 18 | 0–6 |
| details | 0 | 21 | 0–28 |
| .pseudo-code | 15 | 35 | 19–42 |
| 收合區外的預期輸出 | 4 | 11 | 10–21 |
| data-cpp 區塊 | 0 | 35 | — |
| quiz | 7 | 10 | — |
| 字卡 | 7 | 12 | — |

可見輸出 11 段：講義本章可執行的程式只有 12 個（CTurtle 程式不執行），未為了湊數另加。

## speak-human-tw 潤稿摘要

以非互動模式（跳過確認、事後摘要）檢查新增文字，找到並修改 3 處：

1. hanoi 程式說明「正是因為這樣直接回傳，上一層才能接著執行 moveDisk」→「base case 一回傳，上一層就接著執行 moveDisk」（去強調套語）。
2. dp「事實上，這樣做還不算動態規劃」→「嚴格說來，這樣做還不算動態規劃」（去填充詞）。
3. prologue「這正是遞迴的想法」→「這就是遞迴的想法」。

其餘文字無破折號、無三段式套話；全形標點已檢查。

## 限制

- 瀏覽器測試封鎖外部請求，MathJax 與 Google Fonts 未載入，未驗證公式排版。
- 講義 quiz `recursive1.json`（{2,4,6,8,10} 有 4 次遞迴呼叫）是依「只剩一個元素為 base case」的舊版寫的；本頁改寫成符合 `listSumFrom`（空範圍 base case）的題目 `qSumCalls`，答案 6 次呼叫。講義題目本身與講義程式不一致，需講義端決定是否修正。
- 迷宮動畫用頁面自有的小迷宮，不是 maze2.txt；講義程式的實際輸出另以 run 區塊呈現。
- 播放器「→ 單步」需先按「▶ 開始」建立播放器（既有設計，未改）。
