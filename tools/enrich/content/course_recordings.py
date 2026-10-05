"""Chapter recording links, kept when chapter pages are regenerated."""
from html import escape
import re

RECORDINGS = {
    'arrays': 'https://youtube.com/playlist?list=PLY4RRB8N-iEY&si=c1vywZ2WNu8th2hE',
    'linked_lists': 'https://youtube.com/playlist?list=PLY4RRB8N-iEY&si=c1vywZ2WNu8th2hE',
}

def apply_recording(text, chapter):
    link = f'<a id="recording-{chapter}" href="{escape(RECORDINGS[chapter], quote=True)}" target="_blank" rel="noopener">▶ 課程錄影</a>'
    pattern = rf'<a id="recording-{chapter}"[^>]*>.*?</a>'
    if re.search(pattern, text):
        return re.sub(pattern, lambda _: link, text, count=1)
    group = re.search(r'<div class="sg-links">.*?</div>', text, re.S)
    if not group:
        raise ValueError(f'Missing resource links: {chapter}')
    content, count = re.subn(r'(<a\b[^>]*\bdownload="[^"]*"[^>]*>.*?</a>)', lambda m: m[0]+link, group[0], count=1)
    if count != 1:
        raise ValueError(f'Missing PDF download link: {chapter}')
    return text[:group.start()]+content+text[group.end():]
