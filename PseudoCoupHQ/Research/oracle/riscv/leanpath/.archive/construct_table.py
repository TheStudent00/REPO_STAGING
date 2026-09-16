"""construct_table.py -- the side-by-side table of the construction stage,
for the eye: one row per (clause, variant, place, language, way) with
D (Sail's pure form, Lean text and the z3 reading), E (the printed
emulation: file, statements, how many nodes went the plain way and the
built way), U (the lowered instructions), L (the expression composed
back from U through Sail's own decoder). No proof in it.

  python3 construct_table.py <construct dir> <walk dir>... > table.md
"""
import json, os, sys, collections

cdir = sys.argv[1]
walks = {}
for d in sys.argv[2:]:
    p = os.path.join(d, "walk.json")
    if os.path.exists(p):
        for r in json.load(open(p))["rows"]:
            walks[r["unit"]] = r
cell = lambda s: str(s).replace("|", "\\|").replace("\n", " ")[:110]
C = json.load(open(os.path.join(cdir, "construct.json")))
rows = C["rows"]
print("# the construction, side by side: D, E, U, L\n")
print("Counts: %s\n" % json.dumps(C["counts"]))
print("Lowered and composed (the walk, certification off): %d units\n" % len(walks))
verd = collections.Counter(r["verdict"] for r in walks.values())
print("| walk verdict | units |\n|---|---|"); [print("| %s | %d |" % (k, n)) for k, n in verd.most_common()]
print("\n## per clause: variants, places, and how the lowering went\n")
print("| clause | variants | places | files printed | lowered and composed | refused at lowering | printer refusals | term failures |")
print("|---|---|---|---|---|---|---|---|")
per = collections.defaultdict(lambda: collections.Counter())
for r in rows:
    c = r["clause"]
    if "deferred" in r:
        per[c]["deferred"] += 1; continue
    per[c]["variants_places"] += 1
    if "term_failure" in r:
        per[c]["term_failures"] += 1; continue
    for key, f in r["files"].items():
        if "refused" in f:
            per[c]["printer_refusals"] += 1; continue
        per[c]["files"] += 1
        u = walks.get(os.path.basename(f["path"]).rsplit(".", 1)[0])
        if u is None: continue
        if u["verdict"] in ("COMPOSED", "CERTIFIED"): per[c]["composed"] += 1
        elif u["verdict"] == "REFUSED": per[c]["refused"] += 1
for c in sorted(per):
    n = per[c]
    if n["deferred"]:
        print("| %s | deferred | | | | | | |" % c); continue
    print("| %s | %d | | %d | %d | %d | %d | %d |" % (c, n["variants_places"], n["files"], n["composed"], n["refused"], n["printer_refusals"], n["term_failures"]))
print("\n## kinds deferred (not constructed) and why\n")
print("| clause | why |\n|---|---|")
for r in rows:
    if "deferred" in r and "variant" not in r:
        print("| %s | %s |" % (r["clause"], cell(r["deferred"])))
print("\n## terms that could not be built or printed\n")
print("| clause | variant | place | why |\n|---|---|---|---|")
for r in rows:
    if "term_failure" in r:
        print("| %s | %s | %s | %s |" % (r["clause"], cell(r.get("variant")), r.get("place"), cell(r["term_failure"])))
print("\n## every row\n")
print("| clause | variant | place | D (Lean) | D (z3, simplified) | D size: shared/tree nodes | inputs in 64-bit slots | language | way | E: statements (plain/built nodes) | U: instructions | U: the first three | L (composed) | walk |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    if "deferred" in r or "term_failure" in r:
        continue
    size = "%s/%s" % (r.get("dag_nodes", ""), r.get("tree_nodes", ""))
    slots = ", ".join(r.get("slotted", [])) or "none"
    for key, f in sorted(r["files"].items()):
        lang, way = key.split("__")
        if "refused" in f:
            print("| %s | %s | %s | %s | %s | %s | %s | %s | %s | printer refused: %s | | | | |" % (r["clause"], cell(r.get("variant")), r["place"], cell(r["D_lean"]), cell(r.get("D_z3")), size, slots, lang, way, cell(f["refused"])))
            continue
        u = walks.get(os.path.basename(f["path"]).rsplit(".", 1)[0])
        U = u.get("instructions") if u else None
        first3 = "; ".join(i["display"] for i in (U or [])[:3])
        n = (len(U) - 1) if U else ""
        L = u.get("proposal", "") if u else ""
        v = (u["verdict"] if u else "not walked") + ((": " + (u.get("why") or "")[:40]) if u and u["verdict"] == "REFUSED" else "")
        print("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %d (%d/%d) | %s | %s | %s | %s |" % (r["clause"], cell(r.get("variant")), r["place"], cell(r["D_lean"]), cell(r.get("D_z3")), size, slots, lang, way, f["statements"], f["native_nodes"], f["constructed_nodes"], n, cell(first3), cell(L), cell(v)))
