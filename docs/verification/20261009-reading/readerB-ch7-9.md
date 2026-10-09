# 讀者 B：第 7–9 章審閱發現（2026-10-09，唯讀）

主控已核實第 7 章第 2 項：n=10 時最多比較 4 次，⌊log₂n⌋+1 正確，⌈log₂n⌉+1 錯。無高嚴重度項目；49 個 run 程式與所有 quiz 正解已驗證。

## 第 7 章 searching_sorting
| # | 位置 | 摘要 | 決定 |
|---|---|---|---|
| 1 | seq-search 有序版 | 兩張相同的比較次數表 | 刪一張，用語統一 |
| 2 | bin-search 開頭 | 最多比較 ⌈log₂n⌉+1 錯 | 改 ⌊log₂n⌋+1，與 10⁶→20 次一致 |
| 3 | depends 表與 info-box | quicksort／shell「✗ 不行」過度主張 | 改「△ 本章的雙指標 partition 做不到，需改用單向掃描」；shell 改「可做但很慢」 |
| 4 | selection 開頭 | 「和 cppds、HW4 一樣」 | 改成直述版本內容 |
| 5 | shell 面板標題 | 「(對齊講義 §7.6)」 | 刪掉 |
| 6 | shell 統計欄 | 「交換」應為「位移」 | 改 |
| 7 | 字串雜湊 info-box | 權重 i 應為 i+1 | 改 |
| 8 | run 程式註解 | 「(md listing above)」 | 改成具體指出上方的標頭函式（ch8 同類 4 處一起改） |
| 9 | TOC | 順序與 DOM 不符 | 依 DOM 排序 |
| 10 | reference 表 | Shell 平均 O(n^{3/2}) | 註明依 gap 序列而定 |

## 第 8 章 graphs
| # | 位置 | 摘要 | 決定 |
|---|---|---|---|
| 1 | bfs3.png | 圖中佇列應為 poll、fail（講義圖錯） | 圖說與 alt 註明圖中佇列有誤及正確內容；講義圖不改 |
| 2 | scc 逐步圖 | 「轉置圖 G 的 T」 | 改 Gᵀ |
| 3 | prologue 關鍵概念 | Cycle 定義與 path 定義矛盾 | 改 |
| 4 | topsort、dfs 開頭 | 重複定義 | 刪重複段 |
| 5 | ktdfse.png | C 應為白色（講義圖錯） | 已有圖說；alt 也改成說明 |
| 6 | Warnsdorff 8×8 說明 | 「四角數字都很小」與輸出不符 | 改寫 |
| 7 | prim 廣播圖追蹤 | 「D 和 E 可以更新」漏 C | 改 C、D、E |
| 8 | cards | 氾濫、樹定義與內文不一致 | 對齊內文 |

## 第 9 章 trees
| # | 位置 | 摘要 | 決定 |
|---|---|---|---|
| 1 | summary | 「過去兩章」 | 改「第 7 章與本章」 |
| 2 | buildExp 圖說 | 「前三個 token」 | 改「讀入 ( 與 3 之後，讀 + 之前」 |
| 3 | heapify info-box | perc_down | 改 percDown |
| 4 | heap | O(n) 推導重複；操作表缺 print() | 合併；補 print() |
| 5 | bst-analysis 表 | del | 改 remove |
| 6 | cards | Bottom-up buildHeap 格式 | 改「由下往上建堆（Bottom-up buildHeap）」 |
