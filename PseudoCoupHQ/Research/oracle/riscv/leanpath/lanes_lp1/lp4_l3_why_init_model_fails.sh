#!/bin/bash
# lp4_l3_why_init_model_fails.sh -- on the subset executable build: the
# result of sail_model_init, of init_model, of config_is_valid, and of
# reset, each LITERAL, so the half-initialised state has its cause named.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/persist/lp1/Lean_IMZ_exec; cd $X; LIB=LeanIMZExecutable
cat > /work/Init.lean <<L
import $LIB
open Sail Sail.ConcurrencyInterfaceV1 PreSail $LIB $LIB.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
def blank : SequentialState RegisterType trivialChoiceSource :=
  { regs := ∅, choiceState := (), mem := ∅, tags := (), cycleCount := 0, sailOutput := #[] }
def show1 (r : EStateM.Result (Sail.Error exception) (SequentialState RegisterType trivialChoiceSource) Unit) : String :=
  match r with | .ok _ s => s!"ok (regs {s.regs.size})" | .error e s => s!"ERROR {e.print} (regs {s.regs.size})"
def showB (r : EStateM.Result (Sail.Error exception) (SequentialState RegisterType trivialChoiceSource) Bool) : String :=
  match r with | .ok b _ => s!"ok={b}" | .error e _ => s!"ERROR {e.print}"
def s1 := match (sail_model_init ()) blank with | .ok _ s => s | .error _ s => s
#eval IO.println ("sail_model_init on blank: " ++ show1 ((sail_model_init ()) blank))
#eval IO.println ("config_is_valid on s1: " ++ showB ((config_is_valid ()) s1))
#eval IO.println ("reset on s1: " ++ show1 ((reset ()) s1))
#eval IO.println ("init_model on s1: " ++ show1 ((init_model "") s1))
def s2 := match (reset ()) s1 with | .ok _ s => s | .error _ s => s
#eval IO.println ("misa after reset: " ++ (match s2.regs.get? .misa with | some v => toString (repr v) | none => "absent"))
#eval IO.println ("sailOutput after init_model: " ++ toString (match (init_model "") s1 with | .ok _ s => s.sailOutput | .error _ s => s.sailOutput))
L
timeout 600 lake env lean /work/Init.lean 2>&1 | cut -c1-300 | head -12
echo done
