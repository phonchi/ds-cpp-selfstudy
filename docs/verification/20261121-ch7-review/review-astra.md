**你的質疑成立：氣泡、選擇、插入排序都能自然地用鏈結串列實作，表中的評價混用了「演算法需要什麼能力」與「課程的 vector 程式是否需要改寫」。** 審閱另找到 C++ 溢位保證、空間題目及幾處演算法敘述問題。全程唯讀，未修改任何檔案。

## 1. 發現

### 錯誤

**1．`#depends`：三種排序在 Linked List 上的判斷缺乏一致依據**

位置：[search_legacy.py:759](/home/phonchi/ds-cpp-selfstudy/tools/enrich/content/search_legacy.py:759)，氣泡、選擇、插入三列。

原句：

> 氣泡排序：「△ 慢但可」  
> 選擇排序：「△ 慢但可」  
> 插入排序：必要屬性「隨機存取（位移）」，Linked List「△ 變體可行」

**為什麼不對：**

- 氣泡排序保留目前節點與下一個節點，即可用 \(O(1)\) 完成相鄰比較與交換；每輪循序走訪，仍是 \(\Theta(n^2)\) 時間、\(O(1)\) 額外空間。
- 選擇排序在掃描時記住最大節點及未排序區尾端，便可交換兩者資料；同樣維持 \(\Theta(n^2)\) 時間、\(O(1)\) 額外空間。
- 插入排序可以循序尋找插入位置，再重接節點，**不需要隨機存取**。單向串列可向前找位置；雙向串列也能從目前位置往回找。

鏈結串列可能有較差的快取表現，但這不能直接推出三者必然「慢」。若 △ 只是表示需要改寫 vector 程式，同表標 ✓ 的循序搜尋與合併排序也需要改寫，判準便不一致。

**建議：**三列都可標「✓ 可用節點循序操作實作」；插入排序的必要屬性改成「尋找插入位置並移動元素／重接節點」。另說明不代表它們比鏈結串列合併排序更適合大量資料。

**信心：高。**

---

**2．`#hashing`：取餘數後再加 `size`，仍可能溢位**

位置：「為什麼不寫成 `(key + size) % size`（補充）」；[search_more.py:366](/home/phonchi/ds-cpp-selfstudy/tools/enrich/content/search_more.py:366)。

原句：

> 先取一次餘數，絕對值就小於 `size`，再加 `size` 也不會溢位。

**為什麼不對：**以 32-bit `int` 為例：

```cpp
size = 1500000000;
key  = 1000000000;
```

`key % size + size` 的數學結果是 `2500000000`，超過 `INT_MAX = 2147483647`。後面的 `% size` 無法補救前面已發生的 signed overflow；這是未定義行為。[C++ 標準草案：算術運算的可表示範圍](https://eel.is/c++draft/expr.pre)

課程 `hashtable.hpp` 確實使用這個式子，所以這是**課程程式既有的邊界限制，加上頁面錯誤的安全保證**；`size = 11` 的範例沒有問題。

**建議：**限定本例的小尺寸，或介紹對正 `size` 安全的寫法：

```cpp
int r = key % size;
return r < 0 ? r + size : r;
```

同段「key 小於 `-size` 時……仍是負數」也應改成「仍**可能**為負數」；例如 `key=-22, size=11` 的結果是 0。

**信心：高。**

---

**3．`#depends`：把 Iterator、單向串列、雙向串列混成同一種存取能力**

位置：[search_legacy.py:710](/home/phonchi/ds-cpp-selfstudy/tools/enrich/content/search_legacy.py:710)、[search_legacy.py:784](/home/phonchi/ds-cpp-selfstudy/tools/enrich/content/search_legacy.py:784)。

原句：

> 只能從頭往後一個一個走……代表結構 Linked List、Iterator、Generator、Stream。

以及希爾排序列：

> 鏈結串列每次都得從頭走過去才能「跳 gap 格」。

**為什麼不對：**

- Iterator 是介面分類，不代表只能循序存取。隨機存取迭代器支援常數時間的 `it + k`。[C++ 標準草案：random_access_iterator](https://eel.is/c++draft/iterator.concept.random.access)
- `std::list` 提供雙向迭代器，可以往前、往後走。[C++ 標準草案：list](https://eel.is/c++draft/list.overview)
- 雙向串列可以從目前節點往回走 `gap` 步，成本為 \(O(gap)\)，並非每次都必須回到表頭。

**建議：**區分單向串列、雙向串列及迭代器種類。希爾排序改成「一般鏈結串列缺少 \(O(1)\) 跨 gap 存取，直接移植陣列版通常不利」。快速排序列的「需改寫 partition」也應明確限定**單向串列**。

**信心：高。**

---

**4．`#depends`：迭代版不一定需要顯式 stack**

位置：[search_legacy.py:876](/home/phonchi/ds-cpp-selfstudy/tools/enrich/content/search_legacy.py:876)。

原句：

> 如果改寫成 iterative 版本，會明確使用一個 stack 來模擬遞迴。

**為什麼不對：**bottom-up merge sort 依序合併長度 1、2、4……的片段，可以完全不模擬遞迴，也不使用 stack。頁面同節前面已正確說明 bottom-up 鏈結串列版能達到 \(O(1)\) 額外空間，這裡前後矛盾。

**建議：**

> 直接模擬遞迴時，可以使用顯式 stack；bottom-up merge sort 則可改用迴圈安排合併，不需要 stack。

**信心：高。**

### 誤導

**5．`#bankquiz`：額外空間題不能未加條件就排除快速排序**

位置：章末第 7 題；[ch7.json:44](/home/phonchi/ds-cpp-selfstudy/data/questions_zh/ch7.json:44)。

原句：

> 本章的排序中，哪一個需要 O(n) 的額外暫存空間？

唯一正解是合併排序；快速排序的錯誤回饋是：

> quickSort 在原本的 vector 上交換，只需要遞迴堆疊的空間。

**為什麼不對：**遞迴堆疊也是額外空間。課程 `quickSortHelper` 沒有採用「只遞迴較小分區」的空間最佳化；例如所有元素相等時，每次分割留下長度 \(n-1\) 的子問題，堆疊深度為 \(\Theta(n)\)。頁面的比較表其實已正確列出這個最差空間。

**建議：**題幹改成：

> 不計遞迴堆疊，哪一個需要 \(\Theta(n)\) 的額外元素暫存空間？

快速排序回饋則補上「堆疊平均 \(O(\log n)\)、最差 \(O(n)\)」。

**信心：高。**

---

**6．`#reference`：「幾乎已排序」不代表 short bubble 也適合**

位置：選擇指南；[search_legacy.py:915](/home/phonchi/ds-cpp-selfstudy/tools/enrich/content/search_legacy.py:915)。

原句：

> 資料幾乎已排序｜插入排序 / 氣泡（短路）｜O(n) 最佳

**為什麼不對：**考慮：

\[
[2,3,\ldots,n,1]
\]

這組資料只有 \(n-1\) 個逆序對，插入排序只需線性工作量。但課程由左往右掃的氣泡排序，每輪只能把最後面的 1 往左移一格，仍須 \(n-1\) 輪，共

\[
(n-1)+(n-2)+\cdots+1=\frac{n(n-1)}2
\]

次比較。每輪都有交換，短路條件完全幫不上忙。

**建議：**寫「逆序對少：插入排序」；short bubble 另限定為「已排序，或少數幾輪即可完成的資料」。

**信心：高。**

---

**7．`#quick`：由比較次數推到執行時間，漏了課程預設的輸出成本**

位置：[search_more.py:418](/home/phonchi/ds-cpp-selfstudy/tools/enrich/content/search_more.py:418)。

原句：

> 交換不會比比較多，所以執行時間也是這個量級。

**為什麼不對：**這對不含教學輸出的排序核心成立，但課程預設 `sortingTrace = true`。`quickSortHelper` 每次 partition 後都印出**整個原始 vector**，不是只印目前子區間。即使分割平衡，線性數量的 partition 各輸出 \(n\) 個元素，輸出量仍可達 \(\Theta(n^2)\)。

同樣地，已排序資料的 `insertionSort` 雖然只有 \(n-1\) 次元素比較，預設仍會印 \(n-1\) 次完整 vector。

**建議：**在時間分析前明訂：

> 以下時間複雜度不計教學用輸出；對應到程式時，令 `sortingTrace = false`。

頁面已介紹這個開關，但尚未把它與執行時間結論連起來。

**信心：高。**

### 不精確，但會改變學生理解

**8．`#selection`：「每輪只交換一次」應為「最多一次」**

位置：[search_legacy.py:381](/home/phonchi/ds-cpp-selfstudy/tools/enrich/content/search_legacy.py:381)。

原句：

> 每一輪只交換一次……selection sort 每輪只換一次。

**為什麼不對：**課程程式有：

```cpp
if (positionOfMax != fillSlot)
    swap(aList[positionOfMax], aList[fillSlot]);
```

例如 `[1,2,3]` 全程零次交換。後面的範例說明也明確寫了最大值已在尾端時不交換。

**建議：**統一改成「每輪**最多**交換一次」。

**信心：高。**

---

**9．`#insertion`：停止條件漏了「相等」**

位置：[search_depth.py:303](/home/phonchi/ds-cpp-selfstudy/tools/enrich/content/search_depth.py:303)。

原句：

> 碰到比它小的元素或子清單的開頭時，就把它放進空出的位置。

**為什麼不對：**課程條件是 `aList[curPos - 1] > curVal`，所以碰到**相等**元素也立即停止。這正是穩定性成立的關鍵，不能只寫「比它小」。

例如將 `2b` 插入已有 `2a` 的前綴時，必須停在 `2a` 後面。

**建議：**

> 碰到不大於它的元素，或已到子清單開頭時，就把它放進空出的位置。

**信心：高。**

---

**10．`#merge` 補充：能比較，不等於任何型別都能交給 `std::sort`**

位置：「不靠比較的排序」；[search_more.py:482](/home/phonchi/ds-cpp-selfstudy/tools/enrich/content/search_more.py:482)。

原句：

> 只要給得出「誰比較小」，任何型別都能排，不必對資料做額外假設。

**為什麼不對：**可比較只是部分條件。`std::sort` 還要求元素符合移動建構、移動賦值與交換要求，比較規則須符合嚴格弱序。可比較但不可移動、不可交換的型別就是反例。[C++ 標準草案：sort 前置條件](https://eel.is/c++draft/sort)、[比較規則](https://eel.is/c++draft/alg.sorting.general)

**建議：**

> 比較式排序不要求 key 是小範圍整數或特定格式；使用 `std::sort` 時，元素仍須可移動與交換，並提供符合嚴格弱序的比較規則。

**信心：高。**

---

**11．`#bankquiz`：餘數碰撞題漏了非負 key 條件**

位置：章末第 11 題；[ch7.json:72](/home/phonchi/ds-cpp-selfstudy/data/questions_zh/ch7.json:72)。

原句：

> 用餘數法 h(k) = k % m……  
> k1 % m 等於 k2 % m，正好表示兩者的差是 m 的倍數。

**為什麼不對：**若 `%` 指本課 C++ 運算，負數時不能直接套此等價關係：

```cpp
-3 % 11 == -3
 8 % 11 ==  8
```

兩個餘數不同，但差 `-3 - 8 = -11` 能被 11 整除。C++ 整數除法向零截斷，並不直接提供非負的數學模數。[C++ 標準草案：除法與餘數](https://eel.is/c++draft/expr.mul)

本頁又特別介紹了負 key，因此這個條件不宜省略。

**建議：**題幹增加「key 皆為非負整數，\(m>0\)」，或把雜湊函數明訂為正規化後的模數。

**信心：高。**

## 2. 檢查過、確認正確的重點

**`#depends` 其餘列與說明：**

| 項目 | 審閱結果 |
|---|---|
| 循序搜尋、有序循序搜尋 | Array、Linked List 均自然支援，確認無誤。 |
| 二分搜尋 | 串列上可維持 \(O(\log n)\) 次比較、總走訪 \(O(n)\)；頁面也區分了每次從整條串列頭重走的較差寫法，確認無誤。 |
| 雜湊 | 本章以陣列直接定位 slot 的說明正確。但「固定大小 Array 必須／Linked List ✗」應限定為本章實作及保留常數時間定位的要求，不能讀成所有雜湊表永遠不可擴容，或串列完全無法模擬。 |
| 合併排序 | 串列 merge 重接節點只需 \(O(1)\) 輔助空間；遞迴版另需 \(O(\log n)\) 堆疊、bottom-up 可整體 \(O(1)\)，確認無誤。表格的 \(O(1)\) 宜直接標明「bottom-up 版本」。 |
| 快速排序 | 單向串列不適合直接搬用課程的左右雙向 partition，改成單向掃描可行，確認無誤；不應概括到雙向串列。 |

**其他已確認項目：**

- 搜尋的平均探查數與二分搜尋最多 \(\lfloor\log_2 n\rfloor+1\) 次的推導，在頁面宣告的計數模型下正確。
- 固定跳格週期 \(m/\gcd(s,m)\)、加 3 仍會群聚、奇質數平方探查的 \((m+1)/2\) 個候選位置及半滿保證，確認無誤。
- 線性探查、平方探查、雙重雜湊、字串加權雜湊的例子，以及補充 A／B 的主要追蹤結果，確認無誤。
- 插入排序平均比較公式、Shell 折半增量最佳／最差分析、Hibbard 上界推導、merge 峰值空間與比較排序下界，未發現計算錯誤。
- 六種課程實作的穩定性判斷與帶標籤反例，確認無誤。
- quicksort「6 個不同元素平均約 15 次比較」經全部 720 種排列重算，得到約 **15.0111 次**，確認無誤。
- 六種排序逐步輸出、平方探查解答與字串加權輸出經記憶體模擬核對；30 項預期輸出均與實際 HTML 一致。
- 已讀完 13 題頁內 quiz、11 題章末題目、36 張詞彙卡；除上述問題外，未找到其他確定的正解或定義錯誤。

## 3. 沒檢查到的部分

- **未編譯執行 C++**；以課程標頭核對、推導及記憶體模擬驗證。
- 未逐張檢視 PNG 圖中的文字與箭頭；已核對圖說、替代文字及相關數字。
- 已抽查動畫 JavaScript，並在記憶體執行六種排序的代表案例，但**未做瀏覽器逐步操作與畫面驗收**。
- 未取得 Knuth、Papernov–Stasevich 原典逐頁核對歷史歸屬；相關頁內數學推導已另行檢查。