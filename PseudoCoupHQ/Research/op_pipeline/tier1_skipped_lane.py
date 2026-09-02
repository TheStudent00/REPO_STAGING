#!/usr/bin/env python3
"""tier1_skipped_lane.py -- build the Airlock lane that finishes the
solver work verdicts3.py skipped, and fold its answer back.

What was skipped, and why
-------------------------
`verdicts3.py` carries a function `skip_tier1`.  It refuses to run the
WIDER z3 translation (`z3_ext.z3_pair_ext`) on any pair whose operand
type pair mentions `f32` or `f64`.  The reason it states is wall clock:
the sandbox that ran it kills a process after about three minutes, and
z3's FP theory spends seconds per query.  Each such pair kept its
tier-0 verdict and carries the field `tier1_skipped` saying so.

Counted in verdicts3.json:

  2280   pair INSTANCES carrying `tier1_skipped` (one unit pair sitting
         in several rows is counted once per row)
  1302   DISTINCT unit pairs behind those instances

The brief said 2,280 pairs.  That is the instance count.  The solver is
asked once per distinct pair, so the work is 1302 queries.

What this file does
-------------------
1. `--build` writes `agent/drop/pc_tier1_skipped.sh` into Airlock: a
   lane script carrying, gzip+base64 inside itself, the pass, the
   lifter, and a SLIM record of only the units those 1302 pairs need.
   The lane installs z3-solver, pyvex, archinfo and capstone, pins the
   lifter to the version verdicts3.json was produced with, and asks
   every pair with a 20-second solver cap.
2. `--fold` reads the lane's product out of `agent/out/` and writes
   `verdicts3b.json`: verdicts3.json with those pairs re-decided and
   everything else carried unchanged.

No operator token is used anywhere in the choosing: the pair list is
taken from verdicts3.json's own rows, which were built from machine-form
evidence.  The token rides along on each unit as a display label only.

usage:
  tier1_skipped_lane.py --build
  tier1_skipped_lane.py --fold
"""

import base64
import gzip
import io
import json
import os
import sys
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
KFC = os.path.join(os.path.dirname(HERE), "kind_fuzz_clustering")
# Airlock sits beside PseudoCoupHQ in the same programming tree.  It is
# located RELATIVE to this file rather than through $HOME, because the
# sandbox this is developed in mounts the tree somewhere else.
_PROGRAMMING = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
AIRLOCK = os.path.join(_PROGRAMMING, "Airlock")

LANE = "pc_tier1_skipped.sh"

# The lifter verdicts3.json was produced with.  Pinned so the answer
# folded back was computed by the same model of the machine as the
# answers it joins.
PYVEX_PIN = "9.2.213"


def skipped_pairs():
    """(pairs, units) -- the distinct unit pairs verdicts3.py skipped,
    and the slim record of every unit they mention."""
    doc = json.load(open(os.path.join(HERE, "verdicts3.json")))
    pairs = {}
    instances = 0
    for row in doc["rows"]:
        for p in row["pairs"]:
            if not p.get("tier1_skipped"):
                continue
            instances += 1
            key = (p["left"], p["right"])
            if key in pairs:
                continue
            pairs[key] = dict(left=p["left"], right=p["right"],
                              type_pair=p.get("pair_type_pair",
                                              row["type_pair"]))
    return list(pairs.values()), instances


def unit_index():
    index = {}
    for lang in ("c", "cpp", "go", "rust", "swift"):
        path = os.path.join(HERE, "sem_anchored_%s.json" % lang)
        doc = json.load(open(path))
        for n, u in doc["units"].items():
            index["%s/op_%s" % (lang, n)] = dict(
                lang=lang, n=n, meta=u["meta"], bytes=u["bytes"],
                mnem=u["mnem"], sem=u["sem"])
    return index


def slim_units(pairs, index):
    want = set()
    for p in pairs:
        want.add(p["left"])
        want.add(p["right"])
    out = {}
    for label in sorted(want):
        if label not in index:
            continue
        out[label] = index[label]
    return out


def payload(pairs, units):
    """the tar.gz the lane unpacks: the two imported modules the pass
    needs, plus the data."""
    buf = io.BytesIO()
    tar = tarfile.open(fileobj=buf, mode="w:gz")

    def add_file(path, name):
        data = open(path, "rb").read()
        info = tarfile.TarInfo(name)
        info.size = len(data)
        info.mode = 0o644
        tar.addfile(info, io.BytesIO(data))

    def add_bytes(data, name):
        info = tarfile.TarInfo(name)
        info.size = len(data)
        info.mode = 0o644
        tar.addfile(info, io.BytesIO(data))

    for name in ("arch_read.py", "arch_sem.py"):
        add_file(os.path.join(KFC, name), name)
    for name in ("sem_anchored.py", "verdicts.py", "z3_ext.py"):
        add_file(os.path.join(HERE, name), name)
    add_bytes(json.dumps(dict(pairs=pairs)).encode(), "pairs.json")
    add_bytes(json.dumps(units).encode(), "units.json")
    add_bytes(RUNNER.encode(), "run_skipped.py")
    tar.close()
    return base64.b64encode(buf.getvalue()).decode()


RUNNER = '''#!/usr/bin/env python3
"""run_skipped.py -- ask the wider translation about every pair
verdicts3.py skipped.  Written by tier1_skipped_lane.py; not
hand-edited.

The deciding code is z3_ext.z3_pair_ext, imported unchanged.  The only
settings this file makes are the solver cap and the resume point.
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import z3_ext as X
import arch_sem as AS
import z3

X.Z3_TIMEOUT_MS = 20000

OUT = "/out/verdicts3b_pairs.json"


def load_done():
    """the pairs an earlier chunk already answered.  The lane is
    resumable because a long run may be cut off; the file is the resume
    point and it changes no answer."""
    if not os.path.exists(OUT):
        return {}
    doc = json.load(open(OUT))
    out = {}
    for row in doc["pairs"]:
        out[(row["left"], row["right"])] = row
    return out


def save(done, meta):
    doc = dict(meta=meta, pairs=list(done.values()))
    tmp = OUT + ".tmp"
    fh = open(tmp, "w")
    json.dump(doc, fh)
    fh.close()
    os.replace(tmp, OUT)


def main():
    started = time.time()
    pairs = json.load(open("pairs.json"))["pairs"]
    units = json.load(open("units.json"))
    done = load_done()
    total = len(pairs)
    print("pairs to decide: %d   already answered: %d"
          % (total, len(done)))
    print("solver cap: %d ms" % X.Z3_TIMEOUT_MS)
    print("lifter: %s" % AS.LIFTER_ID)
    print("z3: %s" % z3.get_version_string())
    sys.stdout.flush()

    seen = 0
    fresh = 0
    tally = {}
    for p in pairs:
        seen += 1
        key = (p["left"], p["right"])
        if key in done:
            continue
        left = units.get(p["left"])
        right = units.get(p["right"])
        if left is None or right is None:
            verdict = "UNDECIDED"
            detail = "a unit of the pair is not in the accepted set"
            extra = {}
        else:
            try:
                verdict, detail, extra = X.z3_pair_ext(left, right, False)
            except Exception as exc:                       # noqa: BLE001
                verdict = "UNDECIDED"
                detail = ("the wider translation raised: %s: %s"
                          % (type(exc).__name__, exc))
                extra = {}
        row = dict(left=p["left"], right=p["right"],
                   type_pair=p["type_pair"], verdict=verdict,
                   detail=detail)
        for k, v in (extra or {}).items():
            row[k] = v
        done[key] = row
        fresh += 1
        tally[verdict] = tally.get(verdict, 0) + 1
        if fresh % 50 == 0:
            save(done, dict(elapsed_s=int(time.time() - started)))
            print("[progress] %d/%d answered=%d elapsed=%ds tally=%s"
                  % (seen, total, len(done),
                     int(time.time() - started), json.dumps(tally)))
            sys.stdout.flush()

    save(done, dict(elapsed_s=int(time.time() - started),
                    z3=z3.get_version_string(), lifter=AS.LIFTER_ID,
                    solver_cap_ms=X.Z3_TIMEOUT_MS, total=total))
    print("[progress] %d/%d answered=%d elapsed=%ds tally=%s"
          % (seen, total, len(done), int(time.time() - started),
             json.dumps(tally)))
    final = {}
    for row in done.values():
        final[row["verdict"]] = final.get(row["verdict"], 0) + 1
    print("done in %ds: %s" % (int(time.time() - started),
                               json.dumps(final)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


HEAD = """#!/bin/sh
# pc_tier1_skipped -- the solver work verdicts3.py skipped.
#
# verdicts3.py refused the wider z3 translation on every pair whose
# operands are floating point, because the sandbox it ran in kills a
# process after about three minutes.  This lane has an hour and runs
# them.  %(distinct)d distinct unit pairs (%(instances)d row instances).
#
# PseudoCoupHQ is not mounted in the container, so the pass and the data
# travel INSIDE this script, gzip+base64.  The unit records are slim:
# only the %(unitcount)d units these pairs mention, and only the fields
# the pass reads (meta, bytes, mnem, sem).
set -u
export HOME=/work
ROOT=/work/pc_tier1_skipped
echo "=== op_pipeline -- the skipped pairs, full budget ==="
date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ
if ! python3 --version >/dev/null 2>&1; then
  echo "!! REFUSING TO START: python3 is not runnable in this container."
  exit 4
fi
python3 --version
rm -rf "$ROOT"; mkdir -p "$ROOT"
df -Pm /work | awk 'NR==2{print "free /work: " $4 " MB"}'

echo "-- installing the solver and the lifter"
# the lifter is PINNED to the version verdicts3.json was produced with,
# so the answers folded together were computed by one model of the
# machine and not by two.
python3 -m pip install --quiet --disable-pip-version-check \\
    z3-solver pyvex==%(pyvex)s archinfo==%(pyvex)s capstone 2>&1 | tail -5
if ! python3 -c "import z3, pyvex, archinfo, capstone" 2>&1; then
  echo "!! REFUSING TO CONTINUE: a dependency did not import."
  exit 4
fi
python3 -c "import z3, pyvex, archinfo, capstone; \\
print('z3', z3.get_version_string(), '/ pyvex', pyvex.__version__, \\
'/ archinfo', archinfo.__version__, '/ capstone', capstone.__version__)"

echo "-- unpacking the embedded pass and its data"
cd "$ROOT"
sed -n '/^__PAYLOAD__$/,$p' "$0" | tail -n +2 | base64 -d > payload.tgz
md5sum payload.tgz
tar xzf payload.tgz --no-same-owner --no-same-permissions
rm -f payload.tgz
ls -l | awk '{print "   " $5 "  " $9}'

echo "-- the translation's own guard tests, before any pair is judged"
python3 z3_ext.py --selfcheck
rc=$?
if [ $rc -ne 0 ]; then
  echo "!! REFUSING TO CONTINUE: the FP translation failed its own guards."
  exit 5
fi

echo "-- the pass"
python3 -u run_skipped.py
rc=$?
echo "exit=$rc"
ls -l /out/verdicts3b_pairs.json
date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ
exit $rc
__PAYLOAD__
"""


def build():
    pairs, instances = skipped_pairs()
    index = unit_index()
    units = slim_units(pairs, index)
    blob = payload(pairs, units)
    head = HEAD % dict(distinct=len(pairs), instances=instances,
                       unitcount=len(units), pyvex=PYVEX_PIN)
    lines = []
    for i in range(0, len(blob), 76):
        lines.append(blob[i:i + 76])
    text = head + "\n".join(lines) + "\n"
    path = os.path.join(AIRLOCK, "agent", "drop", LANE)
    open(path, "w").write(text)
    os.chmod(path, 0o755)
    print("distinct pairs   %d" % len(pairs))
    print("row instances    %d" % instances)
    print("units embedded   %d" % len(units))
    print("lane             %s (%d bytes)" % (path, len(text)))
    return 0


# ------------------------------------------------------------- folding

def reason_key(detail):
    """the tool's own words, cut to a countable head."""
    text = str(detail or "")
    for head in ("z3 was not asked: ", "the lift was refused: "):
        if text.startswith(head):
            return text[:110]
    return text[:110]


def fold():
    doc = json.load(open(os.path.join(HERE, "verdicts3.json")))
    path = os.path.join(AIRLOCK, "agent", "out", "verdicts3b_pairs.json")
    answer = json.load(open(path))
    fresh = {}
    for row in answer["pairs"]:
        fresh[(row["left"], row["right"])] = row

    before = {}
    after = {}
    before_reasons = {}
    after_reasons = {}
    touched = 0
    moved = {}
    for r in doc["rows"]:
        for p in r["pairs"]:
            before[p["verdict"]] = before.get(p["verdict"], 0) + 1
            if p["verdict"] == "UNDECIDED":
                k = reason_key(p.get("detail"))
                before_reasons[k] = before_reasons.get(k, 0) + 1
            key = (p["left"], p["right"])
            got = fresh.get(key)
            if got is not None and p.get("tier1_skipped"):
                was = p["verdict"]
                p["tier0_verdict"] = was
                p["tier0_detail"] = p.get("detail")
                p["tier1"] = True
                p["tier1_reason"] = ("the skipped floating-point pair, "
                                     "asked in Airlock with a 20-second "
                                     "solver cap")
                p.pop("tier1_skipped", None)
                p["verdict"] = got["verdict"]
                p["ground"] = "z3 over the two lifted forms (tier 1)"
                p["detail"] = got["detail"]
                for k, v in got.items():
                    if k in ("left", "right", "verdict", "detail",
                             "type_pair"):
                        continue
                    p[k] = v
                touched += 1
                if got["verdict"] != was:
                    moved[got["verdict"]] = moved.get(got["verdict"], 0) + 1
            after[p["verdict"]] = after.get(p["verdict"], 0) + 1
            if p["verdict"] == "UNDECIDED":
                k = reason_key(p.get("detail"))
                after_reasons[k] = after_reasons.get(k, 0) + 1

    doc["tally"] = after
    doc["tier1_skipped_finished"] = dict(
        distinct_pairs_asked=len(fresh),
        row_instances_replaced=touched,
        moved_to=moved,
        undecided_before=before.get("UNDECIDED", 0),
        undecided_after=after.get("UNDECIDED", 0),
        undecided_reasons_before=before_reasons,
        undecided_reasons_after=after_reasons,
        lane=LANE,
        solver_cap_ms=answer.get("meta", {}).get("solver_cap_ms"),
        z3=answer.get("meta", {}).get("z3"),
        lifter=answer.get("meta", {}).get("lifter"),
    )
    out = os.path.join(HERE, "verdicts3b.json")
    json.dump(doc, open(out, "w"), indent=1)
    print("wrote %s" % out)
    print("row instances replaced %d" % touched)
    print("before %s" % before)
    print("after  %s" % after)
    return 0


def main(argv):
    if "--build" in argv:
        return build()
    if "--fold" in argv:
        return fold()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
