"""Generator-owned maze trace: shared grid, call stack, and short-circuit returns.

The sample is embedded at build time so the player does not need a network fetch.
"""
import json
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_ROWS = (_ROOT / 'data/mazes/maze2.txt').read_text(encoding='utf-8').splitlines()
assert len(_ROWS) == 11 and all(len(row) == 22 for row in _ROWS)

MAZE_STYLE = '''<style id="recursion-maze-style">
.maze-map {display:grid;grid-template-columns:repeat(var(--maze-cols),minmax(0,1fr));width:min(100%,32rem);gap:1px;background:var(--card-border);padding:2px;margin:.6rem auto;font-family:'JetBrains Mono',monospace;}
.maze-cell {display:flex;align-items:center;justify-content:center;aspect-ratio:1;min-width:0;font-size:clamp(.6rem,1.5vw,.92rem);line-height:1;background:var(--card);color:var(--ink);}
.maze-cell.wall {background:var(--card-border);}
.maze-cell.tried {color:var(--accent2);font-weight:700;}
.maze-cell.dead {color:var(--accent);font-weight:700;}
.maze-cell.path {color:var(--accent3);font-weight:700;}
.maze-cell.start {color:var(--accent2);font-weight:700;}
.maze-cell.current {outline:2px solid var(--accent2);outline-offset:-2px;background:var(--highlight);}
.maze-legend,.maze-position,.maze-checks {font-size:.8rem;line-height:1.7;overflow-wrap:anywhere;}
.maze-legend {margin:.5rem 0;}
.maze-position {margin:.5rem 0;color:var(--ink);}
.maze-checks {margin:.35rem 0;color:var(--ink);}
.maze-state-row {display:flex;flex-wrap:wrap;align-items:center;gap:.4rem .8rem;margin:.7rem 0;}
.maze-state-row strong {color:var(--accent2);}
.maze-stack {max-height:19rem;overflow-y:auto;overscroll-behavior:contain;border:1px solid var(--card-border);padding:.5rem;background:var(--paper);}
.maze-stack-frame {padding:.55rem .65rem;margin-bottom:.45rem;background:var(--card);border:1px solid var(--card-border);font-size:.8rem;line-height:1.6;overflow-wrap:anywhere;}
.maze-stack-frame:last-child {margin-bottom:0;}
.maze-stack-frame.active {border-color:var(--accent2);background:var(--highlight);}
.maze-stack-frame code {padding:0;background:none;white-space:normal;}
.maze-stack-frame .maze-frame-title {font-weight:700;}
.maze-stack-frame small {display:block;font-size:.75rem;}
.maze-stack-empty {font-size:.82rem;margin:.2rem;color:var(--ink);}
.maze-controls label {display:flex;align-items:center;gap:.4rem;flex-wrap:wrap;}
.maze-controls select {max-width:100%;}
@media(max-width:600px){.maze-map{width:100%;}.maze-cell{font-size:.67rem;}.maze-stack{max-height:17rem;}.maze-controls{gap:.5rem;}}
</style>'''

MAZE_JS = r'''/* Maze: parameters identify the checked square; return changes control flow. */
const MAZE_ROWS = __MAZE_ROWS__;
const MAZE_SMALL_ROWS = [
  '++++++++++++',
  '+   +   ++ +',
  '+ +++ + ++ +',
  '+ +   +    +',
  '+ + +++ + ++',
  '+S      +   ',
  '++++++++++++',
];
const MAZE_DIRECTIONS = [
  {name:'北', dr:-1, dc:0, line:9},
  {name:'南', dr:1, dc:0, line:10},
  {name:'西', dr:0, dc:-1, line:11},
  {name:'東', dr:0, dc:1, line:12},
];
let mazePlayer = null;

function mazeFrames(rows = MAZE_ROWS) {
  const grid = rows.map(row => Array.from(row, ch => ch === 'E' ? ' ' : ch));
  if (!grid.length || !grid[0].length || grid.some(row => row.length !== grid[0].length)) {
    throw new Error('迷宮必須是每列等寬的非空格子表。');
  }
  const starts = [];
  grid.forEach((row,r) => row.forEach((ch,c) => { if (ch === 'S') starts.push([r,c]); }));
  if (starts.length !== 1) throw new Error('迷宮必須有一個起點 S。');
  const R = grid.length, C = grid[0].length;
  const stack = [], frames = [];
  let nextId = 1, lastMarked = null;
  function snapshot(kind, cur, msg, line, extra = {}) {
    frames.push({kind, grid:grid.map(row => [...row]), cur:cur ? [...cur] : null,
      lastMarked:lastMarked ? [...lastMarked] : null,
      stack:stack.map(frame => ({...frame, checks:{...frame.checks}, skipped:[...frame.skipped]})),
      msg, line, ...extra});
  }
  snapshot('ready', null, '從 S 開始。先檢查格子，再決定是否展開四個方向。', null);
  function search(row, col) {
    const call = {id:nextId++, row, col, phase:'入口檢查', nextDirection:null,
      pendingDirection:null, returnValue:null, checks:{wall:null, visited:null, exit:null}, skipped:[]};
    stack.push(call);
    snapshot('enter', [row,col], `呼叫 searchFrom(${row}, ${col})：推入一個 frame。`, 1);
    function finish(value, line, reason) {
      call.phase = '返回'; call.returnValue = value;
      const parent = stack.length > 1 ? stack[stack.length-2] : null;
      snapshot('return', [row,col], reason + (parent
        ? ` 回到 (${parent.row},${parent.col}) 的 ${parent.pendingDirection}方呼叫之後，繼續判斷 ||。`
        : ' 回到最初的呼叫者。'), line, {returned:value, returningFrom:[row,col]});
      stack.pop();
      return value;
    }
    // Normal traces cannot reach this guard: an open edge returns before recursing.
    if (row < 0 || row >= R || col < 0 || col >= C) {
      return finish(false, null, '範例防護：座標超出地圖，回傳 false。');
    }
    call.checks.wall = grid[row][col] === '+';
    snapshot('guard', [row,col], `入口檢查 1：(${row},${col}) ${call.checks.wall ? '是牆，停止探索。' : '不是牆。'}`, 2, {guard:'wall',guardResult:call.checks.wall});
    if (call.checks.wall) return finish(false, 2, '遇到牆，回傳 false；格子內容不變。');
    call.checks.visited = grid[row][col] === '.' || grid[row][col] === '-';
    snapshot('guard', [row,col], `入口檢查 2：(${row},${col}) ${call.checks.visited ? '已有探索標記，不再展開。' : '還沒有探索標記。'}`, 3, {guard:'visited',guardResult:call.checks.visited});
    if (call.checks.visited) return finish(false, 3, '遇到已探索的格子，回傳 false；標記保留。');
    call.checks.exit = row === 0 || row === R-1 || col === 0 || col === C-1;
    snapshot('guard', [row,col], `入口檢查 3：(${row},${col}) ${call.checks.exit ? '是可通行的邊界，找到出口。' : '不是邊界。'}`, 4, {guard:'exit',guardResult:call.checks.exit});
    if (call.checks.exit) {
      grid[row][col] = 'O'; lastMarked = [row,col]; call.phase = '標記出口';
      snapshot('mark', [row,col], '將出口標成 O，接著回傳 true。', 5, {update:[row,col,'O']});
      return finish(true, 6, '找到出口，回傳 true。');
    }
    grid[row][col] = '.'; lastMarked = [row,col]; call.phase = '開始探索'; call.nextDirection = '北';
    snapshot('mark', [row,col], `將 (${row},${col}) 標成 .，依序嘗試北、南、西、東。`, 8, {update:[row,col,'.']});
    let found = false;
    for (let i = 0; i < MAZE_DIRECTIONS.length; i++) {
      const d = MAZE_DIRECTIONS[i];
      call.phase = '等待子呼叫'; call.pendingDirection = d.name; call.nextDirection = d.name; call.returnValue = null;
      snapshot('call', [row,col], `(${row},${col}) 嘗試${d.name}方；本層留在堆疊中等待結果。`, d.line,
        {direction:d.name, child:[row+d.dr,col+d.dc]});
      found = search(row+d.dr, col+d.dc);
      call.returnValue = found; call.phase = '子呼叫已返回';
      call.nextDirection = found ? null : (MAZE_DIRECTIONS[i+1]?.name || null);
      call.skipped = found ? MAZE_DIRECTIONS.slice(i+1).map(x=>x.name) : [];
      let message;
      if (found) {
        message = `${d.name}方回傳 true。` + (call.skipped.length
          ? `|| 短路：略過${call.skipped.join('、')}方，不再呼叫。`
          : '四個方向中的最後一個成功。');
      } else {
        message = `${d.name}方回傳 false。` + (call.nextDirection
          ? `回到 (${row},${col})，接著嘗試${call.nextDirection}方；已有的探索標記保留。`
          : '四個方向都回傳 false，現在才判定本格是死路。');
      }
      snapshot('resume', [row,col], message, d.line,
        {childResult:found, child:[row+d.dr,col+d.dc], direction:d.name, skipped:[...call.skipped]});
      if (found) break;
    }
    call.pendingDirection = null; call.nextDirection = null; call.phase = '四方向探索後';
    grid[row][col] = found ? 'O' : '-'; lastMarked = [row,col];
    snapshot('mark', [row,col], found
      ? `子呼叫找到出口，將 (${row},${col}) 標成成功路徑 O。`
      : `四方向皆失敗，將 (${row},${col}) 標成死路 -。`, found ? 13 : 14,
      {update:[row,col,grid[row][col]]});
    return finish(found, 15, `searchFrom(${row}, ${col}) 回傳 ${found}。`);
  }
  const found = search(...starts[0]);
  snapshot('finish', null, found
    ? '搜尋完成：searchFrom 回傳 true。O 標出從起點到出口的路徑，探索標記仍保留。'
    : '搜尋完成：searchFrom 回傳 false。起點無法到達任何可通行的邊界。', null, {found});
  return frames;
}

function mazeEscape(value) {
  return String(value).replace(/[&<>"']/g, ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
}
function mazeApply(frame) {
  const map = $('mazeVis');
  map.style.setProperty('--maze-cols', frame.grid[0].length);
  const classes = {'+':'wall','.':'tried','-':'dead','O':'path','S':'start'};
  const names = {'+':'牆',' ':'未探索空格','.':'已探索','-':'死路','O':'成功路徑','S':'起點'};
  map.innerHTML = frame.grid.map((row,r)=>row.map((ch,c)=>{
    const current = frame.cur && frame.cur[0]===r && frame.cur[1]===c;
    return `<span class="maze-cell ${classes[ch]||''}${current?' current':''}" data-row="${r}" data-col="${c}" data-state="${ch}" aria-label="第 ${r} 列、第 ${c} 欄：${names[ch]||ch}${current?'，目前檢查':''}">${ch===' '?'&nbsp;':mazeEscape(ch)}</span>`;
  }).join('')).join('');
  const coord = p => p ? `(${p[0]}, ${p[1]})` : '無';
  $('mazePosition').textContent = `目前檢查：${coord(frame.cur)}；最近一次更新標記：${coord(frame.lastMarked)}`;
  const active = frame.stack[frame.stack.length-1];
  $('mazePhase').textContent = active ? active.phase : (frame.kind==='finish'?'完成':'尚未呼叫');
  $('mazeDepth').textContent = `${frame.stack.length} 層`;
  const check = value => value===null?'未檢查':String(value);
  $('mazeChecks').textContent = active
    ? `入口檢查：牆 ${check(active.checks.wall)}；已探索 ${check(active.checks.visited)}；出口 ${check(active.checks.exit)}`
    : '入口檢查依序進行；四方向皆失敗是在探索之後才判定。';
  const stackEl = $('mazeStack');
  stackEl.innerHTML = frame.stack.length ? frame.stack.slice().reverse().map((call,i)=>{
    let pending;
    if (call.phase==='返回') pending=`準備回傳 ${call.returnValue}`;
    else if (call.phase==='等待子呼叫') pending=`等待${call.pendingDirection}方的結果`;
    else if (call.phase==='子呼叫已返回') pending=call.returnValue
      ? `子呼叫回傳 true${call.skipped.length?'；略過'+call.skipped.join('、')+'方':''}`
      : `子呼叫回傳 false${call.nextDirection?'；下一個方向：'+call.nextDirection:'；四方向皆失敗'}`;
    else pending=call.nextDirection?`下一個方向：${call.nextDirection}`:call.phase;
    return `<div class="maze-stack-frame${i===0?' active':''}" data-call-id="${call.id}"><div class="maze-frame-title"><code>searchFrom(${call.row}, ${call.col})</code>${i===0?' · top':''}</div><small>${mazeEscape(pending)}</small></div>`;
  }).join('') : '<p class="maze-stack-empty">呼叫堆疊目前是空的。</p>';
  // The active call is rendered first; only this panel scrolls, not the document.
  stackEl.scrollTop = 0;
  setStatus('mazeStatus', mazeEscape(frame.msg));
  hlLine('mazeCode', frame.line);
}
function mazeMake(play) {
  const rows = $('mazeMap').value === 'small' ? MAZE_SMALL_ROWS : MAZE_ROWS;
  mazePlayer = freshPlayer(mazePlayer, {frames:mazeFrames(rows),apply:mazeApply,delayInput:$('mazeSpeed')}, play);
}
function mazeStart() { mazeMake(true); }
function mazeReset() { mazeMake(false); }
function mazeNextReturn() {
  if (!mazePlayer) mazeMake(false);
  mazePlayer.pause();
  const index = mazePlayer.frames.findIndex((f,i)=>i>mazePlayer.i && (f.kind==='resume'||f.kind==='finish'));
  if (index < 0) return;
  mazePlayer.i = index;
  mazePlayer._done = index === mazePlayer.frames.length-1;
  mazePlayer.apply(mazePlayer.frames[index]);
}

$('mazeMap').addEventListener('change', mazeReset);
mazeMake(false);
'''.replace('__MAZE_ROWS__', json.dumps(_ROWS, ensure_ascii=False))
