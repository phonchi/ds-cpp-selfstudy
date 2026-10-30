#!/usr/bin/env node
/* 3D 群島 island/index.html 的瀏覽器驗收。
 *   - WebGL 正常／CDN 被攔／getContext 回傳 null 三種狀態 × 桌面與 390×844
 *   - 點島開面板、鍵盤、足跡、模式切換、導覽路線與續走、代表圖
 *   - 九題猜題、四組對比（步數與本檔獨立計算的結果比對）
 *   - 結構約束實測（island_meta.py 開頭列的那幾條）
 *   - 繪製呼叫上限、拖曳時繪製不重複排程、閒置暫停
 *   - 九個代表圖深連結的落點
 * 用法：SHOT_DIR=/tmp/shots node tools/check_island_browser.js
 * puppeteer-core 裝在 ~/.cache/selfstudy-node（見 build_island_figs.js）。 */
const path = require('path');
const fs = require('fs');

const PPT_HOME = process.env.PPT_HOME || path.join(process.env.HOME, '.cache/selfstudy-node');
const puppeteer = require(path.join(PPT_HOME, 'node_modules', 'puppeteer-core'));
const ROOT = path.resolve(__dirname, '..');
const SHOT_DIR = process.env.SHOT_DIR || path.join(PPT_HOME, 'shots-island');
const CHROME = process.env.CHROME_PATH || (() => {
  const base = path.join(process.env.HOME, '.cache/puppeteer/chrome');
  const dirs = fs.readdirSync(base).sort();
  return path.join(base, dirs[dirs.length - 1], 'chrome-linux64', 'chrome');
})();
const URL_ = 'file://' + path.join(ROOT, 'island', 'index.html');
const IGNORE = [/software WebGL/i, /GL Driver Message/i, /GPU stall/i, /fonts\.g/i, /net::ERR/i, /Failed to load resource/i];
const CORE = ['introduction', 'analysis', 'arrays', 'linked_lists', 'linear_structures', 'recursion', 'searching_sorting', 'graphs', 'trees'];
const sleep = ms => new Promise(r => setTimeout(r, ms));
const problems = [];
const note = m => { problems.push(m); console.log('  ✗ ' + m); };
const ok = m => console.log('  ✓ ' + m);

/* ── 獨立計算（不沿用 island-compare.js 的程式）── */
function indepInsert(pos, n = 8) {
  const copies = n - pos;                                   // 索引 pos..n-1 各複製一次
  return { array: { walk: 0, write: copies + 1 }, list: { walk: pos === 0 ? 0 : pos - 1, write: 2 } };
}
function indepSeq(v, t) { const i = v.indexOf(t); return i < 0 ? v.length : i + 1; }
function indepBin(v, t) { let l = 0, h = v.length - 1, c = 0; while (l <= h) { const m = Math.floor((l + h) / 2); c++; if (v[m] === t) return c; if (v[m] < t) l = m + 1; else h = m - 1; } return c; }
function indepWalk(g) {
  const adj = {}; Object.keys(g.vertices).forEach(k => { adj[k] = new Set(); });
  g.edges.forEach(([a, b]) => { adj[a].add(b); adj[b].add(a); });
  const N = k => [...adj[k]].sort();
  const bfs = [], seen = new Set([g.start]), q = [g.start];
  while (q.length) { const u = q.shift(); bfs.push(u); N(u).forEach(w => { if (!seen.has(w)) { seen.add(w); q.push(w); } }); }
  const dfs = [], vis = new Set();
  (function go(u) { vis.add(u); dfs.push(u); N(u).forEach(w => { if (!vis.has(w)) go(w); }); })(g.start);   // 遞迴版，獨立於堆疊版
  return { bfs, dfs };
}

(async () => {
  fs.mkdirSync(SHOT_DIR, { recursive: true });
  const browser = await puppeteer.launch({ executablePath: CHROME, args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });

  async function open(mode) {
    const page = await browser.newPage();
    const errors = [];
    page.on('console', m => { if (['error', 'warning'].includes(m.type()) && !IGNORE.some(r => r.test(m.text()))) errors.push(m.text()); });
    page.on('pageerror', e => errors.push('pageerror: ' + e.message));
    if (mode === 'cdn') {
      await page.setRequestInterception(true);
      page.on('request', r => (/cdn\.jsdelivr\.net/.test(r.url()) ? r.abort() : r.continue()).catch(() => {}));
    }
    if (mode === 'nogl') {
      await page.evaluateOnNewDocument(() => {
        const o = HTMLCanvasElement.prototype.getContext;
        HTMLCanvasElement.prototype.getContext = function (t, ...r) { return /webgl/i.test(t) ? null : o.call(this, t, ...r); };
      });
    }
    return { page, errors };
  }
  async function layout(page, label) {
    const r = await page.evaluate(() => {
      const de = document.documentElement, links = [...document.querySelectorAll('.isl-link')];
      return { over: de.scrollWidth - de.clientWidth, visible: links.filter(a => a.offsetParent !== null).length, total: links.length, webgl: document.body.classList.contains('webgl-ready') };
    });
    if (r.over > 1) note(`${label}：橫向溢出 ${r.over}px`);
    if (r.visible !== r.total) note(`${label}：只有 ${r.visible}/${r.total} 個入口可見`);
    return r;
  }
  async function canvasColors(page) {
    const el = await page.$('#islCanvas'), b64 = await el.screenshot({ encoding: 'base64' });
    return page.evaluate(async src => {
      const img = new Image(); img.src = 'data:image/png;base64,' + src; await img.decode();
      const c = document.createElement('canvas'); c.width = img.width; c.height = img.height;
      const g = c.getContext('2d'); g.drawImage(img, 0, 0);
      const d = g.getImageData(0, 0, c.width, c.height).data, seen = new Set();
      for (let i = 0; i < d.length; i += 4 * 97) seen.add((d[i] >> 3) << 10 | (d[i + 1] >> 3) << 5 | d[i + 2] >> 3);
      return seen.size;
    }, b64);
  }

  /* ═ (a) WebGL 正常 ═ */
  console.log('(a) WebGL');
  {
    const { page, errors } = await open('gl');
    await page.setViewport({ width: 1280, height: 900 });
    await page.goto(URL_, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.evaluate(() => { ['trail:v1', 'tour:v1', 'mode'].forEach(k => localStorage.removeItem('dscpp-island:' + k)); });
    await page.reload({ waitUntil: 'domcontentloaded' });
    const ready = await page.waitForSelector('body.webgl-ready', { timeout: 40000 }).then(() => true, () => false);
    if (!ready) note('WebGL 可用時沒有進入 3D');
    await sleep(1500);
    const colors = await canvasColors(page);
    if (colors < 30) note(`3D 畫布幾乎是空的（${colors} 種顏色）`); else ok(`3D 畫出 ${colors} 種顏色`);
    await page.screenshot({ path: path.join(SHOT_DIR, '3d_power.png') });

    /* 結構約束 */
    const inv = await page.evaluate(() => window.__island.invariants());
    const gaps = inv.arrays.cells.slice(1).map((c, i) => Math.abs(c.x0 - inv.arrays.cells[i].x1));
    if (Math.max(...gaps) > 1e-9) note(`陣列格子有間距：${gaps}`); else ok('陣列格子間距為 0');
    const n = inv.linked_lists.nodes;
    const area = (a, b, c) => Math.abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1]));
    const collinear = n.slice(2).every((p, i) => area(n[i], n[i + 1], p) < .5);
    if (collinear) note('串列節點共線'); else ok('串列節點不共線');
    if (inv.linear_structures.stackWalls !== 4 || !inv.linear_structures.stackTopOpen) note('堆疊不是四面封閉、頂端開口'); else ok('堆疊四面封閉、只開頂端');
    if (!inv.trees.leafY.every(y => y < inv.trees.rootY)) note('樹的根不在葉之上'); else ok('樹根在最上面');
    if (inv.trees.path.join() !== '70,31,40' || inv.trees.parentOfNew !== 31 || inv.trees.side !== 'r') note(`BST 插入 40 的路徑不對：${inv.trees.path}`); else ok('BST 插入 40：70 → 31 → 右子節點');
    // 圖要有環：連通且邊數 ≥ 頂點數
    const vN = Object.keys(inv.graphs.level).length;
    if (inv.graphs.edges.length < vN) note('圖沒有環'); else ok(`圖有環（${vN} 頂點、${inv.graphs.edges.length} 邊）`);
    // 線性探查：獨立再跑一次
    { const t = Array(11).fill(null), want = [54, 26, 93, 17, 77, 31, 44, 55].map(k => { let i = k % 11; while (t[i] !== null) i = (i + 1) % 11; t[i] = k; return i; });
      const got = inv.searching_sorting.paths.map(p => p.hops[p.hops.length - 1]);
      if (want.join() !== got.join()) note(`雜湊落點不符：${got} vs ${want}`); else ok(`雜湊落點相符：${got}`); }

    /* 每座地標都能跑完整時間軸，頭尾回到靜止 */
    await page.evaluate(stems => { stems.forEach(s => { for (let u = 0; u <= 1; u += .02) window.__island.pose(s, u); window.__island.pose(s, 0); }); }, CORE);
    ok('九座地標的時間軸都跑得完');

    /* 點島 → 面板 */
    const pos = await page.evaluate(() => window.__island.screenPos('recursion'));
    await page.mouse.click(pos.x, pos.y); await sleep(300);
    const t1 = await page.$eval('#islPanelTitle', e => e.textContent);
    if (t1 !== '遞迴') note(`點遞迴島開成「${t1}」`); else ok('點島開對面板');
    const refs = await page.$$eval('.isl-item.is-ref', e => e.length);
    if (refs !== 2) note(`遞迴應高亮 2 個先備，得到 ${refs}`); else ok('先備依賴高亮');
    /* 列表鍵盤 → 焦點；Esc 還原 */
    await page.focus('.isl-item[data-stem="trees"] .isl-link');
    await page.keyboard.press('Enter'); await sleep(900);
    const k = await page.evaluate(() => ({ t: document.getElementById('islPanelTitle').textContent, f: document.activeElement.id, h: document.getElementById('islPanelGo').getAttribute('href') }));
    if (k.t !== '樹與樹演算法' || k.f !== 'islPanelGo' || k.h !== '../trees.html') note(`鍵盤選取失敗：${JSON.stringify(k)}`); else ok('鍵盤選取');
    await page.keyboard.press('Escape');
    const back = await page.evaluate(() => ({ h: document.getElementById('islPanel').hidden, f: document.activeElement.dataset.stem }));
    if (!back.h || back.f !== 'trees') note(`Esc 沒有關閉或還原焦點：${JSON.stringify(back)}`); else ok('Esc 關閉並還原焦點');
    /* 足跡 */
    await page.click('.isl-item[data-stem="introduction"] .isl-mark');
    const done = await page.evaluate(() => ({ c: document.querySelector('.isl-item[data-stem="introduction"]').classList.contains('is-done'), s: (localStorage.getItem('dscpp-island:trail:v1') || '').includes('introduction') }));
    if (!done.c || !done.s) note('標記完成沒有生效'); else ok('標記完成寫入 localStorage');
    /* 標籤：回到全景再數 */
    await page.click('#islReset'); await sleep(1100);
    const tagInfo = await page.$$eval('.isl-tag-core', e => ({ total: e.length, shown: e.filter(x => !x.classList.contains('is-off')).length }));
    if (tagInfo.shown < tagInfo.total) note(`全景時正課標籤只顯示 ${tagInfo.shown}/${tagInfo.total}`); else ok('全景時 9 個正課標籤都在');

    /* 九題猜題：答對與答錯都要有回饋；正解由資料決定 */
    const quizzes = await page.evaluate(() => JSON.parse(document.getElementById('island-data').textContent).pages.filter(p => p.quiz).map(p => ({ stem: p.stem, a: p.quiz.answer })));
    if (quizzes.length !== 9) note(`猜題應有 9 題，得到 ${quizzes.length}`);
    for (let i = 0; i < quizzes.length; i++) {
      const q = quizzes[i];
      await page.evaluate(s => document.querySelector(`.isl-item[data-stem="${s}"] .isl-link`).click(), q.stem); await sleep(120);
      await page.click('#islTabQuiz');
      const before = await page.$eval('#islQuizWhy', e => e.hidden);
      if (!before) note(`${q.stem}：答題前就看到解答`);
      const pick = i % 2 ? q.a : (q.a + 1) % 4;
      await (await page.$$('.isl-opt'))[pick].click(); await sleep(60);
      const r = await page.evaluate(() => ({ why: document.getElementById('islQuizWhy').textContent, right: document.querySelectorAll('.isl-opt.is-right').length, wrong: document.querySelectorAll('.isl-opt.is-wrong').length, plays: window.__island.plays() }));
      if (!r.why || r.right !== 1 || r.wrong !== (pick === q.a ? 0 : 1)) note(`${q.stem}：猜題回饋不對 ${JSON.stringify(r)}`);
      if (!r.plays.includes(q.stem)) note(`${q.stem}：答完沒有播放地標動畫`);
    }
    ok('九題猜題回饋與播放');
    await page.keyboard.press('Escape');

    /* 四組對比：與獨立計算比對 */
    const cmp = await page.evaluate(() => {
      const d = JSON.parse(document.getElementById('island-data').textContent), S = window.__cmpSim, last = a => a[a.length - 1];
      const search = d.compare.pairs.find(p => p.key === 'search');
      return {
        graph: d.graph, values: search.values, targets: search.options.map(o => o.v),
        insert: [0, 4, 8].map(pos => { const r = S('insert', pos); return { pos, a: last(r.left), l: last(r.right) }; }),
        order: (() => { const r = S('order'); return { s: last(r.left).out, q: last(r.right).out, so: last(r.left).ops, qo: last(r.right).ops }; })(),
        search: search.options.map(o => { const r = S('search', o.v); return { t: o.v, s: last(r.left).cmp, b: last(r.right).cmp }; }),
        walk: (() => { const r = S('walk'); return { b: last(r.left).order, d: last(r.right).order }; })(),
      };
    });
    cmp.insert.forEach(({ pos, a, l }) => {
      const w = indepInsert(pos);
      if (a.walk !== w.array.walk || a.write !== w.array.write || l.walk !== w.list.walk || l.write !== w.list.write) note(`插入 pos=${pos} 步數不符：${JSON.stringify({ a: [a.walk, a.write], l: [l.walk, l.write], w })}`);
    });
    if (cmp.order.s.join('') !== 'CBA' || cmp.order.q.join('') !== 'ABC' || cmp.order.so !== 6 || cmp.order.qo !== 6) note(`堆疊／佇列不符：${JSON.stringify(cmp.order)}`);
    cmp.search.forEach(({ t, s, b }) => { if (s !== indepSeq(cmp.values, t) || b !== indepBin(cmp.values, t)) note(`搜尋 ${t} 比較次數不符：${s}/${b}`); });
    const w = indepWalk(cmp.graph);
    if (w.bfs.join() !== cmp.walk.b.join()) note(`BFS 順序不符：${cmp.walk.b} vs ${w.bfs}`);
    if (w.dfs.join() !== cmp.walk.d.join()) note(`DFS 順序不符：${cmp.walk.d} vs ${w.dfs}`);
    ok(`對比與獨立計算相符（BFS ${w.bfs.join('')}、DFS ${w.dfs.join('')}）`);
    /* 對話框實際操作：走到底才出現結論；Esc 只關對話框 */
    await page.click('#islCompare'); await sleep(150);
    const nodeOpen = await page.evaluate(() => ({ open: document.getElementById('cmpDialog').open, note: document.getElementById('cmpNote').textContent }));
    if (!nodeOpen.open || nodeOpen.note) note(`對話框開啟狀態不對：${JSON.stringify(nodeOpen)}`);
    for (let i = 0; i < 40; i++) { if (await page.$eval('#cmpNext', e => e.disabled)) break; await page.click('#cmpNext'); }
    const fin = await page.$eval('#cmpNote', e => e.textContent);
    if (!fin) note('對比走到底沒有結論'); else ok('對比走到底顯示結論');
    await page.screenshot({ path: path.join(SHOT_DIR, 'cmp.png') });
    await page.keyboard.press('Escape'); await sleep(100);
    if (await page.$eval('#cmpDialog', e => e.open)) note('Esc 沒有關閉對比');

    /* 模式 */
    await page.click('#islMode'); await sleep(1300);
    const m = await page.evaluate(() => ({ p: document.getElementById('islMode').getAttribute('aria-pressed'), d: document.documentElement.dataset.mode, k: window.__island.stats().modeK, s: localStorage.getItem('dscpp-island:mode') }));
    if (m.p !== 'true' || m.d !== 'print' || m.k !== 1 || m.s !== 'print') note(`藍圖切換無效：${JSON.stringify(m)}`); else ok('切到藍圖');
    await page.screenshot({ path: path.join(SHOT_DIR, '3d_print.png') });
    // 藍圖靜止時不應持續繪製（先等猜題觸發的地標動畫播完）
    await page.waitForFunction(() => window.__island.plays().length === 0, { timeout: 20000 }).catch(() => note('地標動畫一直沒有播完'));
    await sleep(800);
    const b0 = await page.evaluate(() => window.__island.stats().draws); await sleep(1200);
    const b1 = await page.evaluate(() => window.__island.stats().draws);
    if (b1 !== b0) note(`藍圖靜止時仍在繪製（${b1 - b0} 幀）`); else ok('藍圖靜止時不繪製');
    await page.click('#islMode'); await sleep(1200);

    /* 拖曳時不重複排程 */
    {
      const cv = await page.$('#islCanvas'), bb = await cv.boundingBox();
      await page.evaluate(() => { window.__rafN = 0; const f = () => { window.__rafN++; requestAnimationFrame(f); }; requestAnimationFrame(f); });
      const s0 = await page.evaluate(() => ({ d: window.__island.stats().draws, f: window.__rafN }));
      await page.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2); await page.mouse.down();
      for (let i = 0; i < 25; i++) await page.mouse.move(bb.x + bb.width / 2 + i * 8, bb.y + bb.height / 2, { steps: 2 });
      await page.mouse.up(); await sleep(600);
      const s1 = await page.evaluate(() => ({ d: window.__island.stats().draws, f: window.__rafN }));
      if (s1.d - s0.d > s1.f - s0.f + 3) note(`拖曳時繪製（${s1.d - s0.d}）多於畫面幀（${s1.f - s0.f}）`); else ok(`拖曳：繪製 ${s1.d - s0.d}、畫面幀 ${s1.f - s0.f}`);
    }
    await page.click('#islReset'); await sleep(1100);

    /* 導覽 */
    {
      await page.evaluate(() => document.getElementById('islBubble').hidden = false);
      await page.click('#islBubble'); await sleep(250);
      const routes = await page.$$('#islGuideChoices .isl-choice');
      if (routes.length !== 3) note(`路線應有 3 條，得到 ${routes.length}`);
      await routes[1].click(); await sleep(900);
      await page.waitForFunction(() => document.getElementById('islFigImg').complete, { timeout: 5000 }).catch(() => {});
      const a = await page.evaluate(() => ({ step: document.getElementById('islGuideStep').textContent, title: document.getElementById('islPanelTitle').textContent, img: document.getElementById('islFigImg').naturalWidth, href: document.getElementById('islFigGo').getAttribute('href') }));
      if (!a.step.startsWith('第 1／9 站') || a.title !== 'C++ 導論') note(`導覽第 1 站不對：${JSON.stringify(a)}`);
      if (!a.img) note('代表圖沒有載入');
      if (a.href !== '../introduction.html#ptrVis') note(`代表圖連結錯誤：${a.href}`);
      const g0 = await page.evaluate(() => window.__island.guidePos());
      await page.click('#islGuideNext'); await sleep(1600);
      const b = await page.evaluate(() => ({ t: document.getElementById('islPanelTitle').textContent, g: window.__island.guidePos() }));
      if (b.t !== '演算法分析') note(`下一站不對：${b.t}`);
      if (Math.hypot(b.g.x - g0.x, b.g.z - g0.z) < 1) note('下一站後阿迭沒有移動'); else ok('導覽：阿迭沿路線移動');
      await page.screenshot({ path: path.join(SHOT_DIR, 'tour.png') });
      await page.click('#islGuideEnd'); await sleep(150);
      await page.click('#islBubble'); await sleep(250);
      const r = await page.$$eval('#islGuideChoices .isl-choice b', e => e.map(x => x.textContent));
      if (r[0] !== '接著走') note(`沒有問要不要接著走：${r}`); else ok('導覽可續走');
      await page.click('.isl-choice'); await sleep(500);
      await page.evaluate(() => document.querySelector('.isl-item[data-stem="graphs"] .isl-link').click()); await sleep(200);
      const e = await page.evaluate(() => ({ g: document.getElementById('islGuide').hidden, n: document.getElementById('islGuideNav').hidden }));
      if (!e.g || !e.n) note('導覽中改選別章後對話列沒有收起');
      await page.keyboard.press('Escape');
      // 走完路線：最後一站 → end()
      await page.evaluate(() => localStorage.setItem('dscpp-island:tour:v1', JSON.stringify({ route: 'core', i: 8 })));
      await page.click('#islBubble'); await sleep(200); await page.click('.isl-choice'); await sleep(400);
      await page.click('#islGuideNext'); await sleep(200);
      const bye = await page.$eval('#islGuideText', x => x.textContent);
      if (!bye.includes('end()')) note(`走完路線的台詞不對：${bye}`); else ok('走到 end()');
      await page.click('.isl-choice'); await sleep(100);
    }

    /* 繪製呼叫、閒置 */
    const calls = await page.evaluate(() => window.__island.stats().calls);
    if (calls > 80) note(`每幀繪製呼叫過多：${calls}`); else ok(`繪製呼叫 ${calls}`);
    await page.evaluate(() => { window.__islandIdleMs = 1200; });
    let d0 = 0, d1 = -1;
    for (let i = 0; i < 12 && d1 !== d0; i++) { d0 = await page.evaluate(() => window.__island.stats().draws); await sleep(1000); d1 = await page.evaluate(() => window.__island.stats().draws); }
    if (d1 !== d0) note('閒置後仍在繪製'); else ok('閒置時停止繪製');
    await page.mouse.move(400, 400); await page.mouse.move(420, 410); await sleep(1000);
    if ((await page.evaluate(() => window.__island.stats().draws)) <= d1) note('有操作後沒有恢復繪製'); else ok('有操作就恢復');
    await page.evaluate(() => { window.__islandIdleMs = 0; localStorage.clear(); });

    await layout(page, '桌面 3D');
    await page.setViewport({ width: 390, height: 844 }); await sleep(1000);
    await layout(page, '手機 3D');
    await page.screenshot({ path: path.join(SHOT_DIR, '3d_mobile.png') });
    const mpos = await page.evaluate(() => window.__island.screenPos('graphs'));
    await page.mouse.click(mpos.x, mpos.y); await sleep(1100);
    if ((await page.$eval('#islPanel', e => e.hidden))) note('手機點島沒有開面板');
    await page.screenshot({ path: path.join(SHOT_DIR, '3d_mobile_panel.png') });
    await page.click('#islPanelClose');
    await page.click('#islCompare'); await sleep(200);
    await page.screenshot({ path: path.join(SHOT_DIR, 'cmp_mobile.png') });
    const mo = await page.evaluate(() => { const d = document.getElementById('cmpDialog'); return d.scrollWidth - d.clientWidth; });
    if (mo > 1) note(`手機對比台橫向溢出 ${mo}px`);
    errors.forEach(e => note('console：' + e));
    await page.close();
  }

  /* ═ (b)(c) 退回 2D ═ */
  for (const [mode, label] of [['cdn', 'CDN 失效'], ['nogl', '無 WebGL']]) {
    console.log(`(${mode}) ${label}`);
    const { page, errors } = await open(mode);
    await page.setViewport({ width: 1280, height: 900 });
    await page.goto(URL_, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(() => {});
    await sleep(2500);
    const r = await layout(page, label + '桌面');
    if (r.webgl) note(`${label}時仍進入 3D`);
    if (!(await page.$eval('#islStage', e => e.hidden))) note(`${label}時畫布沒有隱藏`);
    if (await page.evaluate(() => document.documentElement.classList.contains('gl-pending'))) note(`${label}時 gl-pending 沒有移除`);
    await page.screenshot({ path: path.join(SHOT_DIR, `2d_${mode}.png`) });
    // 2D 也能用對比台
    await page.click('#islCompare'); await sleep(150);
    await page.click('#cmpNext');
    if (!(await page.$eval('#cmpDialog', e => e.open))) note(`${label}時對比台開不起來`);
    await page.keyboard.press('Escape');
    await page.setViewport({ width: 390, height: 844 }); await sleep(300);
    await layout(page, label + '手機');
    errors.forEach(e => note(`${label} console：` + e));
    ok(`${label}：退回 2D`);
    await page.close();
  }

  /* ═ 代表圖深連結的落點 ═ */
  console.log('(deep links)');
  {
    const figs = await (async () => { const p = await browser.newPage(); await p.goto(URL_, { waitUntil: 'domcontentloaded' }); const d = await p.evaluate(() => JSON.parse(document.getElementById('island-data').textContent).pages.filter(x => x.fig).map(x => x.fig.href)); await p.close(); return d; })();
    for (const href of figs) {
      const p = await browser.newPage();
      await p.setViewport({ width: 1280, height: 900 });
      await p.goto('file://' + path.resolve(ROOT, 'island', href), { waitUntil: 'networkidle2', timeout: 60000 }).catch(() => {});
      await sleep(2500);
      const r = await p.evaluate(id => { const e = document.getElementById(id), d = e.closest('details:not([open])'); return { top: Math.round(e.getBoundingClientRect().top), hidden: !!d, h: e.getBoundingClientRect().height }; }, href.split('#')[1]);
      const good = !r.hidden && r.top > -40 && r.top < 400;
      console.log(`  ${good ? '✓' : '✗'} ${href.replace('../', '')}  top=${r.top}${r.hidden ? ' 在收合區塊' : ''}`);
      if (!good) note(`${href} 落點偏移（top=${r.top}）`);
      await p.close();
    }
  }

  await browser.close();
  console.log(problems.length ? `\n${problems.length} 個問題` : '\n全部通過');
  process.exit(problems.length ? 1 : 0);
})();
