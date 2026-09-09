#!/usr/bin/env bash
# t98 lane 12 -- the one claim log_203 made in prose with nothing beside
# it, given a command that reproduces it: what log_202 says the 44 units
# short of the term store actually are.
set -u
cd /projects/PseudoCoupHQ
echo
echo "\$ grep -c \"does not converge\" DevComms/log_202_task97_term_pool_canon40.md"
grep -c "does not converge" DevComms/log_202_task97_term_pool_canon40.md
echo
echo "\$ grep -n \"does not converge for 44 of the 30,324\" DevComms/log_202_task97_term_pool_canon40.md"
grep -n "does not converge for 44 of the 30,324" DevComms/log_202_task97_term_pool_canon40.md
