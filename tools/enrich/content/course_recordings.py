"""Chapter recording links, kept when chapter pages are regenerated."""
from html import escape
import re

WEEK5 = 'https://youtube.com/playlist?list=PLY4RRB8N-iEY&si=c1vywZ2WNu8th2hE'
WEEK6 = 'PLKfVlE23FEcw'
WEEK7 = 'PLZAdKohP8LHE'

def _video(video_id, playlist=WEEK6):
    return f'https://www.youtube.com/watch?v={video_id}&list={playlist}'

# Each chapter lists (label, url); the first link keeps the id recording-<chapter>.
RECORDINGS = {
    'arrays': [('▶ 課程錄影', WEEK5)],
    'linked_lists': [
        ('▶ 課程錄影', WEEK5),
        ('▶ 錄影：Unordered List', _video('9xzhOsXvi8k')),
        ('▶ 錄影：Ordered List 與其他變形', _video('I2cQ1JzTEls')),
    ],
    'linear_structures': [
        ('▶ 錄影：Linear ADT 與 Stack', _video('4sY0K264UIo')),
        ('▶ 錄影：Infix、Postfix 與 Prefix', _video('NjoC3Aj30Z0', WEEK7)),
        ('▶ 錄影：Queue', _video('6QvTp5mM6WY', WEEK7)),
        ('▶ 錄影：Deque', _video('j-WFKsrGYqo', WEEK7)),
    ],
}

def _links(chapter):
    out = []
    for i, (label, url) in enumerate(RECORDINGS[chapter]):
        rid = f'recording-{chapter}' if i == 0 else f'recording-{chapter}-{i + 1}'
        out.append(f'<a id="{rid}" href="{escape(url, quote=True)}" target="_blank" rel="noopener">{escape(label)}</a>')
    return ''.join(out)

def apply_recording(text, chapter):
    text = re.sub(rf'<a id="recording-{chapter}(?:-\d+)?"[^>]*>.*?</a>', '', text)
    group = re.search(r'<div class="sg-links">.*?</div>', text, re.S)
    if not group:
        raise ValueError(f'Missing resource links: {chapter}')
    content, count = re.subn(r'(<a\b[^>]*\bdownload="[^"]*"[^>]*>.*?</a>)', lambda m: m[0]+_links(chapter), group[0], count=1)
    if count != 1:
        raise ValueError(f'Missing PDF download link: {chapter}')
    return text[:group.start()]+content+text[group.end():]
