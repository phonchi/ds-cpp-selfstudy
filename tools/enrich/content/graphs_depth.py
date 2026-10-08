"""Chapter 8 (graphs.html) section bodies. Each value of sections() fills one <!-- gen:NAME --> block.

Lecture text and code follow 08_Graphs and Graphing Algorithms.ipynb; headers are
pythonds3/cppds/graph.hpp and graph_algos.hpp. Expected outputs come from compiling the programs
(see graphs_programs.OUT).
"""
from html import escape
from enrich_lib import hl
from content.graphs_figures import figure, steps
from content.graphs_programs import *  # noqa: F401,F403


# ---------------------------------------------------------------- helpers (same conventions as chapters 4-6)
def details(summary, body, cls='gr-detail', did=''):
    ident = f' id="{did}"' if did else ''
    return f'<details class="{cls}"{ident}><summary>{summary}</summary><div class="gr-detail-body">{body}</div></details>'


def fold(title, body, did=''):
    """Content that the lecture does not cover: collapsed and labelled （補充）."""
    return details(title + '（補充）', body, did=did)


def table(headers, rows):
    return ('<div class="table-scroll" tabindex="0" aria-label="表格，可左右捲動"><table class="cmp-table"><thead><tr>'
            + ''.join(f'<th>{h}</th>' for h in headers) + '</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{v}</td>' for v in r) + '</tr>' for r in rows)
            + '</tbody></table></div>')


def quiz(qid, label, question, options, extra=''):
    """options: [(correct, text, feedback)], four per quiz; the page shuffles option order at load time."""
    assert len(options) == 4 and sum(ok for ok, _, _ in options) == 1, qid
    opts = ''.join(
        f'<div class="quiz-opt" data-correct="{"true" if ok else "false"}" data-fb="{escape(fb, quote=True)}" '
        f'onclick="quizCheck(\'{qid}\', this)"><span class="opt-letter">({chr(65 + i)})</span> <span class="opt-text">{text}</span></div>'
        for i, (ok, text, fb) in enumerate(options))
    return (f'<div class="quiz-box">\n  <div class="quiz-label">{label}</div>\n  <p>{question}</p>\n{extra}'
            f'  <div class="quiz-options" id="{qid}Options">\n    {opts}\n  </div>\n'
            f'  <div class="quiz-feedback" id="{qid}Feedback"></div>\n</div>')


def _expected_attr(output):
    return ' data-expected="' + escape(output + '\n', quote=True).replace('\n', '&#10;') + '"'


def _expected_out(output, label='預期輸出'):
    return (f'<div class="expected-out"><span class="eo-tag">{label}</span><pre>'
            + escape(output) + '</pre></div>')


def snippet(label, code, output=None, note=None, kind=None, did=''):
    """Code card. kind: run | fragment | compile-error | exercise | header (chapter-3 convention);
    a run block carries data-expected with the exact stdout."""
    if kind is None:
        kind = 'run' if output is not None and 'int main' in code else 'fragment'
    attrs = f' data-cpp="{kind}"' + (_expected_attr(output) if kind == 'run' and output is not None else '')
    ident = f' id="{did}"' if did else ''
    parts = [f'<div class="deck-extra"{ident}>', f'  <div class="dx-label">{label}</div>',
             f'  <div class="pseudo-code" style="font-size:.8rem;"{attrs}>{hl(code)}</div>']
    if output is not None:
        parts.append('  ' + _expected_out(output))
    if note:
        parts.append(f'  <p class="dx-note">{note}</p>')
    parts.append('</div>')
    return '\n'.join(parts)


def listing(summary, label, code, note=None, kind='fragment'):
    """A lecture listing (function or class) collapsed; the explanation stays in the running text."""
    return details(summary, snippet(label, code, note=note, kind=kind))


def lecture_program(summary, label, code, output, note=None, did=''):
    """Lecture full program: collapse the code, keep the expected output and the note visible."""
    card = snippet(label, code, kind='run').replace('data-cpp="run"', 'data-cpp="run"' + _expected_attr(output), 1)
    out = _expected_out(output)
    if note:
        out += f'<p class="dx-note">{note}</p>'
    return details(summary, card, did=did) + out


def ul(items, cls='gr-ul'):
    return f'<ul class="{cls}">' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'


def ol(items):
    return '<ol class="gr-ul">' + ''.join(f'<li>{x}</li>' for x in items) + '</ol>'


OPTIONAL = '<p class="gr-skip">上課時只講本節的摘要，其餘留給自學。</p>'


# ---------------------------------------------------------------- P00 prologue
def prologue():
    return f'''{figure('digraph')}
<p>這張圖有六個頂點：</p>
<p>$$V = \\{{ v_0, v_1, v_2, v_3, v_4, v_5 \\}}$$</p>
<p>以及九條有權重的邊，每條邊寫成 (起點, 終點, 權重)：</p>
<p>$$E = \\{{ (v_0,v_1,5), (v_1,v_2,4), (v_2,v_3,9), (v_3,v_4,7), (v_4,v_0,1), (v_0,v_5,2), (v_5,v_4,8), (v_3,v_5,3), (v_5,v_2,1) \\}}$$</p>
<p><strong>子圖</strong>（subgraph）是從 $E$ 取一部分邊、從 $V$ 取一部分頂點所組成的圖。</p>
<h3>路徑與循環的精確定義</h3>
{ul(['<strong>路徑</strong>（path）是一串<strong>互不相同</strong>的頂點 $w_1, w_2, \\ldots, w_n$，對每個 $1 \\le i \\le n-1$ 都有 $(w_i, w_{i+1}) \\in E$。不看權重時，路徑長度是邊數 $n-1$；加權路徑長度是路上所有邊的權重和。上圖從 $v_3$ 到 $v_1$ 的路徑是 $(v_3, v_4, v_0, v_1)$，加權長度 7 + 1 + 5 = 13。允許頂點重複的更一般序列叫做 <strong>walk</strong>。',
     '<strong>循環</strong>（cycle）是封閉的序列 $(w_1, w_2, \\ldots, w_n, w_1)$，其中 $w_1, \\ldots, w_n$ 互不相同，相鄰兩點之間都有邊。例如 $(v_5, v_2, v_3, v_5)$。沒有循環的圖叫做<strong>無循環圖</strong>；沒有循環的有向圖叫做 <strong>DAG</strong>（directed acyclic graph）。很多重要的問題，只要能用 DAG 表示，就能有效率地解決。',
     '<strong>樹</strong>（tree）是連通、無循環的無向圖：任兩個頂點之間都有路徑，而且圖中沒有循環。下一章會詳細介紹各種樹。'])}
<p>下面的互動圖就是同一張有向加權圖，按按鈕可以標出上面的路徑與循環。</p>'''


def prologue_legend():
    body = '''<p>BFS 與 DFS 都用「白／灰／黑」三種顏色記錄每個頂點被造訪到什麼程度，本頁的動畫也用同一套顏色：</p>
  <div class="legend">
    <span class="legend-item"><span class="lg-swatch" style="background:var(--node-white)"></span>White：尚未發現</span>
    <span class="legend-item"><span class="lg-swatch" style="background:var(--node-gray)"></span>Gray：已發現、尚未完成</span>
    <span class="legend-item"><span class="lg-swatch" style="background:var(--node-black)"></span>Black：已完全探索</span>
    <span class="legend-item"><span class="lg-swatch" style="background:var(--node-current)"></span>Current：目前處理中</span>
    <span class="legend-item"><span class="lg-swatch" style="background:var(--node-start)"></span>Start：起點</span>
    <span class="legend-item"><span class="lg-edge" style="background:var(--edge-default)"></span>原始邊</span>
    <span class="legend-item"><span class="lg-edge" style="background:var(--edge-tree)"></span>樹邊（搜尋樹）</span>
    <span class="legend-item"><span class="lg-edge" style="background:var(--edge-explore)"></span>正在檢查</span>
  </div>
<p>每一節的動畫版面都是左邊「圖與控制列」、右邊「即時統計、程式與複雜度」。按 <span class="pill pill-green">▶ 開始</span> 播放整段動畫，或按 <span class="pill pill-blue">→ 單步</span> 一步一步看。</p>'''
    return fold('動畫的顏色與操作方式', body)


# ---------------------------------------------------------------- P01 representation
def rep_adt():
    q = quiz('qGraphRep', 'QUIZ · 圖的實作方式', '關於圖的兩種實作方式，下列哪一個敘述正確？', [
        (False, '表示稀疏圖時，相鄰矩陣是最省空間的方法。', '稀疏圖的矩陣大部分格子都是空的，卻還是佔用 |V|² 格的空間。'),
        (True, '圖的連線很稀疏時，相鄰串列比較省空間。', '相鄰串列只儲存實際存在的邊，空間是 O(|V| + |E|)。'),
        (False, '相鄰矩陣中，兩個頂點沒有相連時，那一格不佔記憶體。', '矩陣的每一格都佔空間，不論那裡有沒有邊。'),
        (False, '列出某個頂點的所有鄰居，相鄰矩陣比相鄰串列快。', '矩陣要掃完長度 |V| 的一整列；串列只走實際存在的 deg(v) 個鄰居。'),
    ])
    return f'''<p>頂點可以彼此相連，也可以孤立；邊連接兩個頂點，而且可以有權重。本課程的圖 ADT 提供下面這些操作：</p>
{ul(['<code>Graph()</code>：建立一張空圖。',
     '<code>setVertex(key)</code>：加入一個還不存在的頂點。key 已經存在時什麼都不做，原有的邊與走訪狀態都保留。',
     '<code>addEdge(fromKey, toKey)</code>：加入一條權重為 0 的有向邊；端點不存在時會自動建立。',
     '<code>addEdge(fromKey, toKey, weight)</code>：加入或更新一條有權重的有向邊。',
     '<code>vertices.find(key)</code> 或 <code>vertices.count(key)</code>：檢查某個 key 是否存在。',
     '用 range-based for 迴圈走過 <code>vertices</code>，就能逐一取得每組 key 與 <code>Vertex</code>。'])}
<p>課程的標頭刻意把有序的 <code>vertices</code>（<code>map&lt;string, Vertex&gt;</code>）公開，所以查詢與走訪直接用標準 map 的操作。圖 ADT 有兩種常見的實作：<strong>相鄰矩陣</strong>與<strong>相鄰串列</strong>。</p>
<h3>相鄰矩陣</h3>
<p>最簡單的實作是二維矩陣：每一列與每一欄各代表一個頂點，第 $v$ 列第 $w$ 欄的值表示從 $v$ 到 $w$ 有沒有邊。兩個頂點之間有邊時，稱它們<strong>相鄰</strong>（adjacent），格子裡存邊的權重。</p>
{figure('adjMat')}
<p>矩陣簡單，小圖也一眼就看得出誰跟誰相連；但上面這個矩陣大部分格子是空的，我們說它是<strong>稀疏</strong>（sparse）的，而矩陣不是儲存稀疏資料的好方法。每個頂點各佔一列一欄，要填滿矩陣需要 $|V|^2$ 條邊，所以邊數很多時矩陣才划算。實際問題很少連得這麼密，本章的問題全都是稀疏圖。</p>
<h3>相鄰串列</h3>
<p>稀疏圖改用相鄰結構儲存。在本課程的 C++ 實作中，<code>Graph::vertices</code> 是 <code>map&lt;string, Vertex&gt;</code>，每個 <code>Vertex::neighbors</code> 是 <code>map&lt;string, int&gt;</code>：key 是鄰居，value 是邊的權重。</p>
{figure('adjlist')}
<p>相鄰結構使用 $O(|V|+|E|)$ 的空間，列出頂點 $v$ 的所有鄰居需要 $O(\\deg(v))$ 時間。我們用有序 map，所以查詢頂點要 $O(\\log |V|)$、查詢某條邊要 $O(\\log \\deg(v))$；這兩個對數來自 <code>std::map</code>，不是圖 ADT 本身的要求。</p>
{q}
<h3>互動：同一張圖的兩種表示</h3>
<p>點選頂點，看矩陣的哪一列、串列的哪一行對應到它的鄰居。</p>'''


def rep_impl():
    return f'''<h3 id="dx-rep">C++ 實作：Vertex 與 Graph 類別</h3>
<p>講義先用兩個精簡的類別說明想法。每個 <code>Vertex</code> 用 <code>map&lt;string, int&gt; neighbors</code> 把鄰居的 key 對應到邊的權重：<code>setNeighbor(other, weight)</code> 加入或更新這組對應，<code>getNeighbor(other)</code> 在邊存在時取回權重，不存在時回傳 −1。</p>
{listing('講義程式：Vertex 類別', '講義 08 · Vertex', VERTEX_LECTURE)}
<p><code>Graph</code> 也用 <code>map&lt;string, Vertex&gt; vertices</code> 把頂點的 key 對應到 <code>Vertex</code> 物件。range-based for 迴圈走過的是 key／value 對；<code>vertices.count(key)</code> 檢查頂點是否存在。</p>
{listing('講義程式：Graph 類別', '講義 08 · Graph', GRAPH_LECTURE)}
<p>本章的程式實際 <code>#include</code> 的是課程標頭 <code>pythonds3/cppds/graph.hpp</code>。標頭裡的 <code>Vertex</code> 沒有 <code>getNeighbor</code>／<code>setNeighbor</code>，程式直接讀寫公開的 <code>neighbors</code>；它另外多了 <code>color</code>、<code>distance</code>、<code>previous</code> 三個欄位，給後面的 BFS、DFS、Dijkstra 與 Prim 使用。<code>distance</code> 一開始是 <code>INT_MAX</code>，代表還沒從起點走到。</p>
{listing('課程標頭 graph.hpp 的 Vertex 與 Graph', 'pythonds3/cppds/graph.hpp', HEADER_GRAPH, kind='header')}
<h3>建立講義的範例圖</h3>
<p>先建立編號 0 到 5 的六個頂點，再看 <code>vertices</code> 裡有什麼：每個 key 都對應一個 <code>Vertex</code> 物件。</p>
{lecture_program('講義完整程式：setVertex 建立六個頂點', '講義 08 · setVertex', SETVERTEX_MAIN, OUT['setvertex'],
                 note='map 依 key 排序，所以頂點依 "0" 到 "5" 的順序印出。')}
<p>接著加入連接頂點的邊，最後用兩層迴圈檢查每條邊都正確存好：</p>
{lecture_program('講義完整程式：addEdge 加入九條邊', '講義 08 · addEdge 與走訪相鄰串列', ADDEDGE_MAIN, OUT['addedge'],
                 note='每組 (起點, 終點, 權重) 是一條有向邊，正好是開頭那張圖的九條邊。外層迴圈依頂點的 key 排序，內層依鄰居的 key 排序，所以 (5,2,1) 排在 (5,4,8) 前面。', did='dx-rep-run')}'''


# ---------------------------------------------------------------- P02 word ladder
def word_ladder():
    return f'''<p>先看一個叫 <strong>word ladder</strong> 的謎題：把 FOOL 變成 SAGE，每次只能改<strong>一個字母</strong>，而且每一步都必須是真正的英文單字，不能變成不存在的字。下面是一種解法：</p>
<div class="pseudo-code gr-ladder">FOOL
POOL
POLL
POLE
PALE
SALE
SAGE</div>
<p>這個謎題有很多變化，例如限定步數，或規定一定要經過某個單字。這一節要找的是：從起點單字變到終點單字，<strong>最少</strong>要幾步。做法分兩步：</p>
{ul(['把單字之間的關係表示成一張圖。',
     '用<strong>廣度優先搜尋</strong>（breadth-first search, BFS）這個圖演算法，找出從起點到終點的有效率路徑。'])}
<h3>建立 word ladder 的圖</h3>
<p>第一個問題是把一大堆單字變成圖：兩個單字只差一個字母時，就在它們之間連一條邊。只要建得出這張圖，從一個單字到另一個單字的任何一條路徑，就是這個謎題的一個解。</p>
{figure('wordgraph')}
<p>假設手上有一串長度相同的單字。先替每個單字建立一個頂點。要決定怎麼連邊，最直接的做法是把每個單字跟其他所有單字比較，數有幾個字母不同；只差一個字母就連一條邊。</p>
<p>單字不多時這樣做沒問題。但如果有 5,110 個四個字母的單字，拿每個單字跟其他所有單字比較，大約是 $O(n^2)$ 的演算法：5,110 個字要比較超過 2,600 萬次。</p>
<h3>用 bucket 找出只差一個字母的單字</h3>
<p>改用一些 <strong>bucket</strong>，每個 bucket 的標籤是一個把其中一個字母換成底線的四字母單字。處理單字時，用底線 <code>_</code> 當萬用字元，把單字跟 bucket 標籤比對。每找到一個相符的 bucket，就把單字放進去，例如 <code>POPE</code> 與 <code>POPS</code> 都會進入 <code>POP_</code>。所有單字都放好之後，同一個 bucket 裡的單字一定兩兩相連。</p>
{figure('wordbuckets')}
<p>可重複使用的實作分成兩個標頭：<code>pythonds3/cppds/graph.hpp</code> 放資料結構，<code>pythonds3/cppds/graph_algos.hpp</code> 放演算法，<code>buildGraph</code> 就在後者裡面。bucket 用 <code>map&lt;string, set&lt;string&gt;&gt;</code> 存：萬用字元標籤是 map 的 key，對應的 set 存著符合這個樣式的所有單字。</p>
{listing('講義程式：buildGraph', '講義 08 · buildGraph（graph_algos.hpp）', BUILDGRAPH)}
{ul(['第一段迴圈：每個長度為 L 的單字產生 L 個標籤，例如 <code>word.substr(0, i) + "_" + word.substr(i + 1)</code> 把第 i 個字母換成底線。',
     '第二段迴圈：同一個 bucket 裡任兩個不同的單字之間都加一條邊。兩個方向各加一次，所以這張圖是用有向邊表示的無向圖。'])}
<p>5,110 個單字的相鄰矩陣會有 $5{{,}}110^2 = 26{{,}}112{{,}}100$ 格。<code>buildGraph()</code> 只存了 53,286 筆有向的相鄰資料（26,643 組無向的單字對），大約只佔那些格子的 0.20%，所以這張圖非常稀疏。</p>
<h3>互動：在 15 個單字上找最短的 word ladder</h3>
<p>下面的互動圖已經用 bucket 法建好圖。選起點與終點，按「找最短路徑」就會執行下一節的 BFS。</p>'''


# ---------------------------------------------------------------- P03 BFS
def bfs_intro():
    return f'''<h3>三種顏色記錄進度</h3>
<p>BFS 把每個頂點塗成白、灰、黑三種顏色之一。頂點建立時都是白色，代表還沒被發現；第一次被發現時塗成灰色；BFS 把它完全探索完之後塗成黑色。所以黑色頂點不會有白色的鄰居；灰色頂點則可能還有白色鄰居，表示還有頂點要探索。</p>
<p>下面的 <code>bfs()</code> 使用前面的相鄰串列表示法，另外用一個<strong>佇列</strong>（queue）決定下一個要探索的頂點。佇列是關鍵，原因馬上會看到。</p>
{listing('講義程式：bfs', '講義 08 · bfs', BFS_LECTURE)}
<p>BFS 用到 <code>Vertex</code> 類別的三個額外資料成員：<code>distance</code>、<code>previous</code> 與 <code>color</code>。它們是公開成員，演算法直接讀取與修改。標頭 <code>graph_algos.hpp</code> 裡的版本在開始前先把每個頂點重設為白色、距離 <code>INT_MAX</code>（還走不到）、沒有前一個頂點（空字串），然後把起點的 distance 設為 0，並且<strong>在放進佇列之前</strong>先把起點塗成灰色，再從 FIFO 佇列的前端一個一個取出來探索。</p>
{listing('課程標頭 graph_algos.hpp 的 bfs', 'pythonds3/cppds/graph_algos.hpp · bfs', HEADER_BFS, kind='header')}
<p>檢查相鄰串列上的每個頂點時，先看它的顏色。如果是白色，會做四件事：</p>
{ol(['把這個還沒探索的頂點 <code>neighbor</code> 塗成灰色。',
     '把 <code>neighbor</code> 的前一個頂點設為目前的頂點 <code>current</code>。',
     '把 <code>neighbor</code> 的距離設為 <code>current.distance + 1</code>。',
     '把 <code>neighbor</code> 加到佇列尾端。它會排在所有已經在等待、屬於同一層或更早層的頂點之後。'])}
<h3>互動：一層一層往外擴散</h3>
<p>選一個起點按「開始」，觀察佇列的變化：距離 $k$ 的頂點全部出列之前，距離 $k+1$ 的頂點只會排在佇列後面等。右邊的程式會標出目前執行到哪一行。</p>'''


def bfs_trace():
    q_note = ('BFS 樹裡 sage 的上一個是 page，所以印出 sage->page->pale->…；開頭列的解法經過 sale 與 pole，同樣是 6 步。'
              '距離 5 的 page 與 sale 都和 sage 相鄰，BFS 先從 page 發現 sage，就把 previous 設成 page。')
    return f'''<h3>在單字圖上追蹤 BFS</h3>
<p>從 <code>fool</code> 出發，把所有和 <code>fool</code> 相鄰的頂點加進佇列：<code>pool</code>、<code>foil</code>、<code>foul</code>、<code>cool</code>。這些都是接下來要展開的新頂點。</p>
{figure('bfs1')}
<p>下一步，BFS 從佇列前端取出下一個頂點 <code>pool</code>，對它的每個鄰居重複同樣的處理。檢查到 <code>cool</code> 時，發現它已經是灰色：這表示有更短的路徑能到 <code>cool</code>，而且它已經在佇列裡等著被展開。所以檢查 <code>pool</code> 只新增了 <code>poll</code>。接著是 <code>foil</code>，它唯一能加入樹的新頂點是 <code>fail</code>；再往後的兩個頂點都沒有新增任何東西。</p>
{steps('逐步圖：處理 pool 與第一層之後', ['bfs2', 'bfs3'])}
<p>自己繼續往下追蹤，直到熟悉整個過程。下圖是所有頂點都處理完之後的 BFS 樹：</p>
{figure('bfsDone')}
<p>圖中的鄰居是依課本的順序畫的；C++ 的 <code>neighbors</code> 是 map，會依 key 的字母順序走訪（<code>cool</code>、<code>foil</code>、<code>foul</code>、<code>pool</code>），所以佇列的順序不同，但每個頂點的距離一樣。</p>
<h3>沿 previous 往回走：traverse</h3>
<p>跑完這次 BFS，除了一開始的 FOOL 到 SAGE，其他單字的問題也一起解決了：從 BFS 樹上任何一個頂點出發，沿著 previous 往回走到根，就是從那個單字回到 <code>fool</code> 最短的 word ladder。</p>
{listing('講義程式：traverse', '講義 08 · traverse', TRAVERSE)}
{lecture_program('講義完整程式：bfs 之後用 traverse 印出 sage 的路徑', '講義 08 · buildGraph + bfs + traverse', WL_TRAVERSE_MAIN, OUT['wl_traverse'],
                 note=q_note, did='dx-bfs')}
<p>同一次 BFS 也得到了每個單字和 <code>fool</code> 的距離：</p>
{lecture_program('講義完整程式：印出每個單字的 distance', '講義 08 · 每個單字與 fool 的距離', WL_DIST_MAIN, OUT['wl_dist'],
                 note='距離就是 BFS 樹的層數：cool、foil、foul、pool 在第 1 層，sage 在第 6 層。')}
<h3>BFS 的分析</h3>
<p>先看 <code>while</code> 迴圈：每個頂點必須是白色才會被檢查並加進佇列，所以迴圈最多對每個頂點執行一次，也就是最多 $|V|$ 次，得到 $O(|V|)$。巢狀在裡面的 <code>for</code> 迴圈，對每條邊最多執行一次，最多 $|E|$ 次：每個頂點最多出列一次，而從 $u$ 到 $v$ 的邊只在 $u$ 出列時被檢查。這部分是 $O(|E|)$，兩個迴圈合起來是 $O(|V| + |E|)$。</p>
<p>BFS 只是工作的一部分。沿著 previous 從目標走回起點是另一部分，最壞的情況是整張圖是一條長鏈，要走過所有頂點，花 $O(|V|)$；一般情況只會走過 $|V|$ 的一部分。最後，至少在這個問題裡，還要加上建立整張圖的時間。</p>
{fold('一次 BFS 得到的兩樣東西', '<p>沿著 previous 往回走，可以從任何一個可達的頂點走回起點，而且走的是邊數最少的路徑。一次 BFS 就同時得到起點到所有可達頂點的最短距離，不必對每個目標各跑一次。</p>')}'''


# ---------------------------------------------------------------- P04 knight's tour
def knight():
    big = ('5×5 的棋盤深度是 25 層，平均分支因子 $k = 3.8$，搜尋樹的節點數約為 $3.8^{25} - 1$，也就是 $3.12 \\times 10^{14}$。'
           '6×6 的棋盤 $k = 4.4$，約有 $1.5 \\times 10^{23}$ 個節點；一般 8×8 的棋盤 $k = 5.25$，多達 $1.2 \\times 10^{46}$ 個。')
    return f'''<p>另一個經典問題叫<strong>騎士巡遊</strong>（knight's tour），可以用來說明第二種常見的圖演算法。這個謎題在西洋棋盤上只用一個棋子：騎士。目標是找出一串走法，讓騎士<strong>每一格恰好走過一次</strong>，這樣的一串走法稱為一個 <strong>tour</strong>。8×8 棋盤上合法的 tour 數量上限已知約為 $10^{{35}}$，而走到死路的走法更多。</p>
<p>研究者提出過很多解騎士巡遊的演算法，其中圖搜尋最容易理解、也最容易寫。同樣分兩步：</p>
{ul(['把騎士在棋盤上的合法走法表示成一張圖。',
     '用圖演算法找一條長度為 $rows \\times columns - 1$ 的路徑，圖中每個頂點恰好經過一次。'])}
<h3>建立騎士巡遊的圖</h3>
<p>用兩個想法把騎士巡遊表示成圖：棋盤的每一格是一個頂點，騎士的每一種合法走法是一條邊。</p>
{figure('knightmoves')}
{listing('講義程式：knightGraph', '講義 08 · knightGraph', KNIGHTGRAPH)}
<p><code>knightGraph()</code> 把整個棋盤走一遍。在每一格呼叫 <code>genLegalMoves()</code> 產生合法的目的地座標，每一種合法走法就存成一筆有向的相鄰資料。棋盤上的位置 (row, col) 轉成線性的頂點編號 <code>row * boardSize + col</code>，再轉成字串當作 key。</p>
<p><code>genLegalMoves()</code> 拿到騎士在棋盤上的位置，產生八種可能的走法，並確認每一種都還在棋盤裡：</p>
{listing('講義程式：genLegalMoves', '講義 08 · genLegalMoves', GENLEGALMOVES)}
{figure('bigknight')}
<p>上圖是 8×8 棋盤上所有可能走法構成的完整圖，圖中正好有 336 條邊。注意棋盤邊緣的頂點，連線（合法走法）比中間的頂點少。8×8 的相鄰矩陣有 4,096 格；這個表示法存了 336 筆<strong>有向</strong>的相鄰資料（每一種無向的合法走法兩個方向各存一次），等於 168 條無向邊，所以矩陣只會用到 8.2% 的格子。</p>
<h3>用 DFS 實作騎士巡遊</h3>
<p>解騎士巡遊用的搜尋演算法叫做<strong>深度優先搜尋</strong>（depth-first search, DFS）。廣度優先搜尋一次建立一層<strong>搜尋樹</strong>（search tree）；深度優先搜尋則是沿著樹的一個分支盡量往深處探索。</p>
<p>我們會看兩種 DFS 的實作。第一種專門解騎士巡遊，<strong>明確禁止同一個頂點被走兩次</strong>。第二種比較一般，建樹時允許頂點被多次檢查，後面幾節的演算法都以第二種為基礎。</p>
<p>深度優先的探索方式適合這個問題：找一條經過 64 個頂點（每格一個）、63 條邊的路徑。DFS 走到死路（圖中沒有任何可走的下一步）時，會沿著樹往回退到最近一個還有合法走法的頂點。</p>
<p><code>knightTour()</code> 有四個主要參數：<code>n</code> 是目前的深度；<code>path</code> 是 <code>vector&lt;string&gt;</code>，存已經走過的頂點 key；<code>uKey</code> 是正在探索的頂點；<code>limit</code> 是路徑要達到的深度。最後一個參數是圖本身。</p>
{listing('講義程式：knightTour（暴力 DFS）', '講義 08 · knightTour', KNIGHTTOUR)}
<p>這個函式是遞迴的。路徑達到要求的深度時回傳 <code>true</code>；否則找一個還沒走過的鄰居，往下一層遞迴，並回傳這個選擇最後能不能完成整個 tour。</p>
<p>DFS 同樣用顏色記錄哪些頂點走過：沒走過的是白色，走過的是灰色。如果某個頂點的所有鄰居都試過了，路徑卻還沒達到 64 個頂點，就是走到死路，必須<strong>回溯</strong>（backtrack）。遞迴呼叫回傳 <code>false</code> 時就會回溯：把 path 最後一個 key 移除，並把那個頂點塗回白色。遞迴的呼叫堆疊記住了哪些選擇還要重新考慮。</p>
<p>遞迴呼叫回傳 <code>false</code> 時，迴圈繼續試下一個白色鄰居；如果沒有任何鄰居能完成 tour，目前這次呼叫就把自己的頂點移出 path、塗回白色，然後回傳 <code>false</code>。</p>
<h3>小例子：在六個頂點上追蹤 knightTour</h3>
<p>為了方便追蹤，假設走訪 <code>neighbors</code> map 的順序就是 key 的順序。呼叫 <code>knightTour(1, path, "A", 6, g)</code>，觀察遞迴的選擇與回溯。A 的鄰居是 B 和 D，依 map 的順序先試 B；B 先試 C，走到死路。</p>
{figure('ktdfsc')}
<p>C 沒有白色鄰居，所以 C 的呼叫回傳 <code>false</code>，把 C 塗回白色，回到 B，再試下一個鄰居 D。之後搜尋要等所有必要的頂點都已經在 path 裡，才會再走到 C。這時 base case 的檢查成立，回傳 <code>true</code>，一路傳回每一層遞迴呼叫：</p>
{figure('ktdfsg')}
{steps('逐步圖：其餘四個步驟', ['ktdfsa', 'ktdfsb', 'ktdfse', 'ktdfsf'])}
<p>搜尋成功時，<code>vector&lt;string&gt; path</code> 的內容是 <code>[A, B, D, E, F, C]</code>，這就是每個頂點恰好走過一次的順序。</p>
<h3>在 5×5 棋盤上執行</h3>
<p>課程標頭另外提供 <code>printBoard</code>：不畫圖，而是把棋盤印成表格，每一格顯示騎士在第幾步走到這裡。<code>0</code> 是起點，5×5 的最後一步是 24，8×8 是 63。</p>
{listing('課程標頭的 printBoard', 'pythonds3/cppds/graph_algos.hpp · printBoard', HEADER_PRINTBOARD, kind='header')}
{lecture_program('講義完整程式：暴力 DFS 走 5×5 棋盤', '講義 08 · knightGraph + knightTour + printBoard', KT5_MAIN, OUT['kt5'],
                 note='從左上角 0 號格出發。沿著數字 0、1、2…… 找下去，每一步都是騎士的跳法，25 格各走過一次。')}
<p>每個騎士圖的頂點也帶著 BFS／DFS 用的記錄（color、previous），騎士巡遊用 color 避免重複走同一格。8×8 的棋盤用這個單純的 DFS 就沒有希望了，下面說明原因，並用 Warnsdorff 啟發式解決。</p>
<h3>騎士巡遊的分析</h3>
<p><code>knightTour()</code> 對「下一個要走哪個頂點」的選法非常敏感。單純的 DFS 演算法是指數時間 $O(k^N)$，$N$ 是棋盤的格數，$k$ 是一個不大的常數。用一棵樹來理解：根代表搜尋的起點，演算法從這裡產生並檢查騎士所有可能的走法。可能的走法數取決於騎士在棋盤上的位置：角落只有兩種，角落旁邊三種，棋盤中間八種。</p>
{figure('moveCount')}
<p>樹的下一層，同樣有 2 到 8 種可能的走法。要檢查的位置數，就是搜尋樹的節點數。</p>
{figure('8arrayTree')}
<p>每個節點最多有八個子節點，節點總數很大。因為每個節點的分支數不同，可以用<strong>平均分支因子</strong>估計：節點數是 $\\frac{{k^{{N+1}}-1}}{{k-1}}$，$k$ 是這個棋盤的平均分支因子，這個式子隨 $N$ 指數成長。</p>
<p>{big}</p>
<p>當然，問題有很多解，不必探索每一個節點；但真正要探索的比例只是一個常數倍，不會改變指數成長的本質。</p>
<h3>Warnsdorff 啟發式</h3>
<p><code>orderByAvail()</code> 依每個候選鄰居「還剩幾個白色鄰居」排序，先試剩下走法最少的那一格。這就是 Warnsdorff 規則，它讓 8×8 的情況變得實際可行，但最壞情況仍然是指數時間。</p>
{listing('講義程式：orderByAvail', '講義 08 · orderByAvail', ORDERBYAVAIL)}
<p>也許你會覺得這樣反而不利：為什麼不選剩下走法最多的那一格？選走法最多的頂點，騎士會傾向在一開始就走進棋盤中間；之後很容易被困在棋盤的一側，到不了另一側還沒走過的格子。先走剩下走法最少的格子，騎士會先繞著邊緣走，先把難到的角落處理掉，中間的格子留到必要時再拿來<strong>跳到棋盤的另一邊</strong>。利用這類知識來加速演算法，稱為<strong>啟發式</strong>（heuristic），這一個啟發式叫做 <strong>Warnsdorff 演算法</strong>。</p>
<p>講義把 <code>knightTour</code> 的迴圈改成依 <code>orderByAvail</code> 的順序走訪鄰居；標頭裡這個版本另外取名為 <code>knightTourWarnsdorff</code>，兩個版本可以並存：</p>
{listing('課程標頭的 knightTourWarnsdorff', 'pythonds3/cppds/graph_algos.hpp · knightTourWarnsdorff', HEADER_KTW, kind='header')}
{lecture_program('講義完整程式：Warnsdorff 走 8×8 棋盤', '講義 08 · orderByAvail + knightTourWarnsdorff', KT8_MAIN, OUT['kt8'],
                 note='同樣從 0 號格出發，64 格全部走過。比較四個角落：數字都很小或接近 0 的那一側先被走掉，這就是先處理邊角的效果。')}
<h3>互動：有沒有 Warnsdorff 差多少</h3>
<p>選棋盤大小，切換「使用 Warnsdorff」再按「開始」，比較兩種排序要回溯幾次。動畫裡關閉 Warnsdorff 時，候選格依列、行順序由小到大嘗試。</p>'''


# ---------------------------------------------------------------- P05 general DFS
def dfs_intro():
    return f'''<p>騎士巡遊用深度優先的回溯，找一條走過每一格的簡單路徑。一般的 DFS 目標不同：它探索每一個走得到的頂點，記錄一棵深度優先樹；再從每個還是白色的頂點重新開始，就得到一片<strong>深度優先森林</strong>（depth-first forest），森林裡的樹可以有很多分支。</p>
<p>一般的深度優先搜尋反而更簡單。它的目標是盡量往深處搜尋，在圖中連起越多頂點越好，必要時才分岔。DFS 也可能建出不只一棵樹，這一群樹就是深度優先森林。</p>
<h3>discovery 與 closing 時間</h3>
<p>和 BFS 一樣，DFS 用 previous 連結建構搜尋樹。此外，DFS 替每個頂點記錄兩個時間，存在 <code>DFSGraph</code> 的成員 <code>discovery</code> 與 <code>closing</code> 裡：</p>
{ul(['<strong>discovery</strong>：第一次遇到這個頂點之前，演算法走了幾步。',
     '<strong>closing</strong>：這個頂點塗成黑色之前，演算法走了幾步。'])}
<p>看完演算法之後會發現，這兩個時間有一些很有用的性質，後面的演算法會用到。</p>
{listing('講義程式：DFSGraph（dfs 與 dfsVisit）', '講義 08 · DFSGraph', DFSGRAPH_FULL)}
<p><code>dfs()</code> 和遞迴的輔助函式 <code>dfsVisit()</code> 共用同一個計時器 <code>time</code>，所以它們是 <code>DFSGraph</code> 的成員函式；<code>DFSGraph</code> 繼承 <code>Graph</code>，再加上 <code>time</code>、discovery 與 closing。標頭裡的 <code>dfs()</code> 另外在開始時把 <code>time</code> 歸零並清空兩個 map，同一張圖重跑也會得到一樣的結果。</p>
<p><code>dfs()</code> 先重設走訪狀態，再走過所有頂點，對每個還是白色的頂點呼叫 <code>dfsVisit()</code>，因此產生一片深度優先森林。要走過所有頂點，而不是只從一個指定的起點搜尋，是為了確保圖中每個頂點都被考慮到，沒有頂點被排除在森林之外。迴圈 <code>for (auto& p : vertices)</code> 走過圖自己的 <code>vertices</code> map：<code>p.first</code> 是頂點的 key，<code>p.second</code> 是 <code>Vertex</code> 物件。</p>
<p><code>dfsVisit(startKey)</code> 把一個頂點塗成灰色，盡量往深處遞迴探索它的白色鄰居，最後才把它塗成黑色。<code>dfsVisit()</code> 和 <code>bfs()</code> 用的是同一個顏色檢查，決定性的差別在排程：DFS 遇到白色鄰居立刻遞迴下去，BFS 則把它放進佇列等之後處理。BFS 把待辦的工作存在明確的佇列裡，遞迴的 <code>dfsVisit()</code> 則隱含地使用 C++ 的呼叫堆疊。</p>
<h3>互動：DFS 森林與時間戳記</h3>
<p>按「開始」跑完整的 <code>dfs()</code>，觀察呼叫堆疊與兩個時間怎麼變化。</p>'''


def dfs_trace():
    q = quiz('qBfsDfs', 'QUIZ · BFS 與 DFS 的結構差異', '追蹤「下一個要探索的頂點」時，BFS 和 DFS 在結構上的主要差別是什麼？', [
        (False, 'BFS 用堆疊，DFS 用佇列。', '剛好相反。'),
        (True, 'BFS 用佇列一層一層探索，DFS 用堆疊（通常透過遞迴）盡量往深處走。', 'BFS 用先進先出的佇列維持逐層的順序；DFS 用後進先出的堆疊，遞迴的呼叫堆疊就是現成的堆疊。'),
        (False, '兩者都必須用優先佇列，才能保證搜尋順序正確。', '優先佇列是 Dijkstra、Prim 這類處理權重的演算法在用的。'),
        (False, 'BFS 用 map 追蹤頂點，DFS 只用簡單的 vector。', '兩者都可以用 map 或 set 記錄走過的頂點；核心差別在排程用佇列還是堆疊。'),
    ])
    return f'''<h3>在小圖上追蹤 dfs</h3>
<p>下面的圖示範 DFS 在一張小圖上的執行過程。虛線代表檢查過、但另一端的頂點已經在深度優先樹裡的邊。搜尋從 A 開始，鄰居依字母順序造訪。A 的 discovery 是 1，接著 B 是 2、C 是 3；C 沒有鄰居，探索完畢，closing 是 4：</p>
{figure('gendfsd')}
<p>回到 B，B 剩下的鄰居只有 D，從 D 很快走到 E。E 的鄰居是 B 和 F，B 已經是灰色，走過去會繞圈，所以略過 B、改走 F。F 唯一的鄰居 C 已經是黑色，又到了一個分支的盡頭。之後演算法一路退回第一個頂點，沿途設定 closing 時間、把頂點塗黑：</p>
{figure('gendfsl')}
{steps('逐步圖：其餘十個步驟', ['gendfsa', 'gendfsb', 'gendfsc', 'gendfse', 'gendfsf', 'gendfsg', 'gendfsh', 'gendfsi', 'gendfsj', 'gendfsk'])}
<h3>括號性質</h3>
<p>各頂點的 discovery 與 closing 時間呈現出<strong>括號性質</strong>（parenthesis property）：在深度優先樹裡，一個頂點的所有子孫，discovery 時間都比它晚、closing 時間都比它早。把 discovery 看成左括號、closing 看成右括號，任兩個頂點的區間要嘛一個包住另一個，要嘛完全不重疊。</p>
{lecture_program('講義完整程式：印出 discovery、closing 與 previous', '講義 08 · DFSGraph', DFS_MAIN, OUT['dfs'],
                 note='每個頂點最後都是黑色。C 的 [3, 4] 包在 B 的 [2, 11] 裡，因為 C 是 B 的子孫；E→B 這條邊指向還是灰色的祖先 B，表示圖裡有循環。', did='dx-dfs')}
<h3>DFS 的分析</h3>
<p>不算遞迴裡掃描邊的時間，<code>dfs()</code> 的外層迴圈花 $O(|V|)$：重設時每個頂點走一次，建森林的迴圈也把每個頂點當成可能的根考慮一次。在 <code>dfsVisit()</code> 裡，每一筆有向的相鄰資料只會從它的起點被檢查一次，掃描鄰居的總時間是 $O(|E|)$。所以 DFS 的時間是 $O(|V|+|E|)$。</p>
{q}'''


# ---------------------------------------------------------------- P06 topological sort (optional)
def topsort():
    return f'''<h3>煎鬆餅的步驟圖</h3>
{figure('pancakes')}
<p>煎鬆餅的難處在於知道先做什麼。從圖上可以看到，可以先熱煎鍋，也可以先把任何一樣材料加進鬆餅粉。為了決定每個步驟的確切順序，我們用一個叫做<strong>拓撲排序</strong>（topological sort）的圖演算法。拓撲排序把一張 DAG 的所有頂點排成一條線性順序：只要圖中有邊 $(v, w)$，$v$ 就排在 $w$ 前面。DAG 常用來表示<strong>事件的先後順序</strong>，煎鬆餅只是一個例子，其他例子還有軟體專案的排程、資料庫查詢最佳化的優先順序圖，以及矩陣連乘。</p>
{figure('pancakesTS')}
{steps('DFS 在鬆餅圖上的結果', ['pancakesDFS'], '依 closing 時間由大到小排列，就得到上面那一列順序：所有的模糊都消除了，每個步驟該在什麼時候做一清二楚。')}
{fold('用 DFSGraph 寫出拓撲排序', snippet('拓撲排序：照演算法的三個步驟寫', TOPSORT_SUPP, OUT['topsort'], kind='run',
      note='每一行是「discovery/closing　步驟」。C++ 的 map 依 key 排序，dfs() 從 "1 Tbl oil" 開始，所以時間和上面的圖不同，順序也不同；但每條邊仍然從前面指向後面，同樣是合法的做法。拓撲排序通常不只一種。'))}
<h3>互動：先跑 DFS，再依 closing 排序</h3>'''


# ---------------------------------------------------------------- P07 SCC (optional)
def scc():
    return f'''<h3>講義的例圖</h3>
<p>下圖是一張有三個強連通元件的簡單圖，不同深淺的區域就是不同的元件。</p>
{figure('scc1')}
<p>找出強連通元件之後，把同一個元件的頂點合併成一個大頂點，就能畫出簡化的圖。對這張圖照上面四個步驟走一遍：第一次 DFS 得到每個頂點的 closing 時間，第二次在轉置圖上依 closing 時間由大到小挑起點，最後得到三棵樹。</p>
{steps('逐步圖：簡化圖與兩次 DFS 的時間', ['scc2', 'scc1a', 'scc1b'])}
{figure('sccforest')}
<p>下方的互動圖用另一張八個頂點的圖示範同樣的三個步驟。</p>
<h3>互動：三個步驟走一遍</h3>'''


# ---------------------------------------------------------------- P08 shortest paths / Dijkstra
def dij_intro():
    q = quiz('qBfsShortest', 'QUIZ · BFS 為什麼找得到最短路徑', '為什麼在沒有權重的圖上，BFS 保證找到最短路徑？', [
        (True, '它先探索完所有距離起點 k 的頂點，才前進到距離 k+1 的頂點。', 'BFS 一圈一圈往外擴散，第一次碰到目標時，走的一定是最短的路徑。'),
        (False, '它總是先選權重最小的邊。', 'BFS 用在沒有權重的圖，所有邊都一樣。'),
        (False, '它用貪婪策略剪掉太長的路徑。', 'BFS 不依長度剪枝，只是一層一層把所有可能都走過。'),
        (False, '它只在最短路徑確認之後，才把頂點塗成黑色。', '頂點變黑只代表它的鄰居都探索完了。'),
    ])
    return f'''<h3>最短路徑問題</h3>
<p>上網、寄電子郵件，或從校園另一端登入實驗室的電腦時，背後有很多工作在把你電腦上的資料傳到另一台電腦。資訊在網際網路上怎麼流動，是計算機網路課程的主題。</p>
{figure('Internet')}
<p>上圖是網際網路通訊的高階概觀。用瀏覽器向伺服器要一個網頁時，請求必須經過區域網路，再透過路由器送上網際網路。網際網路上的每台路由器都連到一台或多台其他路由器。在一天中的不同時間執行 <code>traceroute</code> 指令，很可能看到資料在不同時間經過不同的路由器，因為每對路由器之間的連線都有成本，而成本取決於流量、時段等許多因素。</p>
<p>所以路由器組成的網路可以表示成一張<strong>加權圖</strong>。下圖是表示網際網路路由器連線的小例子。要解決的問題是：找出總權重最小的路徑，用來傳送任何一則訊息。</p>
{figure('routeGraph')}
<p>這個問題應該很眼熟：它和用 BFS 解的問題很像，只是這裡在乎的是路徑的總權重，而不是經過幾個路由器。如果所有權重都相同，兩個問題就是同一個。</p>
{q}
<h3>Dijkstra 演算法</h3>
<p><strong>Dijkstra 演算法</strong>是一個迭代的演算法，求出從某一個起點到圖中其他所有頂點的最短路徑，結果同樣和 BFS 很像。</p>
<p>為了記錄從起點到每個目的地的總成本，我們使用 <code>Vertex</code> 類別的 <code>distance</code>，它存著目前已知、從起點到這個頂點的最小總權重。演算法對圖中每個頂點各迭代一次，但迭代的順序由<strong>優先佇列</strong>（priority queue）控制，決定順序的值就是 distance。</p>
<p>優先佇列和佇列一樣，從前端取出項目；但項目在佇列裡的邏輯順序由優先權決定，優先權最高的在最前面、最低的在最後面。所以放進一個新項目時，它可能一路移到最前面。</p>
<p>頂點剛建立時，distance 設成一個非常大的數。理論上應該設成無限大，實務上只要設成比問題中任何真實距離都大的數，課程的標頭用的是 <code>INT_MAX</code>。C++ 用標準的 <code>priority_queue</code> 當作 min-heap：它存 <code>(distance, key)</code> 的 pair，加上 <code>greater&lt;&gt;</code> 之後，每次都先取出距離最小的那一筆。</p>
<div class="info-box warm">
    <span class="info-label">前提：權重不可為負</span>
    Dijkstra 的正確性要求每條邊的權重都<strong>不是負數</strong>；權重為 0 的邊沒有問題。負權重的邊可能在某個頂點已經被當成確定之後，才顯示出一條更短的路，貪婪的證明就不再成立。這不代表程式一定會跑不停，而是結果不再有保證。課程的實作會拒絕負權重。
</div>
{fold('有負權重時改用什麼', '<p>邊權重可以是負數、但圖中沒有負循環時，可以改用 Bellman-Ford 演算法：它對所有邊重複做 |V| − 1 輪鬆弛，時間是 O(|V||E|)。如果第 |V| 輪還能讓某個距離變小，就表示圖中有負循環，最短路徑沒有定義。</p>')}'''


def dij_run():
    q = quiz('qDijk', 'QUIZ · Dijkstra 的特性', '下列哪一個是 Dijkstra 演算法已知的限制或特性？', [
        (False, '它能正確找出含負權重邊的圖上的最短路徑。', 'Dijkstra 要求權重不是負數；權重 0 可以，但負權重會讓貪婪的確定步驟失效。'),
        (True, '它是迭代的演算法，求出從一個起點到其他所有可達頂點的最短路徑。', 'lazy 的 C++ 版本反覆取出最小的候選距離，並略過被後來的改善取代的過期項目。'),
        (False, '它的時間複雜度與圖的邊數無關。', '複雜度是 O((|V| + |E|) log |V|)，同時取決於頂點數與邊數。'),
        (False, '用在路由時，它不需要整張網路的地圖。', '要在路由上使用 Dijkstra，每台路由器都得有完整的網路地圖。'),
    ])
    ex1 = quiz('ex1', 'EXERCISE 1 · 負權重的前提', '下圖有負權重的邊。把它傳給課程的 <code>dijkstra(g, "A")</code> 會發生什麼事？', [
        (False, '回傳 A → B → D', '課程的 dijkstra 不會在負權重的圖上執行優先佇列的走訪，也就不會產生任何路徑。'),
        (False, '回傳 A → C → D', 'A → C → D 的總權重 7 + (−5) = 2 確實比 A → B → D 的 4 小，但函式在開始走訪之前就拒絕了這張圖。'),
        (False, '自動刪掉負權重的邊再繼續', '程式不會修改輸入的圖，只檢查前提是否成立。'),
        (True, '在開始優先佇列的走訪之前，丟出 invalid_argument', '多推入幾筆 pair 的 lazy 寫法，不會讓 Dijkstra 能處理負權重；實作在重設距離時就檢查每條邊，看到負權重立刻丟出例外。'),
    ], extra=figure('Dij') + '\n')
    return f'''<h3>講義的 dijkstra</h3>
{listing('講義程式：dijkstra', '講義 08 · dijkstra', DIJKSTRA)}
<p>本課程的 C++ 實作使用 <strong>lazy 優先佇列</strong>。鬆弛（relaxation）讓某個距離變小時，直接推入一筆新的 <code>(distance, key)</code>，不去 heap 裡找舊的那一筆；之後舊的、比較大的那一筆到了最上面，演算法認出它已經過期，直接略過。</p>
<p>因此同一個頂點可能在優先佇列裡有好幾筆。每一筆都同時帶著暫定距離與頂點的 key，取出最小的那筆時，仍然知道要處理哪個頂點。取出 <code>(queuedDistance, key)</code> 之後，把 <code>queuedDistance</code> 和這個頂點目前存的距離比較；比較大就表示後來的鬆弛已經取代了這一筆，直接略過，不掃描它的相鄰 map。</p>
<p>這個版本沒有 <code>changePriority()</code>。每次成功的鬆弛只做一次 heap push，所以最多推入 $O(|E|)$ 筆，取出的次數也一樣。標頭裡的版本在一開始還會把每個頂點的距離重設為 <code>INT_MAX</code>，並檢查每條邊的權重：</p>
{snippet('graph_algos.hpp · dijkstra 開頭的重設與檢查', HEADER_DIJ_CHECK, kind='fragment')}
<h3>在路由圖上追蹤 Dijkstra</h3>
<p>從 $u$ 開始，<code>distance = 0</code>；其他頂點一開始都是 <code>INT_MAX</code>（還走不到）。鬆弛 $u$ 的每條邊，鄰居第一次得到有限的候選距離，並把 $u$ 記為前一個頂點：</p>
{figure('dijkstraa')}
<p>接下來 $x$ 的總成本最低，所以浮到優先佇列的最前面。取出 $x$ 時檢查它的鄰居 $u$、$v$、$w$、$y$：鬆弛讓 $y$ 第一次得到有限的距離，也讓 $w$ 的候選距離變小。lazy 佇列推入改善後的 pair；被取代的、比較大的那筆，之後到了最上面就被略過。下一步看 $v$ 的鄰居，圖沒有任何變化，於是換到 $y$。在 $y$ 發現到 $w$ 和 $z$ 都更便宜，就調整距離與 previous。最後檢查 $w$ 和 $z$，沒有新的變化，優先佇列也空了，演算法結束。</p>
{steps('逐步圖：依序處理 x、v、y、w', ['dijkstrab', 'dijkstrac', 'dijkstrad', 'dijkstrae'])}
{figure('dijkstraf')}
{lecture_program('講義完整程式：每個頂點的距離與 previous', '講義 08 · dijkstra', DIJ_MAIN, OUT['dij'],
                 note='格式是「頂點: 距離 (previous)」。w 的直達成本是 5，最後降到 3，走的是 u→x→y→w。', did='dx-dij')}
<p>現在每個頂點都存著從 <code>u</code> 出發的<strong>最短</strong>路徑長度，沿 <code>previous</code> 往回走就能重建那條路徑。標頭的 <code>findPath</code> 做的就是這件事：從終點沿 previous 走回起點，再把結果反轉。</p>
{listing('課程標頭的 findPath', 'pythonds3/cppds/graph_algos.hpp · findPath', HEADER_FINDPATH, kind='header')}
{lecture_program('講義完整程式：用 findPath 取出 u 到 z 的路徑', '講義 08 · dijkstra + findPath', DIJ_PATH_MAIN, OUT['dij_path'],
                 note='u 到 z 的最短路徑經過 x 和 y，總長 1 + 1 + 1 = 3。')}
<p>網際網路上實際傳送訊息時，用的是其他找最短路徑的演算法。在網際網路上用 Dijkstra 的一個問題是：演算法執行時需要整張圖的完整表示，也就是每台路由器都要有網際網路上所有路由器的完整地圖。實際上並非如此，其他變形的演算法讓每台路由器邊走邊認識這張圖。</p>
<h3>Dijkstra 的分析</h3>
<p>在 lazy 的 C++ 實作中，重設所有頂點的距離花 $O(|V|)$，一開始只推入 <code>(0, start)</code>。掃描相鄰 map 時，每條有向邊只在有效的展開中被檢查一次。每次成功的鬆弛新增一筆 heap 項目，所以最多 $O(|E|)$ 次 push 與 pop。一次 heap 操作花 $O(\\log |E|) = O(\\log |V|)$（在這種簡單、沒有重複邊的圖上 $|E| \\le |V|^2$），有序 map 查詢頂點也是同樣的對數。總時間是 $O((|V|+|E|)\\log |V|)$，空間（含過期的項目）是 $O(|V|+|E|)$。</p>
{q}
<h3>練習 1：負權重的前提</h3>
{ex1}
{fold('實際執行練習 1 的圖', snippet('練習 1 · 把含負權重的圖交給 dijkstra', EX1_SUPP, OUT['ex1'], kind='run',
      note='dijkstra 在重設距離的迴圈裡就看到 C→D 的權重 −5，丟出 invalid_argument，catch 印出例外的訊息。'))}'''


# ---------------------------------------------------------------- P09 Prim
def prim_intro():
    return f'''<h3>廣播問題</h3>
<p>最後一個圖演算法，來看線上遊戲設計者的一個問題：他們要有效率地把一則訊息傳給所有可能在收聽的人。這在遊戲裡很重要，所有玩家才知道其他玩家的最新位置。</p>
{figure('bcast1')}
<p>這個問題有幾種暴力解法。廣播主機有一份所有聽眾都要收到的資訊，最簡單的做法是主機記住所有聽眾，對每個人各送一份訊息。上圖是一個小網路，有一個廣播主機和幾位聽眾；用這個做法，每則訊息要送四份。假設都走<strong>成本最低的路徑</strong>，來看每台路由器會處理同一則訊息幾次。</p>
<p>廣播主機送出的訊息都經過路由器 A，所以 A 會看到每則訊息的全部四份。路由器 C 只看到一份，是給它的聽眾的。但 B 和 D 會看到三份，因為它們都在聽眾 1、2、4 的<strong>最便宜路徑</strong>上。廣播電台每秒要送出上百則訊息，這會多出很多流量。</p>
<p>另一種暴力解法是廣播主機只送出一份訊息，讓路由器自己處理。最簡單的做法叫做<strong>無控制氾濫</strong>（uncontrolled flooding）：每則訊息一開始帶有一個存活時間（time to live，<code>TTL</code>），設成大於或等於廣播主機到最遠聽眾之間的邊數。每台路由器收到訊息後，轉送給所有相鄰的路由器，轉送時把 TTL 減一。因為每台路由器都持續把訊息轉送給所有鄰居，直到 TTL 變成 0，不難相信這樣產生的多餘訊息比第一種做法還要多得多。</p>
<h3>最小生成樹</h3>
<p>解決辦法是建立一棵最小權重的<strong>生成樹</strong>（spanning tree）。正式定義圖 $G = (V, E)$ 的最小生成樹 $T$：$T$ 是 $E$ 的一個無循環子集合，連接 $V$ 中所有頂點，而且 $T$ 中邊的權重總和最小。下圖是廣播圖的簡化版，標出了構成最小生成樹的邊。</p>
{figure('mst1')}
<p>解決廣播問題時，廣播主機只要送一份訊息進網路。每台路由器把訊息轉給生成樹上的鄰居，但不轉回剛送訊息給它的那個鄰居。在這個例子裡，A 把訊息轉給 B，B 轉給 D 和 C，D 轉給 E，E 轉給 F，F 轉給 G。沒有任何路由器看到同一則訊息兩次，所有想收聽的聽眾都收到了。</p>
<h3>Prim 演算法</h3>
<p>Prim 演算法用在有權重的<strong>無向</strong>圖上，是一個貪婪演算法。每一步它都選一條<strong>安全邊</strong>（safe edge）：在「已經在樹裡的頂點」與「還在樹外的頂點」之間，跨過這條分界（cut）的最小權重邊。全圖其他地方最便宜的邊，不一定有資格被選。</p>
<div class="pseudo-code gr-ladder">While T is not yet a spanning tree
  Find an edge that is safe to add to the tree
  Add the new edge to T</div>
<p>關鍵在於找安全邊：在所有從目前的樹跨到樹外頂點的邊當中，Prim 選權重最小的一條。跨過分界的邊能保持連通又不會形成循環；cut 性質則保證這個最小權重的選擇可以屬於某一棵最小生成樹。</p>
<p>課程的 <code>prim()</code> 要求整張圖是一個連通元件、包含所有頂點。lazy 優先佇列清空之後，它比較加進樹裡的頂點數和 <code>g.vertices.size()</code>，圖不連通時就丟出 <code>invalid_argument</code>。</p>
{listing('講義程式：prim', '講義 08 · prim（完整版在 graph_algos.hpp）', PRIM_FULL)}
<p>和 Dijkstra 比較：Prim 的 <code>newDistance</code> 只是<strong>一條邊</strong>的權重 <code>n.second</code>，不是從起點累加的路徑長度；另外用 <code>inTree</code> 記錄哪些頂點已經從佇列取出、正式進入樹中。</p>
<h3>互動：一步一步長出最小生成樹</h3>'''


def prim_run():
    q1 = quiz('qPrimSafe', 'QUIZ · 什麼是安全邊', '用 Prim 演算法建立最小生成樹時，「安全邊」是指什麼？', [
        (False, '任何加進目前的樹之後不會形成循環的邊。', 'Prim 的安全邊必須跨過目前的樹與樹外頂點之間的分界，而且是其中權重最小的。'),
        (True, '從目前的樹跨到樹外某個頂點的邊當中，權重最小的那一條。', '這就是 Prim 每一步用 cut 性質做出的貪婪選擇。'),
        (False, '權重比全圖邊權重平均值還低的邊。', '演算法看的是目前分界上權重最小的連線，不是平均值。'),
        (False, '對圖做深度優先搜尋時第一條遇到的邊。', 'Prim 和 DFS 是不同的演算法，它依權重決定下一條邊。'),
    ])
    q2 = quiz('qPrimDisc', 'QUIZ · 不連通的圖', '課程的 <code>prim(g, start)</code> 遇到不連通的圖時會怎麼做？', [
        (False, '不說一聲，回傳一片最小生成森林。', '那是另一種約定；這個函式要求一棵包含所有頂點的生成樹。'),
        (False, '自己加上邊，把不同的元件連起來。', 'Prim 只能選圖中已經存在的邊，沒辦法連起分開的元件。'),
        (True, '發現不是每個頂點都進入樹之後，丟出 invalid_argument。', '不連通的圖沒有生成樹，回傳型別是 void 的函式用例外回報前提不成立。'),
        (False, '永遠等待下一筆優先佇列的項目。', 'lazy 佇列最後會清空，之後程式明確檢查連通性。'),
    ])
    return f'''<h3>在廣播圖上追蹤 Prim</h3>
<p>從 A 開始，其他頂點的 key 都初始化為無限大。看 A 的鄰居，B 和 C 經過 A 的成本小於無限大，所以更新它們的 key。這讓 B 和 C 移到優先佇列的前面，並把它們的 previous 設為 A。要注意的是，B 和 C 還沒有正式加入生成樹：<strong>頂點要從優先佇列取出之後，才算是生成樹的一部分</strong>。</p>
{figure('prima')}
<p>B 的距離最小，所以接著看 B。檢查 B 的鄰居，D 和 E 可以更新，兩者都得到新的距離，previous 也跟著更新。佇列裡的下一個是 C，C 的鄰居中還在佇列裡的只有 F，於是更新 F 的距離。接著檢查 D 的鄰居，發現 E 的距離可以從 4 降到 1，E 的 previous 改指向 D，準備接到生成樹的另一個位置。之後的過程就照這樣，把每個新頂點加進樹裡。</p>
{steps('逐步圖：依序加入 B、C、D、E、F', ['primb', 'primc', 'primd', 'prime', 'primf'])}
{figure('primg')}
{lecture_program('講義完整程式：prim 印出最小生成樹的邊', '講義 08 · prim', PRIM_MAIN, OUT['prim'],
                 note='每一組是 (previous, 頂點)。印出的邊組成以 A 為根的最小生成樹，是反覆選擇「跨過目前樹邊界的最便宜邊」得到的，總權重 7。', did='dx-prm')}
{fold('Prim 的時間複雜度', '<p>結構和 lazy 的 Dijkstra 相同：每個頂點從佇列正式取出一次，每條有向邊在它的起點進樹時檢查一次，每次成功的更新推入一筆 heap 項目。總時間同樣是 O((|V| + |E|) log |V|)。</p>')}
{q1}
{q2}'''


# ---------------------------------------------------------------- exercises
def exercises():
    ex2 = quiz('ex2', 'EXERCISE 2 · Prim 從 F 出發', '下面這張圖用 Prim 演算法、<strong>從頂點 F 出發</strong>，最後一條加入最小生成樹的邊，權重是多少？', [
        (False, '3', '權重 3 的 G–E 是第四條加入的邊，之後還有 E–D 與 G–C。'),
        (False, '4', '權重 4 的 E–D 是第五條加入的邊，最後還剩 C 沒有進樹。'),
        (True, '5', 'C 最後才進樹。G 進樹時把 C 的 key 從 7（經 B）降成 5（經 G），之後 D 進樹時 D–C 的 6 不比 5 小，所以最後一條邊是 G–C，權重 5。'),
        (False, '6', 'D–C 的權重 6 比 C 當時的 key 5 大，不會被選進樹。'),
    ], extra=figure('primq') + '\n')
    trace = table(['步驟', '取出', '加入的邊', 'key 的更新'], [
        ['1', 'F（起點）', '—', 'A = 8、E = 9'],
        ['2', 'A', 'F–A (8)', 'B = 1、G = 2'],
        ['3', 'B', 'A–B (1)', 'C = 7'],
        ['4', 'G', 'A–G (2)', 'C 由 7 降為 5、E 由 9 降為 3'],
        ['5', 'E', 'G–E (3)', 'D = 4'],
        ['6', 'D', 'E–D (4)', 'D–C 的 6 不比 5 小，不更新'],
        ['7', 'C', 'G–C (5)', '—'],
    ])
    return f'''<h3>練習 2：最後一條邊</h3>
{ex2}
{details('看完整的追蹤', trace + '<p>最小生成樹的總權重是 8 + 1 + 2 + 3 + 4 + 5 = 23。原因是 Prim 的更新規則只看單一條邊的權重：G 進樹時，C 改由 G–C（5）連進來，比原本的 B–C（7）便宜。</p>')}'''


# ---------------------------------------------------------------- reference
def reference_extra():
    bfs_dfs = table(['面向', 'BFS', 'DFS'], [
        ['探索順序', '按距離由近到遠，一層一層', '沿一條分支走到底，再回退'],
        ['資料結構', 'FIFO 佇列', 'LIFO 堆疊（遞迴的呼叫堆疊）'],
        ['最短路徑', '<span class="best">沒有權重的圖直接得到</span>', '不保證'],
        ['記憶體', '$O(|V|)$（最寬的一層）', '$O(|V|)$（最深的路徑）'],
        ['典型應用', '最少步數、分層結構', '拓撲排序、強連通元件、偵測循環、回溯'],
        ['產生的樹', 'BFS 樹', '深度優先森林（可能多棵樹）'],
    ])
    dij_prim = table(['面向', 'Dijkstra', 'Prim'], [
        ['解決的問題', '單一起點的最短路徑', '最小生成樹'],
        ['更新規則', '<code>d(u) + w(u,v)</code>，累加整條路徑', '<code>w(u,v)</code>，只看一條邊'],
        ['結果的意義', '每個頂點到起點的最短距離', '連通所有頂點、總權重最小的邊集合'],
        ['權重限制', '<span class="worst">不可為負</span>', '可以為負'],
        ['有向／無向', '都可以', '無向圖'],
    ])
    return fold('BFS 與 DFS 行為對照', bfs_dfs) + fold('Dijkstra 與 Prim 的差異', dij_prim)


# ---------------------------------------------------------------- recap
def recap():
    qa = [
        ('為什麼 BFS 的路徑和題目開頭的解法不一樣？',
         '<p>從 fool 到 sage 有不只一條 6 步的路徑。BFS 保證找到的路徑步數最少，但同樣短的路徑有好幾條時，它找到哪一條取決於鄰居的走訪順序。C++ 的 map 依 key 排序，page 比 sale 先被處理，所以 sage 的 previous 是 page。</p>'),
        ('DFS 為什麼不能保證找到最短路徑？',
         '<p>DFS 第一次碰到某個頂點時，走的是目前這條分支，可能繞了很遠；它不像 BFS 那樣先把近的頂點全部處理完。要找最少邊數的路徑用 BFS，邊有權重時用 Dijkstra。</p>'),
        ('騎士巡遊用了 Warnsdorff 就一定很快嗎？',
         '<p>Warnsdorff 只是改變嘗試的順序，讓搜尋通常很快找到解；遇到不幸的情況，回溯仍然可能非常多，最壞情況還是指數時間。啟發式加快的是常見情況，不改變最壞情況的保證。</p>'),
        ('Dijkstra 的佇列裡同一個頂點出現好幾次，不會出錯嗎？',
         '<p>不會。每一筆都帶著推入時的距離；取出時如果這個距離比頂點目前存的距離大，代表後來已經找到更短的路，這筆就是過期的，直接略過。只有和目前距離相同的那一筆會真正展開鄰居。</p>'),
        ('Prim 和 Dijkstra 的程式幾乎一樣，結果差在哪裡？',
         '<p>差在 newDistance 的算法。Dijkstra 用 d(u) + w(u, v)，每個頂點存的是到起點的總距離；Prim 只用 w(u, v)，每個頂點存的是把它接上樹的那條邊的權重。同一張圖，最短路徑樹和最小生成樹不一定相同。</p>'),
    ]
    faq = ''.join(details(f'{q}（補充）', a, cls='gr-detail gr-faq') for q, a in qa)
    return f'''<ul class="gr-ul gr-recap">
<li>圖 $G = (V, E)$ 由頂點與邊組成，邊可以有方向與權重。路徑的頂點互不相同；循環是回到起點的封閉路徑；沒有循環的有向圖叫 DAG。</li>
<li>相鄰矩陣用 $|V|^2$ 格，適合很密的圖；本章的問題都很稀疏，所以用相鄰串列：<code>vertices</code> 與 <code>neighbors</code> 兩層 map，空間 $O(|V|+|E|)$。</li>
<li>Word ladder：用 bucket（把一個字母換成底線）找出只差一個字母的單字建圖，再用 BFS 找最少的步數。</li>
<li>BFS 用佇列，一層一層往外擴散；白、灰、黑三色記錄進度，previous 構成 BFS 樹，traverse 沿 previous 走回起點。時間 $O(|V|+|E|)$。</li>
<li>騎士巡遊：棋盤格是頂點、合法走法是邊；knightTour 用 DFS 加回溯找走過每一格的路徑，單純的搜尋是指數時間，Warnsdorff 先走剩下走法最少的格子，讓 8×8 變得可行。</li>
<li>一般的 DFS（<code>DFSGraph</code>）從每個白色頂點出發建立深度優先森林，記錄 discovery 與 closing 時間，兩者滿足括號性質。時間 $O(|V|+|E|)$。</li>
<li>拓撲排序：對 DAG 跑 dfs()，依 closing 時間由大到小排列。強連通元件：G 上跑 dfs()、建轉置圖、在轉置圖上依 closing 時間遞減再跑一次，每棵樹就是一個元件。</li>
<li>Dijkstra：權重不可為負，用 lazy 優先佇列反覆取出距離最小的頂點並鬆弛它的邊，略過過期的項目；時間 $O((|V|+|E|)\\log|V|)$，用 findPath 沿 previous 取出路徑。</li>
<li>Prim：在連通的無向加權圖上，每一步加入跨過「樹內／樹外」分界的最小權重邊；更新規則只看單一條邊的權重。最小生成樹解決廣播時重複傳送的問題。</li>
</ul>
<h3>常見疑問</h3>
{faq}'''


def sections():
    return {
        'graphs-prologue': prologue(),
        'graphs-prologue-legend': prologue_legend(),
        'graphs-rep-adt': rep_adt(),
        'graphs-rep-impl': rep_impl(),
        'graphs-wl': word_ladder(),
        'graphs-bfs-intro': bfs_intro(),
        'graphs-bfs-trace': bfs_trace(),
        'graphs-knight': knight(),
        'graphs-dfs-intro': dfs_intro(),
        'graphs-dfs-trace': dfs_trace(),
        'graphs-topsort': topsort(),
        'graphs-scc': scc(),
        'graphs-dij-intro': dij_intro(),
        'graphs-dij-run': dij_run(),
        'graphs-prim-intro': prim_intro(),
        'graphs-prim-run': prim_run(),
        'graphs-exercises': exercises(),
        'graphs-ref-extra': reference_extra(),
        'graphs-recap': recap(),
    }


STYLE = """<style id="graphs-depth-style">
.gr-detail{margin:1rem 0;border:1px solid var(--card-border);border-radius:8px;background:var(--card);}
.gr-detail>summary{cursor:pointer;padding:.9rem 1rem;font-weight:600;line-height:1.6;}
.gr-detail-body{padding:0 1rem 1rem;min-width:0;}
.gr-detail-body .pseudo-code{max-width:100%;overflow-x:auto;}
.deck-extra .pseudo-code{max-width:100%;overflow-x:auto;}
.side-panel .pseudo-code{max-width:100%;overflow-x:auto;}
.gr-ul{padding-left:1.4rem;margin:.6rem 0 1rem;}
.gr-ul li{margin:.3rem 0;line-height:1.8;}
.gr-skip{font-size:.88rem;color:var(--muted);}
.gr-ladder{font-size:.85rem;background:var(--card);color:var(--ink);border:1px solid var(--card-border);white-space:pre;}
.viz-layout{min-width:0;}
.viz-layout>div{min-width:0;}
.quiz-opt .opt-text{min-width:0;overflow-wrap:anywhere;}
.quiz-box .gr-figure{max-width:560px;}
.slider-row{flex-wrap:wrap;}
.slider-row select{max-width:100%;}
</style>"""
