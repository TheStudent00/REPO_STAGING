#!/usr/bin/env bash
# t101 lane 1 -- step 1 of the dominant-types join: read the DWARF byte
# size and encoding of every probe parameter out of the stored parameter
# tables. The program refuses by name and stops when no stored row
# carries either field.
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "======== [1/1] types101_join.py ========"
python3 types101_join.py
rc=$?
echo "types101_join.py exit ${rc}"
# exit 4 is this program's named refusal, which is the measured answer,
# not a lane failure.
if [ "${rc}" = "4" ]; then exit 0; fi
exit ${rc}
