#!/usr/bin/env node
// verify_dendro_extended.js -- headless (DOM-less) sanity for the
// extended threshold-spectrum explorer.  No jsdom available, so this
// pulls the inline `const DENDRO = {...}` embed straight out of the
// HTML the way a browser would and checks the two things the picture
// stands on: (1) the two independent cluster-count methods the page
// carries -- a band-walk over the tree nodes vs a count off the merge
// history -- agree at every threshold, for every family; (2) leaf
// counts, monotone merge heights, contiguous leaf order, and cross-link
// endpoints that are real leaves.  Mirrors the jsdom "counts match"
// check of logs 012/014 without a DOM.
const fs = require("fs");
const path = require("path");
const HERE = __dirname;

function loadEmbed() {
  const html = fs.readFileSync(path.join(HERE, "dendrogram_extended.html"), "utf8");
  const m = html.match(/const DENDRO = (\{[\s\S]*?\});\nconst LANG_COLOR/);
  if (!m) throw new Error("could not find the DENDRO embed in the HTML");
  return { html, DENDRO: JSON.parse(m[1]) };
}

function clustersWalk(fam, t) {
  const byId = new Map(fam.tree.nodes.map(r => [r.id, r]));
  let c = 0;
  (function g(r) {
    if (r.birth >= t) { c++; return; }
    for (const sid of r.subs) g(byId.get(sid));
  })(byId.get(fam.tree.root_id));
  return c;
}
function clustersHist(fam, t) {
  const sims = fam.merge_history.map(m => m.similarity);
  return fam.n_leaves - sims.filter(s => s >= t).length;
}

function main() {
  const { html, DENDRO } = loadEmbed();
  // the standalone JSON must match the embed
  const json = JSON.parse(fs.readFileSync(path.join(HERE, "dendro_extended.json"), "utf8"));
  let fail = 0;
  const A = (cond, msg) => { if (!cond) { console.log("  FAIL: " + msg); fail++; }
                             else console.log("  ok: " + msg); };

  A(JSON.stringify(Object.keys(json.families).sort())
      === JSON.stringify(Object.keys(DENDRO.families).sort()),
    "embed families == standalone JSON families");

  for (const name of DENDRO.family_order) {
    const fam = DENDRO.families[name];
    console.log("[" + name + "] " + fam.n_leaves + " leaves, "
      + fam.merge_history.length + " merges, " + fam.crosslinks.length + " cross-links");
    // leaf counts consistent three ways
    const leafNodes = fam.tree.nodes.filter(n => n.label !== null);
    A(fam.n_leaves === fam.leaves.length
      && fam.n_leaves === fam.tree.n_leaves
      && fam.n_leaves === leafNodes.length
      && fam.merge_history.length === fam.n_leaves - 1,
      name + ": leaf counts agree and merges == leaves-1");
    // monotone non-increasing merge heights
    let mono = true;
    for (let i = 1; i < fam.merge_history.length; i++)
      if (fam.merge_history[i].similarity > fam.merge_history[i-1].similarity + 1e-9) mono = false;
    A(mono, name + ": merge heights monotone non-increasing");
    // contiguous leaf order 0..n-1
    const xs = leafNodes.map(n => n.x0).sort((a,b)=>a-b);
    let contig = true;
    for (let i = 0; i < xs.length; i++) if (xs[i] !== i) contig = false;
    A(contig, name + ": leaf x0 positions contiguous 0.." + (fam.n_leaves-1));
    // the two count methods agree at every 0.01 step
    let mism = 0;
    for (let s = 0; s <= 100; s++) {
      const t = s/100;
      if (clustersWalk(fam, t) !== clustersHist(fam, t)) mism++;
    }
    A(mism === 0, name + ": band-walk vs merge-history counts agree at all 101 thresholds");
    // cross-link endpoints are real leaves
    const labs = new Set(fam.leaves);
    let bad = 0;
    for (const lk of fam.crosslinks) if (!labs.has(lk.a) || !labs.has(lk.b)) bad++;
    A(bad === 0, name + ": all cross-link endpoints are leaves of this family");
  }

  // the HTML must actually reference the embed and the family toggle
  A(/const DENDRO = \{/.test(html), "HTML embeds DENDRO inline (script-tag embed)");
  A(/loadFamily\(DENDRO\.family_order\[0\]\)/.test(html), "HTML boots the first family");
  A(/crosslinks/.test(html) && /congruence cross-link/.test(html),
    "HTML renders congruence cross-links with relation on hover");

  // named sanity readings
  const form = DENDRO.families.form, mant = DENDRO.families.mant;
  const mhit = mant.crosslinks.find(c =>
    (c.a==="go.+"&&c.b==="python.+")||(c.a==="python.+"&&c.b==="go.+"));
  A(mhit && /mod 2\^64/.test(mhit.relation),
    "mant: go.+ ~ python.+ cross-link carries a === mod 2^64 relation");
  A(form.leaves.includes("go.+") && form.leaves.includes("rust.+"),
    "form: go.+ and rust.+ are both leaves");

  console.log(fail === 0 ? "\nALL HEADLESS CHECKS PASSED"
                         : "\n" + fail + " CHECK(S) FAILED");
  process.exit(fail === 0 ? 0 : 1);
}
main();
