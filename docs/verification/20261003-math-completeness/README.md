# 第三、四章數學式完整性檢查

## 修改範圍

以 `395a2be` 為基準，補齊正文、表格、圖說、題目回饋、字卡與動畫的 LaTeX。包含 `5×4+3＝23`、位址與跨距、矩陣維度與運算、次方、平均比較次數及大小比較。A／B 矩陣改用 bmatrix，COO 的三條陣列改用 aligned。最長的題目位址推導分行顯示，手機不必左右追整條等式。

保留真正的 C++ 程式、輸出及操作語法。講義圖片原檔不改。數學性的 inline code（例如索引範圍）改為公式；程式中的指標、賦值與函式呼叫維持原樣。

超出講義範圍的收合標題統一加「（補充）」：第三章 13 區、第四章 10 區。DOK 的講義完整類別維持原標題；其語法與限制另放標示「（補充）」的收合區。

## 動態內容

`chapter_math.js` 使用序列化更新，先清除目標區塊的舊 MathJax 項目，再更新與排版。同一元素快速更新時採最新內容，避免上一格的公式覆蓋重設後狀態。題目回饋、字卡洗牌、位址格子、矩陣映射、稀疏統計與串列比較訊息都走此流程。

## 驗證

- 獨立 subagent 先盤點漏式，修正後複核數值、比較方向與矩陣資料，確認無誤。
- `check_static.py`：受保護的 C++ 區塊與預期輸出逐字不變；正文、回饋、字卡掃描無剩餘候選漏式；收合標示一致。
- 20 項 C++ 範例檢查通過；兩章生成器重跑無差異；ID、錨點、JavaScript 語法與連結檢查通過。
- Chromium 實際載入 MathJax：第三、四章初始各 113 個數式，48 個題目選項逐一點選，回饋均有對應排版。
- 驗證矩陣 12 格的兩種 offset、快速切換後重設、完整播放、int／double 位址變換、稀疏統計、串列小於／大於等於／相等／不等比較。
- 每章字卡洗牌 3 次後數學項目數量不增加，沒有殘留舊 MathJax 項目。
- 1440px、390px 無頁面溢出；0 個 MathJax 錯誤、0 個 JavaScript page error。已查看手機截圖中的攤平計算、題目分行推導、矩陣與動畫公式。

## 重跑

```bash
python3 docs/verification/20261003-math-completeness/check_static.py
DSCPP_VERIFY_OUT=docs/verification/20261003-math-completeness \
  python3 docs/verification/20261003-ch3-ch4/check_content.py
python3 docs/verification/20261003-math-completeness/check_math_browser.py
python3 tools/check_links_cpp.py
```

瀏覽器需要允許本機 Chromium 啟動與既有 MathJax CDN；其餘外部請求封鎖。結果及截圖保留在此目錄，不加入學生頁面的入口。
