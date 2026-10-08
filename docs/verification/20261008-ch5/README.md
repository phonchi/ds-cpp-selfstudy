# 第 5 章 linear_structures 依講義擴充驗收（2026-10-08）

## 範圍

來源：`/home/phonchi/ds_cpp/Slides/05_Linear_Structure.ipynb`（未使用 `05_Linear_Structure_2.ipynb`）、`pythonds3/cppds/{stack,queue,deque,expression}.hpp`、講義圖 `nsysu-math208/static_files/presentations/imgs/`。

修改／新增的檔案：

- `linear_structures.html`
- `tools/enrich/enrich_linear.py`：改寫成 gen 驅動的 driver（舊的 `insert_end_of_section` 注入全部移除）
- `tools/enrich/content/linear_depth.py`（新）：22 個 gen 區塊
- `tools/enrich/content/linear_programs.py`（新）：講義程式、標頭片段與 `OUTPUT`
- `tools/enrich/content/linear_figures.py`（新）：16 張講義圖的 figure spec
- `assets/figures/ch5/`：16 張講義圖
- `data/flashcards_zh/ch5.json`：未改（16 張已逐一對應講義 Key terms 的 16 個詞）

gen 區以外的一次性手改（`place_markers.py` 的內容，僅執行一次）：

- 放置 22 對 `<!-- gen:linear-* -->` 標記。
- 移除舊產生器注入的 `dx-stl-api`、`dx-base`、`dx-infix`（含 5 張卡）、`dx-dq` 區塊，以及手寫的 Stack2 搬移表、`一般化：三種括號混用`（含錯誤的 `"([{{"`）、revString 解答卡、印表機的三張程式卡、結果表與 what-if 框、REF 兩張比較表與「關鍵概念複習」框；這些內容改由 gen 區產生（站內沒有連到 `dx-*` 的錨點）。
- Stack／Queue／Deque 的 ADT 操作表改成講義的列（Queue 補上 `q.empty()`，Deque 補上 `d.empty()`）；中序／前序／後序表補上 `A * B + C * D`。
- 動畫側欄程式：`postfixEval` 改為 `double`／`stod`／`operand1`、`operand2`，標題加「（簡化）」；`hotPotato` 參數改 `nameList`、`simQueue`；`palChecker` 改 `aString`、`charDeque`。行數與 `data-l` 不變，JS 未改。
- 兩處「（RISE skip）」字樣改為「課堂上略過…，屬於自學內容」。
- 原有 10 題三選一的頁內 quiz 各補一個選項與錯因說明，成為四選一。
- 使用方式第 ② 點改為「講義的完整程式收在各節的收合區…」（原句要學生回講義看完整程式，已不符）。
- REF 的 h2 改為「參考資料與三種 ADT 比較」；新增 `<section id="recap">`（重點回顧與常見疑問）及其 float-nav、目錄連結；使用方式第 ④ 點加回顧連結。

## 結果（全部實際執行，紀錄見 `run.log`）

| 項目 | 結果 |
|---|---|
| C++：`g++ -std=c++17 -Wall -Wextra -pedantic -I/home/phonchi/ds_cpp/Slides` | 18 個 `data-cpp="run"` 全部編譯無警告，輸出與 `data-expected` 及頁面顯示的輸出逐字相同（`content-results.json`）。本章沒有 `compile-error` 區塊。 |
| 冪等：`pipeline.sh`（enrich_linear → `apply_zh.py --pages linear_structures` → `shuffle_quiz.ensure`）跑兩次 | 兩次 sha256 相同 |
| 重複 id／懸空錨點／img 屬性與檔案／gen 標記成對／inline script `node --check`／每節有 h3／quiz 四選一且單一正解 | 0 錯誤 |
| `tools/check_links_cpp.py`、`tools/check_contrast.py` | 0 錯誤／0 警告；0 失敗 |
| Chromium 1440、390（`check_browser.py`） | 34 個 details 全展開；16 張圖 naturalWidth>0；7 個播放器 15 個案例從第 0 格單步到底（共 204 步），程式面板都有高亮行，並以最快速度播放到結束；stack／queue 手動元件 push、pop、top 可用；16 題 quiz 答錯／答對皆有回饋；16 張字卡翻面、全翻、洗牌可用；無水平溢出、無 page error。截圖 `linear_structures-{stack,infix}-{1440,390}.png` |

## 密度（`density.py`；文字為 `.container` 內去掉 style/script 後的非空白字元）

| 指標 | 前 | 後 | 第 1–3 章 |
|---|---|---|---|
| 可見文字 | 14,775 | 40,588 | 22k–34k |
| h2／h3 | 12／9 | 13／41 | — |
| img | 0 | 16 | 0–6 |
| details | 0 | 34 | 0–28 |
| .pseudo-code | 22 | 47 | 19–42 |
| 收合區外的預期輸出 | 5 | 14 | 10–21 |
| data-cpp 區塊 | 0 | 38 | — |
| quiz | 10 | 16 | — |
| 字卡 | 16 | 16 | — |

文字超出範圍，主要是收合的完整程式（全頁程式碼約 16k 字元）；收合區外的文字約 25k。可見輸出 14 段即講義 12 個程式加 2 個練習的預期輸出，沒有為湊數另加。

## 文案潤稿（speak-human-tw，非互動執行，事後摘要）

對新增文字找到並修改 7 處：刪「換句話說」「這正是」「就某種意義來說…提供了所有能力」等套話與「不只…也」句型，「最重要的用途之一」「是抽象化的一個例子」「說明…的重要性」改為直述。程式碼、輸出、數字與連結未動。

## 限制

- 兩個上課略過的節中有網站自加的（補充）收合區：印表機節的「單獨試用引擎與分佈」、「連續跑 10 次試驗」、「三個問題各要改哪裡」；括號節沒有另加補充。正文本身不超出講義。
- `I2P_MAIN` 保留講義原註解 `// the complete converter (md listing above)`，指的是 notebook 中的程式列表。

- 未呼叫 `chapter_math.render_math`：在本頁試跑時會把 `7 8 + 3 2 + /` 改成 `7 $8 + 3$ 2 + /`、把 `2 ^ 3 ^ 2 = …` 斷成數學式，並把按鈕文字 `pop` 包成 `<code>`。新增文字直接寫 `$…$`；quiz 回饋與狀態列不含 `$`（它們以 innerHTML 寫入，不會重新排版）。手寫區的 `O(n)` 仍為純文字。
- 瀏覽器測試封鎖外部請求，MathJax 與字型未載入，未驗證公式排版。
- 印表機模擬的輸出取決於標準函式庫的 `uniform_int_distribution` 實作；頁面數字為 g++／libstdc++ 的結果，正文已說明換編譯器可能不同。
