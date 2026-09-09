#!/usr/bin/env bash
# t101 lane 6 -- the last two commands the DevComms log pastes, run
# from the working directory the log's verifier uses
# (/projects/PseudoCoupHQ), so both are full-path forms that reproduce
# there.
set -u
cd /projects/PseudoCoupHQ

run() {
  echo "\$ $1"
  eval "$1"
  echo "--------8<--------"
}

echo "======== [1/2] the measured peak memory ========"
run "python3 -c \"import json;d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/types101_dwarf_flag.json'));print(d['memory']['peak_rss_mb'], 'MB peak against a 2048 MB bound')\""

echo "======== [2/2] the spelling-ban guard, full paths ========"
run "python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py /projects/PseudoCoupHQ/Research/op_pipeline/types101_dwarf_flag.json"

exit 0
