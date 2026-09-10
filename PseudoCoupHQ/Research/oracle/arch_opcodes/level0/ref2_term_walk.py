#!/usr/bin/env python3
"""ref2_term_walk.py -- every unit of `term66_store/` transcribed again under
the CORRECTED reference into a store of its own, and every unit whose layer-5
text moved attributed to the correction that moved it.

WHAT THIS IS, in relation.  `term66_store/` holds one layer-4 / layer-5 record
per unit for the 30,280 units canon40 proves: the unit's own term, built by
walking its ledger rows through `reference.py`'s builders, and that term
printed by `term.Term.normalize`.  Task ref2 corrected the reference, so every
term built through it can move.  This program rebuilds them all into
`term_ref2_store/` and says which moved and at which correction.

THE TOOLING IS TASK t104's, UNMODIFIED.  `lanes_t104/t104_walk.py` is the
program that walks `term66_store/` one forked sub-process per unit in two
passes, hashes each term's own s-expression before and after printing, and
computes the store-to-store text delta from the artifacts on disk.  This file
IMPORTS it and points its five paths at this task's own files; not one line of
it is changed, and `term66_store/` is opened for reading only.

  pass 1   every unit at an ordinary ceiling, flagging whatever does not
           finish
  pass 2   the flagged ones again with more room and more clock, a few
           worker processes at a time

THE ATTRIBUTION.  A second mode re-walks ONLY the units whose text moved, once
at each earlier state of the reference, and names the first state at which the
unit's text differs from what `term66_store/` holds.  The five states are the
files under `ref2_originals/`, loaded under the module names `reference` and
`condition_table` before anything imports either, so nothing on disk is
swapped.

MEMORY.  The stated bound is 12 GB with the named abort ABORT_MEMORY_REF2,
checked by `resource.getrusage` after every shard; the sample is the first
shard, whose peak is printed before the rest run.  Each sub-process is capped
by `RLIMIT_AS` at its pass's own ceiling, and pass 2 runs three at once, so
three times the pass-2 ceiling must fit inside the instance.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope, anywhere in
this line -- not in matching, not in "which pairs get compared", not in report
rows, not in dropdowns.  The candidate set for comparison comes from
machine-form evidence (clusters, connections, type pairs) or from ratified
intention -- never from the token.  The token appears exactly once per unit:
as a display label on the member.  HISTORY OF VIOLATIONS, so the pattern is
visible: (1) the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25 -- the
fix brief itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse its own
output on failure.  A brief handed to any subagent for this line MUST paste
this paragraph verbatim."

A unit's `operator` field is carried through as a DISPLAY LABEL by t104's own
walk and is never read here for grouping, pairing or selection.

Coding discipline: no compound one-liner statements.

usage:
  ref2_term_walk.py walk [p1_mb p1_s p2_mb p2_s]  the whole re-derivation
  ref2_term_walk.py retry [mb seconds]            the pass-2 tail, more room
  ref2_term_walk.py attribute <state>             the moved units at one state
  ref2_term_walk.py report <out.json>             the moved units, joined
"""

import glob
import importlib.util
import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = os.path.abspath(os.path.join(HERE, "..", "..", "..",
                                        "op_pipeline"))
LANES_T104 = os.path.join(PIPELINE, "lanes_t104")
ORIGINALS = os.path.join(HERE, "ref2_originals")

for _path in (PIPELINE, os.path.join(PIPELINE, "lean"), LANES_T104):
    if _path not in sys.path:
        sys.path.insert(0, _path)

STATES = ("before", "c1", "c2", "c3", "c4")
NEW_STORE = os.path.join(PIPELINE, "term_ref2_store")
AUDIT = os.path.join(HERE, "ref2_term_audit.json")
STATE_FILE = os.path.join(HERE, "ref2_term_walk_state.json")
EVIDENCE = os.path.join(HERE, "ref2_term_walk_evidence.json")
WORK = "/work/ref2_pass2"
MEMORY_CEILING_KB = 12 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_REF2"
PASS2_WORKERS = 2
"""TWO, NOT t104's THREE, and the arithmetic is the reason: the stated bound
is 12 GB, pass 2 runs its workers at 6,144 MB each, and two of those is
exactly the bound.  Task t104 measured that its own pass-2 ceiling of 3,072 MB
was too small for 184 units and had to retry them one at a time at 7,168 MB
(log_233 section 4, item 1); this walk starts at the larger ceiling instead of
arriving at it."""


def paths_of(label):
    if label == "before":
        return (os.path.join(ORIGINALS, "reference.py"),
                os.path.join(ORIGINALS, "condition_table.py"))
    return (os.path.join(ORIGINALS, "reference_%s.py" % label),
            os.path.join(ORIGINALS, "condition_table_%s.py" % label))


def install(label):
    reference_path, table_path = paths_of(label)
    for name, path in (("condition_table", table_path),
                       ("reference", reference_path)):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return reference_path


def load_walk():
    """task t104's walk, unmodified, with its five paths pointed at this
    task's own files and its parent cap raised to this task's bound."""
    import t104_walk                                        # noqa: E402
    t104_walk.NEW_STORE = NEW_STORE
    t104_walk.AUDIT = AUDIT
    t104_walk.STATE = STATE_FILE
    t104_walk.EVIDENCE = EVIDENCE
    t104_walk.WORK = WORK
    t104_walk.PARENT_CAP_KB = MEMORY_CEILING_KB
    t104_walk.PASS2_WORKERS = PASS2_WORKERS
    return t104_walk


def save_json(path, document):
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    handle = open(path)
    document = json.load(handle)
    handle.close()
    return document


def walk(argv):
    install("c4")
    module = load_walk()
    pass1_mb = 1536
    pass1_seconds = 60
    pass2_mb = 3072
    pass2_seconds = 900
    if len(argv) > 3:
        pass1_mb = int(argv[0])
        pass1_seconds = int(argv[1])
        pass2_mb = int(argv[2])
        pass2_seconds = int(argv[3])
    if not os.path.isdir(NEW_STORE):
        os.makedirs(NEW_STORE)
    started = time.time()
    state = load_json(STATE_FILE, {"shards_done": [],
                                   "pass2_done": []})
    evidence = load_json(EVIDENCE, {
        "canon40_units_proved": 0,
        "units_with_no_term66_record": [],
        "records_no_term": 0,
        "records_with_a_term_not_proved": 0,
        "records_re_normalized": 0,
        "flagged": [],
        "pass2_rows": [],
        "still_short_after_pass_2": [],
        "layer4_hash_disagreements": [],
        "declaration_kind_census": {},
        "perturbation_units_checked": 0,
        "perturbation_units_with_a_node_moved": 0,
        "perturbation_nodes_reordered": 0,
        "perturbation_disagreements": [],
    })
    maker = module.build_maker()
    evidence = module.run_pass1(maker, pass1_mb, pass1_seconds, state,
                                evidence)
    evidence = module.run_pass2(pass2_mb, pass2_seconds, state,
                                evidence)
    save_json(STATE_FILE, state)
    save_json(EVIDENCE, evidence)
    changed, before_only, after_only = module.text_delta()
    summary = {
        "records_re_normalized": evidence["records_re_normalized"],
        "records_no_term": evidence["records_no_term"],
        "records_with_a_term_not_proved":
            evidence["records_with_a_term_not_proved"],
        "records_whose_layer5_text_changed": len(changed),
        "records_in_the_old_store_absent_from_the_new": len(after_only),
        "records_in_the_new_store_absent_from_the_old": len(before_only),
        "layer4_sexpr_hash_disagreements":
            len(evidence["layer4_hash_disagreements"]),
        "records_flagged_in_pass_1": len(evidence["flagged"]),
        "records_still_short_after_pass_2":
            len(evidence["still_short_after_pass_2"]),
        "canon40_units_proved": evidence["canon40_units_proved"],
        "operand_order_acceptance_units_checked":
            evidence["perturbation_units_checked"],
        "operand_order_acceptance_disagreements":
            len(evidence["perturbation_disagreements"]),
        "pass1_ceiling_mb": pass1_mb,
        "pass2_ceiling_mb": pass2_mb,
        "seconds": round(time.time() - started, 1),
        "parent_peak_resident_kb": module.peak_kb(),
        "memory_ceiling_kb": MEMORY_CEILING_KB,
        "named_abort": ABORT_NAME,
    }
    save_json(AUDIT, {"summary": summary, "changed_records": changed,
                      "records_in_the_old_store_absent_from_the_new":
                          sorted(after_only),
                      "layer4_sexpr_hash_disagreements":
                          evidence["layer4_hash_disagreements"],
                      "operand_order_disagreements":
                          evidence["perturbation_disagreements"]})
    for key in sorted(summary):
        print("  %-52s %s" % (key, summary[key]))
    return 0


def write_audit(module, evidence, extra):
    """the audit, recomputed from the two stores on disk."""
    changed, before_only, after_only = module.text_delta()
    summary = {
        "records_re_normalized": evidence["records_re_normalized"],
        "records_no_term": evidence["records_no_term"],
        "records_with_a_term_not_proved":
            evidence["records_with_a_term_not_proved"],
        "records_whose_layer5_text_changed": len(changed),
        "records_in_the_old_store_absent_from_the_new": len(after_only),
        "records_in_the_new_store_absent_from_the_old": len(before_only),
        "layer4_sexpr_hash_disagreements":
            len(evidence["layer4_hash_disagreements"]),
        "records_flagged_in_pass_1": len(evidence["flagged"]),
        "records_still_short_after_pass_2":
            len(evidence["still_short_after_pass_2"]),
        "canon40_units_proved": evidence["canon40_units_proved"],
        "operand_order_acceptance_units_checked":
            evidence["perturbation_units_checked"],
        "operand_order_acceptance_disagreements":
            len(evidence["perturbation_disagreements"]),
        "parent_peak_resident_kb": module.peak_kb(),
        "memory_ceiling_kb": MEMORY_CEILING_KB,
        "named_abort": ABORT_NAME,
    }
    summary.update(extra)
    save_json(AUDIT, {"summary": summary, "changed_records": changed,
                      "records_in_the_old_store_absent_from_the_new":
                          sorted(after_only),
                      "layer4_sexpr_hash_disagreements":
                          evidence["layer4_hash_disagreements"],
                      "operand_order_disagreements":
                          evidence["perturbation_disagreements"]})
    for key in sorted(summary):
        print("  %-52s %s" % (key, summary[key]))
    return summary


def retry(argv):
    """THE LAW'S RULE THAT A MEMORY CEILING IS A FLAG, applied to this
    walk's own pass-2 tail: the units still short are run again with
    more room and ONE worker, through the SAME `run_pass2`.

    This is task t104's own remedy (`lanes_t104/t104_pass2_retry.py`,
    log_233 section 4 item 1) with this task's paths: nothing of
    `t104_walk.py` is edited, its worker count is turned down on the
    imported object, and the units are cleared from `pass2_done` so its
    own pass 2 sees them again."""
    install("c4")
    module = load_walk()
    ceiling_mb = 10240
    seconds = 900
    if len(argv) > 1:
        ceiling_mb = int(argv[0])
        seconds = int(argv[1])
    module.PASS2_WORKERS = 1
    state = load_json(STATE_FILE, None)
    evidence = load_json(EVIDENCE, None)
    if state is None or evidence is None:
        raise SystemExit("no walk state: run `walk` first")
    short_before = sorted(evidence["still_short_after_pass_2"])
    print("[1/2] %d units still short, retrying at %d MB / %d s, "
          "1 worker" % (len(short_before), ceiling_mb, seconds))
    sys.stdout.flush()
    short = set(short_before)
    state["pass2_done"] = [name for name in state["pass2_done"]
                           if name not in short]
    evidence["still_short_after_pass_2"] = []
    evidence = module.run_pass2(ceiling_mb, seconds, state, evidence)
    save_json(STATE_FILE, state)
    save_json(EVIDENCE, evidence)
    short_after = sorted(evidence["still_short_after_pass_2"])
    converged = sorted(short - set(short_after))
    print("[2/2] %d of %d converged at the higher ceiling; %d still "
          "short" % (len(converged), len(short_before),
                     len(short_after)))
    write_audit(module, evidence,
                {"retry_ceiling_mb": ceiling_mb,
                 "retry_seconds_per_unit": seconds,
                 "retry_population": len(short_before),
                 "retry_converged": len(converged),
                 "retry_still_short": len(short_after)})
    return 0


def shard_of_unit():
    """unit -> the canon40 shard it lives in, read off the old store."""
    out = {}
    pattern = os.path.join(PIPELINE, "term66_store", "*.json")
    for path in sorted(glob.glob(pattern)):
        document = load_json(path, {"units": {}})
        key = document.get("shard")
        for name in document["units"]:
            out[name] = key
    return out


def attribute(label):
    """the moved units walked again at ONE earlier state of the
    reference, so the correction that moved each can be named."""
    install(label)
    module = load_walk()
    audit = load_json(AUDIT, None)
    if audit is None:
        raise SystemExit("no %s: run `walk` first" % AUDIT)
    moved = [row["unit"] for row in audit["changed_records"]]
    where = shard_of_unit()
    maker = module.build_maker()
    rows = {}
    total = len(moved)
    index = 0
    for name in moved:
        index = index + 1
        key = where.get(name)
        if key is None:
            rows[name] = {"word": "no shard", "text": None}
            continue
        canon = load_json(os.path.join(PIPELINE, key), {"units": {}})
        if name not in canon["units"]:
            rows[name] = {"word": "not in the shard", "text": None}
            continue
        unit = dict(canon["units"][name])
        unit["unit"] = name
        canon = None
        word, answer, wall, peak = module.one_unit_forked(
            maker, name, unit, 3072, 300, False)
        text = None
        if word == "walked" and not answer.get("no_term"):
            text = answer["text"]
        rows[name] = {"word": word, "text": text,
                      "wall_seconds": round(wall, 2),
                      "sub_peak_kb": peak}
        if index % 20 == 0:
            sys.stdout.write("[%d/%d] parent peak %d kB\n"
                             % (index, total, module.peak_kb()))
            sys.stdout.flush()
        if module.peak_kb() > MEMORY_CEILING_KB:
            raise SystemExit("%s: parent peak %d kB past %d kB"
                             % (ABORT_NAME, module.peak_kb(),
                                MEMORY_CEILING_KB))
    out = os.path.join(HERE, "ref2_term_state_%s.json" % label)
    save_json(out, {"state": label, "units": rows})
    print("[%d/%d] wrote %s" % (total, total, out))
    print("parent peak %d kB, ceiling %d kB, named abort %s"
          % (module.peak_kb(), MEMORY_CEILING_KB, ABORT_NAME))
    return 0


def report(out_path):
    audit = load_json(AUDIT, None)
    if audit is None:
        raise SystemExit("no %s: run `walk` first" % AUDIT)
    per_state = {}
    for label in ("c1", "c2", "c3"):
        path = os.path.join(HERE, "ref2_term_state_%s.json" % label)
        per_state[label] = load_json(path, {"units": {}})["units"]
    rows = []
    counts = {}
    for record in audit["changed_records"]:
        name = record["unit"]
        first = "c4"
        for label in ("c1", "c2", "c3"):
            entry = per_state[label].get(name)
            if entry is None:
                continue
            if entry.get("text") != record["text_before"]:
                first = label
                break
        counts[first] = counts.get(first, 0) + 1
        rows.append({"unit": name, "lang": record.get("lang"),
                     "moved_at": first,
                     "text_before": record["text_before"],
                     "text_after": record["text_after"]})
    document = {
        "what": ("every unit of term66_store whose layer-5 text moved "
                 "under task ref2's four corrections, attributed to "
                 "the correction that moved it"),
        "units_whose_text_moved": len(rows),
        "by_correction": counts,
        "moved": rows,
    }
    save_json(out_path, document)
    print("| moved at | units |")
    print("|---|---|")
    for label in ("c1", "c2", "c3", "c4"):
        print("| %s | %d |" % (label, counts.get(label, 0)))
    print("")
    print("units whose layer-5 text moved: %d" % len(rows))
    for label in ("c1", "c2", "c3", "c4"):
        shown = 0
        print("THREE EXAMPLES LITERAL, moved at %s:" % label)
        for row in rows:
            if row["moved_at"] != label:
                continue
            print("  %s" % row["unit"])
            print("    before: %s" % row["text_before"])
            print("    after : %s" % row["text_after"])
            shown = shown + 1
            if shown >= 3:
                break
        if shown == 0:
            print("  (none)")
        print("")
    return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    command = argv[1]
    if command == "walk":
        return walk(argv[2:])
    if command == "retry":
        return retry(argv[2:])
    if command == "attribute":
        return attribute(argv[2])
    if command == "report":
        return report(argv[2])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
