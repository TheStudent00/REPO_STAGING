#!/bin/bash
# lp1_l21_all_modules_exec_strip_and_walk.sh -- the whole model, because a
# module SUBSET leaves Sail's scattered `currentlyEnabled` without arms for
# the absent extensions, and the decoder, probing them, throws (lane 20:
# "Pattern match failure at extensions/C/zcb_insts.sail:9"). The green pair
# builds all modules. Steps: finish the third launch's all-modules PROOF
# build; emit and build the all-modules EXECUTABLE variant; strip over every
# clause; the walk on the handful. Fetches nothing unless lake insists.
set -uo pipefail
total=6
export OPAMROOT=/persist/opam
export ELAN_HOME=/persist/lp1/elan
export PATH=/persist/opam/default/bin:$ELAN_HOME/bin:/opt/elan/bin:$PATH
SRC=/persist/sail-riscv-6266b40c
CFG=$SRC/build/config/rv64d_v256_e64.json
P=/persist/lp1/Lean_IM_6266b40c_all
X=/persist/lp1/Lean_IM_all_exec
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
echo "[1/$total] the proof build of the all-modules emit (incremental)"
cd $P; cat lean-toolchain; start=$(date +%s); lake build > /work/lake_all.log 2>&1; rc=$?
echo "  lake rc=$rc seconds=$(( $(date +%s) - start ))"; grep -cE '^error' /work/lake_all.log | sed 's/^/  error lines: /'; grep -E 'Build completed|error:' /work/lake_all.log | head -5 | cut -c1-200
[ $rc -eq 0 ] || { echo "FLAG: the all-modules proof build fails"; exit 3; }
echo "[2/$total] the all-modules executable emit"
OUT=/work/emit_all_exec; rm -rf $OUT /work/smtcache3; mkdir -p $OUT; cd $SRC/model
start=$(date +%s)
sail --strict-var --strict-bitvector --strict-exponentials --memo-z3-path /work/smtcache3 \
  --config $CFG --lean --memo-z3 --lean-output-dir $OUT --lean-force-output \
  --lean-non-beq-type instruction --lean-non-beq-type ExecutionResult --lean-non-beq-type Step \
  --lean-import-file ../handwritten_support/RiscvExtrasExecutable.lean -o Lean_IM_all_executable \
  --all-modules riscv.sail_project > /work/emit_all_exec.log 2>&1
rc=$?; echo "  emit rc=$rc seconds=$(( $(date +%s) - start ))"
[ $rc -eq 0 ] || { echo "FLAG: the executable emit failed"; tail -12 /work/emit_all_exec.log; exit 3; }
echo "  Lean files: $(find $OUT -name '*.lean' | wc -l)"
echo "[3/$total] build the executable variant in /persist"
rm -rf $X; cp -a $OUT/Lean_IM_all_executable $X; mkdir -p $X/.lake
cp -a $P/.lake/packages $X/.lake/ && cp $P/lake-manifest.json $X/ && echo "  packages and manifest copied from the proof build"
cd $X; start=$(date +%s); lake build > /work/lake_all_exec.log 2>&1; rc=$?
echo "  lake rc=$rc seconds=$(( $(date +%s) - start ))"; grep -cE '^error' /work/lake_all_exec.log | sed 's/^/  error lines: /'; grep -E 'Build completed|error:' /work/lake_all_exec.log | head -5 | cut -c1-200
grep -qiE 'fetch|clon|download' /work/lake_all_exec.log && { echo "  FETCHED during lake build (LITERAL):"; grep -iE 'fetch|clon|download' /work/lake_all_exec.log | head -3; }
[ $rc -eq 0 ] || { echo "FLAG: the executable build fails"; exit 3; }
echo "[4/$total] the decoder on the initialised state, three words, LITERAL"
XLIB=$(grep -A1 '\[\[lean_lib\]\]' $X/lakefile.toml | grep -oE 'name = "[^"]+"' | cut -d'"' -f2)
cat > /work/Probe3.lean <<L
import $XLIB
open Sail Sail.ConcurrencyInterfaceV1 PreSail $XLIB $XLIB.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
def blank : SequentialState RegisterType trivialChoiceSource :=
  { regs := ∅, choiceState := (), mem := ∅, tags := (), cycleCount := 0, sailOutput := #[] }
def s0r := (do sail_model_init (); init_model "") blank
#eval IO.println ("init: " ++ (match s0r with | .ok _ s => s!"ok, regs {s.regs.size}" | .error e s => s!"ERROR {e.print} (regs {s.regs.size})"))
def s0 : SequentialState RegisterType trivialChoiceSource := match s0r with | .ok _ s => s | .error _ s => s
#eval IO.println ("c.add:  " ++ (match (encdec_compressed_backwards (0x952e#16)) s0 with | .ok i _ => toString (repr i) | .error e _ => "ERROR " ++ e.print))
#eval IO.println ("divw:   " ++ (match (encdec_backwards (0x02b5453b#32)) s0 with | .ok i _ => toString (repr i) | .error e _ => "ERROR " ++ e.print))
#eval IO.println ("mulh:   " ++ (match (encdec_backwards (0x02b54533#32)) s0 with | .ok i _ => toString (repr i) | .error e _ => "ERROR " ++ e.print))
#eval IO.println ("c.jr ra:" ++ (match (encdec_compressed_backwards (0x8082#16)) s0 with | .ok i _ => toString (repr i) | .error e _ => "ERROR " ++ e.print))
L
timeout 900 lake env lean /work/Probe3.lean 2>&1 | cut -c1-240 | head -10
echo "[5/$total] strip over every clause of the all-modules proof emit"
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | cut -d'"' -f2)
cd $A; start=$(date +%s)
python3 -m leanpath strip $P $PLIB $A/strip_6266b40c_8eb1fb6b_all 900 2>&1 | tail -6
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[6/$total] the walk on the handful, over the all-modules pair"
start=$(date +%s)
python3 -u -m leanpath walk $P $X $PLIB $A/strip_6266b40c_8eb1fb6b_all/strip.json $A/handful_units.json $A/walk_handful_all 900 2>&1 | tail -80
echo "  wall seconds=$(( $(date +%s) - start ))"
f=$(python3 - <<'PY'
import json
d=json.load(open("PseudoCoupHQ/Research/oracle/riscv/leanpath/walk_handful_all/walk.json"))
c=[r for r in d["rows"] if r.get("verdict")=="CERTIFIED"]; a=[r for r in d["rows"] if r.get("lean_file")]
print((c or a)[0]["lean_file"] if (c or a) else "")
PY
); [ -n "$f" ] && { echo "--- $f"; grep -n "theorem meaning_" -A4 "$f" | cut -c1-220; }
echo done
