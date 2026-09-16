#!/bin/bash
# lp3_l4_which_reset_step_reads_an_absent_register.sh -- on the pruned
# evaluable build: sail_model_init alone; then each reset step on the state
# it leaves; the registers present after init against the full register
# type; and the reads inside the emitted sail_model_init. LITERAL.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; cd $X
XLIB=$(grep -A1 '\[\[lean_lib\]\]' $X/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
echo "[1/3] reads inside the emitted sail_model_init, and the register count it writes"
awk '/^def sail_model_init /{p=1} p&&/^$/{exit} p' $XLIB.lean > /work/smi.txt; echo "  lines: $(wc -l < /work/smi.txt); writeReg: $(grep -c writeReg /work/smi.txt); readReg: $(grep -c readReg /work/smi.txt)"; grep -n "readReg\|←" /work/smi.txt | head -5 | cut -c1-160
echo "  registers in the type: $(awk '/^inductive Register where/{p=1;next} p&&/^  \| /{n++} p&&/^$/{exit} END{print n}' $XLIB/Defs.lean)"
echo "[2/3] init and the reset steps, one by one"
REGS=$(awk '/^inductive Register where/{p=1;next} p&&/^  \| /{print $2} p&&/^$/{exit}' $XLIB/Defs.lean | tr '\n' ' ')
cat > /work/Steps.lean <<L
import $XLIB
open Sail Sail.ConcurrencyInterfaceV1 PreSail $XLIB $XLIB.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
abbrev St := SequentialState RegisterType trivialChoiceSource
def blank : St := { regs := ∅, choiceState := (), mem := ∅, tags := (), cycleCount := 0, sailOutput := #[] }
def show1 (r : EStateM.Result (Sail.Error exception) St Unit) : String :=
  match r with | .ok _ s => s!"ok (regs {s.regs.size})" | .error e s => s!"ERROR {e.print} (regs {s.regs.size})"
def after (m : SailM Unit) (s : St) : St := match m s with | .ok _ s' => s' | .error _ s' => s'
def s1 := after (sail_model_init ()) blank
#eval IO.println ("sail_model_init on blank: " ++ show1 ((sail_model_init ()) blank))
#eval IO.println ("  then reset_sys:  " ++ show1 ((reset_sys ()) s1))
#eval IO.println ("  then reset_vmem: " ++ show1 ((reset_vmem ()) s1))
#eval IO.println ("  then reset_elp:  " ++ show1 ((reset_elp ()) s1))
#eval IO.println ("  then reset_misa: " ++ show1 ((reset_misa ()) s1))
#eval IO.println ("  then reset_pmp:  " ++ show1 ((reset_pmp ()) s1))
#eval IO.println ("  then reset_tvecs:" ++ show1 ((reset_tvecs ()) s1))
#eval IO.println ("  then reset ():   " ++ show1 ((reset ()) s1))
#eval IO.println ("  then init_model: " ++ show1 ((init_model \"\") s1))
#eval IO.println ("  config_is_valid: " ++ (match (config_is_valid ()) s1 with | .ok b _ => s!"ok={b}" | .error e _ => s!"ERROR {e.print}"))
L
echo '#eval IO.println ("absent after sail_model_init: " ++ toString ((([' >> /work/Steps.lean
for r in $REGS; do echo "  (\"$r\", (s1.regs.get? .$r).isSome)," >> /work/Steps.lean; done
echo '  ] : List (String × Bool)).filter (fun p => !p.2)).map (·.1)))' >> /work/Steps.lean
timeout 900 lake env lean /work/Steps.lean 2>&1 | cut -c1-400 | head -16
echo "[3/3] the reads of reset_sys, LITERAL (first eight)"
grep -n -A40 "^def reset_sys " $XLIB/SysControl.lean | grep -oE "readReg [a-z_0-9A-Z]+" | head -8 | tr '\n' ' '; echo
echo done
