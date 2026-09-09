#!/usr/bin/env bash
# t98 lane 10 -- how pane 5's rows split between its two halves, read off
# the rendered page at its own half marker rather than counted by hand.
set -u
cd /projects/PseudoCoupHQ
echo
echo "\$ python3 Research/op_pipeline/t98_render_check.py split"
python3 Research/op_pipeline/t98_render_check.py split
