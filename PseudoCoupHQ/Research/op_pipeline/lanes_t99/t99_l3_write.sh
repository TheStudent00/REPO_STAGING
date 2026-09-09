#!/usr/bin/env bash
# t99 lane 3 -- item A write.  Masked hash of the store BEFORE, then
# term99_reason.py --write, then masked hash AFTER, then the
# reason-is-None count before/after.  The mask covers only
# reason/reason_source on NO_TERM records -- every other byte of every
# other record must hash identically.
set -u
cd PseudoCoupHQ/Research/op_pipeline

hash_masked () {
python3 - <<'PY'
import glob, hashlib, json
h = hashlib.sha256()
for f in sorted(glob.glob("term66_store/*.json")):
    d = json.load(open(f))
    for uid in sorted(d.get("units", {})):
        rec = dict(d["units"][uid])
        if rec.get("term_state") == "NO_TERM":
            rec["reason"] = None
            rec["reason_source"] = None
        h.update(f.encode())
        h.update(uid.encode())
        h.update(json.dumps(rec, sort_keys=True).encode())
print(h.hexdigest())
PY
}

count_none () {
python3 - <<'PY'
import glob, json
n = 0
for f in glob.glob("term66_store/*.json"):
    d = json.load(open(f))
    for rec in d.get("units", {}).values():
        if rec.get("term_state") == "NO_TERM" and rec.get("reason") is None:
            n += 1
print(n)
PY
}

echo "======== [1/4] masked hash BEFORE ========"
BEFORE=$(hash_masked)
echo "$BEFORE"
echo "======== [2/4] reason-is-None count BEFORE (expect 485) ========"
count_none

echo "======== [3/4] term99_reason.py --write ========"
python3 term99_reason.py --write
rc=$?
echo "exit ${rc}"

echo "======== [4/4] masked hash AFTER, reason-is-None count AFTER (expect 0) ========"
AFTER=$(hash_masked)
echo "$AFTER"
count_none

echo
if [ "$BEFORE" = "$AFTER" ]; then
  echo "MASKED HASH: EQUAL -- no field but reason/reason_source moved"
else
  echo "MASKED HASH: DIFFERS -- something besides reason/reason_source moved"
fi
exit ${rc}
