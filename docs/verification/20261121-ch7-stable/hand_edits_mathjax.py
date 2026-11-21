#!/usr/bin/env python3
"""searching_sorting.html: drop the second MathJax.typesetPromise() in the DOMContentLoaded handler.

The page script is outside the gen regions, so enrich_search.py does not touch it; this edit is idempotent.
MathJax typesets the page itself when it is ready. A second full typeset that overlaps the first also
renders the hidden assistive MathML inside each mjx-container, which made the page wider than a phone
screen (scrollWidth 410-432 px at a 390 px viewport, depending on load timing). No script on this page
writes TeX into the DOM after load, so nothing relies on the second pass.
"""
from pathlib import Path

PAGE = Path(__file__).resolve().parents[3] / 'searching_sorting.html'
OLD = """  // re-typeset MathJax just in case (info-cards already rendered during page load)
  if (window.MathJax && MathJax.typesetPromise) {
    MathJax.typesetPromise();
  }
"""
NEW = """  // MathJax typesets the page by itself once it is ready. A second typesetPromise() here would also
  // render the hidden assistive MathML and widen the page on phones, so it is not called.
"""
s = PAGE.read_text()
if OLD in s:
    assert s.count(OLD) == 1
    s = s.replace(OLD, NEW)
    PAGE.write_text(s)
    print('replaced')
else:
    assert NEW in s, 'neither the old nor the new block was found'
    print('already applied')
