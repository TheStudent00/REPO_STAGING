#!/bin/bash
# lp2_l1_exec_decoder_only.sh -- the evaluable variant with ONLY the two
# decoders computable: every other giant of the instructions module
# (encdec_*_matches, encdec_*forwards*, assembly_*, execute, step, the
# emulator loop and main) is marked noncomputable by name at emit time, so
# the code generator compiles 30k lines instead of 72k. Same modules as
# lane 22 (all leaves but V_instructions, Zvabd_insts). Products under
# /work (this instance's own scratch; lp1's volume is read-only here).
set -uo pipefail
total=4
export OPAMROOT=/persist/opam
export ELAN_HOME=/persist/lp1/elan
export PATH=/persist/opam/default/bin:$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
SRC=/persist/sail-riscv-6266b40c
CFG=$SRC/build/config/rv64d_v256_e64.json
P=/persist/lp1/Lean_IM_6266b40c_all
X=/work/Lean_IM_dec_exec
echo "[1/$total] the modules (as lane 22) and the emit with the giants noncomputable"
cd $SRC/model
MODS=$(python3 - <<'PY'
import re
t=open("riscv.sail_project").read(); names=[]; stack=[]
for ln in t.split("\n"):
    m=re.match(r"^\s*([A-Za-z_0-9]+)\s*\{\s*$", ln)
    if m: stack.append([m.group(1), False]); continue
    if re.match(r"^\s*files\b", ln) and stack: stack[-1][1]=True
    if re.match(r"^\s*\}\s*$", ln) and stack:
        n,leaf=stack.pop()
        if leaf: names.append(n)
print(" ".join(n for n in names if n not in {"V_instructions","Zvabd_insts"}))
PY
)
NC=""; for f in encdec_backwards_matches encdec_compressed_backwards_matches encdec_forwards encdec_forwards_matches encdec_compressed_forwards encdec_compressed_forwards_matches assembly_forwards assembly_backwards assembly_forwards_matches assembly_backwards_matches execute step loop fetch sail_main main; do NC="$NC --lean-noncomputable-function $f"; done
OUT=/work/emit_dec; rm -rf $OUT /work/smtcache5; mkdir -p $OUT
start=$(date +%s)
sail --strict-var --strict-bitvector --strict-exponentials --memo-z3-path /work/smtcache5 \
  --config $CFG --lean --memo-z3 --lean-output-dir $OUT --lean-force-output \
  --lean-non-beq-type instruction --lean-non-beq-type ExecutionResult --lean-non-beq-type Step \
  $NC --lean-import-file ../handwritten_support/RiscvExtrasExecutable.lean -o Lean_IM_dec_executable \
  $MODS riscv.sail_project > /work/emit_dec.log 2>&1
rc=$?; echo "  emit rc=$rc seconds=$(( $(date +%s) - start ))"
[ $rc -eq 0 ] || { echo "FLAG: the emit failed"; tail -12 /work/emit_dec.log; exit 3; }
D=$(ls -d $OUT/Lean_IM_dec_executable/Lean*/ | head -1)
echo "  noncomputable marks in InstsEnd: $(grep -c '^noncomputable def' $D/InstsEnd.lean); computable decoders: $(grep -cE '^def encdec_(compressed_)?backwards ' $D/InstsEnd.lean)"
echo "[2/$total] build under /work"
rm -rf $X; cp -a $OUT/Lean_IM_dec_executable $X; mkdir -p $X/.lake
cp -a $P/.lake/packages $X/.lake/ && cp $P/lake-manifest.json $X/ && echo "  packages and manifest copied from the proof build"
cd $X; start=$(date +%s); lake build > /work/lake_dec.log 2>&1; rc=$?
echo "  lake rc=$rc seconds=$(( $(date +%s) - start ))"; grep -cE '^error' /work/lake_dec.log | sed 's/^/  error lines: /'; grep -E 'Build completed|error:' /work/lake_dec.log | head -6 | cut -c1-200
[ $rc -eq 0 ] || { echo "FLAG: the build fails"; exit 3; }
echo "[3/$total] the decoder on the initialised state, four words, LITERAL"
XLIB=$(grep -A1 '\[\[lean_lib\]\]' $X/lakefile.toml | grep -oE 'name = "[^"]+"' | cut -d'"' -f2)
cat > /work/Probe5.lean <<L
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
timeout 900 lake env lean /work/Probe5.lean 2>&1 | cut -c1-240 | head -10
echo "[4/$total] can lake env lean run in the read-only proof project? one trivial file"
cd $P && echo 'import LeanIM
#check LeanIM.Functions.execute_DIV' > /work/T.lean && timeout 600 lake env lean /work/T.lean 2>&1 | head -4 | cut -c1-200
echo done
