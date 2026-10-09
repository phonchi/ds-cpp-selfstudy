# 讀者 D 完整發現（第 7–9 章，第二輪，唯讀）

讀者的工作檔在 `/tmp/rv2-ch789/`，裡面有逐格紀錄 `frames.json`、編譯用的程式，以及講義純文字 `nb07.txt`、`nb08.txt`、`nb09.txt`。

## 第 7 章 searching_sorting.html

### 中
1. **#quick 面板**：`#quickCode` 的 7 個 `.line` 都沒有 `data-l`。`genQuickSort` 的 pcLine 用到 2、3、6、8、11、13、14，對應的是 partition 的程式，但面板上沒有列出 partition。結果每一格都不會高亮。
   - 建議：面板改列 partition 程式，並補上與 pcLine 對齊的 `data-l`。
2. **#shell Hibbard 模式**：狀態列寫「sublistCount = aList.size() / 2 = 7」，同時高亮 `int gap = a.size() / 2;`。預設 n=9，9/2=4，這裡的 7 其實是 2³−1。後面「sublistCount /= 2 → 3」的說法也錯。
   - 建議：改成「取不超過 n 的最大 2^k−1」，不要再指向 size()/2 那一行。
3. **#selection 面板**：第 8 行是無條件的 `swap(a[maxPos], a[fill]);`，動畫卻有「maxPos == fill，已在正確位置，無需交換」，而且高亮在 `}`。`sorting.hpp:50` 有 `if (positionOfMax != fillSlot)`。
   - 建議：面板補上這個 if，「無需交換」那一格改為高亮這個 if。
4. **#shell 狀態列變數名**：狀態列用 sublistCount、posStart、gapInsertionSort(aList,0,4)、aList[8]=aList[4]=77，但面板用 gap、start、a。
   - 建議：兩邊用同一組名稱。
5. **#bin-search 狀態列**：寫成「midpoint = (0+9)//2 = 4」。`//` 是 Python 的整數除法；面板與 LIVE 標籤寫的是 `first + (last - first) / 2`。原始碼模板是 `(${first}+${last})//2`。
   - 建議：改成「midpoint = 0 + (9 - 0) / 2 = 4」。
6. **#recap 兩則 FAQ 誤標（補充）**：「二分搜尋一定比循序搜尋好嗎？（補充）」對應講義 cell 56–57；「get 回傳空字串，怎麼知道 key 到底在不在？（補充）」對應講義 cell 125。兩則都是講義內容。

### 低
7. **#hashing 折疊法反轉版**：「34 + 56 + 55 + 64 + 10 = 219」應為 43 + 56 + 55 + 64 + 01。講義 cell 84 原本就寫錯。
8. **#supplement B**：「put() 為什麼有 4 個 if/else 分支」。講義 cell 129 只有 3 條路徑，標頭只有 2 個 if。
   - 建議：改成「put() 會遇到的 4 種情況」。
9. **#hashing 小實驗**：文字寫「把 54, 26, 93, 17, 77, 31, 44, 55, 20 全部插入，44、55、20 都會碰撞」，但 `#hashBatch` 預設只有 6 個數。
10. **#hashing 面板複雜度欄**：線性探查 search ½(1+1/(1−λ))、鏈結法 1+λ/2，這兩個都只是成功搜尋的期望值。
    - 建議：標明「成功搜尋」。
11. **#hashing 鏈結法搜尋空鏈**：比較次數顯示 1，因為程式寫了 `opCount = Math.max(opCount, 1)`。空鏈應顯示 0。
12. **#merge 面板**：兩行「複製剩餘」的 while 沒有 `data-l`，也沒有對應的動畫格；「寫入 a[0] = 26」之後直接跳到「[0..1] 合併完成」。
13. **#reference 排序比較表**：快速排序的空間寫「O(log n)」。
    - 建議：改成「O(log n) 期望，最差 O(n)」。
14. （不改）字卡徽章。

## 第 8 章 graphs.html

### 中
1. **#scc 互動**：`sccStep2()` 只檢查 `sccCloseT` 有沒有內容。① 只跑到 E 就按 ②、③，畫面會顯示「完成：1 棵樹＝1 個強連通元件」，SCC1 = {E,B,A}。實際上有 3 個 SCC。
   - 建議：① 播完之前不能按 ②，並提示使用者。
2. **#topsort 互動**：`tsOrder()` 有同樣的問題。DFS 剛出第一個黑點就按 ②，結果只有「開動(f=6)」，卻顯示「完成！保證每條邊…」。
   - 建議：DFS 播完之前不能排序。
3. **#topsort、#scc 的 → 單步**：寫成 `tsPlayer && tsPlayer.step()`，剛載入時按了沒有反應。
   - 建議：還沒開始時，按單步會先建立 ① 的步驟，然後只前進一格。
4. **#knight 起點選單**：選項是 `[0, Math.floor(n/2)]`。7×7 時 (0,3) 是奇色格，7×7 有 24 個奇色格、25 個偶色格，從奇色格出發無解，跑滿 80 萬步才停，訊息卻叫學生改用 Warnsdorff。
5. **#knight 比較回溯次數**：預設 6×6、起點 (0,0)、關掉 Warnsdorff 時，要回溯 183,599 次，約 36.7 萬格，最快也要播 2 小時。6×6 的 (0,3)、(3,3) 和 8×8 全部超過 80 萬步，只有 5×5 實際可以比較（回溯 4,985 次）。
6. **#bfs Google Maps 框**：「看完再回頭讀 PART 08：A* 在已走成本上…」，但 PART 08 是 Dijkstra，整節沒有提到 A*。
   - 建議：改成「回頭對照 PART 08 的 Dijkstra；A* 是在它的優先順序上再加上到終點的估計」。
7. **#word-ladder 複雜度框**：「建圖（bucket） $O(n\cdot L)$」不對。同一 bucket 內要兩兩連邊，成本是 $\sum_b|b|^2$，最壞 $\Theta(n^2)$。
   - 建議：分成兩部分寫：放入 bucket $O(nL)$，連邊 $O(\sum_b|b|^2)$。
8. **#dfs 收合區「BFS vs DFS 的程式碼對照」**：「差別只在內層迴圈最後一行」不正確。BFS 在 if 內設定 color、distance、previous；DFS 只設定 previous，著色與計時在 `dfsVisit` 開頭，還多了 discovery/closing 與外層迴圈。
   - 建議：改成「核心差別在排程：BFS 放進佇列，DFS 立刻遞迴」。

### 低
9. **#representation 相鄰串列卡片**：「❌ 查特定邊需走過鄰居清單」與正文的 O(log deg(v))（std::map）不一致。
   - 建議：改成「O(log deg(v))，不是 O(1)」。
10. **#prim 互動**：「略過 stale entry」那幾格（35–37）高亮的是 `pq.top(); pq.pop();`；`if (inTree.count(currentKey)) continue;` 沒有行號。
    - 建議：替這一行加上行號，略過的格子指到它。
11. **#dijkstra 互動**：「標記為 visited」與 visited 欄位都是 lazy dijkstra 沒有的概念。
    - 建議：改成「展開」，欄名改為「已展開」。
12. **#knight 格內數字**：起點顯示 1，成功時統計顯示 25；但正文與 printBoard 是 0–24。程式區也沒有行號。
    - 建議：格內從 0 起算，統計改名「已走格數」，並補上高亮。
13. **#dfs 起點選單**：動畫把選到的起點移到最前面，但 `dfs()` 一律依 key 順序選根。
    - 建議：註明這個差異，或拿掉選單。
14. **#topsort 用語**：「s/f 是 DFS 的 start／closing time」，全章其他地方都用 discovery/closing。
15. **#scc 步驟數**：「照上面四個步驟走一遍」，h3 與下文卻寫「三個步驟」。講義 cell 239–240 是四步。
    - 建議：統一寫四步。
16. **#knight 分析**：頁面公式 $\frac{k^{N+1}-1}{k-1}$，接著寫「約為 $3.8^{25}-1$，也就是 $3.12\times10^{14}$」。照公式算約 $4.2\times10^{14}$，$3.12\times10^{14}$ 其實是 $3.8^{25}$；6×6 與 8×8 的數字也都是 $k^N$。數字來自講義 cell 825。
    - 建議：寫成「約 $k^N$ 量級」，或照公式重算。
17. **#bfs bfsDone 圖說與 alt**：原圖只有 14 個節點，沒有畫 fall，但預期輸出有 fall(3)；sage 畫成灰色。
    - 建議：圖說註明原圖沒有畫出 fall。
18. **#prologue 收合區「動畫的顏色與操作方式（補充）」**：「BFS 與 DFS 都用…」出現時，BFS、DFS 都還沒定義。
    - 建議：改成「後面的 BFS 與 DFS 會用…」。
19. **#bfs 收合區「一次 BFS 得到的兩樣東西（補充）」**：這是講義 cell 90–91 的內容，正文也已講過。**#recap「為什麼 BFS 的路徑和題目開頭的解法不一樣？（補充）」**：與 traverse 輸出下方的說明重複。
    - 建議：拿掉補充標示，或刪掉重複的內容。
20. **#exercises 收合區「看完整的追蹤」**：講義練習 2 沒有附解答，這段追蹤卻沒標補充；同樣不在講義裡的練習 1 程式卻有標補充。頁首也沒有定義（補充）。追蹤內容本身是正確的（G–C 權重 5，總和 23）。
21. **#dijkstra 追蹤段落**：「最後檢查 w 和 z，沒有新的變化，優先佇列也空了」不對，此時佇列還剩 (4,w)、(5,w) 兩筆過期項目。
    - 建議：補上「再略過剩下的過期項目」。
22. **#prim 追蹤段落**：「C 的鄰居中還在佇列裡的只有 F」不對，F 從來沒進過佇列。
    - 建議：改成「還不在樹裡的只有 F」。
23. **footer**：「Chapter 9」改成「第 8 章」。字卡徽章不改。
24. **字卡「路徑（Path）」**：要補上「頂點互不相同」。

## 第 9 章 trees.html

### 中
1. **#bst-delete 的 target 欄**：`genDeleteSteps` 的物件字面值裡，`target:target.key` 會被後面的 shorthand `target` 蓋掉，導致完成格與 Case 3 copy-key 格顯示 `[object Object]`。Case 3 之後兩格又顯示成 successor 的鍵（35、60）。
   - 建議：節點改用 `targetNode` 之類的名稱，target 欄一律顯示原本要刪的鍵。
2. **#bst put／get 的單步**：`if (player) player.step()` 在剛載入時沒有反應，按 put/get 會直接自動播放。
   - 建議：沒有 player 時，先建立操作但不自動播放，參考刪除動畫的 `startDel(false)`。
3. **#heap 單步**：已到最後一格時再按單步，`heapStep` 會在 `idx >= steps.length-1` 時呼叫 `startOp()`，在已更新的 heap 上重做同一個操作，連按會一直插入 7 或一直 delMin。
   - 建議：最後一格就停住。
4. **#avl LR、RL**：狀態列比樹與階段欄早一格；bf 欄填的是「+2 / -2」「判斷」「中繼」「進行中」這類文字，不是數值。
   - 建議：每格文字描述當格畫出的狀態，bf 欄填實際數值。
5. **bankquiz Q4 選項「1.4」的回饋**：寫「由左往右直接計算 10 / 2 - 6 - 3」，但 10/2−6−3 = −4，算不出 1.4。
6. **#bst 說明框**：「這就是下一節要解決的問題」，但下一節是 #bst-delete。退化在 #bst-analysis 分析，到 #avl 才解決。
   - 建議：寫明節名。
7. **#nodes-refs 逐步建樹的狀態列**：寫「a_tree = BinaryTree("a")」「insert_right("c")」，但高亮行是 C++ 的 `aTree`、`insertRight`。位置約在 trees.html 第 3134 行，屬於主 script。
8. **#bst-delete Case 3 順序**：動畫先複製 key 再 splice out，畫面會短暫出現兩個 35。圖說與程式都是先 `successor->spliceOut();` 再複製。
   - 建議：動畫改成先 splice。
9. **四個程式標題**：「講義的書本樹：以 BinaryTree 建立並做前序走訪」「講義的走訪函式：對解析樹做三種走訪與 postordereval」「對照圖：在圖中的 heap 插入 7，以及執行 delMin」「講義例子：buildHeap({9, 6, 5, 2, 3})」，這幾個 main 程式講義裡都沒有。決定見 readerD-ch7-9.md。

### 低
10. **#traversals、#heap、#bst-delete 沒有高亮**：
    - 走訪動畫的 `applyFrame` 沒有呼叫 `hlLine`；
    - heap 面板固定顯示 percUp，做 delMin 或 heapify 時都是 `line:null`；
    - 刪除動畫的 `applyStep` 沒有高亮。

    建議：依步驟高亮，heap 依操作切換程式。
11. **#heap percUp 停止格**：「heap[1] ≥ heap[0]，停止」那一格仍高亮 if 那一行，`break` 沒有 data-l。
12. **#avl「下面的旋轉示範（補充）」**：頁首只定義收合區的（補充），而「選讀」只說 AVL 內部實作，但 §8.16 高度上界也標了選讀。
    - 建議：調整頁首的定義。
13. **TreeNode listing 與 bst.hpp 不符**：listing 列出 `isRoot()`，但 bst.hpp 第 9–46 行沒有這個函式，反而有 `hasBothChildren()`，Case 3 程式也用到它。另外，`_get()` 在 bst.hpp:138 是 public，頁面寫「私有輔助函式」。
    - 建議：listing 補上 `hasBothChildren()`，「私有」改成「輔助」。
14. **#avl 末段**：「往上更新平衡因子最多 $\log_2 n$ 次，每層一次」應該是「最多樹高 $h = O(\log n)$ 次」，因為 AVL 樹高可達約 1.44 log₂n。
15. **#recap 第 5 點**：同一句裡 p 與 i 混用，統一用 i。
16. **#heap 缺講義 cell 151 的程式**：`buildHeap({10,4,9,8,12,15,3,5,14,18})` 之後示範 findMin()、size() 與 delMin 迴圈。請補上程式與實際輸出。
17. （不改）字卡徽章。
