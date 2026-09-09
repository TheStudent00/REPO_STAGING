#!/usr/bin/env bash
# t101 lane 8 -- re-quote fold.py's row constructor without the docstring
# line. Lane 7's verify scored the first quotation NOT_RERUNNABLE with
# cause `output_annotated`, because fold.py's own docstring contains an
# arrow (`->`) and the verifier reads an arrow in a paste as a
# hand-written gloss. The lines that actually carry the claim -- the two
# `dict(...)` calls that build a row -- are 82 to 91 and carry no arrow.
set -u
cd /projects/PseudoCoupHQ
echo "======== [1/1] fold.py lines 82-91, the row constructor ========"
echo "\$ sed -n '82,91p' /projects/PseudoCoupHQ/Research/op_pipeline/fold.py"
sed -n '82,91p' /projects/PseudoCoupHQ/Research/op_pipeline/fold.py
echo "--------8<--------"
exit 0
