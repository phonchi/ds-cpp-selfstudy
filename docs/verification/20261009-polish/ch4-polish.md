# 第 4 章（`linked_lists.html`）潤稿摘要

這次找到並修改了 6 處。

整體來說，第 4 章正文已經相當乾淨，沒有誇張比喻、罐頭結論或中國用語；中文句子裡的半形括號都是數學式，不是標點。這次只處理空泛導引句、重複敘述與一句誇大用詞。動畫訊息（`linked_interactions.js`）、圖說（`linked_figures.py`）、字卡（`data/flashcards_zh/ch4.json`）與 gen 區外的使用方式框、h2 檢查後不需要修改。

修改都在 `tools/enrich/content/linked_depth.py`，再以 `docs/verification/20261008-ch4/pipeline.sh` 重建頁面。

1. **P02 head 與空串列**
   - 原句：「依此類推。要特別注意：**UnorderedList 物件本身並不包含任何節點**，它只保存……」
   - 為什麼要改：「要特別注意」是空泛導引句，後面已經用粗體標出重點，導引句只是重複強調。
   - 改成了什麼：「依此類推。**UnorderedList 物件本身並不包含任何節點**，它只保存……」

2. **P02 size 的說明**
   - 原句：「能把指標拿來和 NULL 比較，是走訪能停下來的關鍵。」
   - 為什麼要改：「……是……的關鍵」是拔高句型，主詞也繞了一圈。
   - 改成了什麼：「迴圈靠 current 和 NULL 的比較，才知道何時停下。」

3. **P03 OrderedList 的資料成員**
   - 原句：「實作 OrderedList 的方法和無序串列相同，空串列一樣以 head 指向 NULL 表示：」
   - 為什麼要改：上兩段已寫過「實作方式與無序串列相同：空串列仍以 head == NULL 表示」，這句幾乎逐字重複。
   - 改成了什麼：「OrderedList 的資料成員與建構子也和無序串列一樣：」（直接引出下面的程式卡）

4. **P03 add 的說明**
   - 原句：「圖中用 previous 與 current 兩個指標標出這個位置；講義的程式則只用一個 current，改成每次先看下一個節點。」
   - 為什麼要改：下一段開頭就是「講義的 add 只用一個 current，並且每次先看下一個節點」，同一件事連說兩次。
   - 改成了什麼：「圖中用 previous 與 current 兩個指標標出這個位置。」（講義寫法留給下一段完整說明）

5. **P05 雙向串列插入**
   - 原句：「下面的動畫照這四行逐步執行：先設定 newNode 自己的 prev、next，再讓 pred、succ 改指 newNode，共四個指標：」
   - 為什麼要改：同一段前半已說明「前兩行只設定新節點自己的 prev 與 next……後兩行才讓 pred 的 next 與 succ 的 prev 改指新節點」，後半整段複述一次。
   - 改成了什麼：「下面的動畫照這四行逐步執行：」

6. **EXERCISE 1 正確選項的回饋**
   - 原句：「兩者都得從 head 一步步走；這是串列與陣列最根本的差別。」
   - 為什麼要改：「最根本」是誇大用詞；陣列與串列的差別不只這一點。答案與選項意思不變。
   - 改成了什麼：「兩者都得從 head 一步步走；這是串列與陣列的主要差別。」

## 驗證

- `pipeline.sh` 連跑兩次，`sha256sum linked_lists.html` 兩次都是 `2a74d0cb850c5b2baca57b81c5912ee1dece1f7675fbf07e90cdc93b250d1f25`；quiz shuffle 未變動。
- `DSCPP_PAGES=linked_lists python3 docs/verification/20261003-ch3-ch4/check_content.py`：23 examples passed; generators stable; IDs, anchors and JS syntax passed。（這支 checker 會把 `content-results.json` 改寫成只剩本頁結果，跑完已用 `git checkout` 還原。）
- 保真比對（改前／改後頁面）：71 個 `pre`／`.pseudo-code`／`[data-expected]`／`script` 區塊完全相同；1043 個 `href`、`id`、`data-*`（不含可調措辭的 quiz 回饋 `data-fb`）完全相同。行內 `<code>` 少了 6 個，全部是第 1、3、5 處刪掉的敘述中的識別字（head、next、NULL、prev、newNode ×2），不是程式碼區塊。
- `python3 tools/check_links_cpp.py`：22 頁，0 錯誤、0 警告。
- 頁面 5 段 inline script 全數通過 `node --check`。
