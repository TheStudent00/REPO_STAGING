#!/bin/sh
# pc_manifest_role.sh -- Job 3 of the 2026-08-26 lap.
#
# Declares the probe manifests to be generator provenance
# (meta.role = "generator provenance"), then shows the updated guard
# passing them and still failing verdicts.json, the historical
# violation record.
#
# Pure data edit plus a guard run: no compiler, no solver.
set -e

D=$(dirname "$0")/..
cd "$D"

echo "== dry run first"
python3 manifest_role_lane.py --dry-run

echo
echo "== the edit"
python3 manifest_role_lane.py

echo
echo "== the guard on the manifests (expect PASS, exempt)"
python3 check_no_spelling_keys.py probe_manifest_*.json

echo
echo "== the guard on verdicts.json (expect FAIL, still)"
python3 check_no_spelling_keys.py verdicts.json || true

echo
echo "== the nesting test (expect FAIL: a manifest inside a matching artifact)"
python3 guard_nesting_test.py
