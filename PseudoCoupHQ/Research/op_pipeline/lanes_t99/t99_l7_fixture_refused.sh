#!/usr/bin/env bash
# t99 lane 7 -- item B proof (b).  A fixture log, written under /tmp
# INSIDE this lane, whose one claim cats a /logs path that does not
# exist.  Must score REFUSED with reason log_unreachable, never
# DIFFERS.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline

cat > /tmp/t99_fixture_b.md <<'FIXTURE'
# fixture log -- item B proof (b), unreachable log path

## a claim that cats a log file this instance does not have

```
$ cat /logs/does_not_exist.log
some pasted output that will never be compared, because the path
itself is unreachable from this instance
```
FIXTURE

echo "======== [1/1] check_conventions_log_claims.py --verify over the fixture ========"
python3 check_conventions_log_claims.py --verify \
  --timeout 30 \
  --json /out/t99_l7_fixture_refused.json \
  /tmp/t99_fixture_b.md
rc=$?
echo "verifier exit ${rc}"
exit ${rc}
