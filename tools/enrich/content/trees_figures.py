"""Lecture figures for chapter 9 (trees.html), stored in assets/figures/ch9/."""
from html import escape

# fid: (file, display width, natural width, natural height, alt, caption)
_SPECS = {
    'biology': ('biology.png', 560, 1087, 731,
                '生物分類樹：根 Animalia 分成 Chordata 與 Arthropoda，往下依序是綱、目、科、屬、種，最底層是 Human、Chimpanzee、Cat、Lion、Housefly、Firebrat。左側標出 Kingdom 到 Species 七個層級。',
                '生物分類是一棵樹：越上層越一般，越下層越具體。從根 Animalia 一路往下，每一層回答一個問題（脊索動物還是節肢動物？哺乳類嗎？），走到底就是一個物種。到每個葉節點的路徑都是唯一的。'),
    'directory': ('directory.png', 720, 1563, 251,
                  '檔案系統樹：根目錄 / 底下有 dev/、etc/、sbin/、tmp/、Users/、usr/、var/，etc/ 底下有 cups/、httpd/、init.d/、postfix/，Users/、usr/、var/ 也各有子目錄。',
                  '檔案系統的目錄也是樹。從根 / 走到任何一個目錄的路徑就是它的路徑名稱，例如 /etc/httpd。把整棵 etc/ 子樹搬到 usr/ 底下，路徑變成 /usr/etc/httpd，但 httpd 目錄本身與它底下的內容都不受影響。'),
    'treedef1': ('treedef1.png', 360, 403, 281,
                 '方框表示的樹：root node 有 child1、child2 兩個欄位，分別指向 node1 與 node2；node1 有三個欄位指向 node3、node4、node5，node2 有一個欄位指向 node6。',
                 '定義一的例子：節點加上連接節點的有向邊。箭頭方向是 parent 指向 child；除了根以外，每個節點都恰好有一條進來的邊。這棵樹的 node1 有三個子節點，所以它不是二元樹。'),
    'TreeDefRecursive': ('TreeDefRecursive.png', 300, 362, 281,
                         '一個標示 root 的圓圈，往下連到三個三角形，分別標示 subtree 1、subtree 2、subtree 3。',
                         '定義二（遞迴定義）：一棵樹是空的，或由一個根加上零個以上的子樹組成，每個子樹本身也是一棵樹。這張圖的每個三角形都有自己的根，所以這棵樹（若非空）至少有四個節點。'),
    'treerecs': ('treerecs.png', 640, 2640, 1008,
                 '節點與參考的樹：key 為 "a" 的節點有兩個指標，分別指向 key "b" 與 key "c"；"b" 指向 "d" 與 "e"；"c" 的左指標指向 "f"，右指標是 NULL；"d"、"e"、"f" 的兩個指標都是 NULL。底部標示 BinaryTree* leftChild 與 BinaryTree* rightChild。',
                 '用節點與參考表示二元樹：每個 BinaryTree 物件存一個 key 和兩個 BinaryTree* 指標。指標不是 NULL 時就指向另一棵子樹；NULL 表示那一邊是空的。'),
    'nlParse': ('nlParse.png', 380, 545, 443,
                '句子 Lisa plays saxophone 的解析樹：Sentence 分成 Noun Phrase 與 Verb Phrase；Noun Phrase 經 Proper Noun 到 Lisa；Verb Phrase 分成 Verb（plays）與 Noun Phrase，後者經 Noun 到 saxophone。',
                '自然語言的解析樹：句子 Sentence 拆成名詞片語與動詞片語，再一路拆到單字。每個子樹對應句子的一個成分，可以單獨處理。'),
    'meParse': ('meParse.png', 300, 371, 251,
                '運算式樹：根是乘號，左子樹是 + 連著 7 和 3，右子樹是 - 連著 5 和 2。',
                '((7 + 3) * (5 - 2)) 的解析樹：運算子在內部節點，數字在葉節點。乘法在根，表示要先算出左右兩個子樹，才能做最後的乘法。'),
    'meSimple': ('meSimple.png', 150, 179, 155,
                 '簡化後的樹：根是乘號，兩個子節點是 10 和 3。',
                 '把算好的子樹換成一個節點：左子樹 7 + 3 換成 10，右子樹 5 - 2 換成 3，剩下 10 * 3。這就是遞迴求值的想法。'),
    'buildExp1': ('buildExp1.png', 62, 62, 62, '一個灰色的空節點。', '開始：只有一個空的根，它就是目前節點（灰色）。'),
    'buildExp2': ('buildExp2.png', 96, 96, 145, '白色的根，左下方接一個灰色的空節點。', '讀到 (：新增左子節點，往下移到它。'),
    'buildExp3': ('buildExp3.png', 97, 97, 145, '灰色的根，左子節點是 3。', '讀到 3：把目前節點設為 3，回到父節點。'),
    'buildExp4': ('buildExp4.png', 130, 130, 145, '根是 +，左子節點 3，右子節點是灰色的空節點。', '讀到 +：根設為 +，新增右子節點並往下移。'),
    'buildExp5': ('buildExp5.png', 130, 130, 228, '根 +，左 3；右子節點底下又接一個灰色的左子節點。', '讀到 (：在目前節點新增左子節點，往下移。'),
    'buildExp6': ('buildExp6.png', 130, 130, 228, '根 +，左 3；右子節點是灰色，它的左子節點是 4。', '讀到 4：設為 4，回到父節點。'),
    'buildExp7': ('buildExp7.png', 170, 170, 228, '根 +，左 3；右子節點是 *，它的左子節點 4，右子節點是灰色的空節點。', '讀到 *：設為 *，新增右子節點並往下移。'),
    'buildExp8': ('buildExp8.png', 169, 169, 228, '根 +，左 3；右子節點 * 是灰色，底下是 4 和 5。', '讀到 5：設為 5，回到 *。接著兩個 ) 再往上回到根，建樹完成。'),
    'booktree': ('booktree.png', 640, 938, 347,
                 '書的樹：Book 底下是 Chapter 1 與 Chapter 2；Chapter 1 底下是 Section 1.1 與 Section 1.2，Section 1.2 底下是 Section 1.2.1 與 Section 1.2.2；Chapter 2 底下是 Section 2.1 與 Section 2.2，Section 2.2 底下是 Section 2.2.1 與 Section 2.2.2。',
                 '一本書的章節結構：書是根，章是書的子節點，節是章的子節點。由前往後讀這本書的順序，正好就是前序走訪：先讀標題（根），再讀左邊整章，最後讀右邊整章。'),
    'compTree': ('compTree.png', 460, 559, 287,
                 '十個節點的二元樹：5 的子節點是 9 和 11，9 的子節點是 14 和 18，11 的子節點是 19 和 21，14 的子節點是 33 和 17，18 只有左子節點 27。',
                 '完全二元樹：除了最底層之外每一層都填滿，最底層由左往右填。這裡最底層只有 33、17、27，而且都靠左。'),
    'heapOrder': ('heapOrder.png', 460, 533, 377,
                  '同一棵樹，下方是一列陣列 5, 9, 11, 14, 18, 19, 21, 33, 17, 27，索引 0 到 9。',
                  '同一棵完全二元樹存進 vector：由上往下、由左往右依序編號。索引 p 的左子在 2p + 1、右子在 2p + 2，例如 9（索引 1）的子節點是 14（索引 3）與 18（索引 4）。每個父節點都不大於它的子節點，這就是堆積順序性質。'),
    'percUp1': ('percUp1.png', 480, 723, 358,
                '前面的 heap 在 18 的右子位置多了一個白色節點 7，旁邊標示 new item。',
                '插入 7：先放在 vector 的最後一格，也就是 18 的右子。結構性質還在，但 7 比父節點 18 小，順序性質被破壞。'),
    'percUp2': ('percUp2.png', 480, 730, 349,
                '7 與 18 交換位置，虛線箭頭標示 swap 1。',
                '第一次交換：7 小於 18，兩者交換，7 上浮一層。'),
    'percUp3': ('percUp3.png', 480, 723, 353,
                '7 與 9 交換，7 成為 5 的左子節點，標示 swap 2。',
                '第二次交換：7 小於父節點 9，再上浮一層。接著和 5 比較，7 不小於 5，停止。'),
    'percDown1': ('percDown1.png', 460, 667, 391,
                  '根 5 被移出，旁邊標示 remove min；虛線箭頭把最後一個節點 27 搬到空出來的根。',
                  'delMin 的第一步：取出根 5，再把最後一個元素 27 搬到根。這樣樹還是完全二元樹，但 27 太大，順序性質被破壞。'),
    'percDown2': ('percDown2.png', 460, 672, 348,
                  '根變成 9，27 下移到 9 原本的位置，標示 swap 1。',
                  '第一次下沉：27 的子節點是 9 和 11，和較小的 9 交換。'),
    'percDown3': ('percDown3.png', 460, 669, 339,
                  '27 再和 14 交換，標示 swap 2。',
                  '第二次下沉：27 的子節點是 14 和 18，和較小的 14 交換。'),
    'percDown4': ('percDown4.png', 460, 657, 336,
                  '27 和 17 交換，成為 17 的右子葉節點，標示 swap 3。',
                  '第三次下沉：子節點 33 和 17 中較小的是 17，交換後 27 成為葉節點，停止。'),
    'buildheap': ('buildheap.png', 560, 592, 210,
                  '四棵樹由箭頭連接：Initial Heap 是 9, 6, 5, 2, 3；i = 1 時 6 和 2 交換；i = 0 時 9 和 2 交換；最後 9 和 3 交換，得到根 2、子節點 3 和 5、葉節點 6 和 9。',
                  '對 [9, 6, 5, 2, 3] 做 buildHeap。從最後一個非葉節點 i = 1 開始：6 和較小的子節點 2 交換。接著 i = 0：9 和 2 交換後，9 還比子節點 3 大，再交換一次。結果是 [2, 3, 5, 6, 9]。'),
    'simpleBST': ('simpleBST.png', 300, 343, 285,
                  '二元搜尋樹：根 70，左子 31，右子 93；31 的左子是 14，14 的右子是 23；93 的左子 73，右子 94。每個節點畫成三格方框，左右格是指標。',
                  '依序插入 70, 31, 93, 94, 14, 23, 73 得到的 BST。任一節點左子樹的鍵都比它小，右子樹的鍵都比它大，例如 31 的左邊是 14 和 23。'),
    'bstput': ('bstput.png', 440, 488, 182,
               'BST：根 17，左子樹 5（2、16），右子樹 35（29、38），29 的右子是 33；17、35、29 塗成淺灰色，新節點 19 是黑色，用虛線接在 29 的左邊。',
               '插入 19：19 比 17 大往右，比 35 小往左，比 29 小往左，29 的左邊是空的，就放在那裡。淺灰色是途中比較過的節點，比較次數等於走過的層數。'),
    'bstdel1': ('bstdel1.png', 560, 742, 339,
                '左邊的 BST 中 16 是白色葉節點；箭頭右邊是刪掉 16 之後的樹，11 只剩左子 9。',
                '情況一：刪除葉節點 16。直接把父節點 11 的右指標設為 NULL，再釋放節點。'),
    'bstdel2': ('bstdel2.png', 560, 789, 339,
                '左邊的 BST 中 25 是白色，它只有右子 35（底下 29、38）；右邊的樹中 35 直接接在 17 的右邊。',
                '情況二：刪除只有一個子節點的 25。把它唯一的子節點 35 提上來接到 17，並更新 35 的 parent。'),
    'bstdel3': ('bstdel3.png', 560, 733, 414,
                '左邊的 BST 中 5 是白色，它有左子 2 和右子 11；虛線箭頭從 5 指向右子樹中最左的 7，標示 successor；右邊的樹中 5 的位置變成 7，8 接在 9 的左邊。',
                '情況三：刪除有兩個子節點的 5。後繼者是右子樹中最小的 7。先把 7 從原位置拆出（它的右子 8 接到 9），再把 7 的鍵和值複製到 5 的位置。'),
    'skewedTree': ('skewedTree.png', 230, 290, 254,
                   '一條往右下斜的鏈：10 的右子 20，20 的右子 30，30 的右子 40，40 的右子 50。',
                   '依序插入已排序的 10, 20, 30, 40, 50：每個新鍵都比前面的大，只能一直往右接，樹退化成一條鏈，高度是 n - 1。'),
    'unbalanced': ('unbalanced.png', 180, 227, 269,
                   '每個節點標著平衡因子：根 -2，左子 0，右子 -1；右子的左子 0、右子 -1；最下面的葉節點 0。',
                   '右重（right-heavy）的不平衡樹，節點上的數字是平衡因子（左子樹高度減右子樹高度）。根的平衡因子是 -2，超出 -1 到 1 的範圍，需要重新平衡。'),
    'worstAVL': ('worstAVL.png', 480, 519, 259,
                 '四棵左重的樹，高度 0 到 3：只有 A；B 接 A；C 接 B（下接 A）與 D；E 接 C（C 接 B、D，B 接 A）與 G（G 接 F）。每個節點標著平衡因子。',
                 '高度 0、1、2、3 時節點數最少的左重 AVL 樹，分別有 1、2、4、7 個節點。高度 h 的這種樹由根、一棵高度 h - 1 的最瘦樹與一棵高度 h - 2 的最瘦樹組成。'),
    'simpleunbalanced': ('simpleunbalanced.png', 400, 442, 221,
                         '左邊是 A（-2）的右子 B（-1），B 的右子 C（0）；箭頭右邊是 B（0）為根，左子 A（0），右子 C（0）。',
                         '最簡單的左旋：A 的平衡因子是 -2。把右子 B 提為新根，A 變成 B 的左子，三個節點都恢復平衡。'),
    'rightrotate1': ('rightrotate1.png', 480, 554, 281,
                     '左邊是 E（2）有左子 C（1）與右子 F（0），C 有左子 B（1）與右子 D（0），B 有左子 A（0）；右邊是 C（0）為根，左子 B（1，下接 A），右子 E（0，下接 D 和 F）。',
                     '右旋：E 的平衡因子是 2。把左子 C 提為新根，E 變成 C 的右子；C 原本的右子 D 改接成 E 的左子。BST 的大小順序沒有改變。'),
    'bfderive': ('bfderive.png', 420, 449, 189,
                 '左邊 B 的左子樹是三角形 A，右子是 D，D 底下是三角形 C 和 E；箭頭右邊 D 為根，左子 B（底下 A、C），右子樹 E。',
                 '左旋的一般形狀：B 是旋轉前的根，D 是它的右子；A、C、E 是整棵搬動的子樹。旋轉後只有 B 和 D 的子樹改變，所以只需要更新這兩個節點的平衡因子。'),
    'hardunbalanced': ('hardunbalanced.png', 100, 110, 222,
                       'A（-2）的右子是 C（1），C 的左子是 B（0）。',
                       'A 的平衡因子是 -2，但右子 C 是左重。'),
    'badrotate': ('badrotate.png', 100, 111, 237,
                  'C（2）的左子是 A（-1），A 的右子是 B（0）。',
                  '直接左旋 A 的結果：C 的平衡因子變成 2，往另一邊不平衡。'),
    'rotatelr': ('rotatelr.png', 480, 533, 210,
                 '三棵樹：A（-2）右子 C（1）、C 左子 B；先右旋 C 得到 A（-2）右子 B（-1）、B 右子 C；再左旋 A 得到 B 為根、A 和 C 為子節點，平衡因子都是 0。',
                 '雙旋轉：先對右子 C 做右旋，把形狀變成一條往右的鏈，再對 A 做左旋，整棵子樹恢復平衡。'),
}

FIGURES = {fid: {'file': f, 'width': w, 'height': round(w * nh / nw), 'alt': alt, 'caption': cap}
           for fid, (f, w, nw, nh, alt, cap) in _SPECS.items()}


def _img(fid):
    spec = FIGURES[fid]
    alt = escape(spec['alt'], quote=True)
    return (f'<img src="assets/figures/ch9/{spec["file"]}" alt="{alt}" width="{spec["width"]}" '
            f'height="{spec["height"]}" style="--figure-width:{spec["width"]}px" loading="lazy">')


def figure(fid):
    spec = FIGURES[fid]
    alt = escape(spec['alt'], quote=True)
    return (f'<figure class="tree-figure" id="tree-figure-{fid}">'
            f'<div class="tree-figure-scroll" tabindex="0" role="region" aria-label="{alt}">{_img(fid)}</div>'
            f'<figcaption>{escape(spec["caption"], quote=False)}</figcaption></figure>')


def figrow(fids, caption, label):
    """Several small figures side by side; each keeps its own short caption, plus one shared caption."""
    cells = ''.join(f'<div class="tree-figrow-cell">{_img(f)}<span>{escape(FIGURES[f]["caption"], quote=False)}</span></div>'
                    for f in fids)
    return (f'<figure class="tree-figure tree-figrow" id="tree-figure-{fids[0]}">'
            f'<div class="tree-figure-scroll tree-figrow-cells" tabindex="0" role="region" aria-label="{escape(label, quote=True)}">'
            f'{cells}</div><figcaption>{escape(caption, quote=False)}</figcaption></figure>')


STYLE = '''<style id="trees-figures-style">
.tree-figure{margin:1rem 0 1.4rem;max-width:100%;}
.tree-figure-scroll{max-width:100%;overflow-x:auto;background:#fff;border:1px solid var(--card-border);border-radius:8px;padding:.4rem 0;}
.tree-figure img{display:block;height:auto;max-width:100%;width:var(--figure-width);margin:0 auto;}
.tree-figure figcaption{margin-top:.65rem;font-size:.9rem;line-height:1.8;color:var(--ink);}
.tree-figrow-cells{display:flex;flex-wrap:wrap;gap:1rem;justify-content:center;align-items:flex-end;padding:.6rem;}
.tree-figrow-cell{display:flex;flex-direction:column;align-items:center;gap:.4rem;max-width:200px;}
.tree-figrow-cell img{margin:0;}
.tree-figrow-cell span{font-size:.8rem;line-height:1.5;color:var(--ink);text-align:center;}
</style>'''
