"""One-time hand edit outside the gen regions of searching_sorting.html (Animator, main script).
setPointers() hides a pointer 200 ms later via setTimeout; buildBars() (reset / apply) replaces this.pointers
with {}, so the callback read undefined.el and threw. The callback now keeps its own reference. Rerunning is harmless."""
from pathlib import Path

PAGE = Path(__file__).resolve().parents[3] / 'searching_sorting.html'
s = PAGE.read_text()
OLD = """        this.pointers[name].el.style.opacity = '0';
        setTimeout(() => { this.pointers[name].el.style.display = 'none'; }, 200);"""
NEW = """        const p = this.pointers[name];
        p.el.style.opacity = '0';
        setTimeout(() => { p.el.style.display = 'none'; }, 200);   // keep p: reset may replace this.pointers"""
if NEW in s:
    print('already applied')
else:
    assert s.count(OLD) == 1
    PAGE.write_text(s.replace(OLD, NEW, 1))
    print('setPointers patched')
