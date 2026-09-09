#!/usr/bin/env bash
# t97 lane 11 -- the one place this round's 44-record shortfall leaks
# into a cause sentence, measured and named rather than left for a
# reader to find.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
python3 report97_numbers.py contamination
echo "exit $?"
