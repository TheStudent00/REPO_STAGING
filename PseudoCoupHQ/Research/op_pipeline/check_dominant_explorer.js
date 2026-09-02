// check_dominant_explorer.js -- headless check of dominant_explorer.html.
//
// The same pattern as check_explorer2.js, extended to three views:
//
//   1. the boot view (table) computes to display:block, the other two
//      to none -- the id-vs-class specificity defect would show here
//   2. cards render, and each card carries member chips
//   3. the evidence view draws nodes on its svg, and the tier slider
//      changes the drawn grouping
//   4. the landscape view draws one dot per class
//   5. no dropdown entry and no card heading is a bare operator token
//
// usage:
//   npm i jsdom --prefix /tmp/jsdomhome
//   NODE_PATH=/tmp/jsdomhome/node_modules node check_dominant_explorer.js

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const HERE = __dirname;
const page = path.join(HERE, 'dominant_explorer.html');
const html = fs.readFileSync(page, 'utf8');

const dom = new JSDOM(html, { runScripts: 'dangerously',
                              pretendToBeVisual: true });
const doc = dom.window.document;

function shown(id) {
  const e = doc.getElementById(id);
  return dom.window.getComputedStyle(e).display;
}

const tableD = shown('table-view');
const evD = shown('evidence-view');
const lsD = shown('landscape-view');
console.log('table-view     computed display: ' + tableD);
console.log('evidence-view  computed display: ' + evD);
console.log('landscape-view computed display: ' + lsD);

const cards = doc.querySelectorAll('#cards .card');
const chips = doc.querySelectorAll('#cards .chip');
const badges = doc.querySelectorAll('#cards .badge');
console.log('cards rendered on boot: ' + cards.length);
console.log('member chips on those cards: ' + chips.length);
console.log('fence badges on those cards: ' + badges.length);
console.log('table note: ' + doc.getElementById('tablenote').textContent);
console.log('first card heading: ' +
            doc.querySelector('#cards .card h3').textContent);

const nodes = doc.querySelectorAll('#canvas g.node');
const hulls = doc.querySelectorAll('#canvas rect');
console.log('evidence canvas drawn nodes (boot class, tier 1): ' +
            nodes.length);
console.log('evidence canvas group hulls: ' + hulls.length);

// move the slider to tier 4 and redraw
const slider = doc.getElementById('tierslider');
slider.value = '3';
slider.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
const nodes4 = doc.querySelectorAll('#canvas g.node').length;
const hulls4 = doc.querySelectorAll('#canvas rect').length;
console.log('after the slider moves to tier 4 -- nodes: ' + nodes4 +
            ', hulls: ' + hulls4);
console.log('tier label: ' + doc.getElementById('tierlabel').textContent);
console.log('evidence note: ' + doc.getElementById('evnote').textContent);

const dots = doc.querySelectorAll('#landscape circle.lsdot');
console.log('landscape dots drawn: ' + dots.length);

const classOpts = Array.from(doc.querySelectorAll('#classselect option'));
const tpOpts = Array.from(doc.querySelectorAll('#f-tp option'));
const evOpts = Array.from(doc.querySelectorAll('#f-ev option'));
console.log('class dropdown entries: ' + classOpts.length);
console.log('type-pair dropdown entries: ' + tpOpts.length);
console.log('weakest-evidence dropdown entries: ' +
            evOpts.map(o => o.textContent).join(' | '));
console.log('first three class dropdown entries:');
classOpts.slice(0, 3).forEach(o => console.log('   ' + o.textContent));

// the tokens, straight from the manifests
const toks = new Set();
fs.readdirSync(HERE).filter(f => f.startsWith('probe_manifest_') &&
                                 f.endsWith('.json')).forEach(f => {
  const d = JSON.parse(fs.readFileSync(path.join(HERE, f), 'utf8'));
  Object.values(d.probes || {}).forEach(p => {
    if (typeof p.operator === 'string' && p.operator.trim()) toks.add(p.operator);
  });
});
const allOpts = classOpts.concat(tpOpts).concat(evOpts)
  .concat(Array.from(doc.querySelectorAll('#f-lang option')))
  .concat(Array.from(doc.querySelectorAll('#f-modes option')))
  .concat(Array.from(doc.querySelectorAll('#f-sort option')));
const bare = allOpts.filter(o => toks.has(o.textContent.trim()));
console.log('dropdown entries that are a bare operator token: ' + bare.length);
const headings = Array.from(doc.querySelectorAll('#cards .card h3'));
const bareHead = headings.filter(h => toks.has(h.textContent.trim()));
console.log('card headings that are a bare operator token: ' + bareHead.length);

// exercise the view toggles
doc.getElementById('btn-landscape').dispatchEvent(
  new dom.window.Event('click', { bubbles: true }));
console.log('after clicking Landscape -- landscape: ' + shown('landscape-view') +
            ', table: ' + shown('table-view'));
doc.getElementById('btn-evidence').dispatchEvent(
  new dom.window.Event('click', { bubbles: true }));
console.log('after clicking Evidence  -- evidence: ' + shown('evidence-view'));

// a card's Evidence button must open that class in view 2
doc.getElementById('btn-table').dispatchEvent(
  new dom.window.Event('click', { bubbles: true }));
const openBtn = doc.querySelector('#cards button[data-open]');
const wanted = openBtn.getAttribute('data-open');
openBtn.dispatchEvent(new dom.window.Event('click', { bubbles: true }));
const evNote = doc.getElementById('evnote').textContent;
console.log('card button opened ' + wanted + ' -- evidence note starts: ' +
            evNote.slice(0, 40));

let bad = 0;
if (tableD !== 'block'){ console.log('FAIL: table view is not block'); bad++; }
if (evD !== 'none'){ console.log('FAIL: evidence view is not none'); bad++; }
if (lsD !== 'none'){ console.log('FAIL: landscape view is not none'); bad++; }
if (cards.length < 10){ console.log('FAIL: too few cards'); bad++; }
if (chips.length < 10){ console.log('FAIL: too few member chips'); bad++; }
if (nodes.length < 2){ console.log('FAIL: too few drawn nodes'); bad++; }
if (dots.length !== classOpts.length){
  console.log('FAIL: landscape dots do not match the class count'); bad++; }
if (bare.length > 0){ console.log('FAIL: a dropdown entry is a bare token'); bad++; }
if (bareHead.length > 0){ console.log('FAIL: a card heading is a bare token'); bad++; }
if (shown('evidence-view') !== 'block'){
  console.log('FAIL: evidence view did not show'); bad++; }
if (evNote.indexOf(wanted) !== 0){
  console.log('FAIL: the card button did not open its own class'); bad++; }
console.log(bad === 0 ? 'CHECK PASS' : 'CHECK FAIL (' + bad + ')');
process.exit(bad === 0 ? 0 : 1);
