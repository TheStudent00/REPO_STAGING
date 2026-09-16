"""eye_check -- System.eye_check (plan node
hq.research.lean_proof_path_resistant_to_churn.system.eye_check): the
table the owner reads on the handful before the whole run: one row per
rendered emulation, D beside E beside U beside L, and what Lean said.

  python3 -m leanpath eye_check <render.json> <walk.json[,walk.json...]> [equals.json[,...]] > table.md

D  Sail's definition of the arch-opcode (its Lean text over the reads a, b, ...)
E  the emulation as rendered: the composition, and the corpus units it was built from
U  the compiled words, as instructions
L  the meaning read back through Sail's own decoder and definitions
"""
import json
import os
import sys


def cell(s, n=140):
    return str(s).replace("|", "\\|").replace("\n", " ")[:n]


def main(argv):
    render = json.load(open(argv[0]))
    walks = {}
    for p in argv[1].split(","):
        if os.path.exists(p):
            for r in json.load(open(p))["rows"]:
                walks[r["unit"]] = r
    proofs = {}
    if len(argv) > 2:
        for p in argv[2].split(","):
            if os.path.exists(p):
                for r in json.load(open(p))["rows"]:
                    proofs[r["unit"]] = r
    rows = render["rows"]
    print("# the eye table: D beside E beside U beside L\n")
    print("Rendered: %d. Refused at render: %d. Lowered and read back: %d.\n" % (render["rendered"], render["refused"], len(walks)))
    print("| definition | D: Sail's text over the reads | E: the composition | E: built from (subterm -> corpus unit) | U: instructions | L: the meaning read back | walk | proof |")
    print("|---|---|---|---|---|---|---|---|")
    for r in rows:
        name = "%s %s" % (r["clause"], r.get("arm", ""))
        if "refused" in r:
            print("| %s | %s | REFUSED: %s | | | | | |" % (name, cell(r.get("D", "")), cell(r["refused"], 100)))
            continue
        unit = os.path.basename(r["path"]).rsplit(".", 1)[0]
        w = walks.get(unit)
        U = "; ".join(i["display"] for i in (w or {}).get("instructions", [])[:8]) if w else "not lowered"
        L = (w or {}).get("proposal", "") if w else ""
        wv = (w["verdict"] + ((": " + (w.get("why") or "")[:50]) if w["verdict"] != "CERTIFIED" else "")) if w else "not walked"
        pr = proofs.get(unit)
        pv = ""
        if pr:
            ok = pr.get("proved") or []                 # [[definition, [operation], stage], ...]
            pv = ("PROVED equal to %s" % ", ".join("%s %s (%s)" % (c[0], " ".join(c[1]), c[2]) for c in ok[:2])) if ok else "not proved (%d candidates tried)" % pr.get("candidates", 0)
        built = "; ".join("%s -> %s" % (cell(b["subterm"], 40), b["unit"]) for b in r["built_from"])
        print("| %s | %s | %s | %s | %s | %s | %s | %s |" % (name, cell(r["D"]), cell(r["E"], 100), cell(built, 160), cell(U, 120), cell(L), cell(wv, 80), cell(pv, 80)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
