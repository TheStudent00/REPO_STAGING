#!/bin/bash
# lp4_l2_enabled_arms_and_misa.sh -- on the subset executable build: the
# extension type's shape, the arms the emitted currentlyEnabled has, and
# on the initialised state: misa's fields, hartSupports and currentlyEnabled
# for the extensions the handful needs. LITERAL. Writes under /work only.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/persist/lp1/Lean_IMZ_exec; cd $X; LIB=LeanIMZExecutable
echo "[1/3] the extension type and the emitted currentlyEnabled arms"
grep -n "inductive extension" $LIB/*.lean | head -2
f=$(grep -l "inductive extension" $LIB/*.lean | head -1); awk '/inductive extension/{p=1} p{print} p&&/deriving/{exit}' $f | head -8 | cut -c1-160
echo "  constructors: $(awk '/inductive extension/{p=1} p&&/^ *\| /{n++} p&&/deriving/{exit} END{print n}' $f)"
echo "  currentlyEnabled arms in the emit: $(awk '/^def currentlyEnabled /{p=1} p&&/^  \| \./{n++} p&&/^$/{exit} END{print n}' $LIB/PlatformConfig.lean); the default arm:"
awk '/^def currentlyEnabled /{p=1} p&&/\| _ =>/{print; getline; print; exit}' $LIB/PlatformConfig.lean | cut -c1-200
echo "  arms present:"; awk '/^def currentlyEnabled /{p=1} p&&/^  \| \./{print $2} p&&/^$/{exit}' $LIB/PlatformConfig.lean | tr '\n' ' ' | cut -c1-600; echo
echo "[2/3] on the initialised state: misa fields, hartSupports, currentlyEnabled"
cat > /work/Misa.lean <<L
import $LIB
open Sail Sail.ConcurrencyInterfaceV1 PreSail $LIB $LIB.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
def blank : SequentialState RegisterType trivialChoiceSource :=
  { regs := ∅, choiceState := (), mem := ∅, tags := (), cycleCount := 0, sailOutput := #[] }
def s0 : SequentialState RegisterType trivialChoiceSource :=
  match (do sail_model_init (); init_model "") blank with | .ok _ s => s | .error _ s => s
#eval IO.println ("misa: " ++ (match s0.regs.get? .misa with | some v => toString (repr v) | none => "absent"))
#eval IO.println ("misa.M: " ++ (match s0.regs.get? .misa with | some v => toString (repr (_get_Misa_M v)) | none => "absent"))
#eval IO.println ("misa.C: " ++ (match s0.regs.get? .misa with | some v => toString (repr (_get_Misa_C v)) | none => "absent"))
#eval IO.println ("hartSupports M C Zca Zcb Zba A F D V: " ++ toString [hartSupports .Ext_M, hartSupports .Ext_C, hartSupports .Ext_Zca, hartSupports .Ext_Zcb, hartSupports .Ext_Zba, hartSupports .Ext_A, hartSupports .Ext_F, hartSupports .Ext_D, hartSupports .Ext_V])
L
for e in Ext_M Ext_C Ext_Zca Ext_Zcb Ext_Zba Ext_Zbb Ext_Zbs Ext_A Ext_F Ext_D Ext_V Ext_Zicond Ext_Zicsr Ext_Zifencei Ext_Zmmul Ext_Zaamo Ext_Zalrsc Ext_Zfh Ext_Zicfilp Ext_Zimop Ext_Zcmop Ext_Zkn Ext_Zks Ext_Zawrs Ext_Sstc Ext_Svinval Ext_Zicbom Ext_Zicboz Ext_Zicbop; do
  echo "#eval IO.println (\"$e\\t\" ++ (match (currentlyEnabled .$e) s0 with | .ok b _ => \"ok=\" ++ toString b | .error e _ => \"ERROR \" ++ e.print))" >> /work/Misa.lean
done
timeout 600 lake env lean /work/Misa.lean 2>&1 | cut -c1-200 | head -40
echo "[3/3] the first patterns of the 32-bit decoder: which guards come first (the emitted chain, first 3 guards)"
grep -n -m3 -oE "currentlyEnabled [A-Za-z_.]+" $LIB/InstsEnd.lean | head -3; awk '/^noncomputable def encdec_backwards |^def encdec_backwards /{p=1} p&&/currentlyEnabled/{n++; if(n<=6){print NR": "$0}} n>=6{exit}' $LIB/InstsEnd.lean | cut -c1-160
echo done
