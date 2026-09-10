#!/usr/bin/env python3
"""construct.py -- THE SECOND TIER: where the native route refuses a
place because the target lacks a primitive at a width or a kind, the
mapping is CONSTRUCTED from the primitives the target does have, and the
constructed mapping is put through the same four steps as any other.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/PROGRESS.md`).
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_t2_brief.md`.

THE OBJECTS, one sentence each, in relation.
  * THE NATIVE ROUTE is `handful.the_native_route`, which is the driver
    exactly as task ap6 left it: the primitive route, else the term
    route, then compile, carve and gate.
  * THE SECOND TIER is `second_tier` below, called by the driver ONCE,
    unconditionally, on every run: it looks at each place the native
    route did not prove, lowers that place's term to the target's own
    word with `schemas.py`, and puts the LOWERED term through the same
    render, compile, carve and gate.
  * THE WORD is the widest integer holder the target has, read off that
    target's own renderer table.  It is 128 on c, cpp and rust and 64 on
    go and swift -- measured, in lane `t2_l1`, not recalled.
  * TWO OBLIGATIONS, not one.  The GATE answers whether the carved body
    equals the CONSTRUCTED mapping; the EQUALITY answers whether the
    constructed mapping equals the CELL's own.  A place whose gate says
    proved and whose equality is not discharged is NOT a proof about the
    cell, and this file refuses it by cause rather than banking it.
  * THE EQUALITY IS TRIED IN THE BRIEF'S ORDER: the canonical form
    (`term.Term.normalize` on both sides, identical text and no solver),
    then the schema's own lemma at that width (Lean, `construct/lean/`),
    then z3 at a HARD 30-second ceiling, never above it.
  * A RUN IS ONE ROUTE.  The tier's places are written to the store as a
    SECOND run of the same (cell, target, setter) carrying
    `route = constructed`, so the bank keys them exactly as it keys the
    native ones and its own preference rule keeps whichever proves.

WHY THE TIER RUNS ON A PLACE THE NATIVE ROUTE MERELY FAILED TO PROVE,
and not only on one it refused: the rule is a property of the TERM and
not of the outcome.  Where no node of the place's term is wider than the
target's word, `schemas.lower` gives the term back unchanged and the
tier declines by cause; where one is, there is something to construct
whatever the native route's verdict was.  So the call site is
unconditional and the decision is machine form.

MEMORY: this file forks nothing and holds no store; the caller states
the bound and the named abort, and the pass below checks the peak after
every run.

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

HOW THIS FILE OBEYS IT.  Whether the tier acts is decided by widths and
z3 declaration kinds; which places it acts on is decided by the bank's
own keys; a cell is addressed by the triple (`mnem`, operand shape,
`key_width`) and the mnemonic sits in the field `mnem`, which the
ruling of 2026-09-08 states is machine form.

usage:
  construct.py preflight       what the pass would attempt, nothing run
  construct.py run [<n>]       the pass; `<n>` stops after n runs
  construct.py bank            the bank rebuilt with this pass in it
  construct.py readings        the three readings, with this pass in them
  construct.py report          `construct.md`
  construct.py tier <mnem> <shape> <width> <lang>
                               one (cell, target) through both routes,
                               printed -- the walkthrough command

Coding discipline: no compound one-liner statements.
"""

import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
EMULATION = os.path.normpath(os.path.join(HERE, ".."))
HANDFUL = os.path.join(EMULATION, "handful")
AUTOPOLY = os.path.join(EMULATION, "autopoly")
sys.path.insert(0, HERE)
sys.path.insert(0, HANDFUL)
sys.path.insert(0, AUTOPOLY)
# THE RENDERERS' OWN FOLDERS, so `word_of` answers in a process that has
# not imported the driver: the word is read off each target's own
# renderer table, and a reader reproducing that one number should not
# have to build the whole driver to get it.
sys.path.insert(0, EMULATION)
sys.path.insert(0, os.path.join(EMULATION, "rust"))
sys.path.insert(0, os.path.join(EMULATION, "go"))
sys.path.insert(0, os.path.join(EMULATION, "swift"))

import z3                                                        # noqa: E402
import schemas as S                                              # noqa: E402

PASS_LABEL = "t2_construct"
"""this pass's label, from which its store, its aggregate and its source
folder are derived mechanically by `autopoly.paths_of` -- the same rule
every pass since task ap1 has used."""

LEMMAS = os.path.join(HERE, "lean", "lemmas_t2.json")
REPORT = os.path.join(HERE, "construct.md")
AGGREGATE = os.path.join(HERE, "construct.json")

ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_T2"

EQUALITY_CEILING_MS = 30000
"""the brief's HARD ceiling on the last resort, and it is never raised:
z3 is the audit here and not the workhorse."""

UNFOLDED_CEILING = 200000
"""how large a constructed term may be, counted the way the RENDERER
writes it.

THE RENDERER EMITS ONE NESTED EXPRESSION AND NAMES NO INTERMEDIATE
(`emulate.Renderer.render` ends `return <expr>;`), so a sub-term read
twice is written twice.  A schema whose step reads its own previous step
three times therefore renders to a source that grows like 3^width, and
the divider is exactly that shape.  The tier refuses on the MEASURED
size rather than on a rule about which operation it is; the measurement
is in lane `t2_l5` section [4/4]."""

CAUSE_NOTHING_ABOVE_THE_WORD = (
    "no node of this place's term is wider than the target's widest "
    "holder, so the native rendering already spells it and there is "
    "nothing to construct")
CAUSE_ALREADY_PROVED = (
    "the native route proved this place, so there is nothing the second "
    "tier can add")
CAUSE_NOT_RENDERED_UPSTREAM = (
    "the native route did not reach this place's term at all, so the "
    "tier has nothing to lower")
CAUSE_TOO_LARGE = (
    "the constructed term is larger than the renderer can write: the "
    "renderer emits one nested expression and names no intermediate, so "
    "a term whose steps read their own previous step more than once is "
    "written out once per read")
CAUSE_STILL_WIDE = (
    "the pipeline's own normaliser left a node wider than the target's "
    "widest holder in the constructed term, so the tier refuses its own "
    "output")
CAUSE_EQUALITY = (
    "the carved body is proved equal to the CONSTRUCTED mapping, and the "
    "constructed mapping's equality with the CELL's own is not "
    "discharged by any of the three forms")


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


# ==================================================================
# section 1: THE WORD -- read off the target's own renderer table
# ==================================================================

WORD_CACHE = {}


def word_of(lang):
    """the widest integer holder the target has, off that target's own
    renderer table.  MEASURED and never recalled: the brief's
    parenthesis says 64 everywhere, and c, cpp and rust in fact spell a
    128-bit integer holder, which lane `t2_l1` section [4/5] prints."""
    if lang in WORD_CACHE:
        return WORD_CACHE[lang]
    import emulate as E
    table = E.UNSIGNED
    if lang == "rust":
        import rust_render as RR
        table = RR.RU
    elif lang == "go":
        import go_render as GR
        table = GR.GU
    elif lang == "swift":
        import swift_render as SR
        table = SR.SU
    answer = max(table)
    WORD_CACHE[lang] = answer
    return answer


# ==================================================================
# section 2: THE EQUALITY -- the three forms, in the brief's order
# ==================================================================

LEMMA_CACHE = None


def lemma_table():
    """{(schema, width, word): the row} off `construct/lean/lemmas_t2.json`,
    which `construct/lean/run_lemmas_t2.py` writes: one Lean theorem per
    schema per width, each discharged by its own `lean` process."""
    global LEMMA_CACHE
    if LEMMA_CACHE is not None:
        return LEMMA_CACHE
    LEMMA_CACHE = {}
    if not os.path.exists(LEMMAS):
        return LEMMA_CACHE
    handle = open(LEMMAS)
    document = json.load(handle)
    handle.close()
    for row in document.get("rows") or []:
        # THE KEY IS (schema, word, SHAPE) and carries no separate
        # width, because the shape key already carries every width the
        # rewrite has -- and the two sides disagreed about which width
        # to name.  The tier files an extension under the width it
        # produces (65) and the lemma files it under the width it reads
        # (64), so a key carrying one of them missed every extension.
        # Measured, lane `t2_l22`: `extend_zero_w64_t65`, held by the
        # lemma table and reported missing by the tier.
        key = (row["schema"], row["word"], row["shape"])
        LEMMA_CACHE[key] = row
        continue
    return LEMMA_CACHE


def the_equality(cell_term, built_term, instances, word):
    """whether the CONSTRUCTED mapping is the cell's own mapping, in the
    three forms the brief names, in the brief's order.

    1. THE CANONICAL FORM.  Both terms through `term.Term.normalize`,
       which is the pipeline's own fixed print rule; identical text is
       the same mapping and no solver is asked.  This is the study of
       the mappings the brief asks for, and where it fires it is the
       cheapest and the strongest of the three.
    2. THE SCHEMA'S LEMMA.  The lowering replaces each node by the term
       its schema builds, so if every (schema, width) instance the
       lowering used carries a Lean theorem saying those two are equal,
       the whole is equal by structural induction on the term -- which
       is log_221 section 7's "proof by structure", and it is linear.
    3. Z3, at a hard 30-second ceiling, as the last resort.

    A wide multiply or divide is never posed to form 3 alone in the
    hope it lands: it is posed, it answers or it does not, and what it
    answered is recorded either way."""
    import handful as H
    import term as T
    out = {"forms": []}
    started = time.time()
    holder = T.Term()
    # BOTH SIDES THROUGH THE PIPELINE'S OWN NORMALISER FIRST, and it is
    # not cosmetic: `the_normalised_term` is the rule the model table
    # PRINTS by and the rule the renderer walks, it renames the free
    # symbols positionally and then undoes the renaming, so the symbols
    # are the terms' own -- and posing the raw terms instead leaves the
    # solver a miter of two unsimplified circuits.  Measured, lane
    # `t2_l7` against lane `t2_l9`: the same obligation.
    cell_posed = H.the_normalised_term(cell_term)
    built_posed = H.the_normalised_term(built_term)
    cell_text = holder.normalize(cell_posed)
    built_text = holder.normalize(built_posed)
    out["cell_normalized"] = cell_text
    out["constructed_normalized"] = built_text
    out["forms"].append({"form": "canonical",
                         "answer": cell_text == built_text})
    if cell_text == built_text:
        out["proof"] = "canonical"
        out["outcome"] = "PROVED"
        out["reason"] = ("the cell's mapping and the constructed mapping "
                         "print the same text under the pipeline's own "
                         "normaliser, so they are the same mapping")
        out["seconds"] = round(time.time() - started, 3)
        return out
    table = lemma_table()
    missing = []
    held = []
    for row in instances:
        for shape in row["shapes"]:
            key = (row["schema"], row["word"], S.shape_key(shape))
            entry = {"schema": row["schema"], "width": row["width"],
                     "word": row["word"], "shape": S.shape_key(shape)}
            if shape["operation"] == "constant":
                # A NUMERAL IS NOT AN OPERATION.  Its limbs are its own
                # digits in the word's base (`schemas.constant_limbs` is
                # a shift and a mask on a python integer), so there is
                # no rewrite of an operation to state a lemma about.
                # This is the one step of the lowering that carries no
                # theorem and it is named here rather than passed over.
                entry["theorem"] = "none: a numeral's limbs are its own"
                held.append(entry)
                continue
            found = table.get(key)
            if found is None:
                entry["why"] = "no lemma is stated for this shape"
                missing.append(entry)
                continue
            if found.get("outcome") != "PROVED_BY_LEAN":
                entry["why"] = ("the lemma for this shape is %s"
                                % found.get("outcome"))
                missing.append(entry)
                continue
            entry["theorem"] = found.get("theorem_name")
            held.append(entry)
            continue
        continue
    out["forms"].append({"form": "lemma+gate",
                         "answer": not missing and bool(held),
                         "lemmas_held": held,
                         "lemmas_missing": missing})
    if held and not missing:
        out["proof"] = "lemma+gate"
        out["outcome"] = "PROVED"
        out["reason"] = ("every SHAPE the lowering rewrote carries a "
                         "Lean theorem, one per limb, saying the "
                         "schema's term equals the operation it "
                         "replaced at that limb; the lowering is one "
                         "such replacement per node, so the two terms "
                         "are equal by structural induction on the "
                         "term")
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
                         "and the constructed mapping differ")
        return out
    out["proof"] = None
    if answer == z3.sat:
        out["outcome"] = "DISPROVED"
        out["reason"] = ("z3 found an input at which the cell's mapping "
                         "and the constructed mapping differ")
        out["counterexample"] = str(solver.model())[:400]
        return out
    out["outcome"] = "UNDECIDED"
    out["reason"] = ("z3 answered neither way inside the brief's hard "
                     "30-second ceiling; the ceiling is not raised, "
                     "because it is the brief's own")
    return out


# ==================================================================
# section 3: THE TIER -- the driver's one call
# ==================================================================

def second_tier(shared, held, lang, record):
    """the driver's ONE unconditional call: every place of this run
    looked at once, and a SECOND run's worth of places where the tier
    has something to construct.

    Returns None where the tier constructed nothing for any place, so a
    caller that knows nothing about it is unaffected."""
    word = word_of(lang)
    if word is None:
        return None
    inputs = held.get("places")
    if not inputs:
        return None
    natives = record.get("places") or []
    out = []
    built_any = False
    started = time.time()
    for index, place in enumerate(inputs):
        native = None
        if index < len(natives):
            native = natives[index]
        made = one_constructed_place(shared, held, lang, place, native,
                                     word, index)
        out.append(made)
        if made.get("check") is not None:
            built_any = True
        continue
    return {
        "route": "constructed",
        "word_bits": word,
        "places": out,
        "reached_the_gate": built_any,
        "lowered_any_place": any_lowered(out),
        "seconds": round(time.time() - started, 3),
    }


def any_lowered(places):
    """whether the tier CONSTRUCTED anything at all for this run.

    A run where every place declined is not a second route: it is the
    native route and a sentence saying there was nothing above the
    target's widest holder.  `split` writes no second store line for
    one, so the bank is not filled with refusals about a route that was
    never taken -- the same reasoning task ap6 gave for the 2,290 setter
    cells it counted once by cause instead of banking per target."""
    for place in places:
        block = place.get("constructed") or {}
        if block.get("schemas"):
            return True
        continue
    return False


def one_constructed_place(shared, held, lang, place, native, word,
                          index):
    """one written place through the second tier: lower, render,
    compile, carve, gate against the CONSTRUCTED mapping, and discharge
    the equality with the cell's own."""
    import handful as H
    import emulate as E
    out = {
        "writes": place["writes"],
        "text": place.get("text"),
        "sexpr": place.get("sexpr"),
        "bits": place.get("bits"),
        "families": place.get("families"),
        "home": place.get("home"),
        "constructed": {"word_bits": word},
    }
    if place.get("halved") is not None:
        out["halved"] = place["halved"]
    if native is not None:
        check = native.get("check") or {}
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
    term = working.get("term")
    if term is None:
        out["rendered"] = False
        out["refusal_cause"] = CAUSE_NOT_RENDERED_UPSTREAM
        out["refusal_detail"] = "the place carries no term"
        return out
    try:
        built, schemas_used, instances = S.lower(term, word)
    except S.Refused as refusal:
        out["rendered"] = False
        out["refusal_cause"] = refusal.cause
        out["refusal_detail"] = refusal.detail
        return out
    out["constructed"]["schemas"] = schemas_used
    out["constructed"]["instances"] = instances
    if not schemas_used:
        out["rendered"] = False
        out["refusal_cause"] = CAUSE_NOTHING_ABOVE_THE_WORD
        return out
    # THE SIZE IS MEASURED ON THE RAW LOWERED TERM FIRST, before the
    # normaliser is asked anything at all.  `z3.simplify` on a term
    # whose steps each read their own previous step three times is
    # itself the thing that runs away -- the divider at 128 bits took
    # the operating system's memory ceiling out from under lane `t2_l7`
    # -- so the guard runs before it and not after.
    raw_size = S.unfolded_size(built, UNFOLDED_CEILING)
    out["constructed"]["unfolded_ceiling"] = UNFOLDED_CEILING
    if raw_size >= UNFOLDED_CEILING:
        out["rendered"] = False
        out["refusal_cause"] = CAUSE_TOO_LARGE
        out["refusal_detail"] = ("at or above %d nodes written out, "
                                 "before the normaliser was asked"
                                 % UNFOLDED_CEILING)
        out["constructed"]["unfolded_nodes"] = raw_size
        return out
    # THE TIER REFUSES ITS OWN OUTPUT on two mechanical guards, the way
    # every stage of this line is required to: the term the RENDERER
    # will walk is the normalised one, so both guards read that too.
    walked = H.renderer_input(built)
    widest = S.widest_node(walked)
    unfolded = S.unfolded_size(walked, UNFOLDED_CEILING)
    out["constructed"]["widest_node_bits"] = widest
    out["constructed"]["unfolded_nodes"] = unfolded
    if widest > word:
        out["rendered"] = False
        out["refusal_cause"] = CAUSE_STILL_WIDE
        out["refusal_detail"] = "%d bits" % widest
        return out
    if unfolded >= UNFOLDED_CEILING:
        out["rendered"] = False
        out["refusal_cause"] = CAUSE_TOO_LARGE
        out["refusal_detail"] = ("at or above %d nodes written out"
                                 % UNFOLDED_CEILING)
        return out
    made = dict(working)
    made["term"] = built
    label = E.sanitize("%s_%s_%d__%s__%s__constructed"
                       % (held["mnem"], held["shape"], held["key_width"],
                          place["writes"].replace(".", "_"), lang))
    out["label"] = label
    rendered = H.render_one_place(made, lang, label)
    renderer = rendered.pop("renderer", None)
    out.update(rendered)
    if renderer is None:
        return out
    got, refusal = H.compile_one_place(rendered["source"],
                                       rendered["symbol"], lang)
    if got is None:
        out["compiled"] = False
        out["compile_refusal"] = refusal
        return out
    out["compiled"] = True
    raw_bytes, mnem = got
    out["body_bytes"] = " ".join(raw_bytes)
    out["body_text"] = "; ".join(mnem)
    out["landing"] = H.landing_of(mnem, held["mnem"])
    out["constructed"]["instructions"] = len(mnem)
    check = H.check_one_place(shared, made, renderer.params, raw_bytes,
                              mnem, label, lang,
                              answer_bits=held.get("key_width"),
                              attested=H.attested_of(held, None))
    equality = the_equality(term, built, instances, word)
    out["constructed"]["equality"] = equality
    out["constructed"]["proof"] = equality.get("proof")
    if equality.get("outcome") != "PROVED":
        # THE GATE'S ANSWER IS ABOUT THE CONSTRUCTED MAPPING and the
        # equality is what carries it back to the cell.  Without the
        # equality a `proved` here would be a proof about a term this
        # tier invented, so the place is refused BY CAUSE and the gate's
        # own answer is kept beside the refusal rather than banked as a
        # verdict about the cell.
        out["gate_on_the_constructed_mapping"] = check
        out["refusal_cause"] = CAUSE_EQUALITY
        out["refusal_detail"] = "%s: %s" % (equality.get("outcome"),
                                            equality.get("reason"))
        return out
    out["check"] = check
    return out


# ==================================================================
# section 4: THE PASS
# ==================================================================

def configure_pass():
    """this pass's own products, by the label, and the driver pointed at
    them -- `autopoly.configure`'s own rule, called rather than
    restated."""
    import autopoly as AP
    runs, src = store_paths()
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
    return AP


def register_with_the_bank():
    """this pass added to the bank's own pass table, from OUTSIDE the
    bank's source file.

    `bank.PASSES` is data -- one row per pass, with its store, its
    reader and its targets -- and `autopoly.configure` already sets the
    driver's paths from outside the driver by exactly this means.  A
    pass that is not in that table is a pass whose proofs no reading of
    the bank can see, and editing the table's FILE is a change to a
    shared file this task's brief does not name."""
    import bank as BK
    for step in BK.PASSES:
        if step["pass"] == PASS_LABEL:
            return BK
    runs, src = store_paths()
    BK.PASSES.append({
        "pass": PASS_LABEL,
        "store": os.path.basename(runs),
        "reader": "compiled",
        "src": src,
        "task": "t2",
        "log": "this task",
        "targets": list(BK.COMPILED),
        "optional": True,
    })
    return BK


def store_paths():
    """THE STORE LIVES WHERE EVERY PASS'S STORE LIVES, in the autopoly
    folder, and the reason is the spelling guard.

    `bank.store_path` writes a certificate's `produced_by.store` as
    `Research/.../autopoly/<the store's name>`, so a store named with a
    `..` to reach out of that folder puts `..` on a structure field --
    and `..` is an operator token (a range in swift and in ruby), which
    the guard refuses.  Measured, lane `t2_l26`: 5,303 certificates
    refused on exactly that.  The CODE of this task lives under
    `construct/`; its store lives beside the other passes' stores, which
    is also what makes `bank.py backups` able to see it."""
    return (os.path.join(AUTOPOLY, "%s_runs.jsonl" % PASS_LABEL),
            os.path.join(AUTOPOLY, "src_%s" % PASS_LABEL))


def split(record):
    """one finished run as the TWO runs it is: the native route's, and
    the second tier's where the tier built anything.

    The second is a run of its own on the store, so the bank keys it the
    way it keys every other run and its own preference rule keeps
    whichever of the two proves."""
    import autopoly5 as LOOP
    made = record.pop("constructed", None)
    out = [record]
    if made is None:
        return out
    if not made.get("places"):
        return out
    if not made.get("lowered_any_place"):
        return out
    second = {}
    for field in ("mnem", "shape", "key_width", "lang", "row_id",
                  "line", "chosen_by", "attestation", "setter",
                  "code_version", "attested_ledger_rows", "seconds"):
        if field in record:
            second[field] = record[field]
            continue
    second["route"] = "constructed"
    second["word_bits"] = made["word_bits"]
    second["places"] = made["places"]
    second["seconds"] = made.get("seconds")
    second["composition"] = []
    out.append(LOOP.as_machine_form(second))
    return out


def walk(order, runs, done, limit):
    """this pass's own loop: every (cell, target) the bank certifies no
    proof for, put through BOTH routes, one store line each."""
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
    say("the table's own TRANSLATED triples: %d" % len(in_table))
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
                if line.get("route") == "constructed":
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
    say("of them, second-tier runs: %d" % tiers)
    say("lines on %s: %d" % (runs, AP.count_lines(runs)))
    say("")
    say("| where the tier declined, LITERAL | places |")
    say("|---|---|")
    for cause in sorted(declines, key=lambda c: -declines[c]):
        say("| %s | %d |" % (cause.replace("|", "/"), declines[cause]))
        continue
    say("")
    say("peak resident: %d kB" % peak_kb())
    write_declines(declines, ran, tiers, seconds)
    return 0


def tally_the_declines(record, declines):
    """every place the tier looked at and left alone, by cause, counted
    ONCE over the pass instead of banked as a run per target."""
    made = record.get("constructed")
    if not made:
        return declines
    for place in made.get("places") or []:
        block = place.get("constructed") or {}
        if block.get("schemas"):
            continue
        cause = place.get("refusal_cause") or "no cause"
        declines[cause] = declines.get(cause, 0) + 1
        continue
    return declines


def write_declines(declines, ran, tiers, seconds):
    """the pass's own aggregate, beside the store."""
    document = {
        "meta": {
            "what": "task t2's pass: every (cell, target) the bank "
                    "certifies no proof for, through both routes",
            "store_lines": ran,
            "second_tier_runs": tiers,
            "seconds": seconds,
            "memory_bound_kb": ABORT_KB,
            "memory_abort": ABORT_NAME,
            "peak_kb": peak_kb(),
            "equality_ceiling_ms": EQUALITY_CEILING_MS,
            "unfolded_ceiling": UNFOLDED_CEILING,
        },
        "declined_by_cause": declines,
    }
    handle = open(AGGREGATE, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    return


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
    say("peak resident: %d kB" % check_memory("preflight"))
    return 0


def run_command(limit):
    AP = configure_pass()
    runs, src = store_paths()
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
    """the three readings WITH this pass registered.

    `bank.py readings` run on its own reads the twelve passes its own
    file names and this one is not among them, so the reading it prints
    is the reading before this pass; the registration has to be in the
    same process as the reading."""
    configure_pass()
    BK = register_with_the_bank()
    say("this pass registered with the bank as %r" % PASS_LABEL)
    return BK.main(["readings"])


def tier_command(mnem, shape, width, lang):
    """ONE (cell, target) through both routes, printed.  This is the
    walkthrough command: it writes nothing to any store."""
    AP = configure_pass()
    import handful as H
    import model_table as MTAB
    MTAB._install_gpr_widths()
    shared = H.build_shared()
    cells = AP.read_json(AP.CELLS)
    asked = (mnem, shape, int(width))
    say("the word for %s: %d bits" % (lang, word_of(lang)))
    for held in H.cell_inputs(cells, asked):
        record = H.find_emulation(shared, held, lang)
        made = record.get("constructed")
        say("")
        say("setter: %s" % AP.setter_label(record))
        say("| route | place | rendered | compiled | gate | equality | "
            "schemas | landing | instructions |")
        say("|---|---|---|---|---|---|---|---|---|")
        for place in record.get("places") or []:
            check = place.get("check") or {}
            say("| %s | %s | %s | %s | %s | -- | -- | %s | %s |"
                % (record.get("route"), place.get("writes"),
                   place.get("rendered"), place.get("compiled"),
                   check.get("outcome") or place.get("refusal_cause"),
                   (place.get("landing") or {}).get("verdict"),
                   len((place.get("body_text") or "").split(";"))))
            continue
        if made is None:
            say("the second tier: declined for every place")
            continue
        for place in made.get("places") or []:
            check = place.get("check") or {}
            gate = place.get("gate_on_the_constructed_mapping") or {}
            block = place.get("constructed") or {}
            equality = block.get("equality") or {}
            say("| constructed | %s | %s | %s | %s | %s | %s | %s | %s |"
                % (place.get("writes"), place.get("rendered"),
                   place.get("compiled"),
                   check.get("outcome") or gate.get("outcome")
                   or (place.get("refusal_cause") or "")[:60],
                   "%s/%s in %s s" % (equality.get("outcome"),
                                      equality.get("proof"),
                                      equality.get("seconds")),
                   ", ".join(block.get("schemas") or []),
                   (place.get("landing") or {}).get("verdict"),
                   block.get("instructions")))
            continue
        say("")
        say("the constructed bodies, LITERAL:")
        for place in made.get("places") or []:
            if place.get("body_text") is None:
                say("   %s: %s"
                    % (place.get("writes"),
                       (place.get("refusal_cause") or "-")))
                continue
            block = place.get("constructed") or {}
            say("   %s: %s" % (place.get("writes"),
                               place.get("body_text")))
            say("      the constructed term, %d nodes written out, "
                "widest node %s bits"
                % (block.get("unfolded_nodes") or -1,
                   block.get("widest_node_bits")))
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
        import construct_report as CR
        return CR.main(argv[1:])
    if what == "tier":
        return tier_command(argv[2], argv[3], argv[4], argv[5])
    say("unknown command %r" % what)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
