#!/usr/bin/env bash
set -u
echo "[1/2] git?"
cd PseudoCoupHQ
which git && git log --oneline -3
echo "[2/2] pwd/ls"
pwd
echo done
