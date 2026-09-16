#!/bin/bash
# lp2_l2_exec_decoder_only_closure.sh -- lane lp2_l1 again, with the set of
# noncomputable names closed under "mentions a name in the set" over the
# emitted text (Lean requires every caller of a noncomputable definition to
# be noncomputable), the two decoders and the init path checked to be
# outside it, then the emit, the build, the decoder probe.
set -uo pipefail
total=5
export OPAMROOT=/persist/opam
export ELAN_HOME=/persist/lp1/elan
export PATH=/persist/opam/default/bin:$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
SRC=/persist/sail-riscv-6266b40c
CFG=$SRC/build/config/rv64d_v256_e64.json
P=/persist/lp1/Lean_IM_6266b40c_all
PREV=$(ls -d /work/emit_dec/Lean_IM_dec_executable/Lean*/ 2>/dev/null | head -1)
[ -n "$PREV" ] || { echo "FLAG: the previous emit is gone from /work"; exit 3; }
echo "[1/$total] the closure of the noncomputable set over the previous emit ($PREV)"
python3 - "$PREV" > /work/nc_closure.txt <<'PY'
import re, sys, os, glob
d=sys.argv[1]
seed={"encdec_backwards_matches","encdec_compressed_backwards_matches","encdec_forwards","encdec_forwards_matches",
      "encdec_compressed_forwards","encdec_compressed_forwards_matches","assembly_forwards","assembly_backwards",
      "assembly_forwards_matches","assembly_backwards_matches","execute","step","loop","fetch","sail_main","main"}
keep={"encdec_backwards","encdec_compressed_backwards","sail_model_init","init_model","reset"}
defs={}
for f in glob.glob(os.path.join(d,"*.lean"))+glob.glob(os.path.join(d,"..","*.lean")):
    t=open(f).read()
    for m in re.finditer(r"^(?:noncomputable )?def (\w+)\b(.*?)(?=^(?:noncomputable )?def |\Z)", t, re.S|re.M):
        defs.setdefault(m.group(1), "")
        defs[m.group(1)] += m.group(2)
marked=set(seed)
changed=True
while changed:
    changed=False
    pat=re.compile(r"\b(" + "|".join(sorted(map(re.escape, marked))) + r")\b")
    for name, body in defs.items():
        if name in marked: continue
        if pat.search(body):
            marked.add(name); changed=True
bad=sorted(marked & keep)
sys.stderr.write("defs %d; marked %d; decoders or init caught: %s\n" % (len(defs), len(marked), bad or "none"))
for n in sorted(marked): print(n)
PY
echo "  names marked: $(wc -l < /work/nc_closure.txt)"; head -c 600 /work/nc_closure.txt | tr '\n' ' '; echo
grep -qE '^(encdec_backwards|encdec_compressed_backwards|sail_model_init|init_model)$' /work/nc_closure.txt && { echo "FLAG: a decoder or the init path is in the closure; the seed is wrong"; exit 3; }
echo "[2/$total] the emit with that set marked"
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
NC=""; while read -r n; do NC="$NC --lean-noncomputable-function $n"; done < /work/nc_closure.txt
OUT=/work/emit_dec2; rm -rf $OUT /work/smtcache6; mkdir -p $OUT
start=$(date +%s)
sail --strict-var --strict-bitvector --strict-exponentials --memo-z3-path /work/smtcache6 \
  --config $CFG --lean --memo-z3 --lean-output-dir $OUT --lean-force-output \
  --lean-non-beq-type instruction --lean-non-beq-type ExecutionResult --lean-non-beq-type Step \
  $NC --lean-import-file ../handwritten_support/RiscvExtrasExecutable.lean -o Lean_IM_dec_executable \
  $MODS riscv.sail_project > /work/emit_dec2.log 2>&1
rc=$?; echo "  emit rc=$rc seconds=$(( $(date +%s) - start ))"
[ $rc -eq 0 ] || { echo "FLAG: the emit failed"; tail -12 /work/emit_dec2.log; exit 3; }
D=$(ls -d $OUT/Lean_IM_dec_executable/Lean*/ | head -1)
echo "  noncomputable defs in the emit: $(grep -rc '^noncomputable def' $D/*.lean | awk -F: '{s+=$2} END{print s}'); computable decoders: $(grep -cE '^def encdec_(compressed_)?backwards ' $D/InstsEnd.lean)"
echo "[3/$total] build under /work"
X=/work/Lean_IM_dec_exec; rm -rf $X; cp -a $OUT/Lean_IM_dec_executable $X; mkdir -p $X/.lake
cp -a $P/.lake/packages $X/.lake/ && cp $P/lake-manifest.json $X/
cd $X; start=$(date +%s); lake build > /work/lake_dec2.log 2>&1; rc=$?
echo "  lake rc=$rc seconds=$(( $(date +%s) - start ))"; grep -cE '^error' /work/lake_dec2.log | sed 's/^/  error lines: /'; grep -E 'Build completed|error:' /work/lake_dec2.log | head -6 | cut -c1-200
[ $rc -eq 0 ] || { echo "FLAG: the build fails"; exit 3; }
echo "[4/$total] the decoder on the initialised state, four words, LITERAL"
XLIB=$(grep -A1 '\[\[lean_lib\]\]' $X/lakefile.toml | grep -oE 'name = "[^"]+"' | cut -d'"' -f2)
cat > /work/Probe6.lean <<L
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
timeout 900 lake env lean /work/Probe6.lean 2>&1 | cut -c1-240 | head -10
echo "[5/$total] lake env lean in the read-only proof project: one trivial file"
cd $P && printf 'import LeanIM\n#check LeanIM.Functions.execute_DIV\n' > /work/T.lean && timeout 600 lake env lean /work/T.lean 2>&1 | head -4 | cut -c1-200
echo done
