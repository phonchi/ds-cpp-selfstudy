/* 同操作對比：同一個操作在兩種資料結構上並排步進。不需要 Three.js，2D 模式也能用。
 *
 * 每一組由 sim 函式「真的跑一次」產生逐步快照（frame），計數也是模擬時累加的，不寫死。
 * frame 是純資料，render 只負責畫；check_island_browser.js 另外獨立計算一次來比對。
 */
const CMP = DATA.compare.pairs;
const cmpByKey = Object.fromEntries(CMP.map(c => [c.key, c]));
const GRAPH = DATA.graph;

function simInsert(pos, n = 8) {
  const base = Array.from({ length: n }, (_, i) => (i + 1) * 10), X = 99;
  // 陣列：計算位址一步到位，然後由後往前一次複製一格
  const a = base.slice(); a.push(null);
  const L = [{ kind: 'array', cells: a.slice(), hi: [], walk: 0, write: 0, msg: `容量足夠，要在索引 ${pos} 放入 ${X}。` }];
  let write = 0;
  for (let j = n; j > pos; j--) {
    a[j] = a[j - 1]; write++;
    L.push({ kind: 'array', cells: a.slice(), hi: [j], walk: 0, write, msg: `a[${j}] = a[${j - 1}]：複製一格。` });
  }
  a[pos] = X; write++;
  L.push({ kind: 'array', cells: a.slice(), hi: [pos], walk: 0, write, msg: `a[${pos}] = ${X}：完成。` });
  // 串列：只有 head，要插在 pos 就要先走到第 pos-1 個節點，再改兩條指標
  const nodes = base.slice();
  const R = [];
  if (pos === 0) {
    R.push({ kind: 'list', nodes: nodes.slice(), hi: [], walk: 0, write: 0, msg: `要在最前面放入 ${X}，不用走。` });
    R.push({ kind: 'list', nodes: nodes.slice(), hi: [0], added: { at: 0, v: X }, walk: 0, write: 1, msg: '新節點的 next 接住舊的第一個節點；head 還沒改。' });
    R.push({ kind: 'list', nodes: [X, ...nodes], hi: [0], walk: 0, write: 2, msg: 'head 改指新節點：完成。' });
  } else {
    let walk = 0;
    R.push({ kind: 'list', nodes: nodes.slice(), hi: [0], walk, write: 0, msg: 'cur 從 head 開始。' });
    for (let k = 1; k < pos; k++) {
      walk++;
      R.push({ kind: 'list', nodes: nodes.slice(), hi: [k], walk, write: 0, msg: 'cur = cur->next：沿著指標走一步。' });
    }
    R.push({ kind: 'list', nodes: nodes.slice(), hi: [pos - 1], added: { at: pos, v: X }, walk, write: 1, msg: '新節點的 next 接住 cur 的下一個；cur->next 還沒改。' });
    const after = nodes.slice(); after.splice(pos, 0, X);
    R.push({ kind: 'list', nodes: after, hi: [pos], walk, write: 2, msg: 'cur->next 改指新節點：完成。' });
  }
  return { left: L, right: R, counters: [['walk', '走到位置'], ['write', '寫入次數']] };
}

function simOrder() {
  const vals = ['A', 'B', 'C'];
  const run = kind => {
    const items = [], out = [], F = [{ kind, items: [], out: [], ops: 0, msg: '一開始是空的。' }];
    let ops = 0;
    vals.forEach(v => { items.push(v); ops++; F.push({ kind, items: items.slice(), out: out.slice(), ops, msg: kind === 'stack' ? `push(${v})：放到最上面。` : `enqueue(${v})：排到最後面。` }); });
    for (let i = 0; i < vals.length; i++) {
      const v = kind === 'stack' ? items.pop() : items.shift();
      out.push(v); ops++;
      F.push({ kind, items: items.slice(), out: out.slice(), ops, msg: kind === 'stack' ? `pop()：取出最上面的 ${v}。` : `dequeue()：取出最前面的 ${v}。` });
    }
    return F;
  };
  return { left: run('stack'), right: run('queue'), counters: [['ops', '操作次數']] };
}

function simSearch(target, values) {
  const v = values;
  const L = [{ kind: 'array', cells: v, hi: [], cmp: 0, msg: `從頭開始找 ${target}。` }];
  let cmp = 0, found = -1;
  for (let i = 0; i < v.length; i++) {
    cmp++;
    if (v[i] === target) { found = i; L.push({ kind: 'array', cells: v, hi: [i], ok: i, cmp, msg: `a[${i}] = ${v[i]}：找到了。` }); break; }
    L.push({ kind: 'array', cells: v, hi: [i], cmp, msg: `a[${i}] = ${v[i]}，不是，看下一格。` });
  }
  if (found < 0) L.push({ kind: 'array', cells: v, hi: [], cmp, msg: '走到最後都沒有：不存在。' });
  const R = [{ kind: 'array', cells: v, hi: [], lo: 0, up: v.length - 1, cmp: 0, msg: `範圍是整個陣列，找 ${target}。` }];
  let lo = 0, hi = v.length - 1, c = 0, hit = -1;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    c++;
    if (v[mid] === target) { hit = mid; R.push({ kind: 'array', cells: v, hi: [mid], ok: mid, lo, up: hi, cmp: c, msg: `a[${mid}] = ${v[mid]}：找到了。` }); break; }
    const s = { kind: 'array', cells: v, hi: [mid], lo, up: hi, cmp: c };
    if (v[mid] < target) { s.msg = `a[${mid}] = ${v[mid]} 太小，排除左半邊。`; lo = mid + 1; } else { s.msg = `a[${mid}] = ${v[mid]} 太大，排除右半邊。`; hi = mid - 1; }
    R.push(s);
  }
  if (hit < 0) R.push({ kind: 'array', cells: v, hi: [], lo: 0, up: -1, cmp: c, msg: '範圍已經空了：不存在。' });
  return { left: L, right: R, counters: [['cmp', '比較次數']] };
}

function graphAdj() {
  const adj = Object.fromEntries(Object.keys(GRAPH.vertices).map(k => [k, []]));
  GRAPH.edges.forEach(([a, b]) => { adj[a].push(b); adj[b].push(a); });
  Object.values(adj).forEach(l => l.sort());
  return adj;
}
function simWalk() {
  const adj = graphAdj(), S = GRAPH.start;
  const bfs = () => {
    const q = [S], seen = new Set([S]), order = [];
    const F = [{ kind: 'graph', list: 'queue', pend: q.slice(), order: [], cur: null, seen: [S], msg: `起點 ${S} 放進佇列。` }];
    while (q.length) {
      const u = q.shift(); order.push(u);
      const added = [];
      adj[u].forEach(w => { if (!seen.has(w)) { seen.add(w); q.push(w); added.push(w); } });
      F.push({ kind: 'graph', list: 'queue', pend: q.slice(), order: order.slice(), cur: u, seen: [...seen],
        msg: `取出最前面的 ${u}` + (added.length ? `，把 ${added.join('、')} 排到後面。` : '，沒有新鄰居。') });
    }
    return F;
  };
  const dfs = () => {
    const st = [S], seen = new Set(), order = [];
    const F = [{ kind: 'graph', list: 'stack', pend: st.slice(), order: [], cur: null, seen: [], msg: `起點 ${S} 放進堆疊。` }];
    while (st.length) {
      const u = st.pop();
      if (seen.has(u)) { F.push({ kind: 'graph', list: 'stack', pend: st.slice(), order: order.slice(), cur: null, seen: [...seen], msg: `取出 ${u}，但已經走過，略過。` }); continue; }
      seen.add(u); order.push(u);
      const added = adj[u].filter(w => !seen.has(w)).reverse();
      added.forEach(w => st.push(w));
      F.push({ kind: 'graph', list: 'stack', pend: st.slice(), order: order.slice(), cur: u, seen: [...seen],
        msg: `取出最上面的 ${u}` + (added.length ? `，依序把 ${added.join('、')} 疊上去，${added[added.length - 1]} 在最上面。` : '，沒有新鄰居。') });
    }
    return F;
  };
  return { left: bfs(), right: dfs(), counters: [] };
}

function cmpSim(key, opt) {
  const c = cmpByKey[key];
  if (key === 'insert') return simInsert(opt);
  if (key === 'order') return simOrder();
  if (key === 'search') return simSearch(opt, c.values);
  return simWalk();
}
window.__cmpSim = cmpSim;   // 給 check_island_browser.js 用：與獨立計算的結果比對

/* ── 畫面 ── */
const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; };
function drawArray(f) {
  const w = el('div', 'cmp-cells');
  f.cells.forEach((v, i) => {
    const c = el('div', 'cmp-cell', v === null ? '' : String(v));
    const out = f.lo !== undefined && (i < f.lo || i > f.up);
    if (v === null) c.classList.add('is-empty');
    if (out) c.classList.add('is-out');
    if (f.hi.includes(i)) c.classList.add('is-hi');
    if (f.ok === i) c.classList.add('is-ok');
    const idx = el('i', '', String(i)); c.appendChild(idx);
    w.appendChild(c);
  });
  return w;
}
function drawList(f) {
  const w = el('div', 'cmp-list');
  w.appendChild(el('span', 'cmp-head', 'head'));
  const arrow = cls => el('span', 'cmp-arrow' + (cls ? ' ' + cls : ''), '→');
  w.appendChild(arrow());
  f.nodes.forEach((v, i) => {
    const n = el('div', 'cmp-node', String(v));
    if (f.hi.includes(i)) n.classList.add('is-hi');
    w.appendChild(n); w.appendChild(arrow());
  });
  w.appendChild(el('span', 'cmp-null', 'nullptr'));
  if (!f.added) return w;
  // 新節點的 next 已接上，但前一個節點（或 head）還沒改指：新節點先畫在串列外面
  const box = el('div', 'cmp-listbox'), row = el('div', 'cmp-list cmp-pending');
  row.append(el('div', 'cmp-node is-new', String(f.added.v)), arrow('is-new'),
    f.added.at < f.nodes.length ? el('div', 'cmp-node', String(f.nodes[f.added.at])) : el('span', 'cmp-null', 'nullptr'),
    el('span', 'cmp-end', '新節點的 next'));
  box.append(w, row);
  return box;
}
function drawOrder(f) {
  const w = el('div', 'cmp-order');
  const box = el('div', f.kind === 'stack' ? 'cmp-stack' : 'cmp-queue');
  f.items.forEach(v => box.appendChild(el('div', 'cmp-item', v)));
  if (f.kind === 'stack') {
    w.appendChild(el('div', 'cmp-end', '只開頂端'));
    w.appendChild(box);
  } else {
    const row = el('div', 'cmp-qrow');
    row.append(el('span', 'cmp-end', 'front'), box, el('span', 'cmp-end', 'back'));
    w.appendChild(row);
  }
  const out = el('div', 'cmp-out');
  out.append('取出順序：', el('b', '', f.out.join('、') || '—'));
  w.appendChild(out);
  return w;
}
function drawGraph(f) {
  const NS = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', '-11 -9 18 17'); svg.setAttribute('class', 'cmp-graph');
  svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', '圖的走訪狀態');
  const V = GRAPH.vertices;
  GRAPH.edges.forEach(([a, b]) => {
    const l = document.createElementNS(NS, 'line');
    l.setAttribute('x1', V[a][0]); l.setAttribute('y1', V[a][1]); l.setAttribute('x2', V[b][0]); l.setAttribute('y2', V[b][1]);
    l.setAttribute('class', 'cmp-edge'); svg.appendChild(l);
  });
  Object.entries(V).forEach(([k, [x, y]]) => {
    const g = document.createElementNS(NS, 'g');
    const r = document.createElementNS(NS, 'rect');
    r.setAttribute('x', x - 1.2); r.setAttribute('y', y - 1.2); r.setAttribute('width', 2.4); r.setAttribute('height', 2.4); r.setAttribute('rx', .2);
    const orderIdx = f.order.indexOf(k);
    r.setAttribute('class', 'cmp-v' + (k === f.cur ? ' is-cur' : orderIdx >= 0 ? ' is-done' : f.pend.includes(k) ? ' is-pend' : ''));
    const t = document.createElementNS(NS, 'text');
    t.setAttribute('x', x); t.setAttribute('y', y + .55); t.setAttribute('text-anchor', 'middle'); t.textContent = k;
    g.append(r, t); svg.appendChild(g);
  });
  const w = el('div', 'cmp-walk');
  w.appendChild(svg);
  const p = el('div', 'cmp-pend');
  p.append((f.list === 'queue' ? '佇列（前 → 後）：' : '堆疊（底 → 頂）：'), el('b', '', f.pend.join(' ') || '空'));
  const o = el('div', 'cmp-pend');
  o.append('走訪順序：', el('b', '', f.order.join(' ') || '—'));
  w.append(p, o);
  return w;
}
function drawFrame(f) {
  if (f.kind === 'array') return drawArray(f);
  if (f.kind === 'list') return drawList(f);
  if (f.kind === 'graph') return drawGraph(f);
  return drawOrder(f);
}

let cmpKey = CMP[0].key, cmpOpt = {}, cmpRun = null, cmpI = 0, cmpTimer = 0;
const cmpDlg = $('cmpDialog');
function stopCmp() { if (cmpTimer) { clearInterval(cmpTimer); cmpTimer = 0; $('cmpPlay').textContent = '▶ 自動播放'; } }
function cmpSteps() { return Math.max(cmpRun.left.length, cmpRun.right.length); }
function renderSide(host, title, frames) {
  const f = frames[Math.min(cmpI, frames.length - 1)];
  const finished = cmpI >= frames.length - 1;
  host.replaceChildren();
  const h = el('h3', '', title);
  if (finished) h.appendChild(el('span', 'cmp-fin', '完成'));
  host.appendChild(h);
  host.appendChild(drawFrame(f));
  if (cmpRun.counters.length) {
    const cs = el('dl', 'cmp-counters');
    cmpRun.counters.forEach(([k, label]) => {
      const d = el('div'); d.dataset.counter = k;
      d.append(el('dt', '', label), el('dd', '', String(f[k])));
      cs.appendChild(d);
    });
    host.appendChild(cs);
  }
  host.appendChild(el('p', 'cmp-msg', f.msg));
}
function renderCmp() {
  const c = cmpByKey[cmpKey], n = cmpSteps();
  renderSide($('cmpLeft'), c.left, cmpRun.left);
  renderSide($('cmpRight'), c.right, cmpRun.right);
  $('cmpStep').textContent = `第 ${cmpI}／${n - 1} 步`;
  $('cmpPrev').disabled = cmpI === 0;
  $('cmpNext').disabled = cmpI === n - 1;
  const opt = cmpOpt[cmpKey];
  const note = c.notes ? c.notes[String(opt)] : c.note;
  $('cmpNote').textContent = cmpI === n - 1 ? note : '';
}
function loadCmp(key, opt) {
  stopCmp();
  cmpKey = key;
  const c = cmpByKey[key];
  if (opt !== undefined) cmpOpt[key] = opt;
  else if (cmpOpt[key] === undefined) cmpOpt[key] = c.default;
  cmpRun = cmpSim(key, cmpOpt[key]);
  cmpI = 0;
  $('cmpTitle').textContent = c.label;
  $('cmpOp').textContent = c.op;
  $('cmpTabs').querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.key === key)));
  const opts = $('cmpOpts');
  opts.replaceChildren();
  if (c.options) {
    opts.appendChild(el('span', 'cmp-opts-h', c.opt_label));
    c.options.forEach(o => {
      const b = el('button', 'cmp-chip', o.label);
      b.type = 'button'; b.setAttribute('aria-pressed', String(o.v === cmpOpt[key]));
      b.addEventListener('click', () => loadCmp(key, o.v));
      opts.appendChild(b);
    });
  }
  renderCmp();
}
CMP.forEach(c => {
  const b = el('button', 'cmp-tab', c.label);
  b.type = 'button'; b.dataset.key = c.key;
  b.addEventListener('click', () => loadCmp(c.key));
  $('cmpTabs').appendChild(b);
});
function openCompare(key) {
  loadCmp(key || cmpKey);
  if (!cmpDlg.open) cmpDlg.showModal();
}
$('islCompare').addEventListener('click', () => openCompare());
$('cmpClose').addEventListener('click', () => cmpDlg.close());
cmpDlg.addEventListener('close', stopCmp);
cmpDlg.addEventListener('click', e => { if (e.target === cmpDlg) cmpDlg.close(); });   // 點對話框外面
$('cmpPrev').addEventListener('click', () => { stopCmp(); if (cmpI > 0) { cmpI--; renderCmp(); } });
$('cmpNext').addEventListener('click', () => { stopCmp(); if (cmpI < cmpSteps() - 1) { cmpI++; renderCmp(); } });
$('cmpReset').addEventListener('click', () => { stopCmp(); cmpI = 0; renderCmp(); });
$('cmpPlay').addEventListener('click', () => {
  if (cmpTimer) { stopCmp(); return; }
  if (cmpI === cmpSteps() - 1) cmpI = 0;
  $('cmpPlay').textContent = '⏸ 暫停';
  renderCmp();
  cmpTimer = setInterval(() => {
    if (cmpI >= cmpSteps() - 1) { stopCmp(); return; }
    cmpI++; renderCmp();
  }, 950);
});

// 面板上：這一章相關的對比組
function renderPanelCompare(stem) {
  const host = $('islPanelCmp');
  const list = CMP.filter(c => c.stems.includes(stem));
  host.hidden = !list.length;
  host.replaceChildren(...list.map(c => {
    const b = el('button', 'isl-cmp-link', `同操作對比：${c.label} →`);
    b.type = 'button';
    b.addEventListener('click', () => openCompare(c.key));
    return b;
  }));
}
