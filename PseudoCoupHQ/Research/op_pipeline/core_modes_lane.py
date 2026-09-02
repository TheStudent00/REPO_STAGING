#!/usr/bin/env python3
"""core_modes_lane.py -- run core_modes.py's solver route in Airlock.

Why it does not run here
------------------------
Route 2 of `core_modes.py` asks z3 about every connected unit pair whose
cores differ: 3436 pairs, measured at about 0.8 seconds each, which is
roughly 45 minutes of wall clock.  The sandbox this session works in
kills a process after about two minutes, and loading the units costs 60
of those seconds, so a chunked local run would spend most of its time
re-loading.  Airlock has an hour per lane, so the pass goes there whole.

The lane carries the pass and its data gzip+base64 inside itself,
because PseudoCoupHQ is not mounted in the container.  It writes
`core_modes_<lang>.json` and `core_modes_cache.json` to `/out`.

usage:
  core_modes_lane.py --build
  core_modes_lane.py --fold     copy /out products into this directory
"""

import base64
import io
import json
import os
import shutil
import sys
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
KFC = os.path.join(os.path.dirname(HERE), "kind_fuzz_clustering")
_PROGRAMMING = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
AIRLOCK = os.path.join(_PROGRAMMING, "Airlock")

LANE = "pc_core_modes.sh"
PYVEX_PIN = "9.2.213"

LANGS = ["c", "cpp", "go", "rust", "swift"]

FROM_KFC = ["arch_read.py", "arch_sem.py"]

FROM_HERE = ["sem_anchored.py", "verdicts.py", "verdicts3.py", "z3_ext.py",
             "core_modes.py", "clusters.json"]


def strip_op_units(lang):
    """the op_units file with only the fields the DWARF check reads.

    `verdicts.load_units` calls `sem_anchored.dwarf_check(probe, lang)`,
    which reads the probe's anchor DWARF rows and the anchor mnemonics.
    Nothing else of that file is read, so nothing else travels."""
    doc = json.load(open(os.path.join(HERE, "op_units_%s.json" % lang)))
    out = {}
    for n, probe in doc["probes"].items():
        keep = {}
        for field in ("meta", "n", "symbol", "symbol_exact"):
            if field in probe:
                keep[field] = probe[field]
        anchor = probe.get("anchor")
        if isinstance(anchor, dict):
            slim = {}
            for field in ("dwarf", "mnem", "ok", "why"):
                if field in anchor:
                    slim[field] = anchor[field]
            keep["anchor"] = slim
        for field in probe:
            if field in keep:
                continue
            if field in ("ship",):
                continue
            keep[field] = probe[field]
        out[n] = keep
    doc["probes"] = out
    return json.dumps(doc).encode()


def payload():
    buf = io.BytesIO()
    tar = tarfile.open(fileobj=buf, mode="w:gz")

    def add_bytes(data, name):
        info = tarfile.TarInfo(name)
        info.size = len(data)
        info.mode = 0o644
        tar.addfile(info, io.BytesIO(data))

    for name in FROM_KFC:
        add_bytes(open(os.path.join(KFC, name), "rb").read(), name)
    for name in FROM_HERE:
        add_bytes(open(os.path.join(HERE, name), "rb").read(), name)
    for lang in LANGS:
        name = "sem_anchored_%s.json" % lang
        add_bytes(open(os.path.join(HERE, name), "rb").read(), name)
        # the op_units file travels WHOLE.  It could be stripped to the
        # fields the DWARF check reads, and the earlier tier-1 lane did
        # strip it; here it is not, so that nothing downstream can be
        # different because a field was missing.
        name = "op_units_%s.json" % lang
        add_bytes(open(os.path.join(HERE, name), "rb").read(), name)
    tar.close()
    return base64.b64encode(buf.getvalue()).decode()


HEAD = """#!/bin/sh
# pc_core_modes -- the core+modes representation, solver route included.
#
# core_modes.py re-emits every accepted ship unit as a CORE (the
# normal-path lifted form) and a list of MODES.  Route 1 reads the
# existing guard machinery.  Route 2 asks z3 where two connected units
# with different cores disagree, and offers the disagreement a small set
# of simple predicates over the anchored inputs.  Route 2 is the
# expensive half and is why this runs here.
#
# PseudoCoupHQ is not mounted in the container, so the pass and its data
# travel INSIDE this script, gzip+base64.
set -u
export HOME=/work
ROOT=/work/pc_core_modes
echo "=== op_pipeline -- core+modes ==="
date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ
if ! python3 --version >/dev/null 2>&1; then
  echo "!! REFUSING TO START: python3 is not runnable in this container."
  exit 4
fi
python3 --version
rm -rf "$ROOT"; mkdir -p "$ROOT"
df -Pm /work | awk 'NR==2{print "free /work: " $4 " MB"}'

echo "-- installing the solver and the lifter"
# the lifter is PINNED to the version verdicts3.json was produced with.
python3 -m pip install --quiet --disable-pip-version-check \\
    z3-solver pyvex==%(pyvex)s archinfo==%(pyvex)s capstone 2>&1 | tail -5
if ! python3 -c "import z3, pyvex, archinfo, capstone" 2>&1; then
  echo "!! REFUSING TO CONTINUE: a dependency did not import."
  exit 4
fi
python3 -c "import z3, pyvex, archinfo, capstone; \\
print('z3', z3.get_version_string(), '/ pyvex', pyvex.__version__, \\
'/ archinfo', archinfo.__version__, '/ capstone', capstone.__version__)"

echo "-- unpacking"
cd "$ROOT"
sed -n '/^__PAYLOAD__$/,$p' "$0" | tail -n +2 | base64 -d > payload.tgz
md5sum payload.tgz
tar xzf payload.tgz --no-same-owner --no-same-permissions
rm -f payload.tgz
ls -l | awk '{print "   " $5 "  " $9}'

echo "-- the pass"
# the route-2 cache lives in /out, which survives the lane.  A lane that
# is killed at the hour leaves its answers there and a re-dropped lane
# resumes from them.
export CORE_MODES_CACHE_DIR=/out
python3 -u core_modes.py
rc=$?
echo "exit=$rc"
cp -v core_modes_*.json /out/ 2>&1
date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ
exit $rc
__PAYLOAD__
"""


def build():
    blob = payload()
    lines = []
    for i in range(0, len(blob), 76):
        lines.append(blob[i:i + 76])
    text = HEAD % dict(pyvex=PYVEX_PIN) + "\n".join(lines) + "\n"
    path = os.path.join(AIRLOCK, "agent", "drop", LANE)
    open(path, "w").write(text)
    os.chmod(path, 0o755)
    print("lane %s (%d bytes)" % (path, len(text)))
    return 0


def fold():
    out = os.path.join(AIRLOCK, "agent", "out")
    moved = 0
    for lang in LANGS:
        name = "core_modes_%s.json" % lang
        src = os.path.join(out, name)
        if not os.path.exists(src):
            print("missing %s" % name)
            continue
        shutil.copy(src, os.path.join(HERE, name))
        moved += 1
        print("folded %s" % name)
    src = os.path.join(out, "core_modes_cache.json")
    if os.path.exists(src):
        shutil.copy(src, os.path.join(HERE, "core_modes_cache.json"))
        print("folded core_modes_cache.json")
    return 0 if moved == len(LANGS) else 1


def main(argv):
    if "--build" in argv:
        return build()
    if "--fold" in argv:
        return fold()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
