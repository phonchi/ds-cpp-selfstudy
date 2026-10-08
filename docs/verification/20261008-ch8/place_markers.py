"""One-time hand edits on graphs.html (run after reorder_sections.py):
place the <!-- gen:graphs-* --> markers, drop the blocks the old enrich_graphs.py injected (dx-rep, dx-bfs,
dx-dfs, dx-dij, dx-prm) and the hand-written passages now regenerated from content/graphs_depth.py,
rename the animation code panels to the lecture names (data-l values kept so the JS highlighting still
lines up), give the existing quizzes per-option feedback and a fourth option, replace the redrawn
exercise graphs (JS renderers removed; the lecture images come from the gen blocks), add the recap
section and its navigation entries.
Usage: python3 place_markers.py [PATH]   (default: graphs.html in the repo)
"""
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/enrich'))
from enrich_lib import hl  # noqa: E402

P = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'graphs.html'
s = P.read_text()
if '<!-- gen:graphs-prologue -->' in s:
    sys.exit('gen markers already placed; this one-time script must not run again')
order = re.findall(r'<section id="([\w-]+)">', s)
assert order[:10] == ['prologue', 'representation', 'word-ladder', 'bfs', 'knight', 'dfs', 'topsort', 'scc',
                      'dijkstra', 'prim'], 'run reorder_sections.py first'


def gen(name):
    return f'<!-- gen:{name} -->\n<!-- /gen:{name} -->'


def once(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f'expected {count} match(es), got {n}: {old[:90]!r}')
    s = s.replace(old, new)


def cut(start, end, new):
    """Replace from the unique start text through the first end text after it (inclusive)."""
    global s
    assert s.count(start) == 1, start
    i = s.index(start)
    j = s.index(end, i) + len(end)
    s = s[:i] + new + s[j:]


def section_span(sid):
    i = s.index(f'<section id="{sid}">')
    return i, s.index('</section>', i)


def cut_in(sid, start, end, new):
    """cut() restricted to one section."""
    global s
    a, b = section_span(sid)
    i = s.index(start, a)
    assert i < b and s.count(start, a, b) == 1, (sid, start)
    j = s.index(end, i) + len(end)
    assert j <= b, (sid, end)
    s = s[:i] + new + s[j:]


# ================================================================ P00 prologue
once('''如果有權重就寫成 $(v, w, c)$。</p>

  <h3>路徑、循環、樹、DAG</h3>''', '''如果有權重就寫成 $(v, w, c)$。</p>
''' + gen('graphs-prologue') + '''

  <h3>互動：標出路徑與循環</h3>''')
cut_in('prologue', '  <h3>頂點的三色狀態（後續演算法都會用到）</h3>', '一步一步觀察。</p>\n', gen('graphs-prologue-legend') + '\n')

# ================================================================ P01 representation
cut_in('representation', '  <p>本課程的 <code>Graph</code> 以 <code>setVertex(key)</code>', '</p>\n', gen('graphs-rep-adt') + '\n')
cut_in('representation', '  <h3>C++ 實作：Vertex 與 Graph 類別', '''  <p class="dx-note">每組 (from, to, weight) 對應一條有向邊，addEdge 會補上不存在的頂點。ordered map 查頂點為 O(log |V|)、查特定鄰邊為 O(log deg(v))。</p>
</div>
''', gen('graphs-rep-impl') + '\n')

# ================================================================ P02 word ladder
cut_in('word-ladder', '  <p><strong>Word Ladder</strong>：把一個單字一次改一個字母', '''    每個 bucket 內部的所有單字兩兩相連 → 所有「只差一個字母」的單字對都被連上了！
  </div>
''', gen('graphs-wl') + '\n')

# ================================================================ P03 BFS
a, b = section_span('bfs')
i = s.index('  <div class="viz-layout">', a)
s = s[:i] + gen('graphs-bfs-intro') + '\n\n' + s[i:]
cut_in('bfs', '''  <div class="info-box warm">
    <span class="info-label">為什麼是 $O(|V|+|E|)$？</span>''', '''一次 BFS 同時得到起點到「所有可達頂點」的最短距離，不需要重新跑 $|V|$ 次！
  </div>
''', gen('graphs-bfs-trace') + '\n')
cut_in('bfs', '<h3 id="dx-bfs">講義完整範例：Word Ladder 的實際執行</h3>', '''任何可達單字回溯到 fool 都是最短路。</p>
</div>
''', '')

# ================================================================ P04 knight
cut_in('knight', '  <p><strong>騎士巡邏</strong>：在 $n \\times n$ 棋盤上', '''    <strong>下一步永遠選「可走鄰居最少」的格子</strong>。
  </div>
''', gen('graphs-knight') + '\n')
cut_in('knight', '''  <div class="info-box">
    <span class="info-label">為什麼選「鄰居最少」而不是「最多」？</span>''', '''這就是 Warnsdorff 規則奏效的根本原因。
  </div>
''', '')

# ================================================================ P05 DFS
cut_in('dfs', '  <p>BFS 一層一層擴散，<strong>深度優先搜尋', '''每個子節點的 [discovery, closing] 區間都完全嵌套在父節點的區間內。
  </div>
''', gen('graphs-dfs-intro') + '\n')
once('<span class="info-label">為什麼要走訪所有頂點？(line 4)</span>', '<span class="info-label">為什麼要走訪所有頂點？</span>')
once('外層 <code>for v : graph</code> 確保每個白色頂點都會啟動一次 <code>dfsVisit</code>',
     '外層 <code>for (auto&amp; p : vertices)</code> 確保每個白色頂點都會啟動一次 <code>dfsVisit</code>')
once('BFS：<code>queue.enqueue(neighbor)</code>：先把鄰居塞 queue，等以後處理。<br>',
     'BFS：<code>vertQueue.push(n.first)</code>：先把鄰居放進佇列，等以後處理。<br>')
once('DFS：<code>dfsVisit(neighbor)</code>：立刻遞迴下去處理鄰居。<br>',
     'DFS：<code>dfsVisit(n.first)</code>：立刻遞迴下去處理鄰居。<br>')
cut_in('dfs', '''<div class="deck-extra">
  <div class="dx-label">講義 08 · DFSGraph：discovery / closing time 全表</div>''', '''E→B 那條邊指向還是灰色的祖先，是一條 back edge：它宣告圖裡有循環。</p>
</div>
''', gen('graphs-dfs-trace') + '\n')


# ================================================================ quizzes with per-option feedback
def quiz_html(qid, label, question, options):
    opts = '\n'.join(
        f'      <div class="quiz-opt" data-correct="{"true" if ok else "false"}" data-fb="{escape(fb, quote=True)}" '
        f'onclick="quizCheck(\'{qid}\', this)"><span class="opt-letter">({chr(65 + k)})</span> {text}</div>'
        for k, (ok, text, fb) in enumerate(options))
    return (f'  <div class="quiz-box">\n    <div class="quiz-label">{label}</div>\n    <p>{question}</p>\n'
            f'    <div class="quiz-options" id="{qid}Options">\n{opts}\n    </div>\n'
            f'    <div class="quiz-feedback" id="{qid}Feedback"></div>\n  </div>\n')


# ================================================================ P06 topsort
once('① 對圖跑 <code>dfs(g)</code>，目的是替每個頂點算出', '① 對圖 g 呼叫 <code>g.dfs()</code>，目的是替每個頂點算出')
a, b = section_span('topsort')
i = s.index('  <div class="viz-layout">', a)
s = s[:i] + gen('graphs-topsort') + '\n' + s[i:]
cut_in('topsort', '  <div class="quiz-box">\n    <div class="quiz-label">QUIZ · 為什麼「closing time 遞減」就是答案？</div>',
       '<div class="quiz-feedback" id="ts1Feedback"></div>\n  </div>\n',
       quiz_html('ts1', 'QUIZ · 為什麼「closing time 遞減」就是答案？',
                 '對 DAG 跑完 DFS 後，依 closing time 遞減排序，為什麼保證每條邊 $(v,w)$ 的 $v$ 都排在 $w$ 前面？', [
                     (True, '因為 DAG 上有邊 $(v,w)$ 時，$v$ 的 closing time 一定比 $w$ 大',
                      '對 DAG 上任一條邊 (v, w)，DFS 只有兩種可能：w 在 v 的子樹裡，w 先關閉、v 後關閉；或者 w 早已在別的子樹或別棵樹完成，closing time 更小。'
                      '「w 是 v 的祖先」不可能發生，因為那需要一條 w 到 v 的路徑，再加上邊 v → w 就成了循環。所以依 closing time 遞減排序，v 一定排在 w 前面。'
                      '拓撲排序通常不唯一：起點與鄰居的順序不同，會得到不同但同樣合法的順序。'),
                     (False, '因為 closing time 大代表這個點的鄰居比較多',
                      'closing time 和鄰居數量沒有必然關係。關鍵是邊 (v, w) 在 DFS 中只有兩種結局：w 是 v 子樹的一員（先關閉），或 w 早已完成（更早關閉）。'),
                     (False, '因為 DFS 一定會先造訪 $v$ 再造訪 $w$',
                      '不一定：w 可能在另一棵 DFS 樹裡比 v 更早被造訪。即使如此，w 也比 v 早關閉，所以排序結果仍然正確。'),
                     (False, '因為 discovery time 遞增的順序也一樣正確，只是習慣用 closing time',
                      'discovery time 不行：DFS 可能先從 w 所在的樹開始，w 的 discovery time 就比 v 小，排序結果會把 w 放在 v 前面。'),
                 ]))

# ================================================================ P07 SCC
a, b = section_span('scc')
i = s.index('  <div class="viz-layout">', a)
s = s[:i] + gen('graphs-scc') + '\n' + s[i:]
cut_in('scc', '  <div class="quiz-box">\n    <div class="quiz-label">QUIZ · 第二次 DFS 的兩個講究</div>',
       '<div class="quiz-feedback" id="scc1Feedback"></div>\n  </div>\n',
       quiz_html('scc1', 'QUIZ · 第二次 DFS 的兩個講究',
                 'SCC 演算法的第二次 DFS 為什麼要（i）換到 $G^T$ 上跑、（ii）依 closing time 遞減挑起點？', [
                     (True, '兩個條件合起來，讓每棵 DFS 樹恰好「困」在一個 SCC 裡',
                      '第一次 DFS 中，位在上游的 SCC（能通往別的元件、別的元件回不來）一定含有最大的 closing time。'
                      '換到 G<sup>T</sup> 之後，跨元件的邊全部反向；從剩下 closing time 最大的頂點出發，DFS 只能在自己的元件裡走，進不了其他元件。'
                      '走完一棵樹就收掉一個 SCC，再從剩下 closing time 最大的頂點開新的樹。'),
                     (False, '$G^T$ 的邊比較少，跑起來比較快', '轉置只是把邊反向，邊數完全一樣。'),
                     (False, '只是慣例，從任何點開始、在原圖上跑也一樣對',
                      '在原圖 G 上從 A 跑 DFS，一棵樹就會走遍全部 8 個頂點（A 到得了每個點），三個 SCC 全混在一起。'),
                     (False, '為了讓第二次 DFS 的 closing time 和第一次相同',
                      '第二次 DFS 的時間本身不重要，重要的是它長出的每一棵樹；兩次的時間一般也不會相同。'),
                 ]))

# ================================================================ P08 Dijkstra
cut_in('dijkstra', '  <p><strong>Dijkstra 演算法</strong>解決<strong>單源最短路徑</strong>問題', '''對於有負邊但無負環的情況請改用 <strong>Bellman-Ford</strong>。
  </div>
''', gen('graphs-dij-intro') + '\n\n  <h3>互動：Dijkstra 的每一步</h3>\n')
once('第 9–13 行稱為<strong>邊鬆弛</strong>', '程式中計算 <code>newDistance</code> 並比較、更新的那一段稱為<strong>邊鬆弛</strong>')
once('這是 PDF 上的標準範例（雙向邊）', '這是講義的路由範例圖（雙向邊）')
cut_in('dijkstra', '''<div class="deck-extra">
  <div class="dx-label">講義 08 · dijkstra + findPath 的使用畫面</div>''', '''u 到 z 的最短路是 u x y z，總長 3。</p>
</div>
''', gen('graphs-dij-run') + '\n')

# ================================================================ P09 Prim
cut_in('prim', '  <p>想像線上遊戲要把同一筆訊息傳給所有玩家。', '''不會靜默回傳 forest。
  </div>
''', gen('graphs-prim-intro') + '\n')
cut_in('prim', '''<div class="deck-extra">
  <div class="dx-label">講義 08 · prim 的使用畫面：長出 MST</div>''', '''每次選的是跨越「目前樹／樹外頂點」之 cut 的最小權重 safe edge。</p>
</div>
''', gen('graphs-prim-run') + '\n')

# ================================================================ exercises (Ex1 is generated inside the Dijkstra section)
once('  <h2>動手驗證：兩個經典考點</h2>', '  <h2>練習：Prim 加入的最後一條邊</h2>')
cut_in('exercises', '  <div class="quiz-box">\n    <div class="quiz-label">EXERCISE 1 · Dijkstra 與負邊權</div>',
       '<div class="quiz-feedback" id="ex2Feedback"></div>\n  </div>\n', gen('graphs-exercises') + '\n')

# ================================================================ reference: comparison tables become （補充） folds
cut_in('reference', '  <h3>BFS vs DFS 行為對照</h3>', '''      <tr><td>有向／無向</td><td>有向／無向皆可</td><td>無向（有向需特殊處理）</td></tr>
    </tbody>
  </table></div>
''', '  <h3>兩組演算法的對照</h3>\n' + gen('graphs-ref-extra') + '\n')

# ================================================================ recap section + navigation
once('<section id="bankquiz">', '''<section id="recap">
  <div class="section-number">RECAP · 重點回顧</div>
  <h2>重點回顧 <span class="sec-badge">cppds §9 總結</span></h2>
''' + gen('graphs-recap') + '''
</section>

<section id="bankquiz">''')
once('''  <a href="#reference" data-target="reference"><span class="fn-num">REF</span><span class="fn-name">總覽比較</span></a>
''', '''  <a href="#reference" data-target="reference"><span class="fn-num">REF</span><span class="fn-name">總覽比較</span></a>
  <a href="#recap" data-target="recap"><span class="fn-num">SUM</span><span class="fn-name">重點回顧</span></a>
''')
once('''    <a href="#reference"><span class="toc-num">REF</span>總覽比較表</a>
''', '''    <a href="#reference"><span class="toc-num">REF</span>總覽比較表</a>
    <a href="#recap"><span class="toc-num">SUM</span>重點回顧</a>
''')
once('<span class="toc-num">EX</span>練習題</a>', '<span class="toc-num">EX</span>練習：Prim 的最後一條邊</a>')
once('<span class="fn-num">EX</span><span class="fn-name">練習題</span>', '<span class="fn-num">EX</span><span class="fn-name">練習 2</span>')
once('② <strong>對照講義</strong>：頁上 §徽章對應 cppds 章節；細節與完整程式請回講義 08 與 cppds 原文。',
     '② <strong>對照講義</strong>：頁上 §徽章對應 cppds 章節；講義的完整程式收在各節的收合區，預期輸出放在收合區外，可以先猜輸出再展開程式對照。')
once('並用 REF 總覽區當速查表。', '並用 REF 總覽區與<a href="#recap">重點回顧</a>當速查表。')

# ================================================================ animation code panels: lecture names
PANELS = {
    'bfsCode': '''#include "pythonds3/cppds/graph_algos.hpp"
void bfs(Graph& g, string startKey) {
    for (auto& p : g.vertices) {   // reset every vertex
        p.second.color = "white"; p.second.distance = INT_MAX; p.second.previous = "";
    }
    g.vertices[startKey].distance = 0;
    g.vertices[startKey].color = "gray";
    queue<string> vertQueue;
    vertQueue.push(startKey);@6
    while (!vertQueue.empty()) {
        string currentKey = vertQueue.front();@8
        vertQueue.pop();
        Vertex& current = g.vertices[currentKey];
        for (auto& n : current.neighbors) {
            Vertex& neighbor = g.vertices[n.first];
            if (neighbor.color == "white") {@10
                neighbor.color = "gray";@11
                neighbor.distance = current.distance + 1;
                neighbor.previous = currentKey;
                vertQueue.push(n.first);
            }
        }
        current.color = "black";@15
    }
}''',
    'dfsCode': '''// members of DFSGraph (graph_algos.hpp)
void dfs() {
    time = 0; discovery.clear(); closing.clear();
    for (auto& p : vertices) { p.second.color = "white"; p.second.previous = ""; }@2
    for (auto& p : vertices) {
        if (p.second.color == "white") dfsVisit(p.first);@6
    }
}
void dfsVisit(string startKey) {
    vertices[startKey].color = "gray";@9
    time = time + 1;
    discovery[startKey] = time;
    for (auto& n : vertices[startKey].neighbors) {
        if (vertices[n.first].color == "white") {@12
            vertices[n.first].previous = startKey;
            dfsVisit(n.first);@13
        }
    }
    vertices[startKey].color = "black";@16
    time = time + 1;
    closing[startKey] = time;
}''',
    'knightCode': '''#include "pythonds3/cppds/graph_algos.hpp"
bool knightTourWarnsdorff(int n, vector<string>& path, string uKey, int limit, Graph& g) {
    g.vertices[uKey].color = "gray";
    path.push_back(uKey);
    if (n < limit) {
        bool done = false;
        for (string nbKey : orderByAvail(g, uKey)) {   // Warnsdorff order
            if (done) break;
            if (g.vertices[nbKey].color == "white") {
                done = knightTourWarnsdorff(n + 1, path, nbKey, limit, g);
            }
        }
        if (!done) {   // backtrack
            path.pop_back();
            g.vertices[uKey].color = "white";
        }
        return done;
    }
    return true;
}''',
    'dijCode': '''#include "pythonds3/cppds/graph_algos.hpp"
void dijkstra(Graph& g, string startKey) {
    priority_queue<pair<int, string>, vector<pair<int, string>>,
                   greater<pair<int, string>>> pq;
    // the header also resets every distance to INT_MAX
    // and rejects negative weights here
    g.vertices[startKey].distance = 0;
    pq.push({0, startKey});@4
    while (!pq.empty()) {
        auto [distance, currentKey] = pq.top();@6
        pq.pop();
        if (distance > g.vertices[currentKey].distance) continue;@7
        for (auto& n : g.vertices[currentKey].neighbors) {
            int newDistance = g.vertices[currentKey].distance + n.second;@10
            if (newDistance < g.vertices[n.first].distance) {
                g.vertices[n.first].distance = newDistance;@11
                g.vertices[n.first].previous = currentKey;
                pq.push({newDistance, n.first});
            }
        }
    }
}''',
    'primCode': '''#include "pythonds3/cppds/graph_algos.hpp"
void prim(Graph& g, string startKey) {
    priority_queue<pair<int, string>, vector<pair<int, string>>,
                   greater<pair<int, string>>> pq;
    set<string> inTree;
    for (auto& p : g.vertices) { p.second.distance = INT_MAX; p.second.previous = ""; }
    g.vertices[startKey].distance = 0;
    pq.push({0, startKey});@5
    while (!pq.empty()) {
        auto [distance, currentKey] = pq.top(); pq.pop();@8
        if (inTree.count(currentKey)) continue;   // stale entry
        inTree.insert(currentKey);
        for (auto& n : g.vertices[currentKey].neighbors) {
            int newDistance = n.second;   // edge weight only@10
            if (!inTree.count(n.first) && newDistance < g.vertices[n.first].distance) {@11
                g.vertices[n.first].distance = newDistance;@13
                g.vertices[n.first].previous = currentKey;
                pq.push({newDistance, n.first});
            }
        }
    }
    if (inTree.size() != g.vertices.size())
        throw invalid_argument("Prim requires a connected graph");
}''',
}


def panel_html(code):
    marks, plain = {}, []
    for k, line in enumerate(code.split('\n'), 1):
        m = re.search(r'@(\d+)$', line)
        if m:
            marks[k] = m.group(1)
            line = line[:m.start()]
        plain.append(line)
    out = hl('\n'.join(plain))

    def relabel(m):
        k = int(m.group(1))
        return f'<span class="line" data-l="{marks[k]}">' if k in marks else '<span class="line">'
    return re.sub(r'<span class="line" data-l="(\d+)">', relabel, out)


for pid, code in PANELS.items():
    m = re.search(rf'<div class="pseudo-code" id="{pid}">.*?</div>', s, re.S)
    assert m and s.count(f'id="{pid}"') == 1, pid
    s = s[:m.start()] + f'<div class="pseudo-code" id="{pid}">' + panel_html(code) + '</div>' + s[m.end():]

# ================================================================ JS: drop the redrawn exercise graphs, generic quiz feedback
cut('''/* =============================================================
   EXERCISES：練習題的圖（與 PDF 原圖完全一致）''', '''const ex2R = new GraphRenderer('canvas-ex2', ex2Config, {
  directed: false, showWeights: true, width: 600, height: 400,
});
''', '')
a = s.index('function quizCheck(quizId, optEl) {')
b = s.index('\n}\n', a) + 3
s = s[:a] + '''function quizCheck(quizId, optEl) {
  const isCorrect = optEl.dataset.correct === 'true';
  optEl.parentElement.querySelectorAll('.quiz-opt').forEach(o => o.classList.remove('correct', 'wrong'));
  optEl.classList.add(isCorrect ? 'correct' : 'wrong');
  const fb = document.getElementById(`${quizId}Feedback`);
  fb.classList.remove('correct', 'wrong');
  fb.classList.add('show', isCorrect ? 'correct' : 'wrong');
  fb.innerHTML = (isCorrect ? '<strong>正確 ✓</strong> ' : '<strong>不對 ✗</strong> ') + (optEl.dataset.fb || '');
}
''' + s[b:]

P.write_text(s)
print('markers placed:', len(re.findall(r'<!-- gen:graphs-', s)))
