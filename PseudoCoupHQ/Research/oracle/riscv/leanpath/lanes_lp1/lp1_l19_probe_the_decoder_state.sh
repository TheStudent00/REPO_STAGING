#!/bin/bash
# lp1_l19_probe_the_decoder_state.sh -- why the decoder answers ERROR: the
# error text of init_model on a blank state, of reset, and of the decoder
# on the blank and on the initialised state. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
X=/persist/lp1/Lean_IMZ_exec; cd $X
cat > /work/Probe.lean <<'L'
import LeanIMZExecutable
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZExecutable LeanIMZExecutable.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
def blank : SequentialState RegisterType trivialChoiceSource :=
  { regs := ∅, choiceState := (), mem := ∅, tags := (), cycleCount := 0, sailOutput := #[] }
def show1 (r : EStateM.Result (Sail.Error exception) (SequentialState RegisterType trivialChoiceSource) Unit) : String :=
  match r with | .ok _ s => s!"ok, regs {s.regs.size}" | .error e s => s!"ERROR {e.print} (regs {s.regs.size})"
#eval IO.println ("init_model on blank: " ++ show1 ((init_model "") blank))
#eval IO.println ("reset on blank: " ++ show1 ((reset ()) blank))
#eval IO.println ("reset_sys on blank: " ++ show1 ((reset_sys ()) blank))
#eval IO.println ("reset_misa on blank: " ++ show1 ((reset_misa ()) blank))
def s0 : SequentialState RegisterType trivialChoiceSource :=
  match (init_model "") blank with | .ok _ s => s | .error _ s => s
#eval IO.println ("s0 regs: " ++ toString s0.regs.size)
#eval IO.println ("misa in s0: " ++ (match s0.regs.get? .misa with | some v => toString (repr v) | none => "absent"))
#eval IO.println ("decode c.add on s0: " ++ (match (encdec_compressed_backwards (0x952e#16)) s0 with | .ok i _ => toString (repr i) | .error e _ => "ERROR " ++ e.print))
#eval IO.println ("decode divw on s0: " ++ (match (encdec_backwards (0x02b5453b#32)) s0 with | .ok i _ => toString (repr i) | .error e _ => "ERROR " ++ e.print))
#eval IO.println ("currentlyEnabled M on s0: " ++ (match (currentlyEnabled Ext_M) s0 with | .ok b _ => toString b | .error e _ => "ERROR " ++ e.print))
L
echo "[1/1] the probe, LITERAL"
timeout 600 lake env lean /work/Probe.lean 2>&1 | cut -c1-240 | head -30
echo done
