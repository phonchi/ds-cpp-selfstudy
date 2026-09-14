# 講義連結驗證（2026-09-14）

- 九章改為 GitHub Pages HTML 線上閱讀、PDF 閱讀及 PDF 下載。
- 18 個遠端 HTML／PDF URL 均回傳 HTTP 200，Content-Type 分別為 text/html 與 application/pdf。
- Chromium 以正式站點 origin 載入本機修改頁面，1440px／390px 九章按鈕均未超出畫面；截圖已目視確認。
- 實際點擊下載取得 01_Introduction.pdf（3,410,367 bytes），檔案開頭為 %PDF-。
- check.py 為可重跑的瀏覽器檢查，完整輸出見 run.log。
- 下載屬性依賴正式兩站同為 https://phonchi.github.io；若未來改用不同網域，需調整下載方式。
- 課程 repo 的 _lectures/02_week2.md 改為 Microsoft Learn 繁體中文 try／throw／catch 教學；本文不判定原網站是否感染病毒。
