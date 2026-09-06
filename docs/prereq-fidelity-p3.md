# P3 原稿逐項恢復與核對

基準為 `b97fe81:p3_functions.html` 及當時的兩份 p3 JSON。原始檔實際表格、子節與題卡逐項閱讀，
不以大標題相同代替保留。現稿只局部增補，907190b 的所有正常例子、逐步說明與互動均保留。

## 每張原表的實際去向

| 原表／位置 | 原比較資訊 | 新版位置 |
|---|---|---|
| 宣告／定義，約646行 | 外觀、作用、次數、檔案組織 | `#restore-declaration-table`，另補缺少宣告／定義的不同失敗階段；規則限定本頁一般函式 |
| 傳值時機，約717行 | 小型數值、需要副本、大型只讀物件 | `#restore-value-decisions`，保留選擇維度，移除固定byte速度與一律禁止大物件傳值的錯誤斷言 |
| 傳值／參考，約788行 | 取得什麼、修改原物件、複製、呼叫寫法、常量與運算式 | `#restore-value-reference`，保留所有列，補讀取方式與生命週期條件 |
| 參數決策，約967行 | 用途、寫法、複製、能否修改 | `#restore-parameter-decisions`，T 先說明為型別記號，指標列連至 P4 |
| 四路完整矩陣，約1373行 | 傳值、參考、const參考、指標的身分／修改／複製／空值／改目標／呼叫／讀值／用途 | `#restore-four-parameter-matrix`，完整9個比較維度；刪掉課程用量列；指標只複製位址、局部改指標不會自動改呼叫端指標 |
| Python/C++ 對照，約1420行 | 可見宣告、參數共享、預設值、多載、回傳生命週期與遞迴限制 | `#restore-function-task-map`，轉成需求／C++／界線，保留C++資訊而不要求另一語言背景 |
| 資源表，約1448行 | C++ Tutor、reference/default arguments、P4、遞迴 | `#restore-function-task-map` 第二表；兩個cppreference連結與原稿一致，另保留OpenHome及P8導引 |

## 原子節、警告與圖解

| 原內容 | 處理 |
|---|---|
| 以三種 swap 開場 | 替換成已有完整語法前置的運費／點數例；不是刪掉傳參比較。 |
| 宣告定義、傳值、參考與const參考 | 保留907190b完整說明，加上上述原比較表。 |
| 指標參數 | 已移到 P4 `#params`，其前有位址與解參考；P3矩陣提供實際連結。 |
| getter 的尾端const | 已移到 P8 `#constmember`，有對照參數const與成員函式const。 |
| 回傳區域物件連結禁忌 | `#restore-return-warning` 補警告與4列生命週期表，保留原錯誤片段。 |
| 預設引數靠右、多載衝突 | `#restore-default-warning` 補4列核對表，與正常程式、原反例並存。 |
| 遞迴、每次呼叫獨立狀態 | 保留原現稿的倒數及呼叫框架互動。 |
| 遞迴回傳結果 | `#restore-recursive-return` 用逐日閱讀量取代舊例，完整程式與4列返回計算表。 |
| 遞迴空間成本與堆疊溢位 | 同區補固定框架空間時的 O(深度)，以及平台限制和非固定失敗方式；不能用一次試跑判定任意深度安全。 |
| 每頁特有hero | 原 b97fe81 函式框／副本／別名 SVG 已恢復；不是通用網格代替。 |

## 原題庫的知識去向

- 原Q1傳值：P3現Q5與 `#byvalue`。
- 原Q2傳參考：P3別名題、`#byref`完整程式及參考互動；不只提名。
- 原Q3指標參數：移P4的完整三傳法與pointer題，避免P3未教指標就考。
- 原Q4多載與預設值混用：P3新增Q12，三個實際呼叫各自配對版本。
- 原Q5遞迴數值回傳：P3新增Q11與 `#restore-recursive-return`，不是只用進入／離開訊息代替。
- 原Q6大型只讀vector：P3新增Q13以已解釋的T與完整矩陣考相同選擇，vector具體使用在P5。

所有13題都是四個不同選項、唯一boolean正解；每個錯項說明其具體誤解。

## 原18張字卡的知識去向

| 原術語 | 承接位置 |
|---|---|
| Function Prototype | P3宣告／定義字卡與完整對照表 |
| Pass by Value | P3同名字卡與副本完整例 |
| Copy Constructor | P8雙語字卡、複製建構式與生命週期程式 |
| Reference／Pass by Reference | P3兩張雙語字卡與綁定比較 |
| Pass by Pointer／NULL | P4指標參數與nullptr字卡、P3矩陣導引 |
| const Reference | P3雙語字卡與唯讀途徑說明 |
| const Member Function | P8雙語字卡與尾端const對照 |
| Return by Reference | P3雙語字卡與生命週期對照 |
| Dangling Pointer | P4雙語字卡，P3另保留懸空參考 |
| Undefined Behavior | P3補回雙語字卡及回傳警告 |
| Function Overloading／Default Argument | P3雙語字卡、矩陣與混合呼叫題 |
| Call Stack／Stack Frame | P3分別保留呼叫堆疊與呼叫框架雙語字卡 |
| Base Case／Stack Overflow | P3兩張雙語字卡、遞迴返回表及空間限制 |

原稿「參考絕不占空間」「固定指標大小」「回傳必然複製」「遞迴必然某訊號」等不精確處已更正；
保留比較維度與教學用途，不以更正為理由刪除整表。
