"""One-time fix in trees.html's BST-delete widget (page script, outside gen blocks): → 單步 now starts a
deletion paused at its first frame instead of auto-playing it, and ↺ 重建 drops the finished player so the
next → 單步 starts again. Refuses to run twice."""
import sys
from pathlib import Path

P = Path('/home/phonchi/ds-cpp-selfstudy/trees.html')
s = P.read_text()
if 'function startDel(autoplay = true)' in s:
    sys.exit('already applied')


def once(old, new):
    global s
    if s.count(old) != 1:
        sys.exit(f'expected 1 match: {old[:70]!r}')
    s = s.replace(old, new)


once('''    $('delPhase').textContent = '—';
  }

  function startDel() {''', '''    $('delPhase').textContent = '—';
    if (player) player.stop();
    player = null;
  }

  function startDel(autoplay = true) {''')
once('''    player.reset();
    player.play();
  }

  $('delApplyInit').onclick = rebuild;
  $('delPlay').onclick = startDel;
  $('delStep').onclick = () => { if (!player) startDel(); else player.step(); };''', '''    player.reset();
    if (autoplay) player.play();
  }

  $('delApplyInit').onclick = rebuild;
  $('delPlay').onclick = () => startDel(true);
  $('delStep').onclick = () => { if (!player) startDel(false); else player.step(); };''')
P.write_text(s)
print('delete widget fix applied')
