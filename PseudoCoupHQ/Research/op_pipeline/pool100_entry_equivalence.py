#!/usr/bin/env python3
"""pool100_entry_equivalence.py -- TASK 100, master plan step 2: solver
equivalence BETWEEN pool entries, inside each machine type key.

WHAT THE OBJECTS ARE, one sentence each, in relation.
  An ENTRY is one distinct computation in `the_pool5.json` (1,831 of
  them over 30,432 members); it carries `type_key` (arrival register
  families | answer width), its members, and its representative (the
  member with the fewest assembled bytes).
  A TERM is a unit's computation as a z3 expression, built from the
  unit's ledger by `term.Term.transcribe` -- the function
  `term66_run.one_unit` calls -- over the unit's canon40 record.
  A PAIR is two entries of one type key; this program builds the term
  of each entry's representative, asserts the two terms differ, and
  asks the gate's own solver call (`gate.Gate.decide`, 3,000 ms).
  An EDGE is a pair the solver PROVED equal (unsat) whose two terms
  were each proved against their own unit's ship body.
  The POOL6 CANDIDATE is pool5's entries closed under the edges by
  transitivity -- a candidate for the owner to ratify, never `the_pool6.json`.

WHAT IS MISSING FROM THE POOL TODAY, and what this supplies.  The pool
merges on identical wrapped text, on identical layer-5 text among
proved terms, and on banked proved edges (118).  Two entries whose
layer-5 texts DIFFER but whose terms are equal for every input stay
apart.  This program proves or disproves each such pair, term against
term, and records every outcome.

WHAT IS REUSED RATHER THAN COPIED.  `term97_walk.build` builds the
`Reference`, the `Term` and the `Gate` exactly as task 97 did, once, in
the collecting process.  `term.Term.transcribe` builds the layer-4
term; `regate64_run.why_no_term` words a missing one; `gate.Gate.decide`
is the one solver call (the negation of equality: unsat = proved, sat =
counterexample with the seed values, unknown = undecided).  Nothing
existing is edited.

WHY ONE FORKED SUB-PROCESS PER PAIR.  Task 97 measured that the cost of
a term walk is the LIFETIME of the z3 context, not the unit (log_202
section 2): a pristine collecting process that forks one sub-process
per unit ran 24 records in 13.4 s where one long-lived process took
1,112 s.  The same arrangement is used here per pair.  The collecting
process does no z3 work after setup: it forks, reads one JSON payload
back, and records.

HOW THE INPUTS ARE ALIGNED: BY ROW IN-i, as the ledger does.
`Term.input_symbol` names row IN-i by the i-th arrival family
(`seed_<family>`).  The pair's two terms are aligned by ROW: on each
side, the symbol of IN-i is substituted by one common symbol `IN_i`
of that row's width, so IN-0 of one representative is IN-0 of the
other whatever register either compiler chose.  The pair is refused
(UNBUILDABLE, by cause) when the two sides' IN rows differ in count or
in width, or the answer widths differ.  WHY BY ROW AND NOT BY REGISTER
NAME, measured in the sample lane (t100_l2): `the_pool5.json`'s
`type_key` was read off canon39, where a go body was renamed onto the
C calling rule; canon40 keeps every body verbatim, so `go/op_312`
(E00025, pool5 key `rdi,rsi|32`) arrives in `rax,rbx` under canon40
while its c and cpp co-entries arrive in `rdi,rsi`.  Both canon40
family lists are recorded on every pair.  Free symbols that are NOT
inputs are classified and recorded on the pair: a memory cell read by
literal address (`seed_MEM_*`) and the entry stack pointer
(`seed_rsp`) are shared, because both units see one memory and one
stack; a register a body reads before writing that is not one of its
arrival rows keeps its `seed_<family>` name and is shared, because
after the IN substitution no input symbol can collide with it; a
constant-pool read (`ripconst_k`, the k-th rip-relative read of a
body, a value this artifact does not hold) is RENAMED APART per side,
because unit A's k-th constant is not unit B's k-th constant.  A proof
under renamed constants is universal over them, so it is sound; a
counterexample that assigns one is recorded as such and counted by
cause.

WHEN AN EDGE APPLIES.  A solver proof of `term_a == term_b` is a fact
about the two TERMS.  It is a fact about the two UNITS only when each
term was proved equal to its own unit's ship body (the pool rule:
"only a PROVED term counts; an unproved term is not a weaker key, it
is no key").  So every pair carries both terms' own verdicts, read from
`term66_store` (the gate of record over canon40) or, for a
representative without a store record, gated in the sub-process by the
same two routes `term66_run.one_unit` asks, in the same order, with
the layer-5 step left out (it does not converge for 44 units).  A
PROVED pair with an unproved term is recorded as PROVED and NOT applied
to the closure; the count is reported.

THE BOUND (brief section 2.3).  Total pairs x 3 s over the worker
count against four hours: when it exceeds, the 20 largest groups run
in full first, then the rest in pair-count order until the budget, and
the report names exactly which groups are complete.  The order is
fixed in `plan` before any solver runs.

THE MEMORY BOUND, stated as the round requires.  Per sub-process:
RLIMIT_AS at the stated ceiling (1,536 MB in the pair lane, the value
task 97 measured identical records at).  Per collecting process: 6 GB,
checked after every pair, with the named abort ABORT_MEMORY_T100.  The
collecting process holds only the plan and the representatives' records
(one file, streamed out of the canon40 shards once, in `plan`).

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

No operator token appears in this file.  The candidate set is every
unordered pair of entries sharing one `type_key` -- a machine-form key
(arrival register families | answer width) -- and nothing else.  A
member's `operator` field rides along verbatim from `the_pool5.json`
as a display label and is read by nothing here.  `close` runs
`check_no_spelling_keys.py`, unmodified, over every JSON this program
writes and deletes its own edge and candidate files on failure.

usage:
  pool100_entry_equivalence.py plan
  pool100_entry_equivalence.py sample <pairs> <ceiling MB> <seconds>
  pool100_entry_equivalence.py pairs <slice> <count> <ceiling MB> <seconds> <budget seconds>
  pool100_entry_equivalence.py retry <ceiling MB> <seconds>
  pool100_entry_equivalence.py close
"""

import glob
import json
import os
import resource
import signal
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gate as G                                                 # noqa: E402
import reference as R                                            # noqa: E402
import regate64_run as RG                                        # noqa: E402
import term as T                                                 # noqa: E402
import term66_run as TR                                          # noqa: E402
import term97_walk as TW                                         # noqa: E402
import z3                                                        # noqa: E402

POOL5 = os.path.join(HERE, "the_pool5.json")
PLAN = os.path.join(HERE, "pool100_plan.json")
REPRESENTATIVES = os.path.join(HERE, "pool100_representatives.json")
SAMPLE = os.path.join(HERE, "pool100_sample.json")
SLICE_PATTERN = os.path.join(HERE, "pool100_pairs_slice*.json")
RETRY = os.path.join(HERE, "pool100_pairs_retry.json")
EDGES = os.path.join(HERE, "pool100_edges.json")
CANDIDATE = os.path.join(HERE, "pool100_pool6_candidate.json")
REPORT = os.path.join(HERE, "pool100_report.md")
GUARD = os.path.join(HERE, "check_no_spelling_keys.py")
THE_44 = os.path.join(HERE, "term97_pass2_b_slice0.json")

COLLECTOR_CAP_KB = 6 * 1024 * 1024
LARGEST_GROUPS_FIRST = 20
FOUR_HOURS = 4 * 3600

# the pair's four states, the brief's words.  The gate's five verdict
# outcomes ride inside `verdict` unchanged.
PROVED = "PROVED"
DISPROVED = "DISPROVED"
UNDECIDED = "UNDECIDED"
UNBUILDABLE = "UNBUILDABLE"

ROUTE = ("the representative's term of one entry against the "
         "representative's term of another entry of the same machine "
         "type key")
PROVED_REASON = ("z3 proved the two representatives' ledger-transcribed "
                 "OUT-0 terms equal for every value of every input row")


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_collector_memory():
    used = peak_kb()
    if used > COLLECTOR_CAP_KB:
        raise SystemExit(
            "ABORT_MEMORY_T100: the collecting process's peak resident "
            "%d kB passed the stated cap of %d kB"
            % (used, COLLECTOR_CAP_KB))
    return used


def write_json(path, document):
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()


def read_json(path):
    handle = open(path)
    document = json.load(handle)
    handle.close()
    return document


# ==================================================================
# plan: the candidate set, counted before anything runs
# ==================================================================

def group_entries(entries):
    """entries -> {type_key: [entry_id, ...]} in pool order."""
    groups = {}
    for entry in entries:
        key = entry["type_key"]
        if key not in groups:
            groups[key] = []
        groups[key].append(entry["entry_id"])
    return groups


def pair_count(size):
    return size * (size - 1) // 2


def ordered_groups(groups):
    """the run order: the LARGEST_GROUPS_FIRST groups by pair count in
    full first, then the rest in pair-count order.  Ties by type_key
    text, so the order is a function of the data alone."""
    rows = []
    for key in groups:
        rows.append((pair_count(len(groups[key])), key))
    rows.sort(key=lambda row: (-row[0], row[1]))
    out = []
    rank = 0
    for pairs, key in rows:
        rank = rank + 1
        out.append({
            "rank": rank,
            "type_key": key,
            "entries": groups[key],
            "entry_count": len(groups[key]),
            "pair_count": pairs,
            "in_the_first_twenty": rank <= LARGEST_GROUPS_FIRST,
        })
    return out


def pairs_of(group):
    """every unordered pair of the group's entries, in pool order."""
    out = []
    ids = group["entries"]
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            out.append((ids[i], ids[j]))
    return out


def the_44_units():
    document = read_json(THE_44)
    units = []
    for row in document["rows"]:
        if row["stored"]:
            continue
        units.append(row["unit"])
    return sorted(units)


def plan():
    say("-- PLAN: the candidate set, counted before anything runs")
    pool = read_json(POOL5)
    entries = pool["entries"]
    say("   pool5 entries %d, members %d"
        % (len(entries), pool["summary"]["members"]))
    groups = group_entries(entries)
    order = ordered_groups(groups)
    total = 0
    for group in order:
        total = total + group["pair_count"]
    say("   type keys %d" % len(groups))
    say("   pairs total %d" % total)
    say("   pairs in the %d largest groups %d"
        % (LARGEST_GROUPS_FIRST,
           sum(g["pair_count"] for g in order
               if g["in_the_first_twenty"])))
    say("   groups with one entry (no pair) %d"
        % len([g for g in order if g["pair_count"] == 0]))
    workers = 6
    seconds_if_every_pair_took_the_ceiling = total * 3.0 / workers
    say("   bound: %d pairs x 3 s / %d workers = %.0f s = %.2f h "
        "against 4 h"
        % (total, workers, seconds_if_every_pair_took_the_ceiling,
           seconds_if_every_pair_took_the_ceiling / 3600.0))
    bound_fires = seconds_if_every_pair_took_the_ceiling > FOUR_HOURS
    if bound_fires:
        say("   the bound FIRES: the %d largest groups run in full "
            "first, then the rest in pair-count order until the "
            "four-hour budget" % LARGEST_GROUPS_FIRST)
    else:
        say("   the bound does not fire: every group runs")
    say("   the 20 largest groups (type_key, entries, pairs):")
    for group in order[:LARGEST_GROUPS_FIRST]:
        say("      [%2d] %-28s %4d entries %6d pairs"
            % (group["rank"], group["type_key"], group["entry_count"],
               group["pair_count"]))
    # the compact per-entry rows the workers read
    by_id = {}
    entry_of_unit = {}
    for entry in entries:
        by_id[entry["entry_id"]] = {
            "entry_id": entry["entry_id"],
            "type_key": entry["type_key"],
            "representative": entry["representative"],
            "representative_size": entry["representative_size"],
            "member_count": entry["member_count"],
            "languages": entry["languages"],
            "layer5_normalized_texts": entry["layer5_normalized_texts"],
            "members_not_layer5_eligible":
                entry["members_not_layer5_eligible"],
        }
        for member in entry["members"]:
            entry_of_unit[member["unit"]] = entry["entry_id"]
    the_44 = the_44_units()
    entries_of_the_44 = {}
    for unit in the_44:
        entries_of_the_44[unit] = entry_of_unit.get(unit)
    reached_entries = sorted(set(
        e for e in entries_of_the_44.values() if e is not None))
    say("   the 44 non-converging units: %d, in %d pool5 entries "
        "(%d not members of pool5)"
        % (len(the_44), len(reached_entries),
           len([u for u in the_44 if entries_of_the_44[u] is None])))
    wanted = set()
    for entry in entries:
        wanted.add(entry["representative"])
    del pool
    del entries
    say("-- the representatives' canon40 records, streamed out of the "
        "shards one at a time")
    records = {}
    shards = TR.shards()
    position = 0
    for path in shards:
        position = position + 1
        key = os.path.relpath(path, HERE)
        document = read_json(path)
        store_path = TW.store_path(key)
        store = None
        if os.path.exists(store_path):
            store = read_json(store_path)
        found = 0
        for name in document.get("units", {}):
            if name not in wanted:
                continue
            unit = document["units"][name]
            stored = None
            if store is not None:
                stored = store["units"].get(name)
            records[name] = {
                "shard": key,
                "canon40_outcome": unit.get("outcome"),
                "record": unit,
                "store": stored,
            }
            found = found + 1
        del document
        del store
        say("[%d/%d] %s: %d representatives, collector peak %d kB"
            % (position, len(shards), key, found, peak_kb()))
        check_collector_memory()
    missing = sorted(wanted - set(records))
    say("   representatives wanted %d, found in canon40 %d, absent %d"
        % (len(wanted), len(records), len(missing)))
    outcomes = {}
    with_store = 0
    for name in records:
        word = records[name]["canon40_outcome"]
        outcomes[word] = outcomes.get(word, 0) + 1
        if records[name]["store"] is not None:
            with_store = with_store + 1
    say("   canon40 outcomes over the representatives %s"
        % json.dumps(outcomes, sort_keys=True))
    say("   representatives with a term66_store record %d" % with_store)
    write_json(REPRESENTATIVES, {
        "meta": {
            "generator": "pool100_entry_equivalence.py plan",
            "what": "the canon40 record and the term66_store record "
                    "of every pool5 representative, copied verbatim "
                    "out of the shards so a worker holds one small "
                    "file instead of the corpus",
            "source_shards": "term66_run.shards() order",
            "absent_from_canon40": missing,
        },
        "units": records,
    })
    write_json(PLAN, {
        "meta": {
            "generator": "pool100_entry_equivalence.py plan",
            "pool": "the_pool5.json",
            "candidate_set": "every unordered pair of entries sharing "
                             "one type_key (arrival register families "
                             "| answer width); nothing else",
            "order": "the %d largest groups by pair count first, then "
                     "the rest in pair-count order; ties by type_key "
                     "text" % LARGEST_GROUPS_FIRST,
            "bound_fires": bound_fires,
            "seconds_if_every_pair_took_the_ceiling":
                seconds_if_every_pair_took_the_ceiling,
            "workers_assumed": workers,
        },
        "pairs_total": total,
        "groups": order,
        "entries": by_id,
        "the_44_units": the_44,
        "entries_of_the_44": entries_of_the_44,
        "representatives_absent_from_canon40": missing,
    })
    say("-- wrote pool100_plan.json and pool100_representatives.json")
    say("   collector peak %d kB" % peak_kb())


# ==================================================================
# the sub-process: two terms, one solver call
# ==================================================================

def classify_symbols(term, families):
    """the free symbols of a term, sorted into the four kinds the
    module docstring names."""
    inputs = []
    shared = []
    constants = []
    other = []
    for symbol in T.free_symbols_in_order(term):
        name = symbol.decl().name()
        if name.startswith("ripconst_"):
            constants.append(symbol)
            continue
        if name.startswith("seed_MEM_"):
            shared.append(name)
            continue
        if name == "seed_rsp":
            shared.append(name)
            continue
        if name.startswith("seed_"):
            family = name[len("seed_"):]
            if family in families:
                inputs.append(name)
                continue
            other.append(name)
            continue
        other.append(name)
    return inputs, shared, constants, other


def family_bits(family):
    if family in R.XMM_NAMES:
        return 128
    return 64


def input_rows(families):
    """the IN rows one side's arrival contract names, with the width
    `term.seed_of` gives each."""
    rows = []
    for index, family in enumerate(families):
        rows.append({
            "row": "IN-%d" % index,
            "family": family,
            "bits": family_bits(family),
        })
    return rows


def align_by_row(term, rows):
    """IN-i's `seed_<family>` -> the common symbol `IN_i` of the row's
    width, on one side.

    TASK ap5, and it is the ONE change this brief authorises in this
    file: an arrival whose place is the x87 register stack is aligned
    by its IN row like any other.  Such an arrival is not a bit
    pattern -- the model table preseeds the stack as
    `seed_X87_0` / `seed_X87_1` at `reference.X87_SORT`, an 80-bit
    extended float -- so the `z3.BitVec` this function built for it
    was a DIFFERENT constant from the one in the term and the
    substitution silently did nothing, which is why task ap4 built
    those rows in the driver instead.  The row's `bits` field is the
    width `family_bits` gives every family that is not a vector one
    and is not read for an x87 row, because an x87 arrival's width is
    its sort's.

    THE TEST IS THE DRIVER'S OWN, and it is BOTH spellings.  An x87
    arrival reaches a row under two names and the pipeline already
    says so in `emulate.X87_ARRIVAL`: `X87_<k>` is a stack POSITION
    the model table preseeded, and `x87_<mangled operand>` is a
    literal memory operand read at the x87 sort
    (`reference.x87_symbol`), which `handful.x87_as_arrivals` re-reads
    as an arrival of the same sort.  A first draft of this branch
    tested only the first spelling; the loop's own measurement is what
    caught it -- 30 `mem_one` 80 cells on c, whose second arrival is
    the memory one, left `seed_x87__rsi_` free on the cell side while
    the body side was on `IN_1`, and z3 answered `sat` with that
    symbol in the counterexample."""
    substitution = []
    for index, row in enumerate(rows):
        family = row["family"] or ""
        if family.startswith("X87_") or family.startswith("x87_"):
            seed = z3.Const("seed_%s" % family, R.X87_SORT)
            common = z3.Const("IN_%d" % index, R.X87_SORT)
            substitution.append((seed, common))
            continue
        seed = z3.BitVec("seed_%s" % row["family"], row["bits"])
        common = z3.BitVec("IN_%d" % index, row["bits"])
        substitution.append((seed, common))
    if not substitution:
        return term
    return z3.substitute(term, *substitution)


def rows_disagree(rows_a, rows_b):
    """the cause text when two sides' IN rows cannot be aligned, or
    None when they can."""
    if len(rows_a) != len(rows_b):
        return ("the two representatives' canon40 arrival contracts "
                "name %d and %d IN rows" % (len(rows_a), len(rows_b)))
    for index in range(len(rows_a)):
        if rows_a[index]["bits"] != rows_b[index]["bits"]:
            return ("IN-%d is %d bits wide (%s) on one side and %d bits "
                    "(%s) on the other"
                    % (index, rows_a[index]["bits"],
                       rows_a[index]["family"], rows_b[index]["bits"],
                       rows_b[index]["family"]))
    return None


def rename_constants_apart(term, constants, side):
    if not constants:
        return term, []
    substitution = []
    names = []
    for symbol in constants:
        fresh = z3.BitVec("%s_%s" % (symbol.decl().name(), side),
                          symbol.size())
        substitution.append((symbol, fresh))
        names.append(symbol.decl().name())
    return z3.substitute(term, *substitution), names


def term_of(maker, gate, name, held):
    """one representative -> (term, note).  `note` carries the term's
    own verdict against its unit's ship body, or the cause of NO_TERM."""
    unit = dict(held["record"])
    unit["unit"] = name
    note = {
        "unit": name,
        "shard": held["shard"],
        "canon40_outcome": held["canon40_outcome"],
        "arrival_families": list(unit.get("arrival_families") or []),
        "result_width": unit.get("result_width"),
    }
    walked = maker.transcribe(unit)
    if walked.refused is not None:
        note["term_state"] = "NO_TERM"
        note["why_no_term"] = "the relink refused: %s" % walked.refused
        return None, note
    if walked.out_term is None:
        note["term_state"] = "NO_TERM"
        note["why_no_term"] = RG.why_no_term(walked)
        return None, note
    note["term_state"] = "TERM"
    note["holes"] = len(walked.holes)
    stored = held.get("store")
    if stored is not None and "proved" in stored:
        note["own_verdict_source"] = "term66_store"
        note["own_outcome"] = stored.get("outcome")
        note["own_route"] = stored.get("route")
        note["proved_against_own_body"] = bool(stored.get("proved"))
        note["layer5_normalized_text"] = stored.get(
            "layer5_normalized_text")
        return walked.out_term, note
    # no store record: the two routes term66_run.one_unit asks, in its
    # order, layer 5 left out
    first = gate.prove_term_against_ship(walked.out_term, unit)
    verdict = first
    if not first.proved():
        second = gate.prove_term_against_text(walked.out_term, unit)
        if second.proved():
            verdict = second
    note["own_verdict_source"] = (
        "gated in this lane: term66_run.one_unit's two routes in its "
        "order, layer 5 left out")
    note["own_outcome"] = verdict.outcome
    note["own_route"] = verdict.route
    note["own_reason"] = verdict.reason
    note["proved_against_own_body"] = verdict.proved()
    note["layer5_normalized_text"] = None
    return walked.out_term, note


def one_pair(maker, gate, plan_entries, held, left, right):
    """the whole of a pair's work, run inside the forked sub-process."""
    record = {"a": left, "b": right}
    rep_a = plan_entries[left]["representative"]
    rep_b = plan_entries[right]["representative"]
    record["rep_a"] = rep_a
    record["rep_b"] = rep_b
    if rep_a not in held or rep_b not in held:
        record["state"] = UNBUILDABLE
        absent = []
        if rep_a not in held:
            absent.append(rep_a)
        if rep_b not in held:
            absent.append(rep_b)
        record["cause"] = ("representative absent from canon40: %s"
                           % ", ".join(absent))
        return record
    term_a, note_a = term_of(maker, gate, rep_a, held[rep_a])
    term_b, note_b = term_of(maker, gate, rep_b, held[rep_b])
    record["term_a"] = note_a
    record["term_b"] = note_b
    if term_a is None or term_b is None:
        record["state"] = UNBUILDABLE
        causes = []
        if term_a is None:
            causes.append("a: %s" % note_a["why_no_term"])
        if term_b is None:
            causes.append("b: %s" % note_b["why_no_term"])
        record["cause"] = "NO_TERM -- " + "; ".join(causes)
        return record
    rows_a = input_rows(note_a["arrival_families"])
    rows_b = input_rows(note_b["arrival_families"])
    record["arrival_families_under_canon40"] = {
        "a": note_a["arrival_families"], "b": note_b["arrival_families"]}
    record["arrival_families_agree_by_name"] = (
        note_a["arrival_families"] == note_b["arrival_families"])
    disagreement = rows_disagree(rows_a, rows_b)
    if disagreement is not None:
        record["state"] = UNBUILDABLE
        record["cause"] = ("the IN rows cannot be aligned: %s"
                           % disagreement)
        return record
    if note_a["result_width"] != note_b["result_width"]:
        record["state"] = UNBUILDABLE
        record["cause"] = (
            "the two representatives' canon40 answer widths differ "
            "(%s against %s); pool5's type key was read off canon39"
            % (note_a["result_width"], note_b["result_width"]))
        return record
    inputs_a, shared_a, constants_a, other_a = classify_symbols(
        term_a, note_a["arrival_families"])
    inputs_b, shared_b, constants_b, other_b = classify_symbols(
        term_b, note_b["arrival_families"])
    term_a = align_by_row(term_a, rows_a)
    term_b = align_by_row(term_b, rows_b)
    term_a, renamed_a = rename_constants_apart(term_a, constants_a, "a")
    term_b, renamed_b = rename_constants_apart(term_b, constants_b, "b")
    record["inputs"] = []
    for index in range(len(rows_a)):
        record["inputs"].append({
            "row": "IN-%d" % index,
            "symbol": "IN_%d" % index,
            "bits": rows_a[index]["bits"],
            "family_a": rows_a[index]["family"],
            "family_b": rows_b[index]["family"],
            "read_by_a": ("seed_%s" % rows_a[index]["family"]) in inputs_a,
            "read_by_b": ("seed_%s" % rows_b[index]["family"]) in inputs_b,
        })
    record["answer_width"] = note_a["result_width"]
    record["term_widths"] = [term_a.size(), term_b.size()]
    record["shared_symbols"] = {"a": shared_a, "b": shared_b}
    record["constant_pool_symbols_renamed_apart"] = {
        "a": renamed_a, "b": renamed_b}
    record["other_free_symbols"] = {"a": other_a, "b": other_b}
    verdict = gate.decide(term_a, term_b, ROUTE, PROVED_REASON)
    record["verdict"] = verdict.as_dict()
    if verdict.proved():
        record["state"] = PROVED
    elif verdict.outcome == G.DISPROVED:
        record["state"] = DISPROVED
        record["counterexample"] = verdict.counterexample
        record["counterexample_assigns_a_constant_pool_symbol"] = (
            "ripconst_" in (verdict.counterexample or ""))
    else:
        record["state"] = UNDECIDED
        record["cause"] = verdict.reason
    both = note_a["proved_against_own_body"] and \
        note_b["proved_against_own_body"]
    record["both_terms_proved_against_own_body"] = both
    record["edge_applies"] = (record["state"] == PROVED) and both
    return record


def _alarm(signum, frame):
    raise TimeoutError()


def one_pair_forked(maker, gate, plan_entries, held, left, right,
                    ceiling_mb, seconds):
    """one pair answered in a forked sub-process of its own; the
    arrangement of `term97_walk.one_unit_forked`.

    Returns (word, record_or_None, wall_seconds, sub_peak_kb).  `word`
    is walked / TIMED_OUT / ABORTED / RAISED."""
    read_end, write_end = os.pipe()
    started = time.time()
    sub_pid = os.fork()
    if sub_pid == 0:
        os.close(read_end)
        try:
            cap = ceiling_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
            record = one_pair(maker, gate, plan_entries, held, left,
                              right)
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
        # stopped from outside, so a spent budget can never be written
        # down as a solver verdict
        os.kill(sub_pid, signal.SIGKILL)
    stamp = os.wait4(sub_pid, 0)
    wall = time.time() - started
    sub_peak = stamp[2].ru_maxrss
    if timed_out:
        return "TIMED_OUT", None, wall, sub_peak
    if text == "":
        return "ABORTED", None, wall, sub_peak
    answer = json.loads(text)
    if not answer["ok"]:
        return "RAISED", {"raised": answer["raised"]}, wall, sub_peak
    return "walked", answer["record"], wall, sub_peak


def runner_limit_record(left, right, plan_entries, word, record, wall,
                        sub_peak, ceiling_mb, seconds):
    """a pair the RUNNER stopped, recorded as a runner limit and never
    as a solver verdict.  It is UNDECIDED by a runner cause; the retry
    mode re-runs it with more room."""
    out = {
        "a": left,
        "b": right,
        "rep_a": plan_entries[left]["representative"],
        "rep_b": plan_entries[right]["representative"],
        "state": UNDECIDED,
        "cause": "runner limit: %s (sub-process ceiling %d MB, wall "
                 "clock %d s)" % (word, ceiling_mb, seconds),
        "runner_word": word,
    }
    if record is not None:
        out["raised"] = record.get("raised")
    return out


# ==================================================================
# the collecting process
# ==================================================================

def load_plan_and_held():
    plan_document = read_json(PLAN)
    representatives = read_json(REPRESENTATIVES)
    return plan_document, representatives["units"]


def all_pairs_in_order(plan_document):
    out = []
    for group in plan_document["groups"]:
        for left, right in pairs_of(group):
            out.append((group["type_key"], left, right))
    return out


def finish_record(record, word, wall, sub_peak, type_key, ceiling_mb,
                  seconds):
    record["type_key"] = type_key
    record["runner_word"] = word
    record["wall_seconds"] = round(wall, 3)
    record["sub_peak_kb"] = sub_peak
    record["sub_ceiling_mb"] = ceiling_mb
    record["sub_seconds"] = seconds
    return record


def run_pairs(pairs, ceiling_mb, seconds, budget, out_path, label,
              resume_from=None):
    """walk `pairs` (type_key, a, b) in order, one sub-process each,
    inside `budget` seconds of wall clock; write `out_path`.

    RESUME (added 2026-09-06, lane t100_l5, after lane t100_l4 was
    stopped from outside at 4,558 s): `resume_from` is the unfinished
    slice document already on disk.  Its results are kept, each
    checked against the pair it must answer (same type_key, a, b, by
    position), and the walk continues at the first unanswered pair.
    `budget` is this run's wall clock; `wall_seconds` in the written
    document accumulates over the runs."""
    plan_document, held = load_plan_and_held()
    plan_entries = plan_document["entries"]
    say("   setup: building Reference, Term, Gate once")
    maker, gate, attached, readings = TW.build()
    say("   attached callee units %d, runtime answer readings %d"
        % (len(attached), len(readings)))
    say("   sub-process ceiling %d MB, sub-process wall clock %d s, "
        "budget %d s" % (ceiling_mb, seconds, budget))
    results = []
    wall_before = 0.0
    if resume_from is not None:
        results = list(resume_from["results"])
        wall_before = float(resume_from.get("wall_seconds") or 0.0)
        for k in range(len(results)):
            answered = results[k]
            owed = pairs[k]
            if (answered["type_key"], answered["a"], answered["b"]) != owed:
                raise SystemExit(
                    "REFUSED RESUME: result %d of %s answers %s but the "
                    "slice owes %s at that position"
                    % (k, label, (answered["type_key"], answered["a"],
                                  answered["b"]), owed))
        say("   resuming %s at pair %d of %d (%d already answered, "
            "%.0f s of wall clock before this run)"
            % (label, len(results) + 1, len(pairs), len(results),
               wall_before))
    started = time.time() - wall_before
    stopped_by_budget = False
    position = len(results)
    group_key = None
    group_index = 0
    group_total = 0
    words = {}
    states = {}
    for record in results:
        word = record.get("runner_word")
        words[word] = words.get(word, 0) + 1
        states[record["state"]] = states.get(record["state"], 0) + 1
    if results:
        group_key = results[-1]["type_key"]
        group_index = len([r for r in results if r["type_key"] == group_key])
        group_total = len([p for p in pairs if p[0] == group_key])
        say("-- group %s: resumed at %d of %d pairs in this slice"
            % (group_key, group_index, group_total))
    for type_key, left, right in pairs[len(results):]:
        if time.time() - started - wall_before > budget:
            stopped_by_budget = True
            break
        position = position + 1
        if type_key != group_key:
            group_key = type_key
            group_index = 0
            group_total = len([p for p in pairs if p[0] == type_key])
            say("-- group %s: %d pairs in this slice" % (type_key,
                                                          group_total))
        group_index = group_index + 1
        word, record, wall, sub_peak = one_pair_forked(
            maker, gate, plan_entries, held, left, right, ceiling_mb,
            seconds)
        if word != "walked":
            record = runner_limit_record(left, right, plan_entries, word,
                                         record, wall, sub_peak,
                                         ceiling_mb, seconds)
        record = finish_record(record, word, wall, sub_peak, type_key,
                               ceiling_mb, seconds)
        results.append(record)
        words[word] = words.get(word, 0) + 1
        states[record["state"]] = states.get(record["state"], 0) + 1
        say("[%d/%d] %s %s %s: %s %s (%.2fs, %d kB)"
            % (group_index, group_total, type_key, left, right,
               record["state"], record.get("cause", "")[:70], wall,
               sub_peak))
        check_collector_memory()
        if position % 200 == 0:
            write_json(out_path, slice_document(
                label, results, pairs, stopped_by_budget, started,
                ceiling_mb, seconds, budget, finished=False))
    write_json(out_path, slice_document(
        label, results, pairs, stopped_by_budget, started, ceiling_mb,
        seconds, budget, finished=True))
    say("")
    say("-- %s: %d of %d pairs answered, wall %.0f s, collector peak "
        "%d kB, stopped by budget %s"
        % (label, len(results), len(pairs), time.time() - started,
           peak_kb(), stopped_by_budget))
    say("   runner words %s" % json.dumps(words, sort_keys=True))
    say("   pair states  %s" % json.dumps(states, sort_keys=True))
    return results


def slice_document(label, results, pairs, stopped, started, ceiling_mb,
                   seconds, budget, finished):
    return {
        "label": label,
        "pairs_owned": len(pairs),
        "pairs_answered": len(results),
        "stopped_by_budget": stopped,
        "finished": finished,
        "wall_seconds": round(time.time() - started, 1),
        "sub_ceiling_mb": ceiling_mb,
        "sub_seconds": seconds,
        "budget_seconds": budget,
        "collector_peak_kb": peak_kb(),
        "results": results,
    }


def sample(count, ceiling_mb, seconds):
    say("-- SAMPLE: the first %d pairs of the plan's order, one "
        "collecting process" % count)
    plan_document, _held = load_plan_and_held()
    pairs = all_pairs_in_order(plan_document)[:count]
    results = run_pairs(pairs, ceiling_mb, seconds, FOUR_HOURS, SAMPLE,
                        "sample")
    walls = sorted(r["wall_seconds"] for r in results)
    peaks = sorted(r["sub_peak_kb"] for r in results)
    total = plan_document["pairs_total"]
    if walls:
        mean = sum(walls) / len(walls)
        say("   wall per pair: min %.2f  mean %.2f  max %.2f s"
            % (walls[0], mean, walls[-1]))
        say("   sub-process peak: min %d  max %d kB" % (peaks[0],
                                                         peaks[-1]))
        say("   projection: %d pairs x %.2f s / 6 workers = %.0f s = "
            "%.2f h" % (total, mean, total * mean / 6,
                        total * mean / 6 / 3600))


def pairs_slice(index, count, ceiling_mb, seconds, budget):
    say("-- PAIRS: slice %d of %d" % (index, count))
    plan_document, _held = load_plan_and_held()
    every = all_pairs_in_order(plan_document)
    mine = []
    position = 0
    for pair in every:
        if position % count == index:
            mine.append(pair)
        position = position + 1
    say("   pairs total %d, this slice owns %d" % (len(every), len(mine)))
    out_path = os.path.join(HERE, "pool100_pairs_slice%d.json" % index)
    resume_from = None
    if os.path.exists(out_path):
        resume_from = read_json(out_path)
        if resume_from["finished"]:
            say("   %s is already finished on disk (%d of %d answered); "
                "nothing to do" % (out_path, resume_from["pairs_answered"],
                                   resume_from["pairs_owned"]))
            return
        if resume_from["pairs_owned"] != len(mine):
            raise SystemExit(
                "REFUSED RESUME: %s owns %d pairs on disk, this plan "
                "gives it %d" % (out_path, resume_from["pairs_owned"],
                                 len(mine)))
    run_pairs(mine, ceiling_mb, seconds, budget, out_path,
              "slice%d" % index, resume_from=resume_from)


def read_slices():
    out = []
    for path in sorted(glob.glob(SLICE_PATTERN)):
        out.append(read_json(path))
    return out


def retry(ceiling_mb, seconds):
    """every pair a RUNNER limit stopped, re-run with more room; the
    answer is reported as changed or not.  A limit is a flag, never a
    verdict."""
    say("-- RETRY: pairs the runner stopped, with more room")
    plan_document, _held = load_plan_and_held()
    flagged = []
    for document in read_slices():
        for record in document["results"]:
            if record.get("runner_word") == "walked":
                continue
            flagged.append(record)
    say("   flagged pairs %d" % len(flagged))
    pairs = []
    for record in flagged:
        pairs.append((record["type_key"], record["a"], record["b"]))
    results = run_pairs(pairs, ceiling_mb, seconds, FOUR_HOURS, RETRY,
                        "retry")
    by_key = {}
    for record in flagged:
        by_key[(record["a"], record["b"])] = record
    changed = 0
    for record in results:
        before = by_key[(record["a"], record["b"])]
        record["first_attempt"] = before
        same_state = (record["state"] == before["state"])
        same_cause = (record.get("cause") == before.get("cause"))
        record["answer_changed"] = not (same_state and same_cause)
        if record["answer_changed"]:
            changed = changed + 1
    say("   answers changed %d of %d" % (changed, len(results)))
    document = read_json(RETRY)
    document["results"] = results
    document["answers_changed"] = changed
    write_json(RETRY, document)


# ==================================================================
# close: the edges, the closure, the candidate, the report
# ==================================================================

class Joiner(object):
    def __init__(self):
        self.up = {}

    def add(self, x):
        if x not in self.up:
            self.up[x] = x

    def find(self, x):
        self.add(x)
        while self.up[x] != x:
            self.up[x] = self.up[self.up[x]]
            x = self.up[x]
        return x

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        if ra < rb:
            self.up[rb] = ra
        else:
            self.up[ra] = rb
        return True


def collect_results():
    """every pair's final record: the retry's answer supersedes the
    slice's for the same pair."""
    final = {}
    for document in read_slices():
        for record in document["results"]:
            final[(record["a"], record["b"])] = record
    retried = 0
    if os.path.exists(RETRY):
        for record in read_json(RETRY)["results"]:
            final[(record["a"], record["b"])] = record
            retried = retried + 1
    return final, retried


def cause_head(record):
    """the cause of an UNDECIDED or UNBUILDABLE pair, cut to its head
    so equal causes count as one row (report by cause)."""
    cause = record.get("cause") or ""
    if record["state"] == UNBUILDABLE:
        if cause.startswith("NO_TERM"):
            parts = []
            for piece in cause[len("NO_TERM -- "):].split("; "):
                text = piece[3:]
                text = text.split(":")[0]
                text = text.split(";")[0]
                text = text.split("(")[0].strip()
                parts.append(text[:90])
            return "NO_TERM -- " + " / ".join(sorted(set(parts)))
        return cause.split("(")[0].strip()[:120]
    if cause.startswith("runner limit"):
        return cause.split("(")[0].strip()
    if "did not answer inside" in cause:
        return "the solver did not answer inside its 3000 ms limit"
    if "not comparable" in cause:
        return "the two terms are not comparable (z3 sorts)"
    return cause[:120]


def pipe_table(header, rows):
    lines = []
    lines.append("| " + " | ".join(header) + " |")
    lines.append("|" + "|".join(["---"] * len(header)) + "|")
    for row in rows:
        lines.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(lines)


def close():
    say("-- CLOSE")
    plan_document = read_json(PLAN)
    final, retried = collect_results()
    say("   pair records %d (retry superseded %d)" % (len(final),
                                                       retried))
    groups = plan_document["groups"]
    plan_entries = plan_document["entries"]
    # completeness per group
    group_rows = []
    complete = 0
    for group in groups:
        wanted = pairs_of(group)
        answered = 0
        counts = {PROVED: 0, DISPROVED: 0, UNDECIDED: 0, UNBUILDABLE: 0}
        applied = 0
        for pair in wanted:
            record = final.get(pair)
            if record is None:
                continue
            answered = answered + 1
            counts[record["state"]] = counts[record["state"]] + 1
            if record.get("edge_applies"):
                applied = applied + 1
        done = (answered == len(wanted))
        if done:
            complete = complete + 1
        group_rows.append({
            "rank": group["rank"],
            "type_key": group["type_key"],
            "entries_before": group["entry_count"],
            "pairs": len(wanted),
            "pairs_answered": answered,
            "complete": done,
            "proved": counts[PROVED],
            "disproved": counts[DISPROVED],
            "undecided": counts[UNDECIDED],
            "unbuildable": counts[UNBUILDABLE],
            "edges_applied": applied,
        })
    say("   groups complete %d of %d" % (complete, len(groups)))
    # the closure
    joiner = Joiner()
    for entry_id in plan_entries:
        joiner.add(entry_id)
    edges = []
    proved_not_applied = []
    for key in sorted(final):
        record = final[key]
        if record["state"] != PROVED:
            continue
        if record.get("edge_applies"):
            edges.append(record)
            joiner.union(record["a"], record["b"])
        else:
            proved_not_applied.append(record)
    components = {}
    for entry_id in sorted(plan_entries):
        root = joiner.find(entry_id)
        if root not in components:
            components[root] = []
        components[root].append(entry_id)
    say("   edges applied %d, proved but not applied (a term unproved "
        "against its own body) %d" % (len(edges),
                                       len(proved_not_applied)))
    say("   entries before %d, after %d" % (len(plan_entries),
                                             len(components)))
    # entries after, per group
    after_by_key = {}
    for root in components:
        key = plan_entries[root]["type_key"]
        after_by_key[key] = after_by_key.get(key, 0) + 1
    for row in group_rows:
        row["entries_after"] = after_by_key.get(row["type_key"], 0)
    # the candidate, built over pool5's members
    pool = read_json(POOL5)
    by_id = {}
    for entry in pool["entries"]:
        by_id[entry["entry_id"]] = entry
    order = [entry["entry_id"] for entry in pool["entries"]]
    candidate_entries = []
    number = 0
    merges = []
    for root in sorted(components, key=lambda r: order.index(r)):
        merged = sorted(components[root], key=lambda e: order.index(e))
        number = number + 1
        members = []
        languages = []
        texts = []
        wrapped = []
        best = None
        for entry_id in merged:
            entry = by_id[entry_id]
            for member in entry["members"]:
                members.append(member)
            for lang in entry["languages"]:
                if lang not in languages:
                    languages.append(lang)
            for text in entry["layer5_normalized_texts"]:
                if text not in texts:
                    texts.append(text)
            for text in entry["wrapped_texts"]:
                if text not in wrapped:
                    wrapped.append(text)
            size = entry["representative_size"]
            if best is None or size < best[0]:
                best = (size, entry["representative"], entry_id)
        joining = []
        for record in edges:
            if record["a"] in merged and record["b"] in merged:
                joining.append({
                    "a": record["a"],
                    "b": record["b"],
                    "rep_a": record["rep_a"],
                    "rep_b": record["rep_b"],
                    "inputs": record["inputs"],
                    "answer_width": record["answer_width"],
                    "constant_pool_symbols_renamed_apart":
                        record["constant_pool_symbols_renamed_apart"],
                    "verdict": record["verdict"],
                    "term_a_own_outcome": record["term_a"]["own_outcome"],
                    "term_b_own_outcome": record["term_b"]["own_outcome"],
                })
        candidate = {
            "entry_id": "C%05d" % number,
            "merged_from": merged,
            "merged_entry_count": len(merged),
            "type_key": plan_entries[root]["type_key"],
            "members": members,
            "member_count": len(members),
            "languages": sorted(languages),
            "language_count": len(languages),
            "spans_more_than_one_language": len(languages) > 1,
            "layer5_normalized_texts": texts,
            "distinct_layer5_text_count": len(texts),
            "distinct_wrapped_text_count": len(wrapped),
            "representative": best[1],
            "representative_size": best[0],
            "representative_from_pool5_entry": best[2],
            "representative_rule": "the fewest assembled bytes across "
                                   "the merged entries, ties by pool5 "
                                   "entry order (first-in-list)",
            "edges_joining": joining,
        }
        candidate_entries.append(candidate)
        if len(merged) > 1:
            merges.append(candidate)
    del pool
    check_collector_memory()
    write_json(CANDIDATE, {
        "meta": {
            "generator": "pool100_entry_equivalence.py close",
            "what": "a CANDIDATE for the_pool6.json: the_pool5.json's "
                    "entries closed under transitivity over the "
                    "applied edges of pool100_edges.json.  Not "
                    "ratified; the_pool6.json is not written.",
            "grounds": "pool5's three grounds, plus a proved edge "
                       "between two entries' representatives' terms "
                       "inside one machine type key, applied only when "
                       "both terms were proved against their own "
                       "unit's ship body",
            "role_note": "GROUPING artifact -- checked by "
                         "check_no_spelling_keys.py IN FULL; no field "
                         "is put out of the walk.",
            "operator_note": "a member's operator field is a display "
                             "label carried verbatim from "
                             "the_pool5.json and is read by nothing",
            "inherited_artifact": "the_pool5.json was built over canon39 "
                                  "and term65_store; the terms proved "
                                  "here are built over canon40 records "
                                  "and read term66_store verdicts",
        },
        "summary": {
            "entries_before": len(plan_entries),
            "entries_after": len(components),
            "merged_entries": len(merges),
            "edges_applied": len(edges),
            "groups_complete": complete,
            "groups_total": len(groups),
        },
        "entries": candidate_entries,
    })
    say("-- wrote pool100_pool6_candidate.json")
    # the edges file: every pair's final record
    states = {}
    undecided_causes = {}
    unbuildable_causes = {}
    retry_at_120s = 0
    disproved_with_constant = 0
    for key in final:
        record = final[key]
        states[record["state"]] = states.get(record["state"], 0) + 1
        if record["state"] == UNDECIDED:
            head = cause_head(record)
            undecided_causes[head] = undecided_causes.get(head, 0) + 1
            if "3000 ms" in head:
                retry_at_120s = retry_at_120s + 1
        if record["state"] == UNBUILDABLE:
            head = cause_head(record)
            unbuildable_causes[head] = unbuildable_causes.get(head,
                                                              0) + 1
        if record["state"] == DISPROVED and record.get(
                "counterexample_assigns_a_constant_pool_symbol"):
            disproved_with_constant = disproved_with_constant + 1
    the_44 = plan_document["entries_of_the_44"]
    entries_44 = sorted(set(e for e in the_44.values() if e is not None))
    reached_44 = []
    for entry_id in entries_44:
        key = plan_entries[entry_id]["type_key"]
        row = [r for r in group_rows if r["type_key"] == key][0]
        touched = False
        for pair in final:
            if entry_id in pair:
                touched = True
                break
        reached_44.append({
            "entry_id": entry_id,
            "type_key": key,
            "group_complete": row["complete"],
            "entry_had_a_pair_answered": touched,
            "group_pairs": row["pairs"],
        })
    summary = {
        "pairs_total": plan_document["pairs_total"],
        "pairs_answered": len(final),
        "states": states,
        "edges_applied": len(edges),
        "proved_but_not_applied": len(proved_not_applied),
        "undecided_by_cause": undecided_causes,
        "unbuildable_by_cause": unbuildable_causes,
        "undecided_that_would_be_retried_at_120000_ms": retry_at_120s,
        "disproved_whose_counterexample_assigns_a_constant_pool_symbol":
            disproved_with_constant,
        "groups_complete": complete,
        "groups_total": len(groups),
        "entries_before": len(plan_entries),
        "entries_after": len(components),
        "the_44": {
            "units": len(plan_document["the_44_units"]),
            "entries": len(entries_44),
            "entries_in_a_complete_group":
                len([r for r in reached_44 if r["group_complete"]]),
            "entries_with_a_pair_answered":
                len([r for r in reached_44
                     if r["entry_had_a_pair_answered"]]),
            "entries_alone_in_their_group":
                len([r for r in reached_44 if r["group_pairs"] == 0]),
        },
    }
    write_json(EDGES, {
        "meta": {
            "generator": "pool100_entry_equivalence.py close",
            "what": "every pair's final record (the retry's answer "
                    "supersedes the slice's), the applied edges, and "
                    "the counts by cause",
            "solver": "gate.Gate.decide, SOLVER_MILLISECONDS = 3000, "
                      "never raised",
            "role_note": "PAIRING artifact -- checked by "
                         "check_no_spelling_keys.py IN FULL; no field "
                         "is put out of the walk.",
        },
        "summary": summary,
        "groups": group_rows,
        "the_44_entries": reached_44,
        "pairs": [final[k] for k in sorted(final)],
        "edges": edges,
        "proved_but_not_applied": proved_not_applied,
    })
    say("-- wrote pool100_edges.json")
    say(json.dumps(summary, indent=1, sort_keys=True))
    write_report(plan_document, plan_entries, by_id, group_rows,
                 merges, final, summary, reached_44)
    say("-- wrote pool100_report.md")
    # THE GUARD, unmodified, over every JSON this program wrote
    paths = [PLAN, REPRESENTATIVES, EDGES, CANDIDATE]
    if os.path.exists(SAMPLE):
        paths.append(SAMPLE)
    paths.extend(sorted(glob.glob(SLICE_PATTERN)))
    if os.path.exists(RETRY):
        paths.append(RETRY)
    say("-- the spelling guard, unmodified, over %d files" % len(paths))
    proc = subprocess.run([sys.executable, GUARD] + paths,
                          capture_output=True, text=True)
    text = proc.stdout + proc.stderr
    for line in text.splitlines():
        say("   " + line)
    if proc.returncode != 0:
        os.remove(EDGES)
        os.remove(CANDIDATE)
        raise SystemExit(
            "REFUSED OWN OUTPUT: check_no_spelling_keys.py exited %d; "
            "pool100_edges.json and pool100_pool6_candidate.json "
            "removed" % proc.returncode)
    say("-- guard exit 0")


def literal_texts(entry):
    if not entry["layer5_normalized_texts"]:
        return "(no proved layer-5 text: %d of %d members ineligible)" % (
            entry["members_not_layer5_eligible"], entry["member_count"])
    return " ; ".join("`%s`" % t for t in entry["layer5_normalized_texts"])


def why_text_identity_missed(merged, by_id, plan_entries):
    """computed from the data: for each pool5 entry of the merge, does
    it carry a proved layer-5 text, and are the texts equal?"""
    texts = {}
    no_text = []
    for entry_id in merged:
        entry = by_id[entry_id]
        if not entry["layer5_normalized_texts"]:
            no_text.append(entry_id)
            continue
        for text in entry["layer5_normalized_texts"]:
            if text not in texts:
                texts[text] = []
            texts[text].append(entry_id)
    parts = []
    if len(texts) > 1:
        parts.append(
            "ground two joins on STRING IDENTITY of the layer-5 text, "
            "and these entries print %d different texts for terms the "
            "solver proves equal for every input; the normalizer is a "
            "fixed rewrite rule (simplify, order commutative "
            "arguments, rename positionally), not a decision procedure, "
            "so two equal terms may print differently" % len(texts))
    if no_text:
        parts.append(
            "%d of the merged entries (%s) carry NO proved layer-5 "
            "text in pool5 -- every member's term was withdrawn, "
            "undecided or absent under the round-13 gate over canon39 "
            "-- so ground two had no key for them; the term proved "
            "here is built over the canon40 record and its own "
            "verdict is read from term66_store"
            % (len(no_text), ", ".join(no_text)))
    if len(texts) == 1 and not no_text:
        parts.append(
            "the merged entries print ONE layer-5 text in pool5 yet "
            "were not merged there -- pool5 was built over canon39 "
            "and term65_store, where at least one side's term was not "
            "proved; under canon40 both are")
    return " ".join(parts)


def write_report(plan_document, plan_entries, by_id, group_rows, merges,
                 final, summary, reached_44):
    lines = []
    lines.append("# pool100_report -- solver equivalence between pool5 "
                 "entries inside each machine type key (task 100)")
    lines.append("")
    lines.append("Generated by `pool100_entry_equivalence.py close`. "
                 "Every rendering below is LITERAL (the stored object) "
                 "unless marked GLOSS.")
    lines.append("")
    lines.append("## 1. Entries before and after, per type_key "
                 "(the 20 largest groups by pair count, and a total row)")
    lines.append("")
    header = ["rank", "type_key", "entries before", "pairs",
              "answered", "complete", "PROVED", "DISPROVED", "UNDECIDED",
              "UNBUILDABLE", "edges applied", "entries after"]
    rows = []
    for row in group_rows[:LARGEST_GROUPS_FIRST]:
        rows.append([row["rank"], "`%s`" % row["type_key"],
                     row["entries_before"], row["pairs"],
                     row["pairs_answered"], "yes" if row["complete"]
                     else "NO", row["proved"], row["disproved"],
                     row["undecided"], row["unbuildable"],
                     row["edges_applied"], row["entries_after"]])
    totals = ["total", "%d type keys" % len(group_rows)]
    for field in ["entries_before", "pairs", "pairs_answered"]:
        totals.append(sum(r[field] for r in group_rows))
    totals.append("%d of %d" % (summary["groups_complete"],
                                summary["groups_total"]))
    for field in ["proved", "disproved", "undecided", "unbuildable",
                  "edges_applied", "entries_after"]:
        totals.append(sum(r[field] for r in group_rows))
    rows.append(totals)
    lines.append(pipe_table(header, rows))
    lines.append("")
    incomplete = [r for r in group_rows if not r["complete"]]
    lines.append("Groups NOT complete (pairs answered short of pairs): "
                 "%d." % len(incomplete))
    for row in incomplete:
        lines.append("- rank %d `%s`: %d of %d pairs answered"
                     % (row["rank"], row["type_key"],
                        row["pairs_answered"], row["pairs"]))
    lines.append("")
    lines.append("## 2. The three largest merges, layer-5 texts side by "
                 "side (LITERAL), and why text identity missed them")
    lines.append("")
    ranked = sorted(merges, key=lambda c: (-c["merged_entry_count"],
                                           -c["member_count"],
                                           c["entry_id"]))
    for candidate in ranked[:3]:
        lines.append("### %s -- %d pool5 entries, %d members, type_key "
                     "`%s`, representative `%s` (%d bytes)"
                     % (candidate["entry_id"],
                        candidate["merged_entry_count"],
                        candidate["member_count"], candidate["type_key"],
                        candidate["representative"],
                        candidate["representative_size"]))
        lines.append("")
        lines.append(pipe_table(
            ["pool5 entry", "members", "languages", "representative",
             "layer-5 texts in pool5 (LITERAL)"],
            [[e, by_id[e]["member_count"],
              ",".join(by_id[e]["languages"]),
              "`%s`" % by_id[e]["representative"], literal_texts(by_id[e])]
             for e in candidate["merged_from"]]))
        lines.append("")
        lines.append("Why text identity missed them (GLOSS, computed): "
                     + why_text_identity_missed(candidate["merged_from"],
                                                by_id, plan_entries))
        lines.append("")
        lines.append("Edges that joined them (LITERAL, the verdict's own "
                     "words):")
        for edge in candidate["edges_joining"][:6]:
            seeds = ", ".join("%s=%s" % (i["row"], i["symbol"])
                              for i in edge["inputs"])
            lines.append("- `%s` (%s) == `%s` (%s): %s; inputs %s; "
                         "answer width %s; own verdicts %s / %s; "
                         "timeout %s ms"
                         % (edge["a"], edge["rep_a"], edge["b"],
                            edge["rep_b"], edge["verdict"]["outcome"],
                            seeds, edge["answer_width"],
                            edge["term_a_own_outcome"],
                            edge["term_b_own_outcome"],
                            edge["verdict"]["solver_timeout_ms"]))
        if len(candidate["edges_joining"]) > 6:
            lines.append("- ... %d more edges in pool100_pool6_candidate"
                         ".json" % (len(candidate["edges_joining"]) - 6))
        lines.append("")
    if not ranked:
        lines.append("No merge: no applied edge.")
        lines.append("")
    lines.append("## 3. Three DISPROVED pairs with their counterexample "
                 "seeds (LITERAL) -- same type key, different computation")
    lines.append("")
    disproved = [final[k] for k in sorted(final)
                 if final[k]["state"] == DISPROVED
                 and not final[k].get(
                     "counterexample_assigns_a_constant_pool_symbol")]
    disproved.sort(key=lambda r: (-min(by_id[r["a"]]["member_count"],
                                       by_id[r["b"]]["member_count"]),
                                  r["a"], r["b"]))
    for record in disproved[:3]:
        lines.append("### `%s` (`%s`) against `%s` (`%s`), type_key `%s`"
                     % (record["a"], record["rep_a"], record["b"],
                        record["rep_b"], record["type_key"]))
        lines.append("")
        lines.append("- layer-5 texts in pool5: a = %s; b = %s"
                     % (literal_texts(by_id[record["a"]]),
                        literal_texts(by_id[record["b"]])))
        lines.append("- the gate's reason: `%s`"
                     % record["verdict"]["reason"])
        lines.append("- the solver's model (LITERAL):")
        lines.append("")
        lines.append("```")
        lines.append(record["counterexample"])
        lines.append("```")
        lines.append("")
    lines.append("## 4. UNDECIDED and UNBUILDABLE, by cause")
    lines.append("")
    lines.append(pipe_table(["state", "cause", "pairs"],
                            [[UNDECIDED, "`%s`" % c, n] for c, n in sorted(
                                summary["undecided_by_cause"].items(),
                                key=lambda kv: -kv[1])]
                            + [[UNBUILDABLE, "`%s`" % c, n] for c, n in
                               sorted(summary["unbuildable_by_cause"]
                                      .items(), key=lambda kv: -kv[1])]))
    lines.append("")
    lines.append("- UNDECIDED pairs that would be retried at 120,000 ms "
                 "(NOT retried; the ceiling is the owner's, log_204 section "
                 "4.3): %d"
                 % summary["undecided_that_would_be_retried_at_120000_ms"])
    lines.append("- DISPROVED pairs whose counterexample assigns a "
                 "constant-pool symbol (`ripconst_k`, renamed apart per "
                 "side; the value is not held by this artifact, so the "
                 "disproof is about the terms under free constants): %d"
                 % summary[
                     "disproved_whose_counterexample_assigns_a_"
                     "constant_pool_symbol"])
    lines.append("- PROVED pairs NOT applied because one term is not "
                 "proved against its own unit's ship body: %d"
                 % summary["proved_but_not_applied"])
    lines.append("")
    lines.append("## 5. The 44 non-converging units")
    lines.append("")
    lines.append("Their entries take part like any other entry: this "
                 "merge proves term against term and needs no layer-5 "
                 "key.")
    lines.append("")
    the_44 = summary["the_44"]
    lines.append("- units: %d; pool5 entries holding them: %d; of those, "
                 "in a group whose every pair was answered: %d; with at "
                 "least one pair answered: %d; alone in their group (no "
                 "pair to run): %d"
                 % (the_44["units"], the_44["entries"],
                    the_44["entries_in_a_complete_group"],
                    the_44["entries_with_a_pair_answered"],
                    the_44["entries_alone_in_their_group"]))
    lines.append("")
    lines.append(pipe_table(["entry", "type_key", "group pairs",
                             "group complete", "a pair answered"],
                            [[r["entry_id"], "`%s`" % r["type_key"],
                              r["group_pairs"], r["group_complete"],
                              r["entry_had_a_pair_answered"]]
                             for r in reached_44]))
    lines.append("")
    lines.append("## 6. The tally")
    lines.append("")
    lines.append("- pairs total %d; answered %d; states %s; edges applied "
                 "%d; entries %d -> %d; groups complete %d of %d"
                 % (summary["pairs_total"], summary["pairs_answered"],
                    json.dumps(summary["states"], sort_keys=True),
                    summary["edges_applied"], summary["entries_before"],
                    summary["entries_after"], summary["groups_complete"],
                    summary["groups_total"]))
    lines.append("")
    handle = open(REPORT, "w")
    handle.write("\n".join(lines) + "\n")
    handle.close()


# ==================================================================

def main():
    what = sys.argv[1]
    if what == "plan":
        plan()
        return
    if what == "sample":
        sample(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]))
        return
    if what == "pairs":
        pairs_slice(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]),
                    float(sys.argv[5]), float(sys.argv[6]))
        return
    if what == "retry":
        retry(int(sys.argv[2]), float(sys.argv[3]))
        return
    if what == "close":
        close()
        return
    raise SystemExit("unknown mode %r" % what)


if __name__ == "__main__":
    main()
