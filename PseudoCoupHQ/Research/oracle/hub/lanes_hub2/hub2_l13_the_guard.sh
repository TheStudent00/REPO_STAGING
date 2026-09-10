#!/usr/bin/env bash
# hub2_l13_the_guard.sh -- task hub2, lane 13: the spelling guard over
# every json this task writes, and `grep -c exempt` over every file it
# adds.  The guard is never modified; a failure is fixed in what this
# task wrote.
set -uo pipefail
cd PseudoCoupHQ/Research/oracle/hub
G=PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
echo "[1/2] the spelling guard"
for f in dictionary2.json oracle_test2.json measure2.json ; do
    echo "\$ python3 $G PseudoCoupHQ/Research/oracle/hub/$f"
    python3 "$G" "PseudoCoupHQ/Research/oracle/hub/$f"
done
echo "[2/2] no exemption anywhere in what this task adds"
pattern="exem""pt"
echo "hub2.py $(grep -c "$pattern" hub2.py)"
for f in lanes_hub2/*.sh ; do
    echo "$f $(grep -c "$pattern" "$f")"
done
