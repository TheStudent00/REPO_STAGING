#!/bin/bash
# ap6_l1_preflight_and_the_gate_count.sh -- task ap6, lane 1.
#
# WHAT THIS LANE DOES: measures the gates before and after, checks that
# the closed tasks' own commands still answer through the frozen copy of
# the driver, prints the code version the certificates will carry, and
# takes THE MEMORY SAMPLE the law asks for.
#
# THE GATE COUNT is `check_no_task_gates.py`, which parses the file and
# reports every branch whose condition compares against a task label or
# an arch mnemonic.  `handful_frozen.py` is `handful.py` as it stood on
# 2026-09-10 before the gates were stripped, so the two runs of the same
# checker over the two files are the before and the after.
#
# MEMORY: bound 6 GB resident on the one collecting process, named abort
# ABORT_MEMORY_AP6, checked after every store.  Nothing here forks.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_ap6_brief.md
set -u

E=PseudoCoupHQ/Research/oracle/cross_construction/emulation
A=$E/autopoly
H=$E/handful
TOTAL=7

echo "[1/$TOTAL] every file this task changed compiles"
for f in "$H/handful.py" "$H/handful_frozen.py" "$A/autopoly.py" \
         "$A/autopoly1.py" "$A/autopoly5.py" "$A/bank.py" \
         "$E/check_no_task_gates.py" ; do
    python3 -m py_compile "$f" && echo "  $(basename $f) compiles"
done
echo

echo "[2/$TOTAL] THE GATES BEFORE: the driver as it stood this morning"
python3 "$E/check_no_task_gates.py" "$A/autopoly5_cells.json" \
    "$H/handful_frozen.py" > /tmp/ap6_l1_before.txt
tail -6 /tmp/ap6_l1_before.txt
echo
echo "  the task ENTRIES it carried, one per gate:"
grep -c '^def use_task_' "$H/handful_frozen.py"
grep -n '^def use_task_' "$H/handful_frozen.py"
echo

echo "[3/$TOTAL] THE GATES AFTER: the one driver, and the loop over it"
python3 "$E/check_no_task_gates.py" "$A/autopoly5_cells.json" \
    "$H/handful.py" "$A/autopoly.py" "$A/bank.py"
echo
echo "  task entries left in the driver:"
grep -c '^def use_task_' "$H/handful.py" || true
echo

echo "[4/$TOTAL] the frozen copy is the pre-strip file, byte for byte"
git -C PseudoCoupHQ log --oneline -1 2>/dev/null || true
sha256sum "$H/handful.py" "$H/handful_frozen.py"
echo

echo "[5/$TOTAL] a closed task's own command still answers, through the"
echo "          frozen copy the closed pass driver now names"
python3 "$H/handful_frozen.py" tally2
echo
python3 "$A/autopoly.py" preflight > /tmp/ap6_l1_ap1.txt
head -4 /tmp/ap6_l1_ap1.txt
echo

echo "[6/$TOTAL] THE CODE VERSION every certificate of this pass carries"
python3 - "$H" "$A" <<'PY'
import sys, os
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2])
import handful as H
import autopoly as AP
for lang in ["c", "cpp", "rust", "go", "swift"]:
    version = AP.code_version_of(lang)
    print("  %-6s driver %s  loop %s  renderer %s (%s)"
          % (lang, version["driver"][:12], version["loop"][:12],
             version["renderer"][:12], version["renderer_source"]))
PY
echo

echo "[7/$TOTAL] THE MEMORY SAMPLE: the first 20 runs of every store"
python3 "$A/bank.py" sample 20
echo
echo "lane done"
