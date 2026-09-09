#!/bin/bash
# task o13, lane 11: get the exact, reproducible text of the grep -c
# exempt command over this task's files, run from /projects/PseudoCoupHQ
# (the verifier's own working directory), so the log pastes what the
# sandbox actually produces rather than a guess.
set -u
cd /projects/PseudoCoupHQ
echo "[1/1] grep -c exempt, from /projects/PseudoCoupHQ"
grep -c exempt Research/oracle/cross_construction/emulation/mode/mode.py Research/oracle/cross_construction/emulation/mode/mode_diagnose_c.json Research/oracle/cross_construction/emulation/mode/mode_facts.json Research/oracle/cross_construction/emulation/mode/mode_population.json Research/oracle/cross_construction/emulation/mode/mode_results.json Research/oracle/cross_construction/emulation/mode/mode_run_c.json Research/oracle/cross_construction/emulation/mode/mode_run_c_30000_ms.json Research/oracle/cross_construction/emulation/mode/mode_run_rust.json Research/oracle/cross_construction/emulation/mode/mode_run_rust_30000_ms.json
echo "lane o13_l11 done"
