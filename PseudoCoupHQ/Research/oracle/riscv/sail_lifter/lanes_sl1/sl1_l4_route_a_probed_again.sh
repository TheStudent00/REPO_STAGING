#!/bin/bash
# sl1 lane 4 -- lane 3 again after the field rename (a field named f0 shadowed a float register); route (a), Sail's own SMT backend, probed on the first six
# constructors of the base file: does it run on this model, how long, and
# what does its output look like. LITERAL outputs for the log.
set -u
total=6
export HOME=/work
SL=PseudoCoupHQ/Research/oracle/riscv/sail_lifter
W=/work/sl1
mkdir -p $W
echo "[1/$total] the simulator's default configuration, dumped"
sail_riscv_sim --print-default-config > $W/config.json 2>$W/config.err; echo "  exit: $?"; wc -c $W/config.json; head -c 600 $W/config.json; echo
echo "[2/$total] a writable copy of the model"
rm -rf $W/model; cp -r /sources/sail-riscv/model $W/model; echo "  exit: $?"
echo "[3/$total] the probe properties, first six constructors"
python3 $SL/probe_props.py $W/model 6
cat $W/model/sl1_props.sail | head -40
echo "[4/$total] sail --smt, timed"
cd $W/model
S=$(date +%s)
sail --project riscv.sail_project --all-modules --strict-var --strict-bitvector --strict-exponentials --memo-z3-path /work/sl1_smt_cache --config $W/config.json --smt -o $W/probe 2>&1 | tail -40
echo "  exit: ${PIPESTATUS[0]} seconds: $(( $(date +%s) - S ))"
ls -la $W | head -40
echo "[5/$total] the output, LITERAL: sizes, head and tail of the first file"
for f in $W/probe*.smt2; do echo "$f $(wc -c < $f) bytes $(wc -l < $f) lines"; done 2>/dev/null
F=$(ls $W/probe*.smt2 2>/dev/null | head -1)
if [ -n "$F" ]; then head -60 $F; echo ...; tail -40 $F; fi
echo "[6/$total] z3 parses it?"
python3 - <<PYEOF
import glob, z3, time
for f in sorted(glob.glob("$W/probe*.smt2")):
    t = time.time()
    try:
        a = z3.parse_smt2_file(f)
        print(f, "assertions", len(a), "%.1fs" % (time.time() - t))
        s = str(a[-1]); print("  last assertion, first 400 chars:", s[:400])
    except Exception as e:
        print(f, "PARSE FAILED:", str(e)[:400])
PYEOF
echo "done $(date -u +%FT%TZ)"
