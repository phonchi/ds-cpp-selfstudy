/* ---------- helpers: linked list DOM ---------- */
/* linked-interactions：第四章所有逐步動畫。每一格 frame 都是完整的顯示快照，
   重播或單步都只是重畫快照，不會再改動任何串列。 */
const LL_C = {ink:'var(--ink)', blue:'var(--accent2)', green:'var(--accent3)', red:'var(--accent)',
  muted:'var(--muted)', orange:'#a84f00', purple:'#7d3c98'};
const LL_PTR = {head:'blue', current:'orange', previous:'purple', temp:'green', newNode:'green',
  x:'green', left:'purple', right:'orange'};
const LL_NODE = {
  '':    ['var(--card)', 'var(--accent2)', 'var(--ink)', 2, ''],
  hl:    ['#fff3cd', '#d68910', 'var(--ink)', 3, ''],
  cmp:   ['#f4ecf7', '#7d3c98', 'var(--ink)', 3, ''],
  found: ['#d5f5e3', 'var(--accent3)', 'var(--ink)', 3, ''],
  new:   ['#e9f7ef', 'var(--accent3)', 'var(--ink)', 2.5, ''],
  del:   ['none', 'var(--accent)', 'var(--muted)', 2, '5 4'],
  lost:  ['var(--card)', 'var(--muted)', 'var(--muted)', 1.5, '4 3'],
  skip:  ['var(--card)', 'var(--node-gray)', 'var(--muted)', 1.5, ''],
  sent:  ['#eceff1', 'var(--muted)', 'var(--ink)', 2, ''],
};
const llClone = o => JSON.parse(JSON.stringify(o));
const llEsc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/* st = {nodes:[{id,v,col,row,cls,addr,tag}], next:{id:id|null}, prev:{id:id|null}, ptr:{name:id|null},
         es:{id:style}, ps:{id:style}, vars:[[k,v]], dbl, wide, lbl:'above'|'below', arr} */
function llDraw(cid, st) {
  const el = $(cid); if (!el) return;
  const dbl = !!st.dbl, wide = !!st.wide;
  const W = dbl ? 92 : (wide ? 88 : 66), H = 36, P = W + (wide ? 34 : 48);
  const NF = dbl ? 20 : (wide ? 38 : 22);
  const nodes = st.nodes || [], by = {};
  nodes.forEach(n => { by[n.id] = n; });
  const hasHead = st.ptr && Object.prototype.hasOwnProperty.call(st.ptr, 'head');
  const X0 = hasHead ? 100 : 24;
  const above = st.lbl === 'above';
  const labels = {};
  Object.entries(st.ptr || {}).forEach(([name, to]) => {
    if (name !== 'head' && to && by[to]) (labels[to] = labels[to] || []).push(name);
  });
  const stack = n => (labels[n.id] || []).length + (n.tag ? 1 : 0);
  const rowNodes = r => nodes.filter(n => (n.row || 0) === r);
  const lblH = r => { const m = Math.max(0, ...rowNodes(r).map(stack)); return m ? m * 16 + 12 : 0; };
  // 先判斷哪些鏈結需要從上方或下方繞過去
  const edges = [];
  const addEdges = (map, kind, sty) => Object.entries(map || {}).forEach(([a, b]) => {
    if (!by[a] || by[a].cls === 'del' || b === undefined) return;
    edges.push({a, b, kind, sty: (sty || {})[a] || ''});
  });
  addEdges(st.next, 'next', st.es);
  if (dbl) addEdges(st.prev, 'prev', st.ps);
  const route = e => {
    const A = by[e.a], B = e.b && by[e.b];
    if (!B) return 'null';
    if ((A.row || 0) !== (B.row || 0)) return 'diag';
    if (e.a === e.b) return 'self';
    const d = B.col - A.col;
    if (e.kind === 'next') return d > 0 && d <= 1.01 ? 'straight' : (d > 0 ? 'over' : 'under');
    return d < 0 && d >= -1.01 ? 'straight' : 'under';
  };
  edges.forEach(e => { e.r = route(e); });
  const rows = [...new Set(nodes.map(n => n.row || 0))];
  const anyOver = r => edges.some(e => (e.r === 'over' || (e.r === 'self' && !above)) && (by[e.a].row || 0) === r);
  const anyUnder = r => edges.some(e => (e.r === 'under' || (e.r === 'self' && above)) && (by[e.a].row || 0) === r);
  const anyAddr = nodes.some(n => n.addr) || (st.arr && true);
  const nullHead = hasHead && st.ptr.head === null;
  const y = {}; let cur = 14 + (anyAddr ? 16 : 0);
  const maxRow = Math.max(0, ...rows);
  const geo = {};
  for (let r = 0; r <= maxRow; r++) {
    const top = (above ? lblH(r) : 0), over = anyOver(r) ? 30 + top : 0;
    cur += Math.max(top, over);
    y[r] = cur; geo[r] = {top, over};
    const below = (above ? 0 : lblH(r)), under = anyUnder(r) ? 34 + below : 0;
    cur += H + Math.max(below, under, r === 0 && nullHead ? 46 : 0) + 18;
    geo[r].below = below;
  }
  if (st.arr) { y[0] = y[0] || cur; }
  const maxCol = Math.max(0, ...nodes.map(n => n.col + (n.next === null ? 0 : 0)));
  const hasNullRight = edges.some(e => e.r === 'null' && e.kind === 'next');
  let width = X0 + (maxCol + 1) * P + (hasNullRight ? 20 : 0) + 6;
  if (st.arr) width = Math.max(width, 40 + st.arr.vals.length * 66 + 40);
  const height = Math.max(cur, 90);
  const X = n => X0 + n.col * P, Y = n => y[n.row || 0];
  const out = [];
  const colors = ['ink', 'blue', 'green', 'red', 'muted', 'orange', 'purple'];
  const mk = c => `${cid}-m-${c}`;
  out.push(`<svg viewBox="0 0 ${width} ${height}" width="${width}" height="${height}" role="img" aria-label="鏈結串列示意圖" style="width:${width}px;max-width:max(100%, ${Math.round(width * 0.68)}px);height:auto;font-family:'JetBrains Mono',monospace;"><defs>`);
  colors.forEach(c => out.push(`<marker id="${mk(c)}" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" style="fill:${LL_C[c]}"/></marker>`));
  out.push('</defs>');
  const line = (d, c, w, dash) => out.push(`<path d="${d}" style="fill:none;stroke:${LL_C[c]};stroke-width:${w};${dash ? 'stroke-dasharray:' + dash + ';' : ''}" marker-end="url(#${mk(c)})"/>`);
  const text = (x, yy, s, c, size, anchor, weight) => out.push(`<text x="${x}" y="${yy}" text-anchor="${anchor || 'middle'}" style="fill:${LL_C[c] || c};font-size:${size || 13}px;font-weight:${weight || 600};">${llEsc(s)}</text>`);
  // 陣列（連續格子）
  if (st.arr) {
    const a = st.arr, yy = y[0];
    a.vals.forEach((v, i) => {
      const x = 40 + i * 66, on = a.sel === i, done = a.read === i;
      out.push(`<rect x="${x}" y="${yy}" width="66" height="${H}" style="fill:${on ? '#fff3cd' : 'var(--card)'};stroke:${on ? '#d68910' : 'var(--accent2)'};stroke-width:${on ? 3 : 1.6};"/>`);
      text(x + 33, yy + 23, v, done ? 'green' : 'ink', 15, 'middle', 700);
      text(x + 33, yy - 8, a.base + 4 * i, 'muted', 11, 'middle', 500);
      text(x + 33, yy + H + 16, `a[${i}]`, on ? 'orange' : 'muted', 11, 'middle', 600);
    });
  }
  // 窄螢幕時畫面可左右捲動；讓正在處理的節點保持在可見範圍
  const focus = nodes.find(n => ['hl', 'cmp', 'found', 'del', 'new'].includes(n.cls));
  const focusX = focus ? X(focus) + W / 2 : null;
  // 節點
  nodes.forEach(n => {
    const [fill, stroke, ink, sw, dash] = LL_NODE[n.cls || ''] || LL_NODE[''];
    const x = X(n), yy = Y(n);
    out.push(`<rect x="${x}" y="${yy}" width="${W}" height="${H}" rx="6" style="fill:${fill};stroke:${stroke};stroke-width:${sw};${dash ? 'stroke-dasharray:' + dash + ';' : ''}"/>`);
    const divider = xx => out.push(`<line x1="${xx}" y1="${yy}" x2="${xx}" y2="${yy + H}" style="stroke:${stroke};stroke-width:1.2;${dash ? 'stroke-dasharray:' + dash + ';' : ''}"/>`);
    divider(x + W - NF);
    if (dbl) divider(x + NF);
    const cx = dbl ? x + W / 2 : x + (W - NF) / 2;
    const sent = n.cls === 'sent';
    text(cx, yy + (sent ? 22 : 24), n.v, ink, sent ? 11 : 15, 'middle', sent ? 600 : 700);
    if (n.cls === 'del') out.push(`<line x1="${x + 6}" y1="${yy + 6}" x2="${x + W - 6}" y2="${yy + H - 6}" style="stroke:var(--accent);stroke-width:1.5;"/>`);
    if (n.addr) text(x + W / 2, yy - 7, '位址 ' + n.addr, 'muted', 11, 'middle', 500);
    if (n.nextTxt != null) text(x + W - NF / 2, yy + 22, n.nextTxt, 'muted', 10, 'middle', 600);
  });
  // 鏈結
  edges.forEach(e => {
    const A = by[e.a], B = e.b ? by[e.b] : null, ax = X(A), ay = Y(A), acy = ay + H / 2;
    const c = e.sty === 'new' ? 'green' : e.sty === 'bad' ? 'red' : A.cls === 'lost' ? 'muted' : 'ink';
    const w = e.sty ? 2.6 : 1.8, dash = A.cls === 'lost' ? '5 4' : '';
    const isNext = e.kind === 'next';
    const txt = A.nextTxt != null;
    const sx = isNext ? (txt ? ax + W : ax + W - NF / 2) : ax + NF / 2;
    const sy = dbl ? acy + (isNext ? -7 : 7) : acy;
    if (!txt) out.push(`<circle cx="${sx}" cy="${sy}" r="3" style="fill:${LL_C[c]};"/>`);
    if (e.r === 'null') {
      if (!isNext) return;
      line(`M${sx} ${sy}L${ax + W + 12} ${sy}`, c, w, dash);
      text(ax + W + 14, sy + 4, 'NULL', c === 'ink' ? 'muted' : c, 11, 'start', 700);
      return;
    }
    const bx = X(B), by_ = Y(B), bcy = by_ + H / 2;
    const g = geo[A.row || 0];
    if (e.r === 'straight') {
      const ty = dbl ? bcy + (isNext ? -7 : 7) : bcy;
      line(`M${sx} ${sy}L${isNext ? bx - 1 : bx + W + 1} ${ty}`, c, w, dash);
    } else if (e.r === 'over') {
      const h = (g.over || 30) / 0.75, tx = bx + 14;
      line(`M${sx} ${sy}L${sx} ${ay}C${sx} ${ay - h} ${tx} ${by_ - h} ${tx} ${by_ - 1}`, c, w, dash);
    } else if (e.r === 'under') {
      const h = (34 + (above ? 0 : g.below)) / 0.75, tx = isNext ? bx + 14 : bx + W - 14;
      line(`M${sx} ${sy}L${sx} ${ay + H}C${sx} ${ay + H + h} ${tx} ${by_ + H + h} ${tx} ${by_ + H + 1}`, c, w, dash);
    } else if (e.r === 'self') {
      if (above) line(`M${sx} ${sy}L${sx} ${ay + H}C${sx} ${ay + H + 44} ${ax + 12} ${ay + H + 44} ${ax + 12} ${ay + H + 1}`, c, w, dash);
      else line(`M${sx} ${sy}C${ax + W + 40} ${sy} ${ax + W + 40} ${ay - 30} ${ax + W / 2} ${ay - 30}C${ax + 12} ${ay - 30} ${ax + 12} ${ay - 20} ${ax + 12} ${ay - 1}`, c, w, dash);
    } else {
      // 跨列：先水平離開欄位，再彎進目標的上緣或下緣；next 向右、prev 向左，兩種鏈結不會重疊
      const down = (B.row || 0) > (A.row || 0);
      if (B.addr) { line(`M${sx} ${sy}C${sx + 36} ${sy} ${bx - 36} ${bcy} ${bx - 1} ${bcy}`, c, w, dash); return; }
      const tx = bx + W * (isNext ? 0.3 : 0.7), ty = down ? by_ - 1 : by_ + H + 1;
      const hx = isNext ? sx + 36 : sx - 36, vy = down ? ty - 36 : ty + 36;
      line(`M${sx} ${sy}C${hx} ${sy} ${tx} ${vy} ${tx} ${ty}`, c, w, dash);
    }
  });
  // head 方框
  if (hasHead) {
    const hy = y[0], hcy = hy + H / 2, to = st.ptr.head;
    out.push(`<rect x="10" y="${hy + 4}" width="56" height="${H - 8}" rx="5" style="fill:#eef2ff;stroke:var(--accent2);stroke-width:1.6;"/>`);
    text(38, hcy + 5, 'head', 'blue', 13, 'middle', 700);
    const T = to && by[to];
    const hs = st.es && st.es.head, hc = hs === 'new' ? 'green' : (hs === 'bad' || (T && T.cls === 'del')) ? 'red' : 'blue';
    if (!to) {
      line(`M38 ${hy + H - 4}L38 ${hy + H + 18}`, 'blue', 1.8);
      text(38, hy + H + 33, 'NULL', 'muted', 11, 'middle', 700);
    } else if (T) {
      const tx = X(T), ty = Y(T);
      if ((T.row || 0) === 0) line(`M66 ${hcy}L${tx - 1} ${hcy}`, hc, hc === 'green' ? 2.6 : 1.8, hc === 'red' ? '5 4' : '');
      else line(`M66 ${hcy}L${tx + 14} ${ty - 1}`, hc, hc === 'green' ? 2.6 : 1.8, hc === 'red' ? '5 4' : '');
    }
  }
  // 指標標籤與標記
  nodes.forEach(n => {
    const names = labels[n.id] || [], items = names.map(nm => [nm, n.cls === 'del']);
    if (!items.length && !n.tag) return;
    const x = X(n), yy = Y(n), cx = x + W / 2;
    const up = above && (n.row || 0) === 0;
    const base = up ? yy - 12 : yy + H + 22;
    items.forEach(([nm, dead], k) => {
      const c = dead ? 'red' : (LL_PTR[nm] || 'ink');
      const ty = up ? base - 16 * k : base + 16 * k;
      text(cx, ty, dead ? nm + '（失效）' : nm, c, 12, 'middle', 700);
    });
    if (items.length) {
      const c0 = items[0][1] ? 'red' : (LL_PTR[items[0][0]] || 'ink');
      if (up) line(`M${cx} ${yy - 9}L${cx} ${yy - 1}`, c0, 1.6, items[0][1] ? '3 2' : '');
      else line(`M${cx} ${yy + H + 10}L${cx} ${yy + H + 1}`, c0, 1.6, items[0][1] ? '3 2' : '');
    }
    if (n.tag) {
      const k = items.length, ty = up ? base - 16 * k : base + 16 * k;
      text(cx, ty, n.tag, n.cls === 'del' ? 'red' : 'muted', 11, 'middle', 600);
    }
  });
  out.push('</svg>');
  const vars = [];
  Object.entries(st.ptr || {}).forEach(([k, to]) => {
    if (st.hideVars && st.hideVars.includes(k)) return;
    const T = to && by[to];
    vars.push([k, to === null ? 'NULL' : !T ? '—' : T.cls === 'del' ? '已釋放的節點（失效）' : (T.cls === 'sent' ? T.v : '節點 ' + T.v)]);
  });
  const nPtr = vars.length;
  (st.vars || []).forEach(v => vars.push(v));
  const isId = k => /^[A-Za-z_][A-Za-z_0-9]*$/.test(k);
  const old = el.querySelector('.ll-scroll'), keep = old ? old.scrollLeft : 0;
  el.innerHTML = '<div class="ll-scroll">' + out.join('') + '</div>' + (vars.length ? '<div class="ll-vars">' + vars.map(([k, v], i) =>
    `<span>${isId(k) ? '<code>' + llEsc(k) + '</code>' : llEsc(k)}${i < nPtr ? ' → ' : isId(k) ? ' = ' : '：'}${llEsc(v)}</span>`).join('') + '</div>' : '');
  const sc = el.querySelector('.ll-scroll'), svg = sc.querySelector('svg');
  sc.scrollLeft = keep;
  if (sc.scrollWidth > sc.clientWidth + 1 && focusX != null) {
    const scale = svg.getBoundingClientRect().width / width;
    sc.scrollLeft = Math.max(0, focusX * scale - sc.clientWidth / 2);
  }
}

/* ---------- 播放器接線（player-v2） ---------- */
const LLP = {}, LLB = {};
function llRun(p, frames) {
  if (LLP[p]) LLP[p].stop();
  const cnt = $(p + 'Count');
  const player = new Player({frames, delayInput: $(p + 'Speed'), apply: f => {
    llDraw(p + 'Vis', f.st);
    document.querySelectorAll(`[data-ll-code="${p}"]`).forEach(c => { c.hidden = +c.dataset.idx !== (f.code || 0); });
    hlLine(p + 'Code' + (f.code || 0), f.line);
    setStatus(p + 'Status', String(f.msg).replace(/</g, '&lt;'));
    if (cnt) cnt.textContent = `第 ${frames.indexOf(f)} / ${frames.length - 1} 步`;
  }});
  LLP[p] = player;
  const tg = $(p + 'Toggle'); if (tg) tg.textContent = '⏸ 暫停';
  player._btn = tg;   // player-v2 依播放狀態同步 ⏸／▶ 繼續 的文字
  player.reset();
  player.i = 0;   // 第 0 格已顯示，下一次「單步」直接到第 1 格
}
function llCase(p, k, btn) {
  document.querySelectorAll(`.ll-case[data-ll="${p}"]`).forEach(b => b.classList.toggle('on', b === btn));
  llRun(p, LLB[p](k));
}
function llPlay(p) {
  const pl = LLP[p]; if (!pl) return;
  if (pl._done || pl.i >= pl.frames.length - 1) { pl.i = -1; pl._done = false; }
  pl.play();
  const tg = $(p + 'Toggle'); if (tg) tg.textContent = '⏸ 暫停';
}
function llStep(p) { const pl = LLP[p]; if (pl) pl.step(); }
function llToggle(p, btn) { const pl = LLP[p]; if (pl) pl.toggle(btn); }

/* ---------- 狀態工具 ---------- */
function llList(vals, col0 = 0, pre = 'n') {
  const st = {nodes: [], next: {}, ptr: {head: vals.length ? pre + '0' : null}, es: {}, vars: []};
  vals.forEach((v, i) => {
    st.nodes.push({id: pre + i, v, col: col0 + i, row: 0, cls: ''});
    st.next[pre + i] = i + 1 < vals.length ? pre + (i + 1) : null;
  });
  return st;
}
function llSnap(frames, st, line, msg, hl = {}, extra = {}) {
  const s = llClone(st);
  s.nodes.forEach(n => { if (hl[n.id]) n.cls = hl[n.id]; });
  frames.push(Object.assign({st: s, line, msg}, extra));
}
const llN = (st, id) => st.nodes.find(n => n.id === id);
function llChain(st) {
  const ids = []; let c = st.ptr.head, guard = 0;
  while (c && guard++ < 50) { ids.push(c); c = st.next[c]; if (c === st.ptr.head) break; }
  return ids;
}
function llRelayout(st, keep = []) {
  const ids = llChain(st);
  st.nodes = ids.map((id, i) => Object.assign(llN(st, id), {col: i, row: 0, cls: '', tag: ''}));
  Object.keys(st.next).forEach(k => { if (!ids.includes(k)) delete st.next[k]; });
  Object.keys(st.ptr).forEach(k => { if (k !== 'head' && !keep.includes(k)) delete st.ptr[k]; });
  st.es = {}; st.vars = [];
  return ids.map(id => llN(st, id).v);
}
const llVals = st => llChain(st).map(id => llN(st, id).v).join(' → ') || '（空串列）';

/* ---------- P00 陣列與鏈結：讀第 k 項 ---------- */
LLB.mem = k => {
  const vals = [93, 77, 31, 17, 26], addrs = [7080, 2046, 5340, 3012, 6104];
  const idx = Math.max(0, Math.min(4, parseInt(($('memK') || {}).value || '3', 10) || 0));
  const frames = [];
  if (k === 'array') {
    const st = {arr: {vals, base: 1000, sel: -1, read: -1}, nodes: [], vars: [['起點位址', '1000'], ['每格大小', '4 bytes']]};
    llSnap(frames, st, null, `陣列的元素連續存放：起點位址 1000，每個 int 佔 4 bytes。要讀 a[${idx}]。`);
    st.arr.sel = idx; st.vars.push(['a[' + idx + '] 的位址', `1000 + ${idx} × 4 = ${1000 + 4 * idx}`]);
    llSnap(frames, st, null, `用公式一次算出位址：1000 + ${idx} × 4 = ${1000 + 4 * idx}，不必經過前面的格子。`);
    st.arr.read = idx; st.vars.push(['讀到的值', String(vals[idx])]);
    llSnap(frames, st, null, `直接讀出 a[${idx}] = ${vals[idx]}。不論 ${idx} 是多少，都只要一次計算。`);
    return frames;
  }
  const st = llList(vals); st.wide = true;
  st.nodes.forEach((n, i) => { n.addr = addrs[i]; n.row = i % 2; n.col = i; n.nextTxt = i < 4 ? addrs[i + 1] : '—'; });
  st.next.n4 = null; st.ptr.current = 'n0'; st.vars = [['已前進', '0 次']];
  llSnap(frames, st, null, `節點分散在記憶體各處，每個節點的 next 存下一個節點的位址。current = head，從第 0 項開始。`, {n0: 'hl'});
  for (let i = 1; i <= idx; i++) {
    st.ptr.current = 'n' + i; st.vars = [['已前進', i + ' 次']];
    llSnap(frames, st, null, `current = current->getNext()：依 next 存的位址 ${addrs[i]}，走到下一個節點。`, {['n' + i]: 'hl'});
  }
  st.vars.push(['讀到的值', String(vals[idx])]);
  llSnap(frames, st, null, `走到第 ${idx} 項後讀出 current->getData() = ${vals[idx]}。共前進 ${idx} 次；要讀的項越後面，走的步數越多。`, {['n' + idx]: 'found'});
  return frames;
};

/* ---------- P01 Node：配置、讀取、釋放 ---------- */
LLB.node = () => {
  const frames = [];
  const st = {nodes: [{id: 'a', v: 93, col: 0, row: 0, cls: 'new'}], next: {a: null}, ptr: {temp: 'a'}, vars: []};
  llSnap(frames, st, 1, 'new Node<int>(93) 在 heap 配置一個節點；建構子把 data 設為 93、next 設為 NULL。temp 存放這個節點的位址。');
  st.nodes[0].cls = ''; st.vars = [['輸出', '93']];
  llSnap(frames, st, 2, 'temp->getData() 透過指標呼叫方法，取得 data，輸出 93。', {a: 'hl'});
  st.vars = [['輸出', '93　0']];
  llSnap(frames, st, 3, 'temp->getNext() 回傳 next 欄位的值，也就是 NULL；用 cout 印出空指標時顯示 0。', {a: 'hl'});
  st.nodes[0].cls = 'del'; st.nodes[0].tag = '已釋放'; st.next = {};
  llSnap(frames, st, 4, 'delete temp 釋放節點。temp 仍保存舊位址，但那塊記憶體已歸還，temp 成為失效指標，不能再透過它讀寫。');
  return frames;
};

/* ---------- P02 UnorderedList：add ---------- */
LLB.uAdd = k => {
  const frames = [];
  const vals = k === 'empty' ? [] : [93, 17, 77, 31];
  const st = llList(vals, 1);
  st.nodes.push({id: 't', v: 26, col: 0, row: 1, cls: 'new'}); st.next.t = null; st.ptr.temp = 't';
  if (k === 'wrong') {
    llSnap(frames, st, 2, 'new Node<T>(26) 配置新節點，temp 指向它；新節點的 next 是 NULL。', {}, {code: 1});
    st.ptr.head = 't'; st.es.head = 'new';
    st.nodes.forEach(n => { if (n.id !== 't') n.cls = 'lost'; });
    st.nodes[0].tag = '沒有指標指向這裡';
    llSnap(frames, st, 3, '先執行 head = temp：head 改指新節點。原本的 93 → 17 → 77 → 31 還在記憶體中，但已經沒有任何指標指向 93，再也走不到。', {}, {code: 1});
    st.next.t = 't'; st.es.t = 'bad';
    llSnap(frames, st, 4, 'temp->setNext(head)：此時 head 就是 temp，新節點的 next 指向自己。從 head 走訪會一直停在 26；原本四個節點遺失，也無法再 delete。', {}, {code: 1});
    return frames;
  }
  llSnap(frames, st, 2, 'new Node<T>(26) 配置新節點，temp 指向它；建構子把它的 next 設為 NULL。');
  st.next.t = st.ptr.head; st.es.t = 'new';
  llSnap(frames, st, 3, vals.length
    ? '第 1 步 temp->setNext(head)：新節點的 next 接到原本的第一個節點 93。現在 head 與新節點都指向 93，後段不會遺失。'
    : '第 1 步 temp->setNext(head)：head 是 NULL，所以新節點的 next 仍是 NULL。');
  st.ptr.head = 't'; st.es.head = 'new'; st.es.t = '';
  llSnap(frames, st, 4, '第 2 步 head = temp：head 改指新節點，26 成為第一個節點；其餘節點都不用搬動。');
  llRelayout(st);
  llSnap(frames, st, 5, `add 結束：${llVals(st)}。區域變數 temp 隨函式結束而消失，節點仍由串列保管。`);
  return frames;
};

/* ---------- P02 UnorderedList：size ---------- */
LLB.uSize = k => {
  const frames = [];
  const st = llList(k === 'empty' ? [] : [93, 17, 77, 31]);
  const ids = llChain(st);
  st.ptr.current = st.ptr.head; st.vars = [['count', '尚未宣告']];
  llSnap(frames, st, 2, ids.length ? 'current = head：current 與 head 指向同一個節點。之後只移動 current，head 不動。' : 'current = head：串列是空的，current 一開始就是 NULL。', ids.length ? {[ids[0]]: 'hl'} : {});
  let count = 0; st.vars = [['count', '0']];
  llSnap(frames, st, 3, 'count = 0：還沒有數到任何節點。', ids.length ? {[ids[0]]: 'hl'} : {});
  ids.forEach((id, i) => {
    llSnap(frames, st, 4, `current 不是 NULL（指向 ${llN(st, id).v}），進入迴圈。`, {[id]: 'hl'});
    count++; st.vars = [['count', String(count)]];
    llSnap(frames, st, 5, `count++：數到第 ${count} 個節點。`, {[id]: 'hl'});
    st.ptr.current = st.next[id];
    llSnap(frames, st, 6, st.next[id] ? `current = current->getNext()：移到下一個節點 ${llN(st, st.next[id]).v}。` : 'current = current->getNext()：最後一個節點的 next 是 NULL，current 變成 NULL。', st.next[id] ? {[st.next[id]]: 'hl'} : {});
  });
  llSnap(frames, st, 4, 'current == NULL，迴圈結束。');
  llSnap(frames, st, 8, count ? `return count：回傳 ${count}。整個過程 head 都沒有移動，每個節點各數一次，所以是 O(n)。` : 'return count：回傳 0。head 是 NULL，迴圈一次都沒有執行。');
  return frames;
};

/* ---------- P02 UnorderedList：search ---------- */
LLB.uSearch = k => {
  const frames = [], item = k === 'miss' ? 45 : 17;
  const st = llList([54, 26, 93, 17, 77, 31]), ids = llChain(st);
  st.ptr.current = 'n0'; st.vars = [['item', String(item)]];
  llSnap(frames, st, 2, `search(${item})：current = head，從第一個節點 54 開始。`, {n0: 'hl'});
  for (const id of ids) {
    const v = llN(st, id).v;
    llSnap(frames, st, 3, `current 不是 NULL，繼續檢查。`, {[id]: 'hl'});
    if (v === item) {
      llSnap(frames, st, 4, `current->getData() 是 ${v}，等於 ${item}。`, {[id]: 'found'});
      llSnap(frames, st, 5, `return true：找到就立刻回傳，後面的節點不必再看。`, {[id]: 'found'});
      return frames;
    }
    llSnap(frames, st, 4, `current->getData() 是 ${v}，不等於 ${item}。`, {[id]: 'cmp'});
    st.ptr.current = st.next[id];
    llSnap(frames, st, 7, st.next[id] ? `current = current->getNext()：前進到 ${llN(st, st.next[id]).v}。` : 'current = current->getNext()：current 變成 NULL。', st.next[id] ? {[st.next[id]]: 'hl'} : {});
  }
  llSnap(frames, st, 3, 'current == NULL：走到串列尾端，迴圈結束。');
  llSnap(frames, st, 9, `return false：每個節點都比對過，${item} 不在串列中。`);
  return frames;
};

/* ---------- P02 UnorderedList：remove（講義 found 版） ---------- */
LLB.uRemove = k => {
  const frames = [];
  const vals = k === 'only' ? [7] : [54, 26, 93, 17, 77, 31];
  const item = {mid: 17, head: 54, tail: 31, only: 7, miss: 45}[k];
  const st = llList(vals), ids = llChain(st);
  st.ptr.current = st.ptr.head; st.ptr.previous = null; st.vars = [['found', 'false'], ['item', String(item)]];
  llSnap(frames, st, 2, `remove(${item})：current = head，previous = NULL，found = false。`, {[ids[0]]: 'hl'});
  let hit = null;
  for (const id of ids) {
    const v = llN(st, id).v;
    if (v === item) {
      st.vars[0] = ['found', 'true'];
      llSnap(frames, st, 8, `current->getData() 是 ${v}，等於 ${item}：found = true，迴圈條件 !found 不再成立。`, {[id]: 'found'});
      hit = id; break;
    }
    llSnap(frames, st, 7, `current->getData() 是 ${v}，不等於 ${item}。`, {[id]: 'cmp'});
    st.ptr.previous = id;
    llSnap(frames, st, 10, `previous = current：previous 先移到 ${v}。此刻兩個指標暫時指向同一個節點。`, {[id]: 'hl'});
    st.ptr.current = st.next[id];
    llSnap(frames, st, 11, st.next[id] ? `current = current->getNext()：current 再前進到 ${llN(st, st.next[id]).v}，previous 留在它的前一個節點。` : 'current = current->getNext()：current 變成 NULL。', st.next[id] ? {[st.next[id]]: 'hl'} : {});
  }
  if (!hit) {
    llSnap(frames, st, 6, 'current == NULL，迴圈結束；found 仍是 false。');
    llSnap(frames, st, 15, `if (found) 不成立：找不到 ${item}，不改任何鏈結，也不 delete。串列維持原樣。`);
    return frames;
  }
  const prev = st.ptr.previous, after = st.next[hit];
  const afterTxt = after ? llN(st, after).v : 'NULL';
  llSnap(frames, st, 16, prev ? `previous 不是 NULL：要刪的不是第一個節點，改的是前驅 ${llN(st, prev).v} 的 next。` : 'previous == NULL：要刪的是第一個節點，所以改的是 head。', {[hit]: 'found'});
  if (!prev) {
    st.ptr.head = after; st.es.head = 'new';
    llSnap(frames, st, 17, `head = current->getNext()：head 改指 ${afterTxt}。節點 ${item} 已經脫離串列，但記憶體還沒釋放。`, {[hit]: 'found'});
  } else {
    st.next[prev] = after; st.es[prev] = 'new';
    llSnap(frames, st, 19, `previous->setNext(current->getNext())：${llN(st, prev).v} 的 next 改指 ${afterTxt}，${item} 被跳過；節點本身還在，current 仍指著它。`, {[hit]: 'found'});
  }
  const n = llN(st, hit); n.cls = 'del'; n.tag = '已釋放';
  llSnap(frames, st, 21, `delete current：釋放 ${item} 的節點。current 現在是失效指標，不能再讀它的欄位。`);
  llRelayout(st);
  llSnap(frames, st, 23, `remove 結束：${llVals(st)}。`);
  return frames;
};

/* ---------- P03 OrderedList：search（提早停止） ---------- */
LLB.oSearch = k => {
  const frames = [], item = {stop: 45, hit: 31, miss: 100}[k];
  const st = llList([17, 26, 31, 54, 77, 93]), ids = llChain(st);
  st.ptr.current = 'n0'; st.vars = [['item', String(item)]];
  llSnap(frames, st, 2, `search(${item})：current = head。`, {n0: 'hl'});
  for (const id of ids) {
    const v = llN(st, id).v;
    if (v === item) {
      llSnap(frames, st, 4, `current 不是 NULL；${v} 等於 ${item}。`, {[id]: 'found'});
      llSnap(frames, st, 5, 'return true：找到了。', {[id]: 'found'});
      return frames;
    }
    llSnap(frames, st, 4, `current 不是 NULL；${v} 不等於 ${item}。`, {[id]: 'cmp'});
    if (v > item) {
      llSnap(frames, st, 6, `${v} 大於 ${item}：串列由小到大排列，後面的值只會更大。`, {[id]: 'cmp'});
      ids.slice(ids.indexOf(id) + 1).forEach(r => { const n = llN(st, r); n.cls = 'skip'; n.tag = '未走訪'; });
      llSnap(frames, st, 7, `return false：在 ${v} 就停止，後面的節點不必再走訪。`, {[id]: 'cmp'});
      return frames;
    }
    llSnap(frames, st, 6, `${v} 小於 ${item}，目標可能在後面。`, {[id]: 'cmp'});
    st.ptr.current = st.next[id];
    llSnap(frames, st, 9, st.next[id] ? `current = current->getNext()：前進到 ${llN(st, st.next[id]).v}。` : 'current = current->getNext()：current 變成 NULL。', st.next[id] ? {[st.next[id]]: 'hl'} : {});
  }
  llSnap(frames, st, 3, 'current == NULL，迴圈結束。');
  llSnap(frames, st, 11, `return false：${item} 比所有元素都大，必須走完整條串列才能確定。`);
  return frames;
};

/* ---------- P03 OrderedList：add（講義 lookahead 版） ---------- */
LLB.oAdd = k => {
  const frames = [];
  const base = k === 'empty' ? [] : [17, 26, 54, 77, 93];
  const item = {mid: 31, head: 10, tail: 100, empty: 31}[k];
  const headCase = k === 'head' || k === 'empty';
  const st = llList(base, headCase ? 1 : 0);
  const pos = base.filter(v => v < item).length;
  st.nodes.push({id: 'nn', v: item, col: headCase ? 0 : (pos >= base.length ? base.length : pos - 0.5), row: 1, cls: 'new'});
  st.next.nn = null; st.ptr.newNode = 'nn'; st.vars = [['item', String(item)]];
  llSnap(frames, st, 2, `add(${item})：先配置新節點，newNode 指向它。`);
  if (headCase) {
    llSnap(frames, st, 3, base.length ? `head 的值 ${base[0]} >= ${item} 成立：新值應放在最前面。` : 'head == NULL 成立：串列是空的，新節點直接成為第一個節點。', base.length ? {n0: 'cmp'} : {});
    st.next.nn = st.ptr.head; if (st.ptr.head) st.es.nn = 'new';
    llSnap(frames, st, 4, base.length ? `newNode->setNext(head)：新節點先接住原本的第一個節點 ${base[0]}。` : 'newNode->setNext(head)：head 是 NULL，新節點的 next 仍是 NULL。');
    st.ptr.head = 'nn'; st.es.head = 'new'; st.es.nn = '';
    llSnap(frames, st, 5, 'head = newNode：head 改指新節點。');
    llRelayout(st);
    llSnap(frames, st, 14, `add 結束：${llVals(st)}。`);
    return frames;
  }
  llSnap(frames, st, 3, `head 不是 NULL，而且 head 的值 ${base[0]} < ${item}：不放在最前面，進入 else。`, {n0: 'cmp'});
  st.ptr.current = 'n0';
  llSnap(frames, st, 7, 'current = head：current 從第一個節點出發。', {n0: 'hl'});
  let c = 'n0';
  for (;;) {
    const nx = st.next[c];
    if (!nx) {
      llSnap(frames, st, 8, `current->getNext() 是 NULL：${llN(st, c).v} 已是最後一個節點，停止前進。`, {[c]: 'hl'});
      break;
    }
    const nv = llN(st, nx).v;
    if (nv < item) {
      llSnap(frames, st, 8, `往前看下一個節點：${nv} < ${item}，新值應該更後面。`, {[c]: 'hl', [nx]: 'cmp'});
      st.ptr.current = nx; c = nx;
      llSnap(frames, st, 9, `current = current->getNext()：current 前進到 ${nv}。`, {[c]: 'hl'});
    } else {
      llSnap(frames, st, 8, `往前看下一個節點：${nv} < ${item} 不成立，停止。新節點要插在 ${llN(st, c).v} 與 ${nv} 之間。`, {[c]: 'hl', [nx]: 'cmp'});
      break;
    }
  }
  const nx = st.next[c];
  st.next.nn = nx; if (nx) st.es.nn = 'new';
  llSnap(frames, st, 11, nx ? `newNode->setNext(current->getNext())：新節點先接到後段 ${llN(st, nx).v}。` : 'newNode->setNext(current->getNext())：後面沒有節點，新節點的 next 是 NULL。', {[c]: 'hl'});
  st.next[c] = 'nn'; st.es[c] = 'new'; st.es.nn = '';
  llSnap(frames, st, 12, `current->setNext(newNode)：${llN(st, c).v} 的 next 改指新節點，插入完成。`, {[c]: 'hl'});
  llRelayout(st);
  llSnap(frames, st, 14, `add 結束：${llVals(st)}。`);
  return frames;
};

/* ---------- P03 OrderedList：remove ---------- */
LLB.oRemove = k => {
  const frames = [], item = {mid: 54, head: 17, miss: 45}[k];
  const st = llList([17, 26, 31, 54, 77, 93]), ids = llChain(st);
  st.ptr.current = 'n0'; st.ptr.previous = null; st.vars = [['item', String(item)]];
  llSnap(frames, st, 2, `remove(${item})：current = head，previous = NULL。`, {n0: 'hl'});
  let c = 'n0';
  while (c && llN(st, c).v < item) {
    const v = llN(st, c).v;
    llSnap(frames, st, 3, `current 不是 NULL，而且 ${v} < ${item}：繼續往後找。`, {[c]: 'cmp'});
    st.ptr.previous = c;
    llSnap(frames, st, 4, `previous = current：previous 移到 ${v}。`, {[c]: 'hl'});
    c = st.next[c]; st.ptr.current = c;
    llSnap(frames, st, 5, c ? `current = current->getNext()：current 前進到 ${llN(st, c).v}。` : 'current 變成 NULL。', c ? {[c]: 'hl'} : {});
  }
  const v = llN(st, c).v;
  llSnap(frames, st, 3, `${v} < ${item} 不成立，迴圈停止。`, {[c]: 'cmp'});
  if (v !== item) {
    ids.slice(ids.indexOf(c) + 1).forEach(r => { const n = llN(st, r); n.cls = 'skip'; n.tag = '未走訪'; });
    llSnap(frames, st, 7, `current 的值 ${v} 不等於 ${item}：${item} 不在串列中，直接 return，串列不變。`, {[c]: 'cmp'});
    return frames;
  }
  llSnap(frames, st, 7, `current 的值等於 ${item}，往下刪除。`, {[c]: 'found'});
  const prev = st.ptr.previous, after = st.next[c];
  if (!prev) {
    st.ptr.head = after; st.es.head = 'new';
    llSnap(frames, st, 8, `previous == NULL：刪的是第一個節點，head = current->getNext()，改指 ${llN(st, after).v}。`, {[c]: 'found'});
  } else {
    st.next[prev] = after; st.es[prev] = 'new';
    llSnap(frames, st, 9, `previous->setNext(current->getNext())：${llN(st, prev).v} 改指 ${after ? llN(st, after).v : 'NULL'}，跳過 ${item}。`, {[c]: 'found'});
  }
  const n = llN(st, c); n.cls = 'del'; n.tag = '已釋放';
  llSnap(frames, st, 10, `delete current：釋放 ${item} 的節點，current 成為失效指標。`);
  llRelayout(st);
  llSnap(frames, st, 11, `remove 結束：${llVals(st)}。`);
  return frames;
};

/* ---------- P05 雙向串列（header／trailer 哨兵） ---------- */
function llDouble(vals) {
  const st = {dbl: true, nodes: [], next: {}, prev: {}, ptr: {}, es: {}, ps: {}, vars: []};
  const ids = ['h', ...vals.map((v, i) => 'd' + i), 't'];
  ids.forEach((id, i) => {
    const sent = id === 'h' || id === 't';
    st.nodes.push({id, v: id === 'h' ? 'header' : id === 't' ? 'trailer' : vals[i - 1], col: i, row: 0, cls: sent ? 'sent' : ''});
    if (i + 1 < ids.length) st.next[id] = ids[i + 1];
    if (i > 0) st.prev[id] = ids[i - 1];
  });
  return st;
}
function llDoubleFinal(st) {
  const ids = ['h']; let c = 'h';
  while (st.next[c]) { c = st.next[c]; ids.push(c); }
  st.nodes = ids.map((id, i) => Object.assign(llN(st, id), {col: i, row: 0, cls: id === 'h' || id === 't' ? 'sent' : '', tag: ''}));
  st.ptr = {}; st.es = {}; st.ps = {};
  return ids.filter(id => id !== 'h' && id !== 't').map(id => llN(st, id).v).join(' ↔ ');
}
LLB.dIns = k => {
  const frames = [];
  const vals = k === 'empty' ? [] : [54, 93];
  const v = {mid: 26, front: 17, empty: 54}[k];
  const st = llDouble(vals);
  const L = k === 'mid' ? 'd0' : 'h', R = st.next[L];
  st.nodes.push({id: 'x', v, col: llN(st, L).col + 0.5, row: 1, cls: 'new'});
  st.ptr = {left: L, right: R, x: 'x'};
  const nm = id => llN(st, id).v;
  llSnap(frames, st, 1, `x 是新配置的節點 ${v}，要插在相鄰的 ${nm(L)} 與 ${nm(R)} 之間。`);
  st.prev.x = L; st.ps.x = 'new';
  llSnap(frames, st, 2, `x->prev = left：新節點的 prev 指向 ${nm(L)}。`);
  st.next.x = R; st.es.x = 'new'; st.ps.x = '';
  llSnap(frames, st, 3, `x->next = right：新節點的 next 指向 ${nm(R)}。到這裡只改了新節點，原串列還沒變。`);
  st.next[L] = 'x'; st.es[L] = 'new'; st.es.x = '';
  llSnap(frames, st, 4, `left->next = x：${nm(L)} 的 next 改指新節點。`);
  st.prev[R] = 'x'; st.ps[R] = 'new'; st.es[L] = '';
  llSnap(frames, st, 5, `right->prev = x：${nm(R)} 的 prev 也改指新節點。共改四個指標，插入完成。`);
  const s = llDoubleFinal(st);
  llSnap(frames, st, null, `結果：header ↔ ${s} ↔ trailer。不論插在最前、中間或空串列，都是同樣四步。`);
  return frames;
};
LLB.dErase = k => {
  const frames = [];
  const vals = k === 'only' ? [54] : [54, 26, 93];
  const X = k === 'mid' ? 'd1' : 'd0';
  const st = llDouble(vals);
  const nm = id => llN(st, id).v;
  st.ptr = {x: X};
  llSnap(frames, st, 1, `要刪除資料節點 x（${nm(X)}）。它左右一定各有一個鄰居，即使鄰居是哨兵。`, {[X]: 'found'});
  const L = st.prev[X], R = st.next[X];
  st.ptr.left = L;
  llSnap(frames, st, 2, `left = x->prev：取得左鄰 ${nm(L)}。`, {[X]: 'found'});
  st.ptr.right = R;
  llSnap(frames, st, 3, `right = x->next：取得右鄰 ${nm(R)}。`, {[X]: 'found'});
  st.next[L] = R; st.es[L] = 'new';
  llSnap(frames, st, 4, `left->next = right：${nm(L)} 的 next 跳過 x，直接指向 ${nm(R)}。`, {[X]: 'found'});
  st.prev[R] = L; st.ps[R] = 'new'; st.es[L] = '';
  llSnap(frames, st, 5, `right->prev = left：${nm(R)} 的 prev 也跳過 x。實際只改了兩個鏈結，x 已不在串列中。`, {[X]: 'found'});
  const n = llN(st, X); n.cls = 'del'; n.tag = '已釋放'; delete st.next[X]; delete st.prev[X]; st.ps = {};
  llSnap(frames, st, 6, 'delete x：釋放節點，x 成為失效指標。');
  const s = llDoubleFinal(st);
  llSnap(frames, st, null, s ? `結果：header ↔ ${s} ↔ trailer。` : '結果：只剩 header ↔ trailer，回到空串列的樣子。');
  return frames;
};

/* ---------- P05 環狀串列走訪 ---------- */
LLB.cTrav = k => {
  const frames = [];
  const vals = k === 'empty' ? [] : k === 'one' ? [54] : [54, 26, 93, 17];
  const st = llList(vals); st.lbl = 'above';
  if (vals.length) st.next['n' + (vals.length - 1)] = 'n0';
  if (!vals.length) {
    llSnap(frames, st, 1, 'head == nullptr：空串列沒有任何節點，條件不成立，什麼都不印。');
    return frames;
  }
  llSnap(frames, st, 1, vals.length === 1 ? 'head != nullptr。只有一個節點時，它的 next 指向自己。' : 'head != nullptr。最後一個節點的 next 指回 head，串列中沒有 NULL。');
  st.ptr.current = 'n0'; st.vars = [['輸出', '']];
  llSnap(frames, st, 2, 'current = head：記住起點。', {n0: 'hl'});
  const out = [];
  let c = 'n0';
  do {
    out.push(llN(st, c).v); st.vars = [['輸出', out.join(' ')]];
    llSnap(frames, st, 4, `輸出 ${llN(st, c).v}。`, {[c]: 'hl'});
    const nx = st.next[c]; st.ptr.current = nx;
    if (nx === 'n0') {
      llSnap(frames, st, 5, `current = current->getNext()：這一步沿 next 回到起點 ${vals[0]}。`, {n0: 'cmp'});
      llSnap(frames, st, 6, 'current == head：while 條件不成立，停止。每個節點剛好輸出一次。', {n0: 'cmp'});
      break;
    }
    llSnap(frames, st, 5, `current = current->getNext()：前進到 ${llN(st, nx).v}。`, {[nx]: 'hl'});
    llSnap(frames, st, 6, 'current != head，繼續下一輪。', {[nx]: 'hl'});
    c = nx;
  } while (true);
  return frames;
};

/* ---------- 初始畫面：每個動畫先顯示預設案例的第 0 格 ---------- */
document.querySelectorAll('.ll-widget').forEach(w => {
  const btn = w.querySelector('.ll-case');
  if (btn) btn.click();
});

function llRecase(p) { const b = document.querySelector(`.ll-case.on[data-ll="${p}"]`); if (b) b.click(); }
/* /linked-interactions */
