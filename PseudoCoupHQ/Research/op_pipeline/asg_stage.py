#!/usr/bin/env python3
"""asg_stage.py -- put the compound-assignment units and the plain
units into ONE universe, so the existing stages can be run over both
without being edited.

The problem this solves
-----------------------
Every stage in this line reads its input under a fixed name:
sem_anchored.py reads `op_units_<lang>.json`, match_units.py reads the
sem records for `<lang>`, and so on.  The compound-assignment run
wrote its units to `op_units_asg_<lang>.json`.  Nothing reads that
name.

Two ways to fix that were available: edit every stage to take a suffix,
or stage the asg units under the name the stages already read.  The
second is chosen, because it leaves every stage BYTE-IDENTICAL and
therefore leaves the question "did the asg units go through the same
code?" with the answer "yes, literally".  This is the method
dom_ops_java.py used for java.

Why ONE universe rather than an asg-only run
--------------------------------------------
The question this lap asks is how an asg unit relates to the PLAIN
unit whose operation it performs.  A run over the asg units alone
cannot answer that: there would be no plain unit in the room.  So the
staged `op_units_<lang>.json` holds BOTH sets, and every downstream
stage sees one population.

THE UNIT NUMBER, and why it is offset
-------------------------------------
Plain probe 0 and asg probe 0 are different units, and the unit label
is `<lang>/op_<n>`, so the two would collide.  Several stages sort
probes with `int(n)`, so a text prefix would break them.  The asg
units therefore keep a NUMERIC number, offset by ASG_N_OFFSET:

    asg probe 0  ->  n = 100000

Plain numbers run to the high hundreds, so the two ranges cannot meet.
Every staged asg unit records `asg_source_n` (its number in the asg
run) and `bucket` (already `assignment`, written by the probe
generator), so a reader can always get back to the original record.

WHAT `bucket` IS, stated because the spelling ban is absolute: it is
the probe generator's own provenance field, recorded at generation
time, saying which family of probe shapes the generator emitted.  It
is not an operator token, and no operator token is read, written, or
compared anywhere in this file.  The asg units are told apart from the
plain units by their NUMBER RANGE and by that provenance field, never
by how they are spelled.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns.  The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label on
the member.

WHERE THE STAGE SITS: `Research/stage_asg/`, a SIBLING of
op_pipeline.  It has to be a sibling: sem_anchored.py finds the lifter
at `os.path.join(os.path.dirname(HERE), "kind_fuzz_clustering")`, so a
stage nested inside op_pipeline would not find it.

usage:
  asg_stage.py [--stage DIR]
"""

import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

RESEARCH = os.path.dirname(HERE)

DEFAULT_STAGE = os.path.join(RESEARCH, "stage_asg")

LANGS = ["c", "cpp", "go", "rust", "swift"]

ASG_N_OFFSET = 100000

# every module a staged stage needs to import, copied so that the
# stage's own HERE resolves to the stage.
MODULES = [
    "sem_anchored.py", "canon.py", "match_units.py", "verdicts.py",
    "verdicts3.py", "z3_ext.py", "candidates_mirror.py",
    "candidates_mirror2.py", "check_no_spelling_keys.py",
    "core_modes.py", "result_vocab.py",
]

# files a staged stage reads but does not rebuild.
CARRY = ["verdicts2.json", "verdicts3_cache.json"]


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def offset_probes(probes, tally_key):
    """the asg probes, re-numbered into their own range."""
    out = {}
    for k in probes:
        old = int(k)
        new = old + ASG_N_OFFSET
        rec = json.loads(json.dumps(probes[k]))
        meta = rec.get("meta")
        if isinstance(meta, dict):
            meta["asg_source_n"] = old
            meta["n"] = new
        else:
            rec["asg_source_n"] = old
            rec["n"] = new
        out[str(new)] = rec
    return out


def combine(plain_path, asg_path, out_path, what):
    plain = json.load(open(plain_path))
    asg = json.load(open(asg_path))

    probes = {}
    for k in plain["probes"]:
        probes[k] = plain["probes"][k]

    staged = offset_probes(asg["probes"], what)
    for k in staged:
        if k in probes:
            log("!! REFUSING: staged number %s collides with a plain "
                "probe in %s" % (k, plain_path))
            return None
        probes[k] = staged[k]

    out = {}
    for k in plain:
        if k == "probes":
            continue
        out[k] = plain[k]
    out["probes"] = probes
    out["count"] = len(probes)
    out["staged"] = dict(
        note="this file is a STAGE, not an artifact of record.  It is "
             "the plain population and the compound-assignment "
             "population in one universe, so the pipeline stages can "
             "run over both without being edited.",
        plain_source=os.path.basename(plain_path),
        assignment_source=os.path.basename(asg_path),
        plain_probes=len(plain["probes"]),
        assignment_probes=len(staged),
        assignment_number_offset=ASG_N_OFFSET,
        how_to_tell_them_apart="an asg unit has n >= %d and carries "
                               "`asg_source_n`; it is NOT told apart "
                               "by how it is spelled" % ASG_N_OFFSET,
    )
    fh = open(out_path, "w")
    json.dump(out, fh, indent=1)
    fh.write("\n")
    fh.close()
    return out


def main():
    stage = DEFAULT_STAGE
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--stage":
            i = i + 1
            stage = args[i]
        i = i + 1

    if os.path.exists(stage):
        shutil.rmtree(stage)
    os.makedirs(stage)
    log("stage                   %s" % stage)

    total_plain = 0
    total_asg = 0
    for lang in LANGS:
        for pattern, asg_pattern in (
                ("op_units_%s.json", "op_units_asg_%s.json"),
                ("probe_manifest_%s.json", "probe_manifest_asg_%s.json")):
            plain_path = os.path.join(HERE, pattern % lang)
            asg_path = os.path.join(HERE, asg_pattern % lang)
            out_path = os.path.join(stage, pattern % lang)
            if not os.path.exists(plain_path):
                log("!! REFUSING: %s is not present" % plain_path)
                return 4
            if not os.path.exists(asg_path):
                log("!! REFUSING: %s is not present" % asg_path)
                return 4
            got = combine(plain_path, asg_path, out_path, pattern % lang)
            if got is None:
                return 4
            if pattern.startswith("op_units"):
                total_plain += got["staged"]["plain_probes"]
                total_asg += got["staged"]["assignment_probes"]
                log("  %-6s %-24s plain %4d + assignment %4d = %4d"
                    % (lang, pattern % lang,
                       got["staged"]["plain_probes"],
                       got["staged"]["assignment_probes"],
                       got["count"]))

    for name in MODULES:
        src = os.path.join(HERE, name)
        if not os.path.exists(src):
            log("!! REFUSING: module %s is not present" % name)
            return 4
        shutil.copy(src, os.path.join(stage, name))
    log("modules copied          %d" % len(MODULES))

    for name in CARRY:
        src = os.path.join(HERE, name)
        if not os.path.exists(src):
            log("   (no %s to carry)" % name)
            continue
        shutil.copy(src, os.path.join(stage, name))
    log("carried files           %s" % ", ".join(CARRY))

    log("")
    log("probes staged           plain %d + assignment %d = %d"
        % (total_plain, total_asg, total_plain + total_asg))
    log("NOTE: those are CANDIDATE probes.  The accepted units are")
    log("      fewer; the stages apply their own acceptance rules.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
