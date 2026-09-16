"""tally_corpus_final.py -- the per-language, per-arch-opcode, per-arch-unit
tables of pass A with totals, from the walk and equals records in this
folder. `python3 tally_corpus_final.py > tally_corpus_final.md`."""
import json, glob, collections, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from leanpath.equals import enum_values
def L(p): return json.load(open(p))
walk = {}
for k in ("0", "1", "2", "3", "fix2"):
    for r in L("walk_corpus_%s/walk.json" % k)["rows"]: walk[r["unit"]] = r
eq = {}
for d in sorted(glob.glob("equals_corpus_j_*")) + sorted(glob.glob("equals_corpus_survivors3_*")):
    p = os.path.join(d, "equals.json")
    if os.path.exists(p):
        for r in L(p)["rows"]: eq[r["unit"]] = r
lang = lambda u: re.search(r"__(c|cpp|rust|go)__", u).group(1)
route = lambda u: "all_constructed" if "all_constructed" in u else "native_first"
langs = ["c", "cpp", "rust", "go"]
strip = L("strip_6266b40c_8eb1fb6b_all_v5/strip.json")["rows"]
lean_dir = "cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/LeanIM"
cert_clauses = {r["clause"][8:]: r for r in strip if r["verdict"] == "CERTIFIED"}
def enumerable(name):
    r = cert_clauses.get(name)
    if not r or r.get("shape") != "straight": return None
    return all(enum_values(lean_dir, t.strip("() ")) is not None for n, t in r["params"] if t != "regidx")
heads = lambda u: re.findall(r"pure_(\w+)", walk[u]["proposal"])
def classify(u):
    r = walk[u]; e = eq.get(u)
    if r["verdict"] != "CERTIFIED": return "refused"
    if e and e["proved"]: return "matched"
    hs = heads(u)
    if not hs: return "identity"
    if len(set(hs)) == 1 and len(hs) == 1 and enumerable(hs[0]) is False: return "own opcode not a candidate (immediate)"
    if e and any(x["verdict"] in ("UNDECIDED", "NOT_TRIED") for x in e["results"]) and any(x["verdict"] != "REFUTED_BY_EVALUATION" for x in e["results"]): return "open (survived evaluation)"
    return "composite, every candidate refuted"
cls = {u: classify(u) for u in walk}
print("# tally of the corpus: per language, per arch-opcode, per arch-unit, with totals\n")
print("Computed from `walk_corpus_{0,1,2,3,fix2}/walk.json`, `equals_corpus_j_*/equals.json` and `equals_corpus_survivors3_*/equals.json` by `tally_corpus_final.py` beside this file; the tower's `tally_corpus_final.json` gives the same totals.\n")
print("## per language (one arch-unit compiled from each of the 490 rendered sources per language; the same 255 cells for every language, log 279)\n")
print("| language | rendered sources | proof 1 certified | proof 2 matched | same text | integer level | bit level | identity (bare return) | own opcode not a candidate (immediate) | composite, all candidates refuted | open | refused |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for lg in langs + ["all"]:
    us = [u for u in walk if lg == "all" or lang(u) == lg]; c = collections.Counter(cls[u] for u in us)
    st = collections.Counter(eq[u]["proved"][0][2] for u in us if cls[u] == "matched")
    cert = sum(1 for u in us if walk[u]["verdict"] == "CERTIFIED")
    print("| %s | %d | %d | %d | %d | %d | %d | %d | %d | %d | %d | %d |" % (lg, len(us), cert, c["matched"], st["same_text"], st["integer_level"], st["fixed_width"], c["identity"], c["own opcode not a candidate (immediate)"], c["composite, every candidate refuted"], c["open (survived evaluation)"], c["refused"]))
print("\n## per language and route\n")
print("| language | route | units | certified | matched | refused |"); print("|---|---|---|---|---|---|")
for lg in langs:
    for rt in ("native_first", "all_constructed"):
        us = [u for u in walk if lang(u) == lg and route(u) == rt]
        print("| %s | %s | %d | %d | %d | %d |" % (lg, rt, len(us), sum(1 for u in us if walk[u]["verdict"] == "CERTIFIED"), sum(1 for u in us if cls[u] == "matched"), sum(1 for u in us if cls[u] == "refused")))
print("\n## per arch-opcode (the Sail clauses)\n")
print("Sail clauses in the emit: %d. Certified by strip, so usable as definitions: %d (%d straight, %d aliases). Refused: %d. Failed: %d.\n" % (len(strip), len(cert_clauses), sum(1 for r in cert_clauses.values() if r.get("shape") == "straight"), sum(1 for r in cert_clauses.values() if r.get("shape") == "alias"), sum(1 for r in strip if r["verdict"] == "REFUSED"), sum(1 for r in strip if r["verdict"] == "FAILED")))
byop = collections.defaultdict(collections.Counter)
for u in walk:
    if cls[u] == "matched": byop[eq[u]["proved"][0][0]][lang(u)] += 1
print("### matched as the meaning of a unit (proof 2), per language\n")
print("| Sail clause | c | cpp | rust | go | total |"); print("|---|---|---|---|---|---|")
T = collections.Counter()
for op in sorted(byop, key=lambda o: -sum(byop[o].values())):
    c = byop[op]; print("| %s | %d | %d | %d | %d | %d |" % (op, c["c"], c["cpp"], c["rust"], c["go"], sum(c.values()))); T.update(c)
print("| total | %d | %d | %d | %d | %d |" % (T["c"], T["cpp"], T["rust"], T["go"], sum(T.values())))
inprop = collections.defaultdict(collections.Counter)
for u in walk:
    if walk[u]["verdict"] == "CERTIFIED":
        for h in set(heads(u)): inprop[h][lang(u)] += 1
print("\n### present in a certified unit's expression (proof 1), per language (units containing the clause)\n")
print("| Sail clause | enumerable params | c | cpp | rust | go | total |"); print("|---|---|---|---|---|---|---|")
T = collections.Counter()
for op in sorted(inprop, key=lambda o: -sum(inprop[o].values())):
    c = inprop[op]; e = enumerable(op); print("| %s | %s | %d | %d | %d | %d | %d |" % (op, {True: "yes", False: "no (immediate)", None: "alias/other"}[e], c["c"], c["cpp"], c["rust"], c["go"], sum(c.values()))); T.update(c)
print("| total (clause-unit pairs) | | %d | %d | %d | %d | %d |" % (T["c"], T["cpp"], T["rust"], T["go"], sum(T.values())))
straight = sorted(op for op, r in cert_clauses.items() if r.get("shape") == "straight")
print("\n### all %d straight clauses certified by strip\n" % len(straight))
print("| Sail clause | enumerable params | in a unit's expression | matched as a meaning |"); print("|---|---|---|---|")
for op in straight: print("| %s | %s | %d | %d |" % (op, "yes" if enumerable(op) else "no (immediate)", sum(inprop[op].values()), sum(byop[op].values())))
print("| total | | %d clauses used | %d clauses matched |" % (sum(1 for op in straight if inprop[op]), sum(1 for op in straight if byop[op])))
print("\n## per arch-unit (all %d)\n" % len(walk))
print("| unit | language | route | proof 1 | instructions | classification | opcode | stage |"); print("|---|---|---|---|---|---|---|---|")
for u in sorted(walk):
    r = walk[u]; e = eq.get(u); op = e["proved"][0][0] if e and e["proved"] else ""; stg = e["proved"][0][2] if e and e["proved"] else ""
    n = max(len(r.get("instructions", [])) - 1, 0) if r["verdict"] == "CERTIFIED" else ""
    v = r["verdict"] if r["verdict"] != "REFUSED" else "REFUSED: " + (r.get("why") or "")[:40].replace("|", "/")
    print("| %s | %s | %s | %s | %s | %s | %s | %s |" % (u, lang(u), route(u), v, n, cls[u], op, stg))
