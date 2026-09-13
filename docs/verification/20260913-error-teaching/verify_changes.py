"""Recheck new examples and language candidates; --browser checks local rendering."""
import argparse, ast, html, json, re, subprocess, tempfile
from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent

def examples():
    reports = []
    for name in ('p1_cpp_basics.html', 'arrays.html'):
        soup = BeautifulSoup((ROOT / name).read_text(), 'html.parser')
        for block in soup.select('[data-cpp="run"]'):
            expected = block.get('data-expected', '')
            code = block.get_text()
            variants = [('original', code, expected)]
            if block.get('id') == 'division-guard':
                variants += [('nonzero', code.replace('count = 0', 'count = 3'), '4\n')]
            if block.get('id') == 'bounds-guard':
                variants += [(f'index-{i}', code.replace('index = 3', f'index = {i}'), result) for i, result in ((-1, 'Index out of range\n'), (0, '70\n'), (2, '90\n'))]
            for variant, source, result in variants:
                with tempfile.TemporaryDirectory(prefix='teaching-verify-') as d:
                    folder = Path(d)
                    (folder/'main.cpp').write_text(source)
                    command = ['g++','-std=c++17','-Wall','-Wextra','-pedantic','-fsanitize=undefined','-fno-sanitize-recover=all','main.cpp','-o','main']
                    c = subprocess.run(command, cwd=folder, capture_output=True, text=True, timeout=20)
                    assert c.returncode == 0, c.stderr
                    r = subprocess.run(['./main'], cwd=folder, capture_output=True, text=True, timeout=5)
                    assert r.returncode == 0 and r.stdout.rstrip() == result.rstrip() and not r.stderr, (name, variant, r.stdout, r.stderr)
                    reports.append({'page':name,'id':block.get('id'),'variant':variant,'command':command,'stdout':r.stdout,'stderr':r.stderr,'exit':r.returncode})
    (OUT/'new-examples.json').write_text(json.dumps(reports, ensure_ascii=False, indent=2)+'\n')
    print('New complete programs and boundary variants:', len(reports), 'passed')

def language():
    from opencc import OpenCC
    cc = OpenCC('s2t')
    # Individually reviewed variants/shared traditional characters; not a blind conversion.
    accepted = set('台吃群干秘划占床游峰准')
    reports=[]
    for p in sorted([*ROOT.glob('*.html'), *ROOT.glob('data/flashcards_zh/*.json'), *ROOT.glob('data/questions_zh/*.json'), *ROOT.glob('tools/**/*.py')]):
        counts=Counter(c for c in p.read_text() if '\u4e00' <= c <= '\u9fff' and cc.convert(c) != c)
        rejected=set(counts)-accepted
        assert not rejected, (str(p.relative_to(ROOT)), sorted(rejected))
        if counts: reports.append({'file':str(p.relative_to(ROOT)), 'reviewed_candidates':dict(counts)})
    (OUT/'language-candidates.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
    print('All 22 HTML pages, question/card sources and Python generators: no unreviewed simplified candidates')

def browser():
    from playwright.sync_api import sync_playwright
    reports=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(args=['--no-sandbox','--disable-dev-shm-usage'])
        for width in (1440,390):
            page=browser.new_page(viewport={'width':width,'height':960})
            page.route(re.compile('^https?://'),lambda route:route.abort())
            errors=[]
            page.on('pageerror', lambda error:errors.append(str(error)))
            for p in sorted(ROOT.glob('*.html')):
                errors.clear()
                page.goto(p.as_uri(),wait_until='load')
                page.locator('h1').first.wait_for()
                assert not errors, (p.name,errors)
                overflow=page.evaluate('document.documentElement.scrollWidth > innerWidth + 2')
                assert not overflow, (p.name,width,'document overflow')
                reports.append({'page':p.name,'width':width,'javascript_errors':list(errors),'overflow':overflow})
            for name,anchor in (('p1_cpp_basics.html','errors'),('p1_cpp_basics.html','runtime-errors'),('introduction.html','exceptions'),('p4_pointers_memory.html','pitfalls')):
                page.goto((ROOT/name).as_uri(),wait_until='load')
                target=page.locator('#'+anchor)
                if not target.count():
                    # P4's actual dangling pointer section is found by its teaching text.
                    target=page.locator('section').filter(has_text='目標已失效，不可再解參考').first
                target.evaluate("(el)=>window.scrollTo({top:el.getBoundingClientRect().top+scrollY-12,behavior:'instant'})")
                page.screenshot(path=str(OUT/'screenshots'/f'{name[:-5]}-{anchor}-{width}.png'))
            page.close()
        browser.close()
    (OUT/'site-browser.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
    print('All local pages at desktop/mobile widths:',len(reports),'passed')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--browser',action='store_true');args=parser.parse_args()
    if args.browser: browser()
    else: examples();language()
