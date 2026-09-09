#!/usr/bin/env bash
# t97 lane 7 -- the resume state written from the STORE itself, and THE
# CONTROL that answers the other half of the owner's rule.
#
# THE CONTROL asks: does the LARGER budget change an answer the
# ORDINARY budget already produced?  Every 100th record in
# term66_store is re-transcribed and re-gated at the pass-2 budget and
# compared FIELD FOR FIELD against what is stored.  The sample crosses
# both halves of the store -- the 10 inputs walked on the host before
# this round, and the 322 walked here -- so the store's own
# inhomogeneity (log_189 section 7.1) is measured rather than assumed.
#
# THE BUDGET: 4096 MB and 1800 s per unit, one slice.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "======== [1/2] finalize -- term66_state.json written from the store ========"
python3 term97_walk.py finalize
echo "exit $?"
echo
echo "======== [2/2] the control ========"
python3 term97_walk.py control 4096 1800 100
echo "exit $?"
