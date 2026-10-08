"""以真實網路載入 MathJax，統計第 4–9 章公式的排版結果並截圖。"""
import json, pathlib
from playwright.sync_api import sync_playwright
CHROME = '/home/phonchi/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'
ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).parent
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, headless=True, args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    for name in ['linked_lists', 'linear_structures', 'recursion', 'searching_sorting', 'graphs', 'trees']:
        errs.clear()
        pg.goto((ROOT / f'{name}.html').as_uri(), wait_until='load')
        pg.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
        ok = pg.evaluate("""async()=>{for(let i=0;i<60&&!(window.MathJax&&MathJax.typesetPromise);i++)await new Promise(r=>setTimeout(r,500));
          if(!(window.MathJax&&MathJax.typesetPromise))return false; await MathJax.typesetPromise(); return true}""")
        info = pg.evaluate("""()=>{const c=document.querySelectorAll('mjx-container').length;
          const merr=document.querySelectorAll('mjx-merror, [data-mjx-error]').length;
          const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let raw=[];let n;
          while(n=walker.nextNode()){const p=n.parentElement; if(!p||p.closest('script,style,pre,code,textarea,.pseudo-code'))continue;
            const t=n.textContent; const m=t.match(/\\$[^$\\n]{1,60}\\$/); if(m)raw.push(m[0]);}
          return {containers:c, errors:merr, raw_dollar:raw.slice(0,10), raw_count:raw.length}}""")
        info['mathjax_loaded'] = ok; info['page_errors'] = list(errs)
        res[name] = info
        el = pg.query_selector('mjx-container[display="true"]') or pg.query_selector('mjx-container')
        if el:
            el.scroll_into_view_if_needed(); pg.screenshot(path=str(OUT / f'{name}-math.png'))
    b.close()
(OUT / 'mathjax-results.json').write_text(json.dumps(res, ensure_ascii=False, indent=1))
print(json.dumps(res, ensure_ascii=False, indent=1))
