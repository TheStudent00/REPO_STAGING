#!/usr/bin/env bash
# ex1_l11_the_two_float_cells_and_the_jit.sh -- task ex1: two readings
# the tables do not make on their own.
#
# [A] THE TWO FLOAT CELLS.  Every interpreted run of them is refused
# `vector arrival used beyond its low lane`, and the SAME two cells
# render, compile, carve and prove on cpp in this task's own loop.  The
# two routes are handed the cell by the same function, so the
# difference is in the CELL and not in the target: this section prints
# the row each cells file chooses for the two triples, with its places,
# its families and its term, so the reason is on the record rather
# than guessed at.
#
# [B] THE JIT OUTPUT the corpus holds.  The brief says: where the
# language has a JIT whose output the corpus already carves, ALSO carve
# and gate that output the compiled way.  This section asks what
# `Research/op_pipeline/jit_out_*` actually holds and in what shape,
# and what the remaining_languages node records as being on disk, so
# the answer is measured rather than assumed.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful

echo "[1/3] the two float cells, out of each cells file"
python3 - <<'PYEOF'
import os
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")
sys.path.insert(0, "../../../../op_pipeline")

import handful as H

H.use_task_ex1()
FILES = {
    "the handful's own cells file (handful_cells.json)":
        os.path.join(H.HERE, "handful_cells.json"),
    "the 253-cell outer set (expand1_cells.json)":
        os.path.join(H.HERE, "..", "autopoly", "expand1_cells.json"),
}
WANTED = [("addss", "xmm_xmm", 32), ("cvtsi2sd", "gpr_xmm", 64)]
for label in sorted(FILES):
    path = FILES[label]
    if not os.path.exists(path):
        print("== %s: absent at %s" % (label, path))
        continue
    cells = H.read_json(path)
    print("")
    print("== %s" % label)
    for asked in WANTED:
        held = H.cell_input(cells, asked)
        print("   -- `%s` %s %s   row %s   line %r"
              % (asked[0], asked[1], asked[2], held.get("row_id"),
                 held.get("line")))
        if held.get("refusal_cause") is not None:
            print("      REFUSED at the input: %s"
                  % held["refusal_cause"])
            continue
        for place in held["places"]:
            print("      place %-14s bits %-4s families %s"
                  % (place["writes"], place["bits"],
                     place.get("families")))
            text = place["text"]
            if len(text) > 150:
                text = text[:147] + "..."
            print("         term, LITERAL: %s" % text)
PYEOF

echo ""
echo "[2/3] what the corpus's JIT output actually is"
for d in PseudoCoupHQ/Research/op_pipeline/jit_out_*; do
    echo "--- $d"
    echo "    files: $(ls "$d" | wc -l)"
    ls "$d" | head -4 | sed 's/^/      /'
done
echo ""
echo "--- the first instruction lines of each dump, LITERAL:"
for f in PseudoCoupHQ/Research/op_pipeline/jit_out_csharp/all_opt.txt \
         PseudoCoupHQ/Research/op_pipeline/jit_out_dart/all_opt.txt \
         PseudoCoupHQ/Research/op_pipeline/jit_out_javascript/probe_0_opt.txt; do
    echo "  == $f"
    sed -n '1,3p' "$f" | sed 's/^/     /'
done
echo ""
echo "--- what an OBJDUMP line looks like, which is what the carve reads:"
echo '     0:	8d 04 37             	lea    (%rdi,%rsi,1),%eax'

echo ""
echo "[3/3] what the corpus holds as ARCH-UNITS for those three languages"
python3 - <<'PYEOF'
import json
path = ("PseudoCoupHQ/Research/oracle/arch_opcodes/"
        "single_opcode_units.json")
document = json.load(open(path))
groups = document["single_opcode_groups"]
print("   languages `single_opcode_units.json` holds groups for: %s"
      % ", ".join(sorted(groups.keys())))
for language in ("javascript", "dart", "csharp", "java", "cpython",
                 "php", "ruby"):
    held = groups.get(language)
    if held is None:
        print("   %-12s ABSENT from the file entirely" % language)
        continue
    print("   %-12s narrow groups %d" % (language,
                                         len(held.get("narrow", {}))))
PYEOF
echo "done"
