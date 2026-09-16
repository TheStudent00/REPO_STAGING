#!/bin/bash
# lp4_l4_exec_arms_complete_pattern_light.sh -- the evaluable variant over
# every leaf module EXCEPT the three that carry no enabled-check arm but
# hold the bulk of the decoder's patterns (V_instructions, FD_instructions,
# Zvabd_insts): all arms present, about half the patterns. The giants are
# marked noncomputable by the closure computed on a first plain emit. Then
# the build (the measurement) and the decoder probe. Writes under /work.
set -uo pipefail
total=5
export OPAMROOT=/persist/opam
export ELAN_HOME=/persist/lp1/elan
export PATH=/persist/opam/default/bin:$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
SRC=/persist/sail-riscv-6266b40c
CFG=$SRC/build/config/rv64d_v256_e64.json
P=/persist/lp1/Lean_IM_6266b40c_all
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
print(" ".join(n for n in names if n not in {"V_instructions","FD_instructions","Zvabd_insts"}))
PY
)
echo "[1/$total] modules ($(echo $MODS | wc -w)); files: $(sail --config $CFG --list-files $MODS riscv.sail_project 2>/dev/null | tr ' ' '\n' | grep -c .)"
EMIT() { sail --strict-var --strict-bitvector --strict-exponentials --memo-z3-path /work/smtcache7 \
  --config $CFG --lean --memo-z3 --lean-output-dir $1 --lean-force-output \
  --lean-non-beq-type instruction --lean-non-beq-type ExecutionResult --lean-non-beq-type Step \
  $2 --lean-import-file ../handwritten_support/RiscvExtrasExecutable.lean -o Lean_IM_pl_executable \
  $MODS riscv.sail_project; }
echo "[2/$total] a plain emit, for the closure"
OUT1=/work/emit_pl1; rm -rf $OUT1; mkdir -p $OUT1; start=$(date +%s); EMIT $OUT1 "" > /work/emit_pl1.log 2>&1; rc=$?; echo "  emit rc=$rc seconds=$(( $(date +%s) - start ))"; [ $rc -eq 0 ] || { tail -8 /work/emit_pl1.log; exit 3; }
D1=$(ls -d $OUT1/Lean_IM_pl_executable/Lean*/ | head -1)
python3 - "$D1" > /work/nc.txt 2> /work/nc.err <<'PY'
import re, sys, os, glob
d=sys.argv[1]
seed={"encdec_backwards_matches","encdec_compressed_backwards_matches","encdec_forwards","encdec_forwards_matches",
      "encdec_compressed_forwards","encdec_compressed_forwards_matches","assembly_forwards","assembly_backwards",
      "assembly_forwards_matches","assembly_backwards_matches"}
keep={"encdec_backwards","encdec_compressed_backwards","sail_model_init","init_model","reset"}
def code_only(s):
    s=re.sub(r"/-.*?-/", " ", s, flags=re.S); s=re.sub(r"--[^\n]*", " ", s); return re.sub(r'"(?:[^"\\]|\\.)*"', '""', s)
defs={}
for f in glob.glob(os.path.join(d,"*.lean"))+glob.glob(os.path.join(d,"..","*.lean")):
    t=open(f).read()
    for m in re.finditer(r"^(?:noncomputable )?def (\w+)\b(.*?)(?=^(?:noncomputable )?def |\Z)", t, re.S|re.M):
        defs[m.group(1)]=defs.get(m.group(1),"")+code_only(m.group(2))
marked=set(seed); changed=True
while changed:
    changed=False; pat=re.compile(r"\b(" + "|".join(sorted(map(re.escape, marked))) + r")\b")
    for name, body in defs.items():
        if name not in marked and pat.search(body): marked.add(name); changed=True
sys.stderr.write("defs %d marked %d caught %s\n" % (len(defs), len(marked), sorted(marked & keep)))
for n in sorted(marked): print(n)
PY
cat /work/nc.err; grep -qE '^(encdec_backwards|encdec_compressed_backwards|sail_model_init|init_model)$' /work/nc.txt && { echo "FLAG: closure caught a decoder or init"; exit 3; }
echo "[3/$total] the emit with $(wc -l < /work/nc.txt) names marked, then the build (timed)"
NC=""; while read -r n; do NC="$NC --lean-noncomputable-function $n"; done < /work/nc.txt
OUT=/work/emit_pl; rm -rf $OUT; mkdir -p $OUT; start=$(date +%s); EMIT $OUT "$NC" > /work/emit_pl.log 2>&1; rc=$?; echo "  emit rc=$rc seconds=$(( $(date +%s) - start ))"; [ $rc -eq 0 ] || { tail -8 /work/emit_pl.log; exit 3; }
D=$(ls -d $OUT/Lean_IM_pl_executable/Lean*/ | head -1); echo "  InstsEnd lines: $(wc -l < $D/InstsEnd.lean); decoder lines: $(awk '/^def encdec_backwards /{s=NR} s&&/^$/{print NR-s; exit}' $D/InstsEnd.lean)"
X=/work/Lean_IM_pl_exec; rm -rf $X; cp -a $OUT/Lean_IM_pl_executable $X; mkdir -p $X/.lake; cp -a $P/.lake/packages $X/.lake/; cp $P/lake-manifest.json $X/
cd $X; start=$(date +%s); lake build > /work/lake_pl.log 2>&1; rc=$?
echo "  lake rc=$rc seconds=$(( $(date +%s) - start ))"; grep -cE '^error' /work/lake_pl.log | sed 's/^/  error lines: /'; grep -E 'Build completed|error:' /work/lake_pl.log | head -5 | cut -c1-200
[ $rc -eq 0 ] || { echo "FLAG: the build fails"; exit 3; }
echo "[4/$total] init and the decoder on the initialised state, LITERAL"
XLIB=$(grep -A1 '\[\[lean_lib\]\]' $X/lakefile.toml | grep -oE 'name = "[^"]+"' | cut -d'"' -f2)
cat > /work/Probe7.lean <<L
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
L
timeout 900 lake env lean /work/Probe7.lean 2>&1 | cut -c1-240 | head -10
echo "[5/$total] done"
