# 先備頁原版恢復與例子替換

## 本版範圍

本版從 `b97fe81` 重新讀回 P1–P9 的 HTML、題庫與字卡，共 27 檔，再逐段修改。
先前 `05f490e`、`907190b` 與後續重建的 trace、快照及驗收數字，不再描述本版。
正課九章與本輪開始的 `a9425db` 一致；先前已發布的正課改動沒有被回退。

原版重要 C++ 觀念、比較表、背景 SVG 與各頁原生互動保留。課程使用次數與課本專屬例子
改成可獨立理解的情境；沒有改成開放作答或二選一，也沒有用通用 trace 取代原版流程圖。

## 內容與先備銜接

| 頁 | 保留的重要內容 | 本輪例子與必要調整 |
|---|---|---|
| P1 | 編譯四階段、骨架、型別、I/O、printf、轉型與診斷 | 自包含 greeting.hpp、骰子範圍；校正平台大小、未初始化、溢位與編譯診斷 |
| P2 | 短路、分支、各種迴圈、chrono、巢狀計數與成本 | 除數保護、剩餘量減半、獨立迴圈計時；原方形與三角形流程圖保留 |
| P3 | 函式宣告與定義、傳值／參考／指標、回傳生命週期、多載與遞迴 | 開場先拆 deliveryFee 的回傳型別、名稱、參數與呼叫；類別複製／const getter 的完整例子放 P8 |
| P4 | 位址、解參考、nullptr、指標成員、陣列、退化、動態配置及所有權 | Device/Settings 可選具名關聯、設定指標檢查與覆寫 owner 的洩漏，不沿用 Node 串列案例 |
| P5 | vector/string 操作、初始化比較、容量與攤還、迭代器失效、二維資料及標準容器 | 座位預訂、book 子字串、獨立 chrono 比較；原課程統計表改成六列用途表 |
| P6 | map/set、查詢副作用、迭代器、有序／無序、比較與複雜度、計數去重分組 | 部門聯絡名單；不需紅黑樹或圖的表示法；保留排序等價、查詢成本與容器選擇 |
| P7 | 串流、工作目錄、檔案模式、RAII、throw/catch、at/[] 與錯誤邊界 | 自建 notes.txt、用品記錄與負數數量驗證；自訂例外完整類別放 P9 |
| P8 | 類別、成員、存取控制、this、建構／複製、const、串流／friend、組合、標頭防護 | 一般讀數、Timer 與記錄類別；承接 P3 移入的類別細節 |
| P9 | 繼承、virtual、純虛擬、模板、operator、比較／hash、priority_queue、資源複製 | Package、Notification、GridPosition/Point、Task、Inbox、草稿錯誤；不靠樹或圖演算法導入 |

原版各頁比較表數量依序為 17、10、7、7、14、11、4、4、8；本版同為 82 張。
SVG 共 14 張，包含每頁自己的背景圖示；幾何屬性直接與原 commit 比對。文字標籤可因情境替換而調整。
頁內 29 題、末尾題庫 55 題，共 84 道四選一；175 張字卡均使用中文加英文／識別字。

手機版保留頁首完整目錄，隱藏會遮住文字的側邊導覽。寬圖維持原圖形與可讀字級，改在區塊內
水平捲動；表格與互動欄位也在自身容器內處理寬度，沒有用隱藏整頁溢出來掩蓋問題。

## 獨立讀者找到並修正的問題

作者以外的代理交叉審讀原稿與候選稿，確定問題由對應作者修正，再檢查新的版本。包括：

- 回傳失效位址、未初始化與越界讀取不能列固定數值或終止訊號。P7 的 at 範例不再先執行 UB。
- 查詢計時必須使用查詢結果；目前輸出命中數。時間、亂數、桶數、位址與容量均區分示例與保證。
- string 不是 vector<char>；參考是否需要儲存、容器增長倍率與診斷文字都不能硬說成固定實作。
- P9 的 hash 先給完整 Point 定義；比較側欄不再展示課本排序函式或宣稱是 std::sort 固定內部流程。
- P1/P2 與 P4/P8 的例子替換不止改類別名稱：一併校正說明、題庫、字卡與 JavaScript 的畫面標籤。
- 原版驗證工具未涵蓋的手機水平溢出，經完整操作及截圖檢查後修正。

## 可重跑驗證

```sh
python tools/check_prereq_fidelity.py
python tools/check_prereq.py
python tools/check_prereq_runtime.py --report /tmp/prereq-runtime-report.json
python -m unittest discover -s tests -v
python tools/check_links_cpp.py
python tools/check_contrast.py
python tools/check_prereq_browser.py --screenshots /tmp/prereq-final-shots
```

`check_prereq_fidelity.py` 直接讀取原 commit 的章節順序、比較表與 SVG；必要概念由 contract 記錄。
它不能自動判斷每段文字的教學品質，因此仍需上述逐頁閱讀。
`check_prereq.py` 同時檢查原版 `.pseudo-code` DIV 與具 data-cpp 的新增範例。
`check_prereq_runtime.py` 在獨立暫存目錄使用 C++17 與 UBSan 實跑原版完整程式；
四個明確的危險反例不執行，預期編譯錯誤、預期連結失敗及未捕捉例外分開計數。
固定輸出做正規化比對；平台相依範例檢查可確定的事實，不要求重現同一個位址或耗時。

瀏覽器驗證原版按鈕、播放器每個步驟、滑桿兩端、每題所有四個選項、字卡翻面／洗牌，
以及 1440px／390px 的主文樣式與水平溢出。另人工檢視流程圖與背景圖示截圖。

內容補充參考 [C++ Gossip](https://openhome.cc/Gossip/CppGossip/) 的語法主題索引；例子自行撰寫，
不直接搬用課本或網路範例。舊頁面中實作相依的論述另以編譯器驗證和 C++17 語義校正。

最終數字與檢查邊界見[驗證紀錄](prereq-original-validation.md)。多載候選的細節另參考 [C++ draft：implicit conversion sequences](https://eel.is/c++draft/over.best.ics)，正文只保留讀懂本例需要的判斷。
