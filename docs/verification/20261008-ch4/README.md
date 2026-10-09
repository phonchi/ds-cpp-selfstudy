# 第 4 章 linked_lists 密度補齊驗收（2026-10-08）

## 範圍

只針對弱點補齊，既有結構、播放器（12 個、34 個案例）與 gen 架構不動。來源：`/home/phonchi/ds_cpp/Slides/04_Linear_Linked_Structure.ipynb`、`pythonds3/cppds/linked_list.hpp`、講義圖 `nsysu-math208/static_files/presentations/imgs/`。

修改／新增：

- `linked_lists.html`（gen 區由產生器重建；gen 區外只做一次性手改：新增 `<section id="recap">` 與其 gen 標記、float-nav／目錄加 `#recap`、REF 標題與導覽字樣改為「操作成本總覽」、使用方式第 ④ 點加回顧連結）
- `tools/enrich/content/linked_depth.py`：`snippet`／`lecture_program` 改為輸出 `data-cpp`（run／fragment／compile-error）與 `data-expected`；加厚 prologue、node、unordered、ordered、variants；新增 `recap_section()`（gen `linked-recap`）；新增講義 quiz `qOrd`、`qCx`；所有頁內 quiz 改成四選一
- `tools/enrich/content/linked_programs.py`（新）：14 個完整程式與其輸出
- `tools/enrich/content/linked_figures.py`：新增 20 張講義圖的 spec 與 `steps()`（逐步圖收合）
- `assets/figures/ch4/`：新增 20 張講義圖
- `docs/verification/20261003-ch3-ch4/check_content.py`：修正失效 import（見下）

`enrich_linked.py`、`data/flashcards_zh/ch4.json` 沒有改：字卡 11 張已逐一對應講義 Key terms 的 11 個詞。
- 2026-10-09 讀者審閱修正（詳見 `docs/verification/20261009-reading/fixes-ch4-6.md`）：#stl 的 h2 徽章由「cppds §4.7」改為「講義 04 延伸」。
- 2026-10-09 第二輪讀者審閱修正（詳見 `docs/verification/20261009-reading/fixes-ch4-6-round2.md`）：#stl 徽章再改為「講義 04」；使用方式框的標記說明加入「課堂略過・自學」的定義。

## 結果（全部實際執行，紀錄見 `run.log`）

| 項目 | 結果 |
|---|---|
| C++：`g++ -std=c++17 -Wall -Wextra -pedantic -I/home/phonchi/ds_cpp/Slides` | 22 個 `data-cpp="run"` 全部編譯無警告、執行輸出與 `data-expected` 及頁面上顯示的輸出逐字相同；1 個 `compile-error`（直接存取 private `next`）確實編譯失敗。`content-results.json` |
| 冪等：`pipeline.sh`（enrich_linked → apply_zh --pages linked_lists → shuffle_quiz.ensure）跑兩次 | 兩次 sha256 相同 |
| 重複 id／懸空錨點／img 屬性與檔案／inline script `node --check` | 0 錯誤 |
| `tools/check_links_cpp.py`、`tools/check_contrast.py` | 0 錯誤／0 警告；0 失敗 |
| Chromium 1440、390（`check_browser.py`） | 38 個 details 全展開；24 張圖 naturalWidth>0；12 個播放器 34 個案例從第 0 格單步到底（共 315 步）並以最快速度播放到結束；10 題 quiz 皆四選一且答錯／答對有回饋；11 張字卡翻面、全翻、洗牌可用；無水平溢出、無 page error。`browser-results.json`、截圖 `linked_lists-*-{1440,390}.png` |

## 密度（`density.py`；文字為 `.container` 內去掉 style/script 後的非空白字元）

| 指標 | 前 | 後 | 第 1–3 章 |
|---|---|---|---|
| 可見文字 | 21,031 | 37,178 | 22k–34k |
| h2／h3 | 9／19 | 10／27 | — |
| img | 4 | 24 | 0–6 |
| details | 20 | 38 | 0–28 |
| .pseudo-code | 28 | 43 | 19–42 |
| 收合區外的預期輸出 | 4 | 15 | 10–21 |
| 全部預期輸出 | 8 | 25 | — |
| data-cpp 區塊 | 0 | 31 | — |
| quiz | 8 | 10 | — |
| 字卡 | 11 | 11 | — |

## 舊檢查腳本修正

`20261003-ch3-ch4/check_content.py` 原本 `from content.linked_depth import EXAMPLES`，該名稱已不存在。改為兩頁都從頁面上的 `[data-cpp="run|compile-error"]` 區塊收集程式與 `data-expected`；另加環境變數 `DSCPP_PAGES`（預設兩頁）以便只檢查一頁。本次以 `DSCPP_PAGES=linked_lists DSCPP_VERIFY_OUT=legacy-check` 執行，23 個範例通過、產生器冪等；未執行 arrays 部分（避免重建 arrays.html）。

## 限制

- 瀏覽器測試封鎖所有外部請求，MathJax 與 Google Fonts 未載入，未驗證公式排版。
- 可見文字（37k）與 details（38）略高於第 1–3 章範圍，主要來自講義範例的收合完整程式與逐步圖。
- 新文案未另做 speak-human-tw 潤稿。
