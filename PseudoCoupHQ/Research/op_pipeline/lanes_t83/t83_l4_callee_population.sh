#!/usr/bin/env bash
# t83 lane 4 -- the POPULATION of the blocker.  probe83b located the
# runaway inside one unit's walk into an attached runtime callee; this
# lane counts how many canon40-proved units reach that walk at all,
# and through which callee, so the flag carries a number and not an
# impression.  Reads stored ledgers only; builds no term.
set -u
cd PseudoCoupHQ/Research/op_pipeline
python3 probe83d_callee_population.py
echo "exit $?"
