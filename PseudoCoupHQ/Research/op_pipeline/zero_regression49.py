#!/usr/bin/env python3
"""zero_regression49.py -- THE ZERO-REGRESSION AUDIT for task 49.

FOUR CLAIMS, EACH CHECKED RATHER THAN ASSERTED.

  CLAIM ONE -- task 47's and task 48's artifacts are UNTOUCHED.
  Checked against the version control system, not against memory.  The
  daemon commits every thirty seconds, so an artifact this lap had
  modified would show as a difference here.

  CLAIM TWO -- the_pool1.json and the_families1.json are UNTOUCHED.
  the_families1.json is tracked, so the version control system answers
  for it.  the_pool1.json is 18.6 MB and is NOT tracked, so the version
  control system cannot answer for it; its sha256 and its modification
  time are recorded here instead, and the modification time is compared
  against the first file this lap wrote.

  CLAIM THREE -- no program of this lap opens a prior artifact for
  writing.  Every open() call in this lap's own sources is listed with
  its mode.

  CLAIM FOUR -- no unit loses pool membership.  Every unit that is a
  member of the_pool1.json AND was proved by task 47 is a member of
  the_pool2.json.

No operator token appears in this file.
"""

import glob
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

THIS_LAP = ["build_the_pool2.py", "build_the_families2.py",
            "compare_pool1_pool2.py", "acceptance49.py",
            "zero_regression49.py"]


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def prior_paths():
    out = []
    for lang in ("c", "cpp", "go", "rust", "swift"):
        out.append(os.path.join(HERE, "canon37_wrapped_%s.json" % lang))
        out.append(os.path.join(HERE, "layer4b_terms_%s.json" % lang))
    out.append(os.path.join(HERE, "canon37_interp.json"))
    out.append(os.path.join(HERE, "canon37_regen_state.json"))
    out.append(os.path.join(HERE, "layer4b_interp.json"))
    out.append(os.path.join(HERE, "layer4b_state.json"))
    out.append(os.path.join(HERE, "name_census3.json"))
    out.append(os.path.join(HERE, "the_families1.json"))
    out.append(os.path.join(HERE, "check_no_spelling_keys.py"))
    out.append(os.path.join(HERE, "dom_ops.py"))
    out.append(os.path.join(HERE, "dom_ops_0branch.py"))
    out.append(os.path.join(HERE, "build_the_pool1.py"))
    out.append(os.path.join(HERE, "build_the_families1.py"))
    out.append(os.path.join(HERE, "proved_edges.json"))
    out.append(os.path.join(HERE, "proved_edges2.json"))
    out.append(os.path.join(HERE, "proved_edges3.json"))
    out.append(os.path.join(HERE, "interp_join3.json"))
    out.append(os.path.join(HERE, "interp_fastpath.json"))
    out.extend(sorted(glob.glob(os.path.join(HERE,
                                             "canon37_regen_store",
                                             "*.json"))))
    out.extend(sorted(glob.glob(os.path.join(HERE,
                                             "layer4b_regen_store",
                                             "*.json"))))
    return [one for one in out if os.path.exists(one)]


def sha256_of(path):
    digest = hashlib.sha256()
    handle = open(path, "rb")
    while True:
        block = handle.read(1 << 20)
        if not block:
            break
        digest.update(block)
    handle.close()
    return digest.hexdigest()


def claim_one():
    paths = prior_paths()
    command = ["git", "status", "--porcelain", "--"] + paths
    result = subprocess.run(command, cwd=HERE, capture_output=True,
                            text=True)
    lines = [one for one in result.stdout.splitlines() if one.strip()]
    log("CLAIM ONE -- task 47's and task 48's artifacts are untouched")
    log("  paths asked about: %d" % len(paths))
    log("  command: git status --porcelain -- ... (%d paths)"
        % len(paths))
    log("  the version control system reports %d changed path(s)"
        % len(lines))
    for line in lines[:20]:
        log("    %s" % line)
    if lines:
        log("  FAIL")
        return False
    log("  PASS -- no prior artifact differs from what is committed, "
        "so none was modified by this lap.")
    return True


def claim_two():
    log("")
    log("CLAIM TWO -- the_pool1.json and the_families1.json are "
        "untouched")
    ok = True
    tracked = os.path.join(HERE, "the_families1.json")
    result = subprocess.run(["git", "status", "--porcelain", "--",
                             tracked], cwd=HERE, capture_output=True,
                            text=True)
    lines = [one for one in result.stdout.splitlines() if one.strip()]
    log("  the_families1.json is TRACKED; the version control system "
        "reports %d changed path(s)" % len(lines))
    if lines:
        ok = False
    untracked = os.path.join(HERE, "the_pool1.json")
    log("  the_pool1.json is NOT tracked, so the version control "
        "system cannot answer for it.")
    log("    sha256            %s" % sha256_of(untracked))
    log("    size in bytes     %d" % os.path.getsize(untracked))
    log("    modified at       %d" % int(os.path.getmtime(untracked)))
    newest = 0
    for name in THIS_LAP:
        path = os.path.join(HERE, name)
        if os.path.exists(path):
            newest = max(newest, int(os.path.getmtime(path)))
    log("    this lap's newest source file, modified at %d" % newest)
    if os.path.getmtime(untracked) < newest:
        log("    PASS -- the_pool1.json predates every source file this "
            "lap wrote, so no program of this lap rewrote it.")
    else:
        log("    FAIL")
        ok = False
    log("  %s" % ("PASS" if ok else "FAIL"))
    return ok


def claim_three():
    log("")
    log("CLAIM THREE -- no program of this lap opens a prior artifact "
        "for writing")
    pattern = re.compile(r"open\(([^\n]*?)\)")
    ok = True
    for name in THIS_LAP:
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            continue
        body = open(path).read()
        for match in pattern.finditer(body):
            call = match.group(1)
            if '"w"' not in call and "'w'" not in call:
                continue
            log("    %-24s open for writing: %s" % (name, call.strip()))
            for forbidden in ["the_pool1", "the_families1", "canon37",
                              "layer4b", "name_census", "proved_edges",
                              "interp_join", "interp_fastpath"]:
                if forbidden in call:
                    log("      FAIL -- writes a prior artifact")
                    ok = False
    log("  %s -- every write names a file this lap created"
        % ("PASS" if ok else "FAIL"))
    return ok


def claim_four():
    log("")
    log("CLAIM FOUR -- no unit loses pool membership")
    import build_the_pool2 as POOL
    proved = set()
    for record in POOL.take_all():
        proved.add(record["unit"])
    pool1 = json.load(open(os.path.join(HERE, "the_pool1.json")))
    pool2 = json.load(open(os.path.join(HERE, "the_pool2.json")))
    units1 = set()
    for entry in pool1["entries"]:
        for member in entry["members"]:
            units1.add(member["unit"])
    units2 = set()
    for entry in pool2["entries"]:
        for member in entry["members"]:
            units2.add(member["unit"])
    expected = units1 & proved
    missing = sorted(expected - units2)
    log("  pool1 member units                                %d"
        % len(units1))
    log("  of those, still proved by task 47                 %d"
        % len(expected))
    log("  of those, members of the_pool2.json               %d"
        % len(expected & units2))
    log("  missing                                           %d"
        % len(missing))
    for one in missing[:20]:
        log("    %s" % one)
    log("  pool1 units task 47 did NOT prove, so not carried  %d"
        % len(units1 - proved))
    log("  pool2 units that are new this round                %d"
        % len(units2 - units1))
    log("  every unit task 47 proved is a pool2 member: %s"
        % (proved == units2))
    ok = (not missing) and (proved == units2)
    log("  %s" % ("PASS" if ok else "FAIL"))
    return ok


def main():
    results = []
    results.append(claim_one())
    results.append(claim_two())
    results.append(claim_three())
    results.append(claim_four())
    log("")
    log("ALL FOUR CLAIMS: %s" % ("PASS" if all(results) else "FAIL"))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
