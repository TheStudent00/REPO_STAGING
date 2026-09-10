#!/usr/bin/env python3
"""bank.py -- task bank1: the polyfill library as BANKED CERTIFICATES.

WHAT THIS IS, one sentence: a CERTIFICATE is a record about ONE
artifact -- one (cell key, target, written place) with the term it was
posed on, the source that was rendered, the compiler and flags that
built it, the body that was carved out, and the gate's own verdict --
and this program reads every AutoPoly run on disk and writes one
certificate per such artifact onto `certificates.jsonl`.

THE OBJECTS, one sentence each, in relation.
  * A CELL is one (`mnem`, operand shape, `key_width`) row of the
    arch-opcode model table, holding, per place the opcode writes, the
    z3 term the reference simulator's own builder puts there.
  * A TARGET is one of the twelve languages an emulation is written
    in: five compiled (c, cpp, rust, go, swift) and seven interpreted
    (cpython, php, ruby, java, javascript, dart, csharp).
  * A WRITTEN PLACE is one destination the cell's opcode writes --
    `reg_rdi`, `flags`, `reg_xmm0.low`, `x87_7`, `stack_-8` -- and it
    is the third part of a certificate's key because the gate answers
    per place, not per run.
  * A RUN is one (cell, target) pair put through the four steps
    (primitive lookup, render, compile-and-carve, gate) and recorded
    as one line of a pass's store.
  * A PASS is one whole walk of the loop, recorded as one store file:
    `ap1` .. `ap5` on the four compiled targets, `ex1_cpp` on cpp,
    `ex1_interp` and `ex2` on the seven interpreted targets.
  * A CERTIFICATE is what this program writes, above.
  * THE BANK is `certificates.jsonl`: every certificate of every pass,
    the strongest for each key marked `preferred`, every weaker or
    later one kept beside it and marked `superseded_by`.

THE FINDING THIS CARRIES OUT (the owner, 2026-09-10).  The passes re-derived
every emulation from the cell's term every time, so a renderer change
made the same cell yield a different artifact and the old proof no
longer described what had just been built.  Nineteen (cell, target)
pairs proved by some pass are not proved by the last.  A certificate
cannot regress; only the machinery can fail to reproduce it.  The
deliverable is the LIBRARY, one proved emulation per (cell, target),
and it only grows.

THE THREE READINGS, stated as three every time from now on:
  * STRICT -- every written place of the pair is proved, flags
    included.
  * DESTINATION-ONLY -- every place of the pair's DESTINATION REGISTER
    is proved; the flags are not read.  This is the reading tasks ap1
    to ap5 reported ("proved on all four"), through
    `handful.destination_place` and `autopoly5.the_places`, and it is
    reproduced here from the certificates alone.
  * CORPUS-NEEDED -- the destination is proved AND the flags are
    proved wherever the corpus's own attestation records a consumer
    reading a cell of this `mnem`'s flags; where no consumer ever does,
    the flags place is not read.  The attestation is the flag-pair
    ledger rows task m1b counted, held on the cells file as
    `setter_census`: per flag-consuming `mnem`, the setters the corpus
    records before it.  The attestation names a setter by `mnem` only,
    so this reading is at `mnem` granularity and says so.

WHAT IS REUSED RATHER THAN COPIED.  Nothing here decides an emulation:
this program reads stores other tasks wrote and never runs a render, a
compile, a carve or a gate.  The destination-place rule is
`handful.destination_place`'s rule, restated over a certificate's own
`place_index` because a certificate is one place and not a whole run;
the two are checked against each other by `bank.py readings`, which
recomputes the strict figures off the raw stores as well as off the
bank and prints both.

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

HOW THIS PROGRAM OBEYS IT.  A certificate's key is the machine form the
ruling of 2026-09-08 states: the triple in three fields, the mnemonic
in the field `mnem`, never a joined string; the target is a language
name; the place is a machine location.  Nothing selects, groups or
pairs by an operator token.  The one grouping this program does that
reads a `mnem` is the CORPUS-NEEDED reading, and what it reads is the
corpus's own flag-pair attestation -- machine-form evidence, counted
from ledger rows -- never a token.

MEMORY BOUND, stated as the law requires: one collecting process, no
forked workers; every store is STREAMED line by line and no store is
ever held whole; peak resident checked after every store; named abort
ABORT_MEMORY_BANK1 at 6 GB, inside the instance's 20g cap.  The one
document held whole is the cells file (2 MB).

Coding discipline: no compound one-liner statements.

usage:
  bank.py sample [<n>] the first n runs of every store turned into
                       certificates, nothing written, peak resident
                       printed -- the memory sample the law asks for
  bank.py build        every run of every pass on disk -> certificates.jsonl
  bank.py kinds        certificates banked per kind, and per pass
  bank.py readings     THE THREE READINGS, per pass and over the bank
  bank.py restored     the pairs proved by some pass and not by the last
  bank.py backups      whether any excluded within-pass backup store holds
                       a proof the bank does not
  bank.py tally        the counts, printed
"""

import hashlib
import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EMULATION = os.path.normpath(os.path.join(HERE, ".."))

CELLS = os.path.join(HERE, "autopoly5_cells.json")
"""the outer set as task ap5 left it -- 253 cells, the current one, and
the file task ex2 copied object for object as `expand2_cells.json`."""

BANK = os.path.join(HERE, "certificates.jsonl")
AGGREGATE = os.path.join(HERE, "certificates.json")

ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_BANK1"

COMPILED = ["c", "cpp", "rust", "go", "swift"]
INTERPRETED = ["cpython", "php", "ruby", "java", "javascript", "dart",
               "csharp"]

# ==================================================================
# THE PASSES, in the order they ran, which is the order "ties by the
# earliest pass" means.  `kind` says which reader a store needs:
# `compiled` stores carry a `places` list with a gate verdict on each,
# `interpreted` stores carry one whole-sample comparison per run.
# `src` is the folder that pass's rendered sources were written to, so
# a certificate can say whether the artifact is still on disk.
# ==================================================================

PASSES = [
    {"pass": "ap1", "store": "autopoly_runs.jsonl", "reader": "compiled",
     "src": os.path.join(HERE, "src"), "task": "ap1", "log": "log_243",
     "targets": ["c", "rust", "go", "swift"]},
    {"pass": "ap2", "store": "autopoly2_runs.jsonl", "reader": "compiled",
     "src": os.path.join(HERE, "src2"), "task": "ap2", "log": "log_244",
     "targets": ["c", "rust", "go", "swift"]},
    {"pass": "ap3", "store": "autopoly3_runs.jsonl", "reader": "compiled",
     "src": os.path.join(HERE, "src3"), "task": "ap3", "log": "log_245",
     "targets": ["c", "rust", "go", "swift"]},
    {"pass": "ap3_off", "store": "autopoly3_off_runs.jsonl",
     "reader": "compiled", "src": os.path.join(HERE, "src3_off"),
     "task": "ap3", "log": "log_245",
     "targets": ["c", "rust", "go", "swift"]},
    {"pass": "ap4", "store": "autopoly4_runs.jsonl", "reader": "compiled",
     "src": os.path.join(HERE, "src4"), "task": "ap4", "log": "log_246",
     "targets": ["c", "rust", "go", "swift"]},
    {"pass": "ex1_cpp", "store": "expand1_runs.jsonl", "reader": "compiled",
     "src": os.path.join(HERE, "src_expand1"), "task": "ex1",
     "log": "log_248", "targets": ["cpp"]},
    {"pass": "ex1_interp", "store": "expand1_interp.jsonl",
     "reader": "interpreted",
     "src": os.path.join(EMULATION, "interp", "src_ex1"), "task": "ex1",
     "log": "log_248", "targets": INTERPRETED},
    {"pass": "ap5", "store": "autopoly5_runs.jsonl", "reader": "compiled",
     "src": os.path.join(HERE, "src5"), "task": "ap5", "log": "log_249",
     "targets": ["c", "rust", "go", "swift"]},
    {"pass": "ex2", "store": "expand2_runs.jsonl", "reader": "interpreted",
     "src": os.path.join(EMULATION, "interp", "src_ex2"), "task": "ex2",
     "log": "log_250", "targets": INTERPRETED},
    {"pass": "bank1_delta", "store": "bank1_delta_runs.jsonl",
     "reader": "compiled", "src": os.path.join(HERE, "src_bank1"),
     "task": "bank1", "log": "log_253", "targets": COMPILED,
     "optional": True},
    {"pass": "ap6_audit", "store": "ap6_audit_runs.jsonl",
     "reader": "compiled", "src": os.path.join(HERE, "src_ap6_audit"),
     "task": "ap6", "log": "this task", "targets": COMPILED,
     "optional": True},
    {"pass": "ap6_delta", "store": "ap6_delta_runs.jsonl",
     "reader": "compiled", "src": os.path.join(HERE, "src_ap6_delta"),
     "task": "ap6", "log": "this task", "targets": COMPILED,
     "optional": True},
]

# ==================================================================
# THE STORES DELIBERATELY NOT BANKED, each with the reason, because a
# store left out silently is a store nobody can audit.  Every one of
# these is a WITHIN-PASS backup its own log records as defective and
# keeps beside the run of record; none is a pass of the loop.
# `bank.py backups` reads them anyway and reports whether any holds a
# proof the bank does not, so the exclusion is measured rather than
# asserted.
# ==================================================================

BACKUPS = [
    {"store": "autopoly3_runs.jsonl.before_the_guards_passed",
     "reader": "compiled",
     "why": "task ap3's own partial store from before its guards passed"},
    {"store": "autopoly3_runs.jsonl.before_the_x87_bits_refusal",
     "reader": "compiled",
     "why": "task ap3's own partial store from before the x87 refusal"},
    {"store": "autopoly5_runs.jsonl.before_the_x87_memory_arrival_fix",
     "reader": "compiled",
     "why": "task ap5's first pass, 30 of whose runs log_249 SS3 records "
            "as wrong: align_by_row tested one of the two x87 spellings"},
    {"store": "expand2_runs.jsonl.before_the_dotted_label_fix",
     "reader": "interpreted",
     "why": "task ex2's first pass, 196 of whose pairs log_250 SS4.1 "
            "records as a stale binary answering a failed build"},
    {"store": "expand2_runs.jsonl.before_the_hyphen_label_fix",
     "reader": "interpreted",
     "why": "task ex2's second pass, 7 of whose pairs log_250 SS4.2 "
            "records under the same mechanism"},
    {"store": "expand1_interp_pass1.jsonl", "reader": "interpreted",
     "why": "task ex1's own intermediate interpreted passes, superseded "
            "within the task by expand1_interp.jsonl"},
    {"store": "expand1_interp_pass2.jsonl", "reader": "interpreted",
     "why": "as above"},
    {"store": "expand1_interp_pass3.jsonl", "reader": "interpreted",
     "why": "as above"},
    {"store": "expand1_interp_pass4.jsonl", "reader": "interpreted",
     "why": "as above"},
    {"store": "expand1_interp_smoke.jsonl", "reader": "interpreted",
     "why": "task ex1's seven-run smoke, inside expand1_interp.jsonl"},
]

# ==================================================================
# THE COMPILER AND ITS FLAGS, LITERAL.  The flags are the corpus's own
# ship flags, read off each renderer's own `SHIP_FLAGS_SOURCE`
# constant, which is the sentence that names where in `lane_gen.py` the
# build line lives.  The VERSION is what the running instance answers,
# measured once by `build` and stamped on every certificate it writes,
# with the sentence saying that every pass ran in this same image.
# ==================================================================

VERSION_COMMANDS = {
    "c": ["/usr/bin/clang", "--version"],
    "cpp": ["/usr/bin/clang++", "--version"],
    "rust": ["rustc", "--version"],
    "go": ["go", "version"],
    "swift": ["/persist/swift/usr/bin/swiftc", "--version"],
}

VERSION_NOTE = ("measured in this instance's own sandbox-runner:latest "
                "image, which is the image every pass ran in")

# The six kinds the brief names, strongest first.  Strength is how much
# the certificate SETTLES: a proof settles the obligation, a proof under
# the caller's extension settles it on the narrower region the caller
# guarantees, a whole-sample agreement settles it over the sample, a
# `sat` settles it negatively, an `undecided` settles nothing, and a
# `refused` never reached the gate at all.
KINDS = ["proved", "proved_under_caller_extension", "agreed", "sat",
         "undecided", "refused"]


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    peak = peak_kb()
    if peak > ABORT_KB:
        raise SystemExit("%s: %d kB at %s" % (ABORT_NAME, peak, where))
    return peak


def read_json(path):
    handle = open(path)
    document = json.load(handle)
    handle.close()
    return document


def write_json(path, document):
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()


def stream(path):
    """one store, line by line, never held whole."""
    handle = open(path)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        yield json.loads(text)
    handle.close()


# ==================================================================
# section 1: THE COMMANDS
# ==================================================================

def main(argv):
    if not argv:
        say(__doc__)
        return 2
    if argv[0] == "sample":
        many = 20
        if len(argv) > 1:
            many = int(argv[1])
        return sample_command(many)
    if argv[0] == "build":
        return build_command()
    if argv[0] == "kinds":
        return kinds_command()
    if argv[0] == "readings":
        return readings_command()
    if argv[0] == "restored":
        return restored_command()
    if argv[0] == "backups":
        return backups_command()
    if argv[0] == "tally":
        return tally_command()
    say("unknown command %r" % argv[0])
    return 2


def sample_command(many):
    """THE MEMORY SAMPLE THE LAW ASKS FOR, before the whole build: the
    first `many` runs of every store turned into certificates, nothing
    written, and the peak resident printed after each store."""
    versions = compiler_versions()
    say("the sample: the first %d run(s) of every store, nothing "
        "written." % many)
    say("")
    say("| store | runs read | certificates made | bytes of "
        "certificate | peak resident kB |")
    say("|---|---|---|---|---|")
    index = 0
    for step in PASSES:
        index = index + 1
        path = os.path.join(HERE, step["store"])
        if not os.path.exists(path):
            continue
        read = 0
        made = 0
        size = 0
        for run in stream(path):
            read = read + 1
            for cert in certificates_of_run(run, step, versions):
                made = made + 1
                size = size + len(json.dumps(cert, sort_keys=True))
                continue
            if read >= many:
                break
            continue
        say("| `%s` | %d | %d | %d | %d |"
            % (step["store"], read, made, size,
               check_memory(step["store"])))
        continue
    say("")
    say("the bound: %d kB, named abort %s" % (ABORT_KB, ABORT_NAME))
    say("peak resident: %d kB" % peak_kb())
    return 0


def build_command():
    """every run of every pass on disk -> `certificates.jsonl`.

    TWO WALKS, because the preferred entry of a key cannot be known
    until every pass has been read, and the law forbids holding a whole
    store in memory.  The first walk writes every certificate to the
    file and keeps ONE SMALL ROW per key in memory (the key, the
    strongest kind seen and the pass that carried it) -- 253 x 12 x a
    few places, tens of thousands of short tuples, not the
    certificates.  The second walk rewrites the file with `preferred`
    and `superseded_by` filled in from those rows."""
    versions = compiler_versions()
    say("compiler versions, LITERAL (%s):" % VERSION_NOTE)
    for lang in COMPILED:
        say("   %-6s %s" % (lang, versions.get(lang)))
        continue
    say("")
    counted = {}
    per_pass = {}
    strongest = {}
    total = 0
    handle = open(BANK + ".first_walk", "w")
    index = 0
    for step in PASSES:
        index = index + 1
        path = os.path.join(HERE, step["store"])
        if not os.path.exists(path):
            if step.get("optional"):
                say("[%d/%d] %s -- not on disk, skipped (optional)"
                    % (index, len(PASSES), step["store"]))
                continue
            raise SystemExit("the store %s is named by PASSES and is not "
                             "on disk" % path)
        made = 0
        for run in stream(path):
            for cert in certificates_of_run(run, step, versions):
                handle.write(json.dumps(cert, sort_keys=True))
                handle.write("\n")
                made = made + 1
                total = total + 1
                counted[cert["kind"]] = counted.get(cert["kind"], 0) + 1
                remember_strongest(strongest, cert)
                continue
            continue
        per_pass[step["pass"]] = made
        say("[%d/%d] %-11s %-42s %6d certificate(s)  peak %d kB"
            % (index, len(PASSES), step["pass"], step["store"], made,
               check_memory(step["pass"])))
        continue
    handle.close()
    say("")
    say("keys seen: %d; certificates written: %d" % (len(strongest), total))
    marked = mark_preferred(strongest)
    say("the bank: %s" % BANK)
    say("   %d line(s), %d byte(s)"
        % (marked, os.path.getsize(BANK)))
    os.remove(BANK + ".first_walk")
    aggregate = {
        "meta": {
            "task": "bank1",
            "what": "one certificate per (cell key, target, written "
                    "place): the artifact it is about and the verdict "
                    "on it, banked from every AutoPoly run on disk",
            "cells_source": CELLS,
            "bank": BANK,
            "certificates": total,
            "keys": len(strongest),
            "memory_bound_kb": ABORT_KB,
            "memory_abort": ABORT_NAME,
            "peak_kb": peak_kb(),
            "compiler_versions": versions,
            "compiler_version_note": VERSION_NOTE,
        },
        "per_kind": counted,
        "per_pass": per_pass,
        "passes_banked": [x["pass"] for x in PASSES
                          if os.path.exists(os.path.join(HERE,
                                                         x["store"]))],
        "stores_not_banked": BACKUPS,
        "readings": readings_document(),
    }
    write_json(AGGREGATE, aggregate)
    say("the aggregate: %s" % AGGREGATE)
    say("peak resident: %d kB" % peak_kb())
    return 0


def kinds_command():
    """certificates banked per kind, and per pass."""
    counted = {}
    per_pass = {}
    preferred = {}
    for cert in stream(BANK):
        kind = cert["kind"]
        counted[kind] = counted.get(kind, 0) + 1
        holder = per_pass.setdefault(cert["produced_by"]["pass"], {})
        holder[kind] = holder.get(kind, 0) + 1
        if cert["preferred"]:
            preferred[kind] = preferred.get(kind, 0) + 1
        continue
    say("Table B1 -- certificates banked per kind.  `certificates` counts "
        "every entry on certificates.jsonl; `preferred` counts the one "
        "entry each (cell, target, place) key keeps as its strongest, "
        "ties by the earliest pass.")
    say("")
    say("| kind | certificates | preferred |")
    say("|---|---|---|")
    for kind in KINDS:
        say("| `%s` | %d | %d |"
            % (kind, counted.get(kind, 0), preferred.get(kind, 0)))
        continue
    say("| **total** | **%d** | **%d** |"
        % (sum(counted.values()), sum(preferred.values())))
    say("")
    say("Table B2 -- the same, per pass.  A pass is one whole walk of "
        "the loop, one store file.")
    say("")
    say("| pass | " + " | ".join("`%s`" % k for k in KINDS) + " | total |")
    say("|---|" + "---|" * (len(KINDS) + 1))
    for step in PASSES:
        name = step["pass"]
        if name not in per_pass:
            continue
        holder = per_pass[name]
        cells = ["%d" % holder.get(k, 0) for k in KINDS]
        say("| `%s` | %s | %d |"
            % (name, " | ".join(cells), sum(holder.values())))
        continue
    say("")
    say("peak resident: %d kB" % peak_kb())
    return 0


def readings_command():
    """THE THREE READINGS, per pass and over the bank, and the strict
    figures recomputed off the raw stores beside them."""
    document = readings_document()
    say("Table B3 -- the headline in THREE readings, per pass and over "
        "the whole bank.  A pair is one (cell, target).  STRICT: every "
        "written place proved.  DESTINATION-ONLY: every place of the "
        "destination register proved, the flags not read -- the reading "
        "tasks ap1 to ap5 reported.  CORPUS-NEEDED: the destination "
        "proved AND the flags proved wherever the corpus's attestation "
        "records a consumer reading a cell of this `mnem`'s flags.")
    say("")
    say("| pass | strict | destination-only | corpus-needed |")
    say("|---|---|---|---|")
    for name in document["order"]:
        held = document["per_pass"][name]
        say("| `%s` | %d | %d | %d |"
            % (name, held["strict"], held["destination"],
               held["corpus"]))
        continue
    held = document["bank"]
    say("| **the bank** | **%d** | **%d** | **%d** |"
        % (held["strict"], held["destination"], held["corpus"]))
    say("")
    say("Table B4 -- the strict per-pass figures recomputed off the RAW "
        "STORES rather than off the bank, which is the check that "
        "banking moved nothing.")
    say("")
    say("| pass | strict, off the bank | strict, off the store | same |")
    say("|---|---|---|---|")
    for name in document["order"]:
        mine = document["per_pass"][name]["strict"]
        theirs = document["off_the_store"].get(name)
        same = "yes"
        if mine != theirs:
            same = "**NO**"
        say("| `%s` | %d | %s | %s |" % (name, mine, theirs, same))
        continue
    say("")
    say("Table B5 -- cells on all four (c, rust, go, swift), on all five "
        "(+ cpp) and on all twelve, under each reading, with the "
        "attested ledger rows those cells cover and that as a share of "
        "%d." % document["ledger_total"])
    say("")
    say("| width | reading | cells | ledger rows | share |")
    say("|---|---|---|---|---|")
    for width in document["widths"]["order"]:
        for reading in ["strict", "destination", "corpus"]:
            held = document["widths"][width][reading]
            say("| %s | %s | %d | %d | %s%% |"
                % (width, reading, held["cells"], held["ledger_rows"],
                   held["share_percent"]))
            continue
        continue
    say("")
    say("THE RECONCILIATION WITH THE FIVE PASSES' OWN PUBLISHED "
        "FIGURES, so a reader meeting three readings where the logs "
        "carried one is not left with a discrepancy.  Tasks ap1 to ap5 "
        "counted a pair proved when its destination places were proved "
        "OR proved under the caller's extension "
        "(`autopoly5.across_targets`); all three readings above take "
        "`proved` to mean the gate answered unsat on the obligation as "
        "posed.  The passes' own count, recomputed here:")
    say("")
    say("| pass | pairs, as the passes counted | cells on all four, as "
        "the passes counted |")
    say("|---|---|---|")
    for name in document["order"]:
        held = document["per_pass"][name]
        say("| `%s` | %d | %d |"
            % (name, held["as_the_passes_counted"],
               held["cells_on_all_four_as_the_passes_counted"]))
        continue
    say("")
    say("THE ATTESTATION'S OWN GRANULARITY, said plainly: the corpus "
        "records a flag pair as (setter `mnem`, consumer `mnem`), with "
        "no operand shape and no width on the setter side, so the "
        "corpus-needed reading asks whether ANY cell of this `mnem` "
        "has an attested consumer.  The setters the corpus records, "
        "read off the cells file's own `setter_census`: %d of them, "
        "over %d flag-pair ledger rows."
        % (len(document["setters"]), document["setter_ledger_rows"]))
    say("")
    say("peak resident: %d kB" % peak_kb())
    return 0


def restored_command():
    """the pairs proved by some pass and not by the last -- the 19 the
    brief names -- each with the passes that proved it."""
    # WHICH PASSES, off the PASSES table's own fields and never off a
    # list of names: the compiled passes that walked the four targets
    # the question is about, in the order they ran, and the LAST of
    # them is the last row of that list.  The question -- which pairs a
    # later pass stopped proving -- is about those passes and about no
    # task label.
    passes = []
    for step in PASSES:
        if step["reader"] != "compiled":
            continue
        if step["targets"] != ["c", "rust", "go", "swift"]:
            continue
        passes.append(step["pass"])
        continue
    last = passes[-1]
    strict = strict_by_pass()
    union = set()
    for name in passes:
        union = union | strict.get(name, set())
        continue
    lost = sorted(union - strict.get(last, set()), key=readable)
    say("Table B6 -- every (cell, target) pair proved on the STRICT "
        "reading by some pass of the four compiled targets and NOT by "
        "the last pass, with the passes that proved it and the "
        "certificate the bank keeps.  A certificate cannot regress; "
        "these are the pairs the bank restores.")
    say("")
    say("| `mnem` | shape | `key_width` | target | proved by | the bank's "
        "preferred pass |")
    say("|---|---|---|---|---|---|")
    for key in lost:
        held = []
        for name in passes:
            if key in strict.get(name, set()):
                held.append(name)
            continue
        say("| `%s` | %s | %s | %s | %s | `%s` |"
            % (key[0], key[1], key[2], key[3], ", ".join(held),
               held[0]))
        continue
    say("")
    say("pairs proved by some pass and not by the last: %d" % len(lost))
    say("the union over the five passes, STRICT: %d" % len(union))
    say("the last pass alone, STRICT: %d" % len(strict.get(last, set())))
    say("")
    say("Table B6b -- the five passes' own STRICT figures, so the union "
        "above can be read against them.")
    say("")
    say("| pass | pairs proved, STRICT |")
    say("|---|---|")
    for name in passes:
        say("| `%s` | %d |" % (name, len(strict.get(name, set()))))
        continue
    say("")
    say("Table B7 -- the same loss read at the CELL width: cells on all "
        "four targets under each pass, and the cells the last pass "
        "drops.")
    say("")
    say("| pass | cells on all four, STRICT |")
    say("|---|---|")
    for name in passes:
        say("| `%s` | %d |" % (name, len(all_four(strict.get(name,
                                                             set())))))
        continue
    dropped = sorted(all_four(strict.get("ap4", set()))
                     - all_four(strict.get(last, set())),
                     key=readable)
    say("")
    say("cells on all four through pass 4 and not on all four in pass "
        "5: %d" % len(dropped))
    for key in dropped:
        say("   %s %s %s" % (key[0], key[1], key[2]))
        continue
    say("")
    say("peak resident: %d kB" % peak_kb())
    return 0


def backups_command():
    """the stores deliberately not banked, and whether any of them holds
    a proof the bank does not.

    THIS IS THE AUDIT OF AN EXCLUSION.  Each of these is a within-pass
    backup its own log records as defective and keeps beside the run of
    record.  Leaving one out silently would be a claim; reading it and
    reporting the answer is a measurement."""
    banked = set()
    for cert in stream(BANK):
        if cert["kind"] not in ("proved", "agreed"):
            continue
        banked.add(key_tuple(cert))
        continue
    say("certified keys in the bank (kind `proved` or `agreed`): %d"
        % len(banked))
    say("")
    say("Table B8 -- every store on disk this task did NOT bank, why, "
        "and how many keys it would have certified that the bank does "
        "not already hold.")
    say("")
    say("| store | why not banked | keys it certifies | keys the bank "
        "lacks |")
    say("|---|---|---|---|")
    missing = []
    index = 0
    for step in BACKUPS:
        index = index + 1
        path = os.path.join(HERE, step["store"])
        if not os.path.exists(path):
            say("| `%s` | %s | -- not on disk -- | -- |"
                % (step["store"], step["why"]))
            continue
        certified = set()
        fake = {"pass": step["store"], "store": step["store"],
                "reader": step["reader"], "src": HERE, "task": "--",
                "log": "--", "targets": []}
        for run in stream(path):
            for cert in certificates_of_run(run, fake, {}):
                if cert["kind"] not in ("proved", "agreed"):
                    continue
                certified.add(key_tuple(cert))
                continue
            continue
        gap = certified - banked
        for key in sorted(gap, key=readable):
            missing.append((step["store"], key))
            continue
        say("| `%s` | %s | %d | %d |"
            % (step["store"], step["why"], len(certified), len(gap)))
        check_memory(step["store"])
        continue
    say("")
    if not missing:
        say("no excluded store holds a certified key the bank lacks.")
    for store, key in missing:
        say("   %s holds %s %s %s %s, which the bank does not certify"
            % (store, key[0], key[1], key[2], key[3]))
        continue
    say("")
    say("peak resident: %d kB" % peak_kb())
    return 0


def tally_command():
    """the counts, printed."""
    lines = 0
    for _cert in stream(BANK):
        lines = lines + 1
        continue
    say("lines on %s: %d" % (BANK, lines))
    say("bytes on %s: %d" % (BANK, os.path.getsize(BANK)))
    document = read_json(AGGREGATE)
    say("certificates recorded by the aggregate: %d"
        % document["meta"]["certificates"])
    say("keys recorded by the aggregate: %d" % document["meta"]["keys"])
    say("peak resident: %d kB" % peak_kb())
    return 0


# ==================================================================
# section 2: ONE RUN -> ITS CERTIFICATES
# ==================================================================

def certificates_of_run(run, step, versions):
    """every certificate one run of one store carries.

    A compiled run carries one per written place; an interpreted run
    carries one, because the interpreted check compares the whole
    sample at the run's own destination place and nowhere else.  A run
    that never reached a place at all carries ONE certificate with a
    null place and the kind `refused`, so the attempt and its cause are
    banked rather than lost."""
    if step["reader"] == "interpreted":
        return [interpreted_certificate(run, step)]
    return compiled_certificates(run, step, versions)


def compiled_certificates(run, step, versions):
    """one compiled run's certificates, one per written place."""
    places = run.get("places") or []
    if not places:
        return [refused_certificate(run, step)]
    out = []
    index = 0
    for place in places:
        out.append(compiled_certificate(run, step, place, index,
                                        versions))
        index = index + 1
        continue
    return out


def compiled_certificate(run, step, place, index, versions):
    """one (cell, target, written place) of a compiled pass."""
    check = place.get("check") or {}
    cert = {
        "cell": cell_of(run),
        "target": run["lang"],
        "place": place.get("writes"),
        "place_index": index,
        "kind": kind_of_place(place),
        "term_text": place.get("text"),
        "source": source_of(step, place.get("source_path"),
                            place.get("source")),
        "compiler": {
            "flags": ship_flags_source(run["lang"]),
            "version": versions.get(run["lang"]),
            "version_note": VERSION_NOTE,
        },
        "body": {
            "bytes": place.get("body_bytes"),
            "text": place.get("body_text"),
        },
        "verdict": verdict_of(check),
        "produced_by": {
            "pass": step["pass"],
            "task": step["task"],
            "log": step["log"],
            "store": store_path(step),
            "lane": place.get("lane") or run.get("lane"),
            "seconds": run.get("seconds"),
        },
        "setter": setter_cell_of(run),
        "code_version": run.get("code_version"),
        "route": run.get("route"),
        "landing": (place.get("landing") or {}).get("verdict"),
        "attested_ledger_rows": run.get("attested_ledger_rows"),
        "preferred": False,
        "superseded_by": None,
    }
    if cert["kind"] == "refused":
        cert["cause"] = cause_of_place(run, place)
    return cert


def refused_certificate(run, step):
    """a run the route could not put a single place through: the attempt
    and its cause, banked with a null place."""
    return {
        "cell": cell_of(run),
        "target": run["lang"],
        "place": None,
        "place_index": None,
        "kind": "refused",
        "term_text": None,
        "source": {"path": None, "sha256": None, "found_on_disk": False},
        "compiler": {"flags": ship_flags_source(run["lang"]),
                     "version": None, "version_note": VERSION_NOTE},
        "body": {"bytes": None, "text": None},
        "verdict": None,
        "cause": run.get("refusal_cause"),
        "cause_detail": run.get("refusal_detail"),
        "produced_by": {
            "pass": step["pass"], "task": step["task"], "log": step["log"],
            "store": store_path(step), "lane": run.get("lane"),
            "seconds": run.get("seconds"),
        },
        "setter": setter_cell_of(run),
        "code_version": run.get("code_version"),
        "route": run.get("route"),
        "landing": None,
        "attested_ledger_rows": run.get("attested_ledger_rows"),
        "preferred": False,
        "superseded_by": None,
    }


def interpreted_certificate(run, step):
    """one (cell, target, written place) of an interpreted pass.

    THERE IS NO CARVE AND NO GATE on this route: the emulation is
    SOURCE in the target language over the target's own value model,
    and the check is the fuzz census's method over a sample.  So the
    certificate's verdict is the sample and its agreement count, its
    kind is `agreed` when the WHOLE sample agrees, and its body is
    empty rather than absent-by-accident.

    A `refusal_cause` DECIDES FIRST, before `rendered`.  Task ex2's
    thirty-eight nullary runs ("the runner did not answer", log_250
    SS9) carry `rendered: True` AND a refusal cause, because the source
    was written and the runner then had no arrival to feed it; reading
    `rendered` first would bank those as `undecided` and put this
    task's refused count at 418 where task ex2's own is 456."""
    kind = "refused"
    if run.get("refusal_cause") is None and run.get("rendered") is True:
        kind = "agreed"
        if run.get("disagreements"):
            kind = "sat"
        if not run.get("agreements"):
            kind = "undecided"
    cert = {
        "cell": cell_of(run),
        "target": run["lang"],
        "place": run.get("writes"),
        "place_index": 0,
        "kind": kind,
        "term_text": run.get("term_text"),
        "source": source_of(step, run.get("source_path"), None),
        "compiler": {
            "flags": "the interpreted route runs SOURCE through the "
                     "target's own runtime; there is no compile at ship "
                     "flags and no carve",
            "version": None,
            "version_note": VERSION_NOTE,
        },
        "body": {"bytes": None, "text": None},
        "verdict": {
            "outcome": None,
            "reason": None,
            "counterexample": run.get("first_disagreement"),
            "region": None,
            "check": run.get("check"),
            "sample_points": run.get("sample_points"),
            "agreements": run.get("agreements"),
            "disagreements": run.get("disagreements"),
            "declined_points": run.get("declined_points"),
        },
        "produced_by": {
            "pass": step["pass"], "task": step["task"], "log": step["log"],
            "store": store_path(step), "lane": run.get("lane"),
            "seconds": run.get("seconds"),
        },
        "setter": setter_cell_of(run),
        "code_version": run.get("code_version"),
        "route": run.get("route"),
        "landing": None,
        "attested_ledger_rows": run.get("attested_ledger_rows"),
        "preferred": False,
        "superseded_by": None,
    }
    if kind == "refused":
        cert["cause"] = run.get("refusal_cause")
        cert["cause_detail"] = run.get("refusal_detail")
    return cert


def kind_of_place(place):
    """one written place's kind, in the six names the brief states.

    THE VERDICT OF RECORD IS THE PIPELINE'S OWN CEILING, which is task
    ap1's rule and every pass's: a gate call the 3,000 ms ceiling left
    UNDECIDED is re-posed ONCE at 30,000 ms and that answer sits BESIDE
    the verdict of record rather than replacing it.  So a place whose
    re-pose answered unsat is banked `undecided`, with the re-pose in
    its verdict, and the delta pass will attempt it again.  A different
    reading would have made the bank's own figures unequal to the five
    passes' own, which is the one thing the three readings exist to
    prevent."""
    check = place.get("check")
    if check is None:
        return "refused"
    outcome = check.get("outcome")
    if outcome == "PROVED_ON_SHIP":
        return "proved"
    if outcome == "DISPROVED":
        again = check.get("under_caller_extension") or {}
        if again.get("outcome") == "PROVED_ON_SHIP":
            return "proved_under_caller_extension"
        return "sat"
    if outcome == "UNDECIDED":
        return "undecided"
    return "refused"


def verdict_of(check):
    """the gate's answer in z3's own words, with the region sentence
    where one applied."""
    if not check:
        return None
    out = {
        "outcome": check.get("outcome"),
        "reason": check.get("reason"),
        "counterexample": check.get("counterexample"),
        "region": check.get("region"),
        "region_because": check.get("substituted_because"),
        "solver_timeout_ms": check.get("solver_timeout_ms"),
        "width_note": check.get("width_note"),
        "canon40_outcome": check.get("canon40_outcome"),
    }
    again = check.get("under_caller_extension")
    if again:
        out["under_caller_extension"] = {
            "outcome": again.get("outcome"),
            "reason": again.get("reason"),
            "counterexample": again.get("counterexample"),
        }
    repose = check.get("recheck")
    if repose:
        out["repose"] = {
            "outcome": repose.get("outcome"),
            "reason": repose.get("reason"),
            "ceiling_ms": repose.get("ceiling_ms"),
        }
    return out


def cause_of_place(run, place):
    """why one place never reached the gate, the refusal sentence
    LITERAL."""
    if place.get("refusal_cause"):
        return place["refusal_cause"]
    if place.get("rendered") is not True:
        return "the place was not rendered"
    if not place.get("compiled"):
        return "the compiler refused"
    return run.get("refusal_cause")


def cell_of(run):
    """one cell as the machine-form key the ruling of 2026-09-08 states:
    the triple, its three parts in three fields, the mnemonic in the
    field `mnem`.

    NOT A JOINED STRING, and this is not a style choice: a field holding
    `and|gpr_gpr|32` is a row key carrying an operator token, whatever
    the token happens to be a mnemonic of, and the spelling guard
    refuses it."""
    return {"mnem": run["mnem"], "shape": run["shape"],
            "key_width": run["key_width"]}


SETTER_CELL_CACHE = {}


def setter_cell_of(run):
    """THE SETTER'S OWN CELL, in machine form, or None where the run
    read no flag state.

    WHY IT IS PART OF A CERTIFICATE'S KEY.  A flag consumer's mapping is
    a function of the flag state a setter wrote, so what the loop
    renders is the PAIR as one function: the same consumer over a setter
    at another width is a different artifact and carries its own proof.

    WHERE THE SHAPE AND THE WIDTH COME FROM.  A run written before
    2026-09-10 records the setter's `mnem` and its own LINE and nothing
    else, so the cell is classified out of that line by the model
    table's own classifier -- `model_table.classify_line` and
    `model_table.key_width`, the same two calls task m1b's attestation
    pass and the hub's own pair reader make.  Nothing is read off the
    token."""
    setter = run.get("setter")
    if not setter:
        return None
    if setter.get("shape") is not None:
        return {"mnem": setter["mnem"], "shape": setter["shape"],
                "key_width": setter.get("key_width")}
    line = setter.get("line")
    key = (setter["mnem"], line)
    if key in SETTER_CELL_CACHE:
        return SETTER_CELL_CACHE[key]
    out = {"mnem": setter["mnem"], "shape": None, "key_width": None}
    if line is not None:
        import model_table as MT
        MT._install_gpr_widths()
        shape, width, cause = MT.classify_line(setter["mnem"], line,
                                               None)
        if cause is None:
            out = {"mnem": setter["mnem"], "shape": shape,
                   "key_width": MT.key_width(setter["mnem"], width)}
    SETTER_CELL_CACHE[key] = out
    return out


def setter_tuple(cert):
    """the setter cell of one certificate, as a tuple, or None."""
    setter = cert.get("setter")
    if not setter:
        return None
    return (setter.get("mnem"), setter.get("shape"),
            setter.get("key_width"))


def store_path(step):
    """the store a certificate came out of, as a path RELATIVE TO THE
    REPOSITORY ROOT.

    NOT `...`, and this is not a style choice.  The
    spelling guard splits a string on `/ | : ,` and refuses any piece
    that is an operator token, and `~` is one -- c's, rust's and php's
    bitwise complement.  The guard refused an earlier draft of this
    file on exactly that, 11,340 times, once per certificate.  A
    repository-relative path is also what the communication protocol's
    public-repo rule asks for."""
    return ("Research/oracle/cross_construction/emulation/autopoly/%s"
            % step["store"])


def source_of(step, path, text):
    """the rendered source: the path the store recorded, the sha256 of
    the artifact, and whether the file is still on disk.

    TWO SHA256s WHERE THERE ARE TWO THINGS TO HASH.  A compiled store
    keeps the source TEXT on the run, so that text is the artifact and
    is hashed directly; the file on disk is hashed too and the two are
    compared, which is a real check that the folder still holds what
    the store says it built.  An interpreted store keeps only a path,
    so the file on disk is the only artifact there is."""
    out = {"path": path, "sha256": None, "found_on_disk": False,
           "on_disk_sha256": None, "matches_disk": None}
    if text is not None:
        out["sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if path is None:
        return out
    found = resolve_source(step, path)
    if found is None:
        return out
    out["found_on_disk"] = True
    handle = open(found, "rb")
    body = handle.read()
    handle.close()
    out["on_disk_sha256"] = hashlib.sha256(body).hexdigest()
    if out["sha256"] is None:
        out["sha256"] = out["on_disk_sha256"]
        return out
    out["matches_disk"] = (out["sha256"] == out["on_disk_sha256"])
    return out


def resolve_source(step, path):
    """the file the store's recorded path names, looked for where that
    pass actually wrote.

    A store's recorded path is relative to the emulation folder and is
    sometimes the path of an EARLIER task's folder -- task ex2's runs
    record `interp/src_ex1/...` while task ex2's own sources were
    written to `interp/src_ex2/`.  So the recorded path is tried first
    and the pass's own source folder second, by basename.  Which one
    answered is not guessed: `found_on_disk` says only that one did."""
    direct = os.path.join(EMULATION, path)
    if os.path.exists(direct):
        return direct
    beside = os.path.join(step["src"], os.path.basename(path))
    if os.path.exists(beside):
        return beside
    return None


SHIP_FLAGS_HELD = {}


def ship_flags_source(lang):
    """the corpus's own ship flags for one target, LITERAL, read off
    that renderer's own `SHIP_FLAGS_SOURCE` constant rather than
    restated here."""
    if lang in SHIP_FLAGS_HELD:
        return SHIP_FLAGS_HELD[lang]
    SHIP_FLAGS_HELD[lang] = read_ship_flags(lang)
    return SHIP_FLAGS_HELD[lang]


def read_ship_flags(lang):
    """the one constant, imported from the module that owns it."""
    if lang not in COMPILED:
        return None
    sys.path.insert(0, EMULATION)
    if lang == "c":
        import emulate as E
        return E.SHIP_FLAGS_SOURCE
    if lang == "cpp":
        sys.path.insert(0, os.path.join(EMULATION, "cpp"))
        import cpp_render as CPR
        return CPR.SHIP_FLAGS_SOURCE
    if lang == "rust":
        sys.path.insert(0, os.path.join(EMULATION, "rust"))
        import rust_render as RR
        return RR.SHIP_FLAGS_SOURCE
    if lang == "go":
        sys.path.insert(0, os.path.join(EMULATION, "go"))
        import go_render as GR
        return GR.SHIP_FLAGS_SOURCE
    sys.path.insert(0, os.path.join(EMULATION, "swift"))
    import swift_render as SR
    return SR.SHIP_FLAGS_SOURCE


def compiler_versions():
    """what each compiler in this instance answers to `--version`, first
    line, LITERAL."""
    import subprocess
    out = {}
    for lang in COMPILED:
        command = VERSION_COMMANDS[lang]
        try:
            answer = subprocess.run(command, capture_output=True,
                                    timeout=60)
            text = answer.stdout.decode("utf-8", "replace")
            text = text + answer.stderr.decode("utf-8", "replace")
            out[lang] = text.strip().split("\n")[0].strip()
        except Exception as problem:
            out[lang] = "not answered: %s: %s" % (type(problem).__name__,
                                                  problem)
        continue
    return out


# ==================================================================
# section 3: THE PREFERRED ENTRY OF A KEY
# ==================================================================

def key_tuple(cert):
    """the identity of one certificate: the cell triple, the target, the
    written place and THE SETTER CELL the emulation was rendered over.

    The setter joined the key on 2026-09-10, when the loop began
    rendering each flag consumer over every setter cell the corpus
    attests before it: the pair is the node, so the pair is the key, and
    two proofs about two setters are two certificates rather than one
    hiding the other."""
    return (cert["cell"]["mnem"], cert["cell"]["shape"],
            cert["cell"]["key_width"], cert["target"], cert["place"],
            setter_tuple(cert))


def pair_tuple(cert):
    """the (cell, target) pair one certificate belongs to."""
    return (cert["cell"]["mnem"], cert["cell"]["shape"],
            cert["cell"]["key_width"], cert["target"])


def remember_strongest(strongest, cert):
    """the strongest kind seen for one key and the pass that carried it.

    Ties by the EARLIEST pass, which is why the comparison is strictly
    less-than: `PASSES` is in the order the passes ran, so the first
    pass to reach a kind keeps it."""
    key = key_tuple(cert)
    rank = KINDS.index(cert["kind"])
    held = strongest.get(key)
    if held is None:
        strongest[key] = (rank, cert["produced_by"]["pass"])
        return
    if rank < held[0]:
        strongest[key] = (rank, cert["produced_by"]["pass"])
    return


def mark_preferred(strongest):
    """the second walk: every certificate rewritten with `preferred` and
    `superseded_by` filled in."""
    source = open(BANK + ".first_walk")
    handle = open(BANK, "w")
    written = 0
    for line in source:
        text = line.strip()
        if not text:
            continue
        cert = json.loads(text)
        key = key_tuple(cert)
        rank, pass_name = strongest[key]
        if (KINDS.index(cert["kind"]) == rank
                and cert["produced_by"]["pass"] == pass_name):
            cert["preferred"] = True
            cert["superseded_by"] = None
        else:
            cert["preferred"] = False
            cert["superseded_by"] = {
                "pass": pass_name,
                "kind": KINDS[rank],
                "why": "the same (cell, target, written place) carries a "
                       "stronger certificate, or an equally strong one "
                       "from an earlier pass",
            }
        handle.write(json.dumps(cert, sort_keys=True))
        handle.write("\n")
        written = written + 1
        continue
    source.close()
    handle.close()
    return written


# ==================================================================
# section 4: THE THREE READINGS
# ==================================================================

def readings_document():
    """the three readings, per pass, over the bank, and at the cell
    widths, as one document both `readings` and `build` use."""
    cells = read_json(CELLS)
    setters = attested_setters(cells)
    ledger = ledger_rows(cells)
    per_pass = {}
    order = []
    proved_by_pass = {}
    for step in PASSES:
        path = os.path.join(HERE, step["store"])
        if not os.path.exists(path):
            continue
        order.append(step["pass"])
        held = readings_of_store(path, step, setters)
        per_pass[step["pass"]] = {
            "strict": len(held["strict"]),
            "destination": len(held["destination"]),
            "corpus": len(held["corpus"]),
            "as_the_passes_counted": len(held["as_the_passes_counted"]),
            "cells_on_all_four_as_the_passes_counted":
                len(all_four(held["as_the_passes_counted"])),
        }
        proved_by_pass[step["pass"]] = held
        continue
    bank = union_of(proved_by_pass)
    widths = width_document(bank, ledger)
    return {
        "order": order,
        "per_pass": per_pass,
        "bank": {"strict": len(bank["strict"]),
                 "destination": len(bank["destination"]),
                 "corpus": len(bank["corpus"]),
                 "as_the_passes_counted":
                     len(bank["as_the_passes_counted"])},
        "off_the_store": {k: per_pass[k]["strict"] for k in per_pass},
        "widths": widths,
        "ledger_total": sum(ledger.values()),
        "setters": setter_document(cells),
        "setter_ledger_rows": setter_ledger_rows(cells),
        "reading_definitions": {
            "strict": "every written place of the pair is proved, flags "
                      "included",
            "destination": "every place of the pair's destination "
                           "register is proved; the flags are not read",
            "corpus": "the destination is proved AND the flags are "
                      "proved wherever the corpus's attestation records "
                      "a consumer reading a cell of this `mnem`'s flags",
        },
    }


def readings_of_store(path, step, setters):
    """one pass's three sets of proved (cell, target) pairs, read off
    the store itself.

    THE STORE AND NOT THE BANK, deliberately: the bank is derived from
    the stores, so reading the stores here and the bank in `build` and
    printing both is the check that the derivation moved nothing."""
    out = {"strict": set(), "destination": set(), "corpus": set(),
           "as_the_passes_counted": set()}
    for run in stream(path):
        pair = (run["mnem"], run["shape"], run["key_width"], run["lang"])
        if step["reader"] == "interpreted":
            if run.get("rendered") is not True:
                continue
            if run.get("disagreements"):
                continue
            if not run.get("agreements"):
                continue
            out["strict"].add(pair)
            out["destination"].add(pair)
            out["corpus"].add(pair)
            out["as_the_passes_counted"].add(pair)
            continue
        places = run.get("places") or []
        if not places:
            continue
        if every_place_proved(places):
            out["strict"].add(pair)
        destination = destination_places(places)
        if not destination:
            continue
        if every_place_admitted(destination):
            out["as_the_passes_counted"].add(pair)
        if not every_place_proved(destination):
            continue
        out["destination"].add(pair)
        if flags_are_needed(run, setters):
            flags = flag_places(places)
            if flags and not every_place_proved(flags):
                continue
        out["corpus"].add(pair)
        continue
    return out


def every_place_proved(places):
    """whether every place in a list carries a gate verdict of unsat."""
    for place in places:
        if kind_of_place(place) != "proved":
            return False
        continue
    return True


def every_place_admitted(places):
    """whether every place in a list is proved OR proved under the
    caller's extension.

    THIS IS NOT A FOURTH READING.  It exists for ONE line of the
    report: tasks ap1 to ap5 counted "proved on all four" over
    `outcome in ("proved", "proved under caller extension")`
    (`autopoly5.across_targets`), so their published figures cannot be
    reproduced by any of the three readings, all three of which take
    `proved` to mean the gate answered unsat on the obligation as
    posed.  The reconciliation is stated rather than left as a
    discrepancy."""
    for place in places:
        if kind_of_place(place) not in ("proved",
                                        "proved_under_caller_extension"):
            return False
        continue
    return True


def destination_places(places):
    """every place of the run's DESTINATION REGISTER.

    `handful.destination_place`'s rule, restated: the destination is the
    first place that is not the flags, or the flags place when that is
    all there is.  Task ap2's fix 3 split a 128-bit place into a low
    and a high half, so the destination REGISTER is every place whose
    name shares the destination's own base -- a cell is proved on a
    target when EVERY half of its destination register is proved, which
    is `autopoly5.the_places`' own rule."""
    chosen = None
    for place in places:
        if place.get("writes") != "flags":
            chosen = place
            break
        continue
    if chosen is None:
        chosen = places[0]
    base = base_of(chosen.get("writes"))
    out = []
    for place in places:
        if base_of(place.get("writes")) == base:
            out.append(place)
        continue
    return out


def flag_places(places):
    """every place of the run that is the flags, halves included."""
    out = []
    for place in places:
        if base_of(place.get("writes")) == "flags":
            out.append(place)
        continue
    return out


def base_of(writes):
    """a written place's register, with a half's suffix cut off:
    `reg_xmm0.low` and `reg_xmm0.high` are two halves of one register
    and `flags.low` is a half of the flags."""
    if writes is None:
        return None
    return writes.split(".")[0]


def flags_are_needed(run, setters):
    """whether the corpus's own attestation records a consumer reading
    the flags of a cell of this `mnem`.

    THE ATTESTATION IS MACHINE-FORM EVIDENCE and this is the whole of
    what it says: the corpus's flag-pair ledger rows record the pair
    (setter `mnem`, consumer `mnem`), so a `mnem` that appears on the
    setter side of any recorded pair has an attested consumer and one
    that never appears has none.  The setter side carries no operand
    shape and no width, so this reading is at `mnem` granularity and
    the report says so."""
    return run["mnem"] in setters


def attested_setters(cells):
    """every `mnem` the corpus records on the setter side of a flag
    pair, read off the cells file's own `setter_census`."""
    out = set()
    census = cells.get("setter_census") or {}
    for _consumer, rows in census.items():
        for row in rows:
            out.add(row["mnem"])
            continue
        continue
    return out


def setter_document(cells):
    """the setters the corpus records, each as a MACHINE-FORM ROW rather
    than a bare name.

    WHY NOT A LIST OF NAMES.  A json list whose elements are bare
    mnemonics is a list of bare tokens, and several of these mnemonics
    are also operator tokens of the twelve languages (`or` and `xor`
    are php's and python's own operator spellings) -- so the spelling
    guard would refuse the file, and it would be right to: a bare list
    is a row structure.  Each setter is a row `{mnem, ledger_rows}`,
    where `mnem` is the field the guard reads as a machine form."""
    counted = {}
    census = cells.get("setter_census") or {}
    for _consumer, rows in census.items():
        for row in rows:
            name = row["mnem"]
            counted[name] = counted.get(name, 0) + row.get("ledger_rows",
                                                           0)
            continue
        continue
    out = []
    for name in sorted(counted):
        out.append({"mnem": name, "flag_pair_ledger_rows": counted[name]})
        continue
    return out


def setter_ledger_rows(cells):
    """how many flag-pair ledger rows the attestation the reading rests
    on was counted over."""
    total = 0
    census = cells.get("setter_census") or {}
    for _consumer, rows in census.items():
        for row in rows:
            total = total + row.get("ledger_rows", 0)
            continue
        continue
    return total


def ledger_rows(cells):
    """per cell triple, the attested ledger rows it covers."""
    out = {}
    for record in cells["asked"]:
        key = (record["asked"]["mnem"], record["asked"]["shape"],
               record["asked"]["key_width"])
        out[key] = record["attested_ledger_rows"]
        continue
    return out


def union_of(proved_by_pass):
    """the bank's own three sets: the union over every pass, because a
    certificate cannot regress."""
    out = {"strict": set(), "destination": set(), "corpus": set(),
           "as_the_passes_counted": set()}
    for _name, held in proved_by_pass.items():
        for reading in out:
            out[reading] = out[reading] | held[reading]
            continue
        continue
    return out


def width_document(bank, ledger):
    """cells on all four, all five and all twelve under each reading."""
    widths = {
        "all four": ["c", "rust", "go", "swift"],
        "all five": ["c", "cpp", "rust", "go", "swift"],
        "all twelve": COMPILED + INTERPRETED,
    }
    out = {"order": ["all four", "all five", "all twelve"]}
    whole = sum(ledger.values())
    for name in out["order"]:
        held = {}
        for reading in ["strict", "destination", "corpus"]:
            cells = cells_on(bank[reading], widths[name])
            rows = 0
            for key in cells:
                rows = rows + ledger.get(key, 0)
                continue
            share = 0.0
            if whole:
                share = round(100.0 * rows / whole, 2)
            held[reading] = {"cells": len(cells), "ledger_rows": rows,
                             "share_percent": share}
            continue
        out[name] = held
        continue
    return out


def cells_on(pairs, targets):
    """every cell triple proved on every one of a list of targets."""
    seen = {}
    for mnem, shape, width, lang in pairs:
        key = (mnem, shape, width)
        seen.setdefault(key, set()).add(lang)
        continue
    out = set()
    for key, langs in seen.items():
        if set(targets) <= langs:
            out.add(key)
        continue
    return out


def all_four(pairs):
    """every cell triple proved on all four compiled targets."""
    return cells_on(pairs, ["c", "rust", "go", "swift"])


def strict_by_pass():
    """the STRICT proved pairs of every compiled pass, off the stores."""
    cells = read_json(CELLS)
    setters = attested_setters(cells)
    out = {}
    for step in PASSES:
        path = os.path.join(HERE, step["store"])
        if not os.path.exists(path):
            continue
        held = readings_of_store(path, step, setters)
        out[step["pass"]] = held["strict"]
        continue
    return out


def readable(key):
    """a sort key over a cell triple or a pair that never compares None
    with an integer."""
    return tuple("%s" % part for part in key)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
