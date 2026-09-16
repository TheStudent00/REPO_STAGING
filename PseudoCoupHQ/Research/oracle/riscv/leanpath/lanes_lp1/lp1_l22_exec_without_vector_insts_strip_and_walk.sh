#!/bin/bash
# lp1_l22_exec_without_vector_insts_strip_and_walk.sh -- lane 21 spent over an
# hour compiling the whole model's executable instructions module (CI does
# the same build in 6.5 min; the vector extension's clauses are the bulk,
# and the code generator is superlinear on them). Every `currentlyEnabled`
# clause lives OUTSIDE the vector instruction module (measured over the
# model source), so the evaluable variant drops V_instructions and
# Zvabd_insts only, and the decoder keeps every arm. The proof side stays
# the whole model. Then the strip over the whole model and the walk.
set -uo pipefail
total=6
export OPAMROOT=/persist/opam
export ELAN_HOME=/persist/lp1/elan
export PATH=/persist/opam/default/bin:$ELAN_HOME/bin:/opt/elan/bin:$PATH
SRC=/persist/sail-riscv-6266b40c
CFG=$SRC/build/config/rv64d_v256_e64.json
P=/persist/lp1/Lean_IM_6266b40c_all
X=/persist/lp1/Lean_IM_novi_exec
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
echo "[1/$total] the leaf modules of the project file, minus the vector instruction modules"
cd $SRC/model
MODS=$(python3 - <<'PY'
import re
t=open("riscv.sail_project").read()
# a leaf module is a block that directly holds a `files` entry
names=[]; stack=[]
for ln in t.split("\n"):
    m=re.match(r"^\s*([A-Za-z_0-9]+)\s*\{\s*$", ln)
    if m: stack.append([m.group(1), False]); continue
    if re.match(r"^\s*files\b", ln) and stack: stack[-1][1]=True
    if re.match(r"^\s*\}\s*$", ln) and stack:
        n,leaf=stack.pop()
        if leaf: names.append(n)
drop={"V_instructions","Zvabd_insts"}
print(" ".join(n for n in names if n not in drop))
PY
)
echo "  modules ($(echo $MODS | wc -w)): $MODS"
sail --config $CFG --list-files $MODS riscv.sail_project 2>&1 | tr ' ' '\n' | grep -v '^$' > /work/files_novi.txt
echo "  files resolved: $(wc -l < /work/files_novi.txt); vector insts excluded: $(grep -c 'vext_insts\|zvabd' /work/files_novi.txt) present"
[ "$(wc -l < /work/files_novi.txt)" -gt 100 ] || { echo "FLAG: the selection did not resolve"; head -5 /work/files_novi.txt; exit 3; }
echo "[2/$total] the executable emit over that selection"
OUT=/work/emit_novi; rm -rf $OUT /work/smtcache4; mkdir -p $OUT
start=$(date +%s)
sail --strict-var --strict-bitvector --strict-exponentials --memo-z3-path /work/smtcache4 \
  --config $CFG --lean --memo-z3 --lean-output-dir $OUT --lean-force-output \
  --lean-non-beq-type instruction --lean-non-beq-type ExecutionResult --lean-non-beq-type Step \
  --lean-import-file ../handwritten_support/RiscvExtrasExecutable.lean -o Lean_IM_novi_executable \
  $MODS riscv.sail_project > /work/emit_novi.log 2>&1
rc=$?; echo "  emit rc=$rc seconds=$(( $(date +%s) - start ))"
[ $rc -eq 0 ] || { echo "FLAG: the executable emit failed"; tail -12 /work/emit_novi.log; exit 3; }
echo "  Lean files: $(find $OUT -name '*.lean' | wc -l); lines: $(find $OUT -name '*.lean' | xargs cat | wc -l)"
echo "[3/$total] build it in /persist"
rm -rf $X; cp -a $OUT/Lean_IM_novi_executable $X; mkdir -p $X/.lake
cp -a $P/.lake/packages $X/.lake/ && cp $P/lake-manifest.json $X/ && echo "  packages and manifest copied from the proof build"
cd $X; start=$(date +%s); lake build > /work/lake_novi.log 2>&1; rc=$?
echo "  lake rc=$rc seconds=$(( $(date +%s) - start ))"; grep -cE '^error' /work/lake_novi.log | sed 's/^/  error lines: /'; grep -E 'Build completed|error:' /work/lake_novi.log | head -5 | cut -c1-200
[ $rc -eq 0 ] || { echo "FLAG: the executable build fails"; exit 3; }
echo "[4/$total] the decoder on the initialised state, four words, LITERAL"
XLIB=$(grep -A1 '\[\[lean_lib\]\]' $X/lakefile.toml | grep -oE 'name = "[^"]+"' | cut -d'"' -f2)
cat > /work/Probe4.lean <<L
import $XLIB
open Sail Sail.ConcurrencyInterfaceV1 PreSail $XLIB $XLIB.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
def blank : SequentialState RegisterType trivialChoiceSource :=
  { regs := ∅, choiceState := (), mem := ∅, tags := (), cycleCount := 0, sailOutput := #[] }
def s0r := (do sail_model_init (); init_model "") blank
#eval IO.println ("init: " ++ (match s0r with | .ok _ s => s!"ok, regs {s.regs.size}" | .error e s => s!"ERROR {e.print} (regs {s.regs.size})"))
def s0 : SequentialState RegisterType trivialChoiceSource := match s0r with | .ok _ s => s | .error _ s => s
#eval IO.println ("c.add:   " ++ (match (encdec_compressed_backwards (0x952e#16)) s0 with | .ok i _ => toString (repr i) | .error e _ => "ERROR " ++ e.print))
#eval IO.println ("divw:    " ++ (match (encdec_backwards (0x02b5453b#32)) s0 with | .ok i _ => toString (repr i) | .error e _ => "ERROR " ++ e.print))
#eval IO.println ("mulh:    " ++ (match (encdec_backwards (0x02b54533#32)) s0 with | .ok i _ => toString (repr i) | .error e _ => "ERROR " ++ e.print))
#eval IO.println ("c.jr ra: " ++ (match (encdec_compressed_backwards (0x8082#16)) s0 with | .ok i _ => toString (repr i) | .error e _ => "ERROR " ++ e.print))
L
timeout 900 lake env lean /work/Probe4.lean 2>&1 | cut -c1-240 | head -10
echo "[5/$total] strip over every clause of the whole-model proof emit"
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | cut -d'"' -f2)
cd $A; start=$(date +%s)
python3 -m leanpath strip $P $PLIB $A/strip_6266b40c_8eb1fb6b_all 900 2>&1 | tail -4
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[6/$total] the walk on the handful"
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
