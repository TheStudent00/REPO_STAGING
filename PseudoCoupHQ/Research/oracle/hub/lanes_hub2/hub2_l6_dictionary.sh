#!/usr/bin/env bash
# hub2_l6_dictionary.sh -- task hub2, lane 6: the dictionary at two
# levels.  It reads task bank1's certificates.jsonl for the cell level,
# joins each preferred certificate back to the run that produced it for
# the emulation's own source and PARAMETER HOLDERS, keys the same
# entries by the (setter cell, consumer cell) PAIR where the loop
# rendered one, reads tasks o7 / o11 / o13 for the body level, and reads
# the corpus's own go units at all three levels.  It writes
# dictionary2.json and dictionary2.md and nothing else.  Memory bound
# 6 GB, named abort ABORT_MEMORY_HUB2.
set -uo pipefail
echo "[1/1] the dictionary"
cd PseudoCoupHQ/Research/oracle/hub
time python3 hub2.py dictionary
