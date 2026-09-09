#!/usr/bin/env bash
set -u
cd PseudoCoupHQ
echo "[1/3] git available?"
which git && git --version
echo "[2/3] git log in sandbox"
git log --format="COMMIT %H %ad" --date=iso -1 -- Research/oracle/cross_construction/emulation/synthesis/synthesize.py
echo "[3/3] report file present?"
ls -la Research/oracle/cross_construction/emulation/synthesis/synthesis_report.md
