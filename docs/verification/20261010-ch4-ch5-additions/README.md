# 第 4、5 章依使用者要求補充內容（2026-10-10）

內部紀錄，不連到學生頁面。未 commit。

## 改了什麼

來源檔：`tools/enrich/content/linked_depth.py`、`linked_programs.py`、`linear_depth.py`（`linked_figures.py`、`linear_programs.py` 不必改）。
頁面由 `docs/verification/20261008-ch4/pipeline.sh`、`20261008-ch5/pipeline.sh` 重建。

### 第 4 章 `linked_lists.html`

| 項目 | 位置 | 形式 |
|---|---|---|
| 4 鏈結串列的優勢 | prologue「為什麼需要另一種表示法」，原第二段後改成三點清單；`li` 有 id `linked-scattered-memory`、`linked-known-position`、`linked-bulk-update` | 可見正文、無標示 |
| 2 `template <typename T>` | node 一節，Node 類別程式卡（第一次出現）之後；id `linked-template-note`；連到 `p9_oop_advanced.html#tmpl` | 收合（補充） |
| 3 header node 參考做法 | unordered 一節 remove 特殊情況段落（講義 cell 79「留作練習」）與 `figure('remove')` 之後；id `linked-header-node`。練習區「加入 header 節點」補一句連到這裡 | 收合（補充），含完整程式與輸出 |
| 1 STL 比較表 | STL 一節，vector／forward_list／list 表之後，新 h3「課程的串列與 STL 串列」；表後一段說明 forward_list 也有 `sort()`、可用 `insert_after()` 自己維持排序 | 表格可見 |
| 1 用 STL 實作 OrderedList | 上述段落之後；id `linked-stl-ordered` | 收合（補充），含完整程式與輸出 |
| 5 環狀串列的優勢 | variants「環狀串列的用途：輪流與 append」；cell 136 譯為「很適合用來有效率地分配與管理資源，也適合 append() 這類操作」，後接三點清單；原「輪流使用資源」段改為 CPU 輪流排程 | 可見正文 |
| 6 雙向串列的優勢 | 「雙向串列與哨兵節點」第一段：prev 讓已知節點 O(1) 刪除，連回 `#linked-known-position` | 可見正文 |

比較表依 `pythonds3/cppds/linked_list.hpp` 核對：UnorderedList 與 OrderedList 都只有 `isEmpty/add/size/search/remove`（加上複製／移動、`getHead`、`operator<<`），沒有 append／insert，使用者原表成立。
用語調整：「你的」→「課程的」；Singly／Doubly → 單向／雙向；「未實作」→「未提供」（與 prologue ADT 表一致）；OrderedList 頭部插入寫「由 add() 依大小決定位置」。

### 第 5 章 `linear_structures.html`

prologue 表格之後、「本章程式使用的兩套介面」之前，新 h3「已經有陣列和鏈結串列，為什麼還要 stack、queue？」，三點：意圖清楚（連到 `#parens`、提 BFS）、防止誤用、抽象化（`std::stack` 預設 `std::deque`，可指定 `vector`／`list`）。可見正文、無標示（使用者指定為主線內容；講義沒有這段）。

## 新增程式與實際輸出（g++ -std=c++17 -Wall -Wextra -pedantic，0 警告）

`HEADER_LIST_MAIN`（HeaderList）：

```
true
54 26 93 17 77 31 
26 93 77 
3
true
```

另以 `-fsanitize=address` 執行，無錯誤、無洩漏。

`STL_ORDERED_MAIN`（forward_list 版 OrderedList）：

```
17 26 31 54 77 93 
true
false
26 31 54 77 93 
```

兩段輸出都放在收合區內的程式卡下方（`expected-out` 與程式在同一張卡）。

## 驗證結果

- pipeline 連跑兩次 sha256 相同：
  - `linked_lists.html` `94f7910cd35287f0562ffb628ec106b078ec1aae38dbc59dcf955365794bb888`
  - `linear_structures.html` `ea6d12c33bf6be19503dedabbc815c1baa4be0bd4f4144f935032a820a80e0dc`
- `DSCPP_PAGES=linked_lists python3 docs/verification/20261003-ch3-ch4/check_content.py`：25 examples passed，IDs、錨點、JS 語法通過。
- `docs/verification/20261008-ch4/check_content.py`：run 24/24（原 22，兩支新程式皆 `matches_data_expected` 與 `matches_visible`），compile_error 1，errors 0。
- `docs/verification/20261008-ch5/check_content.py`：run 17/17，errors 0；結果 JSON 無變動。
- `20261008-ch4/content-results.json` 因新增兩筆範例（22→24）而有實質變動，保留在原位置，副本為本目錄 `ch4-content-results.json`。
- `20261003-ch3-ch4/content-results.json` 原本是 10-03 的歷史快照（17 筆，檢查範圍不同），這次只跑 linked_lists 會覆蓋成不同範圍，所以已還原；本次結果存為本目錄 `ch4-content-results-20261003-checker.json`。
- `python3 tools/check_links_cpp.py`：22 頁 0 錯誤 0 警告（它只檢查跨頁檔案存在；`p9_oop_advanced.html` 的 `id="tmpl"` 另以 grep 確認存在）。
- inline script：check_content 對每個 inline script 執行 `node --check`，全數通過。
- check_browser（1440／390）：兩章 overflow false、page_errors 空。原目錄的截圖與 browser-results.json 已還原，新結果在本目錄（`ch4-*`、`ch5-*`、`linked_lists-*`、`linear_structures-*`）。
- 另截新增區塊（展開 details）：`ch4-prologue-advantages`、`ch4-template-note`、`ch4-header-node`、`ch4-stl-table`、`ch4-stl-ordered`、`ch5-motivation`，各 1440／390；無 page error、無水平溢出。比較表在 390 寬原本第一欄被擠成單字直排，已加 `min-width:680px`，由外層 `overflow-x:auto` 橫向捲動。

## 潤稿摘要（speak-human-tw，跳過確認、事後摘要，教學文件中等力度）

這次找到並修改了 2 處：

1. 原句「講義的結論是：環狀串列很適合……操作。它的優勢有三點：」／「有三點」是公式化湊數導引，「結論是」語氣生硬／改成「講義指出，環狀串列很適合……操作，理由如下：」。
2. 原句「這才真正做到本章開頭所說、鏈結串列相對於陣列的優勢」／「這才」指涉不清、頓號斷句不順／改成「有了 prev，才真正做到本章開頭所說鏈結串列相對於陣列的優勢」。

其餘新增文字已檢查全形標點、台灣用語、破折號（無）、「不是 A 而是 B」（全部新增文字僅一次）；三點清單的粗體引言保留，因為使用者指定三點結構。

另外兩處是產生器自動加 `<code>` 造成的修正（非潤稿）：`free list` 的 list 會被包成 code，改寫成「空閒串列（free-list）」；模板說明的 `class template` 英文詞會被拆成兩個 code，改為只寫「類別模板」，`template <typename T>` 改以明確 `<code>` 包住。
