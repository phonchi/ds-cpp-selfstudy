# 第三、四章內容與互動驗收（2026-10-03）

## 範圍與來源

第三章 `arrays.html`、第四章 `linked_lists.html` 及兩章生成器／補充來源；第三章字卡同步修正。README 僅更新生成器可重跑的維護說明。講義、課程標頭與其他章節未修改，原始實作階段未發布；後續使用者已授權潤稿並推送，發布結果以 Git 提交與 Pages 部署狀態為準。

對照 `/home/phonchi/ds_cpp/Slides/03_Arrays.ipynb`、`04_Linear_Linked_Structure.ipynb` 與同目錄下 `pythonds3/cppds/{arraylist,sparsematrix,linked_list}.hpp`。`source-manifest.json` 保存本次來源與成果 SHA-256、Git HEAD。正文循講義，延伸使用預設收合區。

## 實作摘要

- 第三章：陣列家族比較、ArrayList 擴容與檢查、int& 讀寫例、pointer/reference_wrapper、C string、vector 矩陣、row/column-major 公式與並列動畫、COO/DOK/單一串列及加減乘成本。
- 第四章：節點接線與邊界、OrderedList、雙向與環狀、list／forward_list 完整例子、複雜度與迭代器有效性。STL 順序依講義置於其他鏈結變形之前。
- 保留既有錨點與互動。第三章新管理的 sections 與動畫由 `tools/enrich/content/arrays_*` 產生；第四章新增內容位於 `linked_depth.py`。原始產生腳本已改為可重跑。
- 修正既有錯誤：SparseMatrix 方法不存在的舊說法、零值項目與非 const 存取副作用、map 對數成本、ArrayList 舊介面、過度泛化的快取與記憶體敘述。

## 確認無誤

- **17 個 C++ 範例檢查**：16 個完整範例編譯、執行並逐字核對輸出；1 個按值回傳後指定的反例確實編譯失敗。使用 `g++ -std=c++17 -Wall -Wextra -pedantic`，標頭取自上述來源。
- **數學／資料結構**：8 組稀疏運算用直接 dense 迴圈作獨立答案，涵蓋零矩陣、相消、沒有匹配項、多項累加與非方形乘法；30 種矩陣形狀核對 row/column-major 位置；ArrayList 零容量擴容、插入／刪除、非法索引通過。
- **生成與靜態結構**：兩章再次生成 bytes 相同；沒有重複 ID、缺失頁內錨點；所有 inline JavaScript 通過 Node 語法檢查。全站連結檢查 0 錯誤／0 警告。
- **Chromium**：1440px／390px 沒有頁面水平溢出；第三章 10 個與第四章 6 個收合區可操作；題目與字卡可用，無 JavaScript page error。
- **動畫**：12 格的兩種 offset 全部核對；column-major 實際排列為 `1,5,9,2,6,10,3,7,11,4,8,12`。播放、暫停、單步、重設、進度與重播通過；resize 後選取格維持可見。既有播放器共逐步檢查第三章 36、第四章 18 個 frame。
- **視覺檢查**：實際檢視桌面／手機矩陣動畫、手機 STL 程式碼及收合說明截圖；桌面兩條完整記憶體帶並排，手機上下排列、內部可橫捲，選取位置置中。

## 驗收過程與限制

- 獨立核對發現合併偽碼須先確認 A 尚未結束才比較座標，已修正；零序列不再讀取不存在項目。
- 初次 Chromium 在 sandbox 被 socket 權限阻擋；一次等待已中止，後以已核准的外部 sandbox 本機執行完成。沒有外部資料傳送。
- 首輪 resize 驗收發現選取格未重新置中，加入 ResizeObserver 後再次通過。
- 瀏覽器測試封鎖外部請求，只驗收本機 HTML、CSS、JS；未驗證 Google Fonts、MathJax CDN 的即時可用性或公開部署。新公式直接以文字／code 呈現，不依賴 MathJax。
- 全部結果與完整輸出分別在 `content-results.json`、`browser-results.json`、`run.log`；截圖在同目錄。頁面沒有加入這些內部驗證入口。

## 重跑

```bash
python3 tools/enrich/enrich_arrays.py
python3 tools/enrich/enrich_linked.py
python3 docs/verification/20261003-ch3-ch4/check_content.py
g++ -std=c++17 -Wall -Wextra -pedantic -I/home/phonchi/ds_cpp/Slides \
  docs/verification/20261003-ch3-ch4/check_math.cpp -o /tmp/ch3-check-math
/tmp/ch3-check-math
python3 tools/check_links_cpp.py
python3 docs/verification/20261003-ch3-ch4/check_browser.py
```

Browser 驗收使用目前已安裝的 Chromium 路徑，受限 sandbox 下須允許本機瀏覽器啟動。C++ 檢查產生的暫存程式會自動刪除；正式證據保留在此目錄。

## 潤稿

使用 speak-human-tw 完成 57 處文案修改，逐項摘要見 `copy-edit-summary.md`，完整前後對照見 `copy-edit-report.json`。保真比對與結果見 `copy-protection.json`。
