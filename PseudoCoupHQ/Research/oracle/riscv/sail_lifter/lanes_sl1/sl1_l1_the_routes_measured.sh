#!/bin/bash
# sl1 lane 1 -- measure the routes FIRST (brief section 1): what the image's
# `sail` offers (-smt, --lean, an IR dump), what the model tree holds, how
# the C simulator was built, whether isla is reachable. Nothing is built
# here; every output is LITERAL for the log.
set -u
total=8
export HOME=/work
M=/sources/sail-riscv
echo "[1/$total] sail --version; sail --help (every option)"
sail --version 2>&1 | head -3
sail --help 2>&1
echo "[2/$total] the model tree and its commit"
ls $M 2>&1 | head -40
git -C $M rev-parse HEAD 2>&1 | head -2
git -C $M log -1 --format='%H %cd %s' 2>&1 | head -2
ls $M/model 2>&1 | head -80
ls $M/model/extensions 2>&1 | head -80
echo "[3/$total] how the simulator was built (the file list and flags)"
ls $M/build 2>&1 | head -20
find $M -maxdepth 3 -name 'CMakeLists.txt' 2>/dev/null | head
sed -n '1,200p' $M/model/CMakeLists.txt 2>&1
echo "[4/$total] the model's own counts: execute clauses, assembly clauses, ast clauses"
grep -rc 'function clause execute' $M/model --include='*.sail' | awk -F: '{s+=$2} END {print "execute clauses:", s}'
grep -rc 'mapping clause assembly' $M/model --include='*.sail' | awk -F: '{s+=$2} END {print "assembly clauses:", s}'
grep -rc 'union clause ast' $M/model --include='*.sail' | awk -F: '{s+=$2} END {print "ast clauses:", s}'
grep -rc 'mapping clause encdec' $M/model --include='*.sail' | awk -F: '{s+=$2} END {print "encdec clauses:", s}'
grep -rn 'union clause ast' $M/model --include='*.sail' | sed 's/.*union clause ast = //' | head -300
echo "[5/$total] one execute clause, one assembly clause, LITERAL (the first of the base file)"
F=$(grep -rl 'function clause execute' $M/model --include='*.sail' | grep -i base | head -1)
echo "file: $F"
grep -n 'function clause execute' $F | head -5
awk '/function clause execute \(RTYPE/,/^}/' $F | head -60
grep -n -A6 'mapping clause assembly = RTYPE' $F | head -20
grep -rn -A20 'mapping rtype_mnemonic' $M/model --include='*.sail' | head -30
echo "[6/$total] isla: opam, PATH"
which isla isla-footprint isla-axiomatic 2>&1 || echo "ABSENT: isla on PATH"
ls /opt/opam 2>&1 | head; ls /opt/opam/*/bin 2>/dev/null | head -40
opam list 2>&1 | grep -i 'isla\|sail\|lem\|linksem' | head
echo "[7/$total] the lean and smt backends: does the option exist"
sail --help 2>&1 | grep -i 'lean\|smt\|jib\|ir\b\|-ir' | head -20
ls $M/lean_emulator 2>&1 | head
echo "[8/$total] register access and the extension checks the execute clauses reach (LITERAL heads)"
grep -rn 'function rX\|function wX\|val rX\|val wX\|function X(' $M/model --include='*.sail' | head
grep -rn 'softfloat\|riscv_f32Add\|f32Add' $M/model --include='*.sail' | head -8
echo "done $(date -u +%FT%TZ)"
