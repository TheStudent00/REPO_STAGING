#!/bin/bash
# task o13, lane 5: THE TIME LIMIT IS A FLAG, not an answer.
# Three of the mode-rendered rows came back UNDECIDED because the
# gate's 3,000 ms solver ceiling ran out (its own words: "the solver
# did not answer inside its 3000 ms limit").  Both targets are re-run
# whole with the ceiling at 30,000 ms -- ten times the room, and still
# inside the runner's own 240 s wall clock per sub-process, which takes
# at most four solver calls -- into their own files, so the two answers
# can be compared rather than the limit reported as a result.
set -u
M=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/mode
G=/projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
export PATH=/opt/cargo/bin:$PATH
echo "[1/3] the c re-run with the solver ceiling at 30000 ms"
cd "$M" && python3 mode.py run c 30000
echo "[2/3] the rust re-run with the solver ceiling at 30000 ms"
cd "$M" && python3 mode.py run rust 30000
echo "[3/3] the guard over the json this lane wrote"
for f in mode_run_c_30000_ms.json mode_run_rust_30000_ms.json; do
  python3 "$G" "$M/$f"
done
echo "lane o13_l5 done"
