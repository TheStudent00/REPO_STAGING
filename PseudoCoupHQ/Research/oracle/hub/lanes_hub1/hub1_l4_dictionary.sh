#!/usr/bin/env bash
# hub1_l4_dictionary.sh -- task hub1, lane 4: the dictionary.
# Step 4 of the master order: the lookup read off the polyfill-complete set.
# Target side from task ap5's own run store; go side from the corpus's own
# single-opcode go units and their ledgers. Memory bound 6 GB, named abort
# ABORT_MEMORY_HUB1. Writes dictionary.json and dictionary.md only.
set -uo pipefail
cd PseudoCoupHQ/Research/oracle/hub
python3 hub.py dictionary
echo "---- the spelling guard over what this lane wrote"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    PseudoCoupHQ/Research/oracle/hub/dictionary.json
