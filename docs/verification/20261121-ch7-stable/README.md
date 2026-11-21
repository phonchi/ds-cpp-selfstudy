# 第 7 章：穩定排序移到正文，補充排序對話（2026-11-21）

內部紀錄，不連到學生頁面。

## 來源與範圍

- 使用者要求：
  - 把「穩定（stable）」從收合區移到正文，並寫得更詳細；
  - 依 ChatGPT 分享對話（20 題，全文 `source-dialog.md`）補充內容，超出講義的放（補充）收合區。
- 講義依據：`~/ds_cpp/Slides/07_Searching and Sorting.ipynb`。講義只在合併排序提到 stable（cell 209）。課程標頭 `~/ds_cpp/Slides/pythonds3/cppds/hashtable.hpp:18` 的 `hashFunction` 是 `(key % size + size) % size`。
- 已定決策：
  - 穩定排序放在 `#reference` 可見的開頭；
  - `std::sort` 不穩定與 `std::stable_sort` 放（補充）；
  - 驗證後兩個 repo 都 commit 並 push。
- 位置規則沿用 11/13：解釋講義既有的說法或程式放正文；講義沒教的方法、API 與推導放（補充）。
- 對話中的程式（最後一個元素當 pivot、`key`/`j` 命名）沒有搬進頁面；所有例子都用課程標頭的迴圈，數字都重新算過。

## 修改

| 位置 | 內容 | 可見／收合 |
|---|---|---|
| `#reference` 開頭（`search_more.stable_section`） | 定義、成績單的多鍵排序例子、六個實作的判斷表（指出決定穩定性的比較運算子）、帶標籤資料的示範程式與三個反例的逐步說明、改運算子就變得不穩定、新 quiz | 正文 |
| 同上 | `std::sort` 不保證穩定、`std::stable_sort`（含成績單程式）、`list.sort()`、用原始索引讓排序穩定 | 補充 |
| 雜湊 `hash_negative` | 標頭版 `(key % size + size) % size` 的理由，附程式 | 正文 |
| 同上 | 為什麼不寫成 `(key + size) % size` | 補充 |
| 氣泡 `bubble_invariant` | 第一輪最大值必到最右的迴圈不變量 | 補充 |
| 插入 `insertion_count` | 平均比較次數的精確式 $\frac{n(n-1)}{4} + n - H_n$ | 補充（擴充既有區塊） |
| 希爾 `shell_cond` | `curPos >= gap` 的意義；最後一定要用增量 1 | 正文 |
| 希爾 `hibbard_note` | $2^k-1$ 互質的想法、起始增量 $k = \lfloor\log_2 n\rfloor$、列出增量的程式、和動畫寫法的差別 | 補充 |
| 合併 `merge_slice` | 迭代器範圍左閉右開，不需要 `mid + 1` | 正文 |
| 合併 `non_comparison` | 計數、基數、桶子排序；和雜湊（直接定址表）的關係 | 補充 |
| 快速 `quick_count` | $O(n\log n)$ 數的是比較，交換不會比比較多 | 正文 |
| 快速 `std_sort_note` | introsort 的組成、隨機存取迭代器、`list.sort()` | 補充 |
| `depends`（legacy） | 鏈結串列合併排序：bottom-up $O(1)$、`std::list::sort`、快取 | 補充（既有區塊） |
| 收合比較表的 info-box | 改成一句定義加連結 | 補充 |
| 重點回顧 | 刪除 FAQ「哪些排序是穩定的？」，改加一條回顧 | 正文 |
| 插入、合併的說明 | 連到 `#stable` | 正文 |

新增的程式在 `search_programs.py`：`stable_demo`、`hash_neg`、`hibbard_gaps`、`stable_stl`；新 quiz 是 `search_quizzes.SITE_QUIZ['stable']`。表格的 CSS（`.stable-table`）放在 `search_depth.STYLE`。

## 重新計算

- 帶標籤的輸入 `1a 2a 2b 1b`：先用 Python 照課程迴圈窮舉長度 4–6、key 1–3 的輸入，這是能讓選擇、希爾、快速三種都不穩定的最短例子，之後 C++ 的輸出與模擬一致。
  - 氣泡、插入、合併：`1a 1b 2a 2b`
  - 選擇：`1b 1a 2b 2a`
  - 希爾、快速：`1a 1b 2b 2a`
- 把合併的 `<=` 改成 `<`、插入或氣泡的 `>` 改成 `>=`：三種都得到 `1b 1a 2b 2a`。
- quiz：`selectionSort` 排 `{3a, 1, 3b}` 得到 `1 3b 3a`（模擬確認）。
- 插入排序的平均比較次數：$n = 2$ 到 7 的全排列窮舉，和 $\frac{n(n-1)}{4} + n - H_n$ 逐一相等（例如 $n = 4$ 是 $\frac{59}{12}$）。
- 基數排序三輪的中間結果、Hibbard 起始增量、負數取餘數的輸出，都由程式產生。

## 結果

| 項目 | 結果 |
|---|---|
| 冪等 | pipeline 連跑兩次，sha256 相同（`final-page.sha`） |
| C++（`ch7/check_content.py`） | 30 個 run 區塊全部通過（新增 4 個），輸出與 `data-expected`、可見輸出逐字相同；2 個填空練習確實無法編譯；0 錯誤 |
| 瀏覽器（`ch7/check_browser.py`，1440 與 390） | 動畫面板、雜湊四種策略、探查週期工具正常；quiz 24 題；details 58；無破圖、無 page error、無水平溢出 |
| MathJax（`check_mathjax.py`） | 第 7–9 章 0 個 merror，0 個殘留 `$…$` |
| `tools/check_links_cpp.py` | 0 錯誤 / 0 警告 |
| 可見字數（`density-after.json`） | 收合區外 27,673 → 30,000（預算 ≤ 30k） |
| 版面 | `stable-1440.png`、`stable-390.png`、`stable-table-390.png`；390 寬時前兩欄不換行 |
| 390 寬、展開全部 details | 和 HEAD 比對，沒有新增超出版面的元素 |
| speak-human-tw | 無半形標點、破折號、中國用語或套話；修正一句邏輯不通的「所以」（桶子排序） |

## 既有問題（未處理）

- 390 寬時，雜湊段落的行內公式 `rehash(pos)=(pos+skip)modsize` 在 MathJax 排版後超出版面，HEAD 就有。`check_browser.py` 在 MathJax 排完前量寬度，所以沒有抓到。
- 新 quiz 插在章末題庫之前，章末 11 題的洗牌順序（以容器序號當種子）因此改變。
- 代表圖 `island/figs/searching_sorting.webp` 是雜湊表元件，這次沒有改到，沒有重新產生。

## 課程網站

`~/nsysu-math208/_lectures/12_week12.md`：2026-11-23，Searching and Sorting。參考 2025 年第二週，沒有投影片連結與錄影。runestone 對 curl 一律回 403（11/16 已在用的連結也一樣）；`Sort/toctree` 存在，由 `pearcej/cppds` 原始碼目錄確認。
