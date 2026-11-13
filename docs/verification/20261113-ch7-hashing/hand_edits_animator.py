"""Hand edits outside the gen regions of searching_sorting.html (Animator, main script).
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

# Median of three: the pivot choice compares the three candidates (3 comparisons at most) but cmp was not
# increased, so the two pivot strategies could not be compared fairly. Count them and say so.
s = PAGE.read_text()
OLD2 = """      pivotIdx = candidates[1].i;
      frames.push({arr:[...a], origIdx:[...oi], highlights:{[first]:'compare',[mid]:'compare',[last]:'compare'}, message:`三者取中：a[${first}]=${a[first]}, a[${mid}]=${a[mid]}, a[${last}]=${a[last]} → 中位數是 a[${pivotIdx}]=${a[pivotIdx]}`,"""
NEW2 = """      pivotIdx = candidates[1].i;
      cmp += 3;   // the median of three values takes at most 3 comparisons
      frames.push({arr:[...a], origIdx:[...oi], highlights:{[first]:'compare',[mid]:'compare',[last]:'compare'}, message:`三者取中（比較 3 次）：a[${first}]=${a[first]}, a[${mid}]=${a[mid]}, a[${last}]=${a[last]} → 中位數是 a[${pivotIdx}]=${a[pivotIdx]}`,"""
if NEW2 in s or 'cmp += medCmp' in s:   # superseded by the explicit count below
    print('median count already applied')
else:
    assert s.count(OLD2) == 1
    PAGE.write_text(s.replace(OLD2, NEW2, 1))
    print('median count patched')

# Count the median-of-three comparisons that are actually made: sort the three candidates with explicit
# compare-and-swap steps (2 or 3 comparisons) instead of Array.sort plus a fixed "+ 3".
s = PAGE.read_text()
OLD3 = """      const candidates = [{i:first, v:a[first]}, {i:mid, v:a[mid]}, {i:last, v:a[last]}].sort((x,y) => x.v - y.v);
      pivotIdx = candidates[1].i;
      cmp += 3;   // the median of three values takes at most 3 comparisons
      frames.push({arr:[...a], origIdx:[...oi], highlights:{[first]:'compare',[mid]:'compare',[last]:'compare'}, message:`三者取中（比較 3 次）："""
NEW3 = """      const candidates = [{i:first, v:a[first]}, {i:mid, v:a[mid]}, {i:last, v:a[last]}];
      let medCmp = 0;
      const less = (x, y) => { medCmp++; return x.v < y.v; };   // count every comparison actually made
      if (less(candidates[1], candidates[0])) [candidates[0], candidates[1]] = [candidates[1], candidates[0]];
      if (less(candidates[2], candidates[1])) {
        [candidates[1], candidates[2]] = [candidates[2], candidates[1]];
        if (less(candidates[1], candidates[0])) [candidates[0], candidates[1]] = [candidates[1], candidates[0]];
      }
      pivotIdx = candidates[1].i;
      cmp += medCmp;
      frames.push({arr:[...a], origIdx:[...oi], highlights:{[first]:'compare',[mid]:'compare',[last]:'compare'}, message:`三者取中（比較 ${medCmp} 次）："""
if NEW3 in s:
    print('explicit median count already applied')
else:
    assert s.count(OLD3) == 1
    PAGE.write_text(s.replace(OLD3, NEW3, 1))
    print('explicit median count patched')
