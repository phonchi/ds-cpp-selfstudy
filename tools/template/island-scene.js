/* 3D 資料結構知識群島的場景層。由 island.js 的 initScene() 呼叫 buildWorld()。
 *
 * 做法（全部程序化，沒有模型或圖檔）：
 *   - 島：不規則輪廓 → 分層倒角擠出（沙底、深崖帶、草頂），外圈淺水與浪花環；島之間以拱橋連成授課航線
 *   - 靜態零件：PartKit 收集（box／圓角 box／cyl／cone／sphere／rock／prism），依種類合併成 InstancedMesh 並逐實例上色；陰影只烘一次
 *   - 地標：每章一棟建築＋一個會動的資料結構模型。模型的可動零件共用動態池（不投影），動畫是純函式 pose(u)
 *   - 拱橋只表示授課順序；資料結構裡的指標是細的紅繩箭頭，兩者不可混用
 *   - 標籤是 HTML，每次繪製時投影定位，依優先序避讓；地面標示（head、nullptr…）是一張貼花圖集
 * 本檔與 island.js、island-compare.js 共用頂層名稱：PAGES、BY、ISLES、items、trail、select、closePanel、$、reduceMotion、DATA、graphAdj。
 */
function buildWorld(THREE, addons, renderer, stage, canvas) {
  const { OrbitControls, RoundedBoxGeometry } = addons;
  const motion = () => !reduceMotion.matches;
  const narrow = () => stage.clientWidth < 768;
  const rnd = mulberry32(208);
  const SQ = Math.SQRT1_2;
  // 初始視角的螢幕座標（u 往右、v 往前＝畫面下方）→ 世界座標 xz
  const toWorld = (u, v) => ({ x: (u + v) * SQ, z: (v - u) * SQ });
  const world = new THREE.Scene();
  const anims = [];          // 地標小動畫 (t) => void
  const life = [];           // 生活感動畫 (t, dt) => void；效能不足時整組停用
  let need = true, raf = 0, onScreen = true, alive = true, lowPower = false, dprLevel = 0, tagsDirty = true, draws = 0;

  /* ── 色盤：黏土色；網站的磚紅、深藍、金、森林綠作為屋頂與重點色 ── */
  const C = {
    grass: '#b4d18a', grass2: '#a3c67e', grass3: '#c4dc9c', sand: '#eedbb0', cliff: '#dcc39a', cliffDark: '#c2a477',
    foam: '#fbfaf2', shallow: '#bfe0d6',
    cream: '#fff4de', wall: '#f5e6cb', wall2: '#efdcc0', peach: '#f0c7a5', roof: '#b9563f', roofDark: '#924231',
    roofNavy: '#2c3e7a', roofGreen: '#3f7f61',
    leaf: '#9fb889', leaf2: '#8fae86', leaf3: '#7c9a76', pine: '#7b997c', pine2: '#68876c',
    wood: '#ab875d', woodDark: '#7a5c3e', stone: '#dacdb6', stoneDark: '#b6a78c', ink: '#4f5a55',
    glass: '#8cbcbc', gold: '#f5b82e', white: '#fffcf3', navy: '#2f4566', forest: '#1a6b4a',
    red: '#b9654f', blue: '#5d7b93', blueL: '#c3d0dc', redL: '#ebc7bb', amber: '#d6a35c', teal: '#5aa39a',
  };
  const DAY = { bg: '#a2dbe6', hemiSky: '#fff4dc', hemiGround: '#7d9d8f', hemi: 1.3, sun: '#ffe4c4', sunI: 2.9, fill: .45, sea: '#ffffff', exposure: 1.0 };
  const NIGHT = { bg: '#1f2e44', hemiSky: '#9fb2da', hemiGround: '#2a3a52', hemi: .85, sun: '#c3cff5', sunI: .55, fill: .18, sea: '#56708f', exposure: 1.15 };

  /* ── Renderer ── */
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFShadowMap;      // r18x 起 PCF 以 shadow.radius 柔化
  renderer.shadowMap.autoUpdate = false;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = DAY.exposure;
  world.background = new THREE.Color(DAY.bg);
  world.fog = new THREE.Fog(DAY.bg, 150, 300);       // 只讓最遠的外海淡出

  // 黏土風幾乎沒有反光：除了海面，一律用較輕的 Lambert（roughness／metalness 參數直接略過）
  const std = (color, extra = {}) => { const { roughness, metalness, ...rest } = extra; void roughness; void metalness; return new THREE.MeshLambertMaterial({ color, ...rest }); };
  const basic = (color, extra) => new THREE.MeshBasicMaterial({ color, ...extra });

  /* ── instancify：把會動的小階層（小人、船、鳥、雲、噴泉球…）合併繪製 ──
     階層本身照常用 Object3D 建立與做動畫，但不加進場景；同幾何＋同類材質的 mesh 合成一個 InstancedMesh，
     不透明的 Lambert 材質改用逐實例顏色共用一份材質。每個動畫幀呼叫 syncProxies() 同步世界矩陣。 */
  const proxyRoots = [], proxyPools = new Map();
  const dynSolid = { [THREE.FrontSide]: null, [THREE.DoubleSide]: null };
  function instancify(root) {
    proxyRoots.push(root);
    root.traverse(o => {
      if (!o.isMesh) return;
      const m = o.material;
      const solid = m.isMeshLambertMaterial && !m.transparent && m.emissive.getHex() === 0;
      const key = o.geometry.uuid + '|' + (solid ? 'solid' + m.side : m.uuid);
      if (!proxyPools.has(key)) {
        if (solid && !dynSolid[m.side]) dynSolid[m.side] = new THREE.MeshLambertMaterial({ color: '#ffffff', side: m.side });
        proxyPools.set(key, { geo: o.geometry, mat: solid ? dynSolid[m.side] : m, list: [] });
      }
      proxyPools.get(key).list.push({ o, color: solid ? m.color.clone() : null });
    });
  }
  function finishProxies() {
    proxyPools.forEach(pool => {
      const mesh = new THREE.InstancedMesh(pool.geo, pool.mat, pool.list.length);
      mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage); mesh.frustumCulled = false;
      pool.list.forEach((r, i) => { if (r.color) mesh.setColorAt(i, r.color); });
      pool.mesh = mesh; world.add(mesh);
    });
    syncProxies();
  }
  function syncProxies() {
    proxyRoots.forEach(r => r.updateMatrixWorld(true));
    proxyPools.forEach(pool => {
      if (!pool.mesh) return;
      pool.list.forEach((r, i) => pool.mesh.setMatrixAt(i, r.o.matrixWorld));
      pool.mesh.instanceMatrix.needsUpdate = true;
    });
  }

  /* ═════════ PartKit：零件 → InstancedMesh ═════════ */
  const prismGeo = (() => {
    const tri = new THREE.Shape();
    tri.moveTo(-.5, -.5); tri.lineTo(.5, -.5); tri.lineTo(0, .5); tri.closePath();
    const g = new THREE.ExtrudeGeometry(tri, { depth: 1, bevelEnabled: false });
    g.translate(0, 0, -.5); g.computeVertexNormals(); return g;
  })();
  const GEO = {
    box: new THREE.BoxGeometry(1, 1, 1),
    round: new RoundedBoxGeometry(1, 1, 1, 1, .14),
    cyl: new THREE.CylinderGeometry(.5, .5, 1, 10),
    cone: new THREE.ConeGeometry(.5, 1, 8),
    sphere: new THREE.SphereGeometry(.5, 9, 6),
    rock: new THREE.DodecahedronGeometry(.5, 0),
    prism: prismGeo,
    torus: new THREE.TorusGeometry(.5, .12, 8, 22),
  };
  const kitMat = std('#ffffff');
  const glowMat = new THREE.MeshLambertMaterial({ color: '#ffffff', emissive: '#ffc46b', emissiveIntensity: 0 });
  const parts = [];
  const lamps = [];          // 夜間光暈的位置
  const ao = [];             // 接觸暗部（假環境光遮蔽）：[x, y, z, r]
  // y 一律是「底面高度」；rx/ry/rz 以 YXZ 順序套用（先轉向、再俯仰）
  function part(kind, x, y, z, w, h, d, color, o = {}) {
    parts.push({ kind, x, y, z, w, h, d, color, rx: o.rx || 0, ry: o.ry || 0, rz: o.rz || 0, glow: !!o.glow });
  }
  // 以 (ox,oz) 為原點、轉 rot、縮放 s 的區域座標畫零件
  function at(ox, oy, oz, rot = 0, s = 1) {
    const c = Math.cos(rot), sn = Math.sin(rot);
    const f = (kind, x, y, z, w, h, d, color, o = {}) =>
      part(kind, ox + (x * c + z * sn) * s, oy + y * s, oz + (-x * sn + z * c) * s, w * s, h * s, d * s, color,
        { ...o, ry: (o.ry || 0) + rot });
    f.ao = (x, z, r) => ao.push([ox + (x * c + z * sn) * s, oy, oz + (-x * sn + z * c) * s, r * s]);
    return f;
  }
  // 在畫筆 p 的區域座標裡再疊一層平移／旋轉／縮放
  function sub(p, ox, oz, rot = 0, s = 1) {
    const c = Math.cos(rot), sn = Math.sin(rot);
    const f = (kind, x, y, z, w, h, d, color, o = {}) =>
      p(kind, ox + (x * c + z * sn) * s, y * s, oz + (-x * sn + z * c) * s, w * s, h * s, d * s, color, { ...o, ry: (o.ry || 0) + rot });
    f.ao = (x, z, r) => p.ao && p.ao(ox + (x * c + z * sn) * s, oz + (-x * sn + z * c) * s, r * s);
    return f;
  }
  function flushParts() {
    const groups = new Map();
    parts.forEach(p => { const k = p.kind + (p.glow ? '|g' : ''); if (!groups.has(k)) groups.set(k, []); groups.get(k).push(p); });
    const o = new THREE.Object3D(); o.rotation.order = 'YXZ';
    const col = new THREE.Color();
    groups.forEach((list, k) => {
      const glow = k.endsWith('|g');
      const mesh = new THREE.InstancedMesh(GEO[list[0].kind], glow ? glowMat : kitMat, list.length);
      list.forEach((p, i) => {
        o.position.set(p.x, p.y + p.h / 2, p.z); o.rotation.set(p.rx, p.ry, p.rz); o.scale.set(p.w, p.h, p.d);
        o.updateMatrix(); mesh.setMatrixAt(i, o.matrix); mesh.setColorAt(i, col.set(p.color));
      });
      mesh.castShadow = !glow; mesh.receiveShadow = true;
      mesh.computeBoundingSphere();
      world.add(mesh);
    });
    parts.length = 0;
  }

  /* ── 共用道具配方（p 是 part 或 at(...) 回傳的畫筆）── */
  const LEAVES = [C.leaf, C.leaf2, C.leaf3];
  // 畫筆外加一個「記錄接觸暗部」的通道：p.ao(x, z, r)
  function tree(p, x, z, s = 1, k = 0) {
    p.ao && p.ao(x, z, .75 * s);
    p('cyl', x, 0, z, .16 * s, 1.0 * s, .16 * s, C.woodDark);
    [[-.24, .75, .08, .9], [.26, .9, .05, .82], [0, 1.18, -.1, .8], [-.05, .86, -.28, .74]].forEach(([dx, dy, dz, d], i) =>
      p('sphere', x + dx * s, dy * s, z + dz * s, d * s, d * .92 * s, d * s, LEAVES[(k + i) % 3]));
  }
  function pine(p, x, z, s = 1, k = 0) {
    p.ao && p.ao(x, z, .7 * s);
    p('cyl', x, 0, z, .13 * s, .7 * s, .13 * s, C.woodDark);
    for (let i = 0; i < 3; i++) p('cone', x, (.45 + i * .42) * s, z, (1.05 - i * .24) * s, .95 * s, (1.05 - i * .24) * s, (i + k) % 2 ? C.pine : C.pine2);
  }
  function bush(p, x, z, s = 1, k = 0) {
    p.ao && p.ao(x, z, .55 * s);
    p('sphere', x, 0, z, .62 * s, .46 * s, .56 * s, LEAVES[k % 3]);
    p('sphere', x + .26 * s, 0, z + .12 * s, .42 * s, .34 * s, .4 * s, LEAVES[(k + 1) % 3]);
  }
  function flowers(p, x, z, k = 0) {
    const petals = ['#f2b8a0', '#f7e1b5', '#e9967a', '#fff4de', '#d9a0c0'];
    for (let i = 0; i < 5; i++) {
      const a = i * 1.3 + k, r = .28 + (i % 2) * .12;
      p('sphere', x + Math.cos(a) * r, 0, z + Math.sin(a) * r, .2, .16, .2, C.leaf2);
      p('sphere', x + Math.cos(a) * r, .1, z + Math.sin(a) * r, .13, .12, .13, petals[(i + k) % petals.length]);
    }
  }
  function rock(p, x, z, s = 1) {
    p('rock', x, -.05 * s, z, .7 * s, .5 * s, .6 * s, C.stoneDark, { ry: rnd() * 6 });
    p('rock', x + .35 * s, -.05 * s, z + .2 * s, .4 * s, .3 * s, .4 * s, C.stone, { ry: rnd() * 6 });
  }
  function lamp(p, x, z) {
    p('cyl', x, 0, z, .12, .12, .12, C.ink);
    p('cyl', x, 0, z, .06, 1.35, .06, C.ink);
    p('sphere', x, 1.3, z, .22, .22, .22, '#ffe9b8', { glow: true });
    p('cone', x, 1.48, z, .3, .16, .3, C.ink);
    return [x, 1.42, z];
  }
  function bench(p, x, z, ry = 0) {
    const q = at(x, 0, z, ry);
    q('box', 0, .32, 0, .9, .07, .32, C.wood); q('box', 0, .45, -.14, .9, .26, .06, C.wood);
    q('box', -.38, 0, 0, .07, .32, .28, C.woodDark); q('box', .38, 0, 0, .07, .32, .28, C.woodDark);
  }
  function cottage(p, x, z, ry, roofC = C.roof, wallC = C.wall, s = 1) {
    const q = sub(p, x, z, ry, s);
    q.ao(0, 0, 1.25);
    q('round', 0, -.02, 0, 1.62, .14, 1.38, C.stoneDark);
    q('round', 0, 0, 0, 1.5, 1.05, 1.25, wallC);
    q('prism', 0, 1.0, 0, 1.75, .78, 1.45, roofC);
    q('box', .45, 1.25, -.25, .26, .62, .26, C.stoneDark);
    q('round', 0, 0, .6, .36, .66, .08, C.woodDark);
    [-.45, .45].forEach(dx => { q('box', dx, .38, .615, .38, .36, .04, C.white); q('box', dx, .42, .62, .3, .28, .05, '#ffe1a0', { glow: true }); });
    q('box', 0, .99, .7, 1.8, .06, .08, C.white);
    q('box', -.76, .42, 0, .05, .28, .3, '#ffe1a0', { glow: true });
  }
  function crate(p, x, z, s = 1, c = C.wood) { p('round', x, 0, z, .5 * s, .5 * s, .5 * s, c, { ry: rnd() }); }

  /* ═════════ 島工廠：分層倒角擠出 ═════════ */
  const M = {
    grass: std(C.grass), grass2: std(C.grass2), grass3: std(C.grass3), sand: std(C.sand),
    cliff: std(C.cliff), cliffDark: std(C.cliffDark),
    foam: basic(C.foam, { transparent: true, opacity: .6, depthWrite: false, side: THREE.DoubleSide }),
    shallow: basic(C.shallow, { transparent: true, opacity: .5, depthWrite: false, side: THREE.DoubleSide }),
  };
  const BASE_H = 1.0, BEVEL = .08, GROUND = BASE_H + BEVEL;
  function outline(seed, radius, wobble = .17, n = 56) {
    const r = mulberry32(seed);
    const hs = [[2, .45], [3, .3], [4, .15], [7, .1]].map(([f, w]) => [f, w, r() * Math.PI * 2]);
    // 一到兩個小灣：在隨機方向往內凹，打破圓餅輪廓
    const bays = Array.from({ length: 1 + Math.floor(r() * 2) }, () => [r() * Math.PI * 2, .12 + r() * .1]);
    return Array.from({ length: n }, (_, i) => {
      const a = i / n * Math.PI * 2;
      let k = 1 + wobble * hs.reduce((s, [f, w, ph]) => s + w * Math.sin(f * a + ph), 0);
      bays.forEach(([b, d]) => { const t = Math.atan2(Math.sin(a - b), Math.cos(a - b)); k -= d * (wobble / .17) * Math.exp(-t * t / .045); });
      return [Math.cos(a) * radius * k, Math.sin(a) * radius * k];
    });
  }
  const scaled = (pts, s, inset = 0) => pts.map(([x, z]) => {
    const r = Math.hypot(x, z), k = inset ? Math.max(r - inset, r * .05) / r : 1;
    return [x * s * k, z * s * k];
  });
  const shapeOf = pts => {                 // shape 的 y＝世界的 -z（rotateX(-π/2) 之後對回 z）
    const sh = new THREE.Shape();
    pts.forEach(([x, z], i) => (i ? sh.lineTo(x, -z) : sh.moveTo(x, -z)));
    sh.closePath(); return sh;
  };
  function slab(pts, depth, mats, y) {
    const g = new THREE.ExtrudeGeometry(shapeOf(pts), { depth, bevelEnabled: true, bevelThickness: BEVEL, bevelSize: .1, bevelSegments: 2, curveSegments: 4 });
    g.rotateX(-Math.PI / 2);
    const m = new THREE.Mesh(g, mats); m.position.y = y; m.castShadow = true; m.receiveShadow = true; return m;
  }
  function ring(pts, inner, outer, mat, y) {
    const sh = shapeOf(scaled(pts, outer));
    const hole = new THREE.Path();
    [...scaled(pts, inner)].reverse().forEach(([x, z], i) => (i ? hole.lineTo(x, -z) : hole.moveTo(x, -z)));
    sh.holes.push(hole);
    const g = new THREE.ShapeGeometry(sh, 2); g.rotateX(-Math.PI / 2);
    const m = new THREE.Mesh(g, mat); m.position.y = y; m.renderOrder = 1; return m;
  }
  const isles = [], isleGroups = [];
  // 所有島的各層（沙底、崖帶、草頂、浪花環）建好後依材質合併：21 座島 × 4 層 → 每種材質一個 mesh
  function mergeIsles() {
    const buckets = new Map();
    isleGroups.forEach(g => {
      g.updateMatrixWorld(true);
      g.traverse(o => {
        if (!o.isMesh) return;
        const geo = (o.geometry.index ? o.geometry.toNonIndexed() : o.geometry.clone()).applyMatrix4(o.matrixWorld);
        const pos = geo.attributes.position.array, nor = geo.attributes.normal.array;
        const mats = Array.isArray(o.material) ? o.material : [o.material];
        const groups = geo.groups.length ? geo.groups : [{ start: 0, count: geo.attributes.position.count, materialIndex: 0 }];
        groups.forEach(gr => {
          const mat = mats[gr.materialIndex];
          if (!buckets.has(mat.uuid)) buckets.set(mat.uuid, { mat, pos: [], nor: [], shadow: o.castShadow, order: o.renderOrder });
          const bk = buckets.get(mat.uuid);
          for (let i = gr.start * 3, e = (gr.start + gr.count) * 3; i < e; i++) { bk.pos.push(pos[i]); bk.nor.push(nor[i]); }
        });
        geo.dispose(); o.geometry.dispose();
      });
    });
    buckets.forEach(bk => {
      const geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.Float32BufferAttribute(bk.pos, 3));
      geo.setAttribute('normal', new THREE.Float32BufferAttribute(bk.nor, 3));
      geo.computeBoundingSphere();
      const m = new THREE.Mesh(geo, bk.mat); m.castShadow = m.receiveShadow = bk.shadow; m.renderOrder = bk.order; world.add(m);
    });
  }
  function makeIsle({ u, v, radius, seed, grass = 'grass', highland = 0, wobble = .17 }) {
    const { x, z } = toWorld(u, v);
    const pts = outline(seed, radius, wobble);
    const g = new THREE.Group(); g.position.set(x, 0, z);
    g.add(ring(pts, 1.13, 1.19, M.foam, .05));
    g.add(slab(scaled(pts, 1.12), .2, [M.sand, M.sand], -.14));
    g.add(slab(scaled(pts, 1.0), .34, [M.cliffDark, M.cliffDark], 0));
    g.add(slab(scaled(pts, 1, .07), BASE_H, [M[grass], M.cliff], 0));
    let top = GROUND;
    if (highland) {
      g.add(slab(scaled(pts, highland, .05), 1.0, [M.grass2, M.cliff], GROUND));
      top = GROUND + 1.0 + BEVEL;
    }
    isleGroups.push(g);
    const angR = a => {                    // 該方向的海岸半徑（線性內插輪廓點）
      const n = pts.length, k = ((a / (Math.PI * 2)) % 1 + 1) % 1 * n, i = Math.floor(k), f = k - i;
      const [x0, z0] = pts[i % n], [x1, z1] = pts[(i + 1) % n];
      return Math.hypot(x0, z0) * (1 - f) + Math.hypot(x1, z1) * f;
    };
    const isle = { x, z, radius, pts, top, angR, gaps: [] };
    isle.inside = (wx, wz, m = .8) => Math.hypot(wx - x, wz - z) < angR(Math.atan2(wz - z, wx - x)) * m;
    isles.push(isle);
    return isle;
  }


  /* ═════════ 佈局（螢幕座標）═════════ */
  const core = PAGES.filter(p => p.grp === 'core');
  // 9 章蛇形三列：01–03 前排往右、04–06 中排往左、07–09 後排往右。島夠大，放得下建築和模型
  const CORE_UV = [[-17, 20], [.5, 21], [17.5, 19.5], [18, .5], [0, -.5], [-17.5, .5], [-17, -20], [.5, -21], [17.5, -19.5]];
  const SAT = { pre: { u: -20, v: 36.5, r: 7.2, seed: 41 }, workshop: { u: 20, v: -37.5, r: 10, seed: 57 } };
  const SLOT = {};       // stem → { isle, x, z, y(base) }
  core.forEach((p, i) => {
    const [u, v] = CORE_UV[i];
    const isle = makeIsle({ u, v, radius: 6.4, seed: 100 + i * 7, grass: i % 3 === 1 ? 'grass2' : 'grass', wobble: .09 });
    SLOT[p.stem] = { isle, x: isle.x, z: isle.z, y: isle.top };
  });
  const SAT_ISLE = {};
  Object.entries(SAT).forEach(([grp, s]) => { SAT_ISLE[grp] = makeIsle({ u: s.u, v: s.v, radius: s.r, seed: s.seed, grass: grp === 'pre' ? 'grass3' : 'grass', wobble: .1 }); });
  // 附屬島上各單元的位置（以初始視角排：左到右、上到下）
  const UNIT_UV = {
    pre: [[-3.2, -2.4], [3.1, -2], [-.2, 3]],
    workshop: [[-5.4, -4.8], [0, -5.8], [5.4, -4.8], [-6.2, .2], [0, .2], [6.2, .2], [-5.2, 5.2], [0, 6], [5.4, 5.2]],
  };
  ['pre', 'workshop'].forEach(grp => {
    const I = SAT_ISLE[grp];
    PAGES.filter(p => p.grp === grp).forEach((p, i) => {
      const [du, dv] = UNIT_UV[grp][i], d = toWorld(du, dv);
      SLOT[p.stem] = { isle: I, x: I.x + d.x, z: I.z + d.z, y: I.top };
    });
  });

  /* ── 拱橋：二次貝茲，木板兩色交替、細扶手、每 3 片一根柱 ── */
  const bridges = [];
  function bridge(A, B) {
    const dx = B.x - A.x, dz = B.z - A.z, L = Math.hypot(dx, dz), ux = dx / L, uz = dz / L;
    const aA = Math.atan2(uz, ux), aB = Math.atan2(-uz, -ux);
    const s0 = A.angR(aA) * .9, s1 = L - B.angR(aB) * .9;
    A.gaps.push(aA); B.gaps.push(aB);
    const p0 = new THREE.Vector3(A.x + ux * s0, A.top - .04, A.z + uz * s0);
    const p2 = new THREE.Vector3(A.x + ux * s1, B.top - .04, A.z + uz * s1);
    const p1 = p0.clone().lerp(p2, .5); p1.y = Math.max(p0.y, p2.y) + Math.min(1.6, .22 * (s1 - s0) + .4);
    const curve = new THREE.QuadraticBezierCurve3(p0, p1, p2);
    const n = Math.max(4, Math.round(curve.getLength() / .3)), pts = curve.getSpacedPoints(n);
    const ry = Math.atan2(ux, uz);
    for (let i = 0; i < n; i++) {
      const a = pts[i], b = pts[i + 1], h = Math.hypot(b.x - a.x, b.z - a.z), m = a.clone().lerp(b, .5);
      const rx = -Math.atan2(b.y - a.y, h);
      part('box', m.x, m.y - .035, m.z, 1.12, .07, h * .92, i % 3 ? C.wood : C.woodDark, { rx, ry });
      [-1, 1].forEach(side => {
        const ox = uz * .56 * side, oz = -ux * .56 * side;
        part('box', m.x + ox, m.y + .44, m.z + oz, .05, .05, h + .02, C.woodDark, { rx, ry });
        if (i % 3 === 0) part('cyl', m.x + ox, m.y - .1, m.z + oz, .08, .58, .08, C.woodDark);
      });
    }
    // 兩端在島上的一小段石板路，讓橋「接上」島
    [[A, -1, p0], [B, 1, p2]].forEach(([I, sgn, end]) => {
      for (let k = 1; k <= 3; k++) {
        const t = k * .45; part('cyl', end.x + ux * t * sgn, I.top - .02, end.z + uz * t * sgn, .5, .05, .5, '#e9dcc0', { ry: rnd() * 3 });
      }
    });
    bridges.push({ A, B, curve, pts });
  }
  const coreIsles = core.map(p => SLOT[p.stem].isle);
  for (let i = 0; i + 1 < coreIsles.length; i++) bridge(coreIsles[i], coreIsles[i + 1]);
  bridge(SAT_ISLE.pre, coreIsles[0]);
  bridge(coreIsles[coreIsles.length - 1], SAT_ISLE.workshop);
  const nearGap = (I, a, tol = .42) => I.gaps.some(g => Math.abs(Math.atan2(Math.sin(a - g), Math.cos(a - g))) < tol);

  /* ═════════ 地標：每章一棟建築＋旁邊會動的資料結構模型 ═════════
     建築是靜態零件（會投影）；模型的可動零件放在下面三個動態池，不投影。
     每座模型的動畫是純函式 pose(u)，u = 0 是靜止姿態；播放只是把 u 從 0 推到 1。
     結構約束列在 tools/island_meta.py 開頭，check_island_browser.js 會用 invariants() 實測。 */
  const FACE = Math.PI / 4;                       // 正面朝向初始視角
  const B = {};                                   // stem → { top, x, z, y, pickR, ... }
  const dynRoot = new THREE.Group();
  const dynMat = new THREE.MeshLambertMaterial({ color: '#ffffff' });
  const _o = new THREE.Object3D(), _zero = new THREE.Matrix4().makeScale(0, 0, 0), _col = new THREE.Color();
  const _UY = new THREE.Vector3(0, 1, 0), _dir = new THREE.Vector3(), _v0 = new THREE.Vector3(), _v1 = new THREE.Vector3();
  _o.rotation.order = 'YXZ';
  function pool(kind, cap) {
    const mesh = new THREE.InstancedMesh(GEO[kind], dynMat, cap);
    mesh.frustumCulled = false; mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage); mesh.receiveShadow = true;
    for (let i = 0; i < cap; i++) { mesh.setMatrixAt(i, _zero); mesh.setColorAt(i, _col.set('#ffffff')); }
    let n = 0; const cols = [];
    const P = {
      alloc(c) { if (n >= cap) throw new Error('動態池已滿：' + kind); cols[n] = c; mesh.setColorAt(n, _col.set(c)); mesh.instanceColor.needsUpdate = true; return n++; },
      color(id, c) { if (cols[id] === c) return; cols[id] = c; mesh.setColorAt(id, _col.set(c)); mesh.instanceColor.needsUpdate = true; },
      hide(id) { mesh.setMatrixAt(id, _zero); mesh.instanceMatrix.needsUpdate = true; },
      at(id, x, y, z, w, h, d, ry = 0) {
        _o.position.set(x, y + h / 2, z); _o.rotation.set(0, ry, 0); _o.quaternion.setFromEuler(_o.rotation); _o.scale.set(w, h, d); _o.updateMatrix();
        mesh.setMatrixAt(id, _o.matrix); mesh.instanceMatrix.needsUpdate = true;
      },
      beam(id, a, b, w) {            // 圓柱沿 a → b（cyl 與 cone 的軸都是 Y）
        _dir.subVectors(b, a); const len = _dir.length();
        if (len < .02) { P.hide(id); return; }
        _o.position.addVectors(a, b).multiplyScalar(.5);
        _o.quaternion.setFromUnitVectors(_UY, _dir.divideScalar(len)); _o.scale.set(w, len, w); _o.updateMatrix();
        mesh.setMatrixAt(id, _o.matrix); mesh.instanceMatrix.needsUpdate = true;
      },
    };
    world.add(mesh);
    return P;
  }
  const RD = pool('round', 240), CY = pool('cyl', 200), CO = pool('cone', 40), SP = pool('sphere', 40);
  // 指標箭頭：細的紅繩＋角錐箭頭（和木造拱橋明顯不同，拱橋只表示授課順序）
  const PTR = '#c0392b';
  function arrowAlloc(c = PTR) { return { b: CY.alloc(c), p: CO.alloc(c) }; }
  function arrowHide(A) { CY.hide(A.b); CO.hide(A.p); }
  function arrowSet(A, a, b) {
    _dir.subVectors(b, a); const len = _dir.length();
    if (len < .15) { arrowHide(A); return; }
    const head = Math.min(.42, len * .45);
    _v0.copy(b).addScaledVector(_dir, -head / len);
    CY.beam(A.b, a, _v0, .085);
    CO.beam(A.p, _v0, b, .34);
  }
  function arrowStatic(a, b, c = PTR) { const A = arrowAlloc(c); arrowSet(A, a, b); return A; }

  /* 地面上的標示（head、nullptr、k mod 11…）：一張貼花圖集、一次繪製 */
  const decals = [];
  // 區域座標：x 往畫面右、z 往畫面前；以島心為原點
  function LOC(S, y = S.y) {
    const c = Math.cos(FACE), sn = Math.sin(FACE);
    const X = (x, z) => S.x + x * c + z * sn, Z = (x, z) => S.z - x * sn + z * c;
    return {
      q: at(S.x, y, S.z, FACE), y,
      P: (x, h, z) => new THREE.Vector3(X(x, z), y + h, Z(x, z)),
      rd: (id, x, h, z, w, hh, d) => RD.at(id, X(x, z), y + h, Z(x, z), w, hh, d, FACE),
      sp: (id, x, h, z, w, hh, d) => SP.at(id, X(x, z), y + h, Z(x, z), w, hh, d, FACE),
      cy: (id, x, h, z, w, hh, d) => CY.at(id, X(x, z), y + h, Z(x, z), w, hh, d, FACE),
      say: (text, x, z, size = .42, ink = '#2c3e7a') => decals.push({ text, x: X(x, z), y: y + .03, z: Z(x, z), size: size * 1.3, ink }),
    };
  }
  function shed(q, x, z, w, d, h, roofC, wallC = C.wall) {     // 這些建築的共通外型：牆＋山形屋頂＋門＋亮燈的窗
    q.ao(x, z, Math.max(w, d) * .62);
    q('round', x, 0, z, w, h, d, wallC);
    q('prism', x, h - .02, z, w + .22, Math.min(.72, w * .36), d + .16, roofC);
    q('round', x, 0, z + d / 2 + .01, Math.min(.42, w * .26), Math.min(.72, h * .6), .07, C.woodDark);
    q('box', x - w * .28, h * .46, z + d / 2 + .01, .28, .26, .04, '#ffe1a0', { glow: true });
    q('box', x + w * .28, h * .46, z + d / 2 + .01, .28, .26, .04, '#ffe1a0', { glow: true });
  }
  const LM = {}, POSE = {}, INV = {};
  const clamp01 = x => Math.max(0, Math.min(1, x));
  const seg = (u, a, b) => { const t = clamp01((u - a) / (b - a)); return t * t * (3 - 2 * t); };
  const lerp = (a, b, t) => a + (b - a) * t;
  const CRATE = [C.amber, C.red, C.forest, C.blue, C.cream];

  // 01 C++ 導論：位址郵局。信箱寬度＝位元組數；路標 p 存的是 x 的位址，*p = 50 只改信箱裡的東西
  LM.introduction = S => {
    const L = LOC(S), { q } = L, s = .52, z0 = 1.3; let cx = -3.55;
    q('round', 0, 0, z0, 7.7, .12, 1.6, C.stone);
    const span = (n, name, bytes) => {
      const x0 = cx;
      for (let i = 0; i < n; i++) { q('round', cx + s / 2, .12, z0, s, .46, 1.05, i % 2 ? C.wall2 : C.cream); cx += s; }
      const c = (x0 + cx) / 2; L.say(name, c, z0 + 1.05, .4); L.say(bytes, n === 1 ? c - .15 : c + .35, n === 1 ? z0 + 2.05 : z0 + 1.55, .3, '#6f6a5f'); cx += .2; return c;
    };
    span(1, 'char', '1 byte'); const xInt = span(4, 'int x', '通常 4 bytes'); span(8, 'double', '通常 8 bytes');
    shed(q, -2.2, -2.3, 3, 2.1, 1.6, C.roof);
    q('box', -2.2, 1.0, -1.23, .78, .46, .05, C.white); q('prism', -2.2, 1.26, -1.2, .78, .2, .04, C.gold, { rx: Math.PI });
    q('cyl', .15, 0, -1.9, .13, 1.55, .13, C.woodDark); q('round', .15, 1.45, -1.9, .9, .34, .34, C.navy);
    L.say('int* p', .15, -.8, .4);
    L.say('int x = 100;', 2.65, -2.7, .34); L.say('int* p = &x;', 2.65, -2.15, .34); L.say('*p = 50;', 2.65, -1.6, .34);
    const val = RD.alloc(C.gold), A = arrowAlloc(), pkt = SP.alloc(C.red);
    POSE.introduction = { dur: 5.2, pose(u) {
      const h = lerp(1.4, .7, seg(u, .45, .58));
      L.rd(val, xInt, .58, z0, 1.9, h, .9);
      const from = L.P(.15, 1.62, -1.9), to = L.P(xInt + .4, .58 + h, z0 - .1);
      arrowSet(A, from, to);       // *p = 50 只改 x 的值，p 仍然指著 x
      if (u > .12 && u < .46) { _v1.lerpVectors(from, to, seg(u, .14, .44)); SP.at(pkt, _v1.x, _v1.y - .15, _v1.z, .32, .32, .32); } else SP.hide(pkt);
    } };
    return 2.9;
  };

  // 02 演算法分析：成長溫室。六株植物的高度真的照 f(n) 計算；撞到屋頂的標紅
  LM.analysis = S => {
    const L = LOC(S), { q } = L, FN = [['1', () => 1], ['log n', n => Math.log2(n)], ['n', n => n], ['n log n', n => n * Math.log2(n)], ['n²', n => n * n], ['2ⁿ', n => 2 ** n]];
    const MAX = 3, K = .045, step = 1.28, x0 = -3.2, z0 = .9;
    q('round', 0, 0, z0, 8.2, .14, 2.2, C.stone);
    [[-4, -.1], [4, -.1], [-4, 1.9], [4, 1.9]].forEach(([x, z]) => q('box', x, .1, z, .1, MAX + .04, .1, C.white));
    [-.1, 1.9].forEach(z => q('box', 0, MAX + .14, z, 8.1, .08, .08, C.white));
    [-4, -2.4, -.8, .8, 2.4, 4].forEach(x => q('box', x, MAX + .14, z0, .06, .06, 2, C.white));
    shed(q, 2.6, -2.5, 2.3, 1.7, 1.2, C.roofGreen);
    L.say('玻璃屋頂＝刻度上限', -1.6, -1.1, .34, '#6f6a5f');
    L.say('n 變大時，誰先撞到屋頂？', -1.2, 3.1, .36, '#6f6a5f');
    const bars = FN.map(([name], i) => {
      q('round', x0 + i * step, .14, z0, 1, .14, 1, C.woodDark);
      L.say(name, x0 + i * step, z0 + 1.55, .34);
      return { bar: RD.alloc(C.forest), cap: SP.alloc(C.leaf) };
    });
    POSE.analysis = { dur: 6, pose(u) {
      const n = lerp(2, 16, seg(u, .04, .9));
      FN.forEach(([, f], i) => {
        const raw = Math.max(.15, f(n) * K), h = Math.min(MAX - .22, raw), hit = raw > MAX - .22;
        L.rd(bars[i].bar, x0 + i * step, .28, z0, .42, h, .42);
        SP.color(bars[i].cap, hit ? C.red : C.leaf);
        L.sp(bars[i].cap, x0 + i * step, .2 + h, z0, .8, .4, .8);
      });
    } };
    return 3.6;
  };

  // 03 陣列：連棟倉庫。隔間零間距；insert(1, 99) 由後往前一次複製一箱（中途有兩個相同的值，這是複製不是交換）
  LM.arrays = S => {
    const L = LOC(S), { q } = L, s = .92, n = 8, x0 = -3.68, z0 = 1.25, cellX = i => x0 + s * i + s / 2;
    INV.arrays = { cells: [] };
    for (let i = 0; i < n; i++) {
      q('box', cellX(i), 0, z0, s, .12, 1.3, i % 2 ? C.wall2 : C.cream);
      INV.arrays.cells.push({ x0: x0 + s * i, x1: x0 + s * (i + 1) });
      L.say(String(i), cellX(i), z0 + .98, .32, '#6f6a5f');
    }
    q('box', 0, 0, z0 - .72, s * n, 1.45, .14, C.wall);                 // 一道共用的後牆：隔間連在一起
    q('prism', 0, 1.42, z0 - .72, .7, .34, s * n + .1, C.roofNavy, { rz: 0, ry: Math.PI / 2 });
    L.say('base + i × sizeof(int)', 0, z0 + 1.45, .36);
    const sparse = [[0, 1], [1, 4], [2, 2], [3, 5]], gx = -3.7, gz = -3.3, gs = .42;
    for (let r = 0; r < 4; r++) for (let c = 0; c < 6; c++) {
      const on = sparse.some(([a, b]) => a === r && b === c);
      q('box', gx + c * gs + gs / 2, 0, gz + r * gs + gs / 2, gs - .03, .05, gs - .03, on ? '#c8a874' : C.grass2);
      if (on) q('sphere', gx + c * gs + gs / 2, .05, gz + r * gs + gs / 2, .36, .5, .36, C.forest);
    }
    shed(q, 2.5, -2.5, 2.1, 1.6, 1.1, C.roof);
    sparse.forEach(([r, c], i) => L.say(`(${r},${c}) → v`, .55, -3.75 + i * .44, .3));
    const roles = [C.amber, C.red, C.forest, C.blue, C.cream], NEWC = C.gold;
    const slots = Array.from({ length: n }, () => RD.alloc(C.amber)), mover = RD.alloc(NEWC);
    const put = (i, c) => { RD.color(slots[i], c); L.rd(slots[i], cellX(i), .12, z0, s - .2, .68, .86); };
    POSE.arrays = { dur: 6, pose(u) {
      if (u >= .985) u = 0;
      const cur = roles.concat([null, null, null]), STEPS = 4, a = .08, span = .13;   // a[4→5]、a[3→4]、a[2→3]、a[1→2]，最後放 99
      RD.hide(mover);
      for (let k = 0; k < STEPS; k++) {
        const from = 4 - k, to = from + 1, t0 = a + k * span, t1 = t0 + span;
        if (u >= t1) cur[to] = cur[from];
        else if (u > t0) {
          const t = seg(u, t0, t1 - .02);
          RD.color(mover, cur[from]);
          L.rd(mover, lerp(cellX(from), cellX(to), t), .8 + Math.sin(t * Math.PI) * .55, z0, s - .3, .6, .76);
        }
      }
      const tP = a + STEPS * span;
      if (u >= tP + .1) cur[1] = NEWC;
      else if (u > tP) { RD.color(mover, NEWC); L.rd(mover, cellX(1), .12 + lerp(2.2, 0, seg(u, tP, tP + .1)), z0, s - .2, .68, .86); }
      slots.forEach((id, i) => { if (cur[i]) put(i, cur[i]); else RD.hide(id); });
    } };
    return 2.5;
  };

  // 04 鏈結串列：散落小屋。小屋不共線，靠紅繩相連，尾端接 nullptr。add(26)：只改繩子，其他小屋不動
  LM.linked_lists = S => {
    const L = LOC(S), { q } = L, NODES = [[-1.5, -2.5], [2.5, -3], [3.5, .6], [-.2, 1.5]], NEW = [-3.5, .55];
    INV.linked_lists = { nodes: NODES.map(n => n.slice()) };
    const h = 1;
    NODES.forEach(([x, z]) => { shed(q, x, z, 1.3, 1.15, h, C.roofNavy); });
    const HD = [-3.7, -2.9];
    q('cyl', HD[0], 0, HD[1], .12, 1.05, .12, C.woodDark); q('round', HD[0], .95, HD[1], .95, .36, .14, C.gold);
    L.say('head', HD[0], HD[1] + .62, .4);
    const NUL = [-2.4, 3.15];
    q('cyl', NUL[0], 0, NUL[1], .12, .9, .12, C.woodDark); q('round', NUL[0], .8, NUL[1], .85, .32, .1, C.red);
    q('round', NUL[0] - .22, 0, NUL[1] + .3, .5, .16, .3, C.stoneDark); q('round', NUL[0] + .28, 0, NUL[1] + .25, .42, .13, .3, C.stone);
    L.say('nullptr', NUL[0] + 1.5, NUL[1] + .2, .4);
    const out = ([x, z]) => L.P(x + .3, h + .55, z), inn = ([x, z]) => L.P(x - .15, h + .62, z);
    for (let i = 0; i + 1 < NODES.length; i++) arrowStatic(out(NODES[i]), inn(NODES[i + 1]));
    arrowStatic(out(NODES[3]), L.P(NUL[0] + .25, .85, NUL[1]));
    const fresh = [RD.alloc(C.cream), RD.alloc(C.forest)], hA = arrowAlloc(), nA = arrowAlloc(C.forest), hOut = L.P(HD[0], 1.15, HD[1]);
    POSE.linked_lists = { dur: 5.4, pose(u) {
      const up = seg(u, .1, .28), on = u > .08 && u < .985;
      if (on) {
        L.rd(fresh[0], NEW[0], lerp(-1.1, 0, up), NEW[1], 1.3, h * up + .001, 1.15);
        L.rd(fresh[1], NEW[0], lerp(-1.1, 0, up) + h * up, NEW[1], 1.45, .42 * up + .001, 1.3);
      } else { RD.hide(fresh[0]); RD.hide(fresh[1]); }
      const g = seg(u, .32, .52);
      if (on && g > .02) arrowSet(nA, out(NEW), new THREE.Vector3().lerpVectors(out(NEW), inn(NODES[0]), g)); else arrowHide(nA);
      const sw = on ? seg(u, .6, .82) : 0;
      arrowSet(hA, hOut, new THREE.Vector3().lerpVectors(inn(NODES[0]), inn(NEW), sw));
    } };
    return 2.4;
  };

  // 05 堆疊／佇列／Deque：碼頭三設施。差別只在開口：貨井只開頂端，驗票通道一進一出，渡口兩端都通
  LM.linear_structures = S => {
    const L = LOC(S), { q } = L;
    q('box', .1, 0, -.1, 8.2, .1, 6.2, C.wood);
    for (let z = -3; z <= 2.9; z += .62) q('box', .1, .1, z, 8.2, .012, .03, C.woodDark);
    const SX = -2.75, SW = 1.5, LV = .78, levels = 3;
    INV.linear_structures = { stackWalls: 4, stackTopOpen: true, levels };
    q('round', SX, .1, .1, SW + .35, .12, SW + .35, C.stoneDark);
    [[-1, -1], [1, -1], [1, 1], [-1, 1]].forEach(([a, b]) => q('box', SX + a * SW / 2, .1, .1 + b * SW / 2, .1, LV * levels + .1, .1, C.woodDark));
    for (let l = 0; l < levels; l++) {
      const y = .42 + l * LV;
      q('box', SX, y, .1 - SW / 2, SW, .07, .07, C.woodDark); q('box', SX, y, .1 + SW / 2, SW, .07, .07, C.woodDark);
      q('box', SX - SW / 2, y, .1, .07, .07, SW, C.woodDark); q('box', SX + SW / 2, y, .1, .07, .07, SW, C.woodDark);
    }
    L.say('stack', SX, 1.35, .42); L.say('只開頂端', SX, 1.8, .3, '#6f6a5f');
    shed(q, SX, -2.15, 1.7, 1.3, .95, C.roof);
    const tube = (z, name, ends) => {
      const x0 = -1.15, x1 = 3.95, cx = (x0 + x1) / 2, Ln = x1 - x0, hw = .62;
      [-1, 1].forEach(s => { q('box', cx, .68, z + s * hw, Ln, .07, .07, C.white); [x0, cx, x1].forEach(px => q('box', px, .1, z + s * hw, .08, .62, .08, C.woodDark)); });
      L.say(name, cx, z + 1.02, .4); L.say(ends[0], x0 + .1, z + 1.02, .3, '#6f6a5f'); L.say(ends[1], x1 - .1, z + 1.02, .3, '#6f6a5f');
    };
    tube(-2.2, 'queue', ['← front', 'rear ←']); tube(.75, 'deque', ['↔ front', 'rear ↔']);
    const ST = [C.amber, C.red, C.forest].map(c => RD.alloc(c)), QU = [C.amber, C.red, C.forest].map(c => RD.alloc(c)), DQ = [C.amber, C.red].map(c => RD.alloc(c));
    const SY = i => .2 + i * LV, QX = i => -.5 + i * 1.3, QOUT = -2, QIN = 4.7;
    POSE.linear_structures = { dur: 8, pose(u) {
      ST.forEach((id, i) => {        // 依序從頂端放入，再依相反順序從頂端取出
        const inA = .06 + i * .08, outA = .36 + (2 - i) * .08;
        if (u < inA || u >= outA + .08) { RD.hide(id); return; }
        const y = u < outA ? lerp(LV * levels + 1.4, SY(i), seg(u, inA, inA + .07)) : lerp(SY(i), LV * levels + 1.4, seg(u, outA, outA + .07));
        L.rd(id, SX, y, .1, 1.15, .66, 1.15);
      });
      QU.forEach((id, i) => {        // 從 rear 進，從 front 出，先進先出
        const inA = .06 + i * .08, outA = .36 + i * .08;
        if (u < inA || u >= outA + .08) { RD.hide(id); return; }
        let x = lerp(QIN, QX(i), seg(u, inA, inA + .07));
        if (u >= .36) {
          const k = (u - .36) / .08, f = Math.floor(k), t = seg(k - f, 0, 1);
          x = i === f ? lerp(QX(0), QOUT, t) : lerp(QX(Math.max(0, i - f)), QX(Math.max(0, i - f - 1)), t);
        }
        L.rd(id, x, .14, -2.2, 1.05, .6, .9);
      });
      DQ.forEach((id, i) => {        // 只能從自己這一端出去，不能穿過另一個元素
        const a = .66 + i * .08, o = .84 + i * .05;
        if (u < a || u >= o + .05) { RD.hide(id); return; }
        const tgt = i === 0 ? QX(2) : QX(1), edge = i === 0 ? QIN : QOUT;
        L.rd(id, u < o ? lerp(edge, tgt, seg(u, a, a + .07)) : lerp(tgt, edge, seg(u, o, o + .05)), .14, .75, 1.05, .6, .9);
      });
    } };
    return 2.5;
  };

  // 06 遞迴：層疊塔。fact(4) 一層層往上蓋，到基底條件插旗，再由上往下拆，回傳值逐層送下
  LM.recursion = S => {
    const L = LOC(S), { q } = L, FX = -1.6, FW = 3.5, FD = 3, H = .78;
    q('round', FX, 0, 0, FW + .7, .14, FD + .7, C.stone);
    [[-1, -1], [1, -1], [1, 1], [-1, 1]].forEach(([a, b]) => q('box', FX + a * (FW / 2 + .14), .14, b * (FD / 2 + .14), .1, H * 4 + .2, .1, C.woodDark));
    [['fact(1)', 'return 1'], ['fact(2)', 'return 2 × 1'], ['fact(3)', 'return 3 × 2'], ['fact(4)', 'return 4 × 6']].forEach(([a, b], i) => {
      L.say(a, 2.15, -2.3 + i * 1.2, .38); L.say(b, 2.15, -1.88 + i * 1.2, .3, '#6f6a5f');
    });
    shed(q, -3, 2.65, 1.5, 1, .8, C.roofNavy);
    const P = [C.blue, C.forest, C.red, C.amber].map(c => RD.alloc(c)), win = P.map(() => RD.alloc('#ffe1a0'));
    const pole = CY.alloc(C.white), cloth = RD.alloc(C.gold), tok = SP.alloc(C.gold), y = i => .16 + i * H;
    POSE.recursion = { dur: 6.4, pose(u) {
      P.forEach((id, i) => {
        const a = .05 + i * .09, o = .78 - i * .09;    // 最先呼叫的最後回傳
        if (u < a || u >= o + .08) { RD.hide(id); RD.hide(win[i]); return; }
        const yy = u < o ? lerp(y(i) + 2.6, y(i), seg(u, a, a + .08)) : lerp(y(i), y(i) + 2.6, seg(u, o, o + .08));
        L.rd(id, FX, yy, 0, FW - .1, H - .05, FD - .1);
        L.rd(win[i], FX, yy + .24, FD / 2 - .03, 1.4, .24, .05);
      });
      if (u > .42 && u < .54) { L.cy(pole, FX + 1.1, y(4), 0, .08, 1.3, .08); L.rd(cloth, FX + 1.5, y(4) + .85, 0, .8, .44, .05); }
      else { CY.hide(pole); RD.hide(cloth); }
      if (u > .51 && u < .86) L.sp(tok, FX + FW / 2 + .45, lerp(y(4), y(0), seg(u, .51, .86)), FD / 2 + .32, .44, .44, .44); else SP.hide(tok);
    } };
    return 3.9;
  };

  // 07 搜尋與排序：郵務分揀所。m = 11、線性探查（與教材同一批值）；旁邊的貨箱堆跑一趟氣泡排序
  LM.searching_sorting = S => {
    const L = LOC(S), { q } = L, M_ = 11, s = .68, x0 = -M_ * s / 2, z0 = 2, sx = i => x0 + s * i + s / 2;
    q('round', 0, 0, z0, M_ * s + .25, .1, 1.25, C.stoneDark);
    for (let i = 0; i < M_; i++) { q('box', sx(i), .1, z0, s, .1, 1.1, i % 2 ? C.wall2 : C.cream); L.say(String(i), sx(i), z0 + .85, .28, '#6f6a5f'); }
    shed(q, -2.45, -2.75, 2.5, 1.5, 1.2, C.roof);
    const fun = { x: 2.2, y: 3.05, z: -1.5 };
    q('cyl', fun.x, 0, fun.z, .14, fun.y - .9, .14, C.woodDark);
    q('cone', fun.x, fun.y - 1, fun.z, 1.5, 1.1, 1.5, C.navy, { rx: Math.PI });
    q('cyl', fun.x, fun.y + .08, fun.z, 1.56, .08, 1.56, C.gold);
    L.say('k mod 11', fun.x, fun.z + 1.05, .42);
    const table = new Array(M_).fill(null), KEYS = [54, 26, 93, 17, 77, 31, 44, 55], paths = [];
    KEYS.forEach(k => { let i = k % M_; const hops = [i]; while (table[i] !== null) { i = (i + 1) % M_; hops.push(i); } table[i] = k; paths.push({ k, hops, collide: hops.length > 1 }); });
    INV.searching_sorting = { m: M_, paths };
    const cubes = paths.map(() => RD.alloc(C.amber));
    const BAR = [5, 2, 4, 1, 3], bx = i => -3.3 + i * .6, bz = -.65;
    const frames = [BAR.slice()], cmpAt = [];
    { const a = BAR.slice(); for (let i = 0; i + 1 < a.length; i++) { cmpAt.push(i); if (a[i] > a[i + 1]) [a[i], a[i + 1]] = [a[i + 1], a[i]]; frames.push(a.slice()); } }
    const bars = BAR.map(() => RD.alloc(C.blue));
    L.say('比較相鄰、必要時交換', -2.1, .3, .3, '#6f6a5f');
    const HASH_END = .74;
    POSE.searching_sorting = { dur: 8.5, pose(u) {
      const per = HASH_END / paths.length;
      paths.forEach((p, i) => {
        const a = i * per, b = a + per;
        if (u < a || u >= .985) { RD.hide(cubes[i]); return; }
        // 先飛到雜湊值那一格的上方，再逐格往後探查，找到空格才放下去：不會穿過已經存好的貨箱
        const t = clamp01((u - a) / (b - a)), fall = seg(t, 0, .45), slide = seg(t, .45, .8), drop = seg(t, .8, 1), HOVER = .85;
        RD.color(cubes[i], p.collide && fall >= 1 ? C.red : C.amber);    // 碰撞取決於表的狀態：撞到才變色
        const land = sx(p.hops[0]), fin = sx(p.hops[p.hops.length - 1]);
        const x = fall < 1 ? lerp(fun.x, land, fall) : lerp(land, fin, slide);
        const y = fall < 1 ? lerp(fun.y - 1.1, HOVER, fall) : lerp(HOVER, .2, drop);
        L.rd(cubes[i], x, y, fall < 1 ? lerp(fun.z, z0, fall) : z0, .52, .5, .8);
      });
      const v = clamp01((u - HASH_END) / (1 - HASH_END - .02)), n = frames.length - 1, f = Math.min(n, Math.floor(v * n));
      frames[f].forEach((h, i) => {
        RD.color(bars[i], f < n && u > HASH_END && (i === cmpAt[f] || i === cmpAt[f] + 1) ? C.gold : C.blue);
        L.rd(bars[i], bx(i), 0, bz, .5, h * .3, .5);
      });
    } };
    return 3.2;
  };

  // 08 圖：車站網。不規則車站、帶權軌道、含環；BFS 的層數真的算出來，站牌逐層點亮。看板是相鄰矩陣
  LM.graphs = S => {
    const L = LOC(S), { q } = L, G = DATA.graph, k = .42, Vs = Object.fromEntries(Object.entries(G.vertices).map(([n, [x, z]]) => [n, [x * k - .3, z * k + .15]]));
    const names = Object.keys(Vs), adj = graphAdj(), level = { [G.start]: 0 }, qu = [G.start];
    while (qu.length) { const u = qu.shift(); adj[u].forEach(w => { if (level[w] === undefined) { level[w] = level[u] + 1; qu.push(w); } }); }
    const maxL = Math.max(...Object.values(level));
    INV.graphs = { level, edges: G.edges, adj };
    const WEIGHT = { 'A-B': 7, 'A-C': 5, 'B-D': 2, 'C-D': 3, 'B-E': 4, 'D-G': 6, 'C-F': 8, 'F-G': 1, 'E-G': 9 };
    G.edges.forEach(([a, b]) => {
      const [ax, az] = Vs[a], [bx, bz] = Vs[b], len = Math.hypot(bx - ax, bz - az), ry = Math.atan2(bx - ax, bz - az);
      [-1, 1].forEach(sd => q('box', (ax + bx) / 2 + Math.cos(ry) * .07 * sd, .03, (az + bz) / 2 - Math.sin(ry) * .07 * sd, .045, .05, len, C.ink, { ry }));
      for (let t = .15; t < .9; t += .17) q('box', lerp(ax, bx, t), .01, lerp(az, bz, t), .3, .03, .07, C.woodDark, { ry });
      L.say(String(WEIGHT[a + '-' + b]), (ax + bx) / 2 + .24, (az + bz) / 2 - .2, .26, '#6f6a5f');
    });
    const sign = names.map(n => {
      const [x, z] = Vs[n];
      q('round', x, 0, z, .95, .1, .8, C.stone);
      q('round', x, .1, z, .62, .42, .5, C.wall);
      L.say(n, x, z + .68, .32);
      return RD.alloc(C.stoneDark);
    });
    // 站務看板：相鄰矩陣，與軌道對稱一致
    const mx = 2.6, mz = -2.9, ms = .2, my = .55;
    q('round', mx + .7, 0, mz, 1.82, 1.95, .12, C.woodDark);
    names.forEach((a, i) => names.forEach((b, j) => q('box', mx + j * ms, my + (6 - i) * ms, mz + .07, ms - .03, ms - .03, .02, adj[a].includes(b) ? C.gold : C.stone)));
    L.say('相鄰矩陣', mx + .7, mz + .62, .28, '#6f6a5f'); L.say('BFS 只數邊數', 2.7, 3.2, .32, '#6f6a5f');
    POSE.graphs = { dur: 5.5, pose(u) {
      const now = u <= 0 ? -1 : Math.floor(clamp01((u - .04) / .78) * (maxL + 1));
      names.forEach((n, i) => {
        const l = level[n], reached = u < .985 && l <= now, cur = reached && l === now;
        RD.color(sign[i], cur ? C.gold : reached ? C.forest : C.stoneDark);
        L.rd(sign[i], Vs[n][0], .5, Vs[n][1], .78, cur ? .62 : .34, .62);
      });
    } };
    return 2.4;
  };

  // 09 樹：山頂纜車站。根在山頂、節點沿纜線往下（依序插入 70、31、93、94、14、23、73），左小右大。插入 40：車廂從根逐站比較，走到空位
  LM.trees = S => {
    const L = LOC(S), { q } = L, KEYS = [70, 31, 93, 94, 14, 23, 73], INS = 40, root = { k: KEYS[0] };
    const put = (n, k) => { const s = k < n.k ? 'l' : 'r'; if (n[s]) put(n[s], k); else n[s] = { k }; };
    KEYS.slice(1).forEach(k => put(root, k));
    const path = []; { let n = root; for (;;) { path.push(n); const s = INS < n.k ? 'l' : 'r'; if (!n[s]) { n[s] = { k: INS, fresh: true }; path.push(n[s]); break; } n = n[s]; } }
    const flat = []; const walk_ = (n, d) => { if (!n) return; walk_(n.l, d + 1); n.d = d; n.i = flat.length; flat.push(n); walk_(n.r, d + 1); }; walk_(root, 0);
    const X = n => -3.7 + n.i * 1.06, Y = n => 3.4 - n.d * .98, Zn = -.3;
    INV.trees = { rootY: Y(root), leafY: flat.filter(n => !n.l && !n.r).map(Y), path: path.map(n => n.k), parentOfNew: path[path.length - 2].k, side: INS < path[path.length - 2].k ? 'l' : 'r' };
    // 山丘：根站蓋在最高處
    const hx = X(root);
    q('sphere', hx, -.5, Zn - .55, 4.3, 2.9, 2.5, C.grass2); q('sphere', hx - .4, -.3, Zn - 1, 2.6, 2.6, 1.8, C.grass);
    flat.forEach(n => {
      if (n.fresh) return;
      q('box', X(n), 0, Zn - .04, .1, Y(n), .1, C.woodDark);
      n.id = RD.alloc(C.cream); L.rd(n.id, X(n), Y(n), Zn, .78, .56, .78);
      L.say(String(n.k), X(n), 1.15, .32);
    });
    q('prism', hx, Y(root) + .56, Zn, 1, .34, .9, C.roof);
    flat.forEach(n => [n.l, n.r].forEach(c => { if (c && !c.fresh) { const id = CY.alloc(C.ink); CY.beam(id, L.P(X(n), Y(n) + .12, Zn), L.P(X(c), Y(c) + .5, Zn), .05); } }));
    L.say('插入 40', -2.4, 2.95, .42); L.say('左小右大', -2.4, 2.2, .42); L.say('比較幾次，就走過幾層', 1.5, 2.2, .32, '#6f6a5f');
    const fresh = path[path.length - 1], parent = path[path.length - 2], ball = RD.alloc(C.forest), link = CY.alloc(C.forest);
    const hops = path.length - 1;
    POSE.trees = { dur: 6.2, pose(u) {
      const v = clamp01((u - .05) / .72), f = v * hops, k = Math.min(hops - 1, Math.floor(f)), t = seg(f - k, 0, 1);
      path.forEach((n, i) => { if (n.id !== undefined) RD.color(n.id, u > .03 && u < .985 && i === (f >= hops ? -1 : k) ? C.gold : C.cream); });
      if (u > .03 && u < .985) {
        const a = path[k], b = path[k + 1], lift = .68;
        const x = lerp(X(a), X(b), t), y = lerp(Y(a) + lift, Y(b) + lift, t);
        const land = u > .78 ? seg(u, .78, .86) : 0;
        L.rd(ball, x, f >= hops ? lerp(Y(fresh) + lift, Y(fresh), land) : y, Zn, .72, .54, .72);
        if (land > 0) CY.beam(link, L.P(X(parent), Y(parent) + .12, Zn), L.P(X(fresh), Y(fresh) + .5, Zn), .05); else CY.hide(link);
      } else { RD.hide(ball); CY.hide(link); }
    } };
    return 4.4;
  };

  // 啟航島：燈塔、補給碼頭、修船塢
  LM['00a_why_code'] = S => {
    const { q } = LOC(S);
    q('cyl', 0, 0, 0, 2.0, .35, 2.0, C.stone);
    [C.red, C.white, C.red, C.white].forEach((c, i) => q('cyl', 0, .35 + i * .75, 0, 1.25 - i * .12, .75, 1.25 - i * .12, c));
    q('cyl', 0, 3.35, 0, 1.25, .12, 1.25, C.navy);
    q('cyl', 0, 3.47, 0, .78, .55, .78, '#fff1c2', { glow: true });
    q('cone', 0, 4.02, 0, 1.15, .7, 1.15, C.navy);
    lamps.push([S.x, S.y + 3.75, S.z, 1.6, true]);
    return 4.8;
  };
  LM['00b_setup'] = S => {
    const { q } = LOC(S);
    q('box', 0, 0, .5, 3.4, .12, 2.4, C.wood);
    shed(q, -.5, -.7, 2.2, 1.5, 1.15, C.roofNavy);
    [[.9, 1], [1.3, .3], [.45, 1.35]].forEach(([x, z], i) => q('round', x, .12, z, .5, .5, .5, [C.amber, C.wood, C.red][i]));
    q('cyl', 1.35, 0, -.8, .12, 2, .12, C.woodDark); q('box', 1, 1.9, -.8, .85, .08, .08, C.woodDark); q('round', .68, 1.5, -.8, .24, .3, .24, C.gold);
    return 2.6;
  };
  LM['00c_vscode_windows'] = S => {
    const { q } = LOC(S);
    q('box', 0, 0, 0, 3.2, .1, 2.2, C.stone);
    q('round', 0, .1, 0, 1, .55, 2.5, C.navy); q('round', 0, .62, 0, .84, .08, 2.3, C.wood);
    q('cyl', 0, .68, -.2, .08, 1.3, .08, C.woodDark);
    [[-.72, -.9], [.72, -.9], [-.72, .9], [.72, .9]].forEach(([x, z]) => q('box', x, .1, z, .12, .75, .12, C.wood));
    q('sphere', -1.1, .1, -.55, .32, .32, .32, C.red); q('round', 1.2, .1, .75, .38, .38, .38, C.gold);
    return 2.3;
  };
  // C++ 工坊島：九間工坊，屋頂與招牌各異
  const SIGN = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9'];
  PAGES.filter(p => p.grp === 'workshop').forEach((p, i) => {
    LM[p.stem] = S => {
      const L = LOC(S), roofs = [C.roofNavy, C.roof, C.roofGreen];
      cottage(L.q, 0, 0, 0, roofs[i % 3], i % 2 ? C.wall : C.wall2, 1.02);
      L.q('torus', -.45, .95, .72, .46, .46, .46, C.gold);
      L.say(SIGN[i], 0, 1.15, .42);
      return 2.3;
    };
  });

  PAGES.forEach(p => {
    const s = SLOT[p.stem];
    const h = LM[p.stem](s);
    const isCore = p.grp === 'core';
    B[p.stem] = { x: s.x, y: s.y, z: s.z, top: s.y + h, isle: s.isle, pickR: isCore ? s.isle.radius * .95 : 1.45, isCore };
  });

  /* ── 每座島的裝飾：小屋、兩種樹、花、岩石、路燈、長椅；避開橋的方向，島心留給地標 ── */
  function decorate(I, { houses = 1, trees = 5, edgeOnly = false, avoid = [], rect = false } = {}) {
    const free = a => !nearGap(I, a);
    const spots = [];
    for (let k = 0; k < 18; k++) {
      const a = k / 18 * Math.PI * 2 + rnd() * .2;
      if (!free(a)) continue;
      spots.push(a);
    }
    const take = () => spots.splice(Math.floor(rnd() * spots.length), 1)[0];
    const pos = (a, f) => [I.x + Math.cos(a) * I.angR(a) * f, I.z + Math.sin(a) * I.angR(a) * f];
    const cf = Math.cos(FACE), sf = Math.sin(FACE);
    const ok = (x, z) => {
      if (avoid.some(([ax, az, r]) => Math.hypot(x - ax, z - az) < r)) return false;
      if (!rect) return true;
      const dx = x - I.x, dz = z - I.z;                 // 換回地標的區域座標，避開中央那塊矩形
      const lz = dx * sf + dz * cf;                       // 前方也留空：樹往上投影會擋住地面標示
      return Math.abs(dx * cf - dz * sf) > 4.6 || lz < -3.7 || lz > 5.6;
    };
    for (let h = 0; h < houses && spots.length; h++) {
      const a = take(), [x, z] = pos(a, .66);
      if (ok(x, z)) cottage(at(x, I.top, z, -a + Math.PI / 2), 0, 0, 0, [C.roof, C.roofNavy, C.roofGreen][(h + Math.round(x)) % 3], C.wall, .74 + rnd() * .14);
    }
    for (let t = 0; t < trees && spots.length; t++) {
      const a = take(), [x, z] = pos(a, edgeOnly ? .86 : .7 + rnd() * .12);
      if (!ok(x, z)) continue;
      (t % 2 ? pine : tree)(at(x, I.top, z), 0, 0, .6 + rnd() * .3, t);
    }
    for (let k = 0; k < 2 && spots.length; k++) { const [x, z] = pos(take(), .88); if (ok(x, z)) flowers(at(x, I.top, z), 0, 0, Math.round(x) + k); }
    for (let k = 0; k < 2 && spots.length; k++) { const [x, z] = pos(take(), .9); if (ok(x, z)) bush(at(x, I.top, z), 0, 0, .8 + rnd() * .3, k); }
    if (spots.length) { const [x, z] = pos(take(), .88); if (ok(x, z)) { lamp(at(x, I.top, z), 0, 0); lamps.push([x, I.top + 1.42, z]); } }
    for (let r = 0; r < 2; r++) { const a = rnd() * Math.PI * 2; if (!nearGap(I, a, .5)) rock(at(I.x + Math.cos(a) * I.angR(a) * 1.02, 0, I.z + Math.sin(a) * I.angR(a) * 1.02), 0, 0, .8 + rnd() * .5); }
  }
  coreIsles.forEach(I => decorate(I, { houses: 0, trees: 7, edgeOnly: true, rect: true }));
  {
    const I = SAT_ISLE.workshop;
    PAGES.filter(p => p.grp === 'workshop').forEach(p => { const s = SLOT[p.stem]; lamp(at(s.x + 1.4, I.top, s.z + 1.2), 0, 0); lamps.push([s.x + 1.4, I.top + 1.42, s.z + 1.2]); });
    decorate(I, { houses: 0, trees: 8, edgeOnly: true, avoid: PAGES.filter(p => p.grp === 'workshop').map(p => [SLOT[p.stem].x, SLOT[p.stem].z, 2.2]) });
  }
  {
    const I = SAT_ISLE.pre;
    decorate(I, { houses: 0, trees: 6, edgeOnly: true, avoid: PAGES.filter(p => p.grp === 'pre').map(p => [SLOT[p.stem].x, SLOT[p.stem].z, 2.4]) });
  }
  // 外圍的小沙洲與礁岩，替畫面收邊
  const framed = isles.slice();          // 取景只算主要島嶼；外圍沙洲可以出血
  const sandbars = [[-37, 8, 2.2], [36, 10, 2.6], [-38, -22, 1.8], [38, -14, 2], [-2, 40, 2], [34, 32, 1.8], [-8, -40, 1.6]];
  sandbars.forEach(([u, v, r], k) => {
    const I = makeIsle({ u, v, radius: r, seed: 300 + k * 13, grass: 'grass3' });
    if (k % 2 === 0) tree(at(I.x, I.top, I.z), 0, 0, .7, k); else rock(at(I.x, I.top - .1, I.z), 0, 0, .9);
  });

  mergeIsles();
  flushParts();
  // 接觸暗部：柔邊的深色圓盤，貼在地面上（不參與陰影）
  {
    const cv = document.createElement('canvas'); cv.width = cv.height = 64;
    const g = cv.getContext('2d'), gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr.addColorStop(0, 'rgba(40,52,40,.55)'); gr.addColorStop(.55, 'rgba(40,52,40,.25)'); gr.addColorStop(1, 'rgba(40,52,40,0)');
    g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
    const tex = new THREE.CanvasTexture(cv);
    const geo = new THREE.PlaneGeometry(1, 1); geo.rotateX(-Math.PI / 2);
    const mesh = new THREE.InstancedMesh(geo, new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, opacity: .55 }), ao.length);
    const o = new THREE.Object3D();
    ao.forEach(([x, y, z, r], i) => { o.position.set(x, y + .015, z); o.scale.set(r * 2.2, 1, r * 2.2); o.updateMatrix(); mesh.setMatrixAt(i, o.matrix); });
    mesh.renderOrder = 2; world.add(mesh);
  }
  /* 地面標示：貼花圖集，只畫一次 */
  const decalMat = (() => {
    const cv = document.createElement('canvas'); cv.width = 2048; cv.height = 1024;
    const g = cv.getContext('2d'), PX = 44;
    g.font = `700 ${PX}px ui-monospace,'SFMono-Regular','Cascadia Mono',Menlo,Consolas,'Noto Sans CJK TC','Microsoft JhengHei',monospace`;
    g.textBaseline = 'middle'; g.textAlign = 'center';
    let cx = 2, cy = 2; const pos = [], uv = [], idx = []; const H = PX + 22, c = Math.cos(FACE), sn = Math.sin(FACE); let n = 0;
    decals.forEach(d => {
      const tw = Math.ceil(g.measureText(d.text).width) + 26;
      if (cx + tw > 2046) { cx = 2; cy += H + 4; }
      g.fillStyle = 'rgba(255,253,247,.86)'; g.beginPath(); g.roundRect(cx, cy, tw, H, 12); g.fill();
      g.fillStyle = d.ink; g.fillText(d.text, cx + tw / 2, cy + H / 2 + 2);
      const hw = d.size * .5 * tw / PX, hh = d.size * .5 * H / PX;
      [[-hw, -hh], [hw, -hh], [hw, hh], [-hw, hh]].forEach(([x, z]) => pos.push(d.x + x * c + z * sn, d.y, d.z - x * sn + z * c));
      uv.push(cx / 2048, 1 - cy / 1024, (cx + tw) / 2048, 1 - cy / 1024, (cx + tw) / 2048, 1 - (cy + H) / 1024, cx / 2048, 1 - (cy + H) / 1024);
      idx.push(n, n + 2, n + 1, n, n + 3, n + 2); n += 4; cx += tw + 4;
    });
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy());
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); geo.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); geo.setIndex(idx);
    const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2 });
    const mesh = new THREE.Mesh(geo, mat); mesh.frustumCulled = false; mesh.renderOrder = 3; world.add(mesh);
    return mat;
  })();

  /* ═════════ 海面：頂點起伏＋依離岸距離的淺深色 ═════════ */
  const SEA_DAY_SHALLOW = new THREE.Color('#86dcd8'), SEA_DAY_DEEP = new THREE.Color('#3f9fcb');
  const seaGeo = new THREE.PlaneGeometry(300, 300, 90, 90); seaGeo.rotateX(-Math.PI / 2);
  {
    const pos = seaGeo.attributes.position, cols = new Float32Array(pos.count * 3), c = new THREE.Color();
    for (let i = 0; i < pos.count; i++) {
      const x = pos.getX(i), z = pos.getZ(i);
      let d = 1e9; isles.forEach(I => { d = Math.min(d, Math.hypot(x - I.x, z - I.z) - I.radius * 1.1); });
      const t = Math.min(1, Math.max(0, d / 12)), k = t * t * (3 - 2 * t);
      c.copy(SEA_DAY_SHALLOW).lerp(SEA_DAY_DEEP, k);
      cols[i * 3] = c.r; cols[i * 3 + 1] = c.g; cols[i * 3 + 2] = c.b;
    }
    seaGeo.setAttribute('color', new THREE.BufferAttribute(cols, 3));
  }
  const seaU = { uTime: { value: 0 } };
  const seaMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: .55, metalness: 0 });
  seaMat.onBeforeCompile = sh => {
    sh.uniforms.uTime = seaU.uTime;
    sh.vertexShader = 'uniform float uTime;\n' + sh.vertexShader.replace('#include <begin_vertex>',
      '#include <begin_vertex>\n transformed.y += sin(position.x * .32 + uTime * .9) * .05 + cos(position.z * .27 + uTime * .7) * .05;');
  };
  const sea = new THREE.Mesh(seaGeo, seaMat); sea.position.y = -.02; sea.receiveShadow = true; world.add(sea);
  // 風格化短浪線
  const dash = new THREE.InstancedMesh(new RoundedBoxGeometry(1, .02, .1, 1, .04), basic('#ffffff', { transparent: true, opacity: .6, depthWrite: false, fog: false }), 46);
  const dashes = [];
  for (let k = 0, n = 0; k < 2000 && n < 46; k++) {
    const x = (rnd() - .5) * 110, z = (rnd() - .5) * 110;
    if (isles.some(I => Math.hypot(x - I.x, z - I.z) < I.radius * 1.7)) continue;
    dashes.push({ x, z, l: .8 + rnd() * 1.0, ph: rnd() * 6 }); n++;
  }
  const dObj = new THREE.Object3D();
  const placeDashes = t => {
    dashes.forEach((d, i) => {
      dObj.position.set(d.x + Math.sin(t * .25 + d.ph) * .6, .06, d.z + Math.cos(t * .2 + d.ph) * .3);
      dObj.rotation.set(0, FACE, 0);              // 與畫面水平方向平行 dObj.scale.set(d.l * (.75 + .25 * Math.sin(t * .6 + d.ph)), 1, 1);
      dObj.updateMatrix(); dash.setMatrixAt(i, dObj.matrix);
    });
    dash.count = dashes.length; dash.instanceMatrix.needsUpdate = true;
  };
  placeDashes(0); world.add(dash);
  life.push(t => { seaU.uTime.value = t; placeDashes(t); });

  /* ═════════ 燈光 ═════════ */
  const hemi = new THREE.HemisphereLight(DAY.hemiSky, DAY.hemiGround, DAY.hemi); world.add(hemi);
  const bounds = isles.reduce((b, I) => ({ minX: Math.min(b.minX, I.x - I.radius), maxX: Math.max(b.maxX, I.x + I.radius),
    minZ: Math.min(b.minZ, I.z - I.radius), maxZ: Math.max(b.maxZ, I.z + I.radius) }), { minX: 1e9, maxX: -1e9, minZ: 1e9, maxZ: -1e9 });
  const center = new THREE.Vector3((bounds.minX + bounds.maxX) / 2, 0, (bounds.minZ + bounds.maxZ) / 2);
  const sun = new THREE.DirectionalLight(DAY.sun, DAY.sunI);
  sun.position.set(center.x - 30, 55, center.z + 24); sun.target.position.copy(center);
  sun.castShadow = true;
  const SM = window.innerWidth < 768 ? 1024 : 2048;   // 陰影只烘一次
  sun.shadow.mapSize.set(SM, SM);
  const ext = Math.max(bounds.maxX - bounds.minX, bounds.maxZ - bounds.minZ) / 2 + 6;
  Object.assign(sun.shadow.camera, { left: -ext, right: ext, top: ext, bottom: -ext, near: 1, far: 160 });
  sun.shadow.camera.updateProjectionMatrix();
  sun.shadow.bias = -.0005; sun.shadow.normalBias = .07; sun.shadow.radius = 2;
  world.add(sun, sun.target);
  const fill = new THREE.DirectionalLight('#d6ecf2', DAY.fill); fill.position.set(center.x + 40, 30, center.z - 50); world.add(fill);
  /* ═════════ 生活感：小人、帆船、鳥、雲 ═════════ */
  const blobMat = basic('#20343a', { transparent: true, opacity: .16, depthWrite: false });
  const blobGeo = new THREE.CircleGeometry(.34, 16); blobGeo.rotateX(-Math.PI / 2);
  function person(shirt, pants, skin, hair) {
    const g = new THREE.Group(), body = new THREE.Group(); g.add(body);
    const m = c => std(c, { roughness: .8 });
    const limb = (c, x, y, w, h) => { const piv = new THREE.Group(); piv.position.set(x, y, 0); const b = new THREE.Mesh(GEO.round, m(c)); b.scale.set(w, h, w); b.position.y = -h / 2; piv.add(b); body.add(piv); return piv; };
    const legL = limb(pants, -.09, .42, .13, .42), legR = limb(pants, .09, .42, .13, .42);
    const torso = new THREE.Mesh(GEO.round, m(shirt)); torso.scale.set(.36, .42, .22); torso.position.y = .63; body.add(torso);
    const armL = limb(shirt, -.24, .8, .1, .36), armR = limb(shirt, .24, .8, .1, .36);
    const head = new THREE.Mesh(GEO.sphere, m(skin)); head.scale.setScalar(.3); head.position.y = 1.0; body.add(head);
    const cap = new THREE.Mesh(GEO.sphere, m(hair)); cap.scale.set(.32, .18, .32); cap.position.set(0, 1.08, -.02); body.add(cap);
    const blob = new THREE.Mesh(blobGeo, blobMat); blob.position.y = .02; g.add(blob);
    g.userData = { legL, legR, armL, armR, body };
    return g;
  }
  const people = [];
  const PALETTE = [['#c4553a', '#3f5b80'], ['#3f7f61', '#4f5a55'], ['#e7a33e', '#2f4566'], ['#4f78ab', '#7a5c3e'], ['#f0c7a5', '#3f7f61'], ['#fff4de', '#924231']];
  const SKIN = ['#f1c9a5', '#d9a77f', '#b98063', '#f6dcc0'], HAIR = ['#3b2a20', '#1f1d1c', '#7a5c3e', '#c9a46a'];
  bridges.forEach((b, i) => {
    if (people.length >= 11) return;
    const [sh, pa] = PALETTE[i % PALETTE.length];
    const g = person(sh, pa, SKIN[i % 4], HAIR[(i + 1) % 4]); g.scale.setScalar(.72); instancify(g);
    const path = [];
    const inA = b.pts[0].clone().lerp(new THREE.Vector3(b.A.x, b.pts[0].y, b.A.z), .45), inB = b.pts[b.pts.length - 1].clone().lerp(new THREE.Vector3(b.B.x, b.pts[b.pts.length - 1].y, b.B.z), .45);
    path.push(inA, ...b.pts, inB);
    const lens = [0]; for (let k = 1; k < path.length; k++) lens.push(lens[k - 1] + path[k].distanceTo(path[k - 1]));
    people.push({ g, path, lens, total: lens[lens.length - 1], s: rnd() * lens[lens.length - 1], dir: rnd() < .5 ? 1 : -1, wait: 0, speed: .75 + rnd() * .35 });
  });
  const pv = new THREE.Vector3();
  const walk = (t, dt) => people.forEach(P => {
    const u = P.g.userData;
    if (P.wait > 0) { P.wait -= dt; u.legL.rotation.x = u.legR.rotation.x = u.armL.rotation.x = 0; u.armR.rotation.x = Math.sin(t * 6) * .8 - .8; return; }
    P.s += P.dir * P.speed * dt;
    if (P.s > P.total || P.s < 0) { P.s = Math.max(0, Math.min(P.total, P.s)); P.dir *= -1; P.wait = 1 + rnd() * 2.5; }
    let k = 1; while (k < P.lens.length - 1 && P.lens[k] < P.s) k++;
    const f = (P.s - P.lens[k - 1]) / Math.max(1e-6, P.lens[k] - P.lens[k - 1]);
    pv.copy(P.path[k - 1]).lerp(P.path[k], f); P.g.position.copy(pv);
    const a = P.path[k], b0 = P.path[k - 1];
    P.g.rotation.y = Math.atan2((a.x - b0.x) * P.dir, (a.z - b0.z) * P.dir);
    const sw = Math.sin(t * 8 * P.speed) * .55;
    u.legL.rotation.x = sw; u.legR.rotation.x = -sw; u.armL.rotation.x = -sw * .8; u.armR.rotation.x = sw * .8;
    u.body.position.y = Math.abs(Math.sin(t * 8 * P.speed)) * .04;
  });
  walk(1.3, 0); life.push(walk);

  /* ── 嚮導阿迭（迭代器）：深藍外套、頭上一個 -> 形帽，什麼都不提，因為迭代器不存資料，只負責指向 ──
     跳到下一站是和 fly 一樣的狀態，由 frame() 裡的 stepGuide() 推進，不另開繪製迴圈。 */
  const guide = (() => {
    const g = person('#2c3e7a', '#3f4a5c', '#f1c9a5', '#3b2a20'), u = g.userData;
    const m = c => std(c);
    const shaft = new THREE.Mesh(GEO.round, m(C.gold)); shaft.scale.set(.44, .1, .1); shaft.position.set(-.06, 1.32, 0); u.body.add(shaft);
    const head = new THREE.Mesh(GEO.cone, m(C.gold)); head.scale.set(.3, .3, .3); head.rotation.z = -Math.PI / 2; head.position.set(.3, 1.32, 0); u.body.add(head);
    const scarf = new THREE.Mesh(GEO.round, m('#c0392b')); scarf.scale.set(.38, .08, .25); scarf.position.y = .84; u.body.add(scarf);
    g.scale.setScalar(1.6);                          // 比路人（.72）大一倍，遠看也認得出來
    world.add(g);
    return g;
  })();
  const camFlat = new THREE.Vector3();
  // 某一站的落腳點：島上朝鏡頭那一側的前緣、略偏一邊，免得被地標擋住
  function guideSpot(stem, out) {
    const b = B[stem]; if (!b) return null;
    camFlat.copy(camera.position).sub(controls.target); camFlat.y = 0; camFlat.normalize();
    const a = Math.atan2(camFlat.z, camFlat.x) - .4, r = b.isCore ? b.isle.radius * .86 : 1.6;
    return out.set(b.x + Math.cos(a) * r, b.y, b.z + Math.sin(a) * r);
  }
  function faceCamera() {
    guide.rotation.y = Math.atan2(camera.position.x - guide.position.x, camera.position.z - guide.position.z);
  }
  let hop = null, waveUntil = 0;
  function stepGuide(now) {
    if (!hop) return false;
    const k = Math.min(1, (now - hop.t0) / hop.dur), e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
    guide.position.lerpVectors(hop.from, hop.to, e);
    guide.position.y += Math.sin(Math.PI * k) * hop.h;
    const u = guide.userData; u.legL.rotation.x = -.6; u.legR.rotation.x = .3; u.armR.rotation.x = -2.4 * Math.sin(Math.PI * k);
    if (k >= 1) { hop = null; faceCamera(); waveUntil = now + 2600; u.legL.rotation.x = u.legR.rotation.x = 0; }
    return true;
  }
  function guideTo(stem) {
    const to = guideSpot(stem, new THREE.Vector3()); if (!to) return;
    if (!motion()) { hop = null; guide.position.copy(to); faceCamera(); requestRender(); return; }
    const d = to.distanceTo(guide.position);
    hop = { from: guide.position.clone(), to, t0: performance.now(), dur: Math.min(1300, 550 + d * 14), h: 1.1 + Math.min(4, d * .1) };
    guide.rotation.y = Math.atan2(to.x - guide.position.x, to.z - guide.position.z);
    requestRender();
  }
  const guideHomeStem = PAGES[0].stem;   // 平時站在啟航島的燈塔旁
  anims.push(t => {
    if (hop) return;
    const u = guide.userData, now = t * 1000;
    // 平時偶爾揮手（約每 9 秒一次）；剛到一站時揮比較久
    const waving = now < waveUntil || (t % 9) < 1.4;
    u.armR.rotation.x = waving ? -2.5 + Math.sin(t * 9) * .35 : 0;
    u.armR.rotation.z = waving ? .25 : 0;
    u.armL.rotation.x = -.35 + Math.sin(t * 1.6) * .08;
    u.body.position.y = Math.abs(Math.sin(t * 1.6)) * .025;
  });

  const WAKE_GEO = new THREE.PlaneGeometry(.7, 2.6), WAKE_MAT = basic('#ffffff', { transparent: true, opacity: .35, depthWrite: false });
  function sailboat(sail, hull) {
    const g = new THREE.Group();
    const h = new THREE.Mesh(GEO.round, std(hull, { roughness: .8 })); h.scale.set(.75, .35, 1.9); h.position.y = .12; g.add(h);
    const deck = new THREE.Mesh(GEO.round, std(C.wood)); deck.scale.set(.62, .08, 1.6); deck.position.y = .3; g.add(deck);
    const mast = new THREE.Mesh(GEO.cyl, std(C.woodDark)); mast.scale.set(.07, 2.0, .07); mast.position.y = 1.3; g.add(mast);
    const s = new THREE.Mesh(GEO.prism, std(sail, { roughness: .9, side: THREE.DoubleSide })); s.scale.set(.06, 1.6, 1.2); s.position.set(0, 1.35, -.2); g.add(s);
    const wake = new THREE.Mesh(WAKE_GEO, WAKE_MAT);
    wake.rotation.x = -Math.PI / 2; wake.position.set(0, .04, -2.1); g.add(wake);
    return g;
  }
  const boats = [[C.cream, C.navy, 46, 30, .05, 0], [C.redL, C.white, 46, 30, .05, Math.PI], [C.white, C.red, 9, 9, -.12, 1]].map(([s, h, a, b, w, ph], i) => {
    const g = sailboat(s, h); instancify(g);
    const c0 = i === 2 ? new THREE.Vector3(SAT_ISLE.pre.x, 0, SAT_ISLE.pre.z) : center.clone();
    return { g, a, b, w, ph, c0 };
  });
  const sail = t => boats.forEach(B0 => {
    const ang = t * B0.w + B0.ph, rot = -FACE;
    const lx = Math.cos(ang) * B0.a, lz = Math.sin(ang) * B0.b;
    const x = B0.c0.x + lx * Math.cos(rot) - lz * Math.sin(rot), z = B0.c0.z + lx * Math.sin(rot) + lz * Math.cos(rot);
    const dx = -Math.sin(ang) * B0.a * Math.sign(B0.w), dz = Math.cos(ang) * B0.b * Math.sign(B0.w);
    const wx = dx * Math.cos(rot) - dz * Math.sin(rot), wz = dx * Math.sin(rot) + dz * Math.cos(rot);
    B0.g.position.set(x, .05 + Math.sin(t * 1.4 + B0.ph) * .05, z);
    B0.g.rotation.set(Math.sin(t * 1.1 + B0.ph) * .04, Math.atan2(wx, wz), Math.sin(t * .9) * .05);
  });
  sail(2); life.push(sail);

  const birds = new THREE.Group();
  const birdMat = std('#fbfaf2', { roughness: .8 });
  const flock = Array.from({ length: 7 }, (_, i) => {
    const g = new THREE.Group();
    const body = new THREE.Mesh(GEO.sphere, birdMat); body.scale.set(.18, .14, .42); g.add(body);
    const wings = [-1, 1].map(s => { const piv = new THREE.Group(); const w = new THREE.Mesh(GEO.box, birdMat); w.scale.set(.6, .03, .22); w.position.x = .3 * s; piv.add(w); g.add(piv); return piv; });
    g.position.set((i % 3 - 1) * 1.1, (i % 2) * .4, -Math.floor(i / 2) * .9); birds.add(g);
    return { g, wings, ph: i * .7 };
  });
  const flapBirds = t => {
    const a = t * .07;
    birds.position.set(center.x + Math.cos(a) * 26, 12 + Math.sin(t * .5) * .6, center.z + Math.sin(a) * 18);
    birds.rotation.y = -a + Math.PI;
    flock.forEach(b => { const f = Math.sin(t * 7 + b.ph) * .7; b.wings[0].rotation.z = f; b.wings[1].rotation.z = -f; });
  };
  flapBirds(3); life.push(flapBirds); instancify(birds);

  const cloudMat = std('#ffffff', { roughness: 1, transparent: true, opacity: .92, emissive: '#ffffff', emissiveIntensity: .25 });
  const clouds = [[-38, 30], [36, 30], [-46, -4], [44, -2]].map(([u, v], k) => {
    const g = new THREE.Group(); const w = toWorld(u, v);
    [[0, 0, 0, 2.2], [1.6, -.3, .3, 1.6], [-1.6, -.4, -.2, 1.5], [.5, .5, -.6, 1.4]].forEach(([x, y, z, r]) => {
      const m = new THREE.Mesh(GEO.sphere, cloudMat); m.scale.set(r * 1.4, r, r * 1.2); m.position.set(x, y, z); g.add(m);
    });
    g.position.set(w.x, 9 + k % 2, w.z); instancify(g);
    return { g, x0: w.x, z0: w.z, ph: k * 1.7 };
  });
  const drift = t => clouds.forEach(c => { c.g.position.x = c.x0 + Math.sin(t * .03 + c.ph) * 6; c.g.position.z = c.z0 + Math.cos(t * .025 + c.ph) * 4; });
  life.push(drift);

  instancify(dynRoot);
  finishProxies();

  /* ═════════ 夜：星星、光暈 ═════════ */
  const glowTex = (() => {
    const cv = document.createElement('canvas'); cv.width = cv.height = 64;
    const g = cv.getContext('2d'), gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr.addColorStop(0, 'rgba(255,214,140,1)'); gr.addColorStop(.35, 'rgba(255,190,100,.45)'); gr.addColorStop(1, 'rgba(255,170,80,0)');
    g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
    const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t;
  })();
  const haloMat = new THREE.SpriteMaterial({ map: glowTex, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending });
  const nightOnly = [];            // 白天完全不畫（透明度 0 也會佔繪製呼叫）
  lamps.forEach(([x, y, z, s = 1.1]) => { const sp = new THREE.Sprite(haloMat); sp.position.set(x, y, z); sp.scale.setScalar(s * 1.6); world.add(sp); nightOnly.push(sp); });
  // 路燈照在地上的光斑（俯瞰視角看不到天空，所以不放星星）
  const poolMat = new THREE.MeshBasicMaterial({ map: glowTex, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending });
  const poolGeo = new THREE.PlaneGeometry(1, 1); poolGeo.rotateX(-Math.PI / 2);
  lamps.forEach(([x, y, z, s = 1.1, noPool]) => { if (noPool) return; const m = new THREE.Mesh(poolGeo, poolMat); m.position.set(x, y - 1.38, z); m.scale.set(s * 3.2, 1, s * 3.2); m.renderOrder = 3; world.add(m); nightOnly.push(m); });

  let night = 0, nightTarget = 0;
  const cA = new THREE.Color(), cB = new THREE.Color();
  const mix = (a, b, k) => cA.set(a).lerp(cB.set(b), k);
  function applyNight(k) {
    world.background.copy(mix(DAY.bg, NIGHT.bg, k)); world.fog.color.copy(world.background);
    hemi.color.copy(mix(DAY.hemiSky, NIGHT.hemiSky, k)); hemi.groundColor.copy(mix(DAY.hemiGround, NIGHT.hemiGround, k));
    hemi.intensity = DAY.hemi + (NIGHT.hemi - DAY.hemi) * k;
    sun.color.copy(mix(DAY.sun, NIGHT.sun, k)); sun.intensity = DAY.sunI + (NIGHT.sunI - DAY.sunI) * k;
    fill.intensity = DAY.fill + (NIGHT.fill - DAY.fill) * k;
    seaMat.color.copy(mix(DAY.sea, NIGHT.sea, k));
    renderer.toneMappingExposure = DAY.exposure + (NIGHT.exposure - DAY.exposure) * k;
    glowMat.emissiveIntensity = k * 1.5; haloMat.opacity = k * .95; poolMat.opacity = k * .7;
    decalMat.color.copy(mix('#ffffff', '#8c9ab8', k));
    nightOnly.forEach(o => { o.visible = k > .01; });
    cloudMat.opacity = .92 - k * .5; cloudMat.emissiveIntensity = .25 - k * .2;
    M.foam.color.copy(mix(C.foam, '#8fa3bd', k));
    dash.material.opacity = .6 - k * .45;
  }
  applyNight(0);
  /* ═════════ 足跡、選取、先備高亮 ═════════ */
  const GLOW_VISIT = new THREE.MeshLambertMaterial({ color: '#ffe0a0', emissive: '#ffb84d', emissiveIntensity: .9 });
  const FLAG = std(C.forest, { roughness: .8, side: THREE.DoubleSide });
  const refMat = basic('#3f5b9a', { transparent: true, opacity: .85, depthWrite: false });
  const refGeo = new THREE.TorusGeometry(1, .07, 6, 40); refGeo.rotateX(Math.PI / 2);
  PAGES.forEach(p => {
    const b = B[p.stem], I = b.isle;
    // 島邊（朝向鏡頭）的燈籠與旗子位置
    const a = Math.atan2(SQ, SQ) + (b.isCore ? .55 : 0);
    const ex = b.isCore ? I.x + Math.cos(a) * I.angR(a) * .8 : b.x + .9, ez = b.isCore ? I.z + Math.sin(a) * I.angR(a) * .8 : b.z + .9;
    const lan = new THREE.Group(); lan.position.set(ex, I.top, ez);
    const post = new THREE.Mesh(GEO.cyl, std(C.woodDark)); post.scale.set(.07, 1.05, .07); post.position.y = .52; lan.add(post);
    const bulb = new THREE.Mesh(GEO.round, GLOW_VISIT); bulb.scale.set(.24, .3, .24); bulb.position.y = 1.15; lan.add(bulb);
    lan.visible = false; world.add(lan);
    const fx = b.isCore ? I.x + Math.cos(a + .5) * I.angR(a + .5) * .72 : b.x - .9, fz = b.isCore ? I.z + Math.sin(a + .5) * I.angR(a + .5) * .72 : b.z + .9;
    const flag = new THREE.Group(); flag.position.set(fx, I.top, fz);
    const pole = new THREE.Mesh(GEO.cyl, std(C.white)); pole.scale.set(.06, 1.9, .06); pole.position.y = .95; flag.add(pole);
    const cloth = new THREE.Mesh(GEO.prism, FLAG); cloth.scale.set(.05, .5, .7); cloth.rotation.x = Math.PI / 2; cloth.position.set(0, 1.62, .35); flag.add(cloth);
    flag.visible = false; world.add(flag);
    const ref = new THREE.Mesh(refGeo, refMat); ref.scale.setScalar(b.isCore ? I.radius * 1.12 : 1.55); ref.position.set(b.isCore ? I.x : b.x, I.top + .06, b.isCore ? I.z : b.z); ref.visible = false; world.add(ref);
    Object.assign(b, { lan, flag, ref });
  });
  const marker = new THREE.Mesh(new THREE.ConeGeometry(.42, .9, 4), new THREE.MeshLambertMaterial({ color: '#f3c15a', emissive: '#f0a83a', emissiveIntensity: .6 }));
  marker.rotation.x = Math.PI; marker.visible = false; world.add(marker);
  let selected = null, refs = [];
  anims.push(t => {
    if (selected) marker.position.y = B[selected].top + 1.4 + Math.sin(t * 3) * .18;
    refMat.opacity = .55 + .35 * Math.sin(t * 3);
  });
  // 先備依賴線：從選到的正課島拉一條虛線航線到相關工坊（森林綠；和紅繩指標、木造拱橋都不同）
  const DASH_N = 18, wireIds = Array.from({ length: 3 * DASH_N }, () => CY.alloc(C.forest));
  function setWires(stem) {
    wireIds.forEach(id => CY.hide(id));
    if (!stem) return;
    const A = B[stem];
    BY[stem].refs.slice(0, 3).forEach((r, k) => {
      const Q = B[r]; if (!Q) return;
      const a = LOC(A).P(-1.4 + k * 1.4, .25, -5.2), b = new THREE.Vector3(Q.x, Q.y + 2.2, Q.z);
      const m = a.clone().lerp(b, .5); m.y += 2.4 + k * .6;
      const curve = new THREE.QuadraticBezierCurve3(a, m, b);
      for (let i = 0; i < DASH_N; i++) {
        const t0 = (i + .1) / DASH_N, t1 = (i + .8) / DASH_N;
        CY.beam(wireIds[k * DASH_N + i], curve.getPoint(t0), curve.getPoint(t1), .1);
      }
    });
  }

  /* ═════════ 相機與操作 ═════════ */
  const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, .1, 500);
  const POLAR = 52 * Math.PI / 180, DIST = 110;
  const HOME = center.clone();
  const controls = new OrbitControls(camera, canvas);
  controls.enablePan = false;
  controls.minPolarAngle = 46 * Math.PI / 180; controls.maxPolarAngle = 62 * Math.PI / 180;
  controls.minZoom = .7; controls.maxZoom = 5;
  controls.enableDamping = motion(); controls.dampingFactor = .08;
  controls.rotateSpeed = .6; controls.zoomSpeed = 1.1;
  controls.touches = { ONE: THREE.TOUCH.ROTATE, TWO: THREE.TOUCH.DOLLY_ROTATE };
  camera.position.set(HOME.x + Math.sin(POLAR) * Math.sin(FACE) * DIST, Math.cos(POLAR) * DIST, HOME.z + Math.sin(POLAR) * Math.cos(FACE) * DIST);
  camera.lookAt(HOME); camera.updateMatrixWorld();
  // 自動取景：把主要島嶼（含地標與標籤高度）投影到鏡頭的左右／上下軸，取外接範圍
  const RV = new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 0), UV = new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 1);
  const FV = camera.getWorldDirection(new THREE.Vector3());
  const FIT = { r: 30, u: 18 };
  {
    let r0 = 1e9, r1 = -1e9, u0 = 1e9, u1 = -1e9; const q = new THREE.Vector3();
    framed.forEach(I => {
      for (let k = 0; k < 16; k++) {
        const a = k / 16 * Math.PI * 2;
        [0, I.top + 3].forEach(h => {
          q.set(I.x + Math.cos(a) * I.radius * 1.15 - HOME.x, h, I.z + Math.sin(a) * I.radius * 1.15 - HOME.z);
          const r = q.dot(RV), u = q.dot(UV); r0 = Math.min(r0, r); r1 = Math.max(r1, r); u0 = Math.min(u0, u); u1 = Math.max(u1, u);
        });
      }
    });
    FIT.r = (r1 - r0) / 2; FIT.u = (u1 - u0) / 2;
    HOME.addScaledVector(RV, (r0 + r1) / 2).addScaledVector(UV, (u0 + u1) / 2);
    HOME.addScaledVector(FV, -HOME.y / FV.y);              // 沿視線滑回地面，畫面位置不變
  }
  controls.target.copy(HOME);
  camera.position.copy(HOME).addScaledVector(FV, -DIST); camera.lookAt(HOME);
  guideSpot(guideHomeStem, guide.position); faceCamera();
  // 視錐：寬度涵蓋整個群島（約 ±36），窄螢幕略裁兩翼
  function resize() {
    const w = stage.clientWidth, h = stage.clientHeight;
    if (!w || !h) return;
    const aspect = w / h;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, DPRS[dprLevel]));
    renderer.setSize(w, h, false);
    // 上方多留一點給島嶼跳轉鈕；窄螢幕允許兩翼略為裁切
    const half = Math.max(FIT.u * 1.12 + 1.5, FIT.r * 1.03 / aspect);
    Object.assign(camera, { left: -half * aspect, right: half * aspect, top: half, bottom: -half });
    camera.updateProjectionMatrix(); measureTags(); tagsDirty = true; requestRender();
  }

  let fly = null;
  function flyTo(target, zoom) {
    if (!motion()) {
      const off = camera.position.clone().sub(controls.target);
      controls.target.copy(target); camera.position.copy(target).add(off);
      camera.zoom = zoom; camera.updateProjectionMatrix(); controls.update(); requestRender(); return;
    }
    fly = { from: controls.target.clone(), to: target.clone(), z0: camera.zoom, z1: zoom, t0: performance.now(), dur: 800 };
    requestRender();
  }
  function stepFly(now) {
    if (!fly) return false;
    const k = Math.min(1, (now - fly.t0) / fly.dur), e = 1 - Math.pow(1 - k, 3);
    const off = camera.position.clone().sub(controls.target);
    controls.target.lerpVectors(fly.from, fly.to, e); camera.position.copy(controls.target).add(off);
    camera.zoom = fly.z0 + (fly.z1 - fly.z0) * e; camera.updateProjectionMatrix();
    if (k >= 1) fly = null;
    return true;
  }

  /* ── 拾取：正課整座島、附屬島的單棟建築 ── */
  const picks = [];
  const pickMat = new THREE.MeshBasicMaterial({ colorWrite: false, depthWrite: false });
  PAGES.forEach(p => {
    const b = B[p.stem];
    const geo = b.isCore ? new THREE.CylinderGeometry(b.pickR, b.pickR, b.top - b.y + 2.2, 16) : new THREE.BoxGeometry(2.4, b.top - b.y + 1.4, 2.4);
    const m = new THREE.Mesh(geo, pickMat);
    m.position.set(b.isCore ? b.isle.x : b.x, (b.top + b.y) / 2, b.isCore ? b.isle.z : b.z); m.userData.stem = p.stem;
    m.visible = false;                // 不繪製；Raycaster 不看 visible，照樣點得到
    world.add(m); picks.push(m);
  });
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2(), v3 = new THREE.Vector3();
  function pickAt(cx, cy) {
    const r = canvas.getBoundingClientRect();
    ndc.set((cx - r.left) / r.width * 2 - 1, -(cy - r.top) / r.height * 2 + 1);
    ray.setFromCamera(ndc, camera);
    const hit = ray.intersectObjects(picks, false)[0];
    return hit ? hit.object.userData.stem : null;
  }
  let hover = null, down = null;
  function setHover(stem) {
    if (stem === hover) return;
    hover = stem; canvas.classList.toggle('is-hover', !!stem);
    tags.forEach(T => T.el.classList.toggle('is-hover', !!stem && T.stem === stem));
    tagsDirty = true; requestRender();
  }
  canvas.addEventListener('pointerdown', e => { down = { x: e.clientX, y: e.clientY }; });
  canvas.addEventListener('pointermove', e => { if (e.pointerType === 'mouse' && !e.buttons) setHover(pickAt(e.clientX, e.clientY)); });
  canvas.addEventListener('pointerleave', () => setHover(null));
  canvas.addEventListener('pointerup', e => {
    if (!down || Math.hypot(e.clientX - down.x, e.clientY - down.y) > 6) { down = null; return; }
    down = null;
    const stem = pickAt(e.clientX, e.clientY);
    if (stem) { select(stem, { trigger: canvas, fly: true }); scrollListTo(stem); } else closePanel();
  });
  function scrollListTo(stem) {
    const it = items.get(stem);
    if (it && window.innerWidth >= 768) { const list = $('islList'); list.scrollTop = it.li.offsetTop - list.clientHeight / 2; }
  }
  canvas.addEventListener('keydown', e => {
    const step = Math.PI / 12;
    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
      const off = camera.position.clone().sub(controls.target);
      off.applyAxisAngle(new THREE.Vector3(0, 1, 0), e.key === 'ArrowLeft' ? -step : step);
      camera.position.copy(controls.target).add(off); controls.update(); requestRender(); e.preventDefault();
    } else if (['+', '=', '-', 'ArrowUp', 'ArrowDown'].includes(e.key)) {
      const zin = e.key === '+' || e.key === '=' || e.key === 'ArrowUp';
      camera.zoom = Math.min(controls.maxZoom, Math.max(controls.minZoom, camera.zoom * (zin ? 1.2 : 1 / 1.2)));
      camera.updateProjectionMatrix(); requestRender(); e.preventDefault();
    }
  });
  controls.addEventListener('change', () => { tagsDirty = true; requestRender(); });

  /* ═════════ 標籤層（HTML）═════════ */
  const layer = $('islLabels');
  const tags = [];
  const UNIT_ZOOM = 1.6;               // 放大到這個倍率以上，才展開工坊島的單元標籤
  function addTag({ stem = null, grp, kind, text, code, anchor, prio }) {
    const el = document.createElement('button');
    el.type = 'button'; el.className = `isl-tag isl-tag-${kind} isl-tag-${grp}`; el.tabIndex = -1; el.setAttribute('aria-hidden', 'true');
    if (code) { const n = document.createElement('span'); n.className = 'isl-tag-num'; n.textContent = code; el.appendChild(n); }
    const t = document.createElement('span'); t.className = 'isl-tag-t'; t.textContent = text; el.appendChild(t);
    el.addEventListener('click', () => {
      if (stem) { select(stem, { trigger: canvas, fly: true }); scrollListTo(stem); } else flyToIsle(grp);
    });
    layer.appendChild(el);
    tags.push({ el, stem, grp, kind, anchor, prio, w: 0, h: 0, cw: 0, num: el.querySelector('.isl-tag-num') });
  }
  PAGES.forEach(p => {
    const b = B[p.stem];
    addTag({ stem: p.stem, grp: p.grp, kind: p.grp === 'core' ? 'core' : 'unit', text: p.title, code: p.code,
      anchor: p.grp === 'core' ? LOC(b).P(0, 0, -6.6) : new THREE.Vector3(b.x, b.top + .35, b.z), prio: p.grp === 'core' ? 2 : 4 });
  });
  Object.entries(SAT_ISLE).forEach(([grp, I]) => {
    addTag({ grp, kind: 'isle', text: ISLES[grp].name, anchor: new THREE.Vector3(I.x, I.top + 4.6, I.z), prio: 3 });
  });
  function measureTags() {
    tags.forEach(T => {
      T.el.classList.remove('is-compact'); T.st = -1; T.w = T.el.offsetWidth; T.h = T.el.offsetHeight;
      T.cw = T.num ? T.num.offsetWidth + 10 : T.w;
    });
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { measureTags(); tagsDirty = true; requestRender(); });
  const placed = [];
  function placeTags() {
    const W = canvas.clientWidth, H = canvas.clientHeight, zoomed = camera.zoom >= UNIT_ZOOM;
    placed.length = 0;
    const sel = T => (!!T.stem && T.stem === selected ? 0 : 1);
    const order = tags.slice().sort((a, b) => sel(a) - sel(b) || a.prio - b.prio);
    order.forEach(T => {
      const isSel = !!T.stem && T.stem === selected, isRef = !!T.stem && refs.includes(T.stem);
      let show = T.kind === 'core' || (T.kind === 'unit' ? zoomed : !zoomed) || isSel || isRef;
      v3.copy(T.anchor).project(camera);
      const x = (v3.x + 1) / 2 * W, y = (1 - v3.y) / 2 * H;
      // 完整標籤與已放好的重疊時，退成只顯示編號的小圓章；仍然重疊才隱藏
      const hits = r => placed.some(q => !(r.r < q.l || r.l > q.r || r.b < q.t || r.t > q.b));
      const box = w => ({ l: x - w / 2 - 3, r: x + w / 2 + 3, t: y - T.h - 8, b: y });
      // 手機上正課標籤預設只顯示編號（選取或滑過時才展開）
      let compact = narrow() && T.kind === 'core' && !isSel && T.stem !== hover, r = box(compact ? T.cw : T.w);
      if (show && (r.l < 2 || r.r > W - 2 || r.t < 0 || r.b > H)) show = false;   // 會被切掉的就不顯示
      if (show && !isSel && hits(r) && !compact) {
        if (T.num && !hits(box(T.cw))) { compact = true; r = box(T.cw); } else show = false;
      }
      if (show) placed.push(r);
      // 只在狀態或位置真的改變時才寫 DOM（每次寫入都會讓瀏覽器重算樣式）
      const st = show ? (compact ? 2 : 1) : 0;
      if (st !== T.st) { T.el.classList.toggle('is-off', !show); T.el.classList.toggle('is-compact', st === 2); T.st = st; }
      if (show) {
        const tf = `translate(${Math.round(x)}px, ${Math.round(y)}px) translate(-50%, calc(-100% - 6px))`;
        if (tf !== T.tf) { T.el.style.transform = tf; T.tf = tf; }
      }
    });
  }

  /* ═════════ 地標播放 ═════════ */
  const playing = new Map();     // stem → 開始時間
  function playLM(stem) {
    if (!POSE[stem] || !motion()) return;
    playing.set(stem, performance.now());
    wake(); requestRender();
  }
  function stepPlays(now) {
    playing.forEach((t0, stem) => {
      const u = (now - t0) / (POSE[stem].dur * 1000);
      if (u >= 1) { POSE[stem].pose(0); playing.delete(stem); } else POSE[stem].pose(u);
    });
  }
  // 沒有選取時，島上輪流跑一座模型；選到的那一座不放，避免先看到猜題的答案
  const CORE_STEMS = core.map(p => p.stem);
  let attractAt = 0, attractI = 0;
  function stepAttract(now) {
    if (nightTarget || playing.size || selected || lowPower || now < attractAt) return;
    attractAt = now + 8000;
    if (attractI > 0 || now > 3000) playLM(CORE_STEMS[attractI++ % CORE_STEMS.length]);
  }
  Object.values(POSE).forEach(l => l.pose(0));

  /* ═════════ 繪製迴圈 ═════════
     - 互動（拖曳、縮放、飛行、日夜過渡）時全速；只剩環境動畫時每 33 ms 才畫一幀
     - 閒置 45 秒（沒有任何 pointer／wheel／key／touch）就停止動畫，有輸入立即恢復
     - 解析度自動調整：最近 2 秒偏慢就降一級 DPR；互動時連續夠快再升回；最低一級仍慢才停用生活感
     - 標籤只在鏡頭、選取或滑過改變時重排 */
  const DPRS = narrow() ? [1.25, 1] : [1.5, 1.25, 1];
  const IDLE_MS = () => window.__islandIdleMs || 45000;          // 檢查腳本可以把門檻調短
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
    const flying = stepFly(now), hopping = stepGuide(now), moved = controls.update(), anim = animating();
    let fading = false;
    if (night !== nightTarget) {
      night = motion() ? (nightTarget > night ? Math.min(nightTarget, night + dt / 1.2) : Math.max(nightTarget, night - dt / 1.2)) : nightTarget;
      applyNight(night); fading = true;
    }
    const playingNow = anim && playing.size > 0;
    const busy = need || flying || hopping || moved || fading || playingNow;
    // 只有環境動畫時限制在約 30fps
    if (!busy && anim && now - lastDraw < 32) { if (!raf) raf = requestAnimationFrame(frame); return; }
    if (anim) {
      const t = now / 1000;
      anims.forEach(f => f(t));
      stepPlays(now); stepAttract(now);
      if (!lowPower) life.forEach(f => f(t, Math.min(.1, (now - (lastDraw || now)) / 1000)));
      syncProxies();
    }
    if (busy || anim) {
      if (lastDraw) {                                   // 幀間隔取樣（略過第一幀與長時間停頓）
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
    if ((anim || flying || hopping || moved || fading) && !raf) raf = requestAnimationFrame(frame);
  }
  const ro = new ResizeObserver(resize); ro.observe(stage);
  new IntersectionObserver(es => { onScreen = es[0].isIntersecting; requestRender(); }).observe(stage);
  document.addEventListener('visibilitychange', requestRender);
  reduceMotion.addEventListener('change', () => { controls.enableDamping = motion(); requestRender(); });
  anims.forEach(f => f(1.7)); life.forEach(f => f(1.7, 0)); syncProxies();
  resize();
  renderer.shadowMap.needsUpdate = true;

  function flyToIsle(grp) {
    if (grp === 'core') { const c = coreIsles.reduce((s, I) => s.add(new THREE.Vector3(I.x, 0, I.z)), new THREE.Vector3()).multiplyScalar(1 / coreIsles.length); flyTo(c, 1.3); return; }
    const I = SAT_ISLE[grp]; if (I) flyTo(new THREE.Vector3(I.x, GROUND, I.z), grp === 'workshop' ? 2.2 : 2.6);
  }

  /* ═════════ 對外介面 ═════════ */
  return {
    select(stem, doFly) {
      refs.forEach(r => { B[r].ref.visible = false; });
      selected = stem && B[stem] ? stem : null;
      refs = selected ? BY[selected].refs.filter(r => B[r]) : [];
      refs.forEach(r => { B[r].ref.visible = true; });
      setWires(selected);
      if (selected && playing.has(selected)) { playing.delete(selected); POSE[selected].pose(0); }   // 剛選到的島先回到靜止，答案不提早露出
      marker.visible = !!selected;
      tags.forEach(T => { T.el.classList.toggle('is-current', !!T.stem && T.stem === selected); T.el.classList.toggle('is-ref', !!T.stem && refs.includes(T.stem)); });
      tagsDirty = true;
      if (selected) {
        const b = B[selected];
        marker.position.set(b.x, b.top + 1.4, b.z);
        if (doFly) {
          setHover(null);
          // 讓選到的島落在面板以外的區域：桌機面板在左下，往右讓；手機面板從下方升起，往上讓
          const zoom = Math.max(camera.zoom, b.isCore ? 3 : 3.4), W = canvas.clientWidth, H = canvas.clientHeight;
          const wpp = (camera.right - camera.left) / zoom / W;
          camera.updateMatrixWorld();
          const R = new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 0), U = new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 1);
          const tgt = new THREE.Vector3(b.isCore ? b.isle.x : b.x, b.y, b.isCore ? b.isle.z : b.z);
          if (window.innerWidth >= 768) tgt.addScaledVector(R, -Math.min(210, W * .22) * wpp);
          else tgt.addScaledVector(U, -H * .2 * wpp);
          flyTo(tgt, zoom);
        }
      }
      requestRender();
    },
    flyToIsle,
    reset() { flyTo(HOME.clone(), 1); },
    guideTo,
    // 走完路線：多跳一步，站到最後一站的外面（end() 的位置）
    guideEnd(stem) {
      const b = B[stem]; if (!b) return;
      guideTo(stem);
      if (hop) { const d = hop.to.clone().sub(new THREE.Vector3(b.x, hop.to.y, b.z)).normalize(); hop.to.addScaledVector(d, 1.8); }
    },
    guidePos() { const p = guide.position; return { x: p.x, y: p.y, z: p.z }; },
    play(stem) { playLM(stem); },
    setNight(on, instant) {
      nightTarget = on ? 1 : 0;
      if (instant || !motion()) { night = nightTarget; applyNight(night); }
      requestRender();
    },
    updateTrail() {
      PAGES.forEach(p => {
        const b = B[p.stem], done = !!trail.done[p.stem], visited = !!trail.visited[p.stem];
        b.flag.visible = done; b.lan.visible = visited && !done;
      });
      tags.forEach(T => {
        if (!T.stem) return;
        T.el.classList.toggle('is-done', !!trail.done[T.stem]);
        T.el.classList.toggle('is-visited', !!trail.visited[T.stem] && !trail.done[T.stem]);
      });
      renderer.shadowMap.needsUpdate = true;
      requestRender();
    },
    // 以下給 tools/check_island_browser.js 用
    stats() { return { draws, dprLevel, lowPower, calls: renderer.info.render.calls, night }; },
    screenPos(stem) {
      const b = B[stem]; if (!b) return null;
      v3.set(b.x, b.y + (b.top - b.y) * .3, b.z).project(camera);
      const r = canvas.getBoundingClientRect();
      return { x: r.left + (v3.x + 1) / 2 * r.width, y: r.top + (1 - v3.y) / 2 * r.height };
    },
    invariants() { return JSON.parse(JSON.stringify(INV)); },
    pose(stem, u) { if (!POSE[stem]) return false; playing.delete(stem); POSE[stem].pose(u); requestRender(); return true; },
    plays() { return [...playing.keys()]; },
    // 先編譯所有著色器（支援平行編譯時不卡主執行緒）並畫好第一幀，再讓畫布淡入
    async warm() {
      try { await renderer.compileAsync(world, camera); } catch (e) { /* 舊版瀏覽器：第一幀時再編譯 */ }
      renderer.shadowMap.needsUpdate = true; renderer.render(world, camera); placeTags(); tagsDirty = false; lastDraw = performance.now();
      requestRender();
    },
    dispose() { alive = false; ro.disconnect(); controls.dispose(); renderer.dispose(); layer.replaceChildren(); },
  };
}

function mulberry32(a) {
  return function () {
    a |= 0; a = a + 0x6D2B79F5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
