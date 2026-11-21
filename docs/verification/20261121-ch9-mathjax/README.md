# 第 9 章：手機寬度的公式溢出與 MathJax 後量寬度（2026-11-21）

內部紀錄，不連到學生頁面。做法與第 7 章相同（`../20261121-ch7-stable/README.md`「手機寬度的公式溢出」一節）。

## 原因

- `trees.html` 的主 script 在 `DOMContentLoaded` 時又呼叫一次 `MathJax.typesetPromise()`。它和 MathJax 自己的第一次排版重疊時，會把隱藏的 assistive MathML 也排成公式，讓頁面變寬；是否發生取決於載入時序。機制已在第 7 章重現。
- 正文的資訊框裡，`bf(x) = height(x.left) − height(x.right)` 是行內公式，寬 365 px，比 390 寬手機的可用寬度 259 px 還寬：details 全收合時頁面就有 418 px。
- 收合區裡的展示公式（AVL 平衡因子的推導等）沒有捲軸，展開後頁面最寬到 572 px。
- 360 寬時，行內的 $\max(a,b)-c=\max(a-c,b-c)$ 也放不下。
- 原本的 `check_browser.py` 擋掉所有 https 請求，MathJax 沒有載入，所以從沒量到這些。

## 修改

| 檔案 | 內容 |
|---|---|
| `hand_edits_mathjax.py`（可重複執行） | 拿掉第二次 `typesetPromise()`。頁面沒有 `<math>` 原始碼，script 也沒有在載入後寫入 TeX（命中的 `$` 都是 JS 的 `${…}` 樣板字串）。主 script 在 gen 區外，pipeline 不會蓋掉。 |
| `tools/enrich/content/trees_depth.py` | STYLE 加上展示公式 `max-width:100%; overflow-x:auto`；AVL 推導裡的 $\max(a,b)-c=\max(a-c,b-c)$ 改成獨立一行。 |
| `tools/enrich/content/trees_legacy.py` | balance factor 資訊框的定義改成兩行的 `aligned` 展示公式，手機上不必捲動（`bf-390.png`）。 |
| `ch9/check_browser.py` | 只放行 MathJax 的 CDN，等 `MathJax.startup.promise` 完成，確認有公式、沒有 merror，先在 details 全收合時量一次寬度，最後全展開時再量一次。 |
| `measure_formulas.py` | 量頁面寬度，並列出比所在區塊還寬的公式。 |

## 結果

| 項目 | 結果 |
|---|---|
| 修改前（`baseline-before.json`、`head-390.json`） | 390 寬：收合 418、展開 572；360 寬：收合 418、展開 572 |
| 修改後（`after.json`） | 390 寬：收合與展開都是 390；360 寬：收合 360、展開 361（檢查容許 1 px）；沒有放不下的行內公式，展示公式都在自己的框內捲動 |
| 冪等 | pipeline 加上 `hand_edits_mathjax.py` 連跑兩次，sha256 相同（`final-page.sha`） |
| `trees.html` 的 diff | 只有 CSS 一行、兩處公式、主 script 的第二次排版 |
| `ch9/check_content.py` | 16 個 run 區塊通過；2 個填空練習確實無法編譯；0 錯誤 |
| `ch9/check_browser.py`（1440 與 390） | MathJax 203 個公式、0 個 merror；收合與展開時寬度都等於視窗；各元件、quiz 16 題、詞彙卡 37 張正常；無 page error |
| `check_mathjax.py` | 第 7–9 章 0 個 merror，0 個殘留 `$…$` |
| `tools/check_links_cpp.py` | 0 錯誤 / 0 警告 |
| 可見字數（收合區外） | 22,314 → 22,349 |
