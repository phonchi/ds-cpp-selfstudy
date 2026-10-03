# 第三、四章程式字體檢查

以 `09bcc0b` 為基準，僅處理第三、四章的程式識別字字體及對應產生來源。

## 修正

- 正文、標題、收合區、表格與題目：函式名、類別／型別、成員與已引入的程式變數使用 `<code>`，沿用網站的 JetBrains Mono／monospace 樣式。
- 完整呼叫與型別盡量保持一組，例如 `std::list::size()`、`vector<vector<int>>`、`prev->setNext(cur->getNext())`、`a[1][2]`。
- Quiz 回饋、字卡與狀態文字在更新時使用相同的識別字規則。只處理文字節點，不重寫元素屬性或執行邏輯。
- 補上斜線右側的識別字；多維陣列格子的 `a[i][j]` 直接使用等寬字體。
- 保留自然術語與座標語境，例如 C-style string、double free、Linear Linked Structures、Linear list、節點（Node）、(row,column)。LaTeX、程式區塊、既有 code、SVG 與講義圖片不套用文字替換。

## 驗證

- 獨立 subagent 盤點與最後複核完成，所指出的斜線漏項、自然術語誤包、局部變數漏項均已修正。
- C++ 區塊與預期輸出逐字相同，所有連結目標不變；兩章沒有巢狀 code，也沒有待處理的識別字候選。
- 靜態 `<code>` 數量：第三章 253、第四章 422；這是整頁現況，不是新增數量。
- 20 項 C++ 範例檢查通過；生成器重跑無差異，ID、錨點、JavaScript 與連結檢查通過。
- Chromium computed font 確認函式／型別及動態字卡使用 monospace。48 個題目選項均點選，字卡各洗牌 3 次，沒有巢狀 code 或遺漏的一般字體識別字。
- 1440px／390px 無頁面溢出；MathJax 回歸包含數學式、12 格映射、快速重設、串列比較、字卡與回饋，無 page error 或 MathJax error。
- 已檢視手機版成本表、收合標題及 STL 說明截圖。

## 重跑

```bash
python3 docs/verification/20261003-code-typeface/check_static.py
DSCPP_VERIFY_OUT=docs/verification/20261003-code-typeface \
  python3 docs/verification/20261003-ch3-ch4/check_content.py
python3 docs/verification/20261003-code-typeface/check_browser.py
DSCPP_VERIFY_OUT=docs/verification/20261003-code-typeface \
  python3 docs/verification/20261003-math-completeness/check_math_browser.py
python3 tools/check_links_cpp.py
```

瀏覽器測試只允許既有 MathJax CDN，其餘外部請求封鎖；computed font 檢查涵蓋 monospace 宣告與本機 fallback，沒有測試 Google Fonts 的即時載入。截圖與機器可讀結果保存在本目錄，不加入學生頁面。
