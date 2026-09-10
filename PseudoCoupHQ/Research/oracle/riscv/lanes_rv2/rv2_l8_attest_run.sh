#!/usr/bin/env bash
# rv2 lane 8 -- THE ATTESTATION on riscv64: a 500-probe sample of the c
# corpus and every go probe, each compiled for riscv64 at the corpus's own
# ship flags, carved at its function symbol, walked by the RISC-V
# reference; the cells the carved bodies spell, and the SINGLETONS -- the
# probes whose whole riscv64 body is one computing instruction, which are
# what the loop's primitive lookup needs on this architecture.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
export HOME=/work
export GOCACHE=/work/rv2gocache GOPATH=/work/rv2gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv2attest
total=3

echo "[1/$total] how many go units the corpus's stores actually spell"
python3 - <<'PY'
import json, os, collections
op = "PseudoCoupHQ/Research/op_pipeline"
for lang in ("c", "go"):
    m = json.load(open(os.path.join(op, "probe_manifest_%s.json" % lang)))
    u = json.load(open(os.path.join(op, "op_units_%s.json" % lang)))
    ship = 0
    for n, rec in u["probes"].items():
        if (rec.get("ship") or {}).get("mnem"):
            ship += 1
    print("   %s: %d probes in the manifest, %d with an x86 ship body"
          % (lang, len(m["probes"]), ship))
store = os.path.join(op, "canon40_regen_store")
c = collections.Counter()
for name in sorted(os.listdir(store)):
    if not name.endswith(".json"):
        continue
    doc = json.load(open(os.path.join(store, name)))
    for uid in (doc.get("units") or {}):
        c[uid.split("/")[0]] += 1
print("   canon40_regen_store, units by language: %s"
      % json.dumps(dict(c), sort_keys=True))
PY

echo "[2/$total] the sweep: 500 c probes and every go probe"
python3 $RV/rv_attest.py run $OP $RV/attest_rv /work/rv2attest 500 all

echo "[3/$total] the spelling guard"
python3 $OP/check_no_spelling_keys.py $RV/attest_rv.json
echo "guard rc=$?"
echo "--- lane finished"
