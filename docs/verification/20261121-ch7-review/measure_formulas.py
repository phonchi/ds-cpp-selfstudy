"""Measure trees.html after MathJax finishes: page width with details closed/open, and inline formulas
wider than the block they sit in (tables that scroll and shrink-to-fit cells are skipped).
Usage: python3 measure_formulas.py [page.html] [width ...]"""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
CHROME = '/home/phonchi/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'
page_file = ROOT / (sys.argv[1] if len(sys.argv) > 1 else 'trees.html')
widths = [int(w) for w in sys.argv[2:]] or [390, 360]
JS = """(openAll) => { if (openAll) document.querySelectorAll('details').forEach(d => d.open = true); const out = [];
 for (const it of MathJax.startup.document.getMathItemsWithin(document.body)) {
   const c = it.typesetRoot; if (!c || c.closest('.table-scroll')) continue;
   const m = c.querySelector('mjx-math'); const r = m.getBoundingClientRect(); if (!r.width) continue;
   let blk = c.parentElement; while (blk && getComputedStyle(blk).display === 'inline') blk = blk.parentElement;
   const cs = getComputedStyle(blk); const avail = blk.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
   if (r.width > avail - 1 && !(blk.scrollWidth > blk.clientWidth && getComputedStyle(c).overflowX === 'auto'))
     out.push([Math.round(r.width), Math.round(avail), it.display, it.math.slice(0, 90), blk.className]); }
 return {scrollWidth: document.documentElement.scrollWidth,
         nested: document.querySelectorAll('mjx-assistive-mml mjx-container').length, tooWide: out}; }"""
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
    for w in widths:
        for open_all in (False, True):
            pg = b.new_page(viewport={'width': w, 'height': 1000})
            pg.route('https://**/*', lambda r: r.continue_() if '/npm/mathjax@' in r.request.url else r.abort())
            pg.goto(page_file.as_uri(), wait_until='load')
            pg.wait_for_function('window.MathJax && MathJax.startup && MathJax.startup.promise', timeout=60000)
            pg.evaluate('MathJax.startup.promise.then(() => true)')
            pg.wait_for_timeout(300)
            res[f"{w}-{'open' if open_all else 'closed'}"] = pg.evaluate(JS, open_all)
            pg.close()
    b.close()
print(json.dumps(res, ensure_ascii=False, indent=1))
