#!/bin/bash
# lp4_l1_which_arms_the_subset_decoder_lacks.sh -- on the subset executable
# build that compiled in four minutes (I, M, Zca, Zcb, Zba, Zbb, Zbs): evaluate
# `currentlyEnabled` for EVERY extension the model declares, on the state the
# model's own init gives, and name the ones that throw (the missing arms);
# then decode the handful's words and name which fail. The answer is the
# smallest set of modules to add. Read-only volume; writes under /work.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/persist/lp1/Lean_IMZ_exec; cd $X
LIB=LeanIMZExecutable
echo "[1/3] the extensions the model declares"
EXTS=$(awk '/^inductive extension where/{p=1;next} p&&/^  \| /{print $2} p&&/^$/{exit}' $LIB/Defs.lean | tr '\n' ' ')
echo "  $(echo $EXTS | wc -w) extensions"
echo "[2/3] currentlyEnabled on each, LITERAL: ok=<value> or ERROR"
{
cat <<L
import $LIB
open Sail Sail.ConcurrencyInterfaceV1 PreSail $LIB $LIB.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
def blank : SequentialState RegisterType trivialChoiceSource :=
  { regs := ∅, choiceState := (), mem := ∅, tags := (), cycleCount := 0, sailOutput := #[] }
def s0 : SequentialState RegisterType trivialChoiceSource :=
  match (do sail_model_init (); init_model "") blank with | .ok _ s => s | .error _ s => s
L
for e in $EXTS; do echo "#eval IO.println (\"$e\\t\" ++ (match (currentlyEnabled .$e) s0 with | .ok b _ => \"ok=\" ++ toString b | .error e _ => \"ERROR \" ++ e.print))"; done
} > /work/Arms.lean
timeout 900 lake env lean /work/Arms.lean > /work/Arms.out 2>&1; rc=$?
echo "  lean rc=$rc; ok: $(grep -c 'ok=' /work/Arms.out); ERROR: $(grep -c 'ERROR' /work/Arms.out)"
echo "  the extensions whose arm is missing (ERROR), LITERAL:"; grep 'ERROR' /work/Arms.out | cut -c1-120 | sed 's/^/    /'
grep -vE 'ok=|ERROR' /work/Arms.out | head -5 | cut -c1-200
echo "[3/3] the handful's distinct words through this decoder"
python3 - <<'PY' > /work/Words.lean
import json
units=json.load(open("PseudoCoupHQ/Research/oracle/riscv/leanpath/handful_units.json"))
words=[]
for u in units:
    for w in u.get("words",[]):
        if w not in words: words.append(w)
print("import LeanIMZExecutable\nopen Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZExecutable LeanIMZExecutable.Functions\nset_option maxHeartbeats 1000000000\nset_option maxRecDepth 100000")
print('def blank : SequentialState RegisterType trivialChoiceSource :=\n  { regs := ∅, choiceState := (), mem := ∅, tags := (), cycleCount := 0, sailOutput := #[] }')
print('def s0 : SequentialState RegisterType trivialChoiceSource :=\n  match (do sail_model_init (); init_model "") blank with | .ok _ s => s | .error _ s => s')
for w in words:
    n=len(w)*4; dec="encdec_backwards" if n==32 else "encdec_compressed_backwards"
    print('#eval IO.println ("%s\\t" ++ (match (%s (0x%s#%d)) s0 with | .ok i _ => toString (repr i) | .error e _ => "ERROR " ++ e.print))' % (w, dec, w, n))
PY
timeout 900 lake env lean /work/Words.lean 2>&1 | cut -c1-200 | head -20
echo done
