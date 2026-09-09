#!/usr/bin/env bash
# t104 lane 6 -- THE POOL, before and after.
#
# Step 1 runs `pool66_run.py` UNMODIFIED so its own refusal is on the
# record: it refuses to write a pool over a member set short of the
# population it names, and 44 members are short.  That refusal is not
# worked around; what step 2 writes is a CANDIDATE that carries the
# shortfall in its own summary.
#
# Step 2 builds the same ruled merge twice over the same member set --
# once with the layer-5 texts of term66_store/ and once with those of
# term104_store/ -- so the difference between the two entry counts is
# the normalizer's and nothing else's, and answers the t100 edge
# question off pool100_edges.json.
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "[1/2] pool66_run.py, unmodified, for its own refusal"
python3 pool66_run.py
echo "pool66_run.py exit $?"
echo "[2/2] the before build, the after build, the candidate, the delta"
python3 PseudoCoupHQ/Research/op_pipeline/lanes_t104/t104_pool.py
echo "exit $?"
