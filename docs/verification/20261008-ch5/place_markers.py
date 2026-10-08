"""One-time hand edits on linear_structures.html: place gen markers, drop old injected blocks,
align ADT tables with the lecture, rename animation-panel identifiers, add 4th quiz options,
add the recap section and its navigation entries."""
import re, sys
from pathlib import Path
P = Path('/home/phonchi/ds-cpp-selfstudy/linear_structures.html')
s = P.read_text()
if '<!-- gen:linear-prologue -->' in s:
    sys.exit('gen markers already placed; this one-time script must not run again')

def gen(name):
    return f'<!-- gen:{name} -->\n<!-- /gen:{name} -->'

def once(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f'expected {count} match(es), got {n}: {old[:80]!r}')
    s = s.replace(old, new)

def cut(start, end, new):
    """Replace from the unique start marker through the unique end marker (inclusive)."""
    global s
    i = s.index(start); assert s.count(start) == 1, start
    j = s.index(end, i) + len(end)
    s = s[:i] + new + s[j:]

# ---- P00 prologue
once('''        之間只有「前後」關係，'''.strip() if False else '''操作只在<strong>端點</strong>發生。不同結構 = 不同的「進出端」組合。</div>
      </div>
    </div>
  </div>
</section>''', '''操作只在<strong>端點</strong>發生。不同結構 = 不同的「進出端」組合。</div>
      </div>
    </div>
  </div>
''' + gen('linear-prologue') + '''
</section>''')

# ---- P01 stack
once('''底部與中間的元素完全動不了。</div>
  </div>
''', '''底部與中間的元素完全動不了。</div>
  </div>
''' + gen('linear-stack-intro') + '\n')
once('''      <tr><td class="mono">s.empty()</td><td class="mono">[]</td><td class="mono">true</td></tr>
      <tr><td class="mono">s.push(4)</td><td class="mono">[4]</td><td></td></tr>
      <tr><td class="mono">s.push(7)</td><td class="mono">[4, 7]</td><td>void</td></tr>
      <tr><td class="mono">s.top()</td><td class="mono">[4, 7]</td><td class="mono">7</td></tr>
      <tr><td class="mono">s.push(2)</td><td class="mono">[4, 7, 2]</td><td>void</td></tr>
      <tr><td class="mono">s.size()</td><td class="mono">[4, 7, 2]</td><td class="mono">3</td></tr>
      <tr><td class="mono">s.pop()</td><td class="mono">[4, 7]</td><td>void</td></tr>''',
'''      <tr><td class="mono">s.empty()</td><td class="mono">[]</td><td class="mono">true</td></tr>
      <tr><td class="mono">s.push(4)</td><td class="mono">[4]</td><td>void</td></tr>
      <tr><td class="mono">s.push(7)</td><td class="mono">[4, 7]</td><td>void</td></tr>
      <tr><td class="mono">s.top()</td><td class="mono">[4, 7]</td><td class="mono">7</td></tr>
      <tr><td class="mono">s.pop()</td><td class="mono">[4]</td><td>void</td></tr>
      <tr><td class="mono">s.size()</td><td class="mono">[4]</td><td class="mono">1</td></tr>''')
cut('<h3 style="margin-top:1.6rem;">課程實作補充：Stack2 的代價</h3>',
    '''這個例子會在第 2 章（演算法分析）被正式量化。</div>
      </div>
    </div>
  </div>''', gen('linear-stack-stl'))
cut('<h3 style="margin-top:1.5rem;">講義練習：用 stack 反轉字串</h3>',
    '''<span class="line">    <span class="kw">return</span> rStr;</span>
<span class="line">}</span></div></div>''', gen('linear-stack-ex'))
cut('''<div class="deck-extra">
  <div class="dx-label">cppds 正文 · STL 與課程 API 對照</div>''', '''三套 API 不可混用。</p>
</div>''', '')

# ---- P02 parens
once('''課堂投影片跳過這兩節（RISE skip）：屬自學補充，''', '''課堂上略過這兩節，屬於自學內容，''')
once('''每個右括號要配的是「<strong>最近一個還沒配對的左括號</strong>」：這就是 stack 的 top。</p>
''', '''每個右括號要配的是「<strong>最近一個還沒配對的左括號</strong>」：這就是 stack 的 top。</p>
''' + gen('linear-parens') + '\n')
cut('<h3 style="margin-top:1.4rem;">一般化：三種括號混用</h3>', '''拿 <code>[{()]</code> 餵餵看。</p>''', gen('linear-parens-general'))

# ---- P03 base
once('''又是一個「<strong>產生順序與使用順序相反</strong>」的問題，stack 出場。</p>
''', '''又是一個「<strong>產生順序與使用順序相反</strong>」的問題，stack 出場。</p>
''' + gen('linear-base-intro') + '\n')
cut('<h3 id="dx-base">講義完整實作：從虛擬碼到 C++</h3>', '''base 16 的餘數 10~15 才印得出 A~F。</p>
</div>''', gen('linear-base-general'))

# ---- P04 infix
once('''      <tr><td class="mono">(A + B) * (C + D)</td><td class="mono">* + A B + C D</td><td class="mono">A B + C D + *</td></tr>
''', '''      <tr><td class="mono">(A + B) * (C + D)</td><td class="mono">* + A B + C D</td><td class="mono">A B + C D + *</td></tr>
      <tr><td class="mono">A * B + C * D</td><td class="mono">+ * A B * C D</td><td class="mono">A B * C D * +</td></tr>
''')
once('''考試手算用這招又快又不會錯。
  </div>
''', '''考試手算用這招又快又不會錯。
  </div>
''' + gen('linear-infix-paren') + '\n')
once('''    <li>掃完把 stack 剩下的全部 pop 輸出。</li>
  </ol>
''', '''    <li>掃完把 stack 剩下的全部 pop 輸出。</li>
  </ol>
''' + gen('linear-infix-convert') + '\n')
cut('<h3 id="dx-infix">講義完整實作：轉換器與求值器的 C++ 全文</h3>', '''還得改「同級要不要彈」的判斷。</p>
</div>''', gen('linear-infix-code'))
once('''<div class="ic-title">postfix 求值 <span class="ic-badge">CODE</span></div>''', '''<div class="ic-title">postfix 求值（簡化） <span class="ic-badge">CODE</span></div>''')
once('''<span class="kw">int</span> <span class="fn">postfixEval</span>(<span class="kw">const</span> vector&lt;string&gt;&amp; tokens) {''',
     '''<span class="kw">double</span> <span class="fn">postfixEval</span>(<span class="kw">const</span> vector&lt;string&gt;&amp; tokens) {''')
once('''    stack&lt;<span class="kw">int</span>&gt; operands;''', '''    stack&lt;<span class="kw">double</span>&gt; operandStack;''')
once('''operands.<span class="fn">push</span>(<span class="fn">stoi</span>(token));''', '''operandStack.<span class="fn">push</span>(<span class="fn">stod</span>(token));''')
once('''<span class="kw">int</span> right = operands.<span class="fn">top</span>(); operands.<span class="fn">pop</span>();''',
     '''<span class="kw">double</span> operand2 = operandStack.<span class="fn">top</span>(); operandStack.<span class="fn">pop</span>();''')
once('''<span class="kw">int</span> left = operands.<span class="fn">top</span>(); operands.<span class="fn">pop</span>();''',
     '''<span class="kw">double</span> operand1 = operandStack.<span class="fn">top</span>(); operandStack.<span class="fn">pop</span>();''')
once('''operands.<span class="fn">push</span>(<span class="fn">doMath</span>(token, left, right)); }''',
     '''operandStack.<span class="fn">push</span>(<span class="fn">doMath</span>(token, operand1, operand2)); }''')
once('''    } <span class="kw">return</span> operands.<span class="fn">top</span>(); }''', '''    } <span class="kw">return</span> operandStack.<span class="fn">top</span>(); }''')

# ---- P05 queue
once('''作業的 <code>enqueue/dequeue/isEmpty</code> 是課程實作補充。</p>
''', '''作業的 <code>enqueue/dequeue/isEmpty</code> 是課程實作補充。</p>
''' + gen('linear-queue-intro') + '\n')
once('''      <tr><td class="mono">q.push(4)</td><td class="mono">[4]</td><td>void</td></tr>
      <tr><td class="mono">q.push(7)</td><td class="mono">[4, 7]</td><td>void</td></tr>
      <tr><td class="mono">q.push(2)</td><td class="mono">[4, 7, 2]</td><td>void</td></tr>
      <tr><td class="mono">q.front()</td><td class="mono">[4, 7, 2]</td><td class="mono">4</td></tr>
      <tr><td class="mono">q.back()</td><td class="mono">[4, 7, 2]</td><td class="mono">2</td></tr>
      <tr><td class="mono">q.pop()</td><td class="mono">[7, 2]</td><td>void</td></tr>''',
'''      <tr><td class="mono">q.empty()</td><td class="mono">[]</td><td class="mono">true</td></tr>
      <tr><td class="mono">q.push(4)</td><td class="mono">[4]</td><td>void</td></tr>
      <tr><td class="mono">q.push(7)</td><td class="mono">[4, 7]</td><td>void</td></tr>
      <tr><td class="mono">q.front()</td><td class="mono">[4, 7]</td><td class="mono">4</td></tr>
      <tr><td class="mono">q.back()</td><td class="mono">[4, 7]</td><td class="mono">7</td></tr>
      <tr><td class="mono">q.pop()</td><td class="mono">[7]</td><td>void</td></tr>''')
once('''只用來研究表示法；一般 C++ 程式優先用 STL。</div>
      </div>
    </div>
  </div>
''', '''只用來研究表示法；一般 C++ 程式優先用 STL。</div>
      </div>
    </div>
  </div>
''' + gen('linear-queue-stl') + '\n')

# ---- P06 hot potato
once('''<strong>把手上的東西傳給下一個人</strong>：front 的人傳完就排到隊伍最尾。</p>
''', '''<strong>把手上的東西傳給下一個人</strong>：front 的人傳完就排到隊伍最尾。</p>
''' + gen('linear-hp-intro') + '\n')
once('''string <span class="fn">hotPotato</span>(vector&lt;string&gt; names, <span class="kw">int</span> num) {''',
     '''string <span class="fn">hotPotato</span>(vector&lt;string&gt; nameList, <span class="kw">int</span> num) {''')
once('''    queue&lt;string&gt; q;</span>
<span class="line" data-l="3">    <span class="kw">for</span> (string name : names) q.<span class="fn">push</span>(name);</span>
<span class="line" data-l="4">    <span class="kw">while</span> (q.<span class="fn">size</span>() &gt; <span class="num">1</span>) {</span>''',
'''    queue&lt;string&gt; simQueue;</span>
<span class="line" data-l="3">    <span class="kw">for</span> (string name : nameList) simQueue.<span class="fn">push</span>(name);</span>
<span class="line" data-l="4">    <span class="kw">while</span> (simQueue.<span class="fn">size</span>() &gt; <span class="num">1</span>) {</span>''')
once('''            q.<span class="fn">push</span>(q.<span class="fn">front</span>()); q.<span class="fn">pop</span>(); <span class="com">// 傳一次</span></span>
<span class="line" data-l="7">        } q.<span class="fn">pop</span>(); <span class="com">// 淘汰 front</span></span>
<span class="line" data-l="8">    } <span class="kw">return</span> q.<span class="fn">front</span>();</span>''',
'''            simQueue.<span class="fn">push</span>(simQueue.<span class="fn">front</span>()); simQueue.<span class="fn">pop</span>(); <span class="com">// 傳一次</span></span>
<span class="line" data-l="7">        } simQueue.<span class="fn">pop</span>(); <span class="com">// 淘汰 front</span></span>
<span class="line" data-l="8">    } <span class="kw">return</span> simQueue.<span class="fn">front</span>();</span>''')
once('''  <div class="quiz-feedback" id="qHpFeedback"></div>
</div>
''', '''  <div class="quiz-feedback" id="qHpFeedback"></div>
</div>
''' + gen('linear-hp-code') + '\n')

# ---- P07 printer
once('''課堂投影片跳過本節（RISE skip）：屬自學補充。''', '''課堂上略過本節，屬於自學內容。''')
once('''講義的做法：<strong>寫一個模擬</strong>，讓隨機事件跑一小時，統計平均等待時間。</p>
''', '''講義的做法：<strong>寫一個模擬</strong>，讓隨機事件跑一小時，統計平均等待時間。</p>
''' + gen('linear-printer-intro') + '\n')
cut('<h3>三個類別、一個主迴圈</h3>', '''模擬的價值就在這裡：改參數比改現實便宜太多，但模擬的可信度永遠不會超過它的假設。
  </div>''', gen('linear-printer'))

# ---- P08 deque
once('''課程的 <code>addFront/removeFront</code> API 是作業用補充。</p>
''', '''課程的 <code>addFront/removeFront</code> API 是作業用補充。</p>
''' + gen('linear-deque-intro') + '\n')
once('''      <tr><td class="mono">d.push_back(4)</td><td class="mono">[4]</td><td>void</td></tr>
      <tr><td class="mono">d.push_back(7)</td><td class="mono">[4, 7]</td><td>void</td></tr>
      <tr><td class="mono">d.push_front(2)</td><td class="mono">[2, 4, 7]</td><td>void</td></tr>
      <tr><td class="mono">d.front()</td><td class="mono">[2, 4, 7]</td><td>2</td></tr>
      <tr><td class="mono">d.back()</td><td class="mono">[2, 4, 7]</td><td>7</td></tr>
      <tr><td class="mono">d.pop_front()</td><td class="mono">[4, 7]</td><td>void</td></tr>''',
'''      <tr><td class="mono">d.empty()</td><td class="mono">[]</td><td class="mono">true</td></tr>
      <tr><td class="mono">d.push_back(4)</td><td class="mono">[4]</td><td>void</td></tr>
      <tr><td class="mono">d.push_front(7)</td><td class="mono">[7, 4]</td><td>void</td></tr>
      <tr><td class="mono">d.front()</td><td class="mono">[7, 4]</td><td class="mono">7</td></tr>
      <tr><td class="mono">d.back()</td><td class="mono">[7, 4]</td><td class="mono">4</td></tr>
      <tr><td class="mono">d.pop_front()</td><td class="mono">[4]</td><td>void</td></tr>''')
once('''<span class="kw">bool</span> <span class="fn">palChecker</span>(<span class="kw">const</span> string&amp; text) {</span>
<span class="line" data-l="2">    deque&lt;<span class="kw">char</span>&gt; chars(text.<span class="fn">begin</span>(), text.<span class="fn">end</span>());</span>
<span class="line" data-l="3">    <span class="kw">while</span> (chars.<span class="fn">size</span>() &gt; <span class="num">1</span>) {</span>
<span class="line" data-l="4">        <span class="kw">char</span> first = chars.<span class="fn">front</span>(); chars.<span class="fn">pop_front</span>();</span>
<span class="line" data-l="5">        <span class="kw">char</span> last = chars.<span class="fn">back</span>(); chars.<span class="fn">pop_back</span>();</span>''',
'''<span class="kw">bool</span> <span class="fn">palChecker</span>(string aString) {</span>
<span class="line" data-l="2">    deque&lt;<span class="kw">char</span>&gt; charDeque(aString.<span class="fn">begin</span>(), aString.<span class="fn">end</span>());</span>
<span class="line" data-l="3">    <span class="kw">while</span> (charDeque.<span class="fn">size</span>() &gt; <span class="num">1</span>) {</span>
<span class="line" data-l="4">        <span class="kw">char</span> first = charDeque.<span class="fn">front</span>(); charDeque.<span class="fn">pop_front</span>();</span>
<span class="line" data-l="5">        <span class="kw">char</span> last = charDeque.<span class="fn">back</span>(); charDeque.<span class="fn">pop_back</span>();</span>''')
cut('''<div class="deck-extra">
  <div class="dx-label">講義 05 · palChecker 的 C++ 全文</div>''', '''deque 兩端 O(1) 的能力在這裡剛好用滿。</p>
</div>''', gen('linear-deque-pal'))

# ---- EX
once('''  <div class="quiz-feedback" id="ex3Feedback"></div>
</div>
</section>''', '''  <div class="quiz-feedback" id="ex3Feedback"></div>
</div>
''' + gen('linear-exercises') + '''
</section>''')

# ---- REF: comparison tables move into the generator (folded); new recap section
cut('''  <h2>三種線性 ADT 一次比較 <span class="sec-badge">cppds §3 總覽</span></h2>''', '''    ③ ADT 與實作分離：介面不變，底層可以換 vector、linked list 或環形緩衝。
  </div>
</section>''', '''  <h2>參考資料與三種 ADT 比較 <span class="sec-badge">cppds §3 總覽</span></h2>
''' + gen('linear-reference') + '''
</section>
<section id="recap">
  <div class="section-number">SUMMARY · 重點回顧</div>
  <h2>重點回顧與常見疑問</h2>
''' + gen('linear-recap') + '''
</section>''')
once('''  <a href="#reference" data-target="reference"><span class="fn-num">REF</span><span class="fn-name">總覽比較</span></a>''',
     '''  <a href="#reference" data-target="reference"><span class="fn-num">REF</span><span class="fn-name">參考資料</span></a>
  <a href="#recap" data-target="recap"><span class="fn-num">SUM</span><span class="fn-name">重點回顧</span></a>''')
once('''    <a href="#reference"><span class="toc-num">REF</span>總覽比較</a>''',
     '''    <a href="#reference"><span class="toc-num">REF</span>參考資料與比較</a>
    <a href="#recap"><span class="toc-num">SUM</span>重點回顧與常見疑問</a>''')
once('''④ 最後翻 <a href="#cards">關鍵詞彙卡（16 張）</a>自測術語（中文為主、術語附英文），並用 REF 總覽區當速查表。''',
     '''④ 最後讀<a href="#recap">重點回顧</a>，再翻 <a href="#cards">關鍵詞彙卡（16 張）</a>自測術語（中文為主、術語附英文）。''')

# ---- fourth option for the existing three-option quizzes
EXTRA = {
    'qStack': ('回傳 <code>2</code>；內容 <code>[2]</code>', 'pop 只移除 top 的 7，壓在底下的 4 還在，所以內容是 [4, 2]。'),
    'qRev': ('push 時就把每個字元插到字串的最前面', 'push 只把字元放上 stack，沒有改動字串；反轉來自 pop 的順序。'),
    'qBase': ('<code>31</code>', '31 是 25 的八進位寫法（3×8 + 1）；這題問的是二進位。'),
    'qInfix': ('<code>A B C * +</code>', '這是 A + B * C 的後序：沒有括號時 * 先算。這題的括號讓 + 先算。'),
    'qCaret': ('把 ^ 的優先權設成和 * 相同；答案 5 3 * 4 2 - ^', '^ 必須比乘除先算。優先權相同時 5 * 3 會先結合，變成 (5 × 3) 的 (4 − 2) 次方 = 225。'),
    'qHp': ('David', 'David 是第一個出局的：第一輪傳了 7 次之後，山芋停在 David 手上。'),
    'qPrn': ('一小時會有 180 位學生送印', '實驗室平均只有 10 人、每人每小時印 2 次；180 是兩個工作之間平均相隔的秒數。'),
    'ex1': ('<code>3 2 1</code>', 'push1 push2 push3 之後連續 pop 三次，就得到 3 2 1，這是可能的。'),
    'ex2': ('<code>1</code>', '1 只是 15/12 的整數商，最後還要再加上 10。'),
    'ex3': ('<code>addFront</code> 與 <code>removeRear</code>', 'removeRear 在 vector 前端 erase(begin())，其餘元素都要往前搬，是 O(n)。'),
}
from html import escape
for qid, (text, fb) in EXTRA.items():
    old = f'''  </div>
  <div class="quiz-feedback" id="{qid}Feedback"></div>'''
    m = re.search(r'<div class="quiz-options" id="' + qid + r'Options">(.*?)\n  </div>\n  <div class="quiz-feedback"', s, re.S)
    assert m and m.group(1).count('class="quiz-opt"') == 3, qid
    opt = (f'<div class="quiz-opt" data-correct="false" data-fb="{escape(fb, quote=True)}" '
           f'onclick="quizCheck(\'{qid}\', this)"><span class="opt-letter">(D)</span> {text}</div>')
    i = m.end(1)
    s = s[:i] + opt + s[i:]

P.write_text(s)
print('ok')
