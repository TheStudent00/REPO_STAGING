"""python3 -m leanpath <command> ...

  definitions <LeanIM dir> <model source> <out.json>
      SailModel.definitions: the text listing of the execute clauses and
      their keys (needs no built model).
  harness <cache root> <project> <out.json>
      the Lean harness: writes Leanpath.lean from its template with the
      model's names (a listing), builds it in the working copy, runs the
      model's own init and reset in Lean to record the base state S0,
      builds LeanpathBase.
  handful <cache root> <project> <workdir> <out.json> [max_units]
      brief lanes 2-4 on the rv1 handful plus mulh on c: strip on the
      definition instances, meaning on each unit, equals in stages.
  pass_a <cache root> <project> <workdir> <sources dir> <out.json> <lang> <route> <count> <seconds>
      pass A over the rv6 corpus (a stated fraction: language, route,
      count) with the lane's time bound in seconds.
  kinds <units.json> <walk.json[,...]> <out.json> [LeanIM dir]
      LeanExpr.kinds: the primitive kind of every parameter and result
      DISCOVERED from each unit's Lean expression alone, compared
      against the manifest's declared holders.

Memory bound 6 GB resident on this driver (ABORT_MEMORY_LP1); the lean
processes it starts are bounded by the instance. One process, no pool.
"""

import json
import os
import re
import resource
import subprocess
import sys
import time

from .sail_model import SailModel
from .lean_expr import LeanExpr, HEADER, HEADER_NOBASE
from . import lean_expr as LE
from .arch_unit import ArchUnit

BOUND_KB = 6 * 1024 * 1024
HERE = os.path.dirname(os.path.abspath(__file__))


def check_memory(where):
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > BOUND_KB:
        raise SystemExit("ABORT_MEMORY_LP1: %d kB at %s (bound 6 GB)" % (peak, where))
    return peak


def say(t):
    sys.stdout.write(t + "\n")
    sys.stdout.flush()


def sh(cmd, cwd=None, timeout=3600):
    t0 = time.time()
    p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    return p.returncode, time.time() - t0, p.stdout.decode("utf-8", "replace")


def write_json(path, doc):
    fh = open(path, "w")
    json.dump(doc, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()


# ---------------------------------------------------------------------- #
def cmd_definitions(argv):
    lean_tree, model_source, out = argv
    doc = SailModel.definitions(lean_tree, model_source)
    peak = check_memory("definitions")
    doc["meta"] = {"what": "SailModel.definitions text listing over the emitted Lean tree (third emit); "
                           "strip's simp form is produced by the harness (command handful)",
                   "lean_tree": lean_tree, "peak_resident_kB": peak}
    write_json(out, doc)
    say("  execute clauses: %d" % doc["clause_count"])
    say("  by extension 'of %d':" % doc["clause_count"])
    for e in sorted(doc["clauses_by_extension"]):
        v = doc["clauses_by_extension"][e]
        say("    %-12s %2d  (%s)" % (e, len(v), ", ".join(v)))
    say("  keys (mnem, operand form, width): %d; ten of %d:" % (doc["key_count"], doc["key_count"]))
    for k in doc["keys"][:10]:
        say("    %-8s | %-18s | %d  <- %s" % (k["mnem"], k["operand_form"], k["width"], k["from_clause"]))
    say("  clauses with no key read: %s" % ", ".join(r["clause"] for r in doc["clauses"] if not r["mnem_count"]))
    say("  wrote %s; peak resident %d kB (bound 6 GB, abort ABORT_MEMORY_LP1)" % (out, peak))
    return 0


# ---------------------------------------------------------------------- #
LAKE_LIB = '''
[[lean_lib]]
name = "Leanpath"
srcDir = "leanpath_src"
roots = ["LeanpathAttr", "Leanpath", "LeanpathBase"]
'''


def cmd_tally(argv):
    """python3 -m leanpath tally <out.json> <walk dir>... -- <equals dir>...
    The tallies over any number of walk and equals outputs; a later directory's
    row for a unit replaces an earlier one's (a re-run over the failures)."""
    import collections
    out = argv[0]
    rest = argv[1:]
    cut = rest.index("--") if "--" in rest else len(rest)
    walk_dirs, eq_dirs = rest[:cut], rest[cut + 1:]
    rows = {}
    for d in walk_dirs:
        for r in json.load(open(os.path.join(d, "walk.json")))["rows"]:
            rows[r["unit"]] = r
    rows = list(rows.values())
    eq = {}
    for d in eq_dirs:
        try:
            for r in json.load(open(os.path.join(d, "equals.json")))["rows"]:
                eq[r["unit"]] = r
        except Exception as ex:
            say("  equals %s: %s" % (d, ex))
    eq = list(eq.values())
    T = {"units": len(rows), "verdicts": collections.Counter(r["verdict"] for r in rows).most_common()}
    say("units %d; verdicts %s" % (T["units"], T["verdicts"]))
    why = collections.Counter(re.sub(r"\d+", "N", (r.get("why") or "")[:64]) for r in rows if r["verdict"] == "REFUSED")
    T["refusals"] = why.most_common(20)
    say("refusals:"); [say("  %5d  %s" % (n, w)) for w, n in T["refusals"]]
    lr = lambda r: (r["cell_display"].split("(")[1].rstrip(")") if r.get("cell_display") and "(" in r["cell_display"] else "?")
    by = collections.Counter((lr(r), r["verdict"]) for r in rows)
    T["by_language_route"] = sorted(by.items())
    say("by language/route:"); [say("  %-28s %-10s %d" % (k[0], k[1], n)) for k, n in T["by_language_route"]]
    cells = collections.defaultdict(list)
    for r in rows:
        if r["verdict"] == "CERTIFIED":
            cells[r["cell_display"].split(" (")[0]].append(r["proposal"])
    T["certified_cells"] = {c: (len(v), v[0]) for c, v in sorted(cells.items())}
    say("certified cells %d" % len(cells)); [say("  %-32s %d  %s" % (c, n, p[:100])) for c, (n, p) in T["certified_cells"].items()]
    T["identity_units"] = sorted(r["unit"] for r in rows if r["verdict"] == "CERTIFIED" and r["proposal"].strip("() ") in ("a", "b"))
    say("certified as the identity on the answering register: %d" % len(T["identity_units"]))
    fails = [r for r in rows if r["verdict"] == "FAILED"]
    T["failed"] = [(r["unit"], r["proposal"][:80], (r["errors"] or [""])[0][-100:]) for r in fails]
    say("failed: %d" % len(fails)); [say("  %-60s %s | %s" % (u[:60], p[:50], e[-70:])) for u, p, e in T["failed"][:30]]
    T["equals"] = {"units": len(eq), "with_a_proved_definition": sum(1 for r in eq if r["proved"]),
                   "stages": collections.Counter(p[2] for r in eq for p in r["proved"][:1]).most_common(),
                   "definitions": collections.Counter(p[0] for r in eq for p in r["proved"][:1]).most_common(60),
                   "unproved": [(r["unit"], r["proposal"][:100]) for r in eq if not r["proved"]]}
    say("equals: %d units, %d with a proved definition; stages %s" % (T["equals"]["units"], T["equals"]["with_a_proved_definition"], T["equals"]["stages"]))
    say("definitions proved: %s" % T["equals"]["definitions"])
    say("unproved: %d" % len(T["equals"]["unproved"])); [say("  %-60s %s" % (u[:60], p[:90])) for u, p in T["equals"]["unproved"][:40]]
    cross = collections.Counter()
    for r in eq:
        for p in r["proved"][:1]:
            head = re.findall(r"pure_(\w+)", r["proposal"])
            cross[("same clause" if head and head[0] == p[0] else "another clause", p[2])] += 1
    T["equals"]["proved_by"] = sorted(cross.items())
    say("proved by: %s" % T["equals"]["proved_by"])
    write_json(out, T)
    return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "definitions":
        return cmd_definitions(argv[2:])
    if cmd == "tally":
        return cmd_tally(argv[2:])
    if cmd == "operator_for":                    # Language.operator_for, filled by System.pass_a_find step 2
        from . import operator_for as OF
        return OF.cmd_operator_for(argv[2:], say=say, write_json=write_json)
    if cmd == "render":                          # Language.render: emulations from operator_for and nothing else
        from . import render as RD
        return RD.cmd_render(argv[2:], say=say, write_json=write_json)
    if cmd == "eye_check":                       # System.eye_check: the table read on the handful
        from . import eye_check as EC
        return EC.main(argv[2:])
    if cmd == "probes":                          # Language.compiler_corpus: the probe manifest as walk units
        from . import compiler_corpus as CC
        return CC.cmd_probes(argv[2:], say=say, write_json=write_json)
    if cmd == "walk":
        # ArchUnit.meaning: python3 -m leanpath walk <proof project> <exec project> <lib> <strip.json> <units.json> <out dir>
        from . import walk as WK
        return WK.cmd_walk(argv[2:], say=say, write_json=write_json, check_memory=check_memory)
    if cmd == "kinds":
        # LeanExpr.kinds: python3 -m leanpath kinds <units.json> <walk.json[,...]> <out.json> [LeanIM dir]
        from . import kinds as KD
        return KD.cmd_kinds(argv[2:], say=say, write_json=write_json)
    if cmd == "equals":
        from . import equals as EQ
        return EQ.cmd_equals(argv[2:], say=say, write_json=write_json, check_memory=check_memory)
    if cmd == "strip":
        # SailModel.strip: python3 -m leanpath strip <project> <lib> <out dir> [timeout_s] [clause ...]
        from . import strip as ST
        project, lib, out = argv[2], argv[3], argv[4]
        timeout_s = int(argv[5]) if len(argv) > 5 else 900
        only = set(argv[6:]) or None
        doc = ST.run(project, lib, out, timeout_s=timeout_s, only=only)
        doc["summary"]["driver_peak_resident_kB"] = check_memory("strip end")
        write_json(os.path.join(out, "strip.json"), doc)
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
