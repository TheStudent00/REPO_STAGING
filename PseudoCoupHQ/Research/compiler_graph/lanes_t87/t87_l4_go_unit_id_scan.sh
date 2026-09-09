#!/usr/bin/env bash
# t87 lane 4 — SURVEY ONLY. A decisive text scan: which artifact in
# op_pipeline mentions go unit ids of the form `go/op_<n>` at all, and
# how many distinct ones. This settles whether go's arch-unit
# population really is 107 of the 590 diaried probes, or whether a
# fuller machine form is on disk under a name lanes 2 and 3 did not try.
#
# THE SPELLING BAN, ABSOLUTE (the owner, 2026-08-25). Nothing here reads an
# operator field; the scan is over unit ids only.
set -u
say() { echo; echo "======== $* ========"; }
cd PseudoCoupHQ/Research/op_pipeline

say "[1/3] files that mention a go unit id"
grep -l '"go/op_' *.json 2>/dev/null | head -40

say "[2/3] distinct go unit ids per such file"
for f in $(grep -l '"go/op_' *.json 2>/dev/null); do
  n=$(grep -o '"go/op_[0-9]*"' "$f" | sort -u | wc -l)
  printf "   %-40s %6d distinct go/op_ ids\n" "$f" "$n"
done

say "[3/3] and how many go probes the manifest declares"
python3 - <<'PY'
import json
doc = json.load(open('PseudoCoupHQ/Research/op_pipeline/'
                     'probe_manifest2_go.json'))
print("   probe_manifest2_go.json count : %s" % doc.get("count"))
probes = doc.get("probes")
print("   probes entries                : %s" % (len(probes) if hasattr(probes, '__len__') else '-'))
doc1 = json.load(open('PseudoCoupHQ/Research/op_pipeline/'
                      'probe_manifest_go.json'))
p1 = doc1.get("probes")
print("   probe_manifest_go.json probes : %s" % (len(p1) if hasattr(p1, '__len__') else '-'))
PY
echo "DONE t87_l4"
