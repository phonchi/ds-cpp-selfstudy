"""Chapter 9 (trees.html) section bodies. Each value of sections() fills one <!-- gen:NAME --> block.

The hand-written part of every section (widgets, explanations) lives in trees_legacy.py; it carries
{{slot:NAME}} tokens where the lecture material below is inserted. Lecture text and code follow
09_Trees and Tree Algorithms.ipynb and the course headers binarytree.hpp, binaryheap.hpp and bst.hpp.
Expected outputs come from compiling the programs (trees_programs.OUT).
"""
import re
from html import escape
from enrich_lib import hl
from content.trees_figures import figure, figrow
from content.trees_programs import RUN, OUT, EX2_BLANK, EX3_BLANK
from content.trees_legacy import LEGACY
from content.trees_quizzes import LECTURE_QUIZ


# ---------------------------------------------------------------- helpers (chapter 3/4/7 conventions)
def details(summary, body, cls='tree-detail', did=''):
    ident = f' id="{did}"' if did else ''
    return f'<details class="{cls}"{ident}><summary>{summary}</summary><div class="tree-detail-body">{body}</div></details>'


def fold(title, body, did=''):
    """Content that the lecture does not cover: collapsed and labelled （補充）."""
    return details(title + '（補充）', body, did=did)


def steps(title, fids, note=''):
    """Further frames of a step-by-step figure sequence, collapsed."""
    return details('逐步圖：' + title, (f'<p>{note}</p>' if note else '') + ''.join(figure(f) for f in fids))


def table(headers, rows):
    return ('<div class="table-scroll" tabindex="0" aria-label="表格，可左右捲動"><table class="cmp-table"><thead><tr>'
            + ''.join(f'<th>{h}</th>' for h in headers) + '</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{v}</td>' for v in r) + '</tr>' for r in rows)
            + '</tbody></table></div>')


def quiz(key, label='QUIZ'):
    """A lecture quiz in this page's sq-item markup (the page script binds every .sq-item)."""
    q = LECTURE_QUIZ[key]
    assert len(q['answers']) == 4 and sum(a['correct'] for a in q['answers']) == 1, key
    opts = '\n'.join(
        f'      <button class="sq-opt" data-c="{1 if a["correct"] else 0}" data-fb="{escape(a["feedback"], quote=True)}">'
        f'{escape(a["answer"], quote=False)}</button>' for a in q['answers'])
    return (f'<div class="sq-item tree-quiz" id="quiz-{key}">\n    <div class="sq-q"><span class="sq-num">{label}</span>'
            f'{escape(q["question"], quote=False)}</div>\n    <div class="sq-opts">\n{opts}\n    </div>\n'
            f'    <div class="sq-fb"></div>\n  </div>')


def _expected_attr(stdout):
    return ' data-expected="' + escape(stdout, quote=True).replace('\n', '&#10;') + '"'


def _expected_out(stdout, label='預期輸出'):
    return (f'<div class="expected-out"><span class="eo-tag">{label}</span><pre>'
            + escape(stdout.rstrip('\n')) + '</pre></div>')


def code(code_text, kind, stdout=None):
    attrs = f' data-cpp="{kind}"' + (_expected_attr(stdout) if kind == 'run' else '')
    return f'  <div class="pseudo-code" style="font-size:.8rem;"{attrs}>{hl(code_text)}</div>'


def card(label, code_text, kind='fragment', stdout=None, note=None, out_label='預期輸出', show_out=False):
    parts = ['<div class="deck-extra">', f'  <div class="dx-label">{label}</div>', code(code_text, kind, stdout)]
    if show_out:
        parts.append('  ' + _expected_out(stdout, out_label))
    if note:
        parts.append(f'  <p class="dx-note">{note}</p>')
    parts.append('</div>')
    return '\n'.join(parts)


def snip(label, code_text, **kw):
    """Lecture slide code: collapsed so the explanation stays readable; the label says what it holds."""
    return details('程式：' + label, card(label, code_text, **kw))


def program(summary, label, key, note=None, out_label='預期輸出'):
    """Lecture program: code collapsed, the output and note visible."""
    out = _expected_out(OUT[key], out_label)
    if note:
        out += f'<p class="dx-note">{note}</p>'
    return details(summary, card(label, RUN[key], kind='run', stdout=OUT[key])) + out


def exercise(label, blank, solution_key, solution_label, extra='', start_key=None):
    """Lecture exercise: the fill-in program stays visible; the answer is collapsed.
    A starter that already compiles (start_key) is a run block with its current output shown."""
    if start_key:
        ex = card(label, RUN[start_key], kind='run', stdout=OUT[start_key], show_out=True, out_label='起始程式的輸出')
    else:
        ex = card(label, blank, kind='exercise')
    sol = card(solution_label, RUN[solution_key], kind='run', stdout=OUT[solution_key],
               show_out=True, out_label='解答的輸出')
    return ex + details('看解答', extra + sol)


def ul(items, cls='tree-ul'):
    return f'<ul class="{cls}">' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'


def fill(sid, slots, tail=''):
    """Insert the lecture material into the hand-written section body."""
    body = LEGACY[sid]
    for name, html in slots.items():
        token = '{{slot:' + name + '}}'
        assert body.count(token) == 1, (sid, name)
        body = body.replace(token, html)
    left = re.findall(r'\{\{slot:[^}]+\}\}', body)
    assert not left, (sid, left)
    return body.rstrip('\n') + ('\n' + tail if tail else '')


INCLUDE_TREE = '#include "pythonds3/cppds/binarytree.hpp"'
VISUALGO_HEAP = '<a href="https://visualgo.net/en/heap" target="_blank" rel="noopener">VisuAlgo 的 heap 動畫</a>'
VISUALGO_BST = '<a href="https://visualgo.net/en/bst" target="_blank" rel="noopener">VisuAlgo 的 BST 動畫</a>'


# ---------------------------------------------------------------- P00 examples
def prologue():
    examples = f'''<h3>兩個例子：生物分類與檔案系統</h3>
<p>電腦科學裡的樹有根（root）、分支（branch）與葉（leaf），只是畫法和自然界的樹相反：根在最上面，葉在最下面。第一個例子是生物分類樹。</p>
{figure('biology')}
<p>這個例子說明樹是<strong>階層式</strong>（hierarchical）的：越上層越一般，越下層越具體。從最上層的界（kingdom）往下，依序是門、綱、目、科、屬、種。每往下一層，就回答一個問題，選擇符合答案的那條路徑。</p>
<p>從這個例子還能看出樹的另外兩個性質：</p>
{ul(['一個節點的子節點，和另一個節點的子節點互不相干。例如 Felidae 底下的 Felis，和 Muscidae 底下的 Musca 沒有關係。',
     '從根到每個葉節點的路徑都是唯一的。例如 Animalia → Chordata → Mammalia → Carnivora → Felidae → Felis → catus 唯一地指出家貓。'])}
<p>第二個例子是每天都會用到的檔案系統。目錄（資料夾）組成一棵樹，從根目錄走到任何一個子目錄的路徑，就是它唯一的路徑名稱。</p>
{figure('directory')}'''
    return fill('prologue', {'examples': examples})


# ---------------------------------------------------------------- P01 vocabulary
def vocabulary():
    terms = f'''<h3>名詞定義</h3>
{table(['術語', '意義'], [
        ['節點（node）', '樹的基本組成。節點有一個名稱，稱為<strong>鍵</strong>（key）；也可以存放其他資料，稱為值（value）或酬載（payload）。'],
        ['邊（edge）', '連接兩個節點，表示它們之間有關係。除了根以外，每個節點都<strong>恰好有一條</strong>從別的節點進來的邊；出去的邊可以有好幾條。'],
        ['根（root）', '樹中唯一沒有進來的邊的節點。'],
        ['路徑（path）', '由邊連起來的一串有順序的節點，例如 Mammalia → Carnivora → Felidae → Felis → catus。'],
        ['子節點（children）', '從同一個節點出發、經由邊連到的那些節點，是該節點的子節點。'],
        ['父節點（parent）', '一個節點是它用出去的邊連到的所有節點的父節點。'],
        ['兄弟節點（sibling）', '有同一個父節點的節點。檔案系統裡的 etc/ 和 usr/ 是兄弟節點。'],
        ['子樹（subtree）', '一個父節點與它所有子孫，連同之間的邊。'],
        ['葉節點（leaf node）', '沒有子節點的節點。'],
        ['層（level）', '從根走到節點 $n$ 的路徑上的邊數。根在第 0 層。'],
        ['高度（height）', '樹中所有節點的最大層數。只有一個節點的樹高度是 0。'],
    ])}'''
    defs = f'''<p>定義一的圖：方框是節點，箭頭是邊，箭頭方向表示連接的方向（從 parent 指向 child）。</p>
{figure('treedef1')}
<p>定義二是遞迴的：每個三角形代表一棵子樹，子樹的根用一條邊接到上層的根。</p>
{figure('TreeDefRecursive')}
{quiz('tree')}'''
    return fill('vocabulary', {'terms': terms, 'defs': defs})


# ---------------------------------------------------------------- P02 Tree ADT
def tree_adt():
    usage = '''BinaryTree r("a");                      // a node with two NULL children
r.insertLeft("b");                      // attach a new left child
r.insertRight("c");                     // attach a new right child
r.getLeftChild()->setRootVal("hello");  // change the value of the left child
cout << r.getRightChild()->getRootVal() << endl;'''
    return f'''<p>有了術語之後，接著定義要用哪些操作來建立與操作一棵二元樹。這組操作就是二元樹的抽象資料型別（ADT）。</p>
<h3>操作清單</h3>
{table(['操作', '作用'], [
        ['<code>BinaryTree(root)</code>', '建立一個節點，值是 <code>root</code>，兩個子指標都是 <code>NULL</code>。'],
        ['<code>getRootVal()</code>／<code>setRootVal(value)</code>', '讀取或替換目前節點的值。'],
        ['<code>getLeftChild()</code>／<code>getRightChild()</code>', '回傳左、右子樹的指標；那一邊是空的時候回傳 <code>NULL</code>。'],
        ['<code>insertLeft(value)</code>／<code>insertRight(value)</code>', '配置一個新節點接成左（右）子節點；原本已經有子節點時，把它往下推一層（下一節說明）。'],
    ])}
<p><code>getLeftChild()</code> 回傳的是一整棵子樹（<code>BinaryTree*</code>），所以可以接著用 <code>-&gt;</code> 呼叫子樹的操作，一路往下走到任何深度。</p>
{snip('Tree ADT 的呼叫方式', usage)}
<h3>從介面到實作</h3>
<p>實作一棵樹時，最關鍵的決定是內部要用什麼方式儲存。本課程使用<strong>節點與參考</strong>（nodes and references）：每個節點是一個物件，用指標連到它的子樹。下一節就用這個方式寫出 <code>BinaryTree</code> 類別。</p>'''


# ---------------------------------------------------------------- P03 nodes and references
CLASS = '''class BinaryTree {
    public:
        string key;
        BinaryTree* leftChild;
        BinaryTree* rightChild;

        BinaryTree(string rootObj) {
            key = rootObj;
            leftChild = NULL;
            rightChild = NULL;
        }
};'''

INSERT = '''void insertLeft(string newNode) {
    if (leftChild == NULL) {
        leftChild = new BinaryTree(newNode);
    } else {
        BinaryTree* newChild = new BinaryTree(newNode);
        newChild->leftChild = leftChild;
        leftChild = newChild;
    }
}

void insertRight(string newNode) {
    if (rightChild == NULL) {
        rightChild = new BinaryTree(newNode);
    } else {
        BinaryTree* newChild = new BinaryTree(newNode);
        newChild->rightChild = rightChild;
        rightChild = newChild;
    }
}'''

ACCESSORS = '''string getRootVal() {
    return key;
}
void setRootVal(string newKey) {
    key = newKey;
}
BinaryTree* getLeftChild() {
    return leftChild;
}
BinaryTree* getRightChild() {
    return rightChild;
}'''


def nodes_refs():
    cls = f'''<h3>BinaryTree 類別</h3>
<p>用節點與參考表示一棵樹時，定義一個類別，存放根的值以及左、右子樹。下圖的六個標籤就是六個 <code>BinaryTree</code> 物件，靠子指標連在一起。</p>
{figure('treerecs')}
<p>在 C++ 裡，<code>leftChild</code> 與 <code>rightChild</code> 是指向其他 <code>BinaryTree</code> 物件的指標；<code>NULL</code> 表示那一邊是空的子樹。節點的值可以是任何型別，這個教學版本用 <code>string</code>。</p>
{snip('BinaryTree 的資料成員與建構子', CLASS)}
<h3>insertLeft 與 insertRight</h3>
<p>要加左子節點，就配置一個新的 <code>BinaryTree</code>，把位址存進 <code>leftChild</code>。插入分兩種情況：原本沒有左子節點時，直接接上；原本已經有左子節點時，新節點插在中間，原本的左子樹變成新節點的左子樹，等於被往下推一層。<code>insertRight</code> 對稱地處理右邊。</p>
{snip('insertLeft 與 insertRight', INSERT)}
<p>最後補上讀取子樹與讀寫根值的函式，一個簡單的二元樹類別就完成了。</p>
{snip('存取函式', ACCESSORS)}
<p>下面的動畫用這些函式一步一步長出一棵樹。</p>'''
    run = f'''<h3 id="dx-voc">實際執行：建立根 a 與子節點 b、c</h3>
<p>完整的類別在 <code>pythonds3/cppds/binarytree.hpp</code>。下面的程式建立根 <code>"a"</code>，再加上左子 <code>"b"</code> 與右子 <code>"c"</code>，最後把右子的值改成 <code>"hello"</code>。</p>
{program('講義完整程式：BinaryTree 的基本操作', '講義 09 · BinaryTree', 'binarytree',
         note='第二行的 0 是空的左子指標：<code>NULL</code> 用 <code>cout</code> 印出來就是 0。<code>getRightChild()</code> 回傳整棵右子樹，所以能接著呼叫 <code>setRootVal</code> 修改它。')}'''
    return fill('nodes-refs', {'class': cls, 'run': run,
                               'lol': fold('List of Lists：Python 的巢狀串列表示', LEGACY['lol'].rstrip('\n'))})


# ---------------------------------------------------------------- P04 parse tree
BUILD = '''BinaryTree* buildParseTree(string fpExpr) {
    stack<BinaryTree*> pStack;
    BinaryTree* exprTree = new BinaryTree("");
    pStack.push(exprTree);
    BinaryTree* currentTree = exprTree;

    stringstream ss(fpExpr);
    string i;
    while (ss >> i) {
        if (i == "(") {
            currentTree->insertLeft("");
            pStack.push(currentTree);
            currentTree = currentTree->getLeftChild();
        } else if (i == "+" || i == "-" || i == "*" || i == "/") {
            currentTree->setRootVal(i);
            currentTree->insertRight("");
            pStack.push(currentTree);
            currentTree = currentTree->getRightChild();
        } else if (i == ")") {
            currentTree = pStack.top();
            pStack.pop();
        } else {
            currentTree->setRootVal(i);   // a number
            currentTree = pStack.top();
            pStack.pop();
        }
    }
    return exprTree;
}'''

EVAL = '''double evaluate(BinaryTree* parseTree) {
    BinaryTree* leftChild = parseTree->getLeftChild();
    BinaryTree* rightChild = parseTree->getRightChild();

    if (leftChild != NULL && rightChild != NULL) {
        string op = parseTree->getRootVal();
        if (op == "+") return evaluate(leftChild) + evaluate(rightChild);
        if (op == "-") return evaluate(leftChild) - evaluate(rightChild);
        if (op == "*") return evaluate(leftChild) * evaluate(rightChild);
        return evaluate(leftChild) / evaluate(rightChild);
    } else {
        return stod(parseTree->getRootVal());   // a leaf: a number
    }
}'''


def parse_tree():
    intro = f'''<h3>句子與運算式都能畫成樹</h3>
<p><strong>解析樹</strong>（parse tree）可以表示句子或數學運算式這類有結構的東西。下圖是一個簡單句子的階層結構；把句子表示成樹之後，就能用子樹分別處理句子的各個部分。</p>
{figure('nlParse')}'''
    tree = f'''{figure('meParse')}
<p>乘法的優先順序比加法、減法高，但因為括號，乘法之前必須先算出括號裡的加法與減法。樹的階層正好表達了這個順序：要算根的乘法，得先算出左子樹（7 + 3 = 10）與右子樹（5 - 2 = 3）。算完的子樹可以整棵換成一個節點：</p>
{figure('meSimple')}
<p>接下來要處理三件事：</p>
{ul(['從完全括號化的運算式建立解析樹。', '計算解析樹所代表的運算式的值。', '從解析樹還原原本的運算式。'])}
<h3>建樹的四條規則</h3>
<p>第一步是把運算式切成 token，存成 <code>vector&lt;string&gt;</code>。token 有四種：左括號、右括號、運算子、運算元。讀到左括號表示開始一個新的子運算式，所以要建立一個新節點；讀到右括號表示一個子運算式結束。運算元一定是葉節點，運算子一定有左右兩個子節點。由此得到四條規則：</p>
<ol class="tree-ul">
<li>目前 token 是 <code>(</code>：在目前節點新增一個左子節點，往下移到這個左子節點。</li>
<li>目前 token 是 <code>+</code>、<code>-</code>、<code>*</code>、<code>/</code> 之一：把運算子存進目前節點，新增一個空的右子節點，往下移到右子節點。</li>
<li>目前 token 是數字：把目前節點的值設為這個數字，回到父節點。</li>
<li>目前 token 是 <code>)</code>：回到目前節點的父節點。</li>
</ol>
<p>以 $(3 + (4 * 5))$ 為例，切出的 token 是 <code>{{"(", "3", "+", "(", "4", "*", "5", ")", ")"}}</code>。從一個空的根開始，一次套用一條規則。下圖的灰色節點是目前節點：</p>
{figrow(['buildExp1', 'buildExp2', 'buildExp3'], '前三個 token：(、3、+ 之前的狀態。讀 ( 往左下走，讀 3 填值後回到根。', '建樹的前三步')}
{details('逐步圖：讀入 +、(、4、*、5', figrow(['buildExp4', 'buildExp5', 'buildExp6', 'buildExp7', 'buildExp8'], '每讀一個 token 就套用一條規則。最後的兩個 ) 只是往上回到父節點：先回到 +，+ 已經沒有父節點，建樹完成。', '建樹的後五步'))}'''
    build = f'''<h3>buildParseTree</h3>
<p>四條規則就是程式中 <code>if</code>／<code>else if</code> 的四個分支。往下走到子節點用 <code>getLeftChild()</code>、<code>getRightChild()</code>；回到父節點則靠 <code>pStack</code>：往下走之前先把目前節點 push，要回去時再 pop。</p>
{snip('buildParseTree（binarytree.hpp）', BUILD)}
<p>這個教學版本假設輸入格式正確，而且 token 之間以空白分隔。實際使用的解析器遇到既不是括號、也不是運算子或數字的 token 時，應該丟出 <code>invalid_argument</code>。</p>
{program('講義完整程式：建立解析樹並以中序印出', '講義 09 · buildParseTree', 'parse_inorder',
         note='<code>inorder</code> 依「左子樹、根、右子樹」的順序印出節點，下一節會說明。印出的運算式少了括號。')}'''
    ev = f'''<h3>evaluate：遞迴求值</h3>
<p>建好解析樹之後，可以利用樹的階層性質，<strong>遞迴地計算每一棵子樹</strong>來求出整個運算式的值。</p>
<p>樹的遞迴演算法常用葉節點當作 base case。解析樹的葉節點一定是運算元，數字不需要再處理，直接回傳葉節點存的值即可。遞迴步驟是對左右兩個子節點呼叫 <code>evaluate</code>，每次呼叫都往葉節點靠近一層。最後把兩個遞迴呼叫的結果，用父節點存的運算子合起來。</p>
{snip('evaluate（binarytree.hpp）', EVAL)}
<p>運算子存成 <code>string</code>，用 <code>if</code>／<code>else if</code> 決定要做哪一種運算；也可以改用字元和 <code>switch</code>。</p>
{program('講義完整程式：evaluate', '講義 09 · evaluate', 'evaluate',
         note='在根節點，<code>evaluate()</code> 看到 <code>+</code>：左子樹是葉節點，回傳 3；右子樹的 <code>*</code> 把葉節點 4 和 5 相乘得到 20。最後根回傳 3 + 20 = 23。')}'''
    return fill('parse-tree', {'intro': intro, 'tree': tree, 'build': build, 'eval': ev})


# ---------------------------------------------------------------- P05 traversals
PREORDER = '''void preorder(BinaryTree* tree) {
    if (tree != NULL) {
        cout << tree->getRootVal() << " ";
        preorder(tree->getLeftChild());
        preorder(tree->getRightChild());
    }
}'''

PREORDER_MEMBER = '''void preorder() {   // a member function of BinaryTree
    cout << key << endl;
    if (leftChild != NULL) {
        leftChild->preorder();
    }
    if (rightChild != NULL) {
        rightChild->preorder();
    }
}'''

POSTORDER = '''void postorder(BinaryTree* tree) {
    if (tree != NULL) {
        postorder(tree->getLeftChild());
        postorder(tree->getRightChild());
        cout << tree->getRootVal() << " ";
    }
}'''

POSTORDEREVAL = '''double postordereval(BinaryTree* tree) {
    if (tree == NULL) return 0;
    if (tree->getLeftChild() != NULL && tree->getRightChild() != NULL) {
        double result1 = postordereval(tree->getLeftChild());
        double result2 = postordereval(tree->getRightChild());
        string op = tree->getRootVal();
        if (op == "+") return result1 + result2;
        if (op == "-") return result1 - result2;
        if (op == "*") return result1 * result2;
        return result1 / result2;
    }
    return stod(tree->getRootVal());
}'''

INORDER = '''void inorder(BinaryTree* tree) {
    if (tree != NULL) {
        inorder(tree->getLeftChild());
        cout << tree->getRootVal() << " ";
        inorder(tree->getRightChild());
    }
}'''

PRINTEXP = '''string printExp(BinaryTree* tree) {
    string result = "";
    if (tree != NULL) {
        result = "(" + printExp(tree->getLeftChild());
        result = result + tree->getRootVal();
        result = result + printExp(tree->getRightChild()) + ")";
    }
    return result;
}'''


def traversals():
    book = f'''<h3>前序走訪：從頭到尾讀一本書</h3>
<p>先用一本書當例子。書是樹的根，每一章是根的子節點，每一節是章的子節點，小節又是節的子節點。</p>
{figure('booktree')}
<p>想從頭到尾讀完這本書，前序走訪的順序就是閱讀順序：從根 Book 開始，遞迴走左子樹 Chapter 1，再遞迴走它的左子樹 Section 1.1。Section 1.1 沒有子節點，回到 Chapter 1，接著走右子樹 Section 1.2，依序讀 Section 1.2.1、Section 1.2.2。Chapter 1 讀完後回到 Book，再用同樣的方式讀 Chapter 2。</p>
<p>寫成外部函式的前序走訪很簡潔：base case 只有 <code>tree == NULL</code>；否則先印出根，再遞迴走左子樹與右子樹。對前面的解析樹，它印出 <code>+ 3 * 4 5</code>，也就是運算式的前序（prefix）形式。</p>
{snip('preorder（binarytree.hpp）', PREORDER)}
{program('講義的書本樹：以 BinaryTree 建立並做前序走訪', '書本樹的前序走訪', 'book',
         note='輸出就是閱讀順序。下方動畫選「講義：書的章節樹」，可以一步一步看這個順序與呼叫堆疊。')}
<h3>成員函式版與外部函式版</h3>
<p><code>preorder</code> 也可以寫成 <code>BinaryTree</code> 的成員函式，作用在 <code>this</code> 上。這時候不能對 <code>NULL</code> 呼叫成員函式，所以遞迴之前要先檢查 <code>leftChild</code>、<code>rightChild</code> 是不是 <code>NULL</code>：</p>
{snip('preorder 的成員函式版（課程標頭沒有收錄）', PREORDER_MEMBER)}
<p>這個例子比較適合寫成外部函式。很少有人只想把樹走一遍，通常是要在走訪的同時完成別的工作；外部函式比較容易改寫成其他用途。下一個例子會看到，後序走訪的寫法和前面計算解析樹的 <code>evaluate</code> 幾乎一樣，所以其餘的走訪都寫成外部函式。</p>'''
    code_html = f'''<h3>後序走訪與 postordereval</h3>
<p>後序走訪和前序只差在印出根的位置：先遞迴走完左右子樹，最後才印根。對解析樹，它印出 <code>3 4 5 * +</code>，也就是後序（postfix）形式。</p>
{snip('postorder（binarytree.hpp）', POSTORDER)}
<p>後序走訪的常見用途就是計算解析樹。假設樹裡只存運算式，照著後序走訪的骨架重寫求值函式：</p>
{snip('postordereval（binarytree.hpp）', POSTORDEREVAL)}
<p>和 <code>postorder</code> 相比，差別只在最後不是印出鍵，而是<strong>回傳</strong>值。兩個遞迴呼叫的回傳值存在 <code>result1</code>、<code>result2</code>，再用根的運算子合起來。</p>
<h3>中序走訪</h3>
<p>中序走訪先走左子樹，再拜訪根，最後走右子樹。對解析樹，它印出 <code>3 + 4 * 5</code>，是熟悉的中序（infix）形式，但少了括號。</p>
{snip('inorder（binarytree.hpp）', INORDER)}
{program('講義的走訪函式：對解析樹做三種走訪與 postordereval', '三種走訪與 postordereval', 'traversals',
         note='前序得到 prefix、中序得到 infix、後序得到 postfix；<code>postordereval</code> 依後序的順序計算，結果和 <code>evaluate</code> 一樣是 23。')}'''
    ex1_extra = ('<p>葉節點的左右子樹都是 <code>NULL</code>。在加括號之前先檢查這件事，葉節點就直接回傳數字本身；'
                 '其他節點照原本的方式在兩側加括號。</p>')
    printexp = f'''<h3>printExp：還原完整括號</h3>
<p>對解析樹做一般的中序走訪，得到的運算式沒有括號。稍微修改中序走訪的骨架，就能還原完整括號的版本：在遞迴走左子樹之前印左括號，走完右子樹之後印右括號。</p>
{snip('printExp（binarytree.hpp）', PRINTEXP)}
{program('講義完整程式：printExp', '講義 09 · printExp', 'printexp',
         note='每一棵子樹都包了一層括號，連只有一個數字的葉節點也被包起來，例如 <code>(3)</code>。')}
{quiz('traversal')}
<h3 id="ex-printexp2">練習 1：葉節點不要加括號</h3>
<p>修改 <code>printExp</code>，讓葉節點的數字不要被括號包住。目標是印出 <code>(3+(4*5))</code>，而不是 <code>((3)+((4)*(5)))</code>。下面的起始程式可以直接執行，目前輸出的還是多餘括號的版本。</p>
{exercise('練習 1 起始程式（printExp2）', None, 'ex1', '練習 1 解答', extra=ex1_extra, start_key='ex1_start')}'''
    return fill('traversals', {'book': book, 'code': code_html, 'printexp': printexp})



# ---------------------------------------------------------------- P06 binary heap
HEAP_SHELL = '''class BinaryHeap {
    public:
        vector<int> heap;   // the complete tree, stored flat

        BinaryHeap() {}
        bool isEmpty() {
            return heap.empty();
        }
};'''

PERCUP = '''void percUp(int i) {
    while (i > 0) {
        int parentIdx = (i - 1) / 2;
        if (heap[i] < heap[parentIdx]) {
            swap(heap[i], heap[parentIdx]);
        } else {
            break;
        }
        i = parentIdx;
    }
}

void insert(int item) {
    heap.push_back(item);
    percUp(heap.size() - 1);
}'''

PERCDOWN = '''void percDown(int i) {
    while (2 * i + 1 < (int)heap.size()) {
        int smChild = getMinChild(i);
        if (heap[i] > heap[smChild]) {
            swap(heap[i], heap[smChild]);
        } else {
            break;
        }
        i = smChild;
    }
}

int getMinChild(int i) {
    if (2 * i + 2 > (int)heap.size() - 1) {
        return 2 * i + 1;
    }
    if (heap[2 * i + 1] < heap[2 * i + 2]) {
        return 2 * i + 1;
    }
    return 2 * i + 2;
}

int delet() {   // legacy name; delete is a C++ keyword
    if (heap.empty()) throw underflow_error("empty heap");
    swap(heap[0], heap.back());
    int result = heap.back();
    heap.pop_back();
    if (!heap.empty()) percDown(0);
    return result;
}

int delMin() { return delet(); }'''

HEAPIFY_CODE = '''void heapify(vector<int> notAHeap) {
    heap = notAHeap;               // copy the vector
    int i = heap.size() / 2 - 1;   // last non-leaf node
    while (i >= 0) {
        percDown(i);
        i = i - 1;
    }
}'''


def heap():
    ops = f'''<p>binary heap 畫出來像一棵完全二元樹，實際上存在一個 <code>vector</code> 裡；在最小堆積（min-heap）中，最小的鍵在索引 0。插入與刪除都是 $O(\\log n)$，讀取最小值是 $O(1)$。</p>
<h3 id="dx-hp">BinaryHeap 的操作</h3>
{table(['操作', '作用'], [
        ['<code>BinaryHeap()</code>', '建立空的最小堆積。'],
        ['<code>insert(k)</code>', '插入一個鍵，$O(\\log n)$。'],
        ['<code>findMin()</code>', '回傳最小值但不移除，$O(1)$。'],
        ['<code>delMin()</code>', '移除並回傳最小值，$O(\\log n)$。舊版的課程程式把同一個操作叫做 <code>delet()</code>。'],
        ['<code>isEmpty()</code>、<code>size()</code>', '回報堆積是否為空、有幾個元素。'],
        ['<code>buildHeap(values)</code>', '由下往上一次建好整個堆積，$O(n)$。<code>heapify(values)</code> 是保留下來的同義舊名。'],
    ])}
{program('講義完整程式：插入 5、7、3、11 再逐一取出', '講義 09 · BinaryHeap', 'heap_basic',
         note='不管以什麼順序插入，每次取出的都是目前最小的值。')}'''
    figs = f'''<h3>完全二元樹與 vector 表示法</h3>
<p>為了保證對數時間，樹必須保持<strong>平衡</strong>：根的左右子樹節點數大致相同。堆積用<strong>完全二元樹</strong>（complete binary tree）來維持平衡：除了最底層之外每一層都填滿，最底層由左往右填。</p>
{figure('compTree')}
<p>完全二元樹可以存在一個 <code>vector</code> 裡，不需要節點指標。索引從 0 開始時，索引 $p$ 的左子在 $2p+1$、右子在 $2p+2$；非根節點 $i$ 的父節點，在 C++ 中用整數除法 <code>(i - 1) / 2</code> 算出。</p>
{figure('heapOrder')}
<p>堆積存放資料的方式依靠<strong>堆積順序性質</strong>（heap order property）：每個節點 $x$ 與它的父節點 $p$，$p$ 的鍵小於或等於 $x$ 的鍵。上圖的樹也滿足這個性質。因為樹的形狀完全由索引決定，類別只需要一個資料成員：</p>
{snip('BinaryHeap 的資料成員', HEAP_SHELL)}
<p>下面的動畫一開始就是圖中的 heap。用「講義」那一列按鈕可以直接載入插入 7、delMin 與 buildHeap 三個例子。</p>'''
    perc = f'''<h3>insert 與 percUp</h3>
<p>插入時先把新元素接在 <code>vector</code> 的尾端，這樣仍然是完全二元樹，結構性質不變。但新元素可能比父節點小，破壞順序性質。這時拿它和父節點比較，比父節點小就交換，一路往上浮（percolate up），直到不再比父節點小，或已經到達根。</p>
{figure('percUp1')}
{steps('percUp 的兩次交換', ['percUp2', 'percUp3'])}
<p>往上浮的時候，新元素和父節點之間的順序性質恢復了，兄弟節點那一側的順序性質也維持不變。新元素很小的話，可能要一路換到根。</p>
{snip('percUp 與 insert', PERCUP)}
<h3>delMin 與 percDown</h3>
<p>最小值就在 <code>heap[0]</code>，所以 <code>findMin()</code> 只要讀它。<code>delMin()</code> 的難處在於移除根之後，要同時恢復結構性質與順序性質，分兩步做：先把根和 <code>vector</code> 最後一個元素交換並移除最後一格，結構維持完整；再對新的根呼叫 <code>percDown(0)</code>，讓它和<strong>較小的子節點</strong>交換，一路往下沉，直到比兩個子節點都小。</p>
{figure('percDown1')}
{steps('percDown 的三次交換', ['percDown2', 'percDown3', 'percDown4'])}
{snip('percDown、getMinChild 與 delMin', PERCDOWN)}
{program('對照圖：在圖中的 heap 插入 7，以及執行 delMin', '圖中的 heap：insert 與 delMin', 'heap_figs',
         note='第一行是插入 7 之後的 vector：7 換到索引 1，9 和 18 各往下一層。第二、三行是另一份同樣的 heap 執行 delMin：回傳 5，27 從根沉到索引 8。')}'''
    build = f'''<h3>buildHeap：由下往上建堆</h3>
<p>一種建堆的方法是逐一插入 $n$ 個鍵。每次 <code>insert()</code> 接在尾端，最壞要往上浮過整個樹高，所以每次 $O(\\log n)$，逐一插入共 $O(n\\log n)$。插入並不需要把元素塞進排序好的 vector 中間；順序性質只規範父節點和子節點。</p>
<p>由下往上的 <code>buildHeap()</code>（舊名 <code>heapify()</code>）比較快：從最後一個非葉節點開始，往根的方向逐一呼叫 <code>percDown()</code>，總成本是 $O(n)$。索引大於等於 <code>heap.size() / 2</code> 的都是葉節點，不需要處理。</p>
{snip('heapify（buildHeap）', HEAPIFY_CODE)}
{figure('buildheap')}
<p>當 <code>i = 0</code> 時，從根往下沉可能要跨好幾層。<code>percDown()</code> 每次交換後都會再檢查較小的子節點，所以 9 會一直往下移，直到最底層。</p>
{program('講義例子：buildHeap({9, 6, 5, 2, 3})', 'buildHeap 小例子', 'build_small',
         note='輸出和圖的最後一棵樹一致。在上面的動畫按「講義：buildHeap [9, 6, 5, 2, 3]」可以逐步看 <code>i = 1</code>、<code>i = 0</code> 兩輪。')}
{program('講義完整程式：heapify 十個數', '講義 09 · heapify', 'heapify',
         note='每個父節點都不大於子節點，例如索引 1 的 4 小於索引 3、4 的 5 和 12；但整個 vector 並沒有排序。')}
<p>$O(n)$ 的上界可以依節點高度計算工作量：大約一半的節點是葉節點，不必移動；約 $n/4$ 個節點最多下沉一層，$n/8$ 個最多兩層，依此類推。總和 $\\sum_{{h\\ge0}}(n/2^{{h+1}})h=O(n)$，不是 $O(n\\log n)$。</p>
{quiz('heap1')}
{quiz('heap2')}'''
    sort = f'''<h3 id="ex-heapsort">練習 2：heapSort</h3>
<p>用 <code>buildHeap()</code>（或舊名 <code>heapify()</code>）與 <code>delMin()</code>（或舊名 <code>delet()</code>）寫一個函式，在 $O(n\\log n)$ 時間內排序一個 vector。目標輸出是 <code>1 2 3 5 7 8 9 10 15</code>。可用的成員函式有 <code>insert</code>、<code>findMin</code>、<code>delMin</code>、<code>size</code>、<code>buildHeap</code>、<code>isEmpty</code>，以及舊名 <code>delet</code>、<code>heapify</code>；對空堆積呼叫 <code>findMin</code> 或 <code>delMin</code> 會丟出 <code>underflow_error</code>。</p>
{exercise('練習 2 填空（heapSort）', EX2_BLANK, 'ex2', '練習 2 解答',
          extra='<p><code>buildHeap</code> 花 $O(n)$，接著 $n$ 次 <code>delMin</code> 各 $O(\\log n)$，每次取出的都是剩下的最小值，依序放進 <code>sortedList</code> 就排好了。</p>')}
<p>想看更多堆積操作的例子，可以參考 {VISUALGO_HEAP}。</p>'''
    heapclass = ('<h3>完整的 BinaryHeap 類別</h3>\n'
                 + details('展開：percUp、percDown、delet、heapify 等成員函式並列', LEGACY['heapclass'].rstrip('\n')))
    return fill('heap', {'ops': ops, 'figs': figs, 'perc': perc, 'build': build, 'heapclass': heapclass, 'sort': sort})


# ---------------------------------------------------------------- P07 BST
BST_SHELL = '''class BinarySearchTree {
    public:
        TreeNode* root = NULL;
        int size = 0;

        BinarySearchTree() = default;
        ~BinarySearchTree();              // releases every node
        BinarySearchTree(const BinarySearchTree& other);  // deep copy
        int length() const { return size; }
};'''

TREENODE = '''class TreeNode {
    public:
        string key;
        string value;
        TreeNode* leftChild;
        TreeNode* rightChild;
        TreeNode* parent;

        TreeNode(string k, string v, TreeNode* p = NULL) {
            key = k;
            value = v;
            leftChild = NULL;
            rightChild = NULL;
            parent = p;
        }

        bool isLeftChild() {
            return parent != NULL && parent->leftChild == this;
        }
        bool isRightChild() {
            return parent != NULL && parent->rightChild == this;
        }
        bool isRoot() {
            return parent == NULL;
        }
        bool isLeaf() {
            return leftChild == NULL && rightChild == NULL;
        }
        bool hasAnyChild() {
            return leftChild != NULL || rightChild != NULL;
        }
};'''

PUT = '''protected:
virtual bool insertOrAssign(string key, string value,
                            TreeNode*& slot, TreeNode* parent) {
    if (slot == NULL) {
        slot = new TreeNode(key, value, parent);
        return true;
    }
    if (key == slot->key) {
        slot->value = value;          // duplicate: update, do not grow size
        return false;
    }
    TreeNode*& child = (key < slot->key) ? slot->leftChild : slot->rightChild;
    return insertOrAssign(key, value, child, slot);
}

public:
void put(string key, string value) {
    if (insertOrAssign(key, value, root, NULL)) size++;
}'''

GET = '''string get(string key) {
    if (root != NULL) {
        TreeNode* result = _get(key, root);
        if (result != NULL) {
            return result->value;
        }
    }
    return "";
}

TreeNode* _get(string key, TreeNode* currentNode) {
    if (currentNode == NULL) {
        return NULL;
    }
    if (currentNode->key == key) {
        return currentNode;
    } else if (key < currentNode->key) {
        return _get(key, currentNode->leftChild);
    } else {
        return _get(key, currentNode->rightChild);
    }
}

bool contains(string key) {
    return _get(key, root) != NULL;
}'''


def bst():
    ops = f'''<p>二元搜尋樹是存放鍵值對的第三種方式。這裡要利用二元樹的結構讓搜尋有效率，元素放在樹中的哪個確切位置並不重要。</p>
<h3>Map ADT 的操作</h3>
{table(['操作', '作用'], [
        ['<code>BinarySearchTree()</code>', '建立空的 map。'],
        ['<code>put(key, value)</code>', '插入一組鍵值對；鍵已經存在時，改成新的值。'],
        ['<code>get(key)</code>', '回傳鍵對應的值；這個簡化的字串版本在鍵不存在時回傳 <code>""</code>。'],
        ['<code>remove(key)</code>', '刪除一組鍵值對；鍵不存在時丟出 <code>invalid_argument</code>。'],
        ['<code>length()</code>', '回傳不同鍵的個數。'],
        ['<code>contains(key)</code>', '回傳 <code>bool</code>，表示鍵在不在樹中。'],
    ])}'''
    impl = f'''<h3>BST 性質與建樹順序</h3>
<p>BST 依靠一個性質：比父節點小的鍵都在左子樹，比父節點大的鍵都在右子樹，稱為 <strong>BST 性質</strong>。下圖只畫鍵，不畫值。</p>
{figure('simpleBST')}
<p>這棵樹是依序插入 $70, 31, 93, 94, 14, 23, 73$ 的結果。70 最先插入，所以是根。31 比 70 小，成為 70 的左子；93 比 70 大，成為右子。94 比 70 和 93 都大，成為 93 的右子；14 比 70 和 31 都小，成為 31 的左子。23 也比 31 小，但比 14 大，所以成為 14 的右子。</p>
<h3>TreeNode 與 BinarySearchTree</h3>
<p>BST 同樣用節點與參考實作。因為必須能建立並操作一棵空的樹，實作分成兩個類別：<code>BinarySearchTree</code> 保存指向根節點的指標，<code>TreeNode</code> 是樹中的節點。外層的公開函式大多先檢查樹是不是空的，再把工作交給以根為參數的輔助函式；樹是空的或要刪除根的時候，需要特別處理。</p>
{snip('BinarySearchTree 的外殼', BST_SHELL,
      note='完整的標頭還提供複製與移動指定，確保兩棵樹不會共用同一批節點。')}
<p><code>TreeNode</code> 提供許多輔助函式，判斷自己是左子還是右子、有沒有子節點，讓 <code>BinarySearchTree</code> 的函式好寫很多。</p>
{snip('TreeNode', TREENODE)}
<p>每個 <code>TreeNode</code> 都存了 parent 指標，在 <code>remove()</code> 重新接上子節點、或拆出中序後繼者時特別有用。建構子的 parent 參數有預設值，所以可以建立根（<code>parent == NULL</code>），也可以建立連到父節點的子節點。</p>
<h3>put 與 insertOrAssign</h3>
<p><code>put()</code> 把每一次插入（包括建立根）都交給受保護的虛擬函式 <code>insertOrAssign()</code>。平衡樹的子類別可以覆寫這個函式，而不會繞過公開的 <code>put()</code> 與它對 <code>size</code> 的計算。插入的步驟是：</p>
{ul(['從根開始比較新鍵與目前節點的鍵：比較小就往左子樹找，比較大就往右子樹找。',
     '找到沒有左（右）子節點可以再往下的位置，就是新節點應該放的地方。',
     '建立一個新的 <code>TreeNode</code>，接在上一步找到的位置。'])}
{snip('insertOrAssign 與 put', PUT)}
<p>鍵重複時採用 <strong>insert-or-assign</strong>：只替換既有的值，不建立新節點，<code>size</code> 也不變，符合 Map ADT 的語意。課程標頭用明確的 <code>put(key, value)</code>，例如 <code>myTree.put("a", "apple")</code>，再用 <code>myTree.get("a")</code> 取值；沒有提供 <code>operator[]</code>。</p>
{figure('bstput')}'''
    get = f'''<h3>get 與 contains</h3>
<p><code>get()</code> 比 <code>put()</code> 更簡單：遞迴往下找，找到相同的鍵就回傳節點的值，走到空指標就表示不存在。私有輔助函式 <code>_get()</code> 回傳的是 <code>TreeNode*</code>，所以 <code>get()</code>、<code>contains()</code> 與 <code>remove()</code> 都能重用同一段搜尋。</p>
{snip('get、_get 與 contains', GET)}'''
    return fill('bst', {'ops': ops, 'impl': impl, 'get': get})


# ---------------------------------------------------------------- P08 BST delete
REMOVE = '''void remove(string key) {
    TreeNode* nodeToRemove = _get(key, root);
    if (nodeToRemove == NULL)
        throw invalid_argument("Error, key not in tree");
    _delete(nodeToRemove);              // reconnects links and deletes storage
    size--;
}'''

CASE1 = '''if (currentNode->isLeaf()) {   // removing a leaf
    if (currentNode == currentNode->parent->leftChild) {
        currentNode->parent->leftChild = NULL;
    } else {
        currentNode->parent->rightChild = NULL;
    }
    delete currentNode;
}'''

CASE2 = '''else {   // removing a node with one child
    if (currentNode->leftChild != NULL) {
        if (currentNode->isLeftChild()) {
            currentNode->leftChild->parent = currentNode->parent;
            currentNode->parent->leftChild = currentNode->leftChild;
        } else if (currentNode->isRightChild()) {
            currentNode->leftChild->parent = currentNode->parent;
            currentNode->parent->rightChild = currentNode->leftChild;
        }
    }
    // (mirror image for a right child)
    delete currentNode;
}'''

CASE3 = '''else if (currentNode->hasBothChildren()) {   // removing a node with two children
    TreeNode* successor = currentNode->findSuccessor();
    successor->spliceOut();
    currentNode->key = successor->key;
    currentNode->value = successor->value;
    delete successor;
}'''

SUCC = '''TreeNode* findSuccessor() {
    return rightChild->findMin();
}

TreeNode* findMin() {   // a method of the TreeNode class
    TreeNode* current = this;
    while (current->leftChild != NULL) {
        current = current->leftChild;
    }
    return current;
}'''

BST_INORDER = '''void inorder(TreeNode* node) {
    if (node != NULL) {
        inorder(node->leftChild);
        cout << node->value << " ";
        inorder(node->rightChild);
    }
}'''


def bst_delete():
    cases = f'''<h3>remove 的骨架</h3>
<p>刪除的第一步是用 <code>_get()</code> 找到要刪的節點；找不到就丟出例外。樹只有一個節點時，要刪的就是根，但仍然要確認根的鍵和要刪的鍵相同，<code>_get()</code> 已經做了這個檢查。刪除根的情況在 <code>_delete()</code> 裡處理：刪掉最後一個節點時，把 <code>root</code> 設為 <code>NULL</code> 並釋放節點。</p>
{snip('remove', REMOVE)}
<h3>情況一：沒有子節點</h3>
{figure('bstdel1')}
<p>目前節點沒有子節點時，只要刪掉它，並把父節點指向它的指標設為 <code>NULL</code>。</p>
{snip('情況一：刪除葉節點', CASE1)}
<h3>情況二：只有一個子節點</h3>
{figure('bstdel2')}
<p>只有一個子節點時，直接把這個子節點提上來取代父節點。左右兩種情況對稱，這裡只看目前節點有左子節點的情形：</p>
{ul(['目前節點是左子：把左子節點的 parent 改成目前節點的父節點，再把父節點的 <code>leftChild</code> 指向這個左子節點。',
     '目前節點是右子：把父節點的 <code>rightChild</code> 直接接到唯一的子節點，並更新子節點的 parent。',
     '目前節點是根：把 <code>root</code> 設為它唯一的子節點（或 <code>NULL</code>），並清掉新根的 parent 指標。每一種情況最後都要刪掉被移除的節點。'])}
{snip('情況二：刪除只有一個子節點的節點', CASE2)}
<h3>情況三：有兩個子節點</h3>
{figure('bstdel3')}
<p>有兩個子節點時，不能直接把其中一個提上來。要在樹中找一個節點來取代被刪的節點，而且左右兩棵子樹的 BST 性質都要維持；這個節點就是鍵次大的那一個，稱為<strong>後繼者</strong>（successor）。後繼者最多只有一個子節點，所以用 <code>spliceOut()</code> 把它拆出、接好它的子節點，再把它的鍵和值複製到目標節點，最後刪掉後繼者節點。</p>
{snip('情況三：刪除有兩個子節點的節點', CASE3)}
<p>刪除時目標節點一定有右子樹，所以後繼者就是右子樹的最小值。<code>findMin()</code> 沿著 <code>leftChild</code> 一直走到下一個是 <code>NULL</code> 為止，最左邊的節點就是子樹中最小的鍵。</p>
{snip('findSuccessor 與 findMin', SUCC)}
<p>這和中序走訪由小到大印出 BST 的性質是同一回事。一般而言找後繼者要考慮三種情況：節點有右子樹時，後繼者是右子樹的最小鍵；沒有右子樹且自己是左子時，父節點就是後繼者；沒有右子樹且自己是右子時，後繼者是父節點的後繼者（不算自己）。刪除時目標節點有兩個子節點，只會用到第一種。</p>'''
    inorder = f'''<h3 id="dx-bst">中序走訪：依鍵的順序處理</h3>
<p>要依鍵的順序處理 BST 的每一個鍵，就用前面學過的中序走訪。課程的類別直接印出值；若要重複使用，可以改成把鍵依序放進一個輸出 vector。每次遞迴處理一棵較小的子樹，base case 是 <code>NULL</code> 指標；在左右兩次遞迴之間處理節點，得到的鍵就是排好的。走訪每個節點一次，時間 $O(n)$，遞迴深度 $O(h)$。</p>
{snip('inorder（BinarySearchTree 的成員函式）', BST_INORDER)}
{program('講義完整程式：BinarySearchTree 當 map 使用', '講義 09 · BinarySearchTree', 'bst',
         note='最後一行依鍵的順序印出值。刪掉 <code>"a"</code> 之後剩 8 個鍵，所以第一個值是 b 對應的 brown。')}
<p>想看更多 BST 插入、搜尋與刪除的例子，可以參考 {VISUALGO_BST}。</p>
<h3 id="ex-treesort">練習 3：treeSort</h3>
<p>用 <code>put()</code> 和中序走訪，在平均 $O(n\\log n)$ 時間內排序一個 vector；再說明為什麼不平衡的 BST 最差會是 $O(n^2)$。目標輸出是 <code>a b d f j l o q t</code>：BST 的中序走訪一定是排好的。</p>
{exercise('練習 3 填空（treeSort）', EX3_BLANK, 'ex3', '練習 3 解答',
          extra='<p>課程類別的 <code>inorder</code> 只會印出值，所以解答另寫一個 <code>inorderKeys</code>，在中序走訪時把鍵放進 <code>result</code>。平均每次 <code>put</code> 是 $O(\\log n)$，共 $O(n\\log n)$；但如果輸入已經排好，每個新鍵都接在最右邊，第 $k$ 次 <code>put</code> 要走過 $k-1$ 個節點，總共 $1+2+\\cdots+(n-1)=O(n^2)$。</p>')}'''
    return fill('bst-delete', {'cases': cases, 'inorder': inorder})


# ---------------------------------------------------------------- P09 BST analysis
def bst_analysis():
    skew = f'''<h3>高度決定 put 的成本</h3>
<p>先看 <code>put()</code>。限制它效能的是樹的高度：高度是根到最深的葉節點之間的邊數，而找插入位置時每一層最多比較一次。鍵以隨機順序加入時，大約一半比根小、一半比根大，樹高大約是 $\\log_2 n$。</p>
<p>二元樹的根那一層有 1 個節點，下一層 2 個，再下一層 4 個，深度 $d$ 那一層有 $2^d$ 個。完美平衡、高度為 $h$ 的二元樹共有 $2^{{h+1}}-1$ 個節點，反過來說高度就是 $\\log_2 n$，也就是 <code>put()</code> 最多要做的比較次數。</p>
<h3>最差情況：已排序的插入順序</h3>
<p>可惜只要把鍵依排序好的順序插入，就能建出高度 $n-1$ 的樹：</p>
{figure('skewedTree')}
<p>這時 <code>put</code> 是 $O(n)$。樹高同樣限制 <code>get()</code>、<code>contains()</code> 與 <code>remove()</code>：最差情況都要走一條長度為 $h$ 的路徑。<code>remove()</code> 可能還要再走一段路找後繼者，但那最多是另一段 $O(h)$；常數倍不影響上界。所以不平衡的 BST 最差是 $O(n)$，AVL 樹則是 $O(\\log n)$。</p>'''
    tail = quiz('bst1') + '\n' + quiz('bst2')
    return fill('bst-analysis', {'skew': skew}, tail=tail)


# ---------------------------------------------------------------- P10 AVL
def avl():
    bf = f'''<h3>平衡因子的例子</h3>
<p>AVL 樹和一般 BST 一樣實作 Map ADT，差別只在效能。下圖是一棵右重的不平衡樹，節點上標的是平衡因子：</p>
{figure('unbalanced')}
<p>根的平衡因子是 -2：左子樹高度 0，右子樹高度 2。只要有節點的平衡因子超出 -1、0、1，就需要把樹調回平衡。</p>
<p class="dx-note">下面的旋轉示範（補充）把 LL、RR、LR、RL 四種不平衡各做一次，可以先看形狀怎麼變，旋轉的細節在本節後半段的選讀內容。</p>'''
    perf = f'''<h3>AVL 樹的高度上界 <span class="sec-badge">cppds §8.16 · 選讀</span></h3>
<p>要求每個平衡因子都是 -1、0、1，能把 AVL 樹的高度限制在 $O(\\log n)$。先看在這個條件下最不平衡的樹長什麼樣子。下圖是高度 0、1、2、3 時，節點最少的左重樹：</p>
{figure('worstAVL')}
<p>令 $N_h$ 為高度 $h$ 的 AVL 樹最少的節點數。高度以邊數計算時 $N_0=1$、$N_1=2$；最瘦的合法樹由一個根、一棵高度 $h-1$ 的最瘦樹和一棵高度 $h-2$ 的最瘦樹組成：</p>
<p>$$N_h = 1 + N_{{h-1}} + N_{{h-2}}$$</p>
<p>這和費氏數列很像。費氏數列定義為 $F_0=0$、$F_1=1$、$F_i=F_{{i-1}}+F_{{i-2}}$（$i\\ge2$），而且 $F_i/F_{{i-1}}$ 越來越接近黃金比例 $\\Phi=\\frac{{1+\\sqrt5}}{{2}}$，可以近似成 $F_i\\approx\\Phi^i/\\sqrt5$。代入初始值可以驗證 $N_h=F_{{h+3}}-1$，所以</p>
<p>$$N_h = F_{{h+3}}-1 \\approx \\frac{{\\Phi^{{h+3}}}}{{\\sqrt5}}-1$$</p>
<p>移項後兩邊取以 2 為底的對數，解出 $h$：</p>
<p>$$h \\approx \\frac{{\\log_2(N_h+1)+\\tfrac12\\log_2 5}}{{\\log_2\\Phi}}-3$$</p>
<p>$1/\\log_2\\Phi\\approx1.44$，所以 $h$ 的成長不會超過大約 $1.44\\log_2 n$（差一個加法常數）。'''
    perf += '</p>'
    rot = f'''<h3>左旋與右旋</h3>
<p>插入新的葉節點之後，要更新它父節點的平衡因子：新節點是右子時，父節點的平衡因子減 1；是左子時加 1。同樣的規則可以遞迴地套用到祖父節點，甚至一路到根。遞迴有兩個停止條件：已經到達根，或某個父節點的平衡因子被調成 0。子樹的平衡因子變成 0 之後，它的高度沒有改變，祖先的平衡因子也不會變。</p>
<p>需要重新平衡時，用一次或多次<strong>旋轉</strong>（rotation）把樹調回平衡。</p>
{figure('simpleunbalanced')}
<p>左旋的步驟：</p>
<ol class="tree-ul">
<li>把右子（B）提為子樹的新根。</li>
<li>把舊根（A）移成新根的左子。</li>
<li>如果新根（B）原本有左子，把它改接成新左子（A）的右子。A 原本的右子就是 B，所以這時 A 的右邊一定是空的，可以直接接上。</li>
</ol>
{figure('rightrotate1')}
<p>右旋對稱：</p>
<ol class="tree-ul">
<li>把左子（C）提為子樹的新根。</li>
<li>把舊根（E）移成新根的右子。</li>
<li>如果新根（C）原本有右子（D），把它改接成新右子（E）的左子。E 原本的左子就是 C，所以這時 E 的左邊一定是空的。</li>
</ol>
<p>概念不難，但程式要依正確的順序搬動，才能維持 BST 的所有性質，而且每個 parent 指標都要更新。下面左欄是 <code>insertOrAssign</code> 的覆寫與 <code>updateBalance</code>，中欄是 <code>rotateLeft</code>（<code>rotateRight</code> 對稱）。<code>rotateLeft</code> 先用暫存變數記住新根，也就是舊根的右子，再把舊根的右子換成新根的左子；接著調整兩個節點的 parent 指標：舊根若是整棵樹的根，就把 <code>root</code> 改成新根，否則讓舊根的父節點改指向新根；最後把舊根的 parent 設為新根。</p>'''
    bfd = f'''<h3>平衡因子的更新公式</h3>
<p><code>rotateLeft</code> 最後兩行更新舊根與新根的平衡因子。其他節點都是整棵子樹一起搬動，平衡因子不受影響。問題是：不重新計算子樹高度，怎麼得到新的平衡因子？</p>
{figure('bfderive')}
<p>B、D 是旋轉的兩個節點，A、C、E 是它們的子樹，$h_x$ 表示以 $x$ 為根的子樹高度。依定義：</p>
<p>$$\\begin{{aligned}}\\text{{new\\_bal}}(B) &= h_A - h_C\\\\ \\text{{old\\_bal}}(B) &= h_A - h_D\\end{{aligned}}$$</p>
<p>D 的舊高度是它兩棵子樹中較高的再加 1，也就是 $h_D = 1 + \\max(h_C, h_E)$，而 $h_C$、$h_E$ 在旋轉中沒有改變。代入第二式：</p>
<p>$$\\text{{old\\_bal}}(B) = h_A - (1 + \\max(h_C, h_E))$$</p>
<p>兩式相減，$h_A$ 消掉：</p>
<p>$$\\text{{new\\_bal}}(B) - \\text{{old\\_bal}}(B) = 1 + \\max(h_C, h_E) - h_C$$</p>
<p>把 $\\text{{old\\_bal}}(B)$ 移到右邊，並用 $\\max(a,b)-c=\\max(a-c,b-c)$：</p>
<p>$$\\text{{new\\_bal}}(B) = \\text{{old\\_bal}}(B) + 1 + \\max(0,\\ h_E - h_C)$$</p>
<p>$h_E - h_C$ 正好是 $-\\text{{old\\_bal}}(D)$。再用 $\\max(-a,-b) = -\\min(a,b)$：</p>
<p>$$\\begin{{aligned}}\\text{{new\\_bal}}(B) &= \\text{{old\\_bal}}(B) + 1 + \\max(0,\\ -\\text{{old\\_bal}}(D))\\\\ &= \\text{{old\\_bal}}(B) + 1 - \\min(0,\\ \\text{{old\\_bal}}(D))\\end{{aligned}}$$</p>
<p>B 是 <code>rotationRoot</code>、D 是 <code>newRoot</code>，這就是程式中的</p>
{snip('rotateLeft 的平衡因子更新', 'rotationRoot->balanceFactor = rotationRoot->balanceFactor + 1\n                              - min(newRoot->balanceFactor, 0);')}
<p>新根 D 的公式，以及右旋時的兩個公式，可以用同樣的方法推導，留作練習。</p>
<h3>需要兩次旋轉的情況</h3>
<p>知道何時左旋、何時右旋似乎就夠了，但看下面左圖：A 的平衡因子是 -2，應該左旋；左旋之後卻變成右圖，往另一邊不平衡。再右旋一次，又回到原狀。</p>
{figrow(['hardunbalanced', 'badrotate'], '只做一次左旋解決不了：右子 C 是左重時，左旋 A 會得到左重的 C。', '直接左旋失敗的例子')}
<p>要解決這個問題，遵守下面兩條規則：</p>
<ol class="tree-ul">
<li>子樹需要左旋時，先檢查右子的平衡因子。右子是左重的話，先對右子做右旋，再做原本的左旋。</li>
<li>子樹需要右旋時，先檢查左子的平衡因子。左子是右重的話，先對左子做左旋，再做原本的右旋。</li>
</ol>
{figure('rotatelr')}
<p>右欄的 <code>rebalance</code> 就是這兩條規則。重新平衡的成本：新節點插在葉節點，往上更新平衡因子最多 $\\log_2 n$ 次，每層一次；發現不平衡時最多兩次旋轉，每次 $O(1)$。所以 <code>put</code> 仍然是 $O(\\log_2 n)$，<code>get</code> 也保持 $O(\\log_2 n)$。刪除節點以及之後的更新與重新平衡，留作練習。</p>
{quiz('avl1')}
{quiz('avl2')}'''
    return fill('avl', {'bf': bf, 'perf': perf, 'rot': rot, 'bfd': bfd})


# ---------------------------------------------------------------- REF summary
def summary():
    return fill('summary', {'real': fold('樹結構在實際系統中的地位', LEGACY['real'].rstrip('\n'))})


# ---------------------------------------------------------------- recap
def recap():
    qa = [
        ('getLeftChild() 為什麼回傳指標，不是回傳值？',
         '<p>因為子節點本身就是一棵 <code>BinaryTree</code>。回傳 <code>BinaryTree*</code> 之後，可以接著用 <code>-&gt;</code> 對子樹呼叫 <code>insertLeft</code>、<code>setRootVal</code> 等操作，一路往下修改；空的子樹則回傳 <code>NULL</code>。如果回傳複本，修改的就不是樹裡的節點。</p>'),
        ('前序、中序、後序要怎麼記？',
         '<p>看「根」排在第幾個：前序是根在最前（根、左、右），中序是根在中間（左、根、右），後序是根在最後（左、右、根）。左子樹永遠在右子樹之前。</p>'),
        ('heap 已經是「排好」的嗎？',
         '<p>不是。堆積只保證父節點不大於子節點，所以最小值一定在 <code>heap[0]</code>；兄弟節點之間、不同子樹之間沒有大小關係。例如 <code>heapify</code> 十個數的結果 <code>3 4 9 5 12 15 10 8 14 18</code> 就不是遞增的。要得到排序結果，得反覆 <code>delMin</code>，也就是練習 2 的 heapSort。</p>'),
        ('buildHeap 為什麼從 heap.size() / 2 - 1 開始？',
         '<p>索引 $i$ 的左子在 $2i+1$。當 $i \\ge$ <code>heap.size() / 2</code> 時，$2i+1$ 已經超出 vector 的範圍，這些節點都是葉節點，自己就滿足堆積性質。所以從最後一個非葉節點開始往前做 <code>percDown</code> 就夠了。</p>'),
        ('BST 和雜湊表都能實作 map，什麼時候選 BST？',
         '<p>雜湊表平均 $O(1)$，但鍵沒有順序。BST 可以用中序走訪依鍵的順序列出所有資料，也方便找最小、最大或某個範圍的鍵；平衡的 BST（例如 AVL 樹，或 <code>std::map</code> 常用的紅黑樹）還保證最差 $O(\\log n)$。</p>'),
    ]
    faq = ''.join(details(f'{q}（補充）', a, cls='tree-detail tree-faq') for q, a in qa)
    return f'''<ul class="tree-ul tree-recap">
<li>樹是階層式的結構：除了根以外每個節點恰好有一個父節點，從根到每個節點的路徑唯一。高度是最大的層數，只有根的樹高度為 0。樹也可以遞迴定義：空樹，或根加上若干棵子樹。</li>
<li>二元樹的每個節點最多兩個子節點。課程用節點與參考實作 <code>BinaryTree</code>：<code>key</code> 加上 <code>leftChild</code>、<code>rightChild</code> 兩個指標，<code>NULL</code> 表示空子樹；<code>insertLeft</code>／<code>insertRight</code> 遇到既有子節點時把它往下推一層。</li>
<li>解析樹把運算式的結構表示成樹：運算子在內部節點、數字在葉節點。<code>buildParseTree</code> 用四條規則加上一個 parent stack 建樹，<code>evaluate</code> 遞迴地先算左右子樹再套用運算子。</li>
<li>三種走訪只差在拜訪根的時機：前序（根、左、右）、中序（左、根、右）、後序（左、右、根）。解析樹的後序就是求值的順序（<code>postordereval</code>），中序加括號就是 <code>printExp</code>。</li>
<li>二元堆積是存在 vector 裡的完全二元樹：索引 $p$ 的子節點在 $2p+1$、$2p+2$，父節點在 <code>(i - 1) / 2</code>。<code>insert</code> 接在尾端再 <code>percUp</code>，<code>delMin</code> 把最後一個搬到根再 <code>percDown</code>，都是 $O(\\log n)$；由下往上的 <code>buildHeap</code> 是 $O(n)$。</li>
<li>BST 滿足左子樹的鍵都比較小、右子樹的鍵都比較大。<code>put</code>、<code>get</code>、<code>contains</code>、<code>remove</code> 都沿著一條路徑走，成本是 $O(h)$；鍵重複時 <code>put</code> 只更新值。刪除分三種情況：葉節點、一個子節點、兩個子節點（用後繼者取代）。</li>
<li>隨機插入時 BST 的高度約為 $\\log_2 n$，但依排序好的順序插入會退化成高度 $n-1$ 的鏈，操作變成 $O(n)$。</li>
<li>AVL 樹要求每個節點的平衡因子（左子樹高度減右子樹高度）是 -1、0 或 1，用旋轉維持平衡，高度上界約 $1.44\\log_2 n$，所有 map 操作都是 $O(\\log n)$。</li>
</ul>
<h3>常見疑問</h3>
{faq}'''


def sections():
    return {
        'trees-prologue': prologue(),
        'trees-vocabulary': vocabulary(),
        'trees-tree-adt': tree_adt(),
        'trees-nodes-refs': nodes_refs(),
        'trees-parse-tree': parse_tree(),
        'trees-traversals': traversals(),
        'trees-heap': heap(),
        'trees-bst': bst(),
        'trees-bst-delete': bst_delete(),
        'trees-bst-analysis': bst_analysis(),
        'trees-avl': avl(),
        'trees-summary': summary(),
        'trees-recap': recap(),
    }


STYLE = """<style id="trees-depth-style">
.tree-detail{margin:1rem 0;border:1px solid var(--card-border);border-radius:8px;background:var(--card);}
.tree-detail>summary{cursor:pointer;padding:.9rem 1rem;font-weight:600;line-height:1.6;}
.tree-detail-body{padding:0 1rem 1rem;min-width:0;}
.tree-detail-body .pseudo-code,.deck-extra .pseudo-code,.side-panel .pseudo-code{max-width:100%;overflow-x:auto;}
.tree-ul{padding-left:1.4rem;margin:.6rem 0 1rem;}
.tree-ul li{margin:.3rem 0;line-height:1.8;}
.tree-quiz{margin-top:1.2rem;}
.tree-quiz .sq-num{margin-right:.6rem;}
.viz-layout,.viz-layout>div{min-width:0;}
#canvas-trav .t-node{font-size:.72rem;}
</style>"""
