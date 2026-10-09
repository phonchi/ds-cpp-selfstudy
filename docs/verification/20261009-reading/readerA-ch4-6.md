# 讀者 A：第 4–6 章審閱發現（2026-10-09，唯讀）

主控已核實第 1 項（makeChange2 的表裡有洞的原因）。其餘依讀者證據處理，修正後由第二位獨立讀者複讀。

| # | 頁 | 位置 | 類別／嚴重度 | 摘要 | 決定 |
|---|---|---|---|---|---|
| 1 | recursion | recap FAQ「makeChange2 的表裡會有洞」 | 正確性／高 | 2、3、4 分有遞迴進入；沒寫入是因為 minCoins 初值 = change，candidate < minCoins 不成立 | 改寫原因 |
| 2 | recursion | #sierpinski「畫的順序」 | 不一致／中 | 「下方中間」應為上方角落 | 改 |
| 3 | recursion | #viz canvas | 不一致／中 | canvas 螺旋 210（43 次）、樹 78/−13 與講義 100（21 次）、75/−15 不同 | 對齊講義參數（必要時縮放繪圖），訊息次數隨之更新 |
| 4 | recursion | #hanoi 動畫 | 不一致／中 | 動畫 A→C 借 B，講義 moveTower(3,"A","B","C") 是 A→B 借 C | 動畫改 A→B 借 C |
| 5 | recursion | reverse 參考解答 | 標示／低 | 講義無解答 | 標「參考解答（補充）」 |
| 6 | recursion | cards | 用語／低 | 正文用 stack frame／base case | 卡片正面用原文術語，中文放括號 |
| 7 | linear_structures | 四個動畫 frames 的 line 值 | 不一致／中 | parFrames、baseFrames、i2pFrames、pevalFrames 高亮錯行 | 依面板 data-l 修正 |
| 8 | linear_structures、recursion | 「講義補充」節徽章與頁首說明 | 標示／中 | 講義內容被標「補充」 | 改為「課堂略過・自學」，「（補充）」只留給講義沒有的延伸 |
| 9 | linear_structures | 迴文動畫訊息 | 用語／中 | addRear/removeFront 與 std::deque 面板不符 | 改 push_back/pop_front/pop_back |
| 10 | linear_structures | deque 圖說 | 不一致／低 | 圖 front 在右，表 front 在左 | 圖說補方向說明 |
| 11 | linear_structures | stack 互動區提示 | 不一致／低 | 預設內容與表不符、無 empty/size | 改提示文字或改成空 stack 起始 |
| 12 | linear_structures | prologue「各節都會列出兩者的對照」 | 不一致／低 | 只有三節有 | 改寫 |
| 13 | linked_lists | REF 與 EX1 第 k 項成本 | 不一致／低 | O(k+1) vs O(k) | 統一並註明 k 從 0 起算 |
| 14 | linked_lists | 雙向插入動畫例子 | 不一致／低 | 動畫插 26 於 54、93 之間；正文與圖是 77 於 26、93 | 動畫預設案例改成與圖一致 |
| 15 | linked_lists | #stl 徽章 §4.7 | 不一致／低 | 4.7 是 Ordered List ADT | 改標「講義 04 延伸」或移除 § |
