#!/bin/bash
set -e

cd /projects/PseudoCoupHQ/Research/op_pipeline

# Run the anchor step (step 4+5) for java
python3 sem_anchored.py --anchor-report
python3 sem_anchored.py

# Run the spill step (step 5.1)
python3 sem_anchored_spill.py

# Run the matching step (step 6+7)
python3 tree_match2.py

echo "Pipeline complete for Java JIT units."
