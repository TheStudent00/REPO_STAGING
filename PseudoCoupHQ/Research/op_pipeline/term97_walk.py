#!/usr/bin/env python3
"""term97_walk.py -- the TWO-PASS walk that finishes `term66` over
canon40, by the owner's rule of 2026-09-04:

  "if it timed out, why not have all those flagged for things to
   either have a look at after or just re-run with the rest of them
   and give them a longer processing time to see if it changes the
   result?"

So: the cheap ones run at the ordinary budget; the expensive ones are
FLAGGED and never stored; pass two re-runs the flagged ones with a
stated larger time and memory budget and reports whether the answer
changed.  Nothing here changes what a term IS.  There is no summarised
callee, no truncated walk, no bounded normalizer.  A unit either gets
the record `term66_run.one_unit` computes, or it is reported as not
finished.

WHAT IS REUSED RATHER THAN COPIED.  `term66_run.one_unit` is THE
record and is called, not re-typed; `term66_run.py` is not edited.
`term66_run.shards`, `.runtime_rows_of` and `.PROVED` are called too.
The store this writes is `term66_store` and the resume state is
`term66_state.json`, because the brief is to COMPLETE term66 and the
downstream drivers read those two names.

WHY A FORKED SUB-PROCESS PER UNIT, and what it is not.  `term66_run.run`
builds one `Reference`, one `Term` and one `Gate` and then walks every
unit of every shard through them, so z3's context accumulates for the
whole run.  Measured under that arrangement, `op_units2_c_c0004` took
1,112 s for 24 records (log_189 section 3.1).  Measured with a pristine
parent that builds the same three objects once and FORKS one
sub-process per unit -- the arrangement here -- the same 24 records took
13.4 s (`probe97a_unit_cost.json`, lane `t97_l1_sample.sh`).  The unit's
record is computed by exactly the same function over exactly the same
objects; only the lifetime of the z3 context differs.

HOW A RUNNER LIMIT IS KEPT OUT OF A TERM'S STATED REASON, mechanically.
Two independent guards, because `Term.transcribe` and
`term66_run.add_layer5` both catch an exception raised while building
and record it as a written reason:

  1. THE WALL CLOCK IS ENFORCED FROM OUTSIDE.  The parent alarms and
     SIGKILLs; the sub-process never sees a deadline, so a spent budget
     cannot be caught and written down.  A sub-process stopped this way
     returns nothing and its unit is flagged.
  2. EVERY RETURNED RECORD IS SCANNED for a memory failure that became
     a written reason, in a hole, a no-term reason, a relink refusal or
     a layer-5 refusal.  A record that carries one is NOT STORED.  Its
     unit is flagged and re-run in pass two.

The scan's token list is `MEMORY_TOKENS` and it was CUT DOWN by
measurement: `canceled` was in the first draft and was removed, because
it is also z3's own word for a solver that spent its WALL CLOCK, which
is a legitimate UNDECIDED verdict and not a runner memory limit
(`probe97b_flag_reason.py`, lane `t97_l2_flag_reason.sh`).

THE MEMORY BOUND, stated as the round requires.  Per sub-process:
`RLIMIT_AS` at the pass's stated ceiling.  Per parent: 6 GB, checked
after every unit, with the named abort ABORT_MEMORY_T97.  The parent
does no z3 work after setup -- it forks and collects -- and its own
peak was measured at 61,748 kB over the sample.

Coding discipline: no compound one-liner statements.

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

No operator token appears in this file.  A unit's `operator` field
rides onto its record as a DISPLAY LABEL, written by
`term66_run.one_unit`, and is never read here for grouping, pairing,
candidate selection or comparison scope.  The order units are walked in
is the shard's own sorted unit-name order; the order shards are walked
in is `term66_run.shards`.

usage:
  term97_walk.py pass1 <ceiling MB> <seconds> <slice index> <slice count>
  term97_walk.py pass2 <ceiling MB> <seconds> <part> <slice index> <slice count> <pass1|part file>
  term97_walk.py control <ceiling MB> <seconds> <every Nth unit>
  term97_walk.py finalize
"""

import glob
import json
import os
import resource
import signal
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canonical_form as CF                                      # noqa: E402
import gate as G                                                 # noqa: E402
import reference as R                                            # noqa: E402
import regate64_run as RG                                        # noqa: E402
import term as T                                                 # noqa: E402
import term66_run as TR                                          # noqa: E402

STORE = os.path.join(HERE, "term66_store")
STATE = os.path.join(HERE, "term66_state.json")
FLAG_GLOB = os.path.join(HERE, "term97_flagged_slice*.json")

# a memory failure that became a written reason.  `canceled` is NOT in
# this list and the reason is measured -- see the module docstring.
MEMORY_TOKENS = ["MemoryError", "out of memory", "out-of-memory",
                 "max. memory exceeded", "std::bad_alloc"]

PARENT_CAP_KB = 6 * 1024 * 1024


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_parent_memory():
    used = peak_kb()
    if used > PARENT_CAP_KB:
        raise SystemExit(
            "ABORT_MEMORY_T97: the parent's peak resident %d kB passed "
            "the stated cap of %d kB" % (used, PARENT_CAP_KB))
    return used


def memory_reason_in(record):
    text = json.dumps(record)
    for token in MEMORY_TOKENS:
        if token in text:
            return token
    return None


def build():
    """the three objects `term66_run.run` builds, built once in the
    parent so every forked sub-process inherits them and pays no
    setup.  The parent does no z3 work with them itself."""
    attached = RG.callee_units()
    readings = CF.runtime_answer_readings()
    reference = R.Reference(runtime_units=attached)
    maker = T.Term(reference=reference,
                   runtime_routines=CF.runtime_routine_names(readings),
                   runtime_units=attached,
                   runtime_answers=readings)
    gate = G.Gate(reference=reference)
    return maker, gate, attached, readings


def _alarm(signum, frame):
    raise TimeoutError()


def one_unit_forked(maker, gate, name, unit, ceiling_mb, seconds):
    """one unit answered in a forked sub-process of its own.

    Returns (word, record_or_None, wall_seconds, peak_kb, token).
    `word` is walked / TIMED_OUT / ABORTED / RAISED / MEMORY_REASON."""
    read_end, write_end = os.pipe()
    started = time.time()
    child = os.fork()
    if child == 0:
        os.close(read_end)
        try:
            cap = ceiling_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
            record = TR.one_unit(maker, gate, name, unit)
            payload = json.dumps({"ok": True, "record": record})
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
        return "TIMED_OUT", None, wall, child_peak, None
    if text == "":
        return "ABORTED", None, wall, child_peak, None
    answer = json.loads(text)
    if not answer["ok"]:
        return "RAISED", {"raised": answer["raised"]}, wall, \
            child_peak, None
    record = answer["record"]
    token = memory_reason_in(record)
    if token is not None:
        return "MEMORY_REASON", record, wall, child_peak, token
    return "walked", record, wall, child_peak, None


def store_path(key):
    return os.path.join(STORE, key.replace("/", "__"))


def remaining_shards():
    """the canon40 inputs `term66_state.json` has not walked, in
    `term66_run.shards` order."""
    state = json.load(open(STATE))
    done = set(state["done"])
    out = []
    for path in TR.shards():
        key = os.path.relpath(path, HERE)
        if key in done:
            continue
        out.append((key, path))
    return out, sorted(done)


def pass1(ceiling, seconds, index, count):
    if not os.path.isdir(STORE):
        os.makedirs(STORE)
    todo, done = remaining_shards()
    mine = []
    position = 0
    for key, path in todo:
        if position % count == index:
            mine.append((key, path))
        position = position + 1
    say("-- PASS 1, slice %d of %d" % (index, count))
    say("   per-unit address-space ceiling %d MB" % ceiling)
    say("   per-unit wall clock %d s, enforced by the parent with "
        "SIGKILL" % seconds)
    say("   inputs already done at handoff %d" % len(done))
    say("   inputs still to walk %d, of which this slice owns %d"
        % (len(todo), len(mine)))
    maker, gate, attached, readings = build()
    say("   setup: attached callee units %d, runtime answer readings %d"
        % (len(attached), len(readings)))
    flagged = []
    walked_total = 0
    started = time.time()
    position = 0
    for key, path in mine:
        position = position + 1
        document = json.load(open(path))
        out = {}
        not_proved = 0
        shard_flagged = 0
        for name in sorted(document.get("units", {})):
            unit = document["units"][name]
            if unit.get("outcome") != TR.PROVED:
                not_proved = not_proved + 1
                continue
            word, record, wall, child, token = one_unit_forked(
                maker, gate, name, unit, ceiling, seconds)
            if word == "walked":
                out[name] = record
                walked_total = walked_total + 1
                continue
            shard_flagged = shard_flagged + 1
            flagged.append({
                "shard": key,
                "unit": name,
                "pass1_word": word,
                "pass1_token": token,
                "pass1_wall_seconds": round(wall, 3),
                "pass1_child_peak_kb": child,
                "pass1_ceiling_mb": ceiling,
                "pass1_seconds": seconds,
                "runtime_callee_rows": TR.runtime_rows_of(unit)[0],
                "pass1_partial_term_state":
                    (record or {}).get("term_state"),
                "pass1_partial_verdict": (record or {}).get("outcome"),
                "pass1_raised": (record or {}).get("raised"),
            })
            check_parent_memory()
        handle = open(store_path(key), "w")
        json.dump({"shard": key,
                   "canon40_not_proved_not_transcribed": not_proved,
                   "units": out}, handle, sort_keys=True)
        handle.close()
        say("[%d/%d] %s: %d transcribed, %d flagged, %d "
            "canon40-not-proved skipped, parent peak %d kB (%.0fs)"
            % (position, len(mine), key, len(out), shard_flagged,
               not_proved, peak_kb(), time.time() - started))
    out_path = os.path.join(HERE,
                            "term97_flagged_slice%d.json" % index)
    handle = open(out_path, "w")
    json.dump({"slice": index,
               "slice_count": count,
               "ceiling_mb": ceiling,
               "seconds": seconds,
               "shards_walked": [key for key, path in mine],
               "records_walked": walked_total,
               "parent_peak_kb": peak_kb(),
               "flagged": flagged}, handle, indent=1, sort_keys=True)
    handle.close()
    say("-- slice %d: %d records walked, %d flagged, wall %.0f s, "
        "parent peak %d kB"
        % (index, walked_total, len(flagged), time.time() - started,
           peak_kb()))
    say("-- wrote %s" % os.path.basename(out_path))


def read_flags():
    rows = []
    for path in sorted(glob.glob(FLAG_GLOB)):
        document = json.load(open(path))
        rows.extend(document["flagged"])
    return rows


def pass2(ceiling, seconds, part, index, count, source):
    """every unit pass 1 flagged, re-run with more time and more room.

    The record that comes back is merged into the store shard pass 1
    already wrote.  A record that STILL carries a runner limit as a
    written reason is still not stored, and is reported as not
    finished.

    `source` is where the flagged set is read from: `pass1` reads
    `term97_flagged_slice*.json`; anything else is a glob over previous
    pass-2 part files, whose UNFINISHED rows become this leg's
    population.  `index`/`count` cut that population into slices that
    run side by side, so the instance holds `count` sub-process
    ceilings at once and no more."""
    if source == "pass1":
        rows = read_flags()
    else:
        rows = []
        found = sorted(glob.glob(os.path.join(HERE, source)))
        if not found:
            raise SystemExit(
                "REFUSED OWN OUTPUT: no part file matches %r, so the "
                "residue population cannot be read" % source)
        for one in found:
            for row in json.load(open(one))["rows"]:
                if row["stored"]:
                    continue
                rows.append(row)
    rows = sorted(rows, key=lambda r: (r["shard"], r["unit"]))
    # THE SLICE IS CUT BY SHARD, never by row.  A pass-2 record is
    # merged back into the store shard pass 1 wrote, so two slices that
    # held rows of the same shard would read and write the same file at
    # the same time and one of them would lose a record.  Cutting by
    # shard gives every store shard exactly one writer.
    every_shard = []
    for row in rows:
        if row["shard"] in every_shard:
            continue
        every_shard.append(row["shard"])
    mine_shards = set()
    position = 0
    for key in every_shard:
        if position % count == index:
            mine_shards.add(key)
        position = position + 1
    mine = []
    for row in rows:
        if row["shard"] not in mine_shards:
            continue
        mine.append(row)
    rows = mine
    say("-- PASS 2, part %s, slice %d of %d, flagged set read from %s"
        % (part, index, count, source))
    say("   per-unit address-space ceiling %d MB (pass 1 gave "
        "%s)" % (ceiling,
                 sorted(set(str(r["pass1_ceiling_mb"]) for r in rows))))
    say("   per-unit wall clock %d s (pass 1 gave %s)"
        % (seconds,
           sorted(set(str(r["pass1_seconds"]) for r in rows))))
    say("   flagged units to re-run %d" % len(rows))
    if not rows:
        say("   nothing was flagged; pass 2 has no population")
    maker, gate, attached, readings = build()
    say("   setup: attached callee units %d, runtime answer readings %d"
        % (len(attached), len(readings)))
    documents = {}
    results = []
    started = time.time()
    position = 0
    for row in sorted(rows, key=lambda r: (r["shard"], r["unit"])):
        position = position + 1
        key = row["shard"]
        if key not in documents:
            documents[key] = json.load(open(os.path.join(HERE, key)))
        unit = documents[key]["units"][row["unit"]]
        word, record, wall, child, token = one_unit_forked(
            maker, gate, row["unit"], unit, ceiling, seconds)
        answer = dict(row)
        answer["pass2_ceiling_mb"] = ceiling
        answer["pass2_seconds"] = seconds
        answer["pass2_word"] = word
        answer["pass2_token"] = token
        answer["pass2_wall_seconds"] = round(wall, 3)
        answer["pass2_child_peak_kb"] = child
        if record is not None and "term_state" in record:
            answer["pass2_term_state"] = record.get("term_state")
            answer["pass2_verdict"] = record.get("outcome")
            answer["pass2_proved"] = record.get("proved")
            answer["pass2_holes"] = len(record.get("holes") or [])
        answer["answer_changed"] = (word != row["pass1_word"])
        if word == "walked":
            merged = json.load(open(store_path(key)))
            merged["units"][row["unit"]] = record
            handle = open(store_path(key), "w")
            json.dump(merged, handle, sort_keys=True)
            handle.close()
            answer["stored"] = True
        else:
            answer["stored"] = False
        results.append(answer)
        say("[%d/%d] %s %s: %s -> %s (%.1fs, %d kB)"
            % (position, len(rows), key, row["unit"],
               row["pass1_word"], word, wall, child))
        check_parent_memory()
    changed = [r for r in results if r["answer_changed"]]
    stored = [r for r in results if r["stored"]]
    stuck = [r for r in results if not r["stored"]]
    say("")
    say("-- PASS 2 over %d flagged units" % len(results))
    say("   changed answer %d" % len(changed))
    say("   now stored     %d" % len(stored))
    say("   still not finished %d" % len(stuck))
    directions = {}
    for r in results:
        word = "%s -> %s" % (r["pass1_word"], r["pass2_word"])
        directions[word] = directions.get(word, 0) + 1
    say("   directions %s" % json.dumps(directions, sort_keys=True))
    out_path = os.path.join(HERE,
                            "term97_pass2_%s_slice%d.json"
                            % (part, index))
    handle = open(out_path, "w")
    json.dump({"part": part,
               "slice": index,
               "slice_count": count,
               "source": source,
               "ceiling_mb": ceiling,
               "seconds": seconds,
               "flagged": len(results),
               "changed_answer": len(changed),
               "now_stored": len(stored),
               "still_not_finished": len(stuck),
               "directions": directions,
               "parent_peak_kb": peak_kb(),
               "rows": results}, handle, indent=1, sort_keys=True)
    handle.close()
    say("-- wrote %s" % os.path.basename(out_path))


def control(ceiling, seconds, every):
    """the other half of the owner's rule: does the LARGER budget change an
    answer that the ORDINARY budget already produced?  Every `every`th
    stored record is re-run at the pass-2 budget and compared field for
    field against what is stored."""
    say("-- THE CONTROL: every %dth stored record re-run at the pass-2 "
        "budget" % every)
    say("   ceiling %d MB, wall clock %d s" % (ceiling, seconds))
    maker, gate, attached, readings = build()
    documents = {}
    rows = []
    position = 0
    for path in sorted(glob.glob(os.path.join(STORE, "*.json"))):
        stored = json.load(open(path))
        key = stored["shard"]
        for name in sorted(stored["units"]):
            position = position + 1
            if position % every != 0:
                continue
            if key not in documents:
                documents[key] = json.load(
                    open(os.path.join(HERE, key)))
            unit = documents[key]["units"][name]
            word, record, wall, child, token = one_unit_forked(
                maker, gate, name, unit, ceiling, seconds)
            same = None
            fields = []
            if word == "walked":
                same = (json.dumps(record, sort_keys=True)
                        == json.dumps(stored["units"][name],
                                      sort_keys=True))
                if not same:
                    for field in sorted(set(list(record)
                                            + list(stored["units"][name]))):
                        if record.get(field) != \
                                stored["units"][name].get(field):
                            fields.append(field)
            rows.append({"shard": key, "unit": name, "word": word,
                         "identical": same, "fields_that_differ": fields,
                         "wall_seconds": round(wall, 3),
                         "child_peak_kb": child})
            check_parent_memory()
    identical = [r for r in rows if r["identical"] is True]
    differ = [r for r in rows if r["identical"] is False]
    say("   records compared %d" % len(rows))
    say("   records identical %d" % len(identical))
    say("   records that differ %d" % len(differ))
    for r in differ[:40]:
        say("      %s/%s  fields %s"
            % (r["shard"], r["unit"], r["fields_that_differ"]))
    out_path = os.path.join(HERE, "term97_control.json")
    handle = open(out_path, "w")
    json.dump({"ceiling_mb": ceiling, "seconds": seconds,
               "every": every,
               "compared": len(rows),
               "identical": len(identical),
               "differ": len(differ),
               "rows": rows}, handle, indent=1, sort_keys=True)
    handle.close()
    say("-- wrote term97_control.json")


def finalize():
    """`term66_state.json` is written from the STORE itself: an input
    is done when every unit canon40 proves in it has a record.  An
    input still short of one is left out, so a later resume picks it
    up rather than reading a gap as an answer."""
    done = []
    short = []
    total = 0
    for path in TR.shards():
        key = os.path.relpath(path, HERE)
        written = store_path(key)
        if not os.path.exists(written):
            short.append({"shard": key, "missing": "no store shard"})
            continue
        document = json.load(open(path))
        stored = json.load(open(written))
        wanted = []
        for name in sorted(document.get("units", {})):
            if document["units"][name].get("outcome") != TR.PROVED:
                continue
            wanted.append(name)
        missing = [n for n in wanted if n not in stored["units"]]
        total = total + len(stored["units"])
        if missing:
            short.append({"shard": key, "missing_units": missing})
            continue
        done.append(key)
    say("-- FINALIZE")
    say("   inputs complete %d of %d" % (len(done), len(TR.shards())))
    say("   inputs short    %d" % len(short))
    say("   records in the store %d" % total)
    for row in short[:40]:
        say("      %s" % json.dumps(row, sort_keys=True))
    state = json.load(open(STATE))
    state["done"] = sorted(done)
    handle = open(STATE, "w")
    json.dump(state, handle, indent=1, sort_keys=True)
    handle.close()
    say("-- term66_state.json now lists %d done inputs" % len(done))
    report = os.path.join(HERE, "term97_finalize.json")
    handle = open(report, "w")
    json.dump({"inputs_total": len(TR.shards()),
               "inputs_complete": len(done),
               "inputs_short": short,
               "records_in_store": total}, handle, indent=1,
              sort_keys=True)
    handle.close()
    say("-- wrote term97_finalize.json")


def main():
    what = sys.argv[1]
    if what == "pass1":
        pass1(int(sys.argv[2]), float(sys.argv[3]),
              int(sys.argv[4]), int(sys.argv[5]))
        return
    if what == "pass2":
        pass2(int(sys.argv[2]), float(sys.argv[3]), sys.argv[4],
              int(sys.argv[5]), int(sys.argv[6]), sys.argv[7])
        return
    if what == "control":
        control(int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))
        return
    if what == "finalize":
        finalize()
        return
    raise SystemExit("unknown mode %r" % what)


if __name__ == "__main__":
    main()
