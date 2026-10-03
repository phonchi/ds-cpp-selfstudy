/* gen:arrays-widgets */
/* 第三章互動元件。播放器一律用頁內 Player（player-v2）；frames 是純資料快照，
   apply(frame) 只依 frame 重畫，重播或單步都不會重複執行操作。 */
const arraysEsc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/* ---------- 位址計算：直接點選，即時計算 ---------- */
const ADDR_BASE = 64, ADDR_N = 6;
let addrSel = -1;
const addrHex = n => '0x' + n.toString(16).padStart(6, '0');
function addrRender() {
  const size = parseInt($('addrSize').value, 10);
  const vis = $('addrVis'); vis.innerHTML = '';
  for (let i = 0; i <= ADDR_N; i++) {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'addr-cell' + (i === ADDR_N ? ' addr-past' : '') + (i === addrSel ? ' is-selected' : '');
    b.innerHTML = `<small>${addrHex(ADDR_BASE + i * size)}</small><b>a[${i}]</b>${i === ADDR_N ? '<small>尾端之後</small>' : ''}`;
    b.setAttribute('aria-pressed', String(i === addrSel));
    b.onclick = () => addrPick(i);
    vis.appendChild(b);
  }
  const steps = $('addrSteps');
  if (addrSel < 0) {
    steps.innerHTML = '<div>① 索引 i</div><div>② 位元組偏移 = i × sizeof</div><div>③ 位址 = base + 偏移</div><div>④ 讀寫該位址</div>';
    setStatus('addrStatus', `每格 ${size} bytes，基底位址 0x40（十進位 64）。點任一格，看位址怎麼算。`);
    return;
  }
  const i = addrSel, off = i * size, addr = ADDR_BASE + off;
  const past = i === ADDR_N;
  steps.innerHTML = `<div>① 索引 i = ${i}</div><div>② 位元組偏移 = ${i} × ${size} = ${off}</div>`
    + `<div>③ 位址 = 64 + ${off} = ${addr}（${addrHex(addr)}）</div>`
    + (past ? '<div class="addr-ub">④ 讀寫 a[6]：未定義行為</div>' : `<div>④ 讀取或寫入 a[${i}]</div>`);
  setStatus('addrStatus', past
    ? `a[6] 是尾端之後的位置：可以算出位址 &amp;a[6]（也就是 a + 6），但讀寫 a[6] 是<strong>未定義行為</strong>，結果無法預期，也不一定有錯誤訊息。`
    : `a[${i}] 的位址只需要一次乘法、一次加法；不論 i 是多少，成本都一樣。`);
}
function addrPick(i) { addrSel = i; addrRender(); }
addrRender();

/* ---------- 緊湊陣列與參考式陣列：讀取 a[i] 的步驟 ---------- */
const CMP_VALS = [1, 3, 5, 7, 9, 11];
const CMP_OBJ = [5120, 4800, 6016, 4416, 5504, 4224];   // p[i] 指向的 int 位址（示意）
let cmpPlayer = null;
function cmpFrames(mode, i) {
  const v = CMP_VALS[i];
  if (mode === 'compact') {
    const addr = 1000 + i * 4;
    return [
      {mode, i, stage: 0, msg: `準備讀取 a[${i}]。`},
      {mode, i, stage: 1, msg: `定位槽位：1000 + ${i} × 4 = ${addr}。`},
      {mode, i, stage: 2, msg: `槽位裡就是資料本身：讀到 ${v}。一次定位就完成。`},
    ];
  }
  const slot = 2000 + i * 8, obj = CMP_OBJ[i];
  return [
    {mode, i, stage: 0, msg: `準備讀取 *p[${i}]。`},
    {mode, i, stage: 1, msg: `定位指標槽：2000 + ${i} × 8 = ${slot}。`},
    {mode, i, stage: 2, msg: `槽位裡存的不是值，而是位址 ${obj}。`},
    {mode, i, stage: 3, msg: `沿著指標前往位址 ${obj}，找到目標物件。`},
    {mode, i, stage: 4, msg: `從目標物件讀到 ${v}。比緊湊陣列多了一層間接存取。`},
  ];
}
function cmpApply(f) {
  const W = 96, X0 = 32, hiFill = 'fill:var(--node-current);stroke:var(--node-current);';
  const box = 'fill:var(--card);stroke:var(--accent2);';
  let svg = '';
  if (f.mode === 'compact') {
    svg += '<text x="32" y="22" style="fill:var(--ink);font-size:13px;font-weight:700;">int a[6]：值直接存在格子裡</text>';
    CMP_VALS.forEach((v, k) => {
      const x = X0 + k * W, on = k === f.i && f.stage >= 1;
      svg += `<text x="${x + 44}" y="52" text-anchor="middle" style="fill:var(--muted);font-size:11px;">${1000 + k * 4}</text>`;
      svg += `<rect x="${x}" y="60" width="88" height="46" rx="6" style="${on ? hiFill : box}stroke-width:2;"></rect>`;
      svg += `<text x="${x + 44}" y="90" text-anchor="middle" style="fill:${on ? '#fff' : 'var(--ink)'};font-size:16px;font-weight:700;">${v}</text>`;
      svg += `<text x="${x + 44}" y="126" text-anchor="middle" style="fill:var(--muted);font-size:12px;">a[${k}]</text>`;
    });
    if (f.stage === 2) svg += `<text x="${X0 + f.i * W + 44}" y="152" text-anchor="middle" style="fill:var(--accent);font-size:13px;font-weight:700;">讀到 ${CMP_VALS[f.i]}</text>`;
    $('cmpVis').innerHTML = `<svg viewBox="0 0 640 170" style="max-width:100%;min-width:480px;height:auto;display:block;" role="img" aria-label="緊湊陣列 a 的六個格子">${svg}</svg>`;
    $('cmpBytes').innerHTML = '<div><b>陣列本體</b>6 × 4 = 24 bytes</div><div><b>目標物件</b>無</div>';
  } else {
    svg += '<defs><marker id="arrCmpArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--edge-default);"></path></marker>'
      + '<marker id="arrCmpArrowHi" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--node-current);"></path></marker></defs>';
    svg += '<text x="32" y="22" style="fill:var(--ink);font-size:13px;font-weight:700;">int* p[6]：格子裡存位址</text>';
    const order = CMP_OBJ.map((a, k) => k).sort((a, b) => CMP_OBJ[a] - CMP_OBJ[b]);
    const objX = k => X0 + order.indexOf(k) * W;
    CMP_VALS.forEach((v, k) => {
      const x = X0 + k * W, hiArrow = k === f.i && f.stage >= 3;
      svg += `<line x1="${x + 44}" y1="106" x2="${objX(k) + 44}" y2="176" style="stroke:${hiArrow ? 'var(--node-current)' : 'var(--edge-default)'};stroke-width:${hiArrow ? 3 : 1.5};" marker-end="url(#${hiArrow ? 'arrCmpArrowHi' : 'arrCmpArrow'})"></line>`;
    });
    CMP_VALS.forEach((v, k) => {
      const x = X0 + k * W, on = k === f.i && f.stage >= 1;
      svg += `<text x="${x + 44}" y="52" text-anchor="middle" style="fill:var(--muted);font-size:11px;">${2000 + k * 8}</text>`;
      svg += `<rect x="${x}" y="60" width="88" height="46" rx="6" style="${on ? hiFill : 'fill:#e8edf7;stroke:var(--accent2);'}stroke-width:2;"></rect>`;
      const label = (k === f.i && f.stage >= 2) ? `→${CMP_OBJ[k]}` : '●';
      svg += `<text x="${x + 44}" y="89" text-anchor="middle" style="fill:${on ? '#fff' : 'var(--ink)'};font-size:14px;font-weight:700;">${label}</text>`;
      svg += `<text x="${x + 16}" y="122" text-anchor="middle" style="fill:var(--muted);font-size:11px;">p[${k}]</text>`;
      const ox = objX(k), objOn = k === f.i && f.stage >= 3;
      svg += `<rect x="${ox + 14}" y="178" width="60" height="38" rx="8" style="${objOn ? hiFill : 'fill:var(--card);stroke:var(--node-black);'}stroke-width:1.5;"></rect>`;
      svg += `<text x="${ox + 44}" y="203" text-anchor="middle" style="fill:${objOn ? '#fff' : 'var(--ink)'};font-size:15px;font-weight:700;">${v}</text>`;
      svg += `<text x="${ox + 44}" y="232" text-anchor="middle" style="fill:var(--muted);font-size:11px;">${CMP_OBJ[k]}</text>`;
    });
    if (f.stage === 4) svg += `<text x="${objX(f.i) + 44}" y="252" text-anchor="middle" style="fill:var(--accent);font-size:13px;font-weight:700;">讀到 ${CMP_VALS[f.i]}</text>`;
    $('cmpVis').innerHTML = `<svg viewBox="0 0 640 262" style="max-width:100%;min-width:480px;height:auto;display:block;" role="img" aria-label="指標陣列 p 的六個格子與它們指向的 int 物件">${svg}</svg>`;
    $('cmpBytes').innerHTML = '<div><b>陣列本體</b>6 × 8 = 48 bytes</div><div><b>目標物件</b>6 × 4 = 24 bytes，另外配置</div>';
  }
  setStatus('cmpStatus', f.msg);
}
function cmpNew() {
  if (cmpPlayer) cmpPlayer.pause();
  cmpPlayer = new Player({frames: cmpFrames($('cmpMode').value, parseInt($('cmpIndex').value, 10)), apply: cmpApply, delayInput: $('cmpSpeed')});
  return cmpPlayer;
}
function cmpLoad() {
  if (cmpPlayer) cmpPlayer.pause();
  cmpPlayer = null;
  cmpApply(cmpFrames($('cmpMode').value, parseInt($('cmpIndex').value, 10))[0]);
}
function cmpPlay() { const p = cmpNew(); p.play(); }
function cmpStep() { (cmpPlayer || cmpNew()).step(); }
cmpLoad();

/* ---------- ArrayList：push_back、grow、insert、erase ---------- */
let alPlayer = null;
function alFrames(kind) {
  const frames = [];
  let arr, size, cap = 4, big = null, freed = false, newCap = null;
  const snap = (line, msg, extra = {}) => frames.push(Object.assign({
    arr: arr.slice(), size, cap, big: big ? big.slice() : null, freed, newCap,
    i: null, hi: [], hiBig: [], line, msg}, extra));
  const full = [10, 20, 30, 40], three = [10, 20, 30, null];
  if (kind === 'push' || kind === 'grow') {
    arr = kind === 'push' ? three.slice() : full.slice();
    size = kind === 'push' ? 3 : 4;
    const val = kind === 'push' ? 40 : 50;
    snap(1, `呼叫 push_back(${val})。lastIndex = ${size}、maxSize = ${cap}。`);
    if (size < cap) {
      snap(2, `比較 lastIndex == maxSize：${size} ≠ ${cap}，還有空位，不必 grow。`);
    } else {
      snap(2, `lastIndex == maxSize（${size} == ${cap}）：陣列已滿，先呼叫 grow()。`);
      newCap = cap * 2;
      snap(7, `newCapacity = ${cap} × 2 = ${newCap}。`);
      big = new Array(newCap).fill(null);
      snap(8, `new int[${newCap}] 配置新陣列 bigger。此刻新舊兩個陣列同時存在。`);
      for (let k = 0; k < size; k++) {
        big[k] = arr[k];
        snap(10, `i = ${k}：bigger[${k}] = myArray[${k}]，複製 ${arr[k]}。`, {i: k, hi: [k], hiBig: [k]});
      }
      freed = true;
      snap(11, 'delete[] myArray：釋放舊陣列，之後不能再使用這塊空間。');
      arr = big; big = null; freed = false;
      snap(12, `myArray = bigger：myArray 改指向新陣列。maxSize 還是 ${cap}。`);
      cap = newCap;
      snap(13, `maxSize = newCapacity = ${cap}。grow 結束，回到 push_back。`);
    }
    arr[size] = val;
    snap(3, `寫入 myArray[${size}] = ${val}。lastIndex 還沒更新，這格暫時不算元素。`, {hi: [size]});
    size++;
    snap(4, `lastIndex++ → ${size}，新元素成為有效元素。`, {hi: [size - 1]});
    return frames;
  }
  if (kind === 'insert' || kind === 'insertTail') {
    arr = three.slice(); size = 3;
    const idx = kind === 'insert' ? 1 : 3, val = kind === 'insert' ? 99 : 40;
    snap(15, `呼叫 insert(${idx}, ${val})。lastIndex = ${size}、maxSize = ${cap}。`);
    snap(16, `檢查索引：0 ≤ ${idx} ≤ ${size}，合法（idx 可以等於 lastIndex，表示插在尾端）。`);
    snap(18, `lastIndex == maxSize？${size} ≠ ${cap}，不必 grow。`);
    for (let k = size; k > idx; k--) {
      arr[k] = arr[k - 1];
      snap(20, `i = ${k}：myArray[${k}] = myArray[${k - 1}]，把 ${arr[k]} 複製到右邊一格；現在 ${arr[k]} 暫時出現兩次。`, {i: k, hi: [k - 1, k]});
    }
    snap(19, `i = ${idx}：條件 i > ${idx} 不成立，迴圈結束${idx === size ? '；插在尾端，一個元素都不必搬' : ''}。`, {i: idx});
    arr[idx] = val;
    snap(21, `myArray[${idx}] = ${val}，寫入新值。`, {hi: [idx]});
    size++;
    snap(22, `++lastIndex → ${size}。`, {hi: [idx]});
    return frames;
  }
  arr = full.slice(); size = 4;
  const idx = kind === 'erase' ? 1 : 3;
  snap(24, `呼叫 erase(${idx})。lastIndex = ${size}。`);
  snap(25, `checkIndex(${idx})：0 ≤ ${idx} < ${size}，合法。`, {hi: [idx]});
  for (let k = idx; k < size - 1; k++) {
    arr[k] = arr[k + 1];
    snap(27, `i = ${k}：myArray[${k}] = myArray[${k + 1}]，把 ${arr[k]} 複製到左邊一格。`, {i: k, hi: [k, k + 1]});
  }
  snap(26, `i = ${size - 1}：條件 i < ${size - 1} 不成立，迴圈結束${idx === size - 1 ? '；刪除最後一項不必搬移' : ''}。`, {i: size - 1});
  size--;
  snap(28, `--lastIndex → ${size}。myArray[${size}] 仍存著 ${arr[size]}，但已不在有效區，不算元素；陣列沒有被釋放或清零。`);
  return frames;
}
function alRow(label, cells, f, hi, rowCls) {
  let h = `<div class="al-row ${rowCls || ''}"><div class="al-label">${label}</div><div class="al-cells">`;
  cells.forEach((v, k) => {
    let cls = rowCls === 'al-freed' ? 'al-freedcell' : (rowCls === 'al-big' ? (v == null ? 'al-empty' : 'al-valid')
      : (k < f.size ? 'al-valid' : (v == null ? 'al-empty' : 'al-stale')));
    if (hi.includes(k)) cls += ' al-hi';
    h += `<div class="al-cell ${cls}"><small>${k}</small><b>${v == null ? '·' : v}</b></div>`;
  });
  return h + '</div></div>';
}
function alApply(f) {
  let h = alRow(f.big ? 'myArray（舊）' : 'myArray', f.arr, f, f.hi, f.freed ? 'al-freed' : '');
  if (f.big) h += alRow('bigger', f.big, f, f.hiBig, 'al-big');
  $('alVis').innerHTML = h;
  $('alVars').innerHTML = `<span>lastIndex（size）= <b>${f.size}</b></span><span>maxSize（capacity）= <b>${f.cap}</b></span>`
    + `<span>i = <b>${f.i == null ? '—' : f.i}</b></span>` + (f.newCap != null ? `<span>newCapacity = <b>${f.newCap}</b></span>` : '');
  setStatus('alStatus', f.msg);
  hlLine('alCode', f.line);
}
function alNew() {
  if (alPlayer) alPlayer.pause();
  alPlayer = new Player({frames: alFrames($('alScenario').value), apply: alApply, delayInput: $('alSpeed')});
  return alPlayer;
}
function alLoad() {
  if (alPlayer) alPlayer.pause();
  alPlayer = null;
  alApply(alFrames($('alScenario').value)[0]);
}
function alPlay() { const p = alNew(); p.play(); }
function alStep() { (alPlayer || alNew()).step(); }
alLoad();

/* ---------- 二維陣列：儲存方式與走訪順序分開切換 ---------- */
const MM_R = 3, MM_C = 4;
let mmPlayer = null;
const mmOffset = (store, i, j) => store === 'row' ? i * MM_C + j : j * MM_R + i;
const mmFormula = (store, i, j) => store === 'row'
  ? `offset = i × Cols + j = ${i} × ${MM_C} + ${j} = ${i * MM_C + j}`
  : `offset = j × Rows + i = ${j} × ${MM_R} + ${i} = ${j * MM_R + i}`;
function mmFrames(store, walk) {
  const order = [];
  if (walk === 'row') { for (let i = 0; i < MM_R; i++) for (let j = 0; j < MM_C; j++) order.push([i, j]); }
  else { for (let j = 0; j < MM_C; j++) for (let i = 0; i < MM_R; i++) order.push([i, j]); }
  const frames = [{store, walk, cur: null, visited: [], line: 1, delta: null,
    msg: `開始走訪：${walk === 'row' ? '外層 i、內層 j' : '外層 j、內層 i'}；資料以 ${store === 'row' ? 'row-major' : 'column-major'} 存放。`}];
  const visited = [];
  let prev = null;
  order.forEach(([i, j], t) => {
    const off = mmOffset(store, i, j);
    const delta = prev == null ? null : (off - prev) * 4;
    visited.push(off);
    frames.push({store, walk, cur: [i, j], visited: visited.slice(), line: 3, delta,
      msg: `第 ${t + 1} 次：(i, j) = (${i}, ${j})，offset ${off}，位址 ${1000 + off * 4}。`
        + (delta == null ? '這是第一次讀取。' : `與上一次相差 ${delta > 0 ? '+' : '−'}${Math.abs(delta)} bytes。`)});
    prev = off;
  });
  const jumps = order.slice(1).filter(([i, j], t) => Math.abs(mmOffset(store, i, j) - mmOffset(store, ...order[t])) !== 1).length;
  frames.push({store, walk, cur: null, visited: visited.slice(), line: null, delta: null,
    msg: jumps === 0 ? '走訪結束：每次都前進 4 bytes，正好沿著記憶體順序。'
      : `走訪結束：11 次移動中有 ${jumps} 次不是移到相鄰的下一格。`});
  return frames;
}
function mmApply(f) {
  const grid = $('mmGrid'); grid.innerHTML = '';
  for (let i = 0; i < MM_R; i++) for (let j = 0; j < MM_C; j++) {
    const off = mmOffset(f.store, i, j);
    const b = document.createElement('button');
    b.type = 'button';
    const cur = f.cur && f.cur[0] === i && f.cur[1] === j;
    b.className = 'mapping-cell' + (cur ? ' is-selected' : (f.visited.includes(off) ? ' is-visited' : ''));
    b.innerHTML = `<small>(${i}, ${j})</small><b>${i * MM_C + j + 1}</b>`;
    b.setAttribute('aria-label', `M[${i}][${j}]，值 ${i * MM_C + j + 1}`);
    b.onclick = () => mmPick(i, j);
    grid.appendChild(b);
  }
  const band = $('mmBand'); band.innerHTML = '';
  for (let off = 0; off < MM_R * MM_C; off++) {
    const i = f.store === 'row' ? Math.floor(off / MM_C) : off % MM_R;
    const j = f.store === 'row' ? off % MM_C : Math.floor(off / MM_R);
    const cur = f.cur && mmOffset(f.store, f.cur[0], f.cur[1]) === off;
    const cell = document.createElement('div');
    cell.className = 'memory-cell' + (cur ? ' is-selected' : (f.visited.includes(off) ? ' is-visited' : ''));
    cell.innerHTML = `<small>(${i},${j})</small><b>${i * MM_C + j + 1}</b><small>${off}</small>`;
    band.appendChild(cell);
  }
  const active = band.querySelector('.is-selected');
  if (active) band.parentElement.scrollLeft = active.offsetLeft - band.offsetLeft - (band.parentElement.clientWidth - active.offsetWidth) / 2;
  if (f.cur) {
    const [i, j] = f.cur, off = mmOffset(f.store, i, j);
    $('mmFormula').innerHTML = `${mmFormula(f.store, i, j)}；位址 = 1000 + ${off} × 4 = ${1000 + off * 4}`
      + (f.delta == null ? '' : `；與上一次相差 ${f.delta > 0 ? '+' : '−'}${Math.abs(f.delta)} bytes`)
      + (f.line ? `<br>迴圈變數：i = ${i}、j = ${j}` : '');
  } else {
    $('mmFormula').innerHTML = f.store === 'row' ? 'row-major：offset = i × Cols + j' : 'column-major：offset = j × Rows + i';
  }
  $('mmCodeRow').hidden = f.walk !== 'row';
  $('mmCodeCol').hidden = f.walk !== 'col';
  hlLine(f.walk === 'row' ? 'mmCodeRow' : 'mmCodeCol', f.line);
  setStatus('mmStatus', f.msg);
}
function mmNew() {
  if (mmPlayer) mmPlayer.pause();
  mmPlayer = new Player({frames: mmFrames($('mmStore').value, $('mmWalk').value), apply: mmApply, delayInput: $('mmSpeed')});
  return mmPlayer;
}
function mmConfig() {
  if (mmPlayer) mmPlayer.pause();
  mmPlayer = null;
  mmApply(mmFrames($('mmStore').value, $('mmWalk').value)[0]);
}
function mmPick(i, j) {
  if (mmPlayer) mmPlayer.pause();
  mmPlayer = null;
  const store = $('mmStore').value, walk = $('mmWalk').value, off = mmOffset(store, i, j);
  mmApply({store, walk, cur: [i, j], visited: [], line: null, delta: null,
    msg: `M[${i}][${j}] = ${i * MM_C + j + 1}：${store === 'row' ? 'row-major' : 'column-major'} 下 offset 是 ${off}。另一種排列的 offset 是 ${mmOffset(store === 'row' ? 'col' : 'row', i, j)}。`});
}
function mmPlay() { const p = mmNew(); p.play(); }
function mmStep() { (mmPlayer || mmNew()).step(); }
mmConfig();
new ResizeObserver(() => {
  const band = $('mmBand'), active = band.querySelector('.is-selected');
  if (active) band.parentElement.scrollLeft = active.offsetLeft - band.offsetLeft - (band.parentElement.clientWidth - active.offsetWidth) / 2;
}).observe($('matrixMapping'));

/* ---------- 稀疏矩陣：同一筆資料在三種格式中的位置 ---------- */
const SP_R = 5, SP_C = 6;
const SP_DEFAULT = {'0,1': 3, '1,4': 7, '3,0': 2, '4,5': 5};
let spData = Object.assign({}, SP_DEFAULT), spSel = null;
const spEntries = () => Object.entries(spData).map(([k, v]) => {
  const [r, c] = k.split(',').map(Number); return {r, c, v, key: k};
}).sort((a, b) => a.r - b.r || a.c - b.c);
function spRender() {
  const g = $('spGrid'); g.innerHTML = '';
  for (let r = 0; r < SP_R; r++) for (let c = 0; c < SP_C; c++) {
    const key = r + ',' + c, v = spData[key];
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'sp-cell' + (v !== undefined ? ' sp-nz' : '') + (key === spSel ? ' is-selected' : '');
    b.textContent = v !== undefined ? v : '0';
    b.setAttribute('aria-label', `第 ${r} 列第 ${c} 欄，值 ${v !== undefined ? v : 0}`);
    b.onclick = () => { spSel = key; spRender(); spDescribe(); };
    g.appendChild(b);
  }
  const es = spEntries(), k = es.findIndex(e => e.key === spSel);
  let coo = '<div class="sp-title">COO</div>';
  if (es.length) {
    coo += '<div class="sp-coo-scroll"><table class="sp-coo"><tr><th>k</th>' + es.map((e, t) => `<th class="${t === k ? 'sp-hi' : ''}">${t}</th>`).join('') + '</tr>';
    for (const [name, f] of [['row', e => e.r], ['col', e => e.c], ['val', e => e.v]])
      coo += `<tr><th>${name}</th>` + es.map((e, t) => `<td class="${t === k ? 'sp-hi' : ''}">${arraysEsc(f(e))}</td>`).join('') + '</tr>';
    coo += '</table></div>';
  } else coo += '<div>三條陣列都是空的</div>';
  const dok = '<div class="sp-title">DOK</div><div class="sp-line">{ ' + es.map(e => `<span class="${e.key === spSel ? 'sp-hi' : ''}">(${e.r},${e.c}): ${arraysEsc(e.v)}</span>`).join(', ') + ' }</div>';
  const chain = '<div class="sp-title">線性串列</div><div class="sp-line">head → ' + es.map(e => `<span class="sp-node ${e.key === spSel ? 'sp-hi' : ''}">(${e.r},${e.c},${arraysEsc(e.v)})</span> → `).join('') + 'nullptr</div>';
  $('spStore').innerHTML = coo + dok + chain;
  const nnz = es.length, total = SP_R * SP_C, dens = nnz / total;
  $('spDensity').innerHTML = `NNZ = ${nnz}，總格數 ${total}<br>密度 = ${nnz}／${total} ≈ ${(100 * dens).toFixed(1)}%<br>sparsity = 1 − 密度 ≈ ${(100 * (1 - dens)).toFixed(1)}%<br>密度 &lt; 0.05？<b>${dens < 0.05 ? '是' : '否'}</b>`;
  $('spSel').textContent = spSel ? `選取：(${spSel.replace(',', ', ')})` : '選取：無';
}
function spDescribe(extra) {
  if (!spSel) { setStatus('spStatus', extra || '點一個格子選取它。'); return; }
  const [r, c] = spSel.split(',');
  const k = spEntries().findIndex(e => e.key === spSel);
  const where = k >= 0
    ? `(${r}, ${c}) 存在三種格式中：COO 的第 k = ${k} 欄、DOK 的鍵 (${r},${c})、串列的第 ${k + 1} 個節點。`
    : `(${r}, ${c}) 沒有存任何項目，讀取時視為 0。`;
  setStatus('spStatus', (extra ? extra + ' ' : '') + where);
}
function spWrite() {
  if (!spSel) { setStatus('spStatus', '請先點一個格子。'); return; }
  const v = Number($('spValue').value);
  if (!Number.isFinite(v) || $('spValue').value.trim() === '') { setStatus('spStatus', '請輸入一個數值。'); return; }
  const had = spData[spSel] !== undefined;
  let note;
  if (v === 0) { delete spData[spSel]; note = had ? '寫入 0：刪除這一項，NNZ 減一。' : '寫入 0：本來就沒有這一項，不必儲存。'; }
  else { spData[spSel] = v; note = had ? '改成另一個非零值：只改值，NNZ 不變。' : '新增一個非零項，NNZ 加一。'; }
  spRender(); spDescribe(note);
}
function spReset() { spData = Object.assign({}, SP_DEFAULT); spSel = null; spRender(); spDescribe('已還原展示用的小矩陣。'); }
function spClear() { spData = {}; spSel = null; spRender(); spDescribe('已清空：所有位置都視為 0。'); }
spRender(); spDescribe();
/* /gen:arrays-widgets */
