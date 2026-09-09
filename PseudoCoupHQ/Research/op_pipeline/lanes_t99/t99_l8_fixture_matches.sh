#!/usr/bin/env bash
# t99 lane 8 -- item B proof (c).  The SAME fixture shape, but the
# claim cats a file that DOES exist inside this instance.  Must score
# MATCHES.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline

echo "reachable fixture content, task 99" > /tmp/t99_fixture_reachable.txt

cat > /tmp/t99_fixture_c.md <<'FIXTURE'
# fixture log -- item B proof (c), reachable path

## a claim that cats a file this instance DOES have

```
$ cat /tmp/t99_fixture_reachable.txt
reachable fixture content, task 99
```
FIXTURE

echo "======== [1/1] check_conventions_log_claims.py --verify over the fixture ========"
python3 check_conventions_log_claims.py --verify \
  --timeout 30 \
  --json /out/t99_l8_fixture_matches.json \
  /tmp/t99_fixture_c.md
rc=$?
echo "verifier exit ${rc}"
exit ${rc}
