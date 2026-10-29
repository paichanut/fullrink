// FullRink 3D rink — a to-scale hockey rink with the six apps placed where they are used.
// three.js r160 from jsDelivr via the import map in index.html. No build step.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';

const host = document.getElementById('rink3d');
if (!host) throw new Error('rink3d host missing');

// ---------- scene ----------
const RINK_W = 60, RINK_H = 26, RINK_R = 8.5; // metres, IIHF-ish
const isLight = () => document.documentElement.getAttribute('data-theme') === 'light';
const palette = () => isLight()
  ? { bg: 0xE9E9EF, floor: 0xD2D2DA, build: 0xF4F4F7, stand: 0xC9C9D2 }
  : { bg: 0x09090B, floor: 0x141418, build: 0x1C1C22, stand: 0x202027 };

const scene = new THREE.Scene();
scene.background = new THREE.Color(palette().bg);
scene.fog = new THREE.Fog(palette().bg, 140, 260);

const camera = new THREE.PerspectiveCamera(42, 1, 0.5, 600);
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
host.appendChild(renderer.domElement);

const labelRenderer = new CSS2DRenderer();
labelRenderer.domElement.className = 'r3-labels';
host.appendChild(labelRenderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.maxPolarAngle = Math.PI / 2 - 0.05;
controls.minDistance = 12;
controls.maxDistance = 220;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.35;
controls.addEventListener('start', () => { controls.autoRotate = false; });

// ---------- helpers ----------
function roundedRect(w, h, r) {
  const s = new THREE.Shape();
  const x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y);
  s.lineTo(x + w - r, y);
  s.quadraticCurveTo(x + w, y, x + w, y + r);
  s.lineTo(x + w, y + h - r);
  s.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  s.lineTo(x + r, y + h);
  s.quadraticCurveTo(x, y + h, x, y + h - r);
  s.lineTo(x, y + r);
  s.quadraticCurveTo(x, y, x + r, y);
  return s;
}
const mat = (color, extra = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.85, metalness: 0.05, ...extra });
function box(w, h, d, material, x, y, z, shadow = true) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material);
  m.position.set(x, y, z);
  m.castShadow = shadow; m.receiveShadow = true;
  scene.add(m);
  return m;
}

// ---------- ice with markings ----------
function iceTexture() {
  const c = document.createElement('canvas');
  c.width = 2048; c.height = 2048 * (RINK_H / RINK_W);
  const g = c.getContext('2d');
  const sx = c.width / RINK_W, sy = c.height / RINK_H;
  g.fillStyle = '#F3F7FB'; g.fillRect(0, 0, c.width, c.height);
  // faint ice texture
  for (let i = 0; i < 4000; i++) {
    g.fillStyle = `rgba(120,160,200,${Math.random() * 0.08})`;
    g.fillRect(Math.random() * c.width, Math.random() * c.height, 2, 2);
  }
  const line = (x, color, w) => { g.fillStyle = color; g.fillRect(x * sx - w / 2, 0, w, c.height); };
  line(RINK_W / 2, '#E0273F', 10);
  line(RINK_W / 2 - 8.6, '#2458C5', 10);
  line(RINK_W / 2 + 8.6, '#2458C5', 10);
  line(4, '#E0273F', 5);
  line(RINK_W - 4, '#E0273F', 5);
  const circle = (x, y, r, color, w) => { g.strokeStyle = color; g.lineWidth = w; g.beginPath(); g.arc(x * sx, y * sy, r * sx, 0, Math.PI * 2); g.stroke(); };
  const dot = (x, y, color) => { g.fillStyle = color; g.beginPath(); g.arc(x * sx, y * sy, 0.3 * sx, 0, Math.PI * 2); g.fill(); };
  circle(RINK_W / 2, RINK_H / 2, 4.5, '#2458C5', 6);
  [[14, 6.5], [14, RINK_H - 6.5], [RINK_W - 14, 6.5], [RINK_W - 14, RINK_H - 6.5]].forEach(([x, y]) => { circle(x, y, 4.5, '#E0273F', 6); dot(x, y, '#E0273F'); });
  [[RINK_W / 2 - 5, 6.5], [RINK_W / 2 - 5, RINK_H - 6.5], [RINK_W / 2 + 5, 6.5], [RINK_W / 2 + 5, RINK_H - 6.5]].forEach(([x, y]) => dot(x, y, '#E0273F'));
  dot(RINK_W / 2, RINK_H / 2, '#2458C5');
  // creases
  const crease = (x, dir) => { g.fillStyle = 'rgba(80,160,230,0.55)'; g.beginPath(); g.arc(x * sx, (RINK_H / 2) * sy, 1.8 * sx, -Math.PI / 2 * dir, Math.PI / 2 * dir, dir < 0); g.fill(); g.strokeStyle = '#E0273F'; g.lineWidth = 4; g.stroke(); };
  crease(4, 1); crease(RINK_W - 4, -1);
  // centre logo
  g.save(); g.translate(c.width / 2, c.height / 2);
  g.font = `900 ${Math.round(2.2 * sx)}px Outfit, sans-serif`; g.textAlign = 'center'; g.textBaseline = 'middle';
  g.fillStyle = 'rgba(224,39,63,0.9)'; g.fillText('FULLRINK', 0, 0);
  g.restore();
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
}
const iceShape = roundedRect(RINK_W, RINK_H, RINK_R);
const iceGeo = new THREE.ShapeGeometry(iceShape, 24);
// map UVs to the rink rectangle
{
  const uv = iceGeo.attributes.uv; const pos = iceGeo.attributes.position;
  for (let i = 0; i < uv.count; i++) uv.setXY(i, (pos.getX(i) + RINK_W / 2) / RINK_W, (pos.getY(i) + RINK_H / 2) / RINK_H);
}
const ice = new THREE.Mesh(iceGeo, new THREE.MeshStandardMaterial({ map: iceTexture(), roughness: 0.25, metalness: 0.05 }));
ice.rotation.x = -Math.PI / 2; ice.position.y = 0.02; ice.receiveShadow = true;
scene.add(ice);

// ---------- boards and glass ----------
function ring(w, h, r, thickness, height, material, y) {
  const outer = roundedRect(w + thickness * 2, h + thickness * 2, r + thickness);
  outer.holes.push(roundedRect(w, h, r));
  const geo = new THREE.ExtrudeGeometry(outer, { depth: height, bevelEnabled: false, curveSegments: 24 });
  const m = new THREE.Mesh(geo, material);
  m.rotation.x = -Math.PI / 2; m.position.y = y + height; // extrude goes -y after rotation, so lift
  m.rotation.x = Math.PI / 2; m.position.y = y; // extrude along +y
  m.castShadow = true; m.receiveShadow = true;
  scene.add(m);
  return m;
}
ring(RINK_W, RINK_H, RINK_R, 0.25, 1.1, mat(0xF2F2F5), 0);                       // boards
ring(RINK_W, RINK_H, RINK_R, 0.25, 0.25, mat(0xE0273F), 0);                      // kick plate (red)
ring(RINK_W, RINK_H, RINK_R, 0.12, 1.6, new THREE.MeshPhysicalMaterial({ color: 0xBFE3FF, transparent: true, opacity: 0.18, roughness: 0.05, metalness: 0, transmission: 0.2 }), 1.1); // glass

// goals
function goal(x, dir) {
  const red = mat(0xE0273F);
  const g = new THREE.Group();
  g.add(new THREE.Mesh(new THREE.BoxGeometry(0.1, 1.2, 1.9), red).translateY(0.6));
  const post = (z) => { const p = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.08, 0.08), red); p.position.set(0.5 * dir, 1.2, z); return p; };
  g.add(post(0.9)); g.add(post(-0.9));
  const net = new THREE.Mesh(new THREE.BoxGeometry(1.1, 1.2, 1.9), new THREE.MeshStandardMaterial({ color: 0xFFFFFF, transparent: true, opacity: 0.25, wireframe: true }));
  net.position.set(0.55 * dir, 0.6, 0); g.add(net);
  g.position.set(x, 0, 0); scene.add(g);
}
goal(-RINK_W / 2 + 4, -1); goal(RINK_W / 2 - 4, 1);

// ---------- surroundings ----------
const P = palette();
const floor = new THREE.Mesh(new THREE.PlaneGeometry(220, 160), mat(P.floor, { roughness: 0.95 }));
floor.rotation.x = -Math.PI / 2; floor.position.y = -0.01; floor.receiveShadow = true; scene.add(floor);
const buildMat = mat(P.build), standMat = mat(P.stand), seatMat = mat(0xE0273F, { roughness: 0.6 });

// benches (player side, -z)
const benchA = box(13, 1.0, 2.2, mat(0x2A2A33), -8, 0.5, -RINK_H / 2 - 1.6);
const benchB = box(13, 1.0, 2.2, mat(0x2A2A33), 8, 0.5, -RINK_H / 2 - 1.6);
[-8, 8].forEach((x) => box(13, 0.15, 2.6, mat(0xE0273F), x, 2.6, -RINK_H / 2 - 1.7)); // bench roofs
// penalty boxes + scorer's table (+z)
box(5, 1.0, 2.0, mat(0x2A2A33), -6, 0.5, RINK_H / 2 + 1.5);
box(5, 1.0, 2.0, mat(0x2A2A33), 6, 0.5, RINK_H / 2 + 1.5);
const scorer = box(4, 0.9, 1.6, mat(0x3A3A44), 0, 0.45, RINK_H / 2 + 1.4);
// stands on +z
for (let i = 0; i < 5; i++) box(RINK_W + 6, 0.8, 2.2, i % 2 ? standMat : seatMat, 0, 0.4 + i * 0.8, RINK_H / 2 + 5 + i * 2.2);
// stands on -z behind benches
for (let i = 0; i < 4; i++) box(RINK_W + 6, 0.8, 2.2, i % 2 ? seatMat : standMat, 0, 0.4 + i * 0.8, -RINK_H / 2 - 5 - i * 2.2);
// buildings: training room (-x), lobby (+x)
const training = box(16, 5, 30, buildMat, -RINK_W / 2 - 14, 2.5, 0);
const lobby = box(14, 5, 34, buildMat, RINK_W / 2 + 13, 2.5, 0);
// roof trusses hint: thin beams
for (let i = -2; i <= 2; i++) box(RINK_W + 20, 0.4, 0.6, mat(0x2A2A33), 0, 14, i * 9, false);
// scoreboard hanging over centre
function scoreboardTexture() {
  const c = document.createElement('canvas'); c.width = 1024; c.height = 400; const g = c.getContext('2d');
  g.fillStyle = '#0B0E14'; g.fillRect(0, 0, c.width, c.height);
  g.strokeStyle = '#3A4252'; g.lineWidth = 8; g.strokeRect(12, 12, c.width - 24, c.height - 24);
  g.textAlign = 'center'; g.textBaseline = 'middle';
  g.fillStyle = '#8A8A96'; g.font = '700 34px JetBrains Mono, monospace';
  g.fillText('BKK ZEUS', 220, 90); g.fillText('3A', 804, 90); g.fillText('PERIOD', 512, 300);
  g.fillStyle = '#F43F5E'; g.font = '900 150px Outfit, sans-serif'; g.fillText('1', 220, 215);
  g.fillStyle = '#8B5CF6'; g.fillText('0', 804, 215);
  g.fillStyle = '#35D07F'; g.font = '900 120px JetBrains Mono, monospace'; g.fillText('7:19', 512, 190);
  g.fillStyle = '#FAFAFA'; g.font = '900 60px Outfit, sans-serif'; g.fillText('1', 512, 350);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
const sbTex = scoreboardTexture();
const sbMats = [mat(0x1A1A20), mat(0x1A1A20), mat(0x1A1A20), mat(0x1A1A20),
  new THREE.MeshStandardMaterial({ map: sbTex, emissive: 0xFFFFFF, emissiveMap: sbTex, emissiveIntensity: 1.2, roughness: 0.4 }),
  new THREE.MeshStandardMaterial({ map: sbTex, emissive: 0xFFFFFF, emissiveMap: sbTex, emissiveIntensity: 1.2, roughness: 0.4 })];
const scoreboard = new THREE.Mesh(new THREE.BoxGeometry(9, 3.5, 2.2), sbMats);
scoreboard.position.set(0, 10.5, 0); scoreboard.castShadow = true; scene.add(scoreboard);
[-3, 3].forEach((x) => box(0.12, 2, 0.12, mat(0x55555F), x, 13.2, 0, false));

// camera phone on a tripod (Live By) at a corner behind the glass
const tripod = new THREE.Group();
const legMat = mat(0x2A2A33);
for (let i = 0; i < 3; i++) {
  const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 2.2, 8), legMat);
  const a = (i / 3) * Math.PI * 2; leg.position.set(Math.cos(a) * 0.5, 1.1, Math.sin(a) * 0.5); leg.rotation.z = Math.cos(a) * 0.25; leg.rotation.x = -Math.sin(a) * 0.25; leg.castShadow = true; tripod.add(leg);
}
const phone = new THREE.Mesh(new THREE.BoxGeometry(0.45, 0.9, 0.06), new THREE.MeshStandardMaterial({ color: 0x111115, emissive: 0x3B82F6, emissiveIntensity: 0.6 }));
phone.position.set(0, 2.4, 0); tripod.add(phone);
tripod.position.set(-RINK_W / 2 + 3, 0, -RINK_H / 2 - 3.2); tripod.lookAt(0, 1, 0); scene.add(tripod);

// players
function player(x, z, color, angle) {
  const g = new THREE.Group();
  const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.32, 0.9, 4, 10), mat(color, { roughness: 0.6 })); body.position.y = 0.95; body.castShadow = true; g.add(body);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.24, 12, 12), mat(0x111115)); head.position.y = 1.72; g.add(head);
  const stick = new THREE.Mesh(new THREE.BoxGeometry(0.06, 1.5, 0.06), mat(0xE8D5B3)); stick.position.set(0.45, 0.75, 0.2); stick.rotation.z = -0.5; g.add(stick);
  g.position.set(x, 0, z); g.rotation.y = angle; scene.add(g);
  return g;
}
const RED = 0xF43F5E, VIO = 0x8B5CF6;
[[-18, 4], [-10, -6], [-4, 2], [6, -5], [12, 6]].forEach(([x, z], i) => player(x, z, RED, i));
[[-14, -3], [-6, 7], [2, -8], [9, 1], [16, -4]].forEach(([x, z], i) => player(x, z, VIO, i + 2));
player(-RINK_W / 2 + 4.8, 0, 0x111115, Math.PI / 2); player(RINK_W / 2 - 4.8, 0, 0x111115, -Math.PI / 2); // goalies
const puck = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.05, 16), mat(0x111115)); puck.position.set(-3.4, 0.06, 1.8); scene.add(puck);
// parking hint (+x beyond lobby)
for (let i = 0; i < 7; i++) box(2.2, 0.9, 4.6, mat([0x2A2A33, 0x3A3A44, 0xE0273F, 0x1F5FD6][i % 4]), RINK_W / 2 + 28, 0.45, -16 + i * 5.2);

// ---------- lights ----------
scene.add(new THREE.HemisphereLight(0xBFD4FF, 0x202024, 0.75));
const sun = new THREE.DirectionalLight(0xFFFFFF, 1.6);
sun.position.set(40, 60, 25); sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, { left: -80, right: 80, top: 60, bottom: -60, near: 10, far: 180 });
scene.add(sun);
const rinkLight = new THREE.PointLight(0xDDEEFF, 60, 80, 1.6); rinkLight.position.set(0, 16, 0); scene.add(rinkLight);

// ---------- hotspots / labels ----------
const spots = [
  { id: 'liveby', n: '01', name: 'Live By', where: 'Camera on the tripod, scoreboard on the stream', pos: [-RINK_W / 2 + 3, 3.2, -RINK_H / 2 - 3.2], cam: [[-RINK_W / 2 - 8, 8, -RINK_H / 2 - 14], [-RINK_W / 2 + 8, 1.5, -RINK_H / 2 + 2]] },
  { id: 'dejavucam', n: '02', name: 'DejaVu Cam', where: 'Second phone on the bench, tap after the goal', pos: [-8, 3.4, -RINK_H / 2 - 1.6], cam: [[-14, 9, -RINK_H / 2 - 16], [-6, 1, -RINK_H / 2 + 4]] },
  { id: 'mobilevar', n: '03', name: 'Mobile VAR', where: 'Officials check the disputed play at the penalty box', pos: [-6, 2.4, RINK_H / 2 + 1.5], cam: [[-4, 8, RINK_H / 2 + 16], [-6, 1, RINK_H / 2 - 2]] },
  { id: 'analytic-cam', n: '04', name: 'Analytic Cam', where: 'Training room: skating technique from a clip', pos: [-RINK_W / 2 - 14, 6, 0], cam: [[-RINK_W / 2 - 34, 14, 18], [-RINK_W / 2 - 14, 2, 0]] },
  { id: 'scoreboard', n: '05', name: 'Live By Scoreboard', where: 'The hanging board, also on any browser', pos: [0, 13.2, 0], cam: [[6, 14, 26], [0, 10, 0]] },
  { id: 'gamemap', n: '06', name: 'GameMap', where: 'Scorer’s table: positions marked on the rink map', pos: [0, 2.4, RINK_H / 2 + 1.4], cam: [[0, 40, 48], [0, 0, 6]] },
];
const labelObjs = [];
for (const s of spots) {
  const el = document.createElement('a');
  el.className = 'r3-label';
  el.dataset.id = s.id;
  el.href = `apps/${s.id}`;
  el.innerHTML = `<b>${s.n}</b><span>${s.name}</span><small>${s.where}</small>`;
  el.addEventListener('click', (e) => { if (!e.metaKey && !e.ctrlKey) { e.preventDefault(); flyTo(s.id); } });
  const o = new CSS2DObject(el); o.position.set(...s.pos); scene.add(o); labelObjs.push(o);
}

// ---------- camera moves ----------
const OVERVIEW = { pos: [50, 60, 78], target: [-24, 0, 2] };
let fly = null;
function flyTo(id) {
  const s = spots.find((x) => x.id === id);
  const to = s ? { pos: s.cam[0], target: s.cam[1] } : OVERVIEW;
  fly = { from: { pos: camera.position.clone(), target: controls.target.clone() }, to: { pos: new THREE.Vector3(...to.pos), target: new THREE.Vector3(...to.target) }, t: 0 };
  controls.autoRotate = false;
  document.querySelectorAll('.r3-panel [data-fly]').forEach((b) => b.classList.toggle('is-active', b.dataset.fly === (s ? id : 'overview')));
  labelObjs.forEach((o) => o.element.classList.toggle('is-active', !!s && o.element.dataset.id === s.id));
}
camera.position.set(...OVERVIEW.pos); controls.target.set(...OVERVIEW.target);

// ---------- UI wiring ----------
document.querySelectorAll('[data-fly]').forEach((b) => b.addEventListener('click', () => flyTo(b.dataset.fly)));
const labelsBtn = document.querySelector('[data-labels]');
labelsBtn && labelsBtn.addEventListener('click', () => { const on = host.classList.toggle('labels-off'); labelsBtn.setAttribute('aria-pressed', String(!on)); });
const saveBtn = document.querySelector('[data-save]');
saveBtn && saveBtn.addEventListener('click', () => {
  renderer.render(scene, camera);
  const a = document.createElement('a'); a.download = 'fullrink-rink.png'; a.href = renderer.domElement.toDataURL('image/png'); a.click();
});
new MutationObserver(() => { const p = palette(); scene.background.set(p.bg); scene.fog.color.set(p.bg); floor.material.color.set(p.floor); buildMat.color.set(p.build); standMat.color.set(p.stand); })
  .observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

// ---------- resize + loop ----------
function resize() {
  const w = host.clientWidth, h = host.clientHeight;
  camera.aspect = w / h; camera.updateProjectionMatrix();
  renderer.setSize(w, h); labelRenderer.setSize(w, h);
}
new ResizeObserver(resize).observe(host); resize();
const ease = (t) => (t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t);
let last = performance.now();
let visible = true;
new IntersectionObserver((e) => { visible = e[0].isIntersecting; }, { threshold: 0.05 }).observe(host);
function loop(now) {
  requestAnimationFrame(loop);
  if (!visible) return;
  const dt = Math.min((now - last) / 1000, 0.05); last = now;
  if (fly) {
    fly.t = Math.min(1, fly.t + dt / 1.1); const k = ease(fly.t);
    camera.position.lerpVectors(fly.from.pos, fly.to.pos, k);
    controls.target.lerpVectors(fly.from.target, fly.to.target, k);
    if (fly.t >= 1) fly = null;
  }
  puck.position.x = -3.4 + Math.sin(now / 900) * 1.2;
  controls.update();
  renderer.render(scene, camera);
  labelRenderer.render(scene, camera);
}
requestAnimationFrame(loop);
host.classList.add('is-ready');
