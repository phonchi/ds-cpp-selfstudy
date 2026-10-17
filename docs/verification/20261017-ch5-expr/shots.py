"""Screenshots of the blocks added on 2026-10-17 (details opened)."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).parent
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (1440, 390):
        pg = b.new_page(viewport={'width': w, 'height': 900})
        pg.route('http*://**', lambda r: r.abort())
        pg.goto((ROOT / 'linear_structures.html').as_uri())
        pg.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
        targets = {
            'stack-infobox': "#stack .info-box",
            'queue-infobox': "#queue .info-box",
            'deque-impl': "details:has(> summary:text-matches('std::deque 怎麼讓'))",
            'i2prefix': "details:has(> summary:text-matches('中序轉前序'))",
            'tokens': "details:has(> summary:text-matches('isalnum'))",
        }
        for name, sel in targets.items():
            pg.locator(sel).first.screenshot(path=str(OUT / f'new-{name}-{w}.png'))
    b.close()
