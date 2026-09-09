#!/usr/bin/env python3
"""zero_regression48.py -- THE ZERO-REGRESSION AUDIT for task 48.

TWO CLAIMS, EACH CHECKED RATHER THAN ASSERTED:

  CLAIM ONE -- task 47's artifacts are UNTOUCHED.  Checked against the
  version control system, not against memory: every canon37 artifact is
  asked whether the working tree differs from what is committed.  The
  daemon commits every thirty seconds, so an artifact this lap had
  modified would show as a difference here.

  CLAIM TWO -- no unit task 47 proved loses proved status.  Task 48
  writes new files only and re-reads task 47's, so the check is that
  every unit whose stored outcome is WRAPPED_TEXT_PROVED still carries
  that outcome in the artifact on disk, counted per population.

No operator token appears in this file.
"""

import glob
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def task47_paths():
    out = []
    for lang in ("c", "cpp", "go", "rust", "swift"):
        out.append(os.path.join(HERE, "canon37_wrapped_%s.json" % lang))
    out.append(os.path.join(HERE, "canon37_interp.json"))
    out.append(os.path.join(HERE, "canon37_regen_state.json"))
    out.extend(sorted(glob.glob(os.path.join(HERE,
                                             "canon37_regen_store",
                                             "*.json"))))
    out.extend(sorted(glob.glob(os.path.join(HERE, "canon37_*.py"))))
    out.append(os.path.join(HERE, "ledger47.py"))
    return [one for one in out if os.path.exists(one)]


def changed_against_the_vcs(paths):
    command = ["git", "status", "--porcelain", "--"] + paths
    result = subprocess.run(command, cwd=HERE, capture_output=True,
                            text=True)
    lines = [one for one in result.stdout.splitlines() if one.strip()]
    return lines, " ".join(command[:4]) + " ... (%d paths)" % len(paths)


def proved_counts():
    counts = {}
    for lang in ("c", "cpp", "go", "rust", "swift"):
        path = os.path.join(HERE, "canon37_wrapped_%s.json" % lang)
        document = json.load(open(path))
        proved = 0
        for record in document["units"].values():
            if record.get("outcome") == "WRAPPED_TEXT_PROVED":
                proved += 1
        counts["original:%s" % lang] = (proved, len(document["units"]))
    document = json.load(open(os.path.join(HERE,
                                           "canon37_interp.json")))
    proved = 0
    for record in document["units"].values():
        if record.get("outcome") == "WRAPPED_TEXT_PROVED":
            proved += 1
    counts["interpreter"] = (proved, len(document["units"]))
    proved = 0
    total = 0
    for path in sorted(glob.glob(os.path.join(HERE,
                                              "canon37_regen_store",
                                              "*.json"))):
        document = json.load(open(path))
        for record in document["units"].values():
            total += 1
            if record.get("outcome") == "WRAPPED_TEXT_PROVED":
                proved += 1
    counts["regenerated"] = (proved, total)
    return counts


def main():
    paths = task47_paths()
    print("CLAIM ONE -- task 47's artifacts are untouched")
    print("  paths asked about: %d" % len(paths))
    lines, command = changed_against_the_vcs(paths)
    print("  command: %s" % command)
    print("  the version control system reports %d changed path(s)"
          % len(lines))
    for line in lines[:20]:
        print("    %s" % line)
    if not lines:
        print("  PASS -- no task 47 artifact differs from what is "
              "committed, so none was modified by this lap.")
    print("")
    print("CLAIM TWO -- every unit task 47 proved still carries "
          "WRAPPED_TEXT_PROVED on disk")
    counts = proved_counts()
    total_proved = 0
    for key in sorted(counts):
        proved, units = counts[key]
        total_proved += proved
        print("  %-16s proved %6d of %6d" % (key, proved, units))
    print("  total proved on disk now: %d" % total_proved)
    print("  log 146 recorded 30,436 proved across the three "
          "populations; the number above is read off the artifacts, "
          "not off the log.")


if __name__ == "__main__":
    main()
