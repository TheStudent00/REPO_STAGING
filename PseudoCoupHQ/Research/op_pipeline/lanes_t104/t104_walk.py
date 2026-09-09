#!/usr/bin/env python3
"""t104_walk.py -- ONE re-normalization walk of every record in
`term66_store/`, into the NEW store `term104_store/`, ONE FORKED
SUB-PROCESS PER UNIT, carrying the whole audit the brief asks for.

WHAT THIS IS.  `term66_store/` holds one layer-4 / layer-5 record per
unit for the 30,280 units canon40 proves and task 97's walk finished.
This program rebuilds each record's LAYER-5 TEXT ONLY -- the term is
transcribed again from canon40 by the same `Term.transcribe`, and
printed again by `Term.normalize` as `term.py` stands -- and writes the
result to a store of its own.  `term66_store/` is never opened for
writing.

WHY ONE SUB-PROCESS PER UNIT.  A first attempt walked in a single
process and stopped making progress inside
`canon40_regen_store/op_units2_c_c0004.json` after 8 minutes at a flat
137 MB resident -- solver time, not memory.  That is the same obstacle
task 97 met and answered by forking one sub-process per unit (log_202
section 2): z3's context accumulates every term the process has built,
so a unit's cost depends on what was walked before it.

DEE'S TWO-PASS RULE.  Pass 1 runs every unit at the ordinary ceiling
and FLAGS whatever does not finish.  Pass 2 re-runs only the flagged
ones with more room and more clock, in a few worker processes at once
so the tail does not cost the whole afternoon.  A unit that does not
finish in pass 2 is NOT written into the store and is named in the
audit as a shortfall -- the same way `term66_store/` carries 30,280 of
30,324 records and names the 44 rather than approximating them.

WHAT EACH SUB-PROCESS MEASURES, per the brief's audit:
  (a) the layer-5 text, so the walk can say how many CHANGED;
  (b) the term's own s-expression hashed BEFORE `normalize` is called
      and again AFTER, inside the process that holds the term, so
      "printing does not touch the term" is checked and not asserted;
  (c) the declaration kinds present in the term, so the report's table
      of commutative operators is read off the terms;
  (d) THE OPERAND-ORDER ACCEPTANCE: a second term built from the first
      by permuting, at every commutative node, that node's own
      operands (a permutation drawn from `random.Random("t104|<unit>")`,
      so it depends on the unit and not on the walk order), normalized
      the same way.  The two texts must be the same string.  This is
      the property the brief's deliverable 2 names, measured directly.
      Pass 2 runs WITHOUT it -- those units are the expensive tail and
      the acceptance names its population rather than stretching to
      cover them.

THE STORE'S RECORD SHAPE IS UNCHANGED.  No field is added to a record:
the audit lives in `t104_audit.json` beside the store, so
`term104_store/` is a drop-in for `pool.read_terms`.

RESUMABLE.  `t104_walk_state.json` names the shards already walked and
the pass-2 units already answered; `t104_walk_evidence.json` carries
the accumulating measurements.  A second run of this program over a
finished walk does nothing and says so.

MEMORY BOUND.  The parent does no z3 work: it forks and collects.  Its
own hard cap is 6 GB with the named abort ABORT_MEMORY_T104.  Each
sub-process is capped by `RLIMIT_AS` at the pass's ceiling; pass 2 runs
3 workers at once, so its own ceiling times three must fit the
instance's 8 GB.

WRITES:  term104_store/*.json, t104_walk_state.json,
         t104_walk_evidence.json, t104_audit.json

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

No operator token appears in this file.  A unit's `operator` field is
carried through untouched as a DISPLAY LABEL and is never read for
grouping, pairing or candidate selection.

Coding discipline: no compound one-liner statements.

usage:
  t104_walk.py [pass1_mb pass1_seconds pass2_mb pass2_seconds]
  t104_walk.py pass2 <names.json> <out.json> <mb> <seconds>
"""

import glob
import hashlib
import json
import os
import random
import resource
import signal
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = os.path.dirname(HERE)
sys.path.insert(0, PIPELINE)

import z3                                                        # noqa: E402
import canonical_form as CF                                      # noqa: E402
import reference as R                                            # noqa: E402
import regate64_run as RG                                        # noqa: E402
import term as T                                                 # noqa: E402

OLD_STORE = os.path.join(PIPELINE, "term66_store")
NEW_STORE = os.path.join(PIPELINE, "term104_store")
AUDIT = os.path.join(PIPELINE, "t104_audit.json")
STATE = os.path.join(PIPELINE, "t104_walk_state.json")
EVIDENCE = os.path.join(PIPELINE, "t104_walk_evidence.json")
WORK = "/tmp/t104_pass2"

PROVED = "WRAPPED_TEXT_PROVED"
PARENT_CAP_KB = 6 * 1024 * 1024
MEMORY_TOKENS = ["MemoryError", "out of memory", "Cannot allocate"]
PASS2_WORKERS = 3   # 3 x the pass-2 ceiling must fit the instance's 8g


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    used = peak_kb()
    if used > PARENT_CAP_KB:
        raise SystemExit(
            "ABORT_MEMORY_T104: the parent's peak resident %d kB "
            "passed the stated cap of %d kB at %s"
            % (used, PARENT_CAP_KB, where))
    return used


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canon40_shards():
    """the canon40 shards, in the order term66_run.py walked them."""
    out = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        out.append(os.path.join(PIPELINE,
                                "canon40_wrapped_%s.json" % lang))
    out.append(os.path.join(PIPELINE, "canon40_interp.json"))
    pattern = os.path.join(PIPELINE, "canon40_regen_store", "*.json")
    out.extend(sorted(glob.glob(pattern)))
    return [path for path in out if os.path.exists(path)]


def old_shard_path(key):
    return os.path.join(OLD_STORE, key.replace("/", "__"))


def new_shard_path(key):
    return os.path.join(NEW_STORE, key.replace("/", "__"))


def kind_census(term):
    """every declaration kind in this term, counted once per node.

    Keyed by the NUMERIC declaration kind alone (2026-09-07, lane 11's
    guard): z3's kind number determines the name 1:1, so the name
    added nothing machine-readable and its presence in the key text
    was a spelling-ban violation (a dict key is a comparison/grouping
    scope). A kind's current name is read off `term.py`'s own tables
    at the point something is DISPLAYED, never stored as part of this
    count's key."""
    counts = {}
    seen = set()
    stack = [term]
    while stack:
        current = stack.pop()
        key = current.get_id()
        if key in seen:
            continue
        seen.add(key)
        if not z3.is_app(current):
            continue
        for index in range(current.num_args()):
            stack.append(current.arg(index))
        declaration = current.decl()
        label = "%d" % declaration.kind()
        counts[label] = counts.get(label, 0) + 1
    return counts


def permute_commutative(term, shuffler):
    """the same computation with every commutative node's own operands
    in a different order, built bottom-up with an explicit stack so a
    deep term cannot exhaust Python's own call stack.

    Returns (the new term, how many nodes actually moved)."""
    cache = {}
    moved = 0
    stack = [(term, False)]
    while stack:
        current, expanded = stack.pop()
        key = current.get_id()
        if key in cache:
            continue
        if not z3.is_app(current):
            cache[key] = current
            continue
        if not expanded:
            stack.append((current, True))
            for index in range(current.num_args()):
                stack.append((current.arg(index), False))
            continue
        declaration = current.decl()
        kind = declaration.kind()
        if current.num_args() == 0:
            cache[key] = current
            continue
        pieces = []
        for index in range(current.num_args()):
            pieces.append(cache[current.arg(index).get_id()])
        if kind in T.COMMUTATIVE_OPERATORS:
            if len(pieces) > 1:
                order = list(range(len(pieces)))
                shuffler.shuffle(order)
                if order != sorted(order):
                    moved = moved + 1
                pieces = [pieces[i] for i in order]
        elif kind in T.ROUNDED_COMMUTATIVE_OPERATORS:
            if len(pieces) > 2:
                order = list(range(1, len(pieces)))
                shuffler.shuffle(order)
                if order != sorted(order):
                    moved = moved + 1
                pieces = pieces[:1] + [pieces[i] for i in order]
        cache[key] = declaration(*pieces)
    return cache[term.get_id()], moved


def _alarm(signum, frame):
    raise TimeoutError()


def one_unit_forked(maker, name, unit, ceiling_mb, seconds, perturb):
    """transcribe and normalize ONE unit in a forked sub-process of its
    own, capped by `RLIMIT_AS` at `ceiling_mb`.

    The shape is `term97_walk.one_unit_forked`'s, with the GATE left
    out: the verdict travels unchanged from `term66_store`, because
    printing a term cannot change what was proved about it -- and the
    hash of the term's own s-expression before and after `normalize`
    is what checks that claim rather than asserting it.

    Returns (word, payload_or_None, wall_seconds, sub_peak_kb).
    `word` is walked / TIMED_OUT / ABORTED / RAISED / MEMORY_REASON."""
    read_end, write_end = os.pipe()
    started = time.time()
    child = os.fork()
    if child == 0:
        os.close(read_end)
        try:
            cap = ceiling_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
            transcription = maker.transcribe(unit)
            if transcription.out_term is None:
                answer = {"ok": True, "no_term": True}
            else:
                raw = transcription.out_term
                before_hash = digest(raw.sexpr())
                counts = kind_census(raw)
                text = maker.normalize(raw)
                after_hash = digest(raw.sexpr())
                answer = {
                    "ok": True,
                    "no_term": False,
                    "text": text,
                    "sha256_before": before_hash,
                    "sha256_after": after_hash,
                    "kinds": counts,
                }
                if perturb:
                    shuffler = random.Random("t104|%s" % name)
                    other, moved = permute_commutative(raw, shuffler)
                    answer["perturbed_text"] = maker.normalize(other)
                    answer["commutative_nodes_reordered"] = moved
            payload = json.dumps(answer)
        except BaseException as problem:
            payload = json.dumps({"ok": False,
                                  "raised": "%s: %s"
                                  % (type(problem).__name__, problem)})
        try:
            handle = os.fdopen(write_end, "w")
            handle.write(payload)
            handle.close()
        except BaseException:
            pass
        os._exit(0)
    os.close(write_end)
    handle = os.fdopen(read_end, "r")
    text = ""
    timed_out = False
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(int(seconds) + 1)
    try:
        text = handle.read()
    except TimeoutError:
        timed_out = True
    signal.alarm(0)
    handle.close()
    if timed_out:
        os.kill(child, signal.SIGKILL)
    stamp = os.wait4(child, 0)
    wall = time.time() - started
    child_peak = stamp[2].ru_maxrss
    if timed_out:
        return "TIMED_OUT", None, wall, child_peak
    if text == "":
        return "ABORTED", None, wall, child_peak
    answer = json.loads(text)
    if not answer["ok"]:
        for token in MEMORY_TOKENS:
            if token in answer["raised"]:
                return "MEMORY_REASON", answer, wall, child_peak
        return "RAISED", answer, wall, child_peak
    return "walked", answer, wall, child_peak


def build_maker():
    attached = RG.callee_units()
    readings = CF.runtime_answer_readings()
    reference = R.Reference(runtime_units=attached)
    return T.Term(reference=reference,
                  runtime_routines=CF.runtime_routine_names(readings),
                  runtime_units=attached,
                  runtime_answers=readings)


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    return json.load(open(path))


def save_json(path, document):
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()


def merge_counts(into, more):
    for key in more:
        into[key] = into.get(key, 0) + more[key]
    return into


# ==================================================================
# the pass-2 worker: one slice of the flagged units, serial, its own
# process, so pass 2 runs a few at a time without a single process
# accumulating every heavy term.
# ==================================================================

def pass2_worker(names_path, out_path, ceiling_mb, seconds):
    names = json.load(open(names_path))
    maker = build_maker()
    rows = []
    index = 0
    for entry in names:
        index = index + 1
        name = entry["unit"]
        key = entry["shard"]
        canon = json.load(open(os.path.join(PIPELINE, key)))
        unit = dict(canon["units"][name])
        unit["unit"] = name
        canon = None
        word, answer, wall, child_peak = one_unit_forked(
            maker, name, unit, ceiling_mb, seconds, False)
        rows.append({
            "unit": name,
            "shard": key,
            "word": word,
            "wall_seconds": round(wall, 2),
            "sub_peak_kb": child_peak,
            "answer": answer,
        })
        save_json(out_path, rows)
        sys.stdout.write("[%d/%d] %s %s %.1fs %d kB\n"
                         % (index, len(names), name, word, wall,
                            child_peak))
        sys.stdout.flush()
    save_json(out_path, rows)
    return 0


# ==================================================================
# the driver
# ==================================================================

def run_pass1(maker, ceiling_mb, seconds, state, evidence):
    paths = canon40_shards()
    total = len(paths)
    started = time.time()
    index = 0
    for path in paths:
        index = index + 1
        key = os.path.relpath(path, PIPELINE)
        if key in state["shards_done"]:
            sys.stdout.write("[%d/%d] %s already walked\n"
                             % (index, total, key))
            sys.stdout.flush()
            continue
        sys.stdout.write("[%d/%d] %s\n" % (index, total, key))
        sys.stdout.flush()
        old_path = old_shard_path(key)
        if not os.path.exists(old_path):
            state["shards_done"].append(key)
            save_json(STATE, state)
            continue
        old = json.load(open(old_path))
        canon = json.load(open(path))
        units = canon.get("units") or {}
        for name in sorted(units):
            if units[name].get("outcome") != PROVED:
                continue
            evidence["canon40_units_proved"] = (
                evidence["canon40_units_proved"] + 1)
            if name not in old["units"]:
                evidence["units_with_no_term66_record"].append(name)
        out = {}
        for name in sorted(old["units"]):
            record = dict(old["units"][name])
            if record.get("term_state") != "TERM":
                evidence["records_no_term"] = (
                    evidence["records_no_term"] + 1)
                out[name] = record
                continue
            if not record.get("proved"):
                evidence["records_with_a_term_not_proved"] = (
                    evidence["records_with_a_term_not_proved"] + 1)
                out[name] = record
                continue
            unit = dict(units[name])
            unit["unit"] = name
            word, answer, wall, child_peak = one_unit_forked(
                maker, name, unit, ceiling_mb, seconds, True)
            if word != "walked":
                evidence["flagged"].append({
                    "unit": name,
                    "shard": key,
                    "pass1_word": word,
                    "pass1_wall_seconds": round(wall, 2),
                    "pass1_sub_peak_kb": child_peak,
                })
                continue
            evidence["records_re_normalized"] = (
                evidence["records_re_normalized"] + 1)
            if answer.get("no_term"):
                record["layer5_normalized_text"] = None
                record["layer5_refusal"] = (
                    "the re-normalization walk built no OUT-0 term")
                out[name] = record
                continue
            merge_counts(evidence["declaration_kind_census"],
                         answer["kinds"])
            if answer["sha256_before"] != answer["sha256_after"]:
                evidence["layer4_hash_disagreements"].append({
                    "unit": name,
                    "sha256_before": answer["sha256_before"],
                    "sha256_after": answer["sha256_after"],
                })
            evidence["perturbation_units_checked"] = (
                evidence["perturbation_units_checked"] + 1)
            moved = answer.get("commutative_nodes_reordered") or 0
            evidence["perturbation_nodes_reordered"] = (
                evidence["perturbation_nodes_reordered"] + moved)
            if moved > 0:
                evidence["perturbation_units_with_a_node_moved"] = (
                    evidence["perturbation_units_with_a_node_moved"]
                    + 1)
            if answer.get("perturbed_text") != answer["text"]:
                evidence["perturbation_disagreements"].append({
                    "unit": name,
                    "commutative_nodes_reordered": moved,
                    "text_from_the_term_as_transcribed":
                        answer["text"],
                    "text_from_the_operand_permuted_term":
                        answer.get("perturbed_text"),
                })
            record["layer5_normalized_text"] = answer["text"]
            out[name] = record
        handle = open(new_shard_path(key), "w")
        json.dump({"shard": key,
                   "canon40_not_proved_not_transcribed":
                       old.get("canon40_not_proved_not_transcribed"),
                   "units": out}, handle, sort_keys=True)
        handle.close()
        old = None
        canon = None
        state["shards_done"].append(key)
        save_json(STATE, state)
        save_json(EVIDENCE, evidence)
        sys.stdout.write("   %d records written, %d re-normalized, "
                         "%d flagged, %d order-disagreements, parent "
                         "peak %d kB (%.0fs)\n"
                         % (len(out),
                            evidence["records_re_normalized"],
                            len(evidence["flagged"]),
                            len(evidence["perturbation_disagreements"]),
                            peak_kb(), time.time() - started))
        sys.stdout.flush()
        check_memory("shard %s" % key)
    return evidence


def run_pass2(ceiling_mb, seconds, state, evidence):
    todo = []
    for row in evidence["flagged"]:
        if row["unit"] in state["pass2_done"]:
            continue
        todo.append({"unit": row["unit"], "shard": row["shard"]})
    sys.stdout.write("-- PASS 2 over %d flagged units, ceiling %d MB, "
                     "%d s each, %d workers\n"
                     % (len(todo), ceiling_mb, seconds,
                        PASS2_WORKERS))
    sys.stdout.flush()
    if not todo:
        return evidence
    if not os.path.isdir(WORK):
        os.makedirs(WORK)
    slices = []
    for index in range(PASS2_WORKERS):
        slices.append([])
    for index, entry in enumerate(todo):
        slices[index % PASS2_WORKERS].append(entry)
    running = []
    for index, chunk in enumerate(slices):
        if not chunk:
            continue
        names_path = os.path.join(WORK, "names%d.json" % index)
        out_path = os.path.join(WORK, "out%d.json" % index)
        save_json(names_path, chunk)
        command = [sys.executable, os.path.abspath(__file__), "pass2",
                   names_path, out_path, str(ceiling_mb), str(seconds)]
        log_path = os.path.join(WORK, "worker%d.log" % index)
        log_handle = open(log_path, "w")
        process = subprocess.Popen(command, stdout=log_handle,
                                   stderr=subprocess.STDOUT)
        running.append((process, out_path, log_path, log_handle,
                        len(chunk)))
    finished = 0
    while finished < len(running):
        time.sleep(20)
        finished = 0
        done_now = 0
        for process, out_path, log_path, _handle, size in running:
            if process.poll() is not None:
                finished = finished + 1
            try:
                rows = load_json(out_path, [])
            except ValueError:
                rows = []
            done_now = done_now + len(rows)
        sys.stdout.write("   pass 2 progress %d of %d answered, "
                         "%d of %d workers finished\n"
                         % (done_now, len(todo), finished,
                            len(running)))
        sys.stdout.flush()
    for _process, _out, _log, handle, _size in running:
        handle.close()
    rows = []
    for _process, out_path, _log, _handle, _size in running:
        rows.extend(load_json(out_path, []))
    by_shard = {}
    for row in rows:
        by_shard.setdefault(row["shard"], []).append(row)
    for key in sorted(by_shard):
        written = new_shard_path(key)
        document = json.load(open(written))
        old = json.load(open(old_shard_path(key)))
        for row in by_shard[key]:
            name = row["unit"]
            state["pass2_done"].append(name)
            evidence["pass2_rows"].append({
                "unit": name,
                "shard": key,
                "word": row["word"],
                "wall_seconds": row["wall_seconds"],
                "sub_peak_kb": row["sub_peak_kb"],
            })
            if row["word"] != "walked":
                evidence["still_short_after_pass_2"].append(name)
                continue
            answer = row["answer"]
            record = dict(old["units"][name])
            if answer.get("no_term"):
                record["layer5_normalized_text"] = None
                record["layer5_refusal"] = (
                    "the re-normalization walk built no OUT-0 term")
            else:
                merge_counts(evidence["declaration_kind_census"],
                             answer["kinds"])
                if answer["sha256_before"] != answer["sha256_after"]:
                    evidence["layer4_hash_disagreements"].append({
                        "unit": name,
                        "sha256_before": answer["sha256_before"],
                        "sha256_after": answer["sha256_after"],
                    })
                record["layer5_normalized_text"] = answer["text"]
            document["units"][name] = record
            evidence["records_re_normalized"] = (
                evidence["records_re_normalized"] + 1)
        handle = open(written, "w")
        json.dump(document, handle, sort_keys=True)
        handle.close()
        document = None
        old = None
        save_json(STATE, state)
        save_json(EVIDENCE, evidence)
    return evidence


def text_delta():
    """the layer-5 texts of the two stores, compared unit by unit.

    Computed from the two stores on disk rather than carried through
    the walk, so the changed-record count can be recomputed by anyone
    from the artifacts alone."""
    changed = []
    before_only = []
    after_only = []
    for path in sorted(glob.glob(os.path.join(OLD_STORE, "*.json"))):
        name = os.path.basename(path)
        old = json.load(open(path))
        new_path = os.path.join(NEW_STORE, name)
        new = load_json(new_path, {"units": {}})
        for unit in sorted(old["units"]):
            before = old["units"][unit].get("layer5_normalized_text")
            if unit not in new["units"]:
                after_only.append(unit)
                continue
            after = new["units"][unit].get("layer5_normalized_text")
            if before == after:
                continue
            changed.append({
                "unit": unit,
                "lang": old["units"][unit].get("lang"),
                "outcome": old["units"][unit].get("outcome"),
                "proved": old["units"][unit].get("proved"),
                "text_before": before,
                "text_after": after,
            })
        for unit in sorted(new["units"]):
            if unit not in old["units"]:
                before_only.append(unit)
        old = None
        new = None
    return changed, before_only, after_only


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "pass2":
            return pass2_worker(sys.argv[2], sys.argv[3],
                                int(sys.argv[4]), int(sys.argv[5]))
    pass1_mb = 1536
    pass1_seconds = 60
    pass2_mb = 3072
    pass2_seconds = 900
    if len(sys.argv) > 4:
        pass1_mb = int(sys.argv[1])
        pass1_seconds = int(sys.argv[2])
        pass2_mb = int(sys.argv[3])
        pass2_seconds = int(sys.argv[4])
    if not os.path.isdir(NEW_STORE):
        os.makedirs(NEW_STORE)
    started = time.time()
    state = load_json(STATE, {"shards_done": [], "pass2_done": []})
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
    maker = build_maker()
    evidence = run_pass1(maker, pass1_mb, pass1_seconds, state,
                         evidence)
    evidence = run_pass2(pass2_mb, pass2_seconds, state, evidence)
    save_json(STATE, state)
    save_json(EVIDENCE, evidence)

    changed, before_only, after_only = text_delta()
    summary = {
        "records_re_normalized": evidence["records_re_normalized"],
        "records_no_term": evidence["records_no_term"],
        "records_with_a_term_not_proved":
            evidence["records_with_a_term_not_proved"],
        "records_whose_layer5_text_changed": len(changed),
        "records_in_term66_store_absent_from_term104_store":
            len(after_only),
        "records_in_term104_store_absent_from_term66_store":
            len(before_only),
        "layer4_sexpr_hash_disagreements":
            len(evidence["layer4_hash_disagreements"]),
        "records_flagged_in_pass_1": len(evidence["flagged"]),
        "records_still_short_after_pass_2":
            len(evidence["still_short_after_pass_2"]),
        "canon40_units_proved": evidence["canon40_units_proved"],
        "canon40_proved_units_with_no_term66_record":
            len(evidence["units_with_no_term66_record"]),
        "operand_order_acceptance_units_checked":
            evidence["perturbation_units_checked"],
        "operand_order_acceptance_units_with_a_node_moved":
            evidence["perturbation_units_with_a_node_moved"],
        "operand_order_acceptance_nodes_reordered":
            evidence["perturbation_nodes_reordered"],
        "operand_order_acceptance_disagreements":
            len(evidence["perturbation_disagreements"]),
        "pass1_ceiling_mb": pass1_mb,
        "pass1_seconds_per_unit": pass1_seconds,
        "pass2_ceiling_mb": pass2_mb,
        "pass2_seconds_per_unit": pass2_seconds,
        "seconds": round(time.time() - started, 1),
        "parent_peak_resident_kb": peak_kb(),
    }
    document = {
        "summary": summary,
        "changed_records": changed,
        "records_in_term66_store_absent_from_term104_store":
            sorted(after_only),
        "layer4_sexpr_hash_disagreements":
            evidence["layer4_hash_disagreements"],
        "operand_order_acceptance": {
            "what_it_measures":
                "for each unit a second term was built by permuting "
                "the operands of every commutative node, with the "
                "permutation drawn from random.Random('t104|<unit>'); "
                "both terms were normalized; the property holds when "
                "the two texts are the same string",
            "population":
                "the units pass 1 walked; the units pass 2 answered "
                "were not perturbation-checked and are named in "
                "pass2_units",
            "units_checked": evidence["perturbation_units_checked"],
            "units_with_a_node_moved":
                evidence["perturbation_units_with_a_node_moved"],
            "nodes_reordered":
                evidence["perturbation_nodes_reordered"],
            "disagreements": evidence["perturbation_disagreements"],
        },
        "pass2_units": evidence["pass2_rows"],
        "records_still_short_after_pass_2":
            sorted(evidence["still_short_after_pass_2"]),
        "canon40_proved_units_with_no_term66_record":
            sorted(evidence["units_with_no_term66_record"]),
        "declaration_kind_census":
            evidence["declaration_kind_census"],
        "commutative_table_in_term_py": {
            "plain": sorted(T.COMMUTATIVE_OPERATORS),
            "rounded": sorted(T.ROUNDED_COMMUTATIVE_OPERATORS),
        },
    }
    save_json(AUDIT, document)
    for name in sorted(summary):
        sys.stdout.write("   %-52s %s\n" % (name, summary[name]))
    sys.stdout.write("-- wrote %s\n" % AUDIT)
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
