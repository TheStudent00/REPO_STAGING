// minimal DOM stub: runs every <script> in a self-contained page and
// reports what each one wrote into which element.
const fs = require('fs'), vm = require('vm');
const file = process.argv[2];
const html = fs.readFileSync(file, 'utf8');
const ids = new Set([...html.matchAll(/id="([A-Za-z0-9_]+)"/g)].map(m => m[1]));
const made = {};
function mk(id) {
  const el = {
    id, _html: '', style: {}, dataset: {}, children: [], value: '',
    className: '', textContent: '',
    get innerHTML() { return this._html; },
    set innerHTML(v) { this._html = String(v); },
    appendChild(c) { this.children.push(c); return c; },
    addEventListener() {}, removeEventListener() {},
    getBoundingClientRect() { return {left:0,top:0,width:1000,height:600}; },
    setAttribute() {}, getAttribute() { return null; },
    querySelector() { return null; }, querySelectorAll() { return []; },
    focus() {}, blur() {}, remove() {}, contains() { return false; },
    scrollIntoView() {}, classList: { add(){}, remove(){}, toggle(){},
                                      contains(){ return false; } },
    insertAdjacentHTML(p, v) { this._html += String(v); },
  };
  return el;
}
for (const id of ids) made[id] = mk(id);
const document = {
  getElementById: id => made[id] || (made[id] = mk(id)),
  createElement: t => mk('<' + t + '>'),
  createElementNS: (n, t) => mk('<' + t + '>'),
  querySelector: () => null, querySelectorAll: () => [],
  addEventListener() {}, body: mk('body'), documentElement: mk('html'),
};
const win = {
  document, addEventListener() {}, removeEventListener() {},
  requestAnimationFrame: f => f(0), innerWidth: 1400, innerHeight: 900,
  devicePixelRatio: 1, getComputedStyle: () => ({ getPropertyValue: () => '' }),
  location: { href: 'file://' + file }, console,
};
win.window = win; win.self = win; win.globalThis = win;
const ctx = vm.createContext(win);
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
let ok = 0, bad = 0;
scripts.forEach((src, i) => {
  try { vm.runInContext(src, ctx, { filename: 'script#' + i }); ok++; }
  catch (e) { bad++; console.log('SCRIPT ' + i + ' THREW: ' + e.message); }
});
console.log('scripts: ' + scripts.length + ' run, ' + ok + ' ok, ' + bad + ' threw');
const filled = Object.entries(made).filter(([k, v]) => v._html.length > 0);
console.log('elements written: ' + filled.length);
for (const [k, v] of filled.sort()) console.log('  #' + k + ' -> ' + v._html.length + ' chars');
// Which ids a page MUST have drawn into is a property of the page, so it
// can be given on the command line:
//     node domstub.js <file.html> [drawn-ids] [filled-ids]
// `drawn-ids' are elements something must have APPENDED into or written
// text into; `filled-ids' are panels whose innerHTML must be non-empty.
// With no arguments both default to the dendrogram convention, so every
// earlier invocation in this node means exactly what it meant before.
const DRAWN = (process.argv[3] || 'chart,curve,count,thval').split(',');
const FILLED = (process.argv[4] || 'smat,sops,worked,plateaus,legend')
  .split(',');
for (const k of DRAWN) {
  const el = made[k];
  if (!el) { console.log('MISSING #' + k); bad++; continue; }
  console.log('  #' + k + ' -> ' + el.children.length + ' appended, text "'
              + el.textContent + '"');
}
const empty = FILLED.filter(k => !made[k] || made[k]._html.length === 0);
if (empty.length) { console.log('EMPTY PANELS: ' + empty.join(', ')); bad++; }
const first = made[DRAWN[0]];
const nchart = first ? first.children.length : 0;
if (!nchart) { console.log('#' + DRAWN[0] + ' EMPTY'); bad++; }
process.exit(bad ? 1 : 0);
