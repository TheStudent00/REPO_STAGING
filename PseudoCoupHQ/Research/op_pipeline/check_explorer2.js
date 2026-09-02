// check_explorer2.js -- headless check of cluster_explorer2.html.
//
// Three things are asserted, and the first is the one the old page got
// wrong: the shown view must actually compute to display:block.  The
// defect was a class rule losing to an id rule; the fix is the
// `#detail-view.active` pattern, and this check would catch its
// removal.
//
//   1. the detail view computes to display:block on boot, and the
//      overview computes to none
//   2. the svg canvas has drawn nodes
//   3. no dropdown entry is a bare operator token
//
// usage:
//   npm i jsdom --prefix /tmp/jsdomhome
//   NODE_PATH=/tmp/jsdomhome/node_modules node check_explorer2.js
// (jsdom is installed outside the repo on purpose, so no node_modules
// tree lands in the research folder.)

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const HERE = __dirname;
const page = path.join(HERE, 'cluster_explorer2.html');
const html = fs.readFileSync(page, 'utf8');

const dom = new JSDOM(html, { runScripts: 'dangerously',
                              pretendToBeVisual: true });
const doc = dom.window.document;

function shown(id) {
  const e = doc.getElementById(id);
  return dom.window.getComputedStyle(e).display;
}

const detail = shown('detail-view');
const overview = shown('overview-view');
console.log('detail-view   computed display: ' + detail);
console.log('overview-view computed display: ' + overview);

const nodes = doc.querySelectorAll('#canvas g.node');
const hulls = doc.querySelectorAll('#canvas rect');
console.log('drawn nodes on the boot row: ' + nodes.length);
console.log('drawn group hulls on the boot row: ' + hulls.length);

const opts = Array.from(doc.querySelectorAll('#rowselect option'));
console.log('dropdown entries: ' + opts.length);
console.log('first three dropdown entries:');
opts.slice(0, 3).forEach(o => console.log('   ' + o.textContent));
console.log('boot row: ' + doc.getElementById('rowselect').value +
            ' -> ' + opts[Number(doc.getElementById('rowselect').value)]
                       .textContent);
console.log('rownote: ' + doc.getElementById('rownote').textContent);

// the tokens, straight from the manifests
const toks = new Set();
fs.readdirSync(HERE).filter(f => f.startsWith('probe_manifest_') &&
                                 f.endsWith('.json')).forEach(f => {
  const d = JSON.parse(fs.readFileSync(path.join(HERE, f), 'utf8'));
  Object.values(d.probes || {}).forEach(p => {
    if (typeof p.operator === 'string' && p.operator.trim()) toks.add(p.operator);
  });
});
const bare = opts.filter(o => toks.has(o.textContent.trim()));
console.log('dropdown entries that are a bare operator token: ' + bare.length);

// switch views, so the toggle is exercised too
doc.getElementById('btn-overview').dispatchEvent(
  new dom.window.Event('click', { bubbles: true }));
console.log('after clicking Overview -- overview: ' + shown('overview-view') +
            ', detail: ' + shown('detail-view'));
console.log('overview rows rendered: ' +
            doc.querySelectorAll('#rowlist .rowitem').length);

let bad = 0;
if (detail !== 'block') { console.log('FAIL: detail view is not block'); bad++; }
if (overview !== 'none') { console.log('FAIL: overview view is not none'); bad++; }
if (nodes.length < 2) { console.log('FAIL: too few drawn nodes'); bad++; }
if (bare.length > 0) { console.log('FAIL: a dropdown entry is a bare token'); bad++; }
if (shown('overview-view') !== 'block') { console.log('FAIL: overview did not show'); bad++; }
console.log(bad === 0 ? 'CHECK PASS' : 'CHECK FAIL (' + bad + ')');
process.exit(bad === 0 ? 0 : 1);
