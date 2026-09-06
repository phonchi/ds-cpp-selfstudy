# P1／P2／P4／P8 fidelity ledger

基準：`b97fe81`。本輪只在既有正文追加可追蹤區塊，不取代 907190b 已有的完整例、trace、練習與更正。舊稿中的 Python 前提、課程使用次數與 Node／Fraction／Stack 教材案例不照搬；保留的知識改用中性敘述或自主案例。

## P1

| 舊稿位置與內容 | 新位置 | 處理 |
|---|---|---|
| `p1_cpp_basics.html:544` Python/C++ 執行差異表 | `#restore-p1-types` | 去除 Python 前提，保留型別決定、錯誤時機；建置差異由既有四階段接手。 |
| `:571` 指令零件／意思／不寫後果 | `#restore-p1-build` | 完整恢復 g++、standard、warnings、source、`-o` 五列。 |
| `:640` 為何分四階段提示 | 既有 `#prologue` 與 `#restore-p1-diagnostics` | 保留診斷用途。 |
| `:662` 骨架零件表 | `#restore-p1-skeleton` | 恢復 include、main、區塊、分號、return 與缺漏後果。 |
| `:674` `<...>` 對 `"..."` | `#restore-p1-skeleton` | 恢復搜尋路徑與使用時機；多檔細節連 P8。 |
| `:708` 現代 C++ 提示 | 既有 `#skeleton` | 保留 `std::` 與列表初始化，未恢復 using-directive 教材習慣。 |
| `:725` 動態／靜態型別矩陣 | `#restore-p1-types` | 中性化為三個靜態型別比較問題。 |
| `:789` 未初始化、`:820` 翻車警告、`:826` 多變數宣告 | 既有 `#types` | 未初始化完整保留；多變數同列不再鼓勵，維持一列一宣告。 |
| `:866` I/O 任務表 | `#restore-p1-io` | 恢復 cout、cin、getline、cerr；getline 混用連 P5。 |
| `:878` endl/換行表 | `#restore-p1-io` | 恢復換行、flush、選擇情境。 |
| `:895` token/整行小節、`:948` 空白警告 | `#restore-p1-io` | 恢復資料邊界，進階混用移 P5。 |
| `:953` printf 小節與`:958`格式表 | `#restore-p1-io` | 恢復 `%d/%lld/%f/%s` 與錯配風險，例句中性化。 |
| `:1029` 整除表 | `#restore-p1-arithmetic` | 恢復正負整除、餘數恆等式與浮點對照，修正「負數向下取整」風險。 |
| `:1043` 遞增與複合指定 | 既有 `#operators` | 保留前後置時機與拆行原則。 |
| `:1075` 優先序、`:1100` 表 | `#restore-p1-arithmetic` | 恢復八層重要運算子與括號準則。 |
| `:1131` rand/srand 提示 | `#restore-p1-random-limits` | 恢復 seed、取模、偏差、重現性與 `<random>` 界線；不固定序列。 |
| `:1161` 隱式／明式轉型表、`:1210/:1215`提示 | `#restore-p1-arithmetic` | 恢復轉型時機；不鼓勵舊 C-style cast。 |
| `:1219` overflow、`:1252/:1256` INT_MAX | 既有 `#convert` + `#restore-p1-random-limits` | 修正舊「帶號必回繞」錯說；恢復上限哨兵、碰撞與加法溢位風險。 |
| `:1278` 錯誤片段、`:1372` 診斷分類、`:1386` debug 習慣 | `#restore-p1-diagnostics` | 恢復編譯／連結／執行／邏輯／warning 五類。 |
| `:1456/:1471/:1485/:1504` reference 四組表 | 既有 `#reference` + `#restore-p1-build/types/io/arithmetic` | 各維度移回相關教學區；刪 Python 欄但未刪 C++ 知識。 |
| `:1532` 延伸閱讀表 | 既有 reference 後連結 | 以主題連結取代資源矩陣。 |

## P2

| 舊稿位置與內容 | 新位置 | 處理 |
|---|---|---|
| `p2_flow_control.html:544` 課程例／次數／成本表 | `#restore-p2-loop-matrix` | 去課程耦合，保留形狀、精確次數與 Big-O。 |
| `:559-630` 循序／選擇／重複 SVG | `#restore-p2-flow-shapes` | 以中性流程重新繪製。 |
| `:685` 運算子／唸法／注意 | `#restore-p2-operators` | 恢復五類與短路、指定陷阱。 |
| `:696` 短路小節 | 既有 `#bool` trace | 完整保留。 |
| `:819/:827` 條件順序與現代寫法 | 既有 `#ifelse` | 以門檻順序與 braces 保留。 |
| `:877` braces 警告、`:882` assignment bug、`:914`習慣 | 既有 `#ifelse` | 保留，警告由正文與題庫承接。 |
| `:919` 三元運算子 | `#restore-p2-conditional` | 恢復語法、短路分支與適用界線，新增可執行例。 |
| `:946` if/switch 形狀表、`:1062` switch/else-if 比較 | `#restore-p2-branch-choice` | 合併恢復條件形狀、順序、結束與情境。 |
| `:1142` 無窮迴圈、`:1165` while 演算法例 | 既有 `#while` | 保留狀態必須前進；教材算法換成數字位數。 |
| `:1311` for 邊界矩陣、`:1322`變數範圍 | `#restore-p2-for-boundaries` + 既有 `#forloop` | 恢復四種邊界與實際值，補 unsigned 倒數警告。 |
| `:1327-1373` chrono 樣板與 include | `#restore-p2-timing` | 恢復 clock、auto、duration_cast、count；只驗證非負，不固定時間。 |
| `:1385-1443` range-for 五維表與複製警告 | P5 `#walk` | 已移頁並在 `#restore-p2-loop-matrix` 明確連結。 |
| `:1533` break/continue | 既有 `#jump` | 完整保留 for 更新與最內層界線。 |
| `:1581` loop形狀／次數／成本 | `#restore-p2-loop-matrix` | 恢復 n、n²、三角和。 |
| `:1628/:1649/:1662/:1682` reference 骨架、選擇、跨語言、規則 | 既有 `#reference` + `#restore-p2-loop-matrix` | 恢復 loop 選擇；跨語言欄刪除。 |
| `:1691` 延伸閱讀 | 既有補充連結 | 保留主題去向。 |

## P4

| 舊稿位置與內容 | 新位置 | 處理 |
|---|---|---|
| `p4_pointers_memory.html:545` 課程使用矩陣 | 既有頁序與 `#restore-p4-stack-heap` | 去使用次數／教材章名，保留 new、空指標、生命週期。 |
| `:625-674` 指標雙格 SVG | `#restore-p4-memory-picture` | 中性重繪 p 與 x，不假定位址值／大小。 |
| `:686` 符號／位置／意思表 | `#restore-p4-symbols` | 恢復宣告與運算式中的 `*`、`&`，另連 P8 `->`。 |
| `:728` 指標用途提示 | 既有 arithmetic/params | 由走訪與可空參數具體承接。 |
| `:732-754` reference vs pointer 表與選擇 | `#restore-p4-reference-pointer` | 擴為值／參考／指標七維；不宣稱參考不占空間。 |
| `:813/:819` NULL 警告與現代對照 | 既有 `#null` | 修為 `nullptr`，保留不可解參考。 |
| `:909` 陣列參數長度警告 | 既有 `#decay` | 保留 `sizeof` 失效原因。 |
| `:930` stack/heap 表 | `#restore-p4-stack-heap` | 恢復建立、結束、大小、風險。 |
| `:1016-1068` new/delete/NULL 三階 SVG | `#restore-p4-lifetime-picture` | 中性重繪並改 `nullptr`；說清 alias 不同步。 |
| `:1080` 三災難表、`:1090/:1095`提示 | `#restore-p4-failure-matrix` + 既有 ownership trace | 恢復症狀並擴充錯配釋放。 |
| `:1113` Node 教材案例 | P8 普通類別與本頁 ownership | 不恢復教材類別；知識由自主例覆蓋。 |
| `:1202/:1221` 語法與四規則 | 既有 `#reference` + restoration tables | 保留且深化。 |
| `:1229` 延伸閱讀 | 既有補充連結 | 保留。 |

## P8

| 舊稿位置與內容 | 新位置 | 處理 |
|---|---|---|
| `p8_oop_basics.html:549` ADT/C++/例子矩陣 | `#restore-p8-adt` | 用 Reading 恢復狀態、操作、介面、實體六列。 |
| `:615/:619` constructor 與 this 子節 | 既有 `#construct/#thisptr` + `#restore-p8-class-syntax` | 保留並納入語法總表。 |
| `:636` self 對照 | 既有 this 解釋 | 去 Python 前提，保留隱含指標語意。 |
| `:674` public/private/protected 表 | `#restore-p8-access` | 三列完整恢復；protected 連 P9。 |
| `:683` class 預設 private 警告 | `#restore-p8-access` | 恢復，未提前展開繼承層級。 |
| `:734` 封裝取捨提示 | 既有 `#encapsulation` | 改以 invariant 判準，移除教材類別對照。 |
| `:773` const 習慣提示 | 既有 `#constmember` | 保留尾端 const 與回傳 const 的差異。 |
| `:821` constructor 候選逐項比較 | 既有 `#candidates` trace | 完整保留。 |
| `:862` most vexing parse | `#restore-p8-vexing` | 以 Timer 恢復四列比較。 |
| `:870-914` operator&lt;&lt; 從失敗到成功與注意 | `#restore-p8-stream-contrast` + 既有 `#stream` | 恢復找不到 overload、簽章、串接、friend 權限。 |
| `:922` composition | 既有 `#composition` | 以 Parcel/Reading 保留 has-a 與建構順序。 |
| `:975/:994` hpp/include guard/template 提示 | 既有 `#files` | 完整三檔例、`::`、guard、編譯命令；template 延至 P9。 |
| `:999` Node 練習 | 既有 Reading/Timer/Parcel 練習 | 教材類別不恢復。 |
| `:1023/:1043` syntax 與跨語言表 | `#restore-p8-class-syntax` | 恢復 C++ 語法，刪跨語言欄。 |
| `:1059` 延伸閱讀 | 既有 reference | 由頁內與 P9 連結承接。 |

## 題庫與字卡

四頁題庫均保留原題語義並擴為每題四個選項；每題恰一個 boolean `correct: true`，錯誤選項各自指出具體誤解。字卡正面統一為「中文（English term 或 C++ identifier）」；背面保留既有深化定義。HTML 的 bankquiz/cards 由共用同步流程統一生成，避免本輪手改兩份來源。

## 逐列補核（第二輪）

第一次 ledger 中以章節概括承接、但原列資訊未完全出現的項目，已改為下列明確去向：

| 舊稿細項 | 完整新 anchor | 實際恢復的列／限制 |
|---|---|---|
| P1 `:1485` 型別大小與範圍 | `#restore-p1-type-complete` | bool、char、short、int、unsigned int、long long、float、double、int*、string 十列；每列含常見大小、標準限制／查法、用途。char signedness、pointer/string大小均標依實作。 |
| P1 `:826` 多名稱宣告提示 | `#restore-p1-declarations` | `int a,b`、`int* p,q`、多個 const 三列；保留合法語法、逐 declarator 判讀與分行建議。 |
| P1 `:1100` 完整優先序 | `#restore-p1-precedence-complete` | 補 `[] . ->`、後置、前置 `* &`、shift、`?:`、`%=`；未教語法逐列連 P2/P4/P5/P8。 |
| P1 `:1161` 轉換判斷 | `#restore-p1-conversion-complete` | 補 `7/2.0`、bool↔int、char→int、int→char；字元編碼與可表示性限定為執行字元集／實作。 |
| P1 `:953-958` printf | `#restore-p1-library-runs` 第一例 | 可跑欄寬／對齊／兩位小數例，並說明格式錯配風險。 |
| P1 `:1131` rand/srand | 同 anchor 第二例 | fixed seed 在同一實作重設後重現、`%6` 範圍不變量；不固定跨平台序列，明示模數偏差。 |
| P1 `:1252-1257` INT_MAX 哨兵 | 同 anchor 第三例 | `numeric_limits<int>::max()` 可跑例、哨兵碰撞前提及 `distance <= max-step` 溢位守衛。 |
| P1 `:1278/:1372` 診斷解剖 | `#restore-p1-diagnostic-anatomy` | file、line、column、severity、message、source/caret 六列與實際診斷片段；錯誤類型矩陣仍在 `#restore-p1-diagnostics`。 |
| P2 `:1311` 倒序邊界 | `#restore-p2-halving` | `i>=0` 含 0、`i>0` 不含 0，皆列 n≥1 與有號限制。 |
| P2 `:1581` 折半／混合成本 | `#restore-p2-halving`、`#restore-p2-loop-matrix` | `/=2` 真實狀態與 floor(log₂n)+1、O(log n)，另列外層 n 次形成 O(n log n)。 |
| P2 `:1385` range-for 五維表 | P5 `#restore-p5-range-bindings` | 負責頁已新增 copy/reference/const-reference 三列與身分、修改、複製、用途五維；P2 `#restore-p2-loop-matrix` 直連該 anchor。 |

## 主代理最終補核

P1已避免在P4前用const char*，printf例直接傳字串字面值；整數界線先用climits，數值工具的模板寫法不作P1前提。
P4三階圖加上時間方向與實／虛線箭頭，並補smart pointer字卡的正文解釋。
P8補回classes規則、物件記憶體觀察與P9的資源表。原詞卡缺詞另已逐項補回；表中的移頁指向真實內容。
