#!/usr/bin/env bash
# t87 lane 1 — SURVEY ONLY, nothing is written into the tree.
#
# What this lane has to settle before any code is written:
#   * that the instance is running the current image and the analysis
#     packages import (log_190 section 3.3: a rebuilt image does not
#     reach an already-created instance, and nothing warns);
#   * which MACHINE-FORM fields a unit record actually carries, per
#     language, so the third connection kind's variant identity can be
#     derived from machine-form evidence and from unit identity ONLY;
#   * how many distinct variants each candidate identity yields over
#     each population, so the identity is chosen against measured
#     numbers rather than a guess;
#   * whether the 2,600 regenerated diaries have unit records on disk
#     at all, and where;
#   * the peak resident set of simply LOADING each graph, which is the
#     fixed cost every later pass carries.
#
# THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
# second violation). No operator token may appear in ANY key, grouping,
# pairing, row structure, candidate selection, or comparison scope,
# anywhere in this line -- not in matching, not in "which pairs get
# compared", not in report rows, not in dropdowns. The candidate set for
# comparison comes from machine-form evidence (clusters, connections,
# type pairs) or from ratified intention -- never from the token. The
# token appears exactly once per unit: as a display label on the member.
# MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
# units must run op_pipeline/check_no_spelling_keys.py and refuse its
# own output on failure.
#
# This lane counts variants under candidate identities. NO IDENTITY
# TRIED HERE READS THE OPERATOR FIELD. The `operator` field is printed
# once, per single unit, only where a unit is shown whole.
set -u
say() { echo; echo "======== $* ========"; }
REPO=/projects/PseudoCoupHQ/Research/compiler_graph
PIPE=/projects/PseudoCoupHQ/Research/op_pipeline
cd "$REPO"

say "[1/7] the image, and that the analysis packages import"
python3 - <<'PY'
import sys
print("   python", sys.version.split()[0])
for name in ("pyvex", "archinfo", "z3", "capstone", "elftools", "tree_sitter"):
    try:
        mod = __import__(name)
        print("   import %-12s OK  %s" % (name, getattr(mod, "__version__", "-")))
    except Exception as problem:
        print("   import %-12s FAILED  %s" % (name, problem))
PY

say "[2/7] the diary populations on disk, counted here"
for d in go c cpp c_and_cpp regen extended; do
  printf "   diaries/%-10s %s files\n" "$d" "$(ls diaries/$d/*.txt 2>/dev/null | wc -l)"
done

say "[3/7] one unit record whole, per language -- what fields exist"
python3 - <<'PY'
import json
for lang in ("go", "c", "cpp"):
    doc = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/'
                         'canon39_wrapped_%s.json' % lang))
    units = doc["units"]
    print("   %-4s units in canon39_wrapped_%s.json : %d" % (lang, lang, len(units)))
    first = units[sorted(units)[0]]
    print("      fields: %s" % ", ".join(sorted(first)))
PY

say "[4/7] the machine-form fields of ONE unit, shown whole"
python3 - <<'PY'
import json
doc = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/'
                     'canon39_wrapped_cpp.json'))
unit = doc["units"]["cpp/op_0"]
for field in ("lang", "n", "operator", "population", "outcome",
              "body_text", "body_bytes", "entry_contract",
              "arrival_families", "out_row", "ledger_entries",
              "ledger_block_bytes", "branch_kind"):
    print("   %-22s %s" % (field, json.dumps(unit.get(field))[:220]))
print("   ledger rows: %d" % len(unit.get("ledger") or []))
print("   ledger produced_by kinds: %s"
      % [row.get("produced_by", {}).get("kind") for row in unit.get("ledger") or []])
PY

say "[5/7] candidate variant identities, COUNTED -- none reads the operator"
python3 - <<'PY'
import hashlib, json
def digest(payload):
    return hashlib.sha256(json.dumps(payload, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()[:12]
IDS = {
  "A body_bytes alone":
      lambda u: [u.get("body_bytes")],
  "B body_text alone":
      lambda u: [u.get("body_text")],
  "C body_text + entry_contract":
      lambda u: [u.get("body_text"), u.get("entry_contract")],
  "D body_text + entry_contract + ledger produced_by shape":
      lambda u: [u.get("body_text"), u.get("entry_contract"),
                 [(r.get("block"), r.get("size"), r.get("type"),
                   r.get("produced_by", {}).get("kind"))
                  for r in (u.get("ledger") or [])]],
  "E ledger produced_by shape alone":
      lambda u: [[(r.get("block"), r.get("size"), r.get("type"),
                   r.get("produced_by", {}).get("kind"))
                  for r in (u.get("ledger") or [])]],
}
for lang in ("go", "c", "cpp"):
    doc = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/'
                         'canon39_wrapped_%s.json' % lang))
    units = doc["units"]
    print("   --- %s, population %d units" % (lang, len(units)))
    for name in sorted(IDS):
        seen = {}
        for uid in sorted(units):
            seen.setdefault(digest(IDS[name](units[uid])), []).append(uid)
        sizes = sorted((len(v) for v in seen.values()), reverse=True)
        singles = sum(1 for s in sizes if s == 1)
        print("      %-52s %5d variants   largest %4d   singletons %5d"
              % (name, len(seen), sizes[0], singles))
# and the two clang languages together, since they share one compiler
docs = {}
for lang in ("c", "cpp"):
    docs.update(json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/'
                              'canon39_wrapped_%s.json' % lang))["units"])
print("   --- c and cpp jointly, population %d units" % len(docs))
for name in sorted(IDS):
    seen = {}
    for uid in sorted(docs):
        seen.setdefault(digest(IDS[name](docs[uid])), []).append(uid)
    sizes = sorted((len(v) for v in seen.values()), reverse=True)
    spanning = sum(1 for v in seen.values()
                   if len({u.split('/')[0] for u in v}) > 1)
    print("      %-52s %5d variants   largest %4d   spanning both %4d"
          % (name, len(seen), sizes[0], spanning))
PY

say "[6/7] do the diary probe names join to unit ids, and what about regen"
python3 - <<'PY'
import json, os
def stems(d):
    p = '/projects/PseudoCoupHQ/Research/compiler_graph/diaries/' + d
    return sorted(n[:-4] for n in os.listdir(p) if n.endswith('.txt'))
for lang, folder in (("go", "go"), ("c", "c"), ("cpp", "cpp")):
    doc = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/'
                         'canon39_wrapped_%s.json' % lang))
    units = doc["units"]
    names = stems(folder)
    hit = sum(1 for n in names if ("%s/%s" % (lang, n)) in units)
    print("   diaries/%-4s %4d files, %4d join to canon39_wrapped_%s.json units"
          % (folder, len(names), hit, lang))
regen = stems('regen')
print("   diaries/regen %d files; first five stems: %s" % (len(regen), regen[:5]))
store = '/projects/PseudoCoupHQ/Research/op_pipeline/canon39_regen_store'
listing = sorted(os.listdir(store))
print("   canon39_regen_store: %d entries; first five: %s"
      % (len(listing), listing[:5]))
state = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/'
                       'canon39_regen_state.json'))
print("   canon39_regen_state.json top-level: %s" % sorted(state)[:20])
PY

say "[7/7] the fixed cost: peak resident of LOADING each graph"
for g in graph_go.json graph_cpp.json; do
  python3 - "$g" <<'PY'
import json, resource, sys, time
path = sys.argv[1]
started = time.time()
payload = json.loads(open('/projects/PseudoCoupHQ/Research/compiler_graph/'
                          + path).read())
defs = sum(1 for r in payload["nodes"] if r.get("kind") == "def")
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
print("   %-16s nodes %8d  defs %7d  edges %8d   PEAK RESIDENT %8.1f MB  wall %5.1f s"
      % (path, len(payload["nodes"]), defs, len(payload["edges"]), peak,
         time.time() - started))
PY
done
free -m | head -2
echo "DONE t87_l1"
