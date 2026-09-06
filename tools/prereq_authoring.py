"""Small helpers for authoring self-contained prerequisite HTML. HTML stays canonical."""
from pathlib import Path
import html,json,re,subprocess
from tools.apply_zh import apply_page
from tools.shuffle_quiz import ensure
ROOT=Path(__file__).resolve().parent.parent
NAMES=['p1_cpp_basics','p2_flow_control','p3_functions','p4_pointers_memory','p5_vector_string','p6_map_set','p7_files_exceptions','p8_oop_basics','p9_oop_advanced']
TITLES=['C++ 基礎與編譯流程','流程控制','函式與參考','陣列、指標與動態記憶體','vector 與 string','map、set 與迭代器','檔案與例外','類別與物件','類別延伸與模板']
def esc(s): return html.escape(str(s),quote=True).replace('\n','&#10;')
def para(s): return '<p>'+s+'</p>\n'
def code(s): return '<code>'+html.escape(s)+'</code>'
def fragment(s): return '<pre class="pseudo-code" data-cpp="fragment">'+html.escape(s.strip())+'</pre>\n'
def cpp(s,expected,stdin=None):
    attr=' data-cpp="run" data-expected="'+esc(expected)+'"'
    before=''
    if stdin is not None:
        attr+=' data-stdin="'+esc(stdin)+'"'
        before='<div class="expected-out"><span class="eo-tag">範例輸入</span><pre>'+esc(stdin)+'</pre></div>'
    return before+'<pre class="pseudo-code"'+attr+'>'+html.escape(s.strip())+'</pre><div class="expected-out"><span class="eo-tag">預期輸出</span><pre>'+esc(expected)+'</pre></div>\n'
def exercise(question,answer):
    return '<div class="info-box"><div class="info-label">動手練習</div><p>'+question+'</p><details><summary>看解答與理由</summary><p>'+answer+'</p></details></div>\n'
def table(headers,rows):
    return '<div class="cmp-table-wrap"><table class="cmp-table"><thead><tr>'+''.join('<th>'+x+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>\n'
def trace(key,title,intro,source,frames):
    # Each frame is a snapshot: note, vars (name/value object), optional line (0 based), output.
    data=json.dumps(frames,ensure_ascii=False).replace('<','\\u003c')
    lines='\n'.join('<span class="line">'+html.escape(line)+'</span>' for line in source.strip().splitlines())
    buttons=[('prev','btn-step','上一步'),('play','btn-play','▶ 播放'),('next','btn-step','下一步'),('reset','btn-reset','重設')]
    return '<div class="deck-extra lesson-trace" id="'+key+'"><h3>'+title+'</h3><p>'+intro+'</p><pre class="pseudo-code" data-cpp="fragment">'+lines+'</pre><div class="controls-bar">'+''.join('<button class="btn '+cls+'" data-action="'+act+'">'+label+'</button>' for act,cls,label in buttons)+'</div><div class="trace-note" aria-live="polite"></div><div class="trace-vars"></div><pre class="trace-output"></pre><script type="application/json" class="trace-data">'+data+'</script></div>\n'
RUNTIME=r'''
/* depth-runtime:start */
(() => {
 const esc = v => String(v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
 document.querySelectorAll('.lesson-trace').forEach(root => {
   const frames=JSON.parse(root.querySelector('.trace-data').textContent);
   let index=0,timer=null;const play=root.querySelector('[data-action="play"]');
   const stop=()=>{clearInterval(timer);timer=null;};
   function draw(){
     const frame=frames[index];
     root.querySelector('.trace-note').textContent=frame.note;
     root.querySelector('.trace-vars').innerHTML='<div class="cmp-table-wrap"><table class="cmp-table"><thead><tr><th>名稱／狀態</th><th>目前的值</th></tr></thead><tbody>'+Object.entries(frame.vars||{}).map(([k,v])=>'<tr><td>'+esc(k)+'</td><td>'+esc(v)+'</td></tr>').join('')+'</tbody></table></div>';
     root.querySelector('.trace-output').textContent=frame.output ? '目前輸出：\n'+frame.output : '目前尚無輸出';
     root.querySelectorAll('.line').forEach((el,i)=>el.classList.toggle('active',i===frame.line));
     play.textContent=timer?'⏸ 暫停':index===frames.length-1?'↻ 重播':'▶ 播放';
     root.dataset.frame=String(index);root.dataset.frames=String(frames.length);
   }
   function next(){index=Math.min(index+1,frames.length-1);if(index===frames.length-1)stop();draw();}
   play.onclick=()=>{if(timer){stop();draw();return;}if(index===frames.length-1)index=0;timer=setInterval(next,850);draw();};
   root.querySelector('[data-action="next"]').onclick=()=>{stop();next();};
   root.querySelector('[data-action="prev"]').onclick=()=>{stop();index=Math.max(0,index-1);draw();};
   root.querySelector('[data-action="reset"]').onclick=()=>{stop();index=0;draw();};draw();
 });
 document.querySelectorAll('.sq-item').forEach(q=>q.querySelectorAll('.sq-opt').forEach(b=>b.onclick=()=>{
   q.querySelectorAll('.sq-opt').forEach(x=>x.classList.remove('correct','wrong'));
   const good=b.dataset.c==='1';b.classList.add(good?'correct':'wrong');
   const f=q.querySelector('.sq-fb');f.textContent=b.dataset.fb;f.className='sq-fb show '+(good?'good':'bad');
 }));
 const grid=document.getElementById('fcGrid');
 function render(cards){grid.innerHTML=cards.map(c=>'<div class="fc-card" tabindex="0" role="button" aria-pressed="false"><div class="fc-inner"><div class="fc-face fc-front">'+esc(c.front)+'</div><div class="fc-face fc-back">'+esc(c.back)+'</div></div></div>').join('');}
 function flip(card,on){card.classList.toggle('flipped',on);card.setAttribute('aria-pressed',String(card.classList.contains('flipped')));}
 grid.onclick=e=>{const c=e.target.closest('.fc-card');if(c)flip(c,!c.classList.contains('flipped'));};
 grid.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){const c=e.target.closest('.fc-card');if(c){e.preventDefault();flip(c,!c.classList.contains('flipped'));}}};
 document.getElementById('fcFlipAll').onclick=()=>grid.querySelectorAll('.fc-card').forEach(c=>flip(c,true));
 document.getElementById('fcUnflip').onclick=()=>grid.querySelectorAll('.fc-card').forEach(c=>flip(c,false));
 document.getElementById('fcShuffle').onclick=()=>{const a=[...FLASHCARDS];for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}render(a);};render(FLASHCARDS);
 const links=[...document.querySelectorAll('.float-nav a[data-target]')];
 const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting)links.forEach(a=>a.classList.toggle('active',a.dataset.target===e.target.id));}),{rootMargin:'-10% 0px -65% 0px'});
 document.querySelectorAll('section[id]').forEach(el=>observer.observe(el));
})();
/* depth-runtime:end */
'''
def write_page(number,subtitle,sections,cards=None,questions=None,*,hero_svg):
    if not isinstance(hero_svg, str) or '<svg' not in hero_svg or 'hero-graph' not in hero_svg:
        raise ValueError('A page-specific hero-graph SVG is required; do not replace an existing page with a generic hero.')
    name=NAMES[number-1]; title=TITLES[number-1]
    # Use the existing main-chapter styling, not the former P1-P3 global overrides.
    head=subprocess.check_output(['git','show','05f490e:p4_pointers_memory.html'],cwd=ROOT,text=True).split('</head>')[0]
    head=re.sub(r'<title>.*?</title>',lambda _:f'<title>{title} — 先備 P{number}（C++）</title>',head,count=1)
    head+='\n<style>.lesson-trace .trace-note{margin:1rem 0;}.lesson-trace .trace-output{white-space:pre-wrap;overflow-wrap:anywhere;}.lesson-trace .line{min-height:1.4em;}.lesson-trace pre{margin:1rem 0;}.lesson-trace pre[data-cpp]{white-space:normal;}.lesson-trace .cmp-table{margin-top:.7rem;}@media(max-width:760px){.float-nav{display:none;}}</style>\n</head>'
    entries=[(s[0],s[1]) for s in sections]+[('bankquiz','自我檢測'),('cards','關鍵詞彙卡')]
    nav='<nav class="float-nav" id="floatNav" aria-label="章節導覽"><div class="fn-title">章節導覽</div>'+''.join(f'<a href="#{key}" data-target="{key}"><span class="fn-num">{i:02d}</span><span class="fn-name">{label}</span></a>' for i,(key,label) in enumerate(entries,1))+'<a href="#top" class="fn-top">↑ TOP</a></nav>'
    hero=f'<div class="hero" id="top"><div class="hero-grid"></div>{hero_svg}<div class="hero-content"><div class="chapter-tag">PREREQ P{number}</div><h1>{title}</h1><div class="subtitle">{subtitle}</div><div class="scroll-hint">逐節閱讀，先預測再操作<span>↓</span></div></div></div>'
    guide='<div class="study-guide"><div class="sg-title">本頁讀法</div><p>先讀用途與語法，再逐行追蹤例子。每支含 main 的完整程式請分開編譯；標成片段的程式會交代放置位置。遇到不熟的符號，先回看前面的說明，再做練習。</p><div class="sg-links"><a href="index.html#prereq">先備頁總覽</a><a href="#reference">語法速查</a></div></div>'
    toc='<div class="toc"><div class="toc-title">CONTENTS · 內容目錄</div><div class="toc-grid">'+''.join(f'<a href="#{key}"><span class="toc-num">{i:02d}</span>{label}</a>' for i,(key,label) in enumerate(entries,1))+'</div></div>'
    body=''.join(f'<section id="{key}"><div class="section-number">PART {i:02d}</div><h2>{heading}</h2>\n{content}\n</section>\n' for i,(key,heading,content) in enumerate(sections,1))
    tail='<section id="bankquiz"></section><section id="cards"><div class="section-number">CARDS</div><h2>關鍵詞彙卡</h2><p>先用自己的話解釋，再翻面核對；可點擊卡片或使用 Enter／空白鍵。</p><div class="fc-controls"><button id="fcShuffle">洗牌</button><button id="fcFlipAll">全部翻面</button><button id="fcUnflip">全部正面</button></div><div class="fc-grid" id="fcGrid"></div></section>'
    prev=f'<a class="prev" href="{NAMES[number-2]}.html"><div class="nav-dir">上一頁</div><div class="nav-title">{TITLES[number-2]}</div></a>' if number>1 else '<span></span>'
    nxt=NAMES[number] if number<9 else 'introduction'; nt=TITLES[number] if number<9 else 'C++ 導論'
    tail+='<div class="chapter-nav">'+prev+'<a class="home" href="index.html#prereq"><div class="nav-dir">INDEX</div><div class="nav-title">先備頁總覽</div></a>'+f'<a class="next" href="{nxt}.html"><div class="nav-dir">下一頁</div><div class="nav-title">{nt}</div></a></div>'
    page=head+'\n<body>'+nav+hero+'<div class="container">'+guide+toc+body+tail+'</div><footer>資料結構 × C++ 互動自學網站</footer><script>\nconst FLASHCARDS = [];\n'+RUNTIME+'</script></body></html>\n'
    (ROOT/f'{name}.html').write_text(page)
    for folder,data in [('flashcards_zh',cards),('questions_zh',questions)]:
        if data is not None:(ROOT/f'data/{folder}/p{number}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    apply_page(name,f'p{number}');ensure(ROOT/f'{name}.html')
