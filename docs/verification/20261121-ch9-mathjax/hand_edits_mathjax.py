#!/usr/bin/env python3
"""trees.html: drop the second MathJax.typesetPromise() in the DOMContentLoaded handler.

Same fix as chapter 7 (docs/verification/20261121-ch7-stable/hand_edits_mathjax.py). The page script is
outside the gen regions, so enrich_trees.py does not touch it; this edit is idempotent. MathJax typesets
the page itself when it is ready. A second full typeset that overlaps the first also renders the hidden
assistive MathML inside each mjx-container and widens the page on phones. The page has no <math> source
and no script writes TeX into the DOM after load, so nothing relies on the second pass.
"""
from pathlib import Path

PAGE = Path(__file__).resolve().parents[3] / 'trees.html'
OLD = """  // MathJax retypeset
  if (window.MathJax && window.MathJax.typesetPromise) {
    window.MathJax.typesetPromise().catch(()=>{});
  }
"""
NEW = """  // MathJax typesets the page by itself once it is ready. A second typesetPromise() here would also
  // render the hidden assistive MathML and widen the page on phones, so it is not called.
"""
s = PAGE.read_text()
if OLD in s:
    assert s.count(OLD) == 1
    PAGE.write_text(s.replace(OLD, NEW))
    print('replaced')
else:
    assert NEW in s, 'neither the old nor the new block was found'
    print('already applied')
