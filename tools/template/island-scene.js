/* 3D 矽晶群島的場景層。由 island.js 的 initScene() 呼叫 buildWorld()。
 *
 * 視覺語言（反向檢查：不可出現倒角、投影、水面、粉彩）：
 *   - 正交鏡頭、限制視角；硬邊方塊，無光照的 MeshBasicMaterial，明暗烘在頂點色（頂面亮、側面暗）
 *   - 靜態零件依種類合併成 InstancedMesh；描邊合併成一條 LineSegments；晶片表面的絲印烘在一張圖集上
 *   - 會動的零件共用兩個動態 InstancedMesh（方塊、角錐），不另建 mesh
 *   - 每座地標的動畫是純函式 pose(u)，u = 0 是靜止姿態；播放只是把 u 從 0 推到 1
 *   - 匯流排（授課順序）是粗的金色走線；資料結構裡的指標是細的紅色箭頭，兩者不可混用
 * 地標的結構約束列在 tools/island_meta.py 開頭，check_island_browser.js 會用 invariants() 實測。
 * 本檔與 island.js 共用頂層名稱：PAGES、BY、ISLES、trail、select、$、reduceMotion、DATA、graphAdj。
 */
function buildWorld(THREE, addons, renderer, stage, canvas) {
  const { OrbitControls } = addons;
  const motion = () => !reduceMotion.matches;
  const narrow = () => stage.clientWidth < 768;
  const world = new THREE.Scene();
  let need = true, raf = 0, onScreen = true, alive = true, lowPower = false, dprLevel = 0, tagsDirty = true, draws = 0;

  /* ── 色盤：站內的墨、深藍、紅、森林綠、金、米白；深底上需要提亮的紅綠由同色相推導 ── */
  const PAL = {
    power: {
      bg: '#0f0f1e', board: '#1a1a2e', boardEdge: '#2c3e7a', pad: '#2d2d4a', sub: '#2c3e7a', die: '#1f1f36', pin: '#c7a14a',
      trace: '#f5b82e', cell: '#3d3d63', cell2: '#33335a', rail: '#9094b5', val: '#f7f3eb', a: '#f5b82e', b: '#e8604c', c: '#3fbf95', d: '#7f97e6', e: '#f7f3eb',
      hi: '#f5b82e', ptr: '#ff7a66', node: '#f7f3eb', next: '#5f78cc', wire: '#3fbf95', dimm: '#1a6b4a', ledOff: '#3a3a58', ledVisit: '#f5b82e', ledDone: '#3fbf95',
      metal: '#9a9db8', sel: '#f7f3eb', ink: '#1a1a2e', dim: '#55587e', line: '#585c85', silk: '#c9c6d6', silkDim: '#6d7096', halo: '#f5b82e',
    },
    print: {
      bg: '#f7f3eb', board: '#fffdf7', boardEdge: '#e8e2d6', pad: '#e8e2d6', sub: '#f1ebdd', die: '#fffdf7', pin: '#8a8578',
      trace: '#2c3e7a', cell: '#f1ebdd', cell2: '#e8e2d6', rail: '#2c3e7a', val: '#2c3e7a', a: '#2c3e7a', b: '#c0392b', c: '#1a6b4a', d: '#8a8578', e: '#1a1a2e',
      hi: '#c0392b', ptr: '#c0392b', node: '#fffdf7', next: '#2c3e7a', wire: '#1a6b4a', dimm: '#e3efe7', ledOff: '#d8d2c4', ledVisit: '#b9770e', ledDone: '#1a6b4a',
      metal: '#c8c2b4', sel: '#c0392b', ink: '#1a1a2e', dim: '#b9b3a4', line: '#2c3e7a', silk: '#2c3e7a', silkDim: '#8a8578', halo: '#ffffff',
    },
  };
  const ROLE = {};                         // role → 目前模式下的顏色
  Object.keys(PAL.power).forEach(k => { ROLE[k] = new THREE.Color(PAL.power[k]); });
  const _ca = new THREE.Color(), _cb = new THREE.Color();
  let modeK = 0, modeTarget = 0;           // 0 = 通電、1 = 藍圖
  const mixRoles = k => Object.keys(PAL.power).forEach(r => ROLE[r].copy(_ca.set(PAL.power[r])).lerp(_cb.set(PAL.print[r]), k));

  world.background = new THREE.Color(PAL.power.bg);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.NoToneMapping;

  /* ── 幾何：明暗直接烘進頂點色 ── */
  function shade(geo) {
    const g = geo.index ? geo.toNonIndexed() : geo;
    g.computeVertexNormals();
    const n = g.attributes.normal, c = new Float32Array(n.count * 3);
    for (let i = 0; i < n.count; i++) {
      const ny = n.getY(i), nx = n.getX(i), nz = n.getZ(i);
      const s = ny > .5 ? 1 : ny < -.5 ? .45 : .6 + .18 * Math.max(0, -nx) + .1 * Math.max(0, nz) + .22 * Math.max(0, ny);
      c[i * 3] = c[i * 3 + 1] = c[i * 3 + 2] = s;
    }
    g.setAttribute('color', new THREE.BufferAttribute(c, 3));
    return g;
  }
  const GEO = {
    box: shade(new THREE.BoxGeometry(1, 1, 1)),
    pyr: shade(new THREE.ConeGeometry(.5, 1, 4).rotateY(Math.PI / 4)),
  };
  const solid = new THREE.MeshBasicMaterial({ vertexColors: true });

  /* ── 靜態零件 ── */
  const parts = { box: [], pyr: [] };
  const edgePos = [];
  const _m = new THREE.Matrix4(), _q = new THREE.Quaternion(), _p = new THREE.Vector3(), _s = new THREE.Vector3();
  const _UX = new THREE.Vector3(0, 0, 1), _UY = new THREE.Vector3(0, 1, 0), _d = new THREE.Vector3(), _e = new THREE.Euler();
  function boxEdges(x0, y0, z0, x1, y1, z1) {
    const v = [[x0, y0, z0], [x1, y0, z0], [x1, y0, z1], [x0, y0, z1], [x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]];
    [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]].forEach(([a, b]) => edgePos.push(...v[a], ...v[b]));
  }
  // y 是底面高度；edge=false 的小零件不描邊
  function box(x, y, z, sx, sy, sz, role, { edge = true } = {}) {
    parts.box.push({ m: new THREE.Matrix4().compose(_p.set(x, y + sy / 2, z), _q.identity(), _s.set(sx, sy, sz)), role });
    if (edge) boxEdges(x - sx / 2, y, z - sz / 2, x + sx / 2, y + sy, z + sz / 2);
  }
  function beamMatrix(m, a, b, w, h) {
    _d.subVectors(b, a); const len = Math.max(.0001, _d.length()); _d.divideScalar(len);
    return m.compose(_p.addVectors(a, b).multiplyScalar(.5), _q.setFromUnitVectors(_UX, _d), _s.set(w, h, len));
  }
  function beam(a, b, w, h, role) { parts.box.push({ m: beamMatrix(new THREE.Matrix4(), a, b, w, h), role }); }

  /* ── 動態零件：共用 InstancedMesh，隱藏＝縮放 0 ── */
  function pool(kind, cap) {
    const mesh = new THREE.InstancedMesh(GEO[kind], solid, cap);
    mesh.frustumCulled = false; mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    const roles = []; const zero = new THREE.Matrix4().makeScale(0, 0, 0);
    mesh.setColorAt(0, ROLE.val);
    for (let i = 0; i < cap; i++) mesh.setMatrixAt(i, zero);
    const P = {
      mesh, roles,
      alloc(role) { if (roles.length >= cap) throw new Error('dyn pool 已滿：' + kind); roles.push(role); mesh.setColorAt(roles.length - 1, ROLE[role]); mesh.instanceColor.needsUpdate = true; return roles.length - 1; },
      role(id, role) { if (roles[id] === role) return; roles[id] = role; mesh.setColorAt(id, ROLE[role]); mesh.instanceColor.needsUpdate = true; },
      hide(id) { mesh.setMatrixAt(id, zero); mesh.instanceMatrix.needsUpdate = true; },
      at(id, x, y, z, sx, sy, sz) { _m.compose(_p.set(x, y + sy / 2, z), _q.identity(), _s.set(sx, sy, sz)); mesh.setMatrixAt(id, _m); mesh.instanceMatrix.needsUpdate = true; },
      beam(id, a, b, w, h) { mesh.setMatrixAt(id, beamMatrix(_m, a, b, w, h)); mesh.instanceMatrix.needsUpdate = true; },
      recolor() { roles.forEach((r, i) => mesh.setColorAt(i, ROLE[r])); mesh.instanceColor.needsUpdate = true; },
    };
    world.add(mesh);
    return P;
  }
  const DB = pool('box', 520), DP = pool('pyr', 60);

  // 指標箭頭：細的紅色光束＋角錐箭頭（和粗的金色匯流排明顯不同）
  function arrowAlloc(role = 'ptr') { return { b: DB.alloc(role), p: DP.alloc(role), role }; }
  const _a0 = new THREE.Vector3(), _a1 = new THREE.Vector3();
  function arrowSet(A, a, b) {
    _d.subVectors(b, a); const len = _d.length();
    if (len < .3) { DB.hide(A.b); DP.hide(A.p); return; }
    const head = Math.min(.85, len * .5);
    _a0.copy(a); _a1.copy(b).addScaledVector(_d.divideScalar(len), -head);
    DB.beam(A.b, _a0, _a1, .24, .24);
    _d.subVectors(b, a).divideScalar(len);
    _p.copy(b).addScaledVector(_d, -head / 2);
    _q.setFromUnitVectors(_UY, _d);
    _m.compose(_p, _q, _s.set(.72, head, .72));
    DP.mesh.setMatrixAt(A.p, _m); DP.mesh.instanceMatrix.needsUpdate = true;
  }
  function arrowHide(A) { DB.hide(A.b); DP.hide(A.p); }
  function arrowStatic(a, b, role = 'ptr') { const A = arrowAlloc(role); arrowSet(A, a, b); return A; }

  const clamp01 = x => Math.max(0, Math.min(1, x));
  const seg = (u, a, b) => { const t = clamp01((u - a) / (b - a)); return t * t * (3 - 2 * t); };
  const lerp = (a, b, t) => a + (b - a) * t;
  const V = (x, y, z) => new THREE.Vector3(x, y, z);

  /* ═════════ 配置 ═════════ */
  const T = 2.9;                           // 晶片表面高度
  const COLX = [-27, 0, 27], ROWZ = [-24, 0, 24];
  const W = 22, D = 17, ROWP = -45, DP_W = 7.6, DP_D = 7, DIMMZ = 44;
  const CORE = PAGES.filter(p => p.grp === 'core').map(p => p.stem);
  const POWER = PAGES.filter(p => p.grp === 'power').map(p => p.stem);
  const DIMM = PAGES.filter(p => p.grp === 'dimm').map(p => p.stem);
  const CHIP = {};
  const SNAKE = [[0, 0], [1, 0], [2, 0], [2, 1], [1, 1], [0, 1], [0, 2], [1, 2], [2, 2]];
  const hex = i => '0x' + (0x1000 + i * 0x100).toString(16).toUpperCase();
  const pageIndex = Object.fromEntries(PAGES.map((p, i) => [p.stem, i]));
  function chipAt(stem, x, z, w, d, atlas) {
    CHIP[stem] = { stem, x, z, w, d, T, atlas, bake: [], top: T + 10, code: BY[stem].code, addr: hex(pageIndex[stem]) };
  }
  const SC = 34;       // 圖集的 px／單位
  CORE.forEach((s, i) => { const [c, r] = SNAKE[i]; chipAt(s, COLX[c], ROWZ[r], W, D, { x: c * 680, y: r * 510, w: 680, h: 510 }); });
  POWER.forEach((s, i) => chipAt(s, COLX[i], ROWP, W, 9, { x: i * 680, y: 1530, w: 680, h: 238 }));
  DIMM.forEach((s, i) => chipAt(s, -34.4 + i * 8.6, DIMMZ, DP_W, DP_D, { x: i * 218, y: 1768, w: 190, h: 170 }));

  /* ── 底板 ── */
  box(0, -2.4, 0, 86, 2.4, 114, 'boardEdge');

  /* ── 匯流排：只表示授課順序。粗、金色、直角轉彎 ── */
  const BUS = [[-27, ROWP], [27, ROWP], [27, -36.5], [-27, -36.5], [-27, ROWZ[0]], [27, ROWZ[0]], [27, ROWZ[1]], [-27, ROWZ[1]], [-27, ROWZ[2]], [27, ROWZ[2]]];
  const haloParts = [];
  for (let i = 0; i < BUS.length - 1; i++) {
    const [x0, z0] = BUS[i], [x1, z1] = BUS[i + 1];
    const cx = (x0 + x1) / 2, cz = (z0 + z1) / 2, sx = Math.abs(x1 - x0) + 1.1, sz = Math.abs(z1 - z0) + 1.1;
    box(cx, .02, cz, sx, .18, sz, 'trace', { edge: false });
    haloParts.push([cx, cz, sx + .9, sz + .9]);
  }
  BUS.forEach(([x, z]) => box(x, .2, z, 1.7, .06, 1.7, 'pin', { edge: false }));   // 轉角的焊墊

  /* ── 晶片本體 ── */
  function buildChip(C, { pad = true } = {}) {
    const { x, z, w, d } = C;
    if (pad) box(x, 0, z, w + 1.6, .1, d + 1.6, 'pad', { edge: false });
    box(x, 1, z, w, 1.4, d, 'sub');
    box(x, 2.4, z, w - 2, .5, d - 2, 'die');
    const pinStep = w > 12 ? 1.5 : 1.2;
    for (let px = -w / 2 + 1; px <= w / 2 - .8; px += pinStep) {
      box(x + px, .08, z - d / 2 - .1, .5, 1.3, .22, 'pin', { edge: false });
      box(x + px, .08, z + d / 2 + .1, .5, 1.3, .22, 'pin', { edge: false });
    }
    for (let pz = -d / 2 + 1; pz <= d / 2 - .8; pz += pinStep) {
      box(x - w / 2 - .1, .08, z + pz, .22, 1.3, .5, 'pin', { edge: false });
      box(x + w / 2 + .1, .08, z + pz, .22, 1.3, .5, 'pin', { edge: false });
    }
    C.led = DB.alloc('ledOff');
    const lx = w > 12 ? w / 2 - 1 : w / 2 - .7;
    DB.at(C.led, x + lx, 2.4, z - d / 2 + .5, .85, .32, .7);
  }
  CORE.concat(POWER).forEach(s => buildChip(CHIP[s]));
  // 先備：一條綠色的記憶體模組（DIMM），九顆顆粒插在上面，前緣是金手指
  box(0, 0, DIMMZ + 1, 78, .95, 12, 'dimm');
  for (let cx = -37.5; cx <= 37.5; cx += 1.25) box(cx, .95, DIMMZ + 6.1, .7, .06, 1.5, 'pin', { edge: false });
  DIMM.forEach(s => buildChip(CHIP[s], { pad: false }));

  /* ═════════ 地標：每座回傳 pose(u)，u = 0 是靜止姿態 ═════════ */
  const LM = {};           // stem → { pose, dur }
  const INV = {};          // 給 check_island_browser.js 的結構約束實測
  const lbox = (C, lx, y, lz, sx, sy, sz, role, o) => box(C.x + lx, C.T + y, C.z + lz, sx, sy, sz, role, o);
  const LP = (C, lx, y, lz) => V(C.x + lx, C.T + y, C.z + lz);
  const say = (C, text, lx, lz, size = .8, align = 'center', role = 'silk') => C.bake.push({ text, lx, lz, size, align, role });
  const dat = (C, id, lx, y, lz, sx, sy, sz) => DB.at(id, C.x + lx, C.T + y, C.z + lz, sx, sy, sz);

  // 01 C++ 導論：位元組與指標。char／int／double 佔不同格數；p 存的是 x 的位址
  {
    const C = CHIP.introduction, s = 1.2, z0 = 2.2; let cx = -8.5;
    const span = (n, name) => {
      const x0 = cx;
      for (let i = 0; i < n; i++) { lbox(C, cx + s / 2, 0, z0, s, .6, 3, i % 2 ? 'cell2' : 'cell'); cx += s; }
      say(C, name, (x0 + cx) / 2, z0 + 2.3, .85); const c = (x0 + cx) / 2; cx += .6; return c;
    };
    span(1, 'char'); const xInt = span(4, 'int x'); span(8, 'double');
    say(C, '1 byte', -7.9, z0 + 3.5, .6, 'center', 'silkDim'); say(C, '4 bytes', xInt, z0 + 3.5, .6, 'center', 'silkDim'); say(C, '8 bytes', 3.1 + 1.2, z0 + 3.5, .6, 'center', 'silkDim');
    lbox(C, 1.4, 0, -4.6, 3.2, 2, 2.6, 'next'); say(C, 'int* p', 1.4, -2.5, .8);
    say(C, 'int x = 100;', 4.2, -6, .68, 'left'); say(C, 'int* p = &x;', 4.2, -4.9, .68, 'left'); say(C, '*p = 50;', 4.2, -3.8, .68, 'left');
    const val = DB.alloc('a'), A = arrowAlloc(), pkt = DB.alloc('hi');
    LM.introduction = { dur: 5.2, pose(u) {
      const h = lerp(3, 1.5, seg(u, .45, .58));
      dat(C, val, xInt, .6, z0, 4.5, h, 2.6);
      const from = LP(C, 1.4, 2, -4.6), to = LP(C, xInt + 1, .6 + h, z0 - .6);
      arrowSet(A, from, to);       // *p = 50 只改 x 的值，p 仍然指著 x
      if (u > .12 && u < .46) { const t = seg(u, .14, .44), P = from.clone().lerp(to, t); DB.at(pkt, P.x, P.y - .25, P.z, .6, .6, .6); } else DB.hide(pkt);
    } };
  }

  // 02 演算法分析：六根柱子的高度真的照 f(n) 計算；超過刻度就截斷並標紅
  {
    const C = CHIP.analysis, FN = [['1', () => 1], ['log n', n => Math.log2(n)], ['n', n => n], ['n log n', n => n * Math.log2(n)], ['n²', n => n * n], ['2ⁿ', n => 2 ** n]];
    const MAX = 8.2, K = .13, step = 3.3, x0 = -8.25;
    lbox(C, -9.6, 0, -2.1, .3, MAX, .3, 'rail', { edge: false }); lbox(C, 9.6, 0, -2.1, .3, MAX, .3, 'rail', { edge: false });
    lbox(C, 0, MAX, -2.1, 19.5, .22, .3, 'rail', { edge: false });
    say(C, '刻度上限', -6.5, -6.6, .72, 'center', 'silkDim');
    const bars = FN.map(([name], i) => {
      lbox(C, x0 + i * step, 0, 1, 2.8, .2, 2.8, 'cell');
      say(C, name, x0 + i * step, 3.6, .78);
      return { bar: DB.alloc('d'), cap: DB.alloc('b') };
    });
    say(C, 'n 變大時，誰先撞到上限？', 0, 5.6, .78, 'center', 'silkDim');
    LM.analysis = { dur: 6, pose(u) {
      const n = lerp(2, 16, seg(u, .04, .9));
      FN.forEach(([, f], i) => {
        const raw = Math.max(.25, f(n) * K), h = Math.min(MAX - .1, raw);
        dat(C, bars[i].bar, x0 + i * step, .2, 1, 2.3, h, 2.3);
        if (raw > MAX - .1) dat(C, bars[i].cap, x0 + i * step, .2 + h, 1, 2.5, .3, 2.5); else DB.hide(bars[i].cap);
      });
    } };
  }

  // 03 陣列：格子零間距。insert(1, 99) 一次複製一格（中途會有兩個相同的值，這是複製不是交換）
  {
    const C = CHIP.arrays, s = 2.2, n = 8, x0 = -8.8, z0 = 3.2, cellX = i => x0 + s * i + s / 2;
    INV.arrays = { cells: [] };
    for (let i = 0; i < n; i++) {
      lbox(C, cellX(i), 0, z0, s, .7, 2.6, i % 2 ? 'cell2' : 'cell');
      INV.arrays.cells.push({ x0: x0 + s * i, x1: x0 + s * (i + 1) });
      say(C, String(i), cellX(i), z0 + 2, .7, 'center', 'silkDim');
    }
    say(C, 'base + i × 4', -5, z0 + 3.3, .72, 'center', 'silkDim');
    // 稀疏矩陣：大多是空格，只存非零項
    const sparse = [[0, 1], [1, 4], [2, 2], [3, 5]], gx = -8.8, gz = -6.6, gs = 1.05;
    for (let r = 0; r < 4; r++) for (let c = 0; c < 6; c++) {
      const on = sparse.some(([a, b]) => a === r && b === c);
      lbox(C, gx + c * gs + gs / 2, 0, gz + r * gs + gs / 2, gs, on ? .9 : .18, gs, on ? 'a' : 'cell2', { edge: false });
    }
    sparse.forEach(([r, c], i) => say(C, `(${r},${c}) → v`, 4.8, gz + .55 + i * 1.05, .74, 'center'));
    const roles = ['a', 'b', 'c', 'd', 'e'];
    const slots = Array.from({ length: n }, () => DB.alloc('a')), mover = DB.alloc('hi');
    const put = (i, role) => { DB.role(slots[i], role); dat(C, slots[i], cellX(i), .7, z0, s - .35, 1.5, 2); };
    LM.arrays = { dur: 6, pose(u) {
      if (u >= .985) u = 0;
      const cur = roles.concat([null, null, null]);
      const STEPS = 4, a = .08, span = .13;          // a[4→5]、a[3→4]、a[2→3]、a[1→2]，最後放 99
      DB.hide(mover);
      for (let k = 0; k < STEPS; k++) {
        const from = 4 - k, to = from + 1, t0 = a + k * span, t1 = t0 + span;
        if (u >= t1) cur[to] = cur[from];
        else if (u > t0) {
          const t = seg(u, t0, t1 - .02);
          DB.role(mover, cur[from]);
          dat(C, mover, lerp(cellX(from), cellX(to), t), .7 + 1.5 + Math.sin(t * Math.PI) * 1.2, z0, s - .5, 1.3, 1.8);
        }
      }
      const tP = a + STEPS * span;
      if (u >= tP + .1 && u < .985) cur[1] = 'hi';
      else if (u > tP && u < .985) { DB.role(mover, 'hi'); dat(C, mover, cellX(1), .7 + lerp(5, 0, seg(u, tP, tP + .1)), z0, s - .35, 1.5, 2); }
      slots.forEach((id, i) => { if (cur[i]) put(i, cur[i]); else DB.hide(id); });
    } };
  }

  // 04 鏈結串列：節點故意不共線，靠箭頭相連。add(26)：只改箭頭，其他節點不動
  {
    const C = CHIP.linked_lists, NODES = [[-4.6, -4.2], [4.8, -5.4], [7.2, 1.6], [-.8, 2.8]], NEW = [-7.6, 1.2], h = 1.5;
    INV.linked_lists = { nodes: NODES.map(n => n.slice()) };
    const node = (x, z) => { lbox(C, x, 0, z, 2, h, 2, 'node'); lbox(C, x + 1.5, 0, z, 1, h, 2, 'next'); };
    NODES.forEach(([x, z]) => node(x, z));
    const head = [-8.6, -6]; lbox(C, head[0], 0, head[1], 2, 1, 1.6, 'cell'); say(C, 'head', head[0], head[1] + 1.6, .78);
    const NUL = [-6.4, 6.2];
    lbox(C, NUL[0], 0, NUL[1], 2.4, .22, .4, 'rail', { edge: false }); lbox(C, NUL[0], 0, NUL[1] + .6, 1.6, .22, .4, 'rail', { edge: false }); lbox(C, NUL[0], 0, NUL[1] + 1.1, .8, .22, .3, 'rail', { edge: false });
    say(C, 'nullptr', NUL[0] + 4.2, NUL[1] + .5, .8);
    const out = ([x, z]) => LP(C, x + 1.5, h + .15, z), inn = ([x, z]) => LP(C, x - .2, h + .15, z);
    for (let i = 0; i + 1 < NODES.length; i++) arrowStatic(out(NODES[i]), inn(NODES[i + 1]));
    arrowStatic(out(NODES[3]), LP(C, NUL[0] + .6, .3, NUL[1]));
    const fresh = [DB.alloc('c'), DB.alloc('next')], hA = arrowAlloc(), nA = arrowAlloc('wire');
    const hOut = LP(C, head[0], 1.15, head[1]);
    LM.linked_lists = { dur: 5.4, pose(u) {
      const up = seg(u, .1, .28), on = u > .08 && u < .985;
      if (on) {
        dat(C, fresh[0], NEW[0], lerp(-1.4, 0, up), NEW[1], 2, h * up + .001, 2);
        dat(C, fresh[1], NEW[0] + 1.5, lerp(-1.4, 0, up), NEW[1], 1, h * up + .001, 2);
      } else { DB.hide(fresh[0]); DB.hide(fresh[1]); }
      const g = seg(u, .32, .52);
      if (on && g > .02) arrowSet(nA, out(NEW), new THREE.Vector3().lerpVectors(out(NEW), inn(NODES[0]), g)); else arrowHide(nA);
      const sw = on ? seg(u, .6, .82) : 0;
      arrowSet(hA, hOut, new THREE.Vector3().lerpVectors(inn(NODES[0]), inn(NEW), sw));
    } };
  }

  // 05 堆疊／佇列／Deque：差別只在開口。護欄四面封閉，堆疊只開頂端
  {
    const C = CHIP.linear_structures;
    const SX = -6.6, SW = 3.2, LV = 1.65, levels = 3;
    INV.linear_structures = { stackWalls: 4, stackTopOpen: true, levels };
    lbox(C, SX, 0, 0, SW + .6, .25, SW + .6, 'cell');
    [[-1, -1], [1, -1], [1, 1], [-1, 1]].forEach(([a, b]) => lbox(C, SX + a * SW / 2, 0, b * SW / 2, .24, LV * levels + .2, .24, 'rail', { edge: false }));
    for (let l = 0; l <= levels - 1; l++) {
      const y = .55 + l * LV;
      lbox(C, SX, y, -SW / 2, SW, .16, .16, 'rail', { edge: false }); lbox(C, SX, y, SW / 2, SW, .16, .16, 'rail', { edge: false });
      lbox(C, SX - SW / 2, y, 0, .16, .16, SW, 'rail', { edge: false }); lbox(C, SX + SW / 2, y, 0, .16, .16, SW, 'rail', { edge: false });
    }
    say(C, 'stack', SX, 3.1, .85); say(C, '只開頂端', SX, 4.2, .68, 'center', 'silkDim');
    // 水平管：長邊有護欄，兩端開口；箭頭烘在晶片上
    const tube = (z, name, ends) => {
      const x0 = -2.2, x1 = 9.2, cx = (x0 + x1) / 2, L = x1 - x0, hw = 1.3;
      [-1, 1].forEach(s => { lbox(C, cx, .1, z + s * hw, L, .14, .14, 'rail', { edge: false }); lbox(C, cx, 1.9, z + s * hw, L, .14, .14, 'rail', { edge: false }); [x0, cx, x1].forEach(px => lbox(C, px, 0, z + s * hw, .16, 2, .16, 'rail', { edge: false })); });
      say(C, name, cx, z + 2.25, .78); say(C, ends[0], x0 - .05, z + 2.25, .66, 'center', 'silkDim'); say(C, ends[1], x1 + .05, z + 2.25, .66, 'center', 'silkDim');
    };
    tube(-5, 'queue', ['← front', 'back ←']); tube(1.6, 'deque', ['↔ front', 'back ↔']);
    const ST = ['a', 'b', 'c'].map(r => DB.alloc(r)), QU = ['a', 'b', 'c'].map(r => DB.alloc(r)), DQ = ['a', 'b'].map(r => DB.alloc(r));
    const SY = i => .3 + i * LV, QX = i => -.8 + i * 2.8;     // 佇列的第 i 個（0 是 front）
    LM.linear_structures = { dur: 8, pose(u) {
      // 堆疊：依序從頂端放入 A、B、C，再依 C、B、A 從頂端取出
      ST.forEach((id, i) => {
        const inA = .06 + i * .08, outA = .36 + (2 - i) * .08;
        if (u < inA || u >= outA + .08) { DB.hide(id); return; }
        const y = u < outA ? lerp(LV * levels + 3, SY(i), seg(u, inA, inA + .07)) : lerp(SY(i), LV * levels + 3, seg(u, outA, outA + .07));
        dat(C, id, SX, y, 0, 2.4, 1.3, 2.4);
      });
      // 佇列：A、B、C 從 back 進，從 front 出，先進先出
      QU.forEach((id, i) => {
        const inA = .06 + i * .08, outA = .36 + i * .08;
        if (u < inA || u >= outA + .08) { DB.hide(id); return; }
        const shifted = Math.max(0, Math.floor(clamp01((u - .36) / .08)));
        const slot = QX(Math.max(0, i - shifted)), start = QX(i);
        let x = lerp(10.6, start, seg(u, inA, inA + .07));
        if (u >= .36) {
          const k = (u - .36) / .08, f = Math.floor(k), t = seg(k - f, 0, 1);
          if (i === f) x = lerp(QX(0), -4, t);
          else x = lerp(slot, QX(Math.max(0, i - f - 1)), t);
        }
        dat(C, id, x, .3, -5, 2.2, 1.3, 2);
      });
      // Deque：同一個結構，兩端都能進出
      DQ.forEach((id, i) => {
        const side = i === 0 ? 1 : -1, a = .66 + i * .08, o = .84 + i * .05;
        if (u < a || u >= o + .05) { DB.hide(id); return; }
        const tgt = i === 0 ? QX(2) : QX(1), edge = i === 0 ? 10.6 : -4;
        const x = u < o ? lerp(edge, tgt, seg(u, a, a + .07)) : lerp(tgt, side > 0 ? 10.6 : -4, seg(u, o, o + .05));   // 只能從自己這一端出去，不能穿過另一個元素
        dat(C, id, x, .3, 1.6, 2.2, 1.3, 2);
      });
    } };
  }

  // 06 遞迴：fact(4) 的呼叫框架。逐層疊上，到基底條件後才由上往下回傳
  {
    const C = CHIP.recursion, FX = -4, FW = 7.6, FD = 5.4, H = 1.4;
    lbox(C, FX, 0, 0, FW + 1, .25, FD + 1, 'cell');
    [[-1, -1], [1, -1], [1, 1], [-1, 1]].forEach(([a, b]) => lbox(C, FX + a * (FW / 2 + .25), 0, b * (FD / 2 + .25), .22, H * 4 + .7, .22, 'rail', { edge: false }));
    [['fact(1)', 'return 1'], ['fact(2)', 'return 2 × 1'], ['fact(3)', 'return 3 × 2'], ['fact(4)', 'return 4 × 6']].forEach(([a, b], i) => {
      say(C, a, 3.4, -5.6 + i * 2.9, .8, 'left'); say(C, b, 3.4, -4.6 + i * 2.9, .68, 'left', 'silkDim');
    });
    const P = [0, 1, 2, 3].map(i => DB.alloc(['d', 'c', 'b', 'a'][i])), flag = [DB.alloc('rail'), DB.alloc('hi')], tok = DB.alloc('hi');
    const y = i => .3 + i * H;
    LM.recursion = { dur: 6.4, pose(u) {
      P.forEach((id, i) => {
        const a = .05 + i * .09, o = .78 - i * .09;    // 最先呼叫的最後回傳
        if (u < a || u >= o + .08) { DB.hide(id); return; }
        const yy = u < o ? lerp(y(i) + 5, y(i), seg(u, a, a + .08)) : lerp(y(i), y(i) + 5, seg(u, o, o + .08));
        dat(C, id, FX, yy, 0, FW - .3, H - .14, FD - .3);
      });
      const on = u > .42 && u < .54;
      if (on) { dat(C, flag[0], FX + 2.6, y(4), 0, .22, 2.4, .22); dat(C, flag[1], FX + 3.5, y(4) + 1.5, 0, 1.6, .9, .14); }
      else { DB.hide(flag[0]); DB.hide(flag[1]); }
      if (u > .51 && u < .86) dat(C, tok, FX, lerp(y(4) + .4, y(0) + .4, seg(u, .51, .86)), FD / 2 + .9, .9, .9, .9); else DB.hide(tok);
    } };
  }

  // 07 搜尋與排序：雜湊表 m = 11，線性探查（與教材相同的一批值）；旁邊是一趟氣泡排序
  {
    const C = CHIP.searching_sorting, M_ = 11, s = 1.72, x0 = -M_ * s / 2, z0 = 3.2, sx = i => x0 + s * i + s / 2;
    for (let i = 0; i < M_; i++) { lbox(C, sx(i), 0, z0, s, .5, 2.8, i % 2 ? 'cell2' : 'cell'); say(C, String(i), sx(i), z0 + 2, .66, 'center', 'silkDim'); }
    // 漏斗：角錐倒放，分流到各 slot
    const fun = { x: 3, y: 5.6, z: -3.6 };
    const fA = C.x + fun.x, fZ = C.z + fun.z;
    parts.pyr.push({ m: new THREE.Matrix4().compose(_p.set(fA, C.T + fun.y, fZ), _q.setFromEuler(_e.set(Math.PI, 0, 0)), _s.set(3, 2.2, 3)), role: 'metal' });
    lbox(C, fun.x, 0, fun.z, .3, fun.y - 1.1, .3, 'rail', { edge: false });
    say(C, 'k mod 11', fun.x + 2.6, -2.3, .86);
    // 真的跑一次線性探查：每個值的路徑由模擬得出
    const table = new Array(M_).fill(null), KEYS = [54, 26, 93, 17, 77, 31, 44, 55], paths = [];
    KEYS.forEach(k => { let i = k % M_; const hops = [i]; while (table[i] !== null) { i = (i + 1) % M_; hops.push(i); } table[i] = k; paths.push({ k, hops, collide: hops.length > 1 }); });
    INV.searching_sorting = { m: M_, paths };
    const cubes = paths.map(p => DB.alloc(p.collide ? 'b' : 'a'));
    // 一趟氣泡排序：每次只比較相鄰兩根，真的排
    const BAR = [5, 2, 4, 1, 3], bx = i => -8.6 + i * 1.5, bz = -5.2;
    const frames = [BAR.slice()], cmpAt = [];
    { const a = BAR.slice(); for (let i = 0; i + 1 < a.length; i++) { cmpAt.push(i); if (a[i] > a[i + 1]) [a[i], a[i + 1]] = [a[i + 1], a[i]]; frames.push(a.slice()); } }
    const bars = BAR.map(() => DB.alloc('d'));
    say(C, '比較相鄰、必要時交換', -5.6, -2.9, .66, 'center', 'silkDim');
    const HASH_END = .74;
    LM.searching_sorting = { dur: 8.5, pose(u) {
      const per = HASH_END / paths.length;
      paths.forEach((p, i) => {
        const a = i * per, b = a + per;
        if (u < a || u >= .985) { DB.hide(cubes[i]); return; }
        const t = clamp01((u - a) / (b - a)), fall = seg(t, 0, .55), slide = seg(t, .55, 1);
        const land = sx(p.hops[0]), fin = sx(p.hops[p.hops.length - 1]);
        const x = fall < 1 ? lerp(fun.x, land, fall) : lerp(land, fin, slide);
        const y = fall < 1 ? lerp(fun.y - 1, .5, fall) : .5;
        const z = fall < 1 ? lerp(fun.z, z0, fall) : z0;
        dat(C, cubes[i], x, y, z, 1.3, 1.1, 1.8);
      });
      const v = clamp01((u - HASH_END) / (1 - HASH_END - .02)), n = frames.length - 1, f = Math.min(n, Math.floor(v * n));
      frames[f].forEach((h, i) => { DB.role(bars[i], (f < n && u > HASH_END && (i === cmpAt[f] || i === cmpAt[f] + 1)) ? 'hi' : 'd'); dat(C, bars[i], bx(i), 0, bz, 1.2, h * .75, 1.2); });
    } };
  }

  // 08 圖：不規則頂點、含環、帶權邊；BFS 逐層染色（層數真的由 BFS 算出），已訪問的不重複。旁邊是相鄰矩陣
  {
    const C = CHIP.graphs, G = DATA.graph, Vs = G.vertices, names = Object.keys(Vs), adj = graphAdj();
    const level = { [G.start]: 0 }, q = [G.start];
    while (q.length) { const u = q.shift(); adj[u].forEach(w => { if (level[w] === undefined) { level[w] = level[u] + 1; q.push(w); } }); }
    const maxL = Math.max(...Object.values(level));
    INV.graphs = { level, edges: G.edges, adj };
    const WEIGHT = { 'A-B': 7, 'A-C': 5, 'B-D': 2, 'C-D': 3, 'B-E': 4, 'D-G': 6, 'C-F': 8, 'F-G': 1, 'E-G': 9 };
    G.edges.forEach(([a, b]) => {
      beam(LP(C, Vs[a][0], .25, Vs[a][1]), LP(C, Vs[b][0], .25, Vs[b][1]), .22, .1, 'rail');
      say(C, String(WEIGHT[a + '-' + b]), (Vs[a][0] + Vs[b][0]) / 2 + .35, (Vs[a][1] + Vs[b][1]) / 2 - .35, .62, 'center', 'silkDim');
    });
    const pil = names.map(n => { say(C, n, Vs[n][0], Vs[n][1] + 1.3, .74); return DB.alloc('node'); });
    // 相鄰矩陣：與圖對稱一致
    const mx = 5.6, mz = -3.6, ms = .62, mat = [];
    names.forEach((a, i) => { names.forEach((b, j) => { const on = adj[a].includes(b); mat.push({ i, j, on }); }); say(C, a, mx - .42, mz + i * ms + .3, .46, 'center', 'silkDim'); say(C, a, mx + i * ms + .3, mz - .42, .46, 'center', 'silkDim'); });
    C.matrix = { mx, mz, ms, cells: mat };
    say(C, '相鄰矩陣', mx + 2.2, mz + 5.4, .62, 'center', 'silkDim');
    LM.graphs = { dur: 5.5, pose(u) {
      const now = u <= 0 ? -1 : Math.floor(clamp01((u - .04) / .78) * (maxL + 1));
      names.forEach((n, i) => {
        const l = level[n], reached = u < .985 && l <= now, cur = reached && l === now;
        DB.role(pil[i], cur ? 'hi' : reached ? 'c' : 'node');
        dat(C, pil[i], Vs[n][0], .1, Vs[n][1], 1.5, cur ? 2.4 : 1.6, 1.5);
      });
    } };
  }

  // 09 樹：根在最上面（依序插入 70、31、93、94、14、23、73）。插入 40：從根開始比較，走到空位
  {
    const C = CHIP.trees, KEYS = [70, 31, 93, 94, 14, 23, 73], INS = 40, root = { k: KEYS[0] };
    const put = (n, k) => { const s = k < n.k ? 'l' : 'r'; if (n[s]) put(n[s], k); else n[s] = { k }; };
    KEYS.slice(1).forEach(k => put(root, k));
    // 插入 40 的路徑（連同新節點一起排版，位置才留得出來）
    const path = []; { let n = root; for (;;) { path.push(n); const s = INS < n.k ? 'l' : 'r'; if (!n[s]) { n[s] = { k: INS, fresh: true }; path.push(n[s]); break; } n = n[s]; } }
    const flat = []; const walk = (n, d) => { if (!n) return; walk(n.l, d + 1); n.d = d; n.i = flat.length; flat.push(n); walk(n.r, d + 1); }; walk(root, 0);
    const X = n => -8.75 + n.i * 2.5, Y = n => 5.3 - n.d * 1.75;
    INV.trees = { rootY: Y(root), leafY: flat.filter(n => !n.l && !n.r).map(Y), path: path.map(n => n.k), parentOfNew: path[path.length - 2].k, side: INS < path[path.length - 2].k ? 'l' : 'r' };
    lbox(C, X(root), 0, -2.6, .34, Y(root) + .6, .34, 'rail', { edge: false });
    lbox(C, X(root), Y(root) + .6, -1.3, .34, .34, 2.9, 'rail', { edge: false });
    flat.forEach(n => { [n.l, n.r].forEach(c => { if (c && !c.fresh) beam(LP(C, X(n), Y(n) + .1, 0), LP(C, X(c), Y(c) + 1.2, 0), .2, .2, 'rail'); }); });
    flat.forEach(n => { if (n.fresh) return; n.id = DB.alloc('node'); dat(C, n.id, X(n), Y(n), 0, 1.7, 1.3, 1.7); say(C, String(n.k), X(n), 2.6, .68, 'center', 'silkDim'); });
    say(C, '左小右大', -6.5, 5.6, .78); say(C, '← 比較走過的層數就是比較次數', 2.7, 5.6, .66, 'center', 'silkDim');
    const fresh = path[path.length - 1], parent = path[path.length - 2], ball = DB.alloc('c'), link = DB.alloc('c');
    const hops = path.length - 1;
    LM.trees = { dur: 6.2, pose(u) {
      const v = clamp01((u - .05) / .72), f = v * hops, k = Math.min(hops - 1, Math.floor(f)), t = seg(f - k, 0, 1);
      path.forEach((n, i) => { if (n.id !== undefined) DB.role(n.id, u > .03 && u < .985 && i === (f >= hops ? -1 : k) ? 'hi' : 'node'); });
      if (u > .03 && u < .985) {
        const a = path[k], b = path[k + 1], lift = 1.7;
        const x = lerp(X(a), X(b), t), y = lerp(Y(a) + lift, Y(b) + lift, t);
        const land = u > .78 ? seg(u, .78, .86) : 0;
        dat(C, ball, x, f >= hops ? lerp(Y(fresh) + lift, Y(fresh), land) : y, 0, 1.5, 1.3, 1.5);
        if (land > 0) DB.beam(link, LP(C, X(parent), Y(parent) + .1, 0), LP(C, X(fresh), Y(fresh) + 1.2, 0), .2, .2); else DB.hide(link);
      } else { DB.hide(ball); DB.hide(link); }
    } };
  }

  /* 課前與先備：靜態地標 */
  {
    const A = CHIP['00a_why_code'], B = CHIP['00b_setup'], P = CHIP['00c_vscode_windows'];
    // 電源開關：底座＋斜撥桿
    lbox(A, 6, 0, 0, 5.6, .8, 3.6, 'cell');
    beam(LP(A, 6, .8, 0), LP(A, 7.8, 3, 0), .9, .9, 'metal');
    lbox(A, 7.8, 2.8, 0, 1.2, .8, 1.2, 'a');
    lbox(A, 2, 0, 0, .9, .5, .9, 'hi');
    // 連接埠：金屬外殼＋一排針腳
    lbox(B, 5.4, 0, 0, 7.6, 2, 3.4, 'metal');
    lbox(B, 5.4, 2, 0, 6.4, .12, 2, 'ink', { edge: false });
    for (let i = 0; i < 7; i++) lbox(B, 2.6 + i * .94, 2.12, 0, .36, .1, 1.4, 'pin', { edge: false });
    // 除錯探針：兩支立柱與一根斜探針，尖端紅色
    lbox(P, 3, 0, 0, 1.4, 3.2, 1.4, 'metal');
    beam(LP(P, 3, 3, 0), LP(P, 8.2, .7, 0), .4, .4, 'rail');
    parts.pyr.push({ m: new THREE.Matrix4().compose(_p.set(P.x + 8.5, P.T + .5, P.z), _q.setFromUnitVectors(_UY, V(.8, -.6, 0).normalize()), _s.set(.6, 1, .6)), role: 'b' });
    lbox(P, 8.6, 0, 0, 2, .16, 2, 'a', { edge: false });
    say(A, '為什麼要學', -3.8, 1.8, .92); say(B, '裝好工具', -3.8, 1.8, .92); say(P, '會設中斷點', -3.8, 1.8, .92);
  }

  /* ── 靜態零件合併 ── */
  const statics = Object.entries(parts).map(([k, list]) => {
    const mesh = new THREE.InstancedMesh(GEO[k], solid, list.length);
    mesh.frustumCulled = false;
    list.forEach((r, i) => mesh.setMatrixAt(i, r.m));
    world.add(mesh);
    return { mesh, list };
  });
  function recolorStatic() {
    statics.forEach(({ mesh, list }) => { list.forEach((r, i) => mesh.setColorAt(i, ROLE[r.role])); mesh.instanceColor.needsUpdate = true; });
    DB.recolor(); DP.recolor();
  }
  const edgeGeo = new THREE.BufferGeometry();
  edgeGeo.setAttribute('position', new THREE.Float32BufferAttribute(edgePos, 3));
  const edgeMat = new THREE.LineBasicMaterial({ color: PAL.power.line });
  const edges = new THREE.LineSegments(edgeGeo, edgeMat);
  edges.frustumCulled = false;
  world.add(edges);

  /* ── 匯流排的光暈（只有通電時）：半透明加色，一次畫完 ── */
  const haloMat = new THREE.MeshBasicMaterial({ color: PAL.power.halo, transparent: true, opacity: .2, blending: THREE.AdditiveBlending, depthWrite: false });
  const halo = new THREE.InstancedMesh(new THREE.PlaneGeometry(1, 1).rotateX(-Math.PI / 2), haloMat, haloParts.length);
  haloParts.forEach(([x, z, sx, sz], i) => halo.setMatrixAt(i, _m.compose(_p.set(x, .23, z), _q.identity(), _s.set(sx, 1, sz))));
  halo.frustumCulled = false;
  world.add(halo);

  /* ── 匯流排上的脈衝：表示授課方向 ── */
  const busLen = []; let busTotal = 0;
  for (let i = 0; i < BUS.length - 1; i++) { const l = Math.abs(BUS[i + 1][0] - BUS[i][0]) + Math.abs(BUS[i + 1][1] - BUS[i][1]); busLen.push(l); busTotal += l; }
  const pulseIds = Array.from({ length: 9 }, () => DB.alloc('val'));
  function busAt(d) {
    d = ((d % busTotal) + busTotal) % busTotal;
    for (let i = 0; i < busLen.length; i++) {
      if (d <= busLen[i]) { const t = d / busLen[i]; return [lerp(BUS[i][0], BUS[i + 1][0], t), lerp(BUS[i][1], BUS[i + 1][1], t)]; }
      d -= busLen[i];
    }
    return BUS[0];
  }
  function stepPulses(t) {
    pulseIds.forEach((id, i) => {
      if (modeTarget === 1) { DB.hide(id); return; }
      const [x, z] = busAt(t * 7 + i * busTotal / pulseIds.length);
      DB.at(id, x, .22, z, .95, .2, .95);
    });
  }

  /* ── 絲印圖集與底板貼圖：兩種模式各畫一份，第二份用到才畫 ── */
  const MONO = "600 %px ui-monospace,'SFMono-Regular','Cascadia Mono',Menlo,Consolas,'Noto Sans CJK TC','Microsoft JhengHei',monospace";
  function makeAtlas(mode) {
    const pal = PAL[mode], cv = document.createElement('canvas');
    cv.width = cv.height = 2048;
    const g = cv.getContext('2d');
    g.fillStyle = pal.die; g.fillRect(0, 0, 2048, 2048);
    g.textBaseline = 'middle';
    Object.values(CHIP).forEach(C => {
      const r = C.atlas, dw = C.w - 2, dh = C.d - 2, sx = r.w / dw, sy = r.h / dh;
      const X = lx => r.x + (lx + dw / 2) * sx, Y = lz => r.y + (lz + dh / 2) * sy;
      g.save();
      g.beginPath(); g.rect(r.x, r.y, r.w, r.h); g.clip();
      g.strokeStyle = pal.silkDim; g.lineWidth = 2; g.strokeRect(r.x + 7, r.y + 7, r.w - 14, r.h - 14);
      if (C.w > 12) {
        g.fillStyle = pal.silkDim; g.textAlign = 'right';
        g.font = MONO.replace('%', 22); g.fillText(C.addr, r.x + r.w - 14, r.y + 24);
        g.textAlign = 'left'; g.font = MONO.replace('%', 26); g.fillText(C.code, r.x + 14, r.y + 24);
      } else {
        g.fillStyle = pal.silk; g.textAlign = 'center'; g.font = MONO.replace('%', 50); g.fillText(C.code, r.x + r.w / 2, r.y + r.h / 2);
      }
      if (C.matrix) {
        const m = C.matrix;
        m.cells.forEach(c => {
          g.fillStyle = c.on ? pal.silk : pal.cell2;
          g.fillRect(X(m.mx + c.j * m.ms) + 1, Y(m.mz + c.i * m.ms) + 1, m.ms * sx - 2, m.ms * sy - 2);
        });
      }
      C.bake.forEach(b => {
        g.fillStyle = pal[b.role]; g.textAlign = b.align;
        g.font = MONO.replace('%', Math.round(b.size * SC));
        g.fillText(b.text, X(b.lx), Y(b.lz));
      });
      g.restore();
    });
    const t = new THREE.CanvasTexture(cv);
    t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy());
    return t;
  }
  function makeBoard(mode) {
    const pal = PAL[mode], cv = document.createElement('canvas'), S = 18;
    cv.width = 86 * S; cv.height = 114 * S;
    const g = cv.getContext('2d');
    g.fillStyle = pal.board; g.fillRect(0, 0, cv.width, cv.height);
    g.strokeStyle = pal.dim; g.globalAlpha = mode === 'power' ? .28 : .5; g.lineWidth = 1;
    for (let x = 0; x <= 86; x += 5) { g.beginPath(); g.moveTo(x * S, 0); g.lineTo(x * S, cv.height); g.stroke(); }
    for (let z = 0; z <= 114; z += 5) { g.beginPath(); g.moveTo(0, z * S); g.lineTo(cv.width, z * S); g.stroke(); }
    g.globalAlpha = 1; g.fillStyle = pal.silkDim; g.font = MONO.replace('%', 15); g.textBaseline = 'middle';
    for (let x = 5; x < 86; x += 20) { g.textAlign = 'left'; g.fillText('0x' + (x * 16).toString(16).toUpperCase().padStart(3, '0'), x * S + 4, 14); g.fillText('0x' + (x * 16).toString(16).toUpperCase().padStart(3, '0'), x * S + 4, cv.height - 14); }
    for (let z = 5; z < 114; z += 15) { g.textAlign = 'left'; g.fillText('0x' + (z * 256).toString(16).toUpperCase().padStart(4, '0'), 6, z * S - 10); }
    const t = new THREE.CanvasTexture(cv);
    t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy());
    return t;
  }
  const atlases = {}, boards = {};
  const atlasOf = m => (atlases[m] = atlases[m] || makeAtlas(m));
  const boardOf = m => (boards[m] = boards[m] || makeBoard(m));
  const dieMat = new THREE.MeshBasicMaterial({ map: atlasOf('power') });
  {
    const pos = [], uv = [], idx = []; let n = 0;
    Object.values(CHIP).forEach(C => {
      const r = C.atlas, dw = C.w - 2, dh = C.d - 2, y = T + .012;
      const x0 = C.x - dw / 2, x1 = C.x + dw / 2, z0 = C.z - dh / 2, z1 = C.z + dh / 2;
      const u0 = r.x / 2048, u1 = (r.x + r.w) / 2048, v0 = 1 - r.y / 2048, v1 = 1 - (r.y + r.h) / 2048;
      pos.push(x0, y, z0, x1, y, z0, x1, y, z1, x0, y, z1);
      uv.push(u0, v0, u1, v0, u1, v1, u0, v1);
      idx.push(n, n + 2, n + 1, n, n + 3, n + 2); n += 4;
    });
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
    g.setIndex(idx);
    const mesh = new THREE.Mesh(g, dieMat); mesh.frustumCulled = false; world.add(mesh);
  }
  const boardMat = new THREE.MeshBasicMaterial({ map: boardOf('power') });
  {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(86, 114).rotateX(-Math.PI / 2), boardMat);
    m.position.y = .005; world.add(m);
  }

  /* ── 選取框、先備連線（綠色，和金色匯流排、紅色指標都不同）── */
  const brackets = Array.from({ length: 8 }, () => DB.alloc('sel'));
  function setBrackets(C) {
    if (!C) { brackets.forEach(id => DB.hide(id)); return; }
    const hx = C.w / 2 + 1.3, hz = C.d / 2 + 1.3, L = Math.min(4, C.w * .3), th = .3, y = .12, h = .9;
    [[-1, -1], [1, -1], [1, 1], [-1, 1]].forEach(([a, b], i) => {
      DB.at(brackets[i * 2], C.x + a * (hx - L / 2), y, C.z + b * hz, L, h, th);
      DB.at(brackets[i * 2 + 1], C.x + a * hx, y, C.z + b * (hz - L / 2), th, h, L);
    });
  }
  const wires = Array.from({ length: 16 }, () => DB.alloc('wire'));
  function setWires(C, refs) {
    wires.forEach(id => DB.hide(id));
    if (!C || !refs.length) return;
    let w = 0;
    const seg2 = (x0, z0, x1, z1) => {
      const cx = (x0 + x1) / 2, cz = (z0 + z1) / 2;
      DB.at(wires[w++], cx, .55, cz, Math.abs(x1 - x0) + .4, .22, Math.abs(z1 - z0) + .4);
    };
    refs.forEach((r, i) => {
      const P = CHIP[r]; if (!P) return;
      const offs = i * .8, laneX = (C.x < 0 ? -13.5 : C.x > 0 ? 13.5 : (P.x < 0 ? -13.5 : 13.5)) + (offs - .8);
      const laneZ = 36.5 + (offs - .8), gapZ = C.z + C.d / 2 + 3.5 + (offs - .8), cx = C.x + (i - 1) * 3;
      seg2(cx, C.z + C.d / 2, cx, gapZ);
      seg2(cx, gapZ, laneX, gapZ);
      seg2(laneX, gapZ, laneX, laneZ);
      seg2(laneX, laneZ, P.x, laneZ);
      seg2(P.x, laneZ, P.x, P.z - P.d / 2);
    });
  }

  /* ── 嚮導阿迭（迭代器）：不帶任何東西，只指向。沿直角路徑走，不跳躍 ── */
  const gParts = { body: DB.alloc('val'), face: DB.alloc('ink'), eye: DB.alloc('hi'), shaft: DB.alloc('hi'), base: DB.alloc('next') };
  const gHead = DP.alloc('hi');
  const guide = V(0, 0, 0);
  function placeGuide(x, y, z) {
    guide.set(x, y, z);
    DB.at(gParts.base, x, y, z, 2.2, .4, 1.8);
    DB.at(gParts.body, x, y + .4, z, 1.8, 1.9, 1.5);
    DB.at(gParts.face, x, y + 1, z + .77, 1.3, .8, .06);
    DB.at(gParts.eye, x + .25, y + 1.15, z + .82, .46, .46, .08);
    DB.at(gParts.shaft, x - .1, y + 2.5, z, 1.7, .4, .4);
    _m.compose(_p.set(x + 1.1, y + 2.7, z), _q.setFromUnitVectors(_UY, V(1, 0, 0)), _s.set(1.15, 1.05, 1.15));
    DP.mesh.setMatrixAt(gHead, _m); DP.mesh.instanceMatrix.needsUpdate = true;
  }
  const guideSpot = stem => {
    const C = CHIP[stem];
    if (C.grp === 'dimm' || C.w < 12) return [C.x - 1, T, C.z - 1];
    return [C.x - C.w / 2 - 2.6, .1, C.z + (C.d > 10 ? C.d / 2 - 3 : 0)];
  };
  { const [x, y, z] = guideSpot(POWER[0]); placeGuide(x, y, z); }
  let walk = null;
  function guideGo(x, y, z) {
    if (!motion()) { placeGuide(x, y, z); requestRender(); return; }
    walk = { x0: guide.x, y0: guide.y, z0: guide.z, x1: x, y1: y, z1: z, t0: performance.now() };
    requestRender();
  }
  function stepGuide(now) {
    if (!walk) return false;
    const u = clamp01((now - walk.t0) / 950), a = seg(u, 0, .5), b = seg(u, .5, 1);
    placeGuide(lerp(walk.x0, walk.x1, a), lerp(walk.y0, walk.y1, seg(u, .4, .6)), lerp(walk.z0, walk.z1, b));
    if (u >= 1) walk = null;
    return true;
  }

  /* ═════════ 鏡頭與操作 ═════════ */
  const AZ0 = -26 * Math.PI / 180, POL0 = 50 * Math.PI / 180, DIST = 220;
  const camera = new THREE.OrthographicCamera(-50, 50, 50, -50, 1, 600);
  const HOME = V(0, 0, 1);
  const setHomePos = () => {
    camera.position.set(HOME.x + DIST * Math.sin(POL0) * Math.sin(AZ0), HOME.y + DIST * Math.cos(POL0), HOME.z + DIST * Math.sin(POL0) * Math.cos(AZ0));
    camera.up.set(0, 1, 0); camera.lookAt(HOME);
  };
  setHomePos();
  const controls = new OrbitControls(camera, canvas);
  controls.target.copy(HOME);
  controls.minAzimuthAngle = AZ0 - .62; controls.maxAzimuthAngle = AZ0 + .62;
  controls.minPolarAngle = 34 * Math.PI / 180; controls.maxPolarAngle = 62 * Math.PI / 180;
  controls.minZoom = .8; controls.maxZoom = 6;
  controls.enableDamping = motion(); controls.dampingFactor = .1;
  controls.rotateSpeed = .5; controls.zoomSpeed = 1.1; controls.screenSpacePanning = false;
  controls.touches = { ONE: THREE.TOUCH.PAN, TWO: THREE.TOUCH.DOLLY_ROTATE };
  controls.update();

  function fitHeight() {
    camera.updateMatrixWorld();
    const R = new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 0), U = new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 1);
    let rx = 0, ry = 0;
    [-1, 1].forEach(a => [-1, 1].forEach(b => [-2.4, 4].forEach(y => {
      const p = V(a * 43, y, b * 57).sub(controls.target);
      rx = Math.max(rx, Math.abs(p.dot(R))); ry = Math.max(ry, Math.abs(p.dot(U)));
    })));
    return { rx, ry };
  }
  const HOMEFIT = fitHeight();
  function resize() {
    const w = stage.clientWidth, h = stage.clientHeight;
    if (!w || !h) return;
    const aspect = w / h, hh = Math.max(HOMEFIT.ry * 1.02, HOMEFIT.rx * 1.02 / aspect);
    camera.top = hh; camera.bottom = -hh; camera.left = -hh * aspect; camera.right = hh * aspect;
    camera.updateProjectionMatrix();
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, DPRS[dprLevel]));
    renderer.setSize(w, h, false);
    tagsDirty = true; requestRender();
  }

  let fly = null;
  function flyTo(target, zoom) {
    if (!motion()) {
      const off = camera.position.clone().sub(controls.target);
      controls.target.copy(target); camera.position.copy(target).add(off);
      camera.zoom = zoom; camera.updateProjectionMatrix(); controls.update(); requestRender(); return;
    }
    fly = { from: controls.target.clone(), to: target.clone(), z0: camera.zoom, z1: zoom, t0: performance.now(), dur: 750 };
    requestRender();
  }
  function stepFly(now) {
    if (!fly) return false;
    const u = clamp01((now - fly.t0) / fly.dur), e = u * u * (3 - 2 * u);
    const off = camera.position.clone().sub(controls.target);
    controls.target.lerpVectors(fly.from, fly.to, e); camera.position.copy(controls.target).add(off);
    camera.zoom = lerp(fly.z0, fly.z1, e); camera.updateProjectionMatrix();
    if (u >= 1) fly = null;
    return true;
  }
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2(), v3 = V(0, 0, 0);
  const BOXES = Object.values(CHIP).map(C => ({ stem: C.stem, box: new THREE.Box3(V(C.x - C.w / 2 - .6, 0, C.z - C.d / 2 - .6), V(C.x + C.w / 2 + .6, C.w > 12 ? T + 1.5 : T + .4, C.z + C.d / 2 + .6)) }));
  function pickAt(cx, cy) {
    const r = canvas.getBoundingClientRect();
    ndc.set((cx - r.left) / r.width * 2 - 1, -(cy - r.top) / r.height * 2 + 1);
    ray.setFromCamera(ndc, camera);
    let best = null, bd = Infinity;
    BOXES.forEach(b => { const hit = ray.ray.intersectBox(b.box, v3); if (hit) { const d = hit.distanceTo(ray.ray.origin); if (d < bd) { bd = d; best = b.stem; } } });
    return best;
  }
  let hover = null, selected = null, down = null;
  function setHover(s) {
    if (s === hover) return;
    hover = s;
    canvas.classList.toggle('is-hover', !!s);
    tags.forEach(T_ => T_.el.classList.toggle('is-hover', !!T_.stem && T_.stem === s));
    tagsDirty = true; requestRender();
  }
  function scrollListTo(stem) {
    const li = document.querySelector(`.isl-item[data-stem="${stem}"]`), list = $('islList');
    if (!li || !list || narrow()) return;
    const a = li.getBoundingClientRect(), b = list.getBoundingClientRect();
    if (a.top < b.top || a.bottom > b.bottom) list.scrollTop += a.top - b.top - b.height / 2 + a.height / 2;
  }
  canvas.addEventListener('pointerdown', e => { down = { x: e.clientX, y: e.clientY }; });
  canvas.addEventListener('pointermove', e => { if (e.pointerType === 'mouse' && !e.buttons) setHover(pickAt(e.clientX, e.clientY)); });
  canvas.addEventListener('pointerleave', () => setHover(null));
  canvas.addEventListener('pointerup', e => {
    if (!down || Math.hypot(e.clientX - down.x, e.clientY - down.y) > 6) return;
    const s = pickAt(e.clientX, e.clientY);
    if (s) { select(s, { trigger: canvas, fly: true }); scrollListTo(s); }
  });
  canvas.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
      const off = camera.position.clone().sub(controls.target);
      const az = Math.atan2(off.x, off.z) + (e.key === 'ArrowLeft' ? -.08 : .08);
      const clampAz = Math.max(controls.minAzimuthAngle, Math.min(controls.maxAzimuthAngle, az));
      off.applyAxisAngle(_UY, clampAz - Math.atan2(off.x, off.z));
      camera.position.copy(controls.target).add(off); controls.update(); requestRender(); e.preventDefault();
    } else if (e.key === '+' || e.key === '=' || e.key === '-') {
      camera.zoom = Math.min(controls.maxZoom, Math.max(controls.minZoom, camera.zoom * (e.key === '-' ? 1 / 1.2 : 1.2)));
      camera.updateProjectionMatrix(); tagsDirty = true; requestRender(); e.preventDefault();
    }
  });
  // 平移不能把底板拖出畫面
  const clampTarget = () => {
    const t = controls.target, cx = Math.max(-40, Math.min(40, t.x)), cz = Math.max(-52, Math.min(52, t.z));
    if (cx !== t.x || cz !== t.z) { const dx = cx - t.x, dz = cz - t.z; t.x = cx; t.z = cz; camera.position.x += dx; camera.position.z += dz; }
  };
  controls.addEventListener('change', () => { clampTarget(); tagsDirty = true; requestRender(); });

  /* ═════════ 標籤層（HTML）：貼在晶片前緣，像絲印的牌子 ═════════ */
  const layer = $('islLabels');
  const tags = [];
  const UNIT_ZOOM = 1.7;
  function addTag({ stem = null, grp, kind, text, code, anchor, prio }) {
    const el = document.createElement('button');
    el.type = 'button'; el.className = `isl-tag isl-tag-${kind}`; el.tabIndex = -1; el.setAttribute('aria-hidden', 'true');
    if (code) { const n = document.createElement('span'); n.className = 'isl-tag-num'; n.textContent = code; el.appendChild(n); }
    const t = document.createElement('span'); t.className = 'isl-tag-t'; t.textContent = text; el.appendChild(t);
    el.addEventListener('click', () => {
      if (stem) { select(stem, { trigger: canvas, fly: true }); scrollListTo(stem); } else flyToIsle(grp);
    });
    layer.appendChild(el);
    tags.push({ el, stem, grp, kind, anchor, prio, w: 0, h: 0, cw: 0, num: el.querySelector('.isl-tag-num') });
  }
  PAGES.forEach(p => {
    const C = CHIP[p.stem];
    addTag({ stem: p.stem, grp: p.grp, kind: p.grp === 'core' ? 'core' : p.grp === 'power' ? 'pre' : 'unit', text: p.title, code: p.code,
      anchor: V(C.x, 0, C.z + C.d / 2 + (p.grp === 'dimm' ? 4.4 : .9)), prio: p.grp === 'core' ? 1 : p.grp === 'power' ? 2 : 3 });
  });
  function measureTags() {
    tags.forEach(T_ => {
      T_.el.classList.remove('is-compact'); T_.st = -1; T_.w = T_.el.offsetWidth; T_.h = T_.el.offsetHeight;
      T_.cw = T_.num ? T_.num.offsetWidth + 8 : T_.w;
    });
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { measureTags(); tagsDirty = true; requestRender(); });
  const placed = [];
  let refs = [];
  function placeTags() {
    const W_ = canvas.clientWidth, H_ = canvas.clientHeight, zoomed = camera.zoom >= UNIT_ZOOM;
    placed.length = 0;
    const sel = T_ => (!!T_.stem && T_.stem === selected ? 0 : 1);
    const order = tags.slice().sort((a, b) => sel(a) - sel(b) || a.prio - b.prio);
    order.forEach(T_ => {
      const isSel = !!T_.stem && T_.stem === selected, isRef = !!T_.stem && refs.includes(T_.stem), isHov = T_.stem === hover;
      v3.copy(T_.anchor).project(camera);
      const x = (v3.x + 1) / 2 * W_, y = (1 - v3.y) / 2 * H_;
      const hits = r => placed.some(q => !(r.r < q.l || r.l > q.r || r.b < q.t || r.t > q.b));
      const bx = w => ({ l: x - w / 2 - 3, r: x + w / 2 + 3, t: y, b: y + T_.h + 3 });
      // 先備顆粒預設只顯示編號；放大、選取或滑過才展開。手機上正課也一樣
      let compact = (T_.kind === 'unit' && !zoomed && !isSel && !isRef && !isHov) || (narrow() && !isSel && !isHov && !zoomed);
      let r = bx(compact ? T_.cw : T_.w), show = true;
      if (r.l < 2 || r.r > W_ - 2 || r.t < 0 || r.b > H_) {
        if (compact || !T_.num) show = false;
        else { compact = true; r = bx(T_.cw); if (r.l < 2 || r.r > W_ - 2 || r.t < 0 || r.b > H_) show = false; }
      }
      if (show && !isSel && hits(r) && !compact) {
        if (T_.num && !hits(bx(T_.cw))) { compact = true; r = bx(T_.cw); } else show = false;
      }
      if (show) placed.push(r);
      const st = show ? (compact ? 2 : 1) : 0;
      if (st !== T_.st) { T_.el.classList.toggle('is-off', !show); T_.el.classList.toggle('is-compact', st === 2); T_.st = st; }
      if (show) {
        const tf = `translate(${Math.round(x)}px, ${Math.round(y)}px) translate(-50%, 0)`;
        if (tf !== T_.tf) { T_.el.style.transform = tf; T_.tf = tf; }
      }
    });
  }

  /* ═════════ 地標播放與模式 ═════════ */
  const playing = new Map();     // stem → 開始時間
  function playLM(stem) {
    if (!LM[stem] || !motion()) return;
    playing.set(stem, performance.now());
    wake(); requestRender();
  }
  function stepPlays(now) {
    if (!playing.size) return false;
    playing.forEach((t0, stem) => {
      const u = (now - t0) / (LM[stem].dur * 1000);
      if (u >= 1) { LM[stem].pose(0); playing.delete(stem); } else LM[stem].pose(u);
    });
    return true;
  }
  // 沒有選取時，島上輪流跑一座地標，讓畫面活著；剛選到、還沒猜的那一座不放，避免先看到答案
  let attractAt = 0, attractI = 0;
  function stepAttract(now) {
    if (modeTarget === 1 || playing.size || selected || lowPower) return;
    if (now < attractAt) return;
    attractAt = now + 9000;
    if (attractI > 0 || now > 3500) playLM(CORE[attractI++ % CORE.length]);
  }
  function applyMode(k) {
    modeK = k;
    mixRoles(k);
    recolorStatic();
    world.background.copy(ROLE.bg);
    edgeMat.color.copy(ROLE.line);
    halo.visible = k < .5;
    const m = k < .5 ? 'power' : 'print';
    if (dieMat.map !== atlasOf(m)) { dieMat.map = atlasOf(m); dieMat.needsUpdate = true; }
    if (boardMat.map !== boardOf(m)) { boardMat.map = boardOf(m); boardMat.needsUpdate = true; }
  }
  applyMode(0);
  Object.values(LM).forEach(l => l.pose(0));

  /* ═════════ 繪製迴圈 ═════════
     - 互動（拖曳、縮放、飛行、模式過渡、地標播放）時全速；只剩脈衝時每 33 ms 才畫一幀；藍圖模式靜止時完全不畫
     - 閒置 45 秒（沒有任何 pointer／wheel／key／touch）就停止動畫，有輸入立即恢復
     - 解析度自動調整：最近 2 秒偏慢就降一級 DPR；互動時連續夠快再升回 */
  const DPRS = narrow() ? [1.25, 1] : [1.5, 1.25, 1];
  const IDLE_MS = () => window.__islandIdleMs || 45000;
  let last = performance.now(), lastDraw = 0, lastInput = performance.now(), sampleT = 0, sampleN = 0, fastWin = 0;
  const idle = () => performance.now() - lastInput > IDLE_MS();
  const animating = () => motion() && onScreen && document.visibilityState === 'visible' && !idle();
  function wake() { const was = idle(); lastInput = performance.now(); if (was) requestRender(); }
  ['pointerdown', 'pointermove', 'wheel', 'keydown', 'touchstart'].forEach(ev => window.addEventListener(ev, wake, { passive: true }));
  function setDprLevel(k) { dprLevel = Math.max(0, Math.min(DPRS.length - 1, k)); resize(); }
  // 任何時候最多只有一個待執行的 frame（raf 非 0 就表示已排程）
  function requestRender() { need = true; if (!raf && alive) raf = requestAnimationFrame(frame); }
  function frame(now) {
    raf = 0; if (!alive) return;
    const dt = Math.min(.1, (now - last) / 1000); last = now;
    const flying = stepFly(now), walking = stepGuide(now), moved = controls.update(), anim = animating();
    let fading = false;
    if (modeK !== modeTarget) {
      const k = motion() ? (modeTarget > modeK ? Math.min(modeTarget, modeK + dt / .45) : Math.max(modeTarget, modeK - dt / .45)) : modeTarget;
      applyMode(k); fading = true;
    }
    const ambient = anim && modeTarget === 0 && !lowPower;
    const playingNow = anim && playing.size > 0;
    const busy = need || flying || walking || moved || fading || playingNow;
    // 只有環境動畫時限制在約 30fps
    if (!busy && ambient && now - lastDraw < 32) { if (!raf) raf = requestAnimationFrame(frame); return; }
    if (anim) {
      stepPlays(now);
      stepAttract(now);
      if (ambient || modeTarget === 1) stepPulses(now / 1000);
    }
    if (busy || ambient) {
      if (lastDraw) {
        const gap = now - lastDraw;
        if (gap < 250) { sampleT += gap; sampleN++; }
        if (sampleT > 2000) {
          const avg = sampleT / sampleN, target = busy ? 22 : 40;
          if (avg > target * 1.6) { if (dprLevel < DPRS.length - 1) setDprLevel(dprLevel + 1); else if (!lowPower) lowPower = true; fastWin = 0; }
          else if (busy && avg < 19 && dprLevel > 0 && ++fastWin >= 3) { setDprLevel(dprLevel - 1); fastWin = 0; }
          sampleT = 0; sampleN = 0;
        }
      }
      renderer.render(world, camera); lastDraw = now; draws++;
      if (tagsDirty || flying || moved) { placeTags(); tagsDirty = false; }
      need = false;
    }
    // 只排一次：controls.update() 會觸發 change → requestRender() 已經排了下一幀，不能再多排一條迴圈
    if ((ambient || flying || walking || moved || fading || playingNow) && !raf) raf = requestAnimationFrame(frame);
  }
  const ro = new ResizeObserver(resize); ro.observe(stage);
  new IntersectionObserver(es => { onScreen = es[0].isIntersecting; requestRender(); }).observe(stage);
  document.addEventListener('visibilitychange', requestRender);
  reduceMotion.addEventListener('change', () => { controls.enableDamping = motion(); requestRender(); });
  stepPulses(1.7);
  resize();
  measureTags();

  function flyToIsle(grp) {
    if (grp === 'core') flyTo(V(0, 0, 0), 1.25);
    else if (grp === 'power') flyTo(V(0, 0, ROWP), 1.8);
    else flyTo(V(0, 0, DIMMZ + 2), 1.8);
  }

  /* ═════════ 對外介面 ═════════ */
  return {
    select(stem, doFly) {
      selected = stem && CHIP[stem] ? stem : null;
      refs = selected ? BY[selected].refs.filter(r => CHIP[r]) : [];
      const C = selected ? CHIP[selected] : null;
      setBrackets(C); setWires(C, refs);
      if (selected && playing.has(selected)) { playing.delete(selected); LM[selected].pose(0); }   // 剛選到的島先回到靜止，答案不提早露出
      tags.forEach(T_ => { T_.el.classList.toggle('is-current', !!T_.stem && T_.stem === selected); T_.el.classList.toggle('is-ref', !!T_.stem && refs.includes(T_.stem)); });
      tagsDirty = true;
      if (selected && doFly) {
        setHover(null);
        // 讓選到的島落在面板以外的區域：桌機面板在左下，往右讓；手機面板從下方升起，往上讓
        const zoom = Math.max(camera.zoom, C.w > 12 ? 2.3 : 3), W_ = canvas.clientWidth, H_ = canvas.clientHeight;
        const wpp = (camera.right - camera.left) / zoom / W_;
        camera.updateMatrixWorld();
        const R = new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 0), U = new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 1);
        const tgt = V(C.x, T, C.z);
        if (window.innerWidth >= 768) tgt.addScaledVector(R, -Math.min(210, W_ * .2) * wpp);
        else tgt.addScaledVector(U, -H_ * .2 * wpp);
        tgt.y = 0;
        flyTo(tgt, zoom);
      }
      requestRender();
    },
    flyToIsle,
    reset() {
      const off = V(DIST * Math.sin(POL0) * Math.sin(AZ0), DIST * Math.cos(POL0), DIST * Math.sin(POL0) * Math.cos(AZ0));
      camera.position.copy(controls.target).add(off);
      controls.update();
      flyTo(HOME.clone(), 1);
    },
    guideTo(stem) { const [x, y, z] = guideSpot(stem); guideGo(x, y, z); },
    guideEnd(stem) { const C = CHIP[stem]; guideGo(C.w < 12 ? Math.min(C.x + 9, 40) : Math.min(C.x + C.w / 2 + 2.6, 41), .1, C.z); },
    guidePos() { return { x: guide.x, y: guide.y, z: guide.z }; },
    setMode(mode, instant) {
      modeTarget = mode === 'print' ? 1 : 0;
      if (instant || !motion()) applyMode(modeTarget);
      if (modeTarget === 1) { pulseIds.forEach(id => DB.hide(id)); }
      else stepPulses(performance.now() / 1000);
      requestRender();
    },
    play(stem) { playLM(stem); },
    updateTrail() {
      PAGES.forEach(p => {
        const C = CHIP[p.stem];
        DB.role(C.led, trail.done[p.stem] ? 'ledDone' : trail.visited[p.stem] ? 'ledVisit' : 'ledOff');
      });
      tags.forEach(T_ => {
        if (!T_.stem) return;
        T_.el.classList.toggle('is-done', !!trail.done[T_.stem]);
        T_.el.classList.toggle('is-visited', !!trail.visited[T_.stem] && !trail.done[T_.stem]);
      });
      requestRender();
    },
    // 以下給 tools/check_island_browser.js 用
    stats() { return { draws, dprLevel, lowPower, calls: renderer.info.render.calls, modeK }; },
    screenPos(stem) {
      const C = CHIP[stem]; if (!C) return null;
      v3.set(C.x, T, C.z).project(camera);
      const r = canvas.getBoundingClientRect();
      return { x: r.left + (v3.x + 1) / 2 * r.width, y: r.top + (1 - v3.y) / 2 * r.height };
    },
    invariants() { return JSON.parse(JSON.stringify(INV)); },
    pose(stem, u) { if (!LM[stem]) return false; playing.delete(stem); LM[stem].pose(u); requestRender(); return true; },
    plays() { return [...playing.keys()]; },
    // 先編譯著色器並畫好第一幀，再讓畫布淡入
    async warm() {
      try { await renderer.compileAsync(world, camera); } catch (e) { /* 舊版瀏覽器：第一幀時再編譯 */ }
      renderer.render(world, camera); placeTags(); tagsDirty = false; lastDraw = performance.now();
      requestRender();
    },
    dispose() { alive = false; ro.disconnect(); controls.dispose(); renderer.dispose(); layer.replaceChildren(); },
  };
}
