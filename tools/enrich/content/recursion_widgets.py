"""Interactive widgets of recursion.html (player-v2 animations and canvases).

The JS that drives them lives in the page's main <script>; the call-stack player for
toStr(10, 2) lives in EXTRA_JS, which enrich_recursion.py keeps in <script id="recursion-extra-js">.
Code panels use the lecture's names; their data-l line numbers are the ones the JS highlights.
"""
from enrich_lib import hl


def _speed(p, lo=120, hi=1200, val=650):
    return (f'<span class="mono" style="font-size:.8rem;color:var(--muted);">速度 <input id="{p}Speed" type="range" '
            f'min="{lo}" max="{hi}" value="{val}" style="vertical-align:middle;" aria-label="每一步的間隔"></span>')


def _buttons(p, start, label='▶ 開始'):
    return (f'<button class="btn" onclick="{start}()">{label}</button>\n'
            f'          <button class="btn" onclick="{p}Player &amp;&amp; {p}Player.step()">→ 單步</button>\n'
            f'          <button class="btn" onclick="{p}Player &amp;&amp; {p}Player.toggle(this)">⏸ 暫停</button>')


def _code_card(title, code, cid=None, size=None):
    ident = f' id="{cid}"' if cid else ''
    style = f' style="font-size:{size};"' if size else ''
    return (f'<div class="info-card"><div class="ic-title">{title} <span class="ic-badge">CODE</span></div>'
            f'<div class="pseudo-code"{ident}{style} data-cpp="fragment">\n{hl(code)}</div></div>')


def _layout(panel, side):
    return f'''<div class="viz-layout">
    <div>
      <div class="viz-panel">
        {panel}
      </div>
    </div>
    <div class="side-panel">
      {side}
    </div>
  </div>'''


LIST_SUM_FROM = '''int listSumFrom(const vector<int>& numList, size_t index) {
    if (index == numList.size()) {
        return 0;                              // empty remaining range
    }
    return numList[index] + listSumFrom(numList, index + 1);
}

int listSum(const vector<int>& numList) {
    return listSumFrom(numList, 0);
}'''

TO_STR = '''string toStr(int n, int base) {
    string convertString = "0123456789ABCDEF";
    if (n < base) {
        return string(1, convertString[n]);
    } else {
        return toStr(n / base, base) + convertString[n % base];
    }
}'''

FACT = '''int fact(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * fact(n - 1);
}'''

SPIRAL = '''void spiral(ct::Turtle& turtle, int length) {
    if (length > 0) {
        turtle.forward(length);
        turtle.right(90);
        spiral(turtle, length - 5);
    }
}'''

TREE = '''void tree(int branchLen, ct::Turtle& turtle) {
    if (branchLen > 5) {
        turtle.forward(branchLen);
        turtle.right(20);
        tree(branchLen - 15, turtle);
        turtle.left(40);
        tree(branchLen - 15, turtle);
        turtle.right(20);
        turtle.backward(branchLen);
    }
}'''

SIERPINSKI = '''void sierpinski(ct::Point a, ct::Point b, ct::Point c,
                int degree, ct::Turtle& turtle) {
    const string colors[] = {
        "blue", "red", "green", "white", "yellow", "violet", "orange"
    };
    drawTriangle(a, b, c, {colors[degree]}, turtle);
    if (degree > 0) {
        sierpinski(a, ct::middle(a, b), ct::middle(a, c), degree - 1, turtle);
        sierpinski(b, ct::middle(a, b), ct::middle(b, c), degree - 1, turtle);
        sierpinski(c, ct::middle(c, b), ct::middle(a, c), degree - 1, turtle);
    }
}'''

MOVE_TOWER = '''void moveTower(int height, string fromPole, string toPole, string withPole) {
    if (height >= 1) {
        moveTower(height - 1, fromPole, withPole, toPole);
        moveDisk(fromPole, toPole);
        moveTower(height - 1, withPole, toPole, fromPole);
    }
}'''

# Same statements as searchFrom in pythonds3/cppds/maze.hpp.
SEARCH_FROM = '''bool searchFrom(Maze& maze, int row, int column) {
    if (maze.get(row, column) == OBSTACLE) return false;
    if (maze.get(row, column) == TRIED || maze.get(row, column) == DEAD_END) return false;
    if (maze.isExit(row, column)) {
        maze.updatePosition(row, column, PART_OF_PATH);
        return true;
    }
    maze.updatePosition(row, column, TRIED);
    bool found = searchFrom(maze, row - 1, column)
              || searchFrom(maze, row + 1, column)
              || searchFrom(maze, row, column - 1)
              || searchFrom(maze, row, column + 1);
    if (found) maze.updatePosition(row, column, PART_OF_PATH);
    else maze.updatePosition(row, column, DEAD_END);
    return found;
}'''

MAKE_CHANGE3 = '''int makeChange3(vector<int>& coinValueList, int change, vector<int>& minCoins) {
    for (int cents = 0; cents <= change; cents++) {
        int coinCount = cents;
        for (int j : coinValueList) {
            if (j <= cents && minCoins[cents - j] + 1 < coinCount) {
                coinCount = minCoins[cents - j] + 1;
            }
        }
        minCoins[cents] = coinCount;
    }
    return minCoins[change];
}'''

PRINT_COINS = '''void printCoins(vector<int>& coinsUsed, int change) {
    int coin = change;
    while (coin > 0) {
        int thisCoin = coinsUsed[coin];
        cout << thisCoin << " ";
        coin = coin - thisCoin;
    }
    cout << endl;
}'''


def w_sum():
    panel = f'''<div class="mono" id="sumTrace" style="font-size:.95rem;line-height:2.2;min-height:150px;overflow-x:auto;"></div>
        <div class="status-banner" id="sumStatus"><span class="status-icon">›</span><span class="status-text">按「開始」看 listSum({{1, 3, 5, 7, 9}}) 怎麼展開再收合。</span></div>
        <div class="controls-bar">
          {_buttons('sum', 'sumStart')}
          {_speed('sum')}
        </div>'''
    side = _code_card('listSumFrom', LIST_SUM_FROM, 'sumCode') + '''
      <p style="font-size:.88rem;"><code>const vector&lt;int&gt;&amp; numList</code> 以唯讀參考傳入，每次呼叫都不複製容器；<code>size_t index</code> 是無號索引，從 0 開始，等於 <code>numList.size()</code> 時先回傳 0，不會越界。詳見 <a href="p3_functions.html#constref">P3 傳參方式</a>。</p>'''
    return _layout(panel, side)


def w_tostr():
    panel = '''<div class="mono" id="tostrTrace" style="font-size:.92rem;line-height:2.1;min-height:160px;overflow-x:auto;"></div>
        <div class="status-banner" id="tostrStatus"><span class="status-icon">›</span><span class="status-text">toStr(769, 10) 的展開與回傳。也可以換成自己的數字與進位。</span></div>
        <div class="controls-bar">
          <input id="tostrN" type="number" class="mono" aria-label="要轉換的整數" style="width:90px;padding:.35rem .5rem;border:1px solid var(--card-border);border-radius:6px;" value="769">
          <select id="tostrB" class="mono" aria-label="進位" style="padding:.35rem;border-radius:6px;border:1px solid var(--card-border);">
            <option value="10" selected>base 10</option><option value="2">base 2</option><option value="16">base 16</option>
          </select>
          ''' + _buttons('tostr', 'tostrStart') + '''
          ''' + _speed('tostr') + '''
        </div>'''
    side = _code_card('toStr', TO_STR, 'tostrCode') + '''
      <div class="info-card">
        <div class="ic-title">跟上一章的 stack 版比一比</div>
        <div style="font-size:.86rem;line-height:1.9;">
        stack 版：自己 push 餘數，最後再 pop 出來。<br>
        遞迴版：把餘數留到遞迴呼叫<strong>回來之後</strong>才接上，由呼叫堆疊記住順序。</div>
      </div>'''
    return _layout(panel, side)


def w_frames_tostr():
    panel = '''<div class="bs-stack" id="tsfVis" style="min-height:260px;"></div>
        <div class="status-banner" id="tsfStatus"><span class="status-icon">›</span><span class="status-text">按「開始」，看 toStr(10, 2) 的 stack frame 怎麼推入與彈出。</span></div>
        <div class="controls-bar">
          ''' + _buttons('tsf', 'tsfStart', '▶ toStr(10, 2)') + '''
          ''' + _speed('tsf') + '''
        </div>'''
    side = _code_card('toStr', TO_STR, 'tsfCode') + '''
      <div class="info-card">
        <div class="ic-title">怎麼看這個動畫</div>
        <div style="font-size:.86rem;line-height:1.9;">最上面一格是正在執行的呼叫，下面的格子都停在第 6 行，等上一層的結果。每一格各有自己的 <code>n</code> 與 <code>base</code>。</div>
      </div>'''
    return _layout(panel, side)


def w_fact():
    panel = '''<div class="bs-stack" id="frameVis" style="min-height:230px;"></div>
        <div class="status-banner" id="frameStatus"><span class="status-icon">›</span><span class="status-text">觀察 fact(4) 的 frame 推入與彈出。</span></div>
        <div class="controls-bar">
          ''' + _buttons('frame', 'frameStart', '▶ fact(4)') + '''
          ''' + _speed('frame') + '''
        </div>'''
    side = _code_card('fact', FACT) + '''
      <div class="info-card">
        <div class="ic-title">為什麼會 stack overflow？</div>
        <div style="font-size:.86rem;line-height:1.9;">call stack 容量有限，上限取決於作業系統、執行環境與設定。
        base case 寫錯時 frame 會持續堆積，最後程式出錯。深度可能很大的線性遞迴，通常應改寫成迴圈。</div>
      </div>
      <div class="info-card">
        <div class="ic-title">尾遞迴</div>
        <div style="font-size:.86rem;line-height:1.9;">若遞迴呼叫是函式的<strong>最後一步</strong>，
        編譯器<strong>可能</strong>做尾呼叫最佳化並重用 frame；C++ 標準不保證一定會做，因此程式正確性不能依賴它。</div>
      </div>'''
    return _layout(panel, side)


def w_viz():
    panel = '''<div style="display:flex;gap:1rem;flex-wrap:wrap;justify-content:center;">
          <canvas id="spiralCv" width="300" height="300" style="background:#fff;border-radius:8px;max-width:100%;" aria-label="螺旋"></canvas>
          <canvas id="treeCv" width="330" height="300" style="background:#fff;border-radius:8px;max-width:100%;" aria-label="碎形樹"></canvas>
        </div>
        <div class="status-banner" id="vizStatus"><span class="status-icon">›</span><span class="status-text">左邊是螺旋（spiral），右邊是碎形樹（tree）。拉動層數滑桿，觀察「樹 = 樹幹 + 兩棵小樹」。</span></div>
        <div class="controls-bar">
          <button class="btn" onclick="spiralStart()">▶ 畫螺旋</button>
          <label class="mono" style="font-size:.8rem;">樹畫到第幾層 <input id="treeDepth" type="range" min="1" max="5" value="5" style="vertical-align:middle;"></label>
          <button class="btn" onclick="treeDraw()">▶ 畫樹</button>
        </div>'''
    side = (_code_card('spiral', SPIRAL, size='.76rem') + '\n      ' + _code_card('tree', TREE, size='.76rem'))
    return _layout(panel, side)


def w_sierpinski():
    panel = '''<canvas id="sierCv" width="560" height="360" style="background:#fff;border-radius:8px;max-width:100%;" aria-label="Sierpinski 三角形"></canvas>
        <div class="status-banner" id="sierStatus"><span class="status-icon">›</span><span class="status-text">拉 degree 滑桿。最小的三角形有 3^degree 個，總共畫 3⁰+…+3^degree 個。</span></div>
        <div class="controls-bar">
          <label class="mono" style="font-size:.8rem;">degree <input id="sierDeg" type="range" min="0" max="6" value="3" style="vertical-align:middle;"> <span id="sierDegLbl">3</span></label>
        </div>'''
    side = _code_card('sierpinski', SIERPINSKI, size='.72rem')
    return _layout(panel, side)


def w_hanoi():
    panel = '''<div style="display:flex;justify-content:space-around;align-items:flex-end;min-height:170px;overflow-x:auto;" id="hanoiVis"></div>
        <div class="status-banner" id="hanoiStatus"><span class="status-icon">›</span><span class="status-text">選盤數後開始。和講義的 <code>moveTower(n, "A", "B", "C")</code> 一樣：A 是 fromPole、B 是 toPole、C 是 withPole。</span></div>
        <div class="controls-bar">
          <select id="hanoiN" class="mono" aria-label="盤數" style="padding:.35rem;border-radius:6px;border:1px solid var(--card-border);">
            <option value="3" selected>3 盤</option><option value="4">4 盤</option><option value="5">5 盤</option>
          </select>
          ''' + _buttons('hanoi', 'hanoiStart') + '''
          ''' + _speed('hanoi', 120, 1000, 420) + '''
        </div>'''
    side = _code_card('moveTower', MOVE_TOWER, 'hanoiCode') + '''
      <div class="info-card">
        <div class="ic-title">移動次數</div>
        <div class="ic-row"><span class="ic-label">3 盤</span><span class="ic-value">7</span></div>
        <div class="ic-row"><span class="ic-label">5 盤</span><span class="ic-value">31</span></div>
        <div class="ic-row"><span class="ic-label">n 盤</span><span class="ic-value">2ⁿ − 1</span></div>
      </div>'''
    return _layout(panel, side)


def w_maze():
    panel = '''<div id="mazeVis" class="mono" style="line-height:1.15;font-size:1.05rem;letter-spacing:.1em;padding:.5rem;overflow-x:auto;"></div>
        <div class="status-banner" id="mazeStatus"><span class="status-icon">›</span><span class="status-text">S 是起點；按「開始」看探索與回溯。</span></div>
        <div class="controls-bar">
          ''' + _buttons('maze', 'mazeStart') + '''
          ''' + _speed('maze', 60, 600, 300) + '''
        </div>
        <div class="mono" style="font-size:.78rem;color:var(--muted);">圖例：<span style="color:#f39c12;">●</span> 目前｜<span style="color:#1a6b4a;">＋</span> 路徑（O）｜<span style="color:#c0392b;">−</span> 死路</div>'''
    side = _code_card('searchFrom', SEARCH_FROM, 'mazeCode', size='.72rem')
    return _layout(panel, side)


def w_dp():
    panel = '''<div class="char-strip" id="dpStrip" style="max-width:100%;overflow-x:auto;flex-wrap:nowrap;"></div>
        <div class="status-banner" id="dpStatus"><span class="status-icon">›</span><span class="status-text">按「填表」填 0～23 分的最少硬幣表。</span></div>
        <div class="controls-bar">
          ''' + _buttons('dp', 'dpStart', '▶ 填表（coins = 1, 5, 10, 21, 25；23 分）') + '''
          ''' + _speed('dp') + '''
        </div>'''
    side = _code_card('makeChange3', MAKE_CHANGE3, 'dpCode', size='.74rem') + '''
      ''' + _code_card('printCoins', PRINT_COINS, size='.74rem')
    return _layout(panel, side)


# ---------------------------------------------------------------- extra JS (toStr(10, 2) call stack)
EXTRA_JS = r'''/* recursion-extra: toStr(10, 2) call stack (player-v2) */
let tsfPlayer = null;
function tsfFrames() {
  const conv = '0123456789ABCDEF', base = 2, frames = [];
  const chain = [10, 5, 2, 1];
  const st = [];
  chain.forEach((n, k) => {
    st.forEach((_, j) => { st[j] = st[j].replace('（執行中）', '（等待中）'); });
    st.push(`toStr(${n}, ${base})　n=${n}（執行中）`);
    frames.push({stack: [...st], line: k === 0 ? 1 : 6,
      msg: k === 0 ? 'main 呼叫 toStr(10, 2)：推入第一個 frame。'
                   : `${chain[k-1]} ≥ 2：先呼叫 toStr(${n}, 2)，餘數 '${conv[chain[k-1] % base]}' 等它回來再接。`});
  });
  st[st.length - 1] = 'toStr(1, 2)　n=1 → 回傳 "1"';
  frames.push({stack: [...st], line: 4, msg: '1 < 2：base case，直接查表回傳 "1"。'});
  let s = '1';
  for (let k = chain.length - 2; k >= 0; k--) {
    st.pop();
    const n = chain[k];
    s = s + conv[n % base];
    st[st.length - 1] = `toStr(${n}, 2)　n=${n} → "${s}"`;
    frames.push({stack: [...st], line: 6,
      msg: `彈出上一層；toStr(${n}, 2) 接上 convertString[${n} % 2] = '${conv[n % base]}'，得到 "${s}"。`});
  }
  st.pop();
  frames.push({stack: [], line: 8, msg: '<strong>所有 frame 都已彈出，main 拿到 "1010"。</strong>'});
  return frames;
}
function tsfStart() {
  tsfPlayer = new Player({frames: tsfFrames(), apply: f => {
    renderBoxStack('tsfVis', f.stack, {highlight: 0}); setStatus('tsfStatus', f.msg); hlLine('tsfCode', f.line);
  }, delayInput: $('tsfSpeed')});
  tsfPlayer.reset(); tsfPlayer.play();
}
renderBoxStack('tsfVis', []);
/* /recursion-extra */'''
