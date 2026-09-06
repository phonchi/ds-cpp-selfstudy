# 完整先備教材：舊版覆蓋、順序與樣式驗收

基準：`b97fe81` 的先備頁。前次 `05f490e` 精簡版刪去過多解釋，本次恢復原有主題與教學深度，
換成獨立例子，並保留先教語法、無課本前提、無 Python 前提及不展示課程使用次數的要求。
HTML 是教材正文的唯一可編輯來源；題庫與詞卡由 `data/` 母檔重生。

## 舊主題的去向

| 舊頁／主題 | 新版位置與處理 |
|---|---|
| P1 編譯四階段、指令、骨架 | 先完整程式，後指令與四階段；明列 Windows／Linux 執行方式 |
| P1 型別、I/O、運算、轉型與錯誤 | 拆解初始化、型別、字元／字串、sizeof、輸入失敗、運算順序、轉型時機、溢位及診斷 |
| P2 比較、分支、switch、while／for | 恢復短路、掉落、單一敘述、大括號、do-while、每輪更新與條件檢查次數 |
| P2 range-for | 移至 P5 walk，在容器、參考與 auto 的說明之後 |
| P2 巢狀迴圈與複雜度 | 保留精確計次與 Big-O 成長直覺，改用獨立小例 |
| P3 宣告、傳值／參考、const 參考 | 恢復參數／引數、呼叫／回傳、作用域／生命週期、別名綁定與修改路徑的完整說明 |
| P3 指標參數與三種傳法 | 移至 P4 params，先建立位址、指標與解參考 |
| P3 回傳參考、多載、預設引數、遞迴 | 保留在 P3；以獨立例與三個逐步圖解說明回傳生命週期及呼叫堆疊 |
| P3 getter 的 const | 移至 P8 constmember，在物件概念之後 |
| P4 位址、指標、空指標、陣列與退化 | 恢復指標本身／目標分離、指標算術、尾後位置、sizeof 與長度契約 |
| P4 stack／heap、new／delete、記憶體錯誤 | 保留單一物件、動態陣列、所有權、別名、洩漏、懸空及錯配／重複釋放 |
| P4 Node 物件指標範例 | 移至 P8 thisptr；改為 Reading 與 WorkStep 工作流程，保留物件指標及同型別連結 |
| P5 建立、增刪、容量、攤還 | 恢復括號／大括號差異、搬移成本、size／capacity／reserve／resize 與擴容模型 |
| P5 走訪、失效、二維容器 | iterator 在 insert／erase 前介紹；保留安全刪除、失效與不規則二維資料 |
| P5 stack／queue／deque、string 與串接成本 | 全數保留，使用待辦、排隊、文字解析；保留 UTF-8／char 邊界及 getline 混用提醒 |
| P6 map、set、缺鍵副作用、有序／無序 | 全數保留；iterator／pair 在 find 結果使用前介紹 |
| P6 iterator、structured binding、計數／去重／分組 | 全數保留，三個完整應用與安全 erase 逐步追蹤 |
| P7 檔案、狀態、例外、at／[]、未捕捉 | 擴寫路徑、模式、stringstream、狀態旗標、RAII、跨函式傳遞與處理責任 |
| P7 自訂例外類別 | 移至 P9 custom_exception；一般 throw 與標準例外保留 P7 |
| P8 class、ctor、this、封裝、const、ctor 多載 | 全數保留，補齊生命週期、基本複製與候選選擇 |
| P8 operator<<／friend、組合、標頭 | 保留原主題；Reading.hpp／Reading.cpp／main.cpp 以真正三檔編譯驗證 |
| P9 繼承、建構順序、virtual、抽象介面 | 全數保留；加入靜態／動態呼叫對照、切片與虛擬解構 |
| P9 ==／<、比較與 hash、容器介面 | 全數保留；解釋嚴格弱序、hash/equality 契約、[] 的參考回傳及 begin／end |
| P9 組合／繼承、模板、priority_queue | 全數保留；先教模板，再拆 priority_queue 三參數 |
| P9 資源複製、Rule of Three | 保留深複製、賦值、自我賦值與失敗安全，說明 Rule of Zero／禁止複製替代 |

刪除的是課程次數統計、Python 對照前提與課本耦合；原本知識點沒有因換例子而消失。
每節提供用途、語法、數段推理、完整範例、對照界線及帶理由的練習答案，主要解釋直接展開。

## 參考與技術核對

- [OpenHome C++ Gossip](https://openhome.cc/Gossip/CppGossip/)：補充教學主題與說明層次，範例自行撰寫。
- [C++17 N4659：初始化](https://timsong-cpp.github.io/cppwp/n4659/dcl.init)：區分預設、零與值初始化，避免將未初始化基本成員說成自動為零。
- [string 元素存取](https://timsong-cpp.github.io/cppwp/n4659/string.access)：區分 string 的尾端空字元與 vector 的索引界線。
- [vector capacity](https://timsong-cpp.github.io/cppwp/n4659/vector.capacity)：reserve 不改 size，容量不保證特定倍數；重配置使相關位置失效。
- [stream flags](https://timsong-cpp.github.io/cppwp/n4659/iostate.flags)：fail 含 failbit／badbit，單獨 eofbit 不等同讀取失敗。

## 樣式契約

九頁沿用主文紙色背景、深藍綠漸層、Noto 字型、17px／1.9 正文與 1180px 欄寬。
P1–P3 原有第二套全域覆寫已移除；所有按鈕、目錄、詞卡使用既有 class。
頁面維持自足單檔；`tools/prereq_authoring.py` 是可選的編寫輔助，不是線上依賴。

`check_prereq_browser.py` 逐頁在 1440px 與 390px 比較 introduction 的 computed style：
body、hero、container、h1/h2、TOC 與標準程式區塊。代表截圖另涵蓋頁首、正文、互動與詞卡。
個別主文範例的 inline 字體覆寫不作為全站基準；使用沒有 inline style 的標準程式區塊比較。
手機保留隱藏浮動導覽的既有可讀性設定；P9 長泛型名稱允許換行，程式區塊在自身範圍捲動。

## 跨組獨立閱讀與修正

P1/P2/P4/P8 由一個 GPT-5.6 context 編寫，P5/P6/P7/P9 由另一個編寫，P3 由主代理編寫。
定稿時兩個 context 交叉完整閱讀未參與撰寫的頁面；主代理逐節校準深度、裁定修正並檢查瀏覽器。

已修正：iterator 使用前置、P1 編排與 Windows 指令、未介紹語法、NUL／泛型 HTML escaping、
P8 trace 的 print 與未說明 move、編譯單元名詞、候選建構式不應推論未顯示的內部值、
reserve 條件過度斷言、例外 trace 的輸出時序、解構 trace 累積輸出、模板 larger 的懸空回傳風險。

完整程式以 C++17 編譯執行，多檔範例按實際檔案組織建置；題目每個選項與所有 trace 控制逐一驗證。
測試不把程式片段冒稱完整程式，也不執行未定義行為來期待固定結果。

## 最終驗收結果

- 85 個完整 C++ 程式、1 組真實三檔程式、41 個明確標示的片段、48 段腳本：檢查 0 errors。
- 21 個互動的播放／暫停／前後步／重設／完成重播通過；99 題的所有 310 個選項與回饋通過。
- 149 張詞卡的資料與顯示一致，翻面、全部翻面／翻回、洗牌與鍵盤操作通過。
- 九頁在 1440px／390px 的主文樣式比較全部相同，沒有整頁水平溢出；另檢視代表畫面。
- 全站連結 0 錯誤／0 警告、對比 0 失敗、git diff --check 通過；限定頁面重生與選項洗牌保持冪等。
- 審查結論限定此來源快照與受測環境；沒有把未定義行為當作固定輸出，也沒有把程式片段算成完整程式。
