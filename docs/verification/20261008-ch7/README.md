# 第 7 章 searching_sorting 依講義擴充驗收（2026-10-08）

## 範圍

來源：`/home/phonchi/ds_cpp/Slides/07_Searching and Sorting.ipynb`、`pythonds3/cppds/{searching,hashtable,sorting}.hpp`、`questions/ch7/*.json`、講義圖 `nsysu-math208/static_files/presentations/imgs/`。

修改／新增：

- `searching_sorting.html`
  - 一次性（`place_markers.py`）：13 個 section 的 h2 之後原有內容全部移進 `<!-- gen:search-<sid> -->`，手寫部分存到 `tools/enrich/content/search_legacy.py`；舊 enrich 注入的 8 段卡片（`dx-srch/hash/bub/sel/ins/shl/mrg/qck`，共 42,117 字元）與舊的 Exercise 3 區塊一併移除，改由 gen 重建並帶 `data-cpp`。動畫面板 HTML 原樣搬入，主 `<script>`（Animator）未改。
  - 一次性（`hand_edits.py`）：新增 `<section id="recap">`（gen `search-recap`）、float-nav 與目錄加 `#recap`（SUM）、supplement 的 h2 由「兩個 PDF 上不容易看出來的細節」改為「平方探查與 put() 分支的逐步追蹤」、使用方式第 ④ 點加回顧連結並說明（補充）收合區。
  - 在 search_legacy.py 內直接修的舊內容：`<code>False</code>`→`false`；Map ADT 表 `in` 列改為 `contains(key)`；supplement 的 `h[77]="bird"` 這類非本課 C++ 寫法改為 `h.put(77, "bird")`、`HashTable h(11);`；hashStr 側欄移除與講義不同的虛擬碼；合併排序說明「寫進新 list」改為「寫回原本的 vector」；移除與講義命名不符的 `binarySearchRecRange(a, …, mid)` 卡與 orderedSequentialSearch／bubbleSortShort 的非講義虛擬碼卡（改為講義完整程式）。
- `tools/enrich/enrich_search.py`：改寫為 gen 驅動、冪等的 driver（不再注入舊內容）；同步目錄與 float-nav 的字卡數、題數標籤。
- `tools/enrich/content/search_depth.py`、`search_legacy.py`、`search_programs.py`、`search_headers.py`（課程標頭函式逐字複本）、`search_figures.py`、`search_quizzes.py`（新）。
- `assets/figures/ch7/`：25 張講義圖（swap.png 屬上課略過的 cell，未用）。
- `data/flashcards_zh/ch7.json`：32 → 35 張（原 32 張已涵蓋講義 32 個 Key terms；新增 Slot、Clustering、Short Bubble；「二次探查」「摺疊法」改為與正文一致的「平方探查」「折疊法」）。
- `data/questions_zh/ch7.json`：原 7 題就是講義的 7 個 quiz，已改放正文各節；題庫改為 8 題章末自我檢測（四選一、每個選項有自己的回饋）。

未呼叫 `chapter_math.render_math` 與 `course_recordings.apply_recording`。`teaching_copy.EDITS['searching_sorting']` 維持空清單。

## 結果（全部實際執行，紀錄見 `run.log`）

| 項目 | 結果 |
|---|---|
| C++（`g++ -std=c++17 -Wall -Wextra -pedantic -I/home/phonchi/ds_cpp/Slides`） | 22 個 `data-cpp="run"` 無警告編譯，stdout 與 `data-expected` 逐字相同、與頁面可見輸出（去掉結尾換行）相同；2 個 `exercise`（練習 1、2 填空）確實編譯失敗。`content-results.json` |
| 標頭複本 | `search_headers.py` 的 17 個函式本體逐字出現在 `sorting.hpp`／`searching.hpp` |
| 冪等：`pipeline.sh`（enrich → apply_zh --pages → shuffle_quiz.ensure 本頁）跑兩次 | sha256 相同 |
| 重複 id／懸空錨點／img 屬性／inline script `node --check`／每節有 h3／15 個 sq-item 四選一且各有回饋／圖檔全部被引用 | 0 錯誤 |
| `tools/check_links_cpp.py`、`tools/check_contrast.py` | 0 錯誤／0 警告；0 失敗 |
| Chromium 1440、390（`check_browser.py`） | 35 個 details 全展開；25 張圖 naturalWidth>0；8 個 Animator 面板（seq、bin、bubble、sel、ins、shell、merge、quick）從重置狀態直接按 → 單步 5 次、↺ 重置、套用、▶ 最快速度播到「重播」；shell gap 與 quick pivot 切換後可單步；雜湊面板批次插入、插入 44、搜尋 44、切換鏈結法再批次插入都正確；15 題 quiz 答錯答對都有回饋；35 張字卡翻面／全翻／洗牌可用；無水平溢出、無 page error。截圖 `searching_sorting-{hashing,quick}-{1440,390}.png` |

## 密度（`density.py`）

| 指標 | 前 | 後 | 第 1–3 章 |
|---|---|---|---|
| 文字（含收合區） | 28,964 | 47,009 | 22k–34k |
| 文字（收合區外） | 28,964 | 24,401 | 16.9k–27.6k |
| h2／h3 | 15／29 | 16／44 | — |
| img | 0 | 25 | 0–6 |
| details | 0 | 35 | 0–28 |
| .pseudo-code | 33 | 49 | 19–42 |
| 收合區外的預期輸出 | 11 | 19 | 10–21 |
| data-cpp 區塊 | 0 | 39 | — |
| quiz（sq-item） | 7 | 15 | — |
| 字卡 | 32 | 35 | — |

收合區外的文字反而變少：原本攤開的「依賴的資料結構」「九個演算法比較」「補充 A／B」三節改為（補充）收合。總文字與 details 數高於基準，主要是收合的完整程式與標頭原始碼。

## speak-human-tw 潤稿摘要

非互動模式（跳過確認、事後摘要），檢查新增文字，找到並修改 3 處：

1. 「要記住：雜湊函數本身必須有效率」→ 刪掉「要記住：」（解說導引句）。
2. 「關於移動和交換：一次移動大約只有……」→ 刪掉導引前綴，直接陳述。
3. 「這一行寫起來很短，背後仍然要一個一個比對。搜尋的做法有很多種，接下來幾節逐一介紹。」→ 併成一句「……；搜尋還有其他做法，接下來幾節逐一介紹。」

新增文字無破折號；全形標點已檢查。

## 限制

- 瀏覽器測試封鎖外部請求，MathJax 與 Google Fonts 未載入，未驗證公式排版。
- quick 面板的「虛擬碼」區塊沒有 `data-l` 行號，動畫無法高亮程式行（既有設計，未改）。seq 面板的結果欄顯示 Python 式的 `True`／`False`（既有 JS 文字，未改）。
- 題庫改為非講義題目，但 `tools/apply_zh.py` 對 ch* 題庫固定輸出「課程題庫 ch7」徽章與「題目取自課程題庫（已譯為繁體中文）」導語，這句現在不精確；需主控決定是否調整 apply_zh（第 8、9 章也有同樣問題）。
- `place_markers.py`、`hand_edits.py` 為一次性腳本，內含防重跑保護。

## 2026-10-09 讀者審閱修正（gen 區外）

- `searching_sorting.html` 的 TOC 末段改成 REF → SUP → SUM → QUIZ → CARD，與 DOM 順序一致。其餘修正都在產生器來源，見 `docs/verification/20261009-reading/fixes-ch7-9.md`。
