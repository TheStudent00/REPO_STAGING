#!/usr/bin/env python3
"""zero_regression53.py -- TASK 53: nothing earlier was touched, and
no unit task 52 proved is lost.

THREE CLAIMS, each computed rather than asserted:

  CLAIM ONE -- every canon38 artifact and every task-48 artifact on
  disk is older than the first file task 53 wrote.  The marker is
  `layer4c.py`'s own modification time, which is the moment this task
  began writing anything.  Each prior file is listed with its
  modification time and the first sixteen characters of its sha256.

  CLAIM TWO -- the version control system agrees: `git status
  --porcelain` over those same paths is empty, so the working tree
  copy is the committed copy.  (The daemon commits every thirty
  seconds, so an edit would show as a commit, not as a dirty path;
  both are checked.)

  CLAIM THREE -- the population is the one task 52 proved.  The number
  of units task 53 transcribed is compared, per population, against
  the number of units carrying a ledger in the canon38 artifacts.

usage:
  zero_regression53.py

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

No operator token appears in this file.

Coding discipline: no compound one-liner statements.
"""

import collections
import glob
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ("c", "cpp", "go", "rust", "swift")


def prior_paths():
    out = []
    for lang in LANGS:
        out.append(os.path.join(HERE, "canon38_wrapped_%s.json" % lang))
        out.append(os.path.join(HERE, "canon37_wrapped_%s.json" % lang))
        out.append(os.path.join(HERE, "layer4b_terms_%s.json" % lang))
    out.append(os.path.join(HERE, "canon38_interp.json"))
    out.append(os.path.join(HERE, "canon38_regen_state.json"))
    out.append(os.path.join(HERE, "layer4b_interp.json"))
    out.append(os.path.join(HERE, "layer4b_state.json"))
    out.append(os.path.join(HERE, "name_census3.json"))
    out.append(os.path.join(HERE, "layer4.py"))
    out.append(os.path.join(HERE, "textwalk48.py"))
    out.append(os.path.join(HERE, "gate48.py"))
    out.append(os.path.join(HERE, "census48b.py"))
    out.append(os.path.join(HERE, "ledger48.py"))
    out.append(os.path.join(HERE, "check_no_spelling_keys.py"))
    live = []
    for path in out:
        if os.path.exists(path):
            live.append(path)
    return live


def digest(path):
    engine = hashlib.sha256()
    handle = open(path, "rb")
    while True:
        block = handle.read(1 << 20)
        if not block:
            break
        engine.update(block)
    handle.close()
    return engine.hexdigest()


def stamp(when):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(when))


def claim_one():
    marker_path = os.path.join(HERE, "layer4c.py")
    marker = os.path.getmtime(marker_path)
    print("CLAIM ONE -- every prior artifact is older than the first "
          "file task 53 wrote")
    print("  the marker: layer4c.py, written %s" % stamp(marker))
    younger = []
    for path in prior_paths():
        when = os.path.getmtime(path)
        if when > marker:
            younger.append(path)
        print("  %-44s %s  %s"
              % (os.path.basename(path), stamp(when),
                 digest(path)[:16]))
    print("  prior artifacts modified after the marker: %d"
          % len(younger))
    for path in younger:
        print("    %s" % path)
    print("")
    return len(younger)


def claim_two():
    print("CLAIM TWO -- the version control system agrees")
    relative = []
    for path in prior_paths():
        relative.append(os.path.relpath(path, "~/Programming/"
                                              "PseudoCoupHQ"))
    command = ["git", "status", "--porcelain", "--"] + relative
    proc = subprocess.run(command, capture_output=True, text=True,
                          cwd="~/Programming/PseudoCoupHQ")
    text = proc.stdout.strip()
    print("  $ git status --porcelain -- <%d prior paths>"
          % len(relative))
    if text:
        print(text)
    else:
        print("  (no output: every prior path matches its committed "
              "copy)")
    print("")
    return len(text.splitlines())


def claim_three():
    print("CLAIM THREE -- the population is the one task 52 proved")
    wrapped = collections.Counter()
    for lang in LANGS:
        path = os.path.join(HERE, "canon38_wrapped_%s.json" % lang)
        if not os.path.exists(path):
            continue
        document = json.load(open(path))
        for name, unit in document["units"].items():
            if "ledger" in unit:
                wrapped["original"] += 1
    path = os.path.join(HERE, "canon38_interp.json")
    if os.path.exists(path):
        document = json.load(open(path))
        for name, unit in document["units"].items():
            if "ledger" in unit:
                wrapped["interpreter"] += 1
    for path in sorted(glob.glob(os.path.join(HERE,
                                              "canon38_regen_store",
                                              "*.json"))):
        document = json.load(open(path))
        for name, unit in document["units"].items():
            if "ledger" in unit:
                wrapped["regenerated"] += 1
    transcribed = collections.Counter()
    for lang in LANGS:
        path = os.path.join(HERE, "layer4c_terms_%s.json" % lang)
        if os.path.exists(path):
            document = json.load(open(path))
            transcribed["original"] += len(document["units"])
    path = os.path.join(HERE, "layer4c_interp.json")
    if os.path.exists(path):
        document = json.load(open(path))
        transcribed["interpreter"] += len(document["units"])
    for path in sorted(glob.glob(os.path.join(HERE,
                                              "layer4c_regen_store",
                                              "*.json"))):
        document = json.load(open(path))
        transcribed["regenerated"] += len(document["units"])
    print("  %-16s %10s %10s %8s"
          % ("population", "canon38", "task 53", "delta"))
    missing = 0
    for population in ("interpreter", "original", "regenerated"):
        left = wrapped[population]
        right = transcribed[population]
        missing += abs(left - right)
        print("  %-16s %10d %10d %8d"
              % (population, left, right, right - left))
    print("  %-16s %10d %10d %8d"
          % ("all three", sum(wrapped.values()),
             sum(transcribed.values()),
             sum(transcribed.values()) - sum(wrapped.values())))
    print("")
    return missing


def main():
    younger = claim_one()
    dirty = claim_two()
    missing = claim_three()
    print("VERDICT")
    print("  prior artifacts touched:      %d" % younger)
    print("  prior paths dirty in the vcs: %d" % dirty)
    print("  units missing from task 53:   %d" % missing)
    if younger or dirty or missing:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
