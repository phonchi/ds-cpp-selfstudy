from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
pages = [p for p in ROOT.glob('*.html') if '下載 PDF</a>' in p.read_text()]
with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True, args=['--no-sandbox'])
    ctx = browser.new_context(accept_downloads=True)
    def route_local(route):
        name = route.request.url.split('/ds-cpp-selfstudy/', 1)[1].split('?')[0]
        path = ROOT / name
        if path.is_file(): route.fulfill(path=str(path))
        else: route.abort()
    ctx.route('https://phonchi.github.io/ds-cpp-selfstudy/**', route_local)
    page = ctx.new_page()
    for width in [1440, 390]:
        page.set_viewport_size({'width': width, 'height': 960})
        for p in pages:
            page.goto('https://phonchi.github.io/ds-cpp-selfstudy/' + p.name)
            links = page.locator('.sg-links')
            assert links.locator('a[download]').count() == 1
            assert links.locator('a[href$=".html#/"]').count() == 1
            assert links.locator('a[href$=".pdf"][target="_blank"]').count() == 1
            assert links.evaluate('(e) => e.getBoundingClientRect().right <= innerWidth')
            assert links.locator('a').evaluate_all('(els) => els.every(e => e.getBoundingClientRect().right <= innerWidth)')
            if p.name == 'introduction.html':
                links.screenshot(path=str(OUT / f'links-{width}.png'))
            print('PASS layout', width, p.name, flush=True)
    page.goto('https://phonchi.github.io/ds-cpp-selfstudy/introduction.html')
    with page.expect_download(timeout=60000) as info:
        page.locator('a[download]').click()
    download = info.value
    assert download.suggested_filename == '01_Introduction.pdf'
    path = Path(download.path())
    assert path.read_bytes().startswith(b'%PDF-')
    print('PASS real PDF download:', download.suggested_filename, path.stat().st_size, 'bytes', flush=True)
    browser.close()
