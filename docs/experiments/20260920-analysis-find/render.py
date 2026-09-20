"""Render the authored HTML; route lecture images to verified local copies."""
import json
import re
from pathlib import Path
from urllib.parse import urlparse, unquote
from playwright.sync_api import sync_playwright
import pikepdf
import pymupdf
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parent
SITE = ROOT.parents[2]
SOURCE = Path('/home/phonchi/ds_cpp/Slides')
REPORT = ROOT / 'validation'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1440, 'height': 1000})
    errors, requests, loaded = [], [], []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('requestfailed', lambda r: requests.append({'url': r.url, 'error': r.failure}))
    def lecture_image(route):
        name = Path(unquote(urlparse(route.request.url).path)).name
        path = ROOT / name if name in ['pop_benchmark.png', 'dict_benchmark.png'] else SOURCE / 'imgs' / name
        assert path.is_file(), path
        loaded.append(str(path))
        route.fulfill(path=str(path), content_type='image/png')
    page.route('https://raw.githubusercontent.com/phonchi/nsysu-math208/**/imgs/*', lecture_image)
    page.goto((ROOT/'staged/02_Analysis.html').as_uri()+'?print-pdf', wait_until='networkidle', timeout=60000)
    page.wait_for_selector('.pdf-page', state='attached', timeout=30000)
    page.evaluate('''() => new Promise(resolve => {
      if (window.MathJax && MathJax.Hub) MathJax.Hub.Queue(resolve); else resolve();
    })''')
    page.evaluate('() => document.fonts.ready')
    imgs = page.evaluate('''() => Array.from(document.images).map(x => ({
      src:x.src, loaded:x.complete && x.naturalWidth>0, width:x.naturalWidth, height:x.naturalHeight
    }))''')
    assert len({x['src'] for x in imgs}) == 4 and all(x['loaded'] for x in imgs), imgs
    headings = page.locator('.reveal .slides h1, .reveal .slides h2').evaluate_all(
        "es => es.map(e => ({level:e.tagName==='H1'?1:2,title:e.textContent.replace(/¶/g,'').replace(/\\s+/g,' ').trim()}))")
    headings = list({h['title']:h for h in headings}.values())
    page.pdf(path=str(ROOT/'02_Analysis.raw.pdf'), print_background=True, prefer_css_page_size=True,
             display_header_footer=False)
    print('PDF rendered; images:', imgs, flush=True)
    report = {'images': imgs, 'local_image_sources': loaded, 'headings': headings,
              'page_errors': errors, 'failed_requests': requests,
              'reveal_pdf_pages': page.locator('.pdf-page').count()}
    (REPORT/'slides_browser.json').write_text(json.dumps(report, indent=2)+'\n')
    assert not errors and not requests, report
    page.close()
    # Check both modified figures and the updated code at desktop/mobile widths.
    checks = []
    for width in [1440, 390]:
        page = browser.new_page(viewport={'width':width, 'height':1000})
        page_errors=[]
        page.on('pageerror', lambda e: page_errors.append(str(e)))
        page.goto((SITE/'analysis.html').as_uri(), wait_until='networkidle', timeout=60000)
        for kind in ['pop', 'lookup']:
            figure = page.locator('#benchmark-'+kind+'-20260906')
            figure.scroll_into_view_if_needed()
            image = figure.locator('img')
            image.evaluate('img => img.decode()')
            box=figure.bounding_box(); imbox=image.bounding_box()
            assert box['x']>=0 and box['x']+box['width']<=width+1, box
            assert abs(imbox['height']/imbox['width']-1159/1800)<.01, imbox
            figure.screenshot(path=str(REPORT/f'{kind}-{width}.png'))
            checks.append({'width':width,'figure':kind,'bounds':box,'image_bounds':imbox})
        blocks=page.locator('.deck-extra').filter(has_text='std::find vs unordered_map::find')
        assert blocks.count()==1
        text=blocks.inner_text()
        assert '100\'000' in text and '800\'000' in text and 'm.find(target)' in text
        assert 'm.count(' not in text
        blocks.screenshot(path=str(REPORT/f'find-code-{width}.png'))
        # Exercise an existing primary interaction near this section.
        details=page.locator('details').filter(has=page.locator('summary',has_text='重現這兩張實測圖'))
        details.locator('summary').click()
        assert details.get_attribute('open') is not None
        details.locator('summary').click()
        assert details.get_attribute('open') is None
        assert not page_errors, page_errors
        page.close()
    (REPORT/'selfstudy_browser.json').write_text(json.dumps(checks, indent=2)+'\n')
    browser.close()

# Map every visible heading to the actual rendered page, including titles with code spans.
doc=pymupdf.open(ROOT/'02_Analysis.raw.pdf')
normalize=lambda s: re.sub(r'\s+', '', s).replace('¶','')
toc=[]
for h in headings:
    key=normalize(h['title'])
    found=[i+1 for i,pg in enumerate(doc) if key in normalize(pg.get_text())]
    assert found, ('Missing heading in rendered PDF',h)
    toc.append([h['level'],h['title'],found[0]])
assert len(toc)==7, toc
pdf=pikepdf.open(ROOT/'02_Analysis.raw.pdf')
removed_blank_tail=0
while len(pdf.pages)>1 and not doc[len(pdf.pages)-1].get_text().strip() and not doc[len(pdf.pages)-1].get_images():
    del pdf.pages[-1]
    removed_blank_tail+=1
with pdf.open_outline() as outline:
    outline.root.clear()
    root=pikepdf.OutlineItem(toc[0][1],toc[0][2]-1)
    for _, title, pg in toc[1:]: root.children.append(pikepdf.OutlineItem(title,pg-1))
    outline.root.append(root)
pdf.save(ROOT/'02_Analysis.pdf')
final=pymupdf.open(ROOT/'02_Analysis.pdf')
assert final.get_toc()==toc
figure_pages=[]
for i,pg in enumerate(final):
    # The four real lecture figures use image XObjects. Keep text/bookmark verification separate.
    if any(final.extract_image(x[0]).get('width')==1800 for x in pg.get_images()):
        figure_pages.append(i+1)
        pg.get_pixmap(matrix=pymupdf.Matrix(1.3,1.3)).save(REPORT/f'pdf-figure-page-{i+1}.png')
assert len(figure_pages)>=2, figure_pages
assert final[-1].get_text().strip(), 'Unexpected blank final page'
for _,title,pg in toc:
    assert normalize(title) in normalize(final[pg-1].get_text())
all_text='\n'.join(pg.get_text() for pg in final)
assert 'm.find' in all_text and '800' in all_text
(REPORT/'pdf.json').write_text(json.dumps({'pages':len(final),'bookmarks':toc,'figure_pages':figure_pages,
                                           'last_page_has_text':True,'removed_blank_tail':removed_blank_tail},indent=2)+'\n')
# Full-page contact sheet for a visual completeness pass.
thumbs=[]
for i,pg in enumerate(final):
    pix=pg.get_pixmap(matrix=pymupdf.Matrix(.25,.25))
    im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
    canvas=Image.new('RGB',(280,230),'#dddddd')
    im.thumbnail((270,205));canvas.paste(im,((280-im.width)//2,20))
    ImageDraw.Draw(canvas).text((8,5),str(i+1),fill='black');thumbs.append(canvas)
sheet=Image.new('RGB',(280*6,230*((len(thumbs)+5)//6)),'white')
for i,im in enumerate(thumbs):sheet.paste(im,((i%6)*280,(i//6)*230))
sheet.save(REPORT/'pdf-all-pages.jpg',quality=85)
print('PASS: PDF pages:',len(final),'bookmarks:',toc,'figure pages:',figure_pages,flush=True)
