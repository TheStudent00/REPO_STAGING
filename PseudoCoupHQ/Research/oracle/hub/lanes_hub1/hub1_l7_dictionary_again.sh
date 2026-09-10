#!/usr/bin/env bash
# hub1_l7_dictionary_again.sh -- task hub1, lane 7: the dictionary rebuilt
# with the whole go population beside the narrow one, so that a node the
# narrow population attests no cell for is a hole with go's OWN body as its
# cause rather than an absence. Memory bound 6 GB, abort ABORT_MEMORY_HUB1.
set -uo pipefail
cd PseudoCoupHQ/Research/oracle/hub
python3 hub.py dictionary
echo "---- the spelling guard"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    PseudoCoupHQ/Research/oracle/hub/dictionary.json
