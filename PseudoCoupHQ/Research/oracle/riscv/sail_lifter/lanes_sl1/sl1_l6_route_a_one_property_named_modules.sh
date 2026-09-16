#!/bin/bash
# sl1 lane 6 -- route (a) again, smaller: the whole project file printed
# (lane 1 cut it at 150 lines), then `sail --smt` on ONE property (the
# first constructor of the base file) with only the modules the brief's
# subset needs named instead of --all-modules, verbose phase timing on,
# and a 5,400 s ceiling so the lane ends with its evidence either way.
set -u
total=5
export HOME=/work
SL=PseudoCoupHQ/Research/oracle/riscv/sail_lifter
W=/work/sl1b
mkdir -p $W
echo "[1/$total] the whole project file, LITERAL"
cat /sources/sail-riscv/model/riscv.sail_project
echo "[2/$total] the configuration and a writable copy of the model"
sail_riscv_sim --print-default-config > $W/config.json; echo "  exit: $?"
rm -rf $W/model; cp -r /sources/sail-riscv/model $W/model; echo "  exit: $?"
echo "[3/$total] one property, first constructor"
python3 $SL/probe_props.py $W/model 1
echo "[4/$total] sail --smt on named modules, verbose, timed, ceiling 5400 s"
cd $W/model
MODS="prelude core exceptions pmp sys I M B FD C Zicond Zicsr Zifencei Zicntr Zihpm Zihintpause Zihintntl mops postlude main sl1_props"
echo "modules: $MODS"
S=$(date +%s)
timeout 5400 sail --project riscv.sail_project $MODS --strict-var --strict-bitvector --strict-exponentials --memo-z3-path /work/sl1_smt_cache --config $W/config.json --verbose 1 --smt -o $W/probe > $W/smt.out 2>&1
echo "  exit: $? seconds: $(( $(date +%s) - S ))"
echo "  --- smt.out, first 60 and last 60 lines ---"
head -60 $W/smt.out; echo ...; tail -60 $W/smt.out
ls -la $W | head -30
echo "[5/$total] the output, LITERAL, if any"
for f in $W/probe*.smt2; do echo "$f $(wc -c < $f) bytes $(wc -l < $f) lines"; head -80 $f; echo ...; tail -40 $f; done 2>/dev/null
echo "done $(date -u +%FT%TZ)"
