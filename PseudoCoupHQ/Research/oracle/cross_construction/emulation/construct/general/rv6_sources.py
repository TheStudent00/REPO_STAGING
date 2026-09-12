#!/usr/bin/env python3
"""rv6_sources: render (and only render) every RISC-V cell's emulation on
c, cpp, go, rust under both routes, and SAVE each source as a file — the
emulations themselves, for the record and the mirror. The compile step is
short-circuited: no compile, no gate, no verdict (rv6's store holds those).
    python3 rv6_sources.py run <ref_dir> <op_dir> <emulation_dir> <twins.json> <model_table_rv.json> <prefix> <src_out> <work>
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import rv_general as RG
RV_DIR = os.path.dirname(os.path.abspath(sys.argv[5])); sys.path.insert(0, RV_DIR)
import rv_loop as RL, inherit as INH, inherit_rv3 as INH3
INH3.install()
RL.untwinned = lambda tw: [{"mnem": r["mnem"], "shape": r["shape"], "key_width": r["key_width"],
                            "places": [p["writes"] for p in r["places"]]} for r in json.load(open(tw))["rows"]]
RG.TARGETS = ["c", "cpp", "go", "rust"]
OUT = sys.argv[8]; os.makedirs(OUT, exist_ok=True)
EXT = {"c": "c", "cpp": "cpp", "go": "go", "rust": "rs"}
_render = RG.RG.render
def render_and_save(ordered, target, families, home_family, bits, label, word, policy, text):
    made = _render(ordered, target, families, home_family, bits, label, word, policy, text)
    path = os.path.join(OUT, "%s.%s" % (label, EXT.get(target, target)))
    with open(path, "w") as f: f.write(made["source"])
    return made
RG.RG.render = render_and_save
def no_compile(source, target, work): return None, "(render only: rv6_sources)", "not compiled by design"
INH.compile_and_carve = no_compile
print("rv6_sources: rendering every RISC-V cell on %s into %s" % (RG.TARGETS, OUT), flush=True)
if __name__ == "__main__": sys.exit(RG.main())
