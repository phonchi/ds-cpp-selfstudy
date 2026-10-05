# DOK 讀取重載說明（2026-10-05）

在現有第三章 DOK 段落加上讀取／寫入小標，說明 const operator() 的 find 查詢、缺值回傳零且不新增項目。const 多載選擇與只讀參考放在緊接兩個方法的「補充」收合區，沿用既有型別字體。

現行完整 SparseMatrix 標頭已包含兩種重載，本次未修改標頭或演算法。範例改成先以 const 參考讀取，再對照非 const 存取；使用本機課程 sparsematrix.hpp、g++ -std=c++17 -Wall -Wextra -pedantic 編譯並核對輸出：

```text
2 0
1
0 2
```

分別證明：已有座標回傳 2、缺少座標回傳 0；const 讀取後仍只有 1 項；非 const 讀取缺少座標會新增零項，變成 2 項。

生成器重跑無差異、ID 唯一、git diff --check 通過。Chromium 已確認收合預設關閉、可以展開，1440px／390px 沒有水平溢出或 JavaScript／MathJax 錯誤。此前 ArrayList kernel 的診斷目錄保持原樣，未納入這次修改。
