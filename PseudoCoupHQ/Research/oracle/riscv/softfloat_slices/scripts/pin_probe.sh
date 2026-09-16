#!/usr/bin/env bash
# Are the three poison pins observable?
#
# Re-emit the C emulations with the OPPOSITE reading of every don't-care
# (scripts/sfemul_altpin.h), then run the SAME SoftFloat differential test.
# Zero mismatches from both readings is what turns "we chose a value" into
# "the value cannot be seen".
#
#   usage: scripts/pin_probe.sh [rounding-mode]      (default 1)
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
BASE="$(dirname "$HERE")"
SCRATCH="${EMUL_SCRATCH:-<scratch>/emul}"
MODE="${1:-1}"
ALT="$SCRATCH/altpin"

rm -rf "$ALT"
EMUL_OUT="$ALT" EMUL_PIN=alt python3 "$HERE/emit_emulations.py" "$MODE" value \
    >/dev/null
cp "$BASE/emulations/c/sfemul.h" "$ALT/c/"
cp "$HERE/sfemul_altpin.h" "$ALT/c/"
echo "alt-pin C emitted into $ALT/c"

EMUL_C_DIR="$ALT/c" EMUL_ONLY=c python3 "$HERE/verify_emulations.py" "$MODE"
