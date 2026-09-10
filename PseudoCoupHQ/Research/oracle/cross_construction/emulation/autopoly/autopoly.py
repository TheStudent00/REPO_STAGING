#!/usr/bin/env python3
"""autopoly.py -- THE LOOP DRIVER, and from task bank1 on it runs in
--bank mode: DELTA PLUS AUDIT.

WHAT CHANGED, one sentence: the loop no longer re-derives every
emulation from the cell's term on every pass -- it attempts only the
(cell, target, written place) triples the bank holds no proof for, and
re-derives a 5% AUDIT SAMPLE of the ones it does, so the count is
monotone by construction and a pass costs a few hundred runs instead of
a thousand.

THE FINDING THIS CARRIES OUT (the owner, 2026-09-10).  Re-deriving everything
every time meant a renderer change made the same cell yield a different
artifact, and the old proof no longer described what had just been
built: nineteen (cell, target) pairs proved by some pass are not proved
by the last, and passes 2 to 5 spent 75% to 98% of their runs re-doing
known results.  A proof is a certificate about ONE artifact and a
certificate cannot regress; only the machinery can fail to reproduce
it.

THE OBJECTS, one sentence each, in relation.
  * A CELL is one (`mnem`, operand shape, `key_width`) row of the
    arch-opcode model table, holding, per place the opcode writes, the
    z3 term the reference simulator's own builder puts there.
  * A CERTIFICATE is one record about one (cell, target, written
    place): the term, the rendered source and its sha256, the compiler
    and its flags, the carved body, and the gate's own verdict.
    `bank.py` writes them; `certificates.jsonl` holds them.
  * THE DELTA is every (cell, target, written place) the bank holds no
    certificate of kind `proved` or `agreed` for.
  * THE AUDIT SAMPLE is 5% of the certified triples, chosen by
    `random.Random("2026-09-10")`, re-derived from the term.
  * AN ALARM is an audited triple whose re-derived verdict differs from
    its certificate ON IDENTICAL INPUTS -- the same term text, the same
    source sha256, the same compiler and flags.  An alarm STOPS the
    pass and names the pair.
  * A CHANGED ARTIFACT is an audited triple whose re-derived source
    hashes differently: the renderer moved, so this is a NEW
    certificate beside the old one and never a replacement of it.

THE TWO MODES, and why the unflagged commands are task ap1's.
  * `autopoly.py --bank <command>` is the mode above, and it is THE WAY
    THE LOOP RUNS FROM NOW ON.
  * `autopoly.py <command>` with no flag is TASK ap1'S OWN DRIVER,
    delegated verbatim to `autopoly1.py`, which is task ap1's file
    copied unchanged.  It is kept because `DevComms/log_243` cites
    seven of its commands as reproducing commands and
    `lanes_ap1/ap1_l5_run.sh` calls its `run`; a driver that answered
    differently under those names would make a closed task's log
    unreproducible.  Nothing about task ap1's answers moves.
  * `autopoly.py --full run` is the whole re-derivation over the five
    compiled targets -- the shape passes ap1 to ap5 ran -- kept so the
    cost of a full pass can be measured against the delta's.

WHAT IS REUSED RATHER THAN COPIED, said out loud.  Everything that
decides an answer is task ap5's driver and the file beneath it:
  `autopoly5.one_run` runs one (cell, target) through the four steps
  and its re-pose, `autopoly5.the_pairs` orders the outer set by
  attested ledger rows descending, `handful.build_shared` builds the
  reference and the gate, `handful.load_in_table` reads the table's
  TRANSLATED triples for the composition step, and `bank.py` supplies
  the kinds, the certificate key and the ship-flag sentences.  This
  file adds the DELTA SELECTION, the AUDIT, and the bookkeeping around
  them, and nothing else.

THE ROUTE IS THE DRIVER'S, AND THERE IS ONLY ONE (2026-09-10).
`handful.py` carried nine `use_task_*` gates, so which contract rules
applied was decided by the NAME of the task asking; they are gone, every
rule applies to every run, and what a certificate records instead is
`code_version` -- the sha256 of the driver's own source and of the
renderer that wrote the target's source.  This file sets
`handful.TARGETS` and the product paths, which are configuration, and
decides nothing about the route.

WHICH PASS'S PRODUCTS, and it is a parameter rather than a name in the
code: `--pass <label>` selects the store, the aggregate and the source
folder mechanically (`<label>_runs.jsonl`, `<label>.json`,
`src_<label>/`).  Its default is the pass that introduced bank mode, so
`DevComms/log_253`'s own reproducing commands answer exactly as they
did.

THE RE-ATTEMPT RULE, which is what replaced the task label.  A key whose
certificate is `refused`, `undecided`, `sat` or `proved_under_caller_
extension` is attempted again only when the code version recorded on
that certificate DIFFERS from the version running now for that target;
a key with no code version on record (every certificate banked before
2026-09-10) differs by definition and is attempted.  A CERTIFIED key --
`proved` or `agreed` -- is only ever re-derived through the audit
sample, which `--audit-share` sets.

MEMORY BOUND, stated as the law requires: one collecting process, no
forked workers; the bank is STREAMED and never held whole; peak
resident checked after every run; named abort ABORT_MEMORY_BANK1 at
6 GB, inside the instance's 20g cap.

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

HOW THE DELTA OBEYS IT.  What a pass attempts is decided by the BANK --
which keys carry a certificate of kind `proved` or `agreed` -- and by
`random.Random("2026-09-10")` for the audit.  Neither reads a token.
The cells are the outer set the corpus attests, in attested-ledger-row
order, exactly as tasks ap1 to ap5 walked them.

Coding discipline: no compound one-liner statements.

usage:
  autopoly.py --bank preflight   what the delta pass would attempt and
                                 audit, and nothing run
  autopoly.py --bank run [<n>]   the delta pass; `<n>` stops after n runs
  autopoly.py --bank report      the cost line: certified before /
                                 attempted / newly certified / audited /
                                 alarms, against a full pass
  autopoly.py --bank audit       every audited triple and its answer
  autopoly.py --bank cost        the delta pass beside a full pass over
                                 the same five targets, both measured
  autopoly.py --bank changed     every audited triple whose ARTIFACT
                                 changed, with the line that differs
  autopoly.py --bank tally       the counts, printed
  autopoly.py --full run [<n>]   the whole re-derivation over the five
                                 compiled targets, for the cost
                                 comparison
  autopoly.py <command>          the first loop driver's own commands,
                                 delegated verbatim to `autopoly1.py`
  the three options, which may precede any mode and change no rule:
  --pass <label>                 which pass's products to read and write
  --audit-share <fraction>       how much of the certified population is
                                 re-derived; `1` is every certificate
  --attempts off                 audit only: attempt no uncertified key,
                                 so what the pass measures is
                                 re-derivation alone
"""

import hashlib
import json
import os
import random
import resource
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
EMULATION = os.path.normpath(os.path.join(HERE, ".."))
HANDFUL = os.path.join(EMULATION, "handful")
sys.path.insert(0, HANDFUL)
sys.path.insert(0, HERE)

import handful as H                                             # noqa: E402
import model_table as MTAB                                      # noqa: E402
import gate as G                                                # noqa: E402
import autopoly5 as LOOP                                        # noqa: E402
import bank as BK                                               # noqa: E402

CELLS = os.path.join(HERE, "autopoly5_cells.json")
"""the outer set as task ap5 left it: 253 cells, the current one."""

PASS_LABEL = "bank1_delta"
"""WHICH PASS'S PRODUCTS, as a parameter.  `--pass <label>` moves it.
The default is the pass that introduced bank mode so that log_253's own
reproducing commands answer as they did; a new pass states its own
label on the command line and writes beside every earlier pass, never
over one."""

FULL_LABEL = "bank1_full"


def paths_of(label):
    """one pass's products, derived from its label mechanically."""
    return {
        "runs": os.path.join(HERE, "%s_runs.jsonl" % label),
        "aggregate": os.path.join(HERE, "%s.json" % label),
        "src": os.path.join(HERE, "src_%s" % label),
        "primitive": os.path.join(HERE, "%s_primitive.json" % label),
        "spellings": os.path.join(HERE, "%s_spellings.json" % label),
        "report": os.path.join(HERE, "%s.md" % label),
    }


HELD = paths_of(PASS_LABEL)
RUNS = HELD["runs"]
AGGREGATE = HELD["aggregate"]
SRC_DIR = HELD["src"]
PRIMITIVE = HELD["primitive"]
SPELLINGS = HELD["spellings"]
REPORT = HELD["report"]

FULL_RUNS = os.path.join(HERE, "%s_runs.jsonl" % FULL_LABEL)
FULL_SRC_DIR = os.path.join(HERE, "src_%s" % FULL_LABEL)

ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_BANK1"

SOLVER_MS = 3000
REPOSE_MS = 30000
"""task ap1's two ceilings, unchanged: the gate of record at 3,000 ms
per place and ONE re-pose at 30,000 ms for an UNDECIDED."""

AUDIT_SHARE = 0.05
"""how much of the certified population one pass re-derives.
`--audit-share 1` is EVERY certificate, which is the audit the gates'
removal is guarded by: a re-derived verdict that differs from its
certificate on identical inputs is an alarm and the pass stops."""

ATTEMPTS_ARE_ON = True
"""whether the pass also attempts the keys no certificate certifies.
`--attempts off` leaves only the audit, so what a pass measures is
re-derivation alone and nothing else."""

AUDIT_DATE = "2026-09-10"
"""the seed the brief names, `random.Random(<date>)`, written out so a
later pass can reproduce this pass's own sample exactly and a NEW pass
takes a new date and therefore a new sample."""

TARGETS = ["c", "cpp", "rust", "go", "swift"]

CAUSE_DRIVER = "the driver raised on this (cell, target) pair"
"""the loop's own refusal cause, in the words every pass since the first
has written it (`autopoly1.CAUSE_DRIVER`, `autopoly5.CAUSE_DRIVER`), so
a refusal of this kind reads the same on every store.  No new outcome
name is coined here."""

AP1_COMMANDS = ["preflight", "run", "aggregate", "report", "tally",
                "reproduce", "tables", "causes", "repose", "store",
                "sat", "branch"]


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


def configure(store, src):
    """the driver pointed at THIS pass's paths, this pass's memory bound
    and the five compiled targets.

    THERE IS NO TASK ENTRY TO CALL ANY MORE.  `handful.py` used to carry
    nine of them and the route a run went through depended on which one
    a driver called; every rule is now unconditional, so what is set
    here is what a configuration is: where the products go, what the
    named abort is called, and which targets the pass walks.

    Every path `handful.py` writes through is repointed into this pass's
    own files, so no lane of this pass can write an earlier pass's
    products."""
    H.TARGETS = list(TARGETS)
    H.RESULTS = AGGREGATE
    H.REPORT = REPORT
    H.SRC_DIR = src
    H.PRIMITIVE = PRIMITIVE
    H.SPELLINGS = SPELLINGS
    H.CELLS = CELLS
    H.HOST_FOLDER = ("PseudoCoupHQ/Research/oracle/"
                     "cross_construction/emulation/autopoly")
    H.ABORT_KB = ABORT_KB
    H.ABORT_NAME = ABORT_NAME
    LOOP.TARGETS = list(TARGETS)
    return


def sha256_of_file(path):
    """the sha256 of one source file's bytes."""
    handle = open(path, "rb")
    digest = hashlib.sha256(handle.read()).hexdigest()
    handle.close()
    return digest


LOOP_VERSION = None


def code_version_of(lang):
    """THE VERSION OF THE MACHINERY ONE RUN WAS PRODUCED BY: the
    driver's own source, this loop's own source, and the source of the
    renderer that wrote the target -- each by the sha256 of its bytes.

    It is the object that replaced the nine task gates.  A task label
    said WHO ran; this says WHAT ran, and a later pass compares it
    against the version it is running to decide whether an answer is
    worth deriving again."""
    global LOOP_VERSION
    if LOOP_VERSION is None:
        LOOP_VERSION = sha256_of_file(os.path.abspath(__file__))
    out = dict(H.code_version(lang))
    out["loop"] = LOOP_VERSION
    out["loop_source"] = os.path.basename(os.path.abspath(__file__))
    return out


def version_key(version):
    """the three shas of one code version, as a tuple, so two versions
    compare as objects rather than as text.  A certificate banked before
    2026-09-10 carries none and answers `None` here, which differs from
    every real version -- so it is attempted again, which is the
    intended reading."""
    if not version:
        return None
    return (version.get("driver"), version.get("loop"),
            version.get("renderer"))


# ==================================================================
# section 1: THE COMMANDS
# ==================================================================

def main(argv):
    """the three options first, then the mode.

    AN OPTION IS A CONFIGURATION and never a rule: which pass's products
    to read, how much of the certified population to re-derive, and
    whether uncertified keys are attempted at all.  Nothing any of them
    sets is asked about inside a run."""
    global PASS_LABEL, HELD, RUNS, AGGREGATE, SRC_DIR, PRIMITIVE
    global SPELLINGS, REPORT, AUDIT_SHARE, ATTEMPTS_ARE_ON
    while argv and argv[0] in ("--pass", "--audit-share", "--attempts"):
        if argv[0] == "--pass":
            PASS_LABEL = argv[1]
            HELD = paths_of(PASS_LABEL)
            RUNS = HELD["runs"]
            AGGREGATE = HELD["aggregate"]
            SRC_DIR = HELD["src"]
            PRIMITIVE = HELD["primitive"]
            SPELLINGS = HELD["spellings"]
            REPORT = HELD["report"]
        if argv[0] == "--audit-share":
            AUDIT_SHARE = float(argv[1])
        if argv[0] == "--attempts":
            ATTEMPTS_ARE_ON = argv[1] == "on"
        argv = argv[2:]
    if not argv:
        say(__doc__)
        return 2
    if argv[0] == "--bank":
        return bank_main(argv[1:])
    if argv[0] == "--full":
        return full_main(argv[1:])
    if argv[0] in AP1_COMMANDS:
        return task_ap1(argv)
    say("unknown command %r" % argv[0])
    return 2


def task_ap1(argv):
    """the first loop driver's own commands, delegated verbatim.

    `autopoly1.py` is task ap1's file, copied unchanged when this file
    became the bank-mode driver.  It reads and writes task ap1's own
    paths, so `DevComms/log_243`'s seven reproducing commands and
    `lanes_ap1/ap1_l5_run.sh` answer exactly as they did."""
    import autopoly1 as AP1
    return AP1.main(argv)


def bank_main(argv):
    if not argv:
        say(__doc__)
        return 2
    if argv[0] == "preflight":
        return bank_preflight_command()
    if argv[0] == "run":
        limit = None
        if len(argv) > 1:
            limit = int(argv[1])
        return bank_run_command(limit)
    if argv[0] == "report":
        return bank_report_command()
    if argv[0] == "audit":
        return bank_audit_command()
    if argv[0] == "cost":
        return bank_cost_command()
    if argv[0] == "changed":
        return bank_changed_command()
    if argv[0] == "tally":
        return bank_tally_command()
    say("unknown --bank command %r" % argv[0])
    return 2


def full_main(argv):
    if not argv:
        say(__doc__)
        return 2
    if argv[0] == "run":
        limit = None
        if len(argv) > 1:
            limit = int(argv[1])
        return full_run_command(limit)
    say("unknown --full command %r" % argv[0])
    return 2


def bank_preflight_command():
    """what the delta pass would attempt and audit, and nothing run."""
    configure(RUNS, SRC_DIR)
    plan = the_delta()
    say("the bank: %s" % BK.BANK)
    say("the outer set: %s" % CELLS)
    say("the targets: %s" % ", ".join(TARGETS))
    say("")
    say("Table D1 -- what a delta pass costs against a full one.  A "
        "PLACE-TRIPLE is one (cell, target, written place); a RUN is "
        "one (cell, target), which is the unit the loop actually "
        "executes because the four steps render, compile and carve "
        "every place of a pair together.")
    say("")
    say("| step | place-triples | runs |")
    say("|---|---|---|")
    say("| a full pass over these five targets | %d | %d |"
        % (plan["known_triples"], plan["pairs_total"]))
    say("| certified before this pass (kind `proved` or `agreed`) | %d "
        "| -- |" % plan["certified_before"])
    say("| the delta: no certificate of kind `proved` or `agreed` | %d "
        "| %d |" % (plan["attempt_triples"], plan["attempt_pairs"]))
    say("| the audit sample: %s%% of the certified, seed `%s` | %d | %d |"
        % (round(AUDIT_SHARE * 100), AUDIT_DATE, plan["audit_triples"],
           plan["audit_pairs"]))
    say("| held by the code version: the machinery that answered it "
        "has not moved | %d | -- |" % plan["held_by_version"])
    say("| the runs this pass executes | -- | **%d** |"
        % plan["runs_to_execute"])
    say("")
    say("pairs never attempted by any pass on this store: %d"
        % plan["pairs_never_attempted"])
    say("peak resident: %d kB" % check_memory("preflight"))
    return 0


def bank_run_command(limit):
    """THE DELTA PASS.  One line on `bank1_delta_runs.jsonl` per
    finished run, and the audit's answers beside it."""
    configure(RUNS, SRC_DIR)
    if not os.path.isdir(SRC_DIR):
        os.makedirs(SRC_DIR)
    plan = the_delta()
    certificates = certificates_for(plan["audit_triples_list"])
    say("certified before: %d place-triple(s)" % plan["certified_before"])
    say("attempted: %d place-triple(s) over %d run(s)"
        % (plan["attempt_triples"], plan["attempt_pairs"]))
    say("audited: %d place-triple(s), seed %r"
        % (plan["audit_triples"], AUDIT_DATE))
    say("runs to execute: %d" % plan["runs_to_execute"])
    say("")
    done = already_recorded(RUNS)
    say("runs already on %s: %d" % (RUNS, len(done)))
    outcome = walk(plan["runs_list"], RUNS, done, limit, certificates,
                   plan)
    return outcome


def full_run_command(limit):
    """the whole re-derivation over the five compiled targets, so the
    delta's cost has something measured to stand against."""
    configure(FULL_RUNS, FULL_SRC_DIR)
    if not os.path.isdir(FULL_SRC_DIR):
        os.makedirs(FULL_SRC_DIR)
    cells = read_json(CELLS)
    pairs = LOOP.the_pairs(cells)
    held = []
    for asked, lang, ledger in pairs:
        held.append((asked, lang, ledger))
        continue
    say("a FULL pass: %d run(s)" % len(held))
    done = already_recorded(FULL_RUNS)
    return walk(held, FULL_RUNS, done, limit, {}, None)


def bank_report_command():
    """the cost line."""
    document = read_json(AGGREGATE)
    held = document["cost"]
    say("Table D2 -- the delta pass's own cost line, in the five counts "
        "the brief names.  `certified before` counts (cell, target, "
        "written place) triples the bank certified before this pass; "
        "`attempted` counts the triples with no such certificate; "
        "`newly certified` counts the triples this pass certified; "
        "`audited` counts the certified triples re-derived from the "
        "term; `alarms` counts the audited triples whose re-derived "
        "verdict differs from its certificate on identical inputs.")
    say("")
    say("| pass | certified before | attempted | newly certified | "
        "audited | alarms |")
    say("|---|---|---|---|---|---|")
    say("| `bank1_delta` | %d | %d | %d | %d | %d |"
        % (held["certified_before"], held["attempted"],
           held["newly_certified"], held["audited"], held["alarms"]))
    say("")
    say("Table D3 -- what the pass cost against a full pass over the "
        "same five targets.")
    say("")
    say("| | runs | seconds |")
    say("|---|---|---|")
    say("| a full pass over these five targets | %d | %s |"
        % (held["full_pass_runs"], held["full_pass_seconds"]))
    say("| this delta pass | %d | %s |"
        % (held["runs_executed"], held["seconds"]))
    say("")
    say("the delta pass ran %s%% of a full pass's runs."
        % round(100.0 * held["runs_executed"]
                / max(1, held["full_pass_runs"]), 1))
    say("peak resident: %d kB" % peak_kb())
    return 0


def bank_changed_command():
    """every audited triple whose ARTIFACT changed, one by one.

    THE CERTIFICATE'S SOURCE AGAINST THE RE-DERIVATION'S, and the first
    line on which they differ, which is the measurement.  A changed
    artifact is not an alarm: the renderer moved, so the same cell now
    yields something else, and the new record is a certificate BESIDE
    the old one rather than in place of it."""
    document = read_json(AGGREGATE)
    changed = []
    for row in document["audit"]:
        if row["reading"] != "the artifact changed":
            continue
        changed.append(row)
        continue
    wanted = set()
    for row in changed:
        wanted.add(key_of_audit_row(row))
        continue
    certificate = {}
    for cert in BK.stream(BK.BANK):
        key = BK.key_tuple(cert)
        if key not in wanted:
            continue
        if not cert["preferred"]:
            continue
        certificate[key] = cert
        continue
    rederived = {}
    handle = open(RUNS)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        run = json.loads(text)
        for place in run.get("places") or []:
            key = (run["mnem"], run["shape"], run["key_width"],
                   run["lang"], place.get("writes"),
                   setter_key(run.get("setter")))
            if key not in wanted:
                continue
            rederived[key] = place
            continue
        continue
    handle.close()
    say("Table D7 -- the audited triples whose artifact changed.  The "
        "two source columns hold the FIRST line on which the two "
        "rendered sources differ, which is the measurement; the several "
        "hundred characters of preamble they share are not shown.")
    say("")
    say("| `mnem` | shape | `key_width` | target | place | "
        "certificate's pass | certificate | re-derived | the "
        "certificate's source | the re-derivation's source |")
    say("|---|---|---|---|---|---|---|---|---|---|")
    for row in changed:
        key = key_of_audit_row(row)
        cert = certificate.get(key)
        place = rederived.get(key)
        new_source = None
        if place is not None:
            new_source = place.get("source")
        path = None
        if cert is not None:
            path = (cert["source"] or {}).get("path")
        left, right = first_difference(source_text(path), new_source)
        say("| `%s` | %s | %s | %s | `%s` | `%s` | %s | %s | `%s` | "
            "`%s` |"
            % (key[0], key[1], key[2], key[3], key[4],
               row["certificate_pass"], row["certificate_kind"],
               row["rederived_kind"], escaped(left[:170]),
               escaped(right[:170])))
        continue
    say("")
    for row in changed:
        key = key_of_audit_row(row)
        cert = certificate.get(key)
        place = rederived.get(key)
        say("%s %s %s on %s at %s" % (key[0], key[1], key[2], key[3],
                                      key[4]))
        path = "--"
        if cert is not None:
            path = (cert["source"] or {}).get("path")
        say("   the certificate: pass %s, kind %s, source %s, sha256 %s"
            % (row["certificate_pass"], row["certificate_kind"], path,
               row["certificate_sha256"]))
        say("   the re-derivation: kind %s, sha256 %s"
            % (row["rederived_kind"], row["rederived_sha256"]))
        if place is not None:
            check = place.get("check") or {}
            say("   the re-derivation's verdict: %s -- %s"
                % (check.get("outcome"), check.get("reason")))
            if place.get("refusal_cause"):
                say("   the re-derivation's refusal cause: %s"
                    % place["refusal_cause"])
            if place.get("refusal_detail"):
                say("   the re-derivation's refusal detail: %s"
                    % place["refusal_detail"])
        say("")
        continue
    say("audited triples whose artifact changed: %d" % len(changed))
    return 0


def key_of_audit_row(row):
    """one audited row's key, the same six-part key the bank uses."""
    setter = row.get("setter")
    held = None
    if setter is not None:
        held = (setter.get("mnem"), setter.get("shape"),
                setter.get("key_width"))
    return (row["cell"]["mnem"], row["cell"]["shape"],
            row["cell"]["key_width"], row["target"], row["place"],
            held)


def source_text(path):
    """the rendered source a certificate names, looked for where the
    passes actually wrote: this folder first, the folder above second,
    which is the order `bank.resolve_source` reads it in."""
    if path is None:
        return None
    for root in [HERE, EMULATION]:
        candidate = os.path.join(root, path)
        if os.path.exists(candidate):
            handle = open(candidate)
            body = handle.read()
            handle.close()
            return body
        continue
    return None


def first_difference(left, right):
    """the first line two rendered sources do not share, one cell each.

    A whole source is several hundred characters of preamble the two
    always share -- the allow-list, the provenance comment, the
    signature -- so showing both whole would hide the one line that is
    the measurement."""
    if left is None:
        return ("-- the certificate's source is not on disk --", "--")
    if right is None:
        return ("--", "-- the re-derivation rendered nothing --")
    one = left.split("\n")
    two = right.split("\n")
    for index in range(max(len(one), len(two))):
        a = "-- ends --"
        if index < len(one):
            a = one[index].strip()
        b = "-- ends --"
        if index < len(two):
            b = two[index].strip()
        if a == b:
            continue
        return (a, b)
    return ("-- identical text --", "-- identical text --")


def escaped(text):
    """a markdown table cell cannot carry a bare pipe."""
    return text.replace("|", "\\|")


def bank_cost_command():
    """THE MEASURED COST: the delta pass beside the full pass over the
    same five targets, both run in this instance, in this image, in the
    same hour, at the same two ceilings.

    The seconds are the runs' OWN recorded seconds summed, not a lane's
    wall clock, so the two figures count the same thing and neither
    carries the reading of the bank around it."""
    say("Table D5 -- the delta pass beside a full pass over the same "
        "five compiled targets.  Both were run in this instance, in "
        "this image, at the same two ceilings; the only difference is "
        "which runs were attempted.  `seconds` sums each store's own "
        "recorded per-run seconds.")
    say("")
    say("| pass | runs | seconds | seconds per run |")
    say("|---|---|---|---|")
    held = {}
    for name, store in [("a full pass", FULL_RUNS),
                        ("this delta pass", RUNS)]:
        runs = 0
        seconds = 0.0
        if os.path.exists(store):
            handle = open(store)
            for line in handle:
                text = line.strip()
                if not text:
                    continue
                run = json.loads(text)
                runs = runs + 1
                seconds = seconds + (run.get("seconds") or 0)
                continue
            handle.close()
        held[name] = (runs, seconds)
        each = 0.0
        if runs:
            each = round(seconds / runs, 2)
        say("| %s | %d | %s | %s |" % (name, runs, round(seconds), each))
        continue
    full = held["a full pass"]
    delta = held["this delta pass"]
    if full[0] and full[1]:
        say("")
        say("the delta pass ran %s%% of the full pass's runs and cost "
            "%s%% of its seconds."
            % (round(100.0 * delta[0] / full[0], 1),
               round(100.0 * delta[1] / full[1], 1)))
    say("")
    say("Table D6 -- what the full pass answered, so the delta's own "
        "answers can be read against a pass that attempted everything.")
    say("")
    document = read_json(AGGREGATE)
    say("| | delta | full |")
    say("|---|---|---|")
    say("| runs | %d | %d |" % (delta[0], full[0]))
    say("| place-triples proved | %d | %d |"
        % (proved_places(RUNS), proved_places(FULL_RUNS)))
    say("| pairs proved, STRICT | %d | %d |"
        % (strict_pairs(RUNS), strict_pairs(FULL_RUNS)))
    say("| newly certified against the bank as it stood | %d | -- |"
        % document["cost"]["newly_certified"])
    say("")
    say("peak resident: %d kB" % peak_kb())
    return 0


def proved_places(store):
    """how many written places one store proved."""
    if not os.path.exists(store):
        return 0
    total = 0
    handle = open(store)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        run = json.loads(text)
        for place in run.get("places") or []:
            if BK.kind_of_place(place) == "proved":
                total = total + 1
            continue
        continue
    handle.close()
    return total


def strict_pairs(store):
    """how many (cell, target) pairs one store proved on the STRICT
    reading -- every written place proved."""
    if not os.path.exists(store):
        return 0
    total = 0
    handle = open(store)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        run = json.loads(text)
        places = run.get("places") or []
        if not places:
            continue
        if BK.every_place_proved(places):
            total = total + 1
        continue
    handle.close()
    return total


def bank_audit_command():
    """every audited triple and its answer."""
    document = read_json(AGGREGATE)
    say("Table D4 -- every audited (cell, target, written place), its "
        "certificate's kind and the kind the re-derivation answered, "
        "and whether the inputs were identical.  A row whose inputs "
        "were identical and whose kinds differ is an ALARM; a row whose "
        "source sha256 moved is a CHANGED ARTIFACT and is banked as a "
        "new certificate beside the old one, never in place of it.")
    say("")
    say("| `mnem` | shape | `key_width` | target | place | the "
        "certificate's pass | certificate | re-derived | inputs "
        "identical | reading |")
    say("|---|---|---|---|---|---|---|---|---|---|")
    for row in document["audit"]:
        say("| `%s` | %s | %s | %s | `%s` | `%s` | %s | %s | %s | %s |"
            % (row["cell"]["mnem"], row["cell"]["shape"],
               row["cell"]["key_width"], row["target"], row["place"],
               row["certificate_pass"], row["certificate_kind"],
               row["rederived_kind"],
               yes_or_no(row["inputs_identical"]), row["reading"]))
        continue
    say("")
    counted = {}
    for row in document["audit"]:
        counted[row["reading"]] = counted.get(row["reading"], 0) + 1
        continue
    say("| reading | rows |")
    say("|---|---|")
    for reading in sorted(counted):
        say("| %s | %d |" % (reading, counted[reading]))
        continue
    say("")
    say("peak resident: %d kB" % peak_kb())
    return 0


def bank_tally_command():
    """the counts, printed."""
    say("lines on %s: %d" % (RUNS, count_lines(RUNS)))
    if os.path.exists(FULL_RUNS):
        say("lines on %s: %d" % (FULL_RUNS, count_lines(FULL_RUNS)))
    if os.path.exists(SRC_DIR):
        say("rendered sources under %s: %d"
            % (SRC_DIR, len(os.listdir(SRC_DIR))))
    document = read_json(AGGREGATE)
    say("runs executed: %d" % document["cost"]["runs_executed"])
    say("alarms: %d" % document["cost"]["alarms"])
    say("peak resident: %d kB" % peak_kb())
    return 0


def yes_or_no(value):
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return "--"


def count_lines(path):
    if not os.path.exists(path):
        return 0
    total = 0
    handle = open(path)
    for _line in handle:
        total = total + 1
        continue
    handle.close()
    return total


# ==================================================================
# section 2: THE DELTA AND THE AUDIT SAMPLE
# ==================================================================

def the_delta():
    """what this pass attempts and what it audits, read off the bank.

    THREE SETS AND ONE SAMPLE.
      * CERTIFIED is every key the bank holds a certificate of kind
        `proved` or `agreed` for.  A certified key is only ever
        re-derived through the audit.
      * KNOWN is every (cell, target) with the keys any pass ever
        recorded for it, which is how the delta knows what a pair's
        places and setters ARE without running it.
      * The delta is KNOWN minus CERTIFIED, FILTERED BY CODE VERSION:
        an uncertified key is attempted again only when the code
        version on its certificate differs from the version running now
        for that target.  That is what replaced the task label -- a
        refusal or a `sat` is re-derived because the machinery MOVED,
        not because a new task asked.  A key no pass ever reached is
        attempted whatever the version, and a pair no pass ever ran is
        attempted whole.
      * The audit is `AUDIT_SHARE` of CERTIFIED, chosen by
        `random.Random(AUDIT_DATE)` over the sorted list, so the sample
        is the same every time this pass is re-run and different on the
        next date.  At `--audit-share 1` it is every certificate, which
        is the guard the removal of the task gates is measured by.

    A KEY IS (cell, target, written place, SETTER CELL).  The setter is
    part of it because a flag consumer rendered over another setter cell
    is another artifact: the pair is the node, so the pair is the key."""
    certified = set()
    known = {}
    version_on_record = {}
    for cert in BK.stream(BK.BANK):
        target = cert["target"]
        if target not in TARGETS:
            continue
        pair = BK.pair_tuple(cert)
        key = BK.key_tuple(cert)
        known.setdefault(pair, set())
        if cert["place"] is not None:
            known[pair].add((cert["place"], BK.setter_tuple(cert)))
        if cert["kind"] in ("proved", "agreed"):
            certified.add(key)
        if cert["preferred"]:
            version_on_record[key] = version_key(cert.get("code_version"))
        continue
    current = {}
    for lang in TARGETS:
        current[lang] = version_key(code_version_of(lang))
    cells = read_json(CELLS)
    pairs = []
    for record in cells["asked"]:
        asked = (record["asked"]["mnem"], record["asked"]["shape"],
                 record["asked"]["key_width"])
        for lang in TARGETS:
            pairs.append((asked, lang, record["attested_ledger_rows"]))
            continue
        continue
    attempt = []
    held_by_version = 0
    never = 0
    for asked, lang, ledger in pairs:
        pair = (asked[0], asked[1], asked[2], lang)
        places = known.get(pair)
        if places is None:
            never = never + 1
            attempt.append((pair, None, None))
            continue
        if not places:
            attempt.append((pair, None, None))
            continue
        for place, setter in sorted(places,
                                    key=lambda p: ("%s" % (p[0],),
                                                   "%s" % (p[1],))):
            key = (pair[0], pair[1], pair[2], pair[3], place, setter)
            if key in certified:
                continue
            if version_on_record.get(key) == current[lang]:
                # THE RE-ATTEMPT RULE.  The machinery that answered this
                # key is the machinery running now, so deriving it again
                # would produce the same artifact and the same verdict.
                held_by_version = held_by_version + 1
                continue
            attempt.append((pair, place, setter))
            continue
        continue
    if not ATTEMPTS_ARE_ON:
        attempt = []
    audit = the_audit_sample(certified)
    attempt_pairs = set()
    for pair, _place, _setter in attempt:
        attempt_pairs.add(pair)
        continue
    audit_pairs = set()
    for key in audit:
        audit_pairs.add((key[0], key[1], key[2], key[3]))
        continue
    execute = attempt_pairs | audit_pairs
    order = []
    for asked, lang, ledger in pairs:
        pair = (asked[0], asked[1], asked[2], lang)
        if pair not in execute:
            continue
        order.append((asked, lang, ledger))
        continue
    known_triples = 0
    for pair in known:
        known_triples = known_triples + max(1, len(known[pair]))
        continue
    return {
        "certified_before": len(certified),
        "attempt_triples": len(attempt),
        "attempt_pairs": len(attempt_pairs),
        "attempt_list": attempt,
        "held_by_version": held_by_version,
        "audit_triples": len(audit),
        "audit_triples_list": audit,
        "audit_pairs": len(audit_pairs),
        "runs_to_execute": len(order),
        "runs_list": order,
        "pairs_total": len(pairs),
        "pairs_never_attempted": never,
        "known_triples": known_triples,
        "code_version": current,
    }


def the_audit_sample(certified):
    """5% of the certified triples, chosen by `random.Random(<date>)`.

    THE SORT IS THE POINT.  A set has no order, so a sample drawn over
    a set is not reproducible; the list is sorted into one fixed order
    first and the seeded generator draws over that, so this pass's
    sample can be re-derived by anyone with the same bank and the same
    date."""
    held = sorted(certified, key=lambda k: tuple("%s" % p for p in k))
    if not held:
        return []
    many = int(round(len(held) * AUDIT_SHARE))
    if many < 1:
        many = 1
    if many > len(held):
        many = len(held)
    chooser = random.Random(AUDIT_DATE)
    return sorted(chooser.sample(held, many),
                  key=lambda k: tuple("%s" % p for p in k))


def certificates_for(keys):
    """the certificate the bank prefers for each audited key, with the
    four fields an alarm is decided on."""
    wanted = set(keys)
    out = {}
    for cert in BK.stream(BK.BANK):
        key = BK.key_tuple(cert)
        if key not in wanted:
            continue
        if not cert["preferred"]:
            continue
        out[key] = {
            "kind": cert["kind"],
            "term_text": cert["term_text"],
            "sha256": (cert["source"] or {}).get("sha256"),
            "flags": (cert["compiler"] or {}).get("flags"),
            "version": (cert["compiler"] or {}).get("version"),
            "pass": cert["produced_by"]["pass"],
        }
        continue
    return out


# ==================================================================
# section 3: THE WALK
# ==================================================================

def walk(order, store, done, limit, certificates, plan):
    """the runs, one line per finished run, with the audit checked as
    each run comes back.

    ONE PAIR IS SEVERAL RUNS WHERE THE CORPUS ATTESTS SEVERAL SETTERS.
    `handful.cell_inputs` answers one held cell per setter cell the
    corpus attests before this consumer, and each is rendered, compiled,
    carved and gated on its own, because the pair IS the node and a
    consumer over another setter is another artifact.  A cell that reads
    no flag state answers exactly one held cell, which is every cell the
    loop ran before 2026-09-10.

    AN ALARM STOPS THE PASS, which is the brief's own rule: a re-derived
    verdict that differs from its certificate on identical inputs means
    the machinery and the record disagree, and running on would bank
    more records from machinery already known to disagree."""
    shared = H.build_shared()
    say("the gate of record: %d ms; the one re-pose: %d ms"
        % (shared["gate"].solver_timeout_ms, REPOSE_MS))
    reposer = G.Gate(reference=shared["reference"],
                     solver_timeout_ms=REPOSE_MS)
    MTAB._install_gpr_widths()
    in_table = H.load_in_table()
    say("the table's own TRANSLATED triples, for the composition step: %d"
        % len(in_table))
    say("peak resident after the two reads: %d kB"
        % check_memory("after load_in_table"))
    cells = read_json(CELLS)
    audit_rows = []
    alarms = []
    total = len(order)
    index = 0
    ran = 0
    started = time.time()
    for asked, lang, ledger in order:
        index = index + 1
        say("[%d/%d] %s %s %s -> %s (ledger_rows %d)"
            % (index, total, asked[0], asked[1], asked[2], lang,
               ledger))
        for record in one_pair(shared, reposer, cells, asked, lang,
                               ledger, in_table, done):
            if record is None:
                continue
            append_run(store, record)
            ran = ran + 1
            say("   %s | %s | %s | %d s | peak resident: %d kB"
                % (record.get("route") or "-",
                   setter_label(record), one_line_verdict(record),
                   round(record["seconds"]),
                   check_memory("run %d" % index)))
            for row in audited_rows_of(record, asked, lang,
                                       certificates):
                audit_rows.append(row)
                if row["reading"] == "ALARM":
                    alarms.append(row)
                continue
            continue
        if alarms:
            say("")
            say("ALARM: the re-derived verdict differs from the "
                "certificate on IDENTICAL inputs.  The pass stops here, "
                "as the brief requires.")
            for row in alarms:
                say("   %s %s %s on %s at %s: the certificate says %s, "
                    "the re-derivation says %s"
                    % (row["cell"]["mnem"], row["cell"]["shape"],
                       row["cell"]["key_width"], row["target"],
                       row["place"], row["certificate_kind"],
                       row["rederived_kind"]))
                continue
            break
        if limit is not None and ran >= limit:
            say("")
            say("the sample's own stop: %d run(s) performed" % ran)
            break
        continue
    seconds = round(time.time() - started)
    say("")
    say("runs performed this lane: %d in %d s" % (ran, seconds))
    say("lines on %s: %d" % (store, count_lines(store)))
    say("audited place-triples this lane: %d" % len(audit_rows))
    say("alarms: %d" % len(alarms))
    say("peak resident: %d kB" % peak_kb())
    if plan is not None:
        write_cost(plan, store, ran, seconds, audit_rows, alarms)
    if alarms:
        return 1
    return 0


def one_pair(shared, reposer, cells, asked, lang, ledger, in_table,
             done):
    """every run of one (cell, target): one per held cell the driver
    answers, which is one per attested setter where the cell reads a
    flag state and exactly one where it does not."""
    started = time.time()
    try:
        held_cells = H.cell_inputs(cells, asked)
    except Exception as problem:                              # noqa: BLE001
        record = {
            "mnem": asked[0], "shape": asked[1], "key_width": asked[2],
            "lang": lang, "attested_ledger_rows": ledger, "places": [],
            "refusal_cause": CAUSE_DRIVER,
            "refusal_detail": named(problem),
            "refusal_traceback": last_frame(problem),
            "composition": [],
            "code_version": code_version_of(lang),
            "seconds": round(time.time() - started, 3),
        }
        return [record]
    out = []
    for held in held_cells:
        if key_of(asked, lang, held.get("setter")) in done:
            continue
        out.append(one_run(shared, reposer, held, asked, lang, ledger,
                           in_table))
        continue
    return out


def one_run(shared, reposer, held, asked, lang, ledger, in_table):
    """one held cell of one (cell, target), wrapped.

    THE WRAP IS THE LOOP'S OWN RULE: a cell the route cannot handle is a
    RESULT BY CAUSE.  An exception out of the driver is recorded as this
    run's `refusal_cause` with the exception LITERAL and the line it came
    from, and the loop goes on."""
    started = time.time()
    record = {
        "mnem": asked[0],
        "shape": asked[1],
        "key_width": asked[2],
        "lang": lang,
        "attested_ledger_rows": ledger,
        "places": [],
    }
    try:
        record = H.find_emulation(shared, held, lang)
        record["attested_ledger_rows"] = ledger
    except Exception as problem:                              # noqa: BLE001
        record["refusal_cause"] = CAUSE_DRIVER
        record["refusal_detail"] = named(problem)
        record["refusal_traceback"] = last_frame(problem)
        record["composition"] = []
        record["setter"] = held.get("setter")
        record["code_version"] = code_version_of(lang)
        record["seconds"] = round(time.time() - started, 3)
        return record
    # THE TWO STEPS AFTER THE RUN are wrapped separately, so a failure
    # in either is recorded as its own field and never as a refusal of
    # the run itself.
    try:
        reposed(shared, reposer, held, record)
    except Exception as problem:                              # noqa: BLE001
        record["repose_refusal"] = named(problem)
        record["repose_refusal_traceback"] = last_frame(problem)
    try:
        record["composition"] = H.composition_of_run(record, in_table)
    except Exception as problem:                              # noqa: BLE001
        record["composition"] = []
        record["composition_refusal"] = named(problem)
        record["composition_refusal_traceback"] = last_frame(problem)
    record["code_version"] = code_version_of(lang)
    record["seconds"] = round(time.time() - started, 3)
    return record


def reposed(shared, reposer, held, record):
    """every gate call the 3,000 ms ceiling left UNDECIDED, re-posed
    ONCE with more room.

    THE LAW'S RULE, followed literally: a time limit is a FLAG, so the
    obligation is re-run with a larger ceiling and whether the answer
    changed is reported.  The verdict OF RECORD stays the one the
    pipeline's own ceiling gave and this answer sits beside it."""
    if record.get("refusal_cause") is not None:
        return
    cache = {(held["mnem"], held["shape"], held["key_width"]): held}
    of_record = shared["gate"]
    for place in record.get("places") or []:
        check = place.get("check") or {}
        if check.get("outcome") != "UNDECIDED":
            continue
        if not place.get("compiled"):
            continue
        shared["gate"] = reposer
        try:
            again = H.one_recheck(shared, cache, record, place)
        finally:
            shared["gate"] = of_record
        again["ceiling_ms"] = REPOSE_MS
        check["recheck"] = again
        continue
    return


def named(problem):
    """an exception as the record carries it: its own class and its own
    message, LITERAL."""
    return "%s: %s" % (type(problem).__name__, problem)


def last_frame(problem):
    """the one line of the traceback that names where the driver
    stopped, LITERAL."""
    frames = traceback.extract_tb(problem.__traceback__)
    if not frames:
        return ""
    frame = frames[-1]
    return "%s:%d in %s -- %s" % (os.path.basename(frame.filename),
                                  frame.lineno, frame.name, frame.line)


def key_of(asked, lang, setter):
    """the identity of one run on the incremental store, so a stopped
    lane resumes by skipping what it already wrote.  The setter is part
    of it because a consumer over another setter is another run."""
    return (asked[0], asked[1], asked[2], lang, setter_key(setter))


def setter_key(setter):
    """the setter's own cell, as a tuple, or None where the cell reads
    no flag state."""
    if not setter:
        return None
    return (setter.get("mnem"), setter.get("shape"),
            setter.get("key_width"))


def setter_label(record):
    """the setter this run was rendered over, for the lane's progress
    line."""
    setter = record.get("setter")
    if not setter:
        return "-"
    return "%s %s %s" % (setter.get("mnem"), setter.get("shape"),
                         setter.get("key_width"))


def one_line_verdict(run):
    """the run's answer on one line, for the lane's own progress
    print."""
    verdict = H.verdict_of_run(run)
    if verdict["cause"]:
        return "REFUSED: %s" % verdict["cause"][:70]
    return "%s / %s" % (verdict["landed"], verdict["gate"])


def append_run(store, record):
    """one finished run, appended and flushed to the operating system
    before the next run begins, so a lane the wall clock stops loses
    nothing."""
    handle = open(store, "a")
    handle.write(json.dumps(LOOP.as_machine_form(record),
                            sort_keys=True))
    handle.write("\n")
    handle.flush()
    os.fsync(handle.fileno())
    handle.close()
    return


def already_recorded(store):
    """the (cell, target) pairs already on a store, so a stopped lane
    resumes by skipping them."""
    out = set()
    if not os.path.exists(store):
        return out
    handle = open(store)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        run = json.loads(text)
        asked = (run["mnem"], run["shape"], run["key_width"])
        out.add(key_of(asked, run["lang"], run.get("setter")))
        continue
    handle.close()
    return out


def audited_rows_of(record, asked, lang, certificates):
    """every audited place of one finished run, read against its
    certificate."""
    out = []
    places = {}
    for place in record.get("places") or []:
        places[place.get("writes")] = place
        continue
    for key in sorted(certificates,
                      key=lambda k: tuple("%s" % p for p in k)):
        if key[0] != asked[0]:
            continue
        if key[1] != asked[1]:
            continue
        if key[2] != asked[2]:
            continue
        if key[3] != lang:
            continue
        out.append(one_audited_row(record, key, places.get(key[4]),
                                   certificates[key]))
        continue
    return out


def one_audited_row(record, key, place, cert):
    """one audited (cell, target, written place), and the reading.

    THE THREE READINGS OF AN AUDIT, and only the first is an alarm:
      * ALARM -- the inputs are identical (same term text, same source
        sha256, same compiler and flags) and the kind differs.  The
        machinery and the record disagree about the same artifact.
      * `the artifact changed` -- the source sha256 moved, so the
        renderer built something else and this is a NEW certificate
        beside the old one, never a replacement.  The brief's own
        words.
      * `not reproduced` -- the re-derivation produced no place at all
        for this key.  The certificate stands; the machinery could not
        reproduce it, which is the one direction the brief says is
        possible."""
    row = {
        "cell": {"mnem": key[0], "shape": key[1], "key_width": key[2]},
        "target": key[3],
        "place": key[4],
        "setter": setter_record(key[5]),
        "certificate_kind": cert["kind"],
        "certificate_pass": cert["pass"],
        "rederived_kind": None,
        "inputs_identical": None,
        "reading": "not reproduced",
        "certificate_sha256": cert["sha256"],
        "rederived_sha256": None,
    }
    if place is None:
        row["cause"] = record.get("refusal_cause")
        return row
    row["rederived_kind"] = BK.kind_of_place(place)
    text = place.get("source")
    if text is not None:
        row["rederived_sha256"] = hashlib.sha256(
            text.encode("utf-8")).hexdigest()
    same = True
    if row["rederived_sha256"] != cert["sha256"]:
        same = False
    if place.get("text") != cert["term_text"]:
        same = False
    if BK.ship_flags_source(key[3]) != cert["flags"]:
        same = False
    row["inputs_identical"] = same
    if not same:
        row["reading"] = "the artifact changed"
        return row
    if row["rederived_kind"] != cert["kind"]:
        row["reading"] = "ALARM"
        return row
    row["reading"] = "reproduced"
    return row


def setter_record(setter):
    """one setter cell as a record with its mnemonic in `mnem`, which is
    the machine form the guard reads, or None where the cell reads no
    flag state."""
    if setter is None:
        return None
    return {"mnem": setter[0], "shape": setter[1],
            "key_width": setter[2]}


def write_cost(plan, store, ran, seconds, audit_rows, alarms):
    """the aggregate: the five counts the brief names, the audit's own
    rows, and the full pass to stand them against."""
    newly = newly_certified(store, plan)
    full_runs = plan["pairs_total"]
    full_seconds = full_pass_seconds()
    document = {
        "meta": {
            "pass": PASS_LABEL,
            "what": "one delta-plus-audit pass over the five compiled "
                    "targets",
            "code_version": plan["code_version"],
            "attempts_are_on": ATTEMPTS_ARE_ON,
            "cells_source": CELLS,
            "bank": BK.BANK,
            "store": store,
            "audit_share": AUDIT_SHARE,
            "audit_seed": AUDIT_DATE,
            "solver_ceiling_ms": SOLVER_MS,
            "repose_ceiling_ms": REPOSE_MS,
            "memory_bound_kb": ABORT_KB,
            "memory_abort": ABORT_NAME,
            "peak_kb": peak_kb(),
            "targets": TARGETS,
        },
        "cost": {
            "certified_before": plan["certified_before"],
            "attempted": plan["attempt_triples"],
            "held_by_the_code_version": plan["held_by_version"],
            "newly_certified": newly,
            "audited": len(audit_rows),
            "alarms": len(alarms),
            "runs_executed": ran,
            "seconds": seconds,
            "full_pass_runs": full_runs,
            "full_pass_seconds": full_seconds,
        },
        "audit": audit_rows,
    }
    write_json(AGGREGATE, document)
    return


def newly_certified(store, plan):
    """how many of the attempted place-triples this pass certified."""
    wanted = set()
    unknown = set()
    for pair, place, setter in plan["attempt_list"]:
        if place is None:
            unknown.add(pair)
            continue
        wanted.add((pair[0], pair[1], pair[2], pair[3], place, setter))
        continue
    got = 0
    handle = open(store)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        run = json.loads(text)
        pair = (run["mnem"], run["shape"], run["key_width"], run["lang"])
        for place in run.get("places") or []:
            key = (pair[0], pair[1], pair[2], pair[3],
                   place.get("writes"), setter_key(run.get("setter")))
            if key not in wanted and pair not in unknown:
                continue
            if BK.kind_of_place(place) != "proved":
                continue
            got = got + 1
            continue
        continue
    handle.close()
    return got


def full_pass_seconds():
    """what a full pass over the four compiled targets cost, read off
    task ap5's own aggregate rather than restated."""
    path = os.path.join(HERE, "autopoly5.json")
    if not os.path.exists(path):
        return None
    document = read_json(path)
    held = document.get("seconds")
    if isinstance(held, dict):
        return held.get("total")
    return held


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
