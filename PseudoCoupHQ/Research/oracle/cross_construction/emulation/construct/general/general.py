#!/usr/bin/env python3
"""general.py -- THE GENERAL TIER: every place the native route did not
prove, rendered again by `render_general` -- one named intermediate per
node, the language's own operator where it has one and the construction
where it does not -- then compiled, carved, gated, and the construction's
own equality discharged per OPERATION KIND.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_t4_brief.md`.

THE OBJECTS, one sentence each, in relation.
  * THE NATIVE ROUTE is `handful.the_native_route`, the driver as task
    ap6 left it, unchanged and called and never copied.
  * THE GENERAL TIER is `general_tier` below: per place, the term
    rendered by `render_general.render` under a POLICY, compiled at the
    corpus's ship flags, carved, and gated.
  * THE TWO POLICIES are `native_first` -- the brief's own rule, the
    language's own operator wherever it has one -- and
    `all_constructed`, where the construction answers every node whose
    kind has one.  The second is the GUARANTEE's own measurement and
    the first is the route of record; both are attempted per place and
    whichever proves is the one banked, which is task t2's section 3
    rule ("whoever gets there first") read at the run.
  * TWO OBLIGATIONS, not one, exactly as task t2 states them.  THE GATE
    answers whether the carved body equals the term the render actually
    wrote; THE EQUALITY answers whether that term is the CELL's own.
  * THE EQUALITY IS DISCHARGED PER OPERATION KIND.  Where the render
    constructed nothing the two terms are the same object and the
    canonical form fires with no solver.  Where it constructed
    something, every constructed node is one application of a
    construction whose correctness at that (kind, width, word) is
    proved ONCE -- by a Lean lemma where one closes, else by z3 on the
    construction alone -- and the composition is equal by structural
    induction on the term.  z3 on the whole miter is the last resort
    and is bounded at the brief's hard 30 seconds.

MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4, checked after
every store line.

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

HOW THIS FILE OBEYS IT.  Which places the tier acts on is the bank's own
keys; which route a node takes is whether the target's renderer raises;
a cell is addressed by (`mnem`, operand shape, `key_width`), and the
mnemonic sits in `mnem`, which the ruling of 2026-09-08 states is
machine form.

usage:
  general.py preflight            what the pass would attempt
  general.py run [<n>]            the pass; `<n>` stops after n runs
  general.py bank                 the bank rebuilt with this pass in it
  general.py readings             the three readings with this pass in
  general.py report               `general.md`
  general.py tier <mnem> <shape> <width> <lang>
                                  one (cell, target), printed

Coding discipline: no compound one-liner statements.
"""

import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CONSTRUCT = os.path.normpath(os.path.join(HERE, ".."))
EMULATION = os.path.normpath(os.path.join(CONSTRUCT, ".."))
HANDFUL = os.path.join(EMULATION, "handful")
AUTOPOLY = os.path.join(EMULATION, "autopoly")
sys.path.insert(0, HERE)
sys.path.insert(0, CONSTRUCT)
sys.path.insert(0, HANDFUL)
sys.path.insert(0, AUTOPOLY)
sys.path.insert(0, EMULATION)
sys.path.insert(0, os.path.join(EMULATION, "rust"))
sys.path.insert(0, os.path.join(EMULATION, "go"))
sys.path.insert(0, os.path.join(EMULATION, "swift"))

import z3                                                        # noqa: E402
import build as B                                                # noqa: E402
import render_general as RG                                      # noqa: E402

PASS_LABEL = "t4_general"

REPORT = os.path.join(HERE, "general.md")
AGGREGATE = os.path.join(HERE, "general.json")
PROOFS = os.path.join(HERE, "construction_proofs.json")

ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_T4"

EQUALITY_CEILING_MS = 30000
"""the brief's HARD ceiling on the last resort; never raised."""

POLICIES = ("native_first", "all_constructed")

CAUSE_ALREADY_PROVED = ("the native route proved this place, so there "
                        "is nothing the general tier can add")
CAUSE_NOT_RENDERED_UPSTREAM = ("the native route did not reach this "
                               "place's term at all, so the tier has "
                               "nothing to render")
CAUSE_EQUALITY = ("the carved body is proved equal to the term the "
                  "render wrote, and that term's equality with the "
                  "CELL's own is not discharged by any of the three "
                  "forms")
CAUSE_NO_80_BIT_HOLDER = ("an arrival or answer home on the x87 stack: "
                          "%s has no 80-bit holder, so the value cannot "
                          "be received or answered with at all")


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


def word_of(lang):
    import construct as CONS
    return CONS.word_of(lang)


# ==================================================================
# section 1: the proof table, one row per (kind, width, word)
# ==================================================================

PROOF_CACHE = None


def proof_table():
    """{(kind, width, word): the row} -- the construction's own proof at
    that instance, off `construction_proofs.json`, which
    `collect_proofs.py` writes from the Lean lemmas and from
    `check_constructions.py`'s z3 rows.

    A row's `form` is `lemma` (a Lean theorem closed), `sat` (z3 proved
    the construction equal to the operation at that instance) or absent
    (neither)."""
    global PROOF_CACHE
    if PROOF_CACHE is not None:
        return PROOF_CACHE
    PROOF_CACHE = {}
    if not os.path.exists(PROOFS):
        return PROOF_CACHE
    handle = open(PROOFS)
    document = json.load(handle)
    handle.close()
    for row in document.get("rows") or []:
        key = (row["kind"], int(row["width"]), int(row["word"]))
        PROOF_CACHE[key] = row
        continue
    return PROOF_CACHE


def the_equality(cell_term, built_term, constructed_widths, word):
    """whether the term the render WROTE is the cell's own mapping, in
    the three forms the brief names, in the brief's order."""
    import handful as H
    import term as T
    out = {"forms": []}
    started = time.time()
    if built_term.get_id() == cell_term.get_id():
        out["forms"].append({"form": "canonical", "answer": True})
        out["proof"] = "canonical"
        out["outcome"] = "PROVED"
        out["reason"] = ("the render wrote the cell's own term: every "
                         "node of it is the target's own operator, so "
                         "there is nothing constructed to discharge")
        out["seconds"] = round(time.time() - started, 3)
        return out
    holder = T.Term()
    cell_posed = H.the_normalised_term(cell_term)
    built_posed = H.the_normalised_term(built_term)
    cell_text = holder.normalize(cell_posed)
    built_text = holder.normalize(built_posed)
    same = (cell_text == built_text)
    out["forms"].append({"form": "canonical", "answer": same})
    if same:
        out["proof"] = "canonical"
        out["outcome"] = "PROVED"
        out["reason"] = ("the cell's mapping and the term the render "
                         "wrote print the same text under the "
                         "pipeline's own normaliser")
        out["seconds"] = round(time.time() - started, 3)
        return out
    table = proof_table()
    held = []
    missing = []
    for kind in sorted(constructed_widths):
        for width in sorted(constructed_widths[kind]):
            key = (kind, int(width), word)
            entry = {"kind": kind, "width": int(width), "word": word,
                     "nodes": constructed_widths[kind][width]}
            found = table.get(key)
            if found is None:
                entry["why"] = ("no proof is recorded for this "
                                "construction at this width over this "
                                "word")
                missing.append(entry)
                continue
            if found.get("form") is None:
                entry["why"] = ("the construction's own proof at this "
                                "instance is %s" % found.get("outcome"))
                missing.append(entry)
                continue
            entry["form"] = found["form"]
            entry["proof_of_record"] = found.get("theorem") \
                or found.get("outcome")
            held.append(entry)
            continue
        continue
    answered = bool(held) and not missing
    out["forms"].append({"form": "kind lemma", "answer": answered,
                         "proofs_held": held,
                         "proofs_missing": missing})
    if answered:
        out["proof"] = "kind"
        out["outcome"] = "PROVED"
        out["reason"] = ("every node the render CONSTRUCTED is one "
                         "application of a construction proved equal "
                         "to the operation it replaced at that width "
                         "over that word; the render is one such "
                         "replacement per node, so the two terms are "
                         "equal by structural induction on the term")
        out["seconds"] = round(time.time() - started, 3)
        return out
    solver = z3.Solver()
    solver.set("timeout", EQUALITY_CEILING_MS)
    solver.add(cell_posed != built_posed)
    answer = solver.check()
    out["forms"].append({"form": "sat", "answer": str(answer)})
    out["solver_timeout_ms"] = EQUALITY_CEILING_MS
    out["seconds"] = round(time.time() - started, 3)
    if answer == z3.unsat:
        out["proof"] = "sat"
        out["outcome"] = "PROVED"
        out["reason"] = ("z3 found no input at which the cell's mapping "
                         "and the term the render wrote differ")
        return out
    out["proof"] = None
    if answer == z3.sat:
        out["outcome"] = "DISPROVED"
        out["reason"] = ("z3 found an input at which the cell's mapping "
                         "and the term the render wrote differ")
        out["counterexample"] = str(solver.model())[:400]
        return out
    out["outcome"] = "UNDECIDED"
    out["reason"] = ("z3 answered neither way inside the brief's hard "
                     "30-second ceiling; the ceiling is the brief's own "
                     "and is not raised")
    return out


# ==================================================================
# section 2: one place, one policy
# ==================================================================

def general_tier(shared, held, lang, record):
    """the driver's ONE call: every place of this run rendered again by
    the general render, under both policies.

    Returns None where the tier rendered nothing for any place."""
    word = word_of(lang)
    if word is None:
        return None
    inputs = held.get("places")
    if not inputs:
        return None
    natives = record.get("places") or []
    out = []
    reached = False
    started = time.time()
    for index, place in enumerate(inputs):
        native = None
        if index < len(natives):
            native = natives[index]
        made = one_place(shared, held, lang, place, native, word, index)
        out.append(made)
        if made.get("check") is not None:
            reached = True
        continue
    return {
        "route": "general",
        "word_bits": word,
        "places": out,
        "reached_the_gate": reached,
        "rendered_any_place": any_rendered(out),
        "seconds": round(time.time() - started, 3),
    }


def any_rendered(places):
    for place in places:
        if place.get("rendered"):
            return True
        continue
    return False


def one_place(shared, held, lang, place, native, word, index):
    """one written place through the general tier: both policies, the
    better answer kept."""
    import handful as H
    out = {
        "writes": place["writes"],
        "text": place.get("text"),
        "sexpr": place.get("sexpr"),
        "bits": place.get("bits"),
        "families": place.get("families"),
        "home": place.get("home"),
    }
    if place.get("halved") is not None:
        out["halved"] = place["halved"]
    if native is not None:
        check = (native.get("check") or {})
        if check.get("outcome") == "PROVED_ON_SHIP":
            out["rendered"] = False
            out["refusal_cause"] = CAUSE_ALREADY_PROVED
            return out
    if place.get("not_rendered") is not None:
        out["rendered"] = False
        out["refusal_cause"] = CAUSE_NOT_RENDERED_UPSTREAM
        out["refusal_detail"] = place["not_rendered"]
        return out
    working = place
    if place.get("halved") is None:
        projected = H.projected_lane(shared, place, held["key_width"])
        if projected is not None:
            out["lane"] = projected["lane"]
            if projected.get("refusal_cause") is not None:
                out["rendered"] = False
                out["refusal_cause"] = CAUSE_NOT_RENDERED_UPSTREAM
                out["refusal_detail"] = projected["refusal_cause"]
                return out
            working = projected["place"]
    if working.get("term") is None:
        out["rendered"] = False
        out["refusal_cause"] = CAUSE_NOT_RENDERED_UPSTREAM
        out["refusal_detail"] = "the place carries no term"
        return out
    attempts = []
    for policy in POLICIES:
        attempt = one_attempt(shared, held, lang, working, place, word,
                              policy, index)
        attempts.append(attempt)
        continue
    out["attempts"] = attempts
    chosen = the_better(attempts)
    if chosen is None:
        out["rendered"] = False
        out["refusal_cause"] = attempts[0].get("refusal_cause") \
            or attempts[1].get("refusal_cause") or "no attempt rendered"
        out["refusal_detail"] = attempts[0].get("refusal_detail")
        return out
    for field in ("rendered", "source", "source_path", "symbol",
                  "compiled", "compile_refusal", "body_bytes",
                  "body_text", "landing", "label", "policy",
                  "statements", "constructed_kinds",
                  "constructed_widths", "native_nodes",
                  "constructed_nodes", "check",
                  "gate_on_the_written_term", "equality",
                  "refusal_cause", "refusal_detail", "proof"):
        if field in chosen:
            out[field] = chosen[field]
            continue
    return out


def the_better(attempts):
    """whoever gets there first: the attempt that PROVED, and the
    smaller carved body where both did; else the one that reached the
    gate; else the first that rendered."""
    proved = []
    for attempt in attempts:
        check = attempt.get("check") or {}
        if check.get("outcome") == "PROVED_ON_SHIP":
            proved.append(attempt)
            continue
        continue
    if proved:
        proved.sort(key=lambda one: one.get("instructions") or 10 ** 6)
        return proved[0]
    for attempt in attempts:
        if attempt.get("gate_on_the_written_term") is not None:
            return attempt
        continue
    for attempt in attempts:
        if attempt.get("rendered"):
            return attempt
        continue
    return None


def one_attempt(shared, held, lang, working, place, word, policy,
                index):
    """one policy: render, compile, carve, gate, discharge."""
    import emulate as E
    import handful as H
    out = {"policy": policy}
    label = E.sanitize("%s_%s_%d__%s__%s__%s"
                       % (held["mnem"], held["shape"], held["key_width"],
                          place["writes"].replace(".", "_"), lang,
                          policy))
    out["label"] = label
    term = working["term"]
    ordered = H.renderer_input(term)
    home = working["home"]
    if E.is_an_x87_arrival(home.get("family")):
        if lang not in H.TARGETS_WITH_AN_80_BIT_HOLDER:
            out["rendered"] = False
            out["refusal_cause"] = CAUSE_NO_80_BIT_HOLDER % lang
            return out
        ordered = H.the_x87_value(ordered)
    try:
        made = RG.render(ordered, lang, working["families"],
                         home["family"], working["bits"], label, word,
                         policy, working.get("text") or "")
    except Exception as problem:
        if not RG.is_a_refusal(problem):
            out["rendered"] = False
            out["refusal_cause"] = "the render raised"
            out["refusal_detail"] = "%s: %s" % (type(problem).__name__,
                                                problem)
            return out
        out["rendered"] = False
        out["refusal_cause"] = getattr(problem, "cause", "%s" % problem)
        out["refusal_detail"] = getattr(problem, "detail", "")
        return out
    out["rendered"] = True
    out["source"] = made["source"]
    out["symbol"] = made["symbol"]
    out["statements"] = made["statements"]
    out["native_nodes"] = made["native_nodes"]
    out["constructed_nodes"] = made["constructed_nodes"]
    out["constructed_kinds"] = made["constructed_kinds"]
    out["constructed_widths"] = made["constructed_widths"]
    out["source_path"] = write_source(label, lang, made["source"])
    got, refusal = H.compile_one_place(made["source"], made["symbol"],
                                       lang)
    if got is None:
        out["compiled"] = False
        out["compile_refusal"] = refusal
        return out
    out["compiled"] = True
    raw_bytes, mnem = got
    out["body_bytes"] = " ".join(raw_bytes)
    out["body_text"] = "; ".join(mnem)
    out["instructions"] = len(mnem)
    out["landing"] = H.landing_of(mnem, held["mnem"])
    written = made.get("written_term")
    posed = dict(working)
    if written is not None:
        posed["term"] = written
    check = H.check_one_place(shared, posed, made["params"], raw_bytes,
                              mnem, label, lang,
                              answer_bits=held.get("key_width"),
                              attested=H.attested_of(held, None))
    if written is None or written.get_id() == term.get_id():
        out["check"] = check
        out["equality"] = {"proof": "canonical", "outcome": "PROVED",
                           "reason": ("the render wrote the cell's own "
                                      "term")}
        out["proof"] = "canonical"
        return out
    equality = the_equality(term, written, made["constructed_widths"],
                            word)
    out["equality"] = equality
    out["proof"] = equality.get("proof")
    if equality.get("outcome") != "PROVED":
        out["gate_on_the_written_term"] = check
        out["refusal_cause"] = CAUSE_EQUALITY
        out["refusal_detail"] = "%s: %s" % (equality.get("outcome"),
                                            equality.get("reason"))
        return out
    out["check"] = check
    return out


SRC_DIR = None


def write_source(label, lang, source):
    import handful as H
    if SRC_DIR is None:
        return None
    if not os.path.isdir(SRC_DIR):
        os.makedirs(SRC_DIR)
    name = label + H.suffix_of(lang)
    handle = open(os.path.join(SRC_DIR, name), "w")
    handle.write(source)
    handle.close()
    return os.path.join(os.path.basename(SRC_DIR), name)


# ==================================================================
# section 3: the driver's dispatch, and the pass
# ==================================================================

def find_emulation(shared, held, lang):
    """the driver's run with THIS tier in place of task t2's eight
    schemas: the native route, then the general tier, unconditionally."""
    import handful as H
    record = H.the_native_route(shared, held, lang)
    record["general"] = general_tier(shared, held, lang, record)
    return record


def configure_pass():
    import autopoly as AP
    global SRC_DIR
    runs, src = store_paths()
    SRC_DIR = src
    AP.PASS_LABEL = PASS_LABEL
    AP.HELD = {
        "runs": runs,
        "aggregate": AGGREGATE,
        "src": src,
        "primitive": os.path.join(HERE, "%s_primitive.json" % PASS_LABEL),
        "spellings": os.path.join(HERE, "%s_spellings.json" % PASS_LABEL),
        "report": REPORT,
    }
    AP.RUNS = AP.HELD["runs"]
    AP.AGGREGATE = AP.HELD["aggregate"]
    AP.SRC_DIR = AP.HELD["src"]
    AP.PRIMITIVE = AP.HELD["primitive"]
    AP.SPELLINGS = AP.HELD["spellings"]
    AP.REPORT = AP.HELD["report"]
    if not os.path.isdir(src):
        os.makedirs(src)
    AP.AUDIT_SHARE = 0.0
    AP.ATTEMPTS_ARE_ON = True
    AP.ABORT_NAME = ABORT_NAME
    AP.configure(AP.RUNS, AP.SRC_DIR)
    import handful as H
    H.find_emulation = find_emulation
    return AP


def store_paths():
    """THE STORE LIVES WHERE EVERY PASS'S STORE LIVES, in the autopoly
    folder, for task t2's own reason: `bank.store_path` writes a
    certificate's `produced_by.store` relative to that folder, and a
    store reached with `..` puts an operator token on a structure field,
    which the guard refuses."""
    return (os.path.join(AUTOPOLY, "%s_runs.jsonl" % PASS_LABEL),
            os.path.join(AUTOPOLY, "src_%s" % PASS_LABEL))


def register_with_the_bank():
    import bank as BK
    for step in BK.PASSES:
        if step["pass"] == PASS_LABEL:
            return BK
        continue
    runs, src = store_paths()
    BK.PASSES.append({
        "pass": PASS_LABEL,
        "store": os.path.basename(runs),
        "reader": "compiled",
        "src": src,
        "task": "t4",
        "log": "this task",
        "targets": list(BK.COMPILED),
        "optional": True,
    })
    return BK


def split(record):
    """one finished run as the two runs it is: the native route's, and
    the general tier's where the tier rendered anything."""
    import autopoly5 as LOOP
    made = record.pop("general", None)
    out = [record]
    if made is None:
        return out
    if not made.get("places"):
        return out
    if not made.get("rendered_any_place"):
        return out
    second = {}
    for field in ("mnem", "shape", "key_width", "lang", "row_id",
                  "line", "chosen_by", "attestation", "setter",
                  "code_version", "attested_ledger_rows", "seconds"):
        if field in record:
            second[field] = record[field]
            continue
    second["route"] = "general"
    second["word_bits"] = made["word_bits"]
    second["places"] = trimmed(made["places"])
    second["seconds"] = made.get("seconds")
    second["composition"] = []
    out.append(LOOP.as_machine_form(second))
    return out


def trimmed(places):
    """the places with the two attempts' full sources dropped: the
    CHOSEN attempt's source is already on the place and is written to
    the source folder, and a store line carrying both is the store
    filled with text nobody reads."""
    out = []
    for place in places:
        made = dict(place)
        attempts = made.pop("attempts", None)
        if attempts is not None:
            short = []
            for attempt in attempts:
                row = dict(attempt)
                row.pop("source", None)
                short.append(row)
                continue
            made["attempts"] = short
        out.append(made)
        continue
    return out


def walk(order, runs, done, limit):
    import autopoly as AP
    import gate as G
    import handful as H
    import model_table as MTAB
    shared = H.build_shared()
    reposer = G.Gate(reference=shared["reference"],
                     solver_timeout_ms=AP.REPOSE_MS)
    MTAB._install_gpr_widths()
    in_table = H.load_in_table()
    cells = AP.read_json(AP.CELLS)
    say("the gate of record: %d ms; the one re-pose: %d ms; the "
        "equality's ceiling: %d ms"
        % (shared["gate"].solver_timeout_ms, AP.REPOSE_MS,
           EQUALITY_CEILING_MS))
    say("the construction proofs on record: %d (kind, width, word) rows"
        % len(proof_table()))
    total = len(order)
    index = 0
    ran = 0
    tiers = 0
    declines = {}
    started = time.time()
    for asked, lang, ledger in order:
        index = index + 1
        say("[%d/%d] %s %s %s -> %s (ledger_rows %d)"
            % (index, total, asked[0], asked[1], asked[2], lang,
               ledger))
        for record in AP.one_pair(shared, reposer, cells, asked, lang,
                                  ledger, in_table, done):
            if record is None:
                continue
            tally_the_declines(record, declines)
            for line in split(record):
                AP.append_run(runs, line)
                ran = ran + 1
                if line.get("route") == "general":
                    tiers = tiers + 1
                say("   %s | %s | %s | peak resident: %d kB"
                    % (line.get("route") or "-",
                       AP.setter_label(line),
                       AP.one_line_verdict(line),
                       check_memory("run %d" % index)))
                continue
            continue
        if limit is not None and ran >= limit:
            say("")
            say("the sample's own stop: %d store line(s) written" % ran)
            break
        continue
    seconds = round(time.time() - started)
    say("")
    say("store lines written this lane: %d in %d s" % (ran, seconds))
    say("of them, general-tier runs: %d" % tiers)
    say("lines on %s: %d" % (runs, AP.count_lines(runs)))
    say("")
    say("| where the tier declined, LITERAL | places |")
    say("|---|---|")
    for cause in sorted(declines, key=lambda one: -declines[one]):
        say("| %s | %d |" % (cause.replace("|", "/")[:180],
                             declines[cause]))
        continue
    say("")
    say("peak resident: %d kB" % peak_kb())
    write_declines(declines, ran, tiers, seconds)
    return 0


def tally_the_declines(record, declines):
    made = record.get("general")
    if not made:
        return declines
    for place in made.get("places") or []:
        if place.get("rendered"):
            continue
        cause = place.get("refusal_cause") or "no cause"
        declines[cause] = declines.get(cause, 0) + 1
        continue
    return declines


def write_declines(declines, ran, tiers, seconds):
    document = {
        "meta": {
            "what": "task t4's pass: every (cell, target) the bank "
                    "certifies no proof for, through the native route "
                    "and the general tier under both policies",
            "store_lines": ran,
            "general_tier_runs": tiers,
            "seconds": seconds,
            "memory_bound_kb": ABORT_KB,
            "memory_abort": ABORT_NAME,
            "peak_kb": peak_kb(),
            "equality_ceiling_ms": EQUALITY_CEILING_MS,
            "statement_ceiling": RG.STATEMENT_CEILING,
            "policies": list(POLICIES),
        },
        "declined_by_cause": declines,
    }
    handle = open(AGGREGATE, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    return


# ==================================================================
# section 4: the commands
# ==================================================================

def preflight_command():
    AP = configure_pass()
    plan = AP.the_delta()
    say("the bank: %s" % __import__("bank").BANK)
    say("the outer set: %s" % AP.CELLS)
    say("the targets: %s" % ", ".join(AP.TARGETS))
    say("")
    say("| what | count |")
    say("|---|---|")
    say("| (cell, target, written place, setter) keys the bank "
        "certifies | %d |" % plan["certified_before"])
    say("| keys with no such certificate, which this pass attempts | "
        "%d |" % plan["attempt_triples"])
    say("| of them, held back because the machinery has not moved | %d |"
        % plan["held_by_version"])
    say("| the (cell, target) runs this pass executes | %d |"
        % plan["runs_to_execute"])
    say("")
    say("| target | the word, off its own renderer table |")
    say("|---|---|")
    for lang in AP.TARGETS:
        say("| %s | %d |" % (lang, word_of(lang)))
        continue
    say("")
    say("the construction proofs on record: %d rows" % len(proof_table()))
    say("peak resident: %d kB" % check_memory("preflight"))
    return 0


def run_command(limit):
    AP = configure_pass()
    runs, _src = store_paths()
    plan = AP.the_delta()
    say("keys with no proof: %d over %d run(s)"
        % (plan["attempt_triples"], plan["attempt_pairs"]))
    say("runs to execute: %d" % plan["runs_to_execute"])
    done = AP.already_recorded(runs)
    say("runs already on %s: %d" % (runs, len(done)))
    say("")
    return walk(plan["runs_list"], runs, done, limit)


def bank_command():
    configure_pass()
    BK = register_with_the_bank()
    say("this pass registered with the bank as %r" % PASS_LABEL)
    return BK.main(["build"])


def readings_command():
    configure_pass()
    BK = register_with_the_bank()
    say("this pass registered with the bank as %r" % PASS_LABEL)
    return BK.main(["readings"])


def tier_command(mnem, shape, width, lang):
    """ONE (cell, target) through the native route and the general tier,
    printed.  The walkthrough command; it writes no store line."""
    AP = configure_pass()
    import handful as H
    import model_table as MTAB
    MTAB._install_gpr_widths()
    shared = H.build_shared()
    cells = AP.read_json(AP.CELLS)
    asked = (mnem, shape, int(width))
    say("the word for %s: %d bits" % (lang, word_of(lang)))
    for held in H.cell_inputs(cells, asked):
        record = find_emulation(shared, held, lang)
        made = record.get("general")
        say("")
        say("setter: %s" % AP.setter_label(record))
        say("| route | place | rendered | compiled | gate | statements "
            "| constructed | landing | instructions |")
        say("|---|---|---|---|---|---|---|---|---|")
        for place in record.get("places") or []:
            check = place.get("check") or {}
            say("| native | %s | %s | %s | %s | -- | -- | %s | %d |"
                % (place.get("writes"), place.get("rendered"),
                   place.get("compiled"),
                   check.get("outcome") or place.get("refusal_cause"),
                   (place.get("landing") or {}).get("verdict"),
                   len((place.get("body_text") or "").split(";"))))
            continue
        if made is None:
            say("the general tier: declined for every place")
            continue
        for place in made.get("places") or []:
            for attempt in place.get("attempts") or []:
                check = attempt.get("check") or {}
                gate = attempt.get("gate_on_the_written_term") or {}
                kinds = attempt.get("constructed_kinds") or {}
                say("| %s | %s | %s | %s | %s | %s | %s | %s | %s |"
                    % (attempt.get("policy"), place.get("writes"),
                       attempt.get("rendered"), attempt.get("compiled"),
                       check.get("outcome") or gate.get("outcome")
                       or (attempt.get("refusal_cause") or "")[:70],
                       attempt.get("statements"),
                       ", ".join(sorted(kinds)) or "--",
                       (attempt.get("landing") or {}).get("verdict"),
                       attempt.get("instructions")))
                continue
            continue
        say("")
        say("the carved bodies, LITERAL:")
        for place in made.get("places") or []:
            for attempt in place.get("attempts") or []:
                if attempt.get("body_text") is None:
                    say("   %s / %s: %s"
                        % (place.get("writes"), attempt.get("policy"),
                           (attempt.get("refusal_cause") or "-")[:150]))
                    continue
                say("   %s / %s: %s"
                    % (place.get("writes"), attempt.get("policy"),
                       attempt.get("body_text")))
                equality = attempt.get("equality") or {}
                say("      statements %s; native nodes %s; constructed "
                    "nodes %s; equality %s by %s"
                    % (attempt.get("statements"),
                       attempt.get("native_nodes"),
                       attempt.get("constructed_nodes"),
                       equality.get("outcome"), equality.get("proof")))
                continue
            continue
        continue
    say("")
    say("peak resident: %d kB" % peak_kb())
    return 0


def main(argv):
    if len(argv) < 2:
        say(__doc__)
        return 2
    what = argv[1]
    if what == "preflight":
        return preflight_command()
    if what == "run":
        limit = None
        if len(argv) > 2:
            limit = int(argv[2])
        return run_command(limit)
    if what == "bank":
        return bank_command()
    if what == "readings":
        return readings_command()
    if what == "report":
        import general_report as GRP
        return GRP.main(argv[1:])
    if what == "tier":
        return tier_command(argv[2], argv[3], argv[4], argv[5])
    say("unknown command %r" % what)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
