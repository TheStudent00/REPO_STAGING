#!/usr/bin/env python3
"""canon38_guard.py -- THE GUARD, UNMODIFIED, OVER EVERY canon38 FILE,
IN ONE PROCESS.

This file RUNS `check_no_spelling_keys.py` as a separate process, with
its own interpreter, over every artifact this task wrote.  It adds
NOTHING to any field set, declares no exemption, and edits no guard
file.  Log 147 §13.7's lesson is the rule here: a stage that quiets
the checker about its own field has failed.

TWO TRANSCRIPTS ARE PRODUCED, so the before and the after sit side by
side:

  * `canon38_guard_transcript.txt` -- the AFTER: every canon38
    artifact, one process.  `grep -c exempt` must be 0, because no
    canon38 artifact declares the provenance role.
  * `canon38_guard_canon37_norole_transcript.txt` -- the BEFORE: task
    47's own canon37 artifacts, copied to a scratch directory with the
    one `role` line removed from `meta` and NOTHING else changed, then
    walked by the same unmodified guard.  Log 150 §3 predicts a FAIL
    with 579 places in `canon37_wrapped_c.json`.  The canon37 files on
    disk are never modified: only the copies are read.

usage:
  canon38_guard.py [--scratch DIR]
"""

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GUARD = os.path.join(HERE, "check_no_spelling_keys.py")
AFTER = os.path.join(HERE, "canon38_guard_transcript.txt")
BEFORE = os.path.join(HERE,
                      "canon38_guard_canon37_norole_transcript.txt")
SUMMARY = os.path.join(HERE, "canon38_guard.json")

LANGS = ["c", "cpp", "go", "rust", "swift"]


def canon38_paths():
    out = []
    for lang in LANGS:
        out.append(os.path.join(HERE, "canon38_wrapped_%s.json" % lang))
    out.append(os.path.join(HERE, "canon38_interp.json"))
    out.append(os.path.join(HERE, "canon38_regen_state.json"))
    out.append(os.path.join(HERE, "canon38_zero_regression.json"))
    for name in ("canon38_assemble.json", "canon38_guard.json"):
        later = os.path.join(HERE, name)
        if os.path.exists(later):
            out.append(later)
    out.extend(sorted(glob.glob(os.path.join(HERE,
                                             "canon38_regen_store",
                                             "*.json"))))
    live = []
    for path in out:
        if os.path.exists(path):
            live.append(path)
    return live


def canon37_paths():
    out = []
    for lang in LANGS:
        out.append(os.path.join(HERE, "canon37_wrapped_%s.json" % lang))
    out.append(os.path.join(HERE, "canon37_interp.json"))
    out.extend(sorted(glob.glob(os.path.join(HERE,
                                             "canon37_regen_store",
                                             "*.json"))))
    live = []
    for path in out:
        if os.path.exists(path):
            live.append(path)
    return live


def strip_role(source, destination):
    """a copy with the one `role` line removed from `meta`, and nothing
    else changed."""
    document = json.load(open(source))
    removed = False
    meta = document.get("meta")
    if isinstance(meta, dict):
        if "role" in meta:
            del meta["role"]
            removed = True
    if "role" in document:
        del document["role"]
        removed = True
    handle = open(destination, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    return removed


def run_guard(paths, transcript_path, heading):
    command = [sys.executable, GUARD] + paths
    proc = subprocess.run(command, capture_output=True, text=True)
    handle = open(transcript_path, "w")
    handle.write("%s\n" % heading)
    handle.write("$ python3 check_no_spelling_keys.py "
                 "<%d paths, one process>\n\n" % len(paths))
    handle.write(proc.stdout)
    if proc.stderr.strip():
        handle.write("\n-- stderr --\n")
        handle.write(proc.stderr)
    handle.write("\nGUARD EXIT CODE = %d\n" % proc.returncode)
    handle.close()
    text = proc.stdout
    counts = {
        "paths": len(paths),
        "pass_lines": text.count("\nPASS ") + int(
            text.startswith("PASS ")),
        "fail_lines": text.count("\nFAIL ") + int(
            text.startswith("FAIL ")),
        "exempt_lines": 0,
        "exit_code": proc.returncode,
    }
    for line in text.splitlines():
        if "exempt" in line:
            counts["exempt_lines"] = counts["exempt_lines"] + 1
    return counts


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch",
                        default="/tmp/canon38_guard_scratch")
    args = parser.parse_args(argv[1:])

    after_paths = canon38_paths()
    after = run_guard(after_paths, AFTER,
                      "canon38_guard.py -- THE AFTER: every canon38 "
                      "artifact, unmodified guard, ONE process. No "
                      "file declares the provenance role and nothing "
                      "was added to any field set.")
    print("AFTER  : %d paths  PASS %d  FAIL %d  exempt %d  exit %d"
          % (after["paths"], after["pass_lines"], after["fail_lines"],
             after["exempt_lines"], after["exit_code"]))

    scratch = args.scratch
    if os.path.isdir(scratch):
        shutil.rmtree(scratch)
    os.makedirs(scratch)
    before_paths = []
    stripped = 0
    for path in canon37_paths():
        destination = os.path.join(scratch, os.path.basename(path))
        if strip_role(path, destination):
            stripped = stripped + 1
        before_paths.append(destination)
    before = run_guard(before_paths, BEFORE,
                       "canon38_guard.py -- THE BEFORE: task 47's own "
                       "canon37 artifacts, copied with the one `role` "
                       "line removed and nothing else changed, walked "
                       "by the same unmodified guard.  The canon37 "
                       "files on disk are untouched.")
    print("BEFORE : %d paths  PASS %d  FAIL %d  exempt %d  exit %d  "
          "(role removed from %d copies)"
          % (before["paths"], before["pass_lines"],
             before["fail_lines"], before["exempt_lines"],
             before["exit_code"], stripped))

    handle = open(SUMMARY, "w")
    json.dump({
        "meta": {
            "produced_by": "canon38_guard.py",
            "guard": "check_no_spelling_keys.py, unmodified, run as a "
                     "separate process; nothing added to any field "
                     "set, no exemption declared",
        },
        "after_canon38": after,
        "before_canon37_with_the_role_line_removed": before,
        "scratch_directory": scratch,
        "canon37_files_on_disk_were_modified": False,
    }, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
