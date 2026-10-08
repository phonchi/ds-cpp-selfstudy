"""Density table for chapter pages: text (style/script removed), headings, figures, details, code, visible outputs, cards."""
import json, re, sys
from pathlib import Path
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[3]

def density(html):
    soup = BeautifulSoup(html, 'html.parser')
    for t in soup(['style', 'script']):
        t.decompose()
    main = soup.select_one('.container') or soup
    text = re.sub(r'\s+', '', main.get_text())
    outside = BeautifulSoup(str(main), 'html.parser')
    for d in outside.select('details'):
        d.decompose()
    text_outside = len(re.sub(r'\s+', '', outside.get_text()))
    vis_out = [e for e in main.select('.expected-out') if not e.find_parent('details')]
    m = re.search(r'const\s+FLASHCARDS\s*=\s*(\[.*?\]);', html, re.S)
    cards = len(json.loads(m.group(1))) if m else 0
    return {'text_chars': len(text), 'text_outside_details': text_outside, 'h2': len(main.select('h2')), 'h3': len(main.select('h3')),
            'img': len(main.select('img')), 'details': len(main.select('details')),
            'pseudo_code': len(main.select('.pseudo-code')), 'visible_expected_out': len(vis_out),
            'data_cpp': len(main.select('[data-cpp]')), 'quiz': len(main.select('.quiz-box')) + len(main.select('.sq-item')), 'flashcards': cards}

if __name__ == '__main__':
    pages = sys.argv[1:] or ['introduction', 'analysis', 'arrays', 'linked_lists']
    res = {p: density((ROOT / (p if p.endswith('.html') else p + '.html')).read_text()) for p in pages}
    print(json.dumps(res, ensure_ascii=False, indent=1))
