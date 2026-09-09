#!/usr/bin/env bash
# t98 lane 5 -- which row keys the pane drew as UNEXPLAINED, and at which
# moment.  Lane 4 found 9 unexplained rows at two commits of 2026-09-03
# and none at any other; this names the keys, so an earlier generation's
# summary field can be given its own record rather than left showing the
# marker.
set -u
cd PseudoCoupHQ/Research/op_pipeline
( ulimit -v 6291456 ; python3 t98_render_check.py keys 14 )
echo "-- exit $?"
