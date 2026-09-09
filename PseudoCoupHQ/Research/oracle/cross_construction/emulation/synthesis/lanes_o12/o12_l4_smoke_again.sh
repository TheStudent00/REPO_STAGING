#!/usr/bin/env bash
# o12 lane 4 -- the same three targets again, after two corrections:
# the root no longer demands the DWARF result holder match (one bucket
# is one answer width, and the holder table's own rows carry
# `DW_AT_encoding_absent`), and a component whose z3 reprint differs
# only in the order of a commutative operator's arguments is now
# rebuilt rather than refused.
set -u
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/synthesis
echo "[1/1] smoke again, three targets"
python3 - <<'PY'
import resource, subprocess, sys
r = subprocess.run([sys.executable, "synthesize.py", "sample", "3"])
print("PEAK_RSS_KB(children)=%d"
      % resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
sys.exit(r.returncode)
PY
echo "-- exit $?"
echo
echo "-- the three records"
python3 - <<'PY'
import json
d = json.load(open("synthesis_sample.json"))
for record in d["results"]:
    print(record["entry_id"], record.get("outcome"),
          "library", record.get("library_size"), "->",
          record.get("library_rebuilt"),
          "wire-capable", record.get("library_wire_capable"),
          "commutative-order", record.get("library_rebuilt_up_to_commutative_order"))
    print("   rounds", record.get("rounds"),
          "counterexamples", len(record.get("counterexamples") or []),
          "wall", record.get("wall_seconds"))
    print("   composition", (record.get("composition") or {}).get("expression"))
PY
