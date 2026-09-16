#!/bin/bash
# lp3_l3_root_main_then_strip_and_walk.sh -- the pruned evaluable build
# reached 103 of 104 modules; the root file's generated `main` calls the
# emulator loop the closure marked noncomputable, and the emit's flag does
# not reach that `main`. The build copy's root `main` is marked
# noncomputable here (a build step on a build product, no definition
# touched), the root module rebuilt, the decoder probed on the state the
# model's own init gives; then the proof project is copied to writable
# scratch, the strip runs over the whole model, and the walk over the
# handful. Fetches nothing.
set -uo pipefail
total=6
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath
XLIB=$(grep -A1 '\[\[lean_lib\]\]' $X/lakefile.toml | grep -oE 'name = "[^"]+"' | cut -d'"' -f2)
echo "[1/$total] the instructions module's own compile time, from the build log, LITERAL"
grep -E "Built $XLIB\.(InstsEnd|ZicsrInsts|Model|Main) " /work/lake_pr.log | cut -c1-100
echo "[2/$total] the root file's main, marked noncomputable in the build copy; rebuild"
cd $X; grep -n "^def main " $XLIB.lean | head -2
sed -i 's/^def main (/noncomputable def main (/' $XLIB.lean
start=$(date +%s); lake build > /work/lake_pr2.log 2>&1; rc=$?
echo "  lake rc=$rc seconds=$(( $(date +%s) - start ))"; grep -E 'Build completed|error:' /work/lake_pr2.log | head -4 | cut -c1-200
[ $rc -eq 0 ] || { echo "FLAG: the build still fails"; exit 3; }
echo "[3/$total] init and the decoder on the initialised state, LITERAL"
cat > /work/Probe9.lean <<L
import $XLIB
open Sail Sail.ConcurrencyInterfaceV1 PreSail $XLIB $XLIB.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
def blank : SequentialState RegisterType trivialChoiceSource :=
  { regs := ∅, choiceState := (), mem := ∅, tags := (), cycleCount := 0, sailOutput := #[] }
def s0r := (do sail_model_init (); init_model "") blank
#eval IO.println ("init: " ++ (match s0r with | .ok _ s => s!"ok, regs {s.regs.size}" | .error e s => s!"ERROR {e.print} (regs {s.regs.size})"))
def s0 : SequentialState RegisterType trivialChoiceSource := match s0r with | .ok _ s => s | .error _ s => s
#eval IO.println ("misa: " ++ (match s0.regs.get? .misa with | some v => toString (repr v) | none => "absent"))
#eval IO.println ("c.add:   " ++ (match (encdec_compressed_backwards (0x952e#16)) s0 with | .ok i _ => toString (repr i) | .error e _ => "ERROR " ++ e.print))
#eval IO.println ("divw:    " ++ (match (encdec_backwards (0x02b5453b#32)) s0 with | .ok i _ => toString (repr i) | .error e _ => "ERROR " ++ e.print))
#eval IO.println ("mulh:    " ++ (match (encdec_backwards (0x02b54533#32)) s0 with | .ok i _ => toString (repr i) | .error e _ => "ERROR " ++ e.print))
#eval IO.println ("c.jr ra: " ++ (match (encdec_compressed_backwards (0x8082#16)) s0 with | .ok i _ => toString (repr i) | .error e _ => "ERROR " ++ e.print))
#eval IO.println ("fcvt.s.w:" ++ (match (encdec_backwards (0xd00577d3#32)) s0 with | .ok i _ => toString (repr i) | .error e _ => "ERROR " ++ e.print))
L
timeout 900 lake env lean /work/Probe9.lean 2>&1 | cut -c1-240 | head -10
grep -q "divw:    .*instruction\." <(timeout 900 lake env lean /work/Probe9.lean 2>&1) || { echo "FLAG: the decoder does not answer on this build"; exit 3; }
echo "[4/$total] the proof project copied to writable scratch (the volume is read-only here)"
P=/work/proof; rm -rf $P; cp -a /persist/lp1/Lean_IM_6266b40c_all $P; rm -rf $P/leanpath_src; du -sh $P | cut -f1
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | cut -d'"' -f2)
cd $P && printf 'import %s\n#check %s.Functions.execute_DIV\n' $PLIB $PLIB > /work/T.lean && timeout 600 lake env lean /work/T.lean 2>&1 | head -3 | cut -c1-200
echo "[5/$total] strip over every clause of the whole-model proof emit"
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
