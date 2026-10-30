"""3D 資料結構矽晶群島（island/index.html）的全部文案與資料。

ds-cpp 沒有 pages.py，頁面清單就放在這裡；build_island.py 會比對每個 stem 的 .html 是否存在、
refs 與代表圖 id 是否有效、路線與猜題是否齊全，有缺就報錯。

  PAGES   — 21 頁（順序＝列表順序與授課順序）
  FIGS    — 正課各章的代表互動圖（教材頁裡的元素 id；不可在收合的 <details> 內，否則深連結看不到）
  GUIDE   — 阿迭到每一站時說的話
  TOUR    — 路線與台詞
  QUIZ    — 「先猜下一步」：每章一題，answer 是選項索引；build 會檢查正解位置是否平衡
  GRAPH   — 第 8 章地標與 BFS／DFS 對照共用的圖
  COMPARE — 「同操作對比」的四組；步數由 island.js 模擬算出，這裡只放文字

地標的結構約束（改 island-scene.js 時不能違反，check_island_browser.js 會實測）：
  - 陣列的格子彼此間距為 0
  - 鏈結串列的節點不共線，一定靠箭頭相連，尾端接 nullptr
  - 堆疊只有頂端開口，四面都有護欄
  - 樹的根在最上面，葉在下面
  - 圖要有環，已訪問的頂點不重複加入
  - 匯流排只表示授課順序，樣式必須和資料結構裡的指標箭頭不同
"""

# 三區。鍵＝Page 的 grp；順序＝列表順序。
ISLES = {
    "power": dict(name="電源島", sub="課前準備 · 先讀", note="先接上電源：弄清楚為什麼要學，把開發環境準備好。"),
    "core": dict(name="正課九島", sub="授課順序 01–09", note="金色匯流排依授課順序串起九座晶片島，可以自由進入任何一章。"),
    "dimm": dict(name="先備記憶體模組", sub="C++ 先備 · 查閱用", note="插在主機板上的九顆記憶體：讀正課卡在語法時，再回來查。"),
}

PAGES = [
    dict(stem="00a_why_code", grp="power", code="00A", title="AI 時代，為什麼還要學資料結構？", label="先讀",
         landmark="電源開關",
         blurb="從「能編譯」到「資料變多還跑得動」的距離，選錯容器的代價，以及記憶體是你自己的責任。"),
    dict(stem="00b_setup", grp="power", code="00B", title="課前準備與環境安裝", label="必做",
         landmark="連接埠",
         blurb="安裝 g++ 與 gdb，讓課程 notebook 能跑 C++，並跑通第一支程式。"),
    dict(stem="00c_vscode_windows", grp="power", code="00C", title="Windows VS Code 作業實戰", label="作業首選",
         landmark="除錯探針",
         blurb="設定編譯與除錯、練習多檔編譯和命令列參數，並用中斷點一步步看程式執行。"),

    dict(stem="introduction", grp="core", code="01", title="C++ 導論", label="cppds Ch.1",
         landmark="位址暫存器", refs=["p1_cpp_basics", "p4_pointers_memory", "p8_oop_basics"],
         blurb="型別佔多少位元組、指標存的是位址，再用 Fraction 與邏輯閘電路走完類別、多載與繼承。"),
    dict(stem="analysis", grp="core", code="02", title="演算法分析", label="cppds Ch.2",
         landmark="成長曲線塔", refs=["p2_flow_control", "p5_vector_string", "p6_map_set"],
         blurb="用大 O（Big-O）描述成長速度，比較 anagram 的四種解法，並看 vector 與 string 各操作的成本。"),
    dict(stem="arrays", grp="core", code="03", title="陣列與稀疏矩陣", label="附錄 A",
         landmark="記憶體條", refs=["p4_pointers_memory", "p5_vector_string", "p8_oop_basics"],
         blurb="連續格子與位址計算、二維陣列的列優先（row-major）配置、自己寫 ArrayList，以及稀疏矩陣的字典式表示法（Dictionary of Keys，DOK）。"),
    dict(stem="linked_lists", grp="core", code="04", title="鏈結串列", label="cppds Ch.4",
         landmark="散落節點站", refs=["p4_pointers_memory", "p8_oop_basics", "p9_oop_advanced"],
         blurb="節點散在記憶體各處，只靠指標相連。實作無序與有序串列，再學哨兵節點、雙向與環狀串列。"),
    dict(stem="linear_structures", grp="core", code="05", title="堆疊、佇列與 Deque", label="cppds Ch.3",
         landmark="三根存取管", refs=["p5_vector_string", "p8_oop_basics", "p9_oop_advanced"],
         blurb="限制「從哪裡進、從哪裡出」帶來的力量：括號配對、中序轉後序、印表機模擬與回文判斷。"),
    dict(stem="recursion", grp="core", code="06", title="遞迴", label="cppds Ch.5",
         landmark="呼叫框架塔", refs=["p3_functions", "p5_vector_string"],
         blurb="遞迴三法則與呼叫堆疊，河內塔、碎形與迷宮，最後用動態規劃解找零錢。"),
    dict(stem="searching_sorting", grp="core", code="07", title="搜尋與排序", label="cppds Ch.6–7",
         landmark="雜湊櫃與比較柱列", refs=["p5_vector_string", "p6_map_set"],
         blurb="循序與二分搜尋、雜湊表與碰撞處理，以及六種排序法的逐步動畫。"),
    dict(stem="graphs", grp="core", code="08", title="圖與圖演算法", label="cppds Ch.9",
         landmark="頂點接線盤", refs=["p5_vector_string", "p6_map_set", "p8_oop_basics"],
         blurb="相鄰矩陣與相鄰串列、廣度優先搜尋（Breadth-First Search，BFS）與深度優先搜尋（Depth-First Search，DFS），再到 Dijkstra 最短路徑與 Prim 最小生成樹。"),
    dict(stem="trees", grp="core", code="09", title="樹與樹演算法", label="cppds Ch.8",
         landmark="二元搜尋樹掛架", refs=["p4_pointers_memory", "p8_oop_basics", "p9_oop_advanced"],
         blurb="三種走訪、Binary Heap 與優先佇列、二元搜尋樹（Binary Search Tree，BST）的插入與刪除，到 AVL 旋轉。"),

    dict(stem="p1_cpp_basics", grp="dimm", code="P1", title="C++ 基礎與編譯流程", label="從這裡開始",
         landmark="記憶體顆粒 P1",
         blurb="從完整程式走過編譯四階段，拆解型別、輸入輸出與轉型，再練習讀懂錯誤訊息。"),
    dict(stem="p2_flow_control", grp="dimm", code="P2", title="流程控制", label="條件與重複",
         landmark="記憶體顆粒 P2",
         blurb="追蹤短路求值、條件分支與各種迴圈，並計算巢狀迴圈的執行次數。"),
    dict(stem="p3_functions", grp="dimm", code="P3", title="函式與參考", label="重要基礎",
         landmark="記憶體顆粒 P3",
         blurb="追蹤引數、回傳與作用域，分清傳值和傳參考，並理解遞迴的呼叫堆疊。"),
    dict(stem="p4_pointers_memory", grp="dimm", code="P4", title="陣列、指標與動態記憶體", label="重要基礎",
         landmark="記憶體顆粒 P4",
         blurb="分清指標本身與目標物件，理解指標算術、堆疊與堆積，以及配置、釋放和所有權。"),
    dict(stem="p5_vector_string", grp="dimm", code="P5", title="vector 與 string", label="清單與文字",
         landmark="記憶體顆粒 P5",
         blurb="容器增刪、容量與攤還、三種走訪、迭代器失效，以及文字處理和串接成本。"),
    dict(stem="p6_map_set", grp="dimm", code="P6", title="map、set 與迭代器", label="查詢與去重",
         landmark="記憶體顆粒 P6",
         blurb="從鍵值查詢走到迭代器、有序與無序容器，再完成計數、去重和分組。"),
    dict(stem="p7_files_exceptions", grp="dimm", code="P7", title="檔案與例外", label="讀寫與錯誤處理",
         landmark="記憶體顆粒 P7",
         blurb="處理路徑、讀寫模式與逐行解析，追蹤串流狀態，並讓例外跨函式傳遞。"),
    dict(stem="p8_oop_basics", grp="dimm", code="P8", title="類別與物件", label="重要基礎",
         landmark="記憶體顆粒 P8",
         blurb="把資料和操作包成類別：建構子、封裝與成員函式，是讀懂課程標頭的基礎。"),
    dict(stem="p9_oop_advanced", grp="dimm", code="P9", title="類別延伸與模板入門", label="接著讀 P8",
         landmark="記憶體顆粒 P9",
         blurb="繼承與多型、抽象介面、運算子，以及看懂 template <typename T> 的容器寫法。"),
]

# 正課九章的代表互動圖。prep＝截圖前在教材頁執行的 JS，wait＝之後等待的毫秒數。
FIGS = {
    "introduction": dict(fig="ptrVis", caption="照順序按四顆按鈕，看變數格與指標格怎麼變。",
                         prep="ptrStep(1);ptrStep(2);ptrStep(3)", wait=400),
    "analysis": dict(fig="growthCanvas", caption="把 n 拉大，看哪一條線先離開畫面：那就是成長最快的項。"),
    "arrays": dict(fig="alVis", caption="insert(1, 99) 一次複製一格；中途會暫時出現兩個相同的值。",
                   prep="alScenario.value='insert';alLoad();for(let i=0;i<3;i++)alStep()", wait=500),
    "linked_lists": dict(fig="uAddVis", caption="單步看 add(26)：新節點先接住原本的第一個節點，head 才改指。",
                         prep="llCase('uAdd','mid',document.querySelector('[data-ll=uAdd]'));llStep('uAdd');llStep('uAdd');llStep('uAdd')", wait=500),
    "linear_structures": dict(fig="stackVis", caption="push、pop、top 都只碰得到最上面那一個。"),
    "recursion": dict(fig="hanoiVis", caption="河內塔：每次遞迴都把問題縮小一層，並留下要回來處理的工作。",
                      prep="hanoiStart()", wait=3500),
    "searching_sorting": dict(fig="hashTable", caption="選線性探查或鏈結法，把同一批值放進表裡，比較碰撞怎麼處理。",
                              prep="document.getElementById('hashBatchInsert').click()", wait=500),
    "graphs": dict(fig="canvas-bfs", caption="BFS 一層一層往外擴散：相距 k 條邊的頂點全部出列之前，相距 k+1 條邊的只能排隊。",
                   prep="document.getElementById('bfsPlay').click()", wait=5000),
    "trees": dict(fig="canvas-bst", caption="輸入一個 key，看它從根開始一路比較、往左或往右走。"),
}

# 阿迭到每一站時說的話（路線 ①＋③ 涵蓋全部頁面，所以每頁都要有）
GUIDE = {
    "00a_why_code": "我是迭代器（iterator），不存資料，只負責指向下一站。第一站先想清楚：為什麼要花時間學這些？",
    "00b_setup": "接上連接埠！g++ 和 kernel 裝好，後面每一章的程式才跑得起來。",
    "00c_vscode_windows": "這根探針是除錯器。會設中斷點，就不必靠猜來找錯。",
    "introduction": "正課開始！先看這排位元組：指標 p 存的不是值，是位址。",
    "analysis": "同樣把 n 變大，六根柱子長得完全不同。寫程式之前，先學會預估成長速度。",
    "arrays": "格子一格緊貼一格，所以算得出第 i 格的位址；代價是中間插入時，後面全部要搬。",
    "linked_lists": "節點散在各處，靠箭頭才找得到彼此。插入只改箭頭，其他節點不動；但要先走到那裡。",
    "linear_structures": "這三根管子的差別只在開口：堆疊只開一端，佇列一進一出，Deque 兩端都能進出。",
    "recursion": "每呼叫一次就疊一層框架，到了基底條件才一層一層回傳。別想跳過中間那幾層。",
    "searching_sorting": "雜湊讓你直接算出位置，不必一格一格找。可是兩個值算出同一格時，就要處理碰撞。",
    "graphs": "圖沒有上下之分，還可能繞回原點，所以要記住走過哪裡。",
    "trees": "根在最上面，比它小往左、比它大往右，每比一次就少走一半……前提是樹夠平衡。",
    "p1_cpp_basics": "先備第一顆：一支 C++ 程式如何從原始碼變成執行檔。",
    "p2_flow_control": "條件與迴圈。第 2 章算步數時，靠的就是數這些迴圈。",
    "p3_functions": "傳值還是傳參考？弄懂這顆，遞迴和類別都會順很多。",
    "p4_pointers_memory": "很重要的一顆：指標、new 和 delete。鏈結串列和樹都建在它上面。",
    "p5_vector_string": "vector 和 string 幾乎每一章都會用，也是理解容量與攤還的地方。",
    "p6_map_set": "map、set，還有我的本行：迭代器。",
    "p7_files_exceptions": "讀檔和例外處理：課程範例開檔或 throw 時，看這裡。",
    "p8_oop_basics": "課程標頭全都是類別，先看懂建構子和成員函式。",
    "p9_oop_advanced": "看到 template <typename T> 別緊張，這顆會解釋。",
}

_CORE = ["introduction", "analysis", "arrays", "linked_lists", "linear_structures", "recursion",
         "searching_sorting", "graphs", "trees"]
_PRE = ["00a_why_code", "00b_setup", "00c_vscode_windows"]
_DIMM = [p["stem"] for p in PAGES if p["grp"] == "dimm"]

TOUR = dict(
    name="阿迭",
    hello="嗨，我是阿迭（it），要我帶你走一趟嗎？",
    short="阿迭帶路",
    ask="想走哪一條路線？",
    resume="上次走到第 {n} 站「{title}」，要接著走嗎？",
    bye="我現在是 end()，別解參考我！想去哪座島，直接點它就好；需要我時再按「阿迭帶路」。",
    routes=[
        dict(key="first", label="第一次來", note="電源島 3 站，再照授課順序走正課 9 章", stems=_PRE + _CORE),
        dict(key="core", label="照正課走", note="正課 9 章，每站都能猜一題", stems=_CORE),
        dict(key="prereq", label="補 C++ 先備", note="記憶體模組 P1 到 P9", stems=_DIMM),
    ],
)

# 先猜下一步：九章各一題。答完才播放該島的地標動畫。
QUIZ = {
    "introduction": dict(
        q="int x = 100; int* p = &x; *p = 50; 之後，cout << x 印出什麼？",
        options=["100", "50", "x 的位址", "編譯錯誤"], answer=1,
        why="p 存的是 x 的位址，*p 沿著位址找到 x 本人，所以寫入 50 改的就是 x。"),
    "analysis": dict(
        q="某個演算法的步數約為 c·n²（n 夠大，主導項已經佔優勢）。n 變成 2 倍時，步數大約變成幾倍？",
        options=["2 倍", "3 倍", "4 倍", "8 倍"], answer=2,
        why="c·(2n)² = 4·c·n²。動畫裡把 n 調大，n² 會比 n 和 n log n 更快撞到刻度上限。"),
    "arrays": dict(
        q="ArrayList 裡有 5 個元素，容量足夠。insert(1, 99) 要先複製幾個元素，才空得出位置？",
        options=["4 個", "1 個", "5 個", "0 個"], answer=0,
        why="索引 1 到 4 這 4 個都要往後複製一格，而且要從最後面開始，才不會蓋掉還沒搬的值。"),
    "linked_lists": dict(
        q="在無序串列的最前面 add(26)，原有的節點要搬動幾個？",
        options=["全部", "一半", "1 個", "0 個"], answer=3,
        why="節點不必相鄰，所以不用搬。只改兩條指標：新節點的 next 先接住舊的第一個，head 再指向新節點。"),
    "linear_structures": dict(
        q="對空堆疊依序 push A、B、C，再 pop 三次。取出的順序是？",
        options=["A、B、C", "C、B、A", "B、A、C", "A、C、B"], answer=1,
        why="堆疊只能碰最上面，最後放的最先出來。旁邊的佇列放同樣三個值，出來的順序就是 A、B、C。"),
    "recursion": dict(
        q="呼叫 fact(4) 時，哪一層最先回傳？",
        options=["fact(4)", "fact(3)", "fact(2)", "fact(1)"], answer=3,
        why="fact(4) 要等 fact(3)，一路等到基底條件 fact(1) 回傳 1，才能一層一層乘回來。"),
    "searching_sorting": dict(
        q="表的大小是 11，用線性探查。77 已經在 slot 0，再插入 44（44 mod 11 = 0），44 會落在哪裡？",
        options=["slot 1", "slot 0，蓋掉 77", "slot 4", "slot 10"], answer=0,
        why="slot 0 被佔了，線性探查一次往後看一格，所以落在下一個空位 slot 1。"),
    "graphs": dict(
        q="BFS 從 A 出發。離 A 有 2 條邊的頂點，什麼時候才會出列？",
        options=["碰到它就立刻處理", "隨機決定", "所有離 A 只有 1 條邊的頂點都出列之後", "等 DFS 走完之後"], answer=2,
        why="佇列先進先出，相距 k+1 條邊的頂點只會排在相距 k 條邊的後面，所以一層一層往外擴散。這裡數的是邊數；要考慮邊上的權重，就要用 Dijkstra。"),
    "trees": dict(
        q="在這棵 BST（依序插入 70、31、93、94、14、23、73）插入 40，它會變成誰的子節點？",
        options=["70 的左子節點", "14 的右子節點", "93 的左子節點", "31 的右子節點"], answer=3,
        why="40 比 70 小往左，比 31 大往右，而 31 的右邊是空的，就放在那裡。"),
}

# 第 8 章地標與 BFS／DFS 對照共用。座標是晶片島上的局部座標（單位同場景）；邊含環 A-B-D-C-A。
GRAPH = dict(
    start="A",
    vertices={"A": [-8, -5], "B": [-2, -6.3], "C": [-7, 1], "D": [-1.5, -1], "E": [3.2, -5], "F": [-3, 5.5], "G": [3, 4.5]},
    edges=[["A", "B"], ["A", "C"], ["B", "D"], ["C", "D"], ["B", "E"], ["D", "G"], ["C", "F"], ["F", "G"], ["E", "G"]],
)

COMPARE = dict(
    pairs=[
        dict(key="insert", label="陣列 vs 鏈結串列", left="陣列", right="鏈結串列", stems=["arrays", "linked_lists"],
             op="在指定位置插入一個值",
             options=[dict(v=0, label="最前面"), dict(v=4, label="中間"), dict(v=8, label="尾端")], default=4,
             opt_label="插入位置",
             notes={"0": "插在最前面：陣列要搬動全部元素，串列只改 2 條指標。",
                    "4": "插在中間：兩邊都要花 O(n)。陣列花在搬移，串列花在從 head 走過去。只有已經拿著前一個節點時，串列的插入才是 O(1)。",
                    "8": "插在尾端：陣列容量夠就一步完成；這條串列沒有 tail 指標，要從 head 一路走到底。"}),
        dict(key="order", label="堆疊 vs 佇列", left="堆疊", right="佇列", stems=["linear_structures"],
             op="放入 A、B、C，再取出三次",
             note="操作次數完全相同，差別只在取出的那一端：堆疊是後進先出，佇列是先進先出。"),
        dict(key="search", label="循序 vs 二分搜尋", left="循序搜尋", right="二分搜尋", stems=["searching_sorting"],
             op="在同一個已排序陣列裡找同一個值",
             values=[3, 8, 11, 17, 20, 26, 31, 44, 54, 55, 62, 70, 77, 81, 93, 99],
             options=[dict(v=3, label="3"), dict(v=44, label="44"), dict(v=99, label="99"), dict(v=50, label="50（不存在）")], default=99,
             opt_label="要找的值",
             note="二分搜尋每比一次就排除一半，但前提是資料已排序；對未排序、也沒有建立索引的陣列，兩者之中只有循序搜尋能用。值就在最前面時，循序搜尋反而比較快。這裡的循序搜尋沒有利用排序，所以找不到時會看完全部；資料有序時，看到比目標大的值就能提早停止。"),
        dict(key="walk", label="BFS vs DFS", left="BFS（用佇列）", right="DFS（用堆疊）", stems=["graphs"],
             op="同一張圖、同一個起點 A，鄰居依字母順序",
             note="程式幾乎一樣，只差待處理清單是佇列還是堆疊：BFS 先處理最早發現的頂點，所以逐層擴散；DFS 先處理最新發現的頂點，所以一路走到底再回頭。"),
    ],
)
