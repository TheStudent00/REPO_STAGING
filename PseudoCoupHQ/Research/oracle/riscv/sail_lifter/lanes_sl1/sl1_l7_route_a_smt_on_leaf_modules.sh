#!/bin/bash
# sl1 lane 7 -- route (a) with LEAF module names (log_274 §3: groups such
# as `I` hold no execute clause; the leaves `I_insts`, `M_insts` do), one
# property, verbose, a 3,600 s ceiling. Lane 6 named groups and is
# expected to fail fast; this is the corrected probe.
set -u
total=5
export HOME=/work
SL=PseudoCoupHQ/Research/oracle/riscv/sail_lifter
W=/work/sl1c
mkdir -p $W
echo "[1/$total] the leaves of the subset, read off the project file"
LEAVES=$(python3 $SL/select_modules.py /sources/sail-riscv/model/riscv.sail_project I M B FD C Zicond Zicsr Zifencei)
echo "leaves: $LEAVES"
echo "[2/$total] the configuration and a writable copy of the model"
sail_riscv_sim --print-default-config > $W/config.json; echo "  exit: $?"
rm -rf $W/model; cp -r /sources/sail-riscv/model $W/model; echo "  exit: $?"
cd $W/model
echo "  list-files over the selection (seconds, per log_274):"
S=$(date +%s); sail --project riscv.sail_project --list-files $LEAVES postlude main 2>&1 | tr ' ' '\n' | wc -l; echo "  seconds: $(( $(date +%s) - S ))"
echo "[3/$total] one property, first constructor"
python3 $SL/generate.py props $W/model 1
echo "[4/$total] sail --smt on the leaves, verbose, ceiling 3600 s"
S=$(date +%s)
timeout 3600 sail --project riscv.sail_project $LEAVES postlude main sl1_props --strict-var --strict-bitvector --strict-exponentials --memo-z3-path /work/sl1_smt_cache --config $W/config.json --verbose 1 --smt -o $W/probe > $W/smt.out 2>&1
echo "  exit: $? seconds: $(( $(date +%s) - S ))"
head -60 $W/smt.out; echo ...; tail -60 $W/smt.out
ls -la $W | head -30
echo "[5/$total] the output, LITERAL, if any"
for f in $W/probe*.smt2; do echo "$f $(wc -c < $f) bytes $(wc -l < $f) lines"; head -80 $f; echo ...; tail -40 $f; done 2>/dev/null
echo "done $(date -u +%FT%TZ)"
