#!/usr/bin/env python3
"""handful.py -- THE DRIVER: one (cell, target) put through the four
steps, with every contract rule unconditional and the code that decided
it recorded on the answer.

Node: hq.research.arch_unit_oracle
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`,
the "goal" section of 2026-09-07 and the ruling of 2026-09-08).

WHAT CHANGED ON 2026-09-10, one sentence: the nine `use_task_*` gates
are gone and every rule below applies to every run, because a rule that
is switched on by the NAME of the task asking is provenance done in the
worst way -- what a reader needs is whether the machinery that produced
an answer is the machinery running now, and that is `code_version`, the
sha256 of this file and of the target's renderer, carried on every run
and on every certificate the bank writes from it.

THE OBJECTS, one sentence each, in relation.
  * A CELL is one (`mnem`, operand shape, `key_width`) row of the
    arch-opcode model table
    (`Research/oracle/arch_opcodes/model/model_table.json`, tasks
    m1/m1b), which holds, per place the opcode writes, the z3 term the
    reference simulator's own builder puts there.
  * A WRITTEN PLACE is one destination that opcode writes (`reg_rdi`,
    `flags`, `reg_xmm0.low`, `x87_7`); the gate answers PER PLACE.
  * A RUN is `find_emulation(cell, lang)`: the emulation rendered,
    compiled at the corpus's ship flags, carved, and put back to z3
    against the cell's own term, place by place.
  * THE CHECK has no unit behind it.  Task o8 ran this on SINGLETON
    UNITS and could gate the emulation against the unit's own body; a
    cell of the table is a mapping and nothing else, so the comparison
    is the cell's term against the term of the body the compiler
    emitted.
  * THE CODE VERSION is the sha256 of this file and of the renderer
    that wrote the target's source.  It is what a later pass asks
    before it re-attempts anything.

THE ROUTE, in the order it is asked, and NOT ONE STEP OF IT IS KEYED ON
WHO IS ASKING.
  1. THE IMMEDIATE IS AN INPUT (log 249).  Where the cell's chosen row
     carries a symbolic immediate, there is no primitive: the lookup's
     key is the cell's own triple and carries no immediate, so a body
     it matched would carry a baked-in immediate of its own.  The route
     is the term route and the gate quantifies over the immediate.
  2. THE PRIMITIVE ROUTE (log 241, widened in log 242): does the target
     have an OPERATOR whose whole lowered body IS this cell, possibly
     with zero-operand setup instructions from the reference's own
     `SPREAD_SIGN` / `ACCUMULATOR_WIDEN` tables beside it and nothing
     else?  Where it has, the chosen member's OWN probe source is
     rendered, its symbol renamed and nothing else changed.
  3. THE TERM ROUTE otherwise: the term the pipeline's own normaliser
     leaves is handed to the existing renderer, which writes it in the
     target's own operators (log 240's fix 1, unconditional since log
     244).
  4. COMPILE at the corpus's own ship flags, CARVE with `lane_gen.
     DRIVER`'s objdump reader, and put the carved body back to z3
     against the cell's term, inputs aligned by IN row.

THE CONTRACT RULES, each one unconditional, each with the reading it
came from.  They are the rules the nine gates used to switch on.
  * A VECTOR CELL'S PLACE IS A LANE (log 240's fix 2): the lane the
    operation writes is projected out of the 128-bit place and rendered,
    and what the bits above it hold is put to the gate as well.
  * A 128-BIT PLACE IS TWO 64-BIT PLACES (log 244): a whole-register
    place with no narrower lane is split into its two halves, and a
    HALF is not a lane -- `projected_lane` is not asked about one.
  * A MEMORY OPERAND IS AN ARRIVING VALUE, and so is a value on the
    x87 register stack (logs 244, 246, 249).
  * A FLAG CONSUMER'S SETTER IS IN THE ATTESTATION (log 244): a
    flag-reading cell's mapping is a function of the flags a setter
    wrote, so the pair is rendered as ONE function -- the comparison,
    then the select -- and no flag state crosses the call.
  * A PRESEEDED ROW THAT READS NO FLAG STATE IS NOT A FLAG CONSUMER
    (log 245).
  * AN ARRIVAL THAT IS A FUNCTION OF ANOTHER ARRIVAL IS ONE, AN EMPTY
    BODY IS THE IDENTITY ON ITS ARRIVAL, AND A HALF OF THE FLAGS PLACE
    IS THE FLAGS PLACE (log 246).
  * A NARROW ARGUMENT IS RE-POSED under the target's own caller
    extension, and the re-pose is recorded BESIDE the verdict, never in
    place of it (task o7's precedent).

WHAT IS REUSED RATHER THAN COPIED, said out loud.
  `model_table.places_of_attempt` rebuilds a row's z3 terms by
  re-running the row's own line on the reference -- the same call the
  m1b edges pass makes.  `emulate.Renderer` writes c,
  `rust_render.RustRenderer` rust, `go_render.GoRenderer` go,
  `swift_render.SwiftRenderer` swift and `cpp_render.CppRenderer` cpp,
  all unchanged; their refusal causes are theirs.  `emulate.
  compile_and_carve` and each renderer's own compile at that corpus's
  ship flags.  `single_opcode_units.strip_chaff` / `parse_insn` are
  task o2's own narrow chaff rule.  `canonical_form.render_one` wraps,
  `reference.answer_for_unit` answers, `pool100_entry_equivalence`
  aligns the two sides by IN row, and `gate.Gate.decide` is the one
  solver call.  Nothing under `Research/op_pipeline/` or
  `Research/oracle/arch_opcodes/` is edited.

  ONE THING IS RESTATED RATHER THAN CALLED, and here is why.
  `emulate.prove_against_x` is the o7/o8/o11 proof step, and it takes
  an X UNIT -- a canon40 record whose body is the other side of the
  comparison.  This driver's other side is a table cell, which has no
  body and no record, so that function cannot be handed the arguments
  it names.  `check_one_place` below poses the same obligation through
  the same objects (`pool100_entry_equivalence.input_rows` /
  `align_by_row` / `classify_symbols` / `rename_constants_apart`, then
  `gate.Gate.decide`).

THE COMPOSITION COLUMN (log 239).  A carved body is a sequence of arch
opcodes, each a cell of the model table, so the body's term is a
composition of table cells: `composition_of_run` walks the destination
place's RAW carved body in body order and classifies each instruction
by the SAME functions task m1b used -- `model_table.operand_class` /
`model_table.SHAPE_OF_CLASSES` inside `model_table.classify_line`,
imported and never re-implemented -- against the triples that are
TRANSLATED rows of the table.  Three outcomes per instruction, each
named, never merged: a TABLE CELL; CHAFF (`ret` or a
calling-convention move, task o2's own `single_opcode_units.is_chaff`
under its narrow rule); or an instruction that maps to no table cell,
named with its own line and the classifier's own cause.

THIS FILE IS A LIBRARY.  The loop's own entry is `autopoly.py --bank
<command>`.  The commands the closed tasks' logs cite -- `report2`,
`run3`, `report3b`, `changes3c`, `whynot3c`, `bodies3c`, `rechecked3b`,
`reclassify`, `sources_counts` and the rest -- are those tasks' own
report commands over those tasks' own products, and they are answered
by `handful_frozen.py`, which is this file copied byte for byte on
2026-09-10 before the gates were stripped: `python3 handful_frozen.py
<command>` reproduces a closed log's output exactly.

MEMORY BOUND, stated as the law requires: one collecting process, no
forked workers (each run is one compile and one gate call per written
place), peak resident checked after every run, named abort in
`ABORT_NAME` at `ABORT_KB`, both of which the caller states.  This
program never reads the 73 MB `model_table.json`: it reads the cells
file its caller points `CELLS` at.

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

HOW THIS FILE OBEYS IT.  A cell is addressed by the triple (`mnem`,
operand shape, `key_width`), which the ruling of 2026-09-08 states is
machine form, and every field carrying a mnemonic is named `mnem`,
which the guard reads as machine form.  Nothing here groups, pairs or
selects by a token: the population is the outer set the caller hands
in, in the order the corpus's own attested ledger rows give.

Coding discipline: no compound one-liner statements.
"""

import json
import os
import re
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EMULATION = os.path.normpath(os.path.join(HERE, ".."))
RUST = os.path.join(EMULATION, "rust")
CROSS = os.path.normpath(os.path.join(HERE, "..", ".."))
OP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                  "op_pipeline"))
LEAN = os.path.join(OP, "lean")
ARCH_OPCODES = os.path.normpath(os.path.join(HERE, "..", "..", "..",
                                             "arch_opcodes"))
MODEL = os.path.join(ARCH_OPCODES, "model")
sys.path.insert(0, OP)
sys.path.insert(0, LEAN)
sys.path.insert(0, CROSS)
sys.path.insert(0, EMULATION)
sys.path.insert(0, RUST)
sys.path.insert(0, ARCH_OPCODES)
sys.path.insert(0, MODEL)

GO = os.path.join(EMULATION, "go")
SWIFT = os.path.join(EMULATION, "swift")
CPP = os.path.join(EMULATION, "cpp")
sys.path.insert(0, GO)
sys.path.insert(0, SWIFT)
sys.path.insert(0, CPP)

import z3                                                        # noqa: E402
import canon                                                     # noqa: E402
import reference as R                                            # noqa: E402
import term as T                                                 # noqa: E402
import emulate as E                                              # noqa: E402
import rust_render as RR                                         # noqa: E402
import go_render as GR                                           # noqa: E402
import swift_render as SR                                        # noqa: E402
import cpp_render as CPR                                          # noqa: E402
import model_table as MTAB                                       # noqa: E402
import model_translate as MT                                     # noqa: E402
import single_opcode_units as SOU                                # noqa: E402

GENERAL_FAMILIES = frozenset(canon.FAMILY_OF.values()) - R.XMM_NAMES

CELLS = os.path.join(HERE, "handful_cells.json")
"""THE CONFIGURATION, and every one of these is a PATH, not a rule.  A
caller repoints them at its own products before it runs (`autopoly.py`
does, in one function); nothing about what the driver decides moves
with them."""
RESULTS = os.path.join(HERE, "handful_driver.json")
REPORT = os.path.join(HERE, "handful_driver.md")
SRC_DIR = os.path.join(HERE, "src_driver")
PRIMITIVE = os.path.join(HERE, "handful_driver_primitive.json")
SPELLINGS = os.path.join(HERE, "handful_driver_spellings.json")
HOST_FOLDER = ("PseudoCoupHQ/Research/oracle/"
               "cross_construction/emulation/handful")

TARGETS = ["c", "cpp", "rust", "go", "swift"]
"""the compiled targets, in the order the briefs name them.  A list a
caller may repoint, and never a question asked about who is running."""

ABORT_KB = 4 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_DRIVER"

DRIVER_FILE = os.path.abspath(__file__)
RENDERER_FILE = {
    "c": os.path.join(EMULATION, "emulate.py"),
    "cpp": os.path.join(CPP, "cpp_render.py"),
    "rust": os.path.join(RUST, "rust_render.py"),
    "go": os.path.join(GO, "go_render.py"),
    "swift": os.path.join(SWIFT, "swift_render.py"),
}
"""THE CODE VERSION'S OWN INPUTS: the driver's source file, and the
source file of the renderer that writes each target.  A certificate
carries the sha256 of both, which is how a later pass knows whether the
machinery that produced it has moved -- the question the nine task-name
gates used to answer by label."""

VERSION_CACHE = {}


def sha256_of_file(path):
    """the sha256 of one source file's bytes, cached for the process."""
    if path in VERSION_CACHE:
        return VERSION_CACHE[path]
    import hashlib
    handle = open(path, "rb")
    digest = hashlib.sha256(handle.read()).hexdigest()
    handle.close()
    VERSION_CACHE[path] = digest
    return digest


def code_version(lang):
    """THE VERSION OF THE MACHINERY THIS RUN WAS PRODUCED BY: the
    driver's own source and the target's renderer, each by the sha256 of
    its bytes.

    IT REPLACES THE NINE TASK GATES.  Provenance used to be a task
    LABEL, switched on by name so an older pass reproduced verbatim;
    what a reader actually needs to know is whether the code that
    produced a certificate is the code running now, and that is a
    measurement of the files rather than a claim about a task."""
    out = {
        "driver": sha256_of_file(DRIVER_FILE),
        "driver_source": os.path.basename(DRIVER_FILE),
        "how": "sha256 of the source file's bytes",
    }
    path = RENDERER_FILE.get(lang)
    if path is not None:
        out["renderer"] = sha256_of_file(path)
        out["renderer_source"] = os.path.basename(path)
    return out


def targets():
    """the target languages, which is `TARGETS` and nothing else.

    It was a question about WHICH TASK was running: two targets under
    the first two names, four under the next four, five under the last.
    A target list is a configuration a caller states, so the caller
    states it."""
    return list(TARGETS)


# THE TEN CELLS, as the brief names them: (mnem, operand shape,
# key_width).  Ratified intention, in the brief's own order.
ASKED = [
    ("add", "gpr_gpr", 32),
    ("sub", "imm_gpr", 64),
    ("imul", "gpr_gpr", 32),
    ("sar", "cl_gpr", 32),
    ("shr", "cl_gpr", 64),
    ("idiv", "gpr_one", 32),
    ("cmovne", "gpr_gpr", 32),
    ("setne", "gpr_one", 8),
    ("addss", "xmm_xmm", 32),
    ("cvtsi2sd", "gpr_xmm", 64),
]

CAUSE_IMMEDIATE_IS_AN_INPUT = (
    "the immediate is an input of the mapping, and a corpus body "
    "carries a baked-in immediate of its own")
CAUSE_NO_ROW = "no TRANSLATED row at this cell"
CAUSE_NO_SETTER = "no setter row to compose the flag pair from"
CAUSE_FLAG_WIDTH = "the setter's flag values and the consumer's flag " \
                   "arrival are of different widths"
CAUSE_PASS_THROUGH = "the flags place of a preseeded row is the flag " \
                     "state that ARRIVED, not a place this opcode writes"


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


# ==================================================================
# section 1: THE COMMANDS
# ==================================================================





def one_recheck(shared, cells, run, place):
    """one recorded obligation, re-posed: the carved body as the record
    holds it, the cell's term rebuilt, the same alignment."""
    key = (run["mnem"], run["shape"], run["key_width"])
    if key not in cells:
        cells[key] = cell_input(read_json(CELLS), key)
    held = cells[key]
    wanted = None
    for candidate in held["places"]:
        if candidate["writes"] == place["writes"]:
            wanted = candidate
    if wanted is None:
        return {"outcome": "UNDECIDED",
                "reason": "the cell no longer carries this place"}
    # THE PARAMETER PLAN IS THE ARRIVAL CONTRACT, so it must be the one
    # the run itself used and never a rebuilt guess.  `check_one_place`
    # derives `body_families` from it (`expected_families(lang,
    # params)`), and the IN-row alignment is that against the cell's own
    # families -- so a plan of the wrong length or the wrong order does
    # not fail loudly, it aligns the wrong rows and the gate answers
    # about a comparison nobody posed.
    #
    # THE DEFECT THIS REPLACES, found by task g1b on 2026-09-09 and
    # named rather than worked around.  `rebuilt_renderer` builds the
    # TERM-ROUTE renderer for the place and takes its params.  That is
    # right for a term-route place and WRONG for a primitive-route one,
    # whose plan comes from `primitive_params(probe)` -- the operand
    # types the manifest records, which for `idiv gpr_one 32` in c is
    # TWO rows where the term route's is three.  The first pass had
    # already answered UNDECIDED for exactly that reason ("the IN rows
    # cannot be aligned: 3 and 2 IN rows"); the re-pose, handed three
    # rows, aligned the body's first argument against the cell's high
    # dividend half and returned DISPROVED with a counterexample about
    # a comparison that was never posed.
    #
    # The fix is the general one: use the plan the place RECORDS, which
    # every primitive-route place already carries, and rebuild only for
    # a place that carries none (the term route, whose rebuild is what
    # it always was).
    params = place.get("params")
    if params is None:
        renderer = rebuilt_renderer(wanted, run["lang"], place["label"])
        params = renderer.params
    raw_bytes = place["body_bytes"].split()
    mnem = place["body_text"].split("; ")
    return check_one_place(shared, wanted, params, raw_bytes,
                           mnem, place["label"], run["lang"],
                           attested=attested_of(
                               held,
                               ((run.get("primitive") or {})
                                .get("row"))))


def rebuilt_renderer(place, lang, label):
    """the renderer object again, for its parameter plan alone -- the
    source it writes is already on the record and is not rewritten."""
    built = render_one_place(place, lang, label)
    return built["renderer"]


def build_shared():
    """the three objects the pipeline's walk needs, built once."""
    import term97_walk as TW
    import canonical_form as CF
    maker, gate, _attached, _readings = TW.build()
    form = CF.new_form()
    return {
        "maker": maker,
        "gate": gate,
        "form": form,
        "reference": maker.reference,
    }


# ==================================================================
# section 2: ONE RUN -- the four steps
# ==================================================================

def find_emulation(shared, held, lang):
    """one (cell, target): the input, the render, the compile and
    carve, the check.  Every step's object is on the record."""
    record = {
        "mnem": held["mnem"],
        "shape": held["shape"],
        "key_width": held["key_width"],
        "lang": lang,
        "row_id": held.get("row_id"),
        "line": held.get("line"),
        "chosen_by": held.get("chosen_by"),
        "attestation": held.get("attestation"),
        "setter": held.get("setter"),
        "code_version": code_version(lang),
        "places": [],
    }
    if held.get("refusal_cause") is not None:
        record["refusal_cause"] = held["refusal_cause"]
        record["refusal_detail"] = held.get("refusal_detail")
        return record
    if held.get("imm_symbolic"):
        # THE IMMEDIATE IS AN INPUT, SO THERE IS NO PRIMITIVE, task
        # ap5.  `primitive_lookup`'s key is the cell's own triple
        # (`mnem`, operand shape, `key_width`) and that triple carries
        # NO IMMEDIATE, so at an `imm_*` cell it matches a corpus body
        # whose immediate is whatever constant that body happens to
        # spell -- `mov $0x8,%eax` against a cell whose own line is
        # `mov $0x3,%edi`.  Comparing those two is comparing two
        # different mappings that share a key, and every one of the six
        # `sat` verdicts task ap4's loop left at an `imm_*` cell is on
        # this route (lane `ap5_l2`, section 3: the imm_* runs are 102
        # `term` and 6 `primitive`, and the 6 are the 6 `sat`).
        #
        # Once the immediate is an INPUT of the mapping, a body with a
        # baked-in immediate is not a function of it and so is not an
        # emulation of it: the route is the term route, where the
        # immediate is rendered as one more parameter of the operand's
        # own width and the gate quantifies over it.  The refusal is
        # recorded in the same `primitive` field every other run
        # carries, so nothing about the record's shape changes.
        record["primitive"] = {
            "lang": lang,
            "cell": [held["mnem"], held["shape"], held["key_width"]],
            "row": None,
            "cause": CAUSE_IMMEDIATE_IS_AN_INPUT,
            "lookup": "not asked: the lookup's key is the cell's own "
                      "triple, which carries no immediate, so a body "
                      "it matches would carry a baked-in immediate of "
                      "its own",
        }
        record["route"] = "term"
    else:
        # PRIMITIVE-FIRST, task g1's one design decision: before the
        # cell's term is rendered at all, ask whether the target has an
        # operator whose whole lowered body IS this cell, and render
        # THAT.  `primitive_route` returns None when it does not, and
        # the term route below is then exactly what tasks h1 and h2 ran.
        found = primitive_lookup(held, lang)
        record["primitive"] = found
        if found.get("row") is not None:
            record["route"] = route_name(found["row"])
            run_primitive(shared, held, lang, record, found)
            return record
        record["route"] = "term"
    for place in held["places"]:
        record["places"].append(one_place(shared, held, place, lang))
    return record


def one_place(shared, held, place, lang):
    """steps 2, 3 and 4 for one written place of one cell."""
    out = {
        "writes": place["writes"],
        "text": place["text"],
        "sexpr": place["sexpr"],
        "bits": place["bits"],
        "families": place.get("families"),
        "home": place.get("home"),
    }
    if place.get("halved") is not None:
        out["halved"] = place["halved"]
    if place.get("not_rendered") is not None:
        out["rendered"] = False
        out["refusal_cause"] = place["not_rendered"]
        out["refusal_detail"] = place.get("not_rendered_detail")
        return out
    # THE LABEL BECOMES A c FUNCTION NAME (`emu_<label>`), so the place
    # name's own dot -- which task ap2's halves carry, `reg_xmm0.low` --
    # is spelled `_` here and nowhere else: the PLACE keeps its name on
    # the record and in the report, and only the symbol is sanitised.
    label = E.sanitize("%s_%s_%d__%s__%s"
                       % (held["mnem"], held["shape"], held["key_width"],
                          place["writes"].replace(".", "_"), lang))
    out["label"] = label
    # FIX 2 (task h2), in the DRIVER: a vector cell's place carries the
    # whole 128-bit register, so the lane the operation writes is
    # projected out of it and it is that lane which is rendered, compiled
    # and checked.  `working` is the place the four steps below act on --
    # the projected lane for a vector place under task h2, and the
    # place itself in every other case.
    working = place
    if place.get("halved") is None:
        # A HALF IS NOT A LANE (task ap2, fix 3).  `in_halves_where_it_
        # must_be` has already decided that this place has no narrower
        # lane to project and has split it into its two 64-bit halves;
        # asking `projected_lane` about a half would ask task h2's fix 2
        # the same question again, over a place whose whole point is
        # that the answer was no.
        projected = projected_lane(shared, place, held["key_width"])
        if projected is not None:
            out["lane"] = projected["lane"]
            if projected.get("refusal_cause") is not None:
                out["rendered"] = False
                out["refusal_cause"] = projected["refusal_cause"]
                out["refusal_detail"] = projected.get("refusal_detail")
                return out
            working = projected["place"]
    built = render_one_place(working, lang, label)
    renderer = built.pop("renderer", None)
    out.update(built)
    if renderer is None:
        return out
    got, refusal = compile_one_place(built["source"], built["symbol"],
                                     lang)
    if got is None:
        out["compiled"] = False
        out["compile_refusal"] = refusal
        return out
    out["compiled"] = True
    raw_bytes, mnem = got
    out["body_bytes"] = " ".join(raw_bytes)
    out["body_text"] = "; ".join(mnem)
    out["landing"] = landing_of(mnem, held["mnem"])
    out["check"] = check_one_place(shared, working, renderer.params,
                                   raw_bytes, mnem, label, lang,
                                   attested=attested_of(held, None))
    return out


# ------------------------------------------------------------------
# step 1: the input -- the cell's term per written place
# ------------------------------------------------------------------

CAUSE_NO_SEEDED_ROW = ("no TRANSLATED row at this cell whose "
                       "arriving flag state was written by this setter")


def cell_inputs(cells, asked):
    """EVERY held cell of one (`mnem`, operand shape, `key_width`): one
    per setter cell the corpus attests before this consumer, and exactly
    one where the cell reads no flag state.

    THE RULE, and it is the one the loop got wrong until 2026-09-10.  A
    flag consumer's mapping is a function of the flag state a setter
    wrote, so what is proved is the PAIR -- and the loop rendered each
    consumer over ONE setter, the mnemonic its own attestation records
    the most ledger rows for, at ONE width.  The hub measured what that
    costs: the corpus attests 44 distinct pairs over its go units and
    the dictionary could serve 10 of the 104 units that carry one,
    because every other attested pair is at another width and the
    setter's width is part of the machine-form key (log_254 SS4, and its
    awaiting-the owner item 1).  So the driver now answers one held cell per
    ATTESTED SETTER CELL, each rendered, compiled, carved and gated on
    its own.

    WHERE THE ATTESTED SETTER CELLS COME FROM: the cells file's own
    `setter_cells` for this cell, which the corpus's own flag-pair
    ledger rows give at cell granularity -- the setter's own LINE
    classified by `model_table.classify_line`, the same reading task m1b
    made and the hub's pair reader repeats.  Nothing is read off a
    token.  Where the cells file carries none (the outer sets built
    before 2026-09-10 record a setter by `mnem` alone), the answer is
    the one held cell the loop always built, and the record says which
    setter it is.  THE LOOP'S OWN CHOICE IS ALWAYS INCLUDED, so a
    certificate banked before this change is still derivable."""
    first = cell_input(cells, asked)
    if first.get("setter") is None:
        return [first]
    wanted = attested_setter_cells(cells, asked)
    held_by_key = {}
    order = []
    default = (first["setter"].get("mnem"), first["setter"].get("shape"),
               first["setter"].get("key_width"))
    held_by_key[default] = first
    order.append(default)
    for setter_cell in wanted:
        key = (setter_cell["mnem"], setter_cell["shape"],
               setter_cell["key_width"])
        if key in held_by_key:
            continue
        held_by_key[key] = cell_input(cells, asked, setter_cell)
        order.append(key)
        continue
    out = []
    for key in order:
        out.append(held_by_key[key])
        continue
    return out


def attested_setter_cells(cells, asked):
    """the setter CELLS the corpus attests before this consumer cell,
    off the cells file's own `setter_cells`, strongest attestation
    first."""
    mnem, shape, key_width = asked
    for record in cells["asked"]:
        if record["asked"]["mnem"] != mnem:
            continue
        if record["asked"]["shape"] != shape:
            continue
        if record["asked"]["key_width"] != key_width:
            continue
        held = record.get("setter_cells") or []
        return sorted(held,
                      key=lambda entry: (-(entry.get("ledger_rows") or 0),
                                         entry["mnem"],
                                         "%s" % entry.get("shape"),
                                         "%s" % entry.get("key_width")))
    return []


def cell_input(cells, asked, setter_cell=None):
    """the cell as the model table holds it, with the z3 term of every
    written place rebuilt by re-running the row's own line.

    `setter_cell`, where it is given, is the setter cell this held cell
    is to be composed over: the row chosen is the one the sweep seeded
    with THAT setter's flag state, and the setter's own row is the one
    at that cell's shape and width."""
    mnem, shape, key_width = asked
    held = {"mnem": mnem, "shape": shape, "key_width": key_width}
    row = chosen_row(cells, asked, held, setter_cell)
    if row is None:
        held["refusal_cause"] = CAUSE_NO_ROW
        if held.pop("no_seeded_row", None):
            held["refusal_cause"] = CAUSE_NO_SEEDED_ROW
        return held
    held["row_id"] = row["row_id"]
    held["line"] = row.get("text")
    held["width"] = row.get("width")
    held["attestation"] = row.get("attestation")
    # THE IMMEDIATE IS AN INPUT (log 249): whether THIS cell's chosen
    # row is the one whose
    # immediate is an input of the mapping.  It rides on `held`, which
    # is the driver's own working object, and not on the run record --
    # `chosen_by` is what the record says about it, and the cells file
    # carries the row's own `imm_symbolic` field.
    held["imm_symbolic"] = bool(row.get("imm_symbolic"))
    places, flags = terms_of_row(row)
    if places is None:
        held["refusal_cause"] = CAUSE_NO_ROW
        held["refusal_detail"] = flags
        return held
    substitution = []
    if row.get("preseeded") and a_place_reads_the_arriving_flags(places,
                                                                flags):
        composed = compose_the_pair(cells, row, places, setter_cell)
        if composed.get("refusal_cause") is not None:
            held["refusal_cause"] = composed["refusal_cause"]
            held["refusal_detail"] = composed.get("refusal_detail")
            return held
        held["setter"] = composed["setter"]
        substitution = composed["substitution"]
    held["places"] = vector_arrivals_in_halves(
        in_halves_where_it_must_be(
            places_as_records(row, places, flags, substitution),
            held["key_width"]),
        held["key_width"])
    return held


HALF_BITS = 64


def in_halves_where_it_must_be(records, key_width):
    """FIX 3 (task ap2), in the DRIVER: A 128-BIT PLACE IS TWO 64-BIT
    PLACES.

    THE TWO DEFECTS THIS ONE CHANGE ANSWERS, both task ap1's
    (log_243 section 6).
      * `the cell's own key_width is not narrower than the place, so
        there is no lane to project` -- 56 runs, 19,324 attested ledger
        rows, all four targets.  Task h2's fix 2 projects a vector
        cell's LANE out of its 128-bit place, and a whole-register cell
        (`xorps` xmm_same 128, `movaps` xmm_xmm 128) has no narrower
        lane to project, so the driver said so and stopped.
      * `a width c has no holder for` -- 30 runs, 25,130 attested
        ledger rows, go and swift only.  The flags place of a 64-bit
        comparison is the two operands CONCATENATED, 128 bits wide, and
        neither the go nor the swift renderer has a 128-bit integer
        holder to answer in.  c and rust do (`unsigned __int128`,
        `i128`), which is why the same cells stopped on two targets and
        not the other two.

    THE FIX, one sentence: a written place wider than the widest thing
    a target can answer in is rendered as TWO places -- its low 64 bits
    and its high 64 bits -- each its OWN written place, each rendered,
    compiled, carved and put to the gate on its own, so nothing about
    what is compared changes and only the number of comparisons does.

    WHY THAT IS NOT A WEAKENING.  The obligation over a 128-bit place
    is that every one of its bits equals the cell's, and the
    conjunction of the two halves' obligations is exactly that -- the
    same bits, in two questions instead of one.  What it costs is that
    a cell is proved on a target only when BOTH halves prove, and the
    loop's own report is what has to say so rather than count the first
    half; `autopoly2.outcome_of` is where that is written down.

    WHY IT IS DONE IN EVERY TARGET AND NOT ONLY IN go AND swift.  A
    place that c answers in one `unsigned __int128` and go answers in
    two `uint64` would be two different comparisons carrying one
    verdict column, and the four targets' rows would stop being
    comparable row for row -- which is the whole point of the table.
    So the spelling is the same everywhere.

    WHAT IS NOT TOUCHED.  A vector place with a lane NARROWER than
    itself is task h2's fix 2 and is left to it: `one_place` projects
    the lane and this function passes the place through untouched, so
    the handful's four vector cells (`addss` 32, `cvtsi2sd` 64 and
    their like) run exactly as task g1b ran them."""
    out = []
    for record in records:
        if record.get("bits") is None or record["bits"] <= HALF_BITS:
            out.append(record)
            continue
        if is_a_lane_to_project(record, key_width):
            out.append(record)
            continue
        if E.is_an_x87_arrival((record.get("home") or {}).get("family")):
            # AN x87 PLACE IS NOT HALVED (task ap3, fix 2).  The reason
            # this function halves is that no target can ANSWER more
            # than 64 bits; c can answer an x87 place whole, in a
            # `long double`, so halving it would cut a value in two
            # that the target holds in one -- and its high half is 15
            # bits, which is not a holder anywhere.  The targets with
            # no 80-bit holder refuse the place by nature
            # (`render_one_place`), which is the brief's own rule and
            # is why these rows are NOT comparable target for target.
            out.append(record)
            continue
        out.extend(halves_of(record))
    return out


def is_a_lane_to_project(record, key_width):
    """whether task h2's fix 2 will project a narrower lane out of this
    place, which is the one case this fix leaves alone.  The test is
    `projected_lane`'s own, restated over the record alone so no gate
    call is made to answer it."""
    home = record.get("home") or {}
    if home.get("family") not in R.XMM_NAMES:
        return False
    if key_width is None:
        return False
    return key_width < record["bits"]


def halves_of(record):
    """the place as its low half and its high half, each a written
    place in its own right.

    The name each half writes is the place's own name with `.low` or
    `.high` after it.  That name is a PLACE name, not a key over a
    spelling: the place's own `writes` field is what the report,
    `destination_place` and `one_recheck` already read, and the two
    halves are two of them."""
    out = []
    term = record["term"]
    bits = term.size()
    for name, high, low in (("low", HALF_BITS - 1, 0),
                            ("high", bits - 1, HALF_BITS)):
        piece = z3.simplify(z3.Extract(high, low, term))
        half = place_record("%s.%s" % (record["writes"], name), piece)
        half["home"] = dict(record["home"])
        half["halved"] = {
            "of_place": record["writes"],
            "of_bits": bits,
            "half": name,
            "projection": "Extract(%d, %d, the cell's own term for "
                          "this place)" % (high, low),
        }
        if record.get("not_rendered") is not None:
            half["not_rendered"] = record["not_rendered"]
            half["not_rendered_detail"] = record.get("not_rendered_detail")
        out.append(half)
    return out


def chosen_row(cells, asked, held, setter_cell=None):
    """the one row of the cell.

    A cell can carry several sweep rows: the sweep walks four operand
    WIDTHS and `key_width` is the operation's own lane width, so a
    vector or convert cell holds one row per loop width; and a
    flag-reading mnemonic is re-run once per flag-setting mnemonic the
    sweep saw.  The rules, both machine form: take the row whose own
    `width` equals the cell's `key_width`, and among the flag-reading
    rows take the one whose `flags_in` is the setter the cell's own
    attestation records most ledger rows for."""
    mnem, shape, key_width = asked
    rows = []
    for record in cells["asked"]:
        if record["asked"]["mnem"] != mnem:
            continue
        if record["asked"]["shape"] != shape:
            continue
        if record["asked"]["key_width"] != key_width:
            continue
        rows = record["rows"]
    translated = []
    for row in rows:
        if row.get("outcome") == "TRANSLATED":
            translated.append(row)
    if not translated:
        return None
    if setter_cell is not None:
        # THE ROW SEEDED WITH THIS SETTER.  The sweep re-runs a
        # flag-reading mnemonic once per flag-SETTING mnemonic it saw
        # and seeds the flag state as (`the setter's mnem`,
        # `seed_FLAG_L`, `seed_FLAG_R`), so the consumer's own term is
        # written against that setter's flag semantics.  Composing it
        # over another setter's values would be composing two mappings
        # that were never posed together, so where the sweep never
        # seeded this cell with this setter the answer is a refusal by
        # cause and never a substitution.
        for row in translated:
            if (row.get("flags_in") or {}).get("mnem") != setter_cell["mnem"]:
                continue
            if row.get("width") != key_width:
                continue
            held["chosen_by"] = ("of the %d TRANSLATED rows at this "
                                 "cell, the one whose arriving flag "
                                 "state was written by the setter cell "
                                 "this run composes over"
                                 % len(translated))
            return row
        for row in translated:
            if (row.get("flags_in") or {}).get("mnem") != setter_cell["mnem"]:
                continue
            held["chosen_by"] = ("of the %d TRANSLATED rows at this "
                                 "cell, the one seeded by this run's "
                                 "own setter mnemonic"
                                 % len(translated))
            return row
        held["refusal_detail"] = ("%s %s %s"
                                  % (setter_cell["mnem"],
                                     setter_cell["shape"],
                                     setter_cell["key_width"]))
        held["no_seeded_row"] = True
        return None
    symbolic = the_symbolic_immediate_row(translated)
    if symbolic is not None:
        held["chosen_by"] = ("of the %d TRANSLATED rows at this cell, "
                             "the one whose immediate is an INPUT of "
                             "the mapping rather than a literal "
                             "(`imm_symbolic`)" % len(translated))
        return symbolic
    if len(translated) == 1:
        held["chosen_by"] = "the one TRANSLATED row at this cell"
        return translated[0]
    wanted = best_setter(translated)
    if wanted is None:
        wanted = setter_from_the_corpus(cells, mnem, held)
    if wanted is not None:
        for row in translated:
            if (row.get("flags_in") or {}).get("mnem") != wanted:
                continue
            held["chosen_by"] = ("of the %d TRANSLATED rows at this "
                                 "cell, the one whose arriving flag "
                                 "state was written by the setter the "
                                 "cell's own attestation records the "
                                 "most ledger rows for"
                                 % len(translated))
            return row
    for row in translated:
        if row.get("width") == key_width:
            held["chosen_by"] = ("of the %d TRANSLATED rows at this "
                                 "cell, the one whose own sweep width "
                                 "equals the cell's key_width"
                                 % len(translated))
            return row
    held["chosen_by"] = "the first TRANSLATED row at this cell"
    return translated[0]


def the_symbolic_immediate_row(rows):
    """the row of this cell whose immediate is an INPUT of the mapping,
    or None where the cell has none.

    THE DRIVER'S HALF OF THE SYMBOLIC IMMEDIATE (log 249).  A cell key is
    (`mnem`, operand shape, `key_width`) and carries no immediate, so
    the sweep's own `imm_*` spelling bakes its literal `$0x3` into the
    mapping while the corpus rows the cell is attested by spell
    `$0x1`, `$0x8` and the rest -- which is why `mov` imm_gpr 8 and 32
    disproved against them with an EMPTY counterexample (log_246
    section 5.2: both sides constants, different constants, no free
    variable for z3 to name).  `model_translate.shapes_for` now spells
    each `imm_*` shape a second time with a register of the operand's
    own width in the immediate's slot, which is how the reference's
    own operand reader spells a value of that width that is not a
    literal, and this function is what makes the driver ask THAT row.

    THE FIELD AND NOT THE TOKEN.  The row is found by its own
    `imm_symbolic` field, which the row carries; nothing here reads a
    mnemonic, an operand text or a shape spelling to decide it."""
    for row in rows:
        if row.get("imm_symbolic"):
            return row
    return None


def best_setter(rows):
    """the flag-setting mnemonic the cell's own attestation records the
    most ledger rows for, or None when the cell records none."""
    counted = {}
    for row in rows:
        for entry in ((row.get("attestation") or {}).get("setter") or []):
            name = entry.get("mnem")
            counted[name] = max(counted.get(name, 0),
                                entry.get("ledger_rows") or 0)
    if not counted:
        return None
    best = None
    for name in sorted(counted):
        if best is None or counted[name] > counted[best]:
            best = name
    return best


def setter_from_the_corpus(cells, mnem, held):
    """FIX 2 (task ap2), in the DRIVER: THE SETTER A FLAG CONSUMER'S
    OWN CELL DOES NOT NAME, TAKEN FROM THE ATTESTATION.

    THE DEFECT.  A flag-reading cell's mapping is a function of the
    flags a SETTER wrote, so `compose_the_pair` composes the two into
    one function; where the chosen row names no setter it answers the
    cause `no setter row to compose the flag pair from: None at width
    8`, which was task ap1's second largest -- 128 runs over 6,284
    attested ledger rows, 32 cells, on all four targets (log_243
    section 6).  `best_setter` reads the setter off THIS CELL's own
    attestation, and where the corpus attested the consumer without
    ever recording which setter preceded it, that list is empty and the
    row chosen is one the sweep seeded with a generic flag state.

    THE FIX, and it invents nothing.  The corpus DOES record the pair.
    A ledger row whose producer is a flag pair carries a two-element
    `mnem` list -- the setter, then the consumer -- and task m1b's
    attestation pass walked 22,741 of them
    (`attestation_flag_pair_rows_seen`).  So where this cell names no
    setter, the setter is the one the corpus records most often before
    THIS CONSUMER anywhere: the census `cells["setter_census"]`, which
    the task's own cells lane sums straight off
    `model_table_attest.json` over every attested cell of the
    consumer's mnemonic.  It is the same quantity `best_setter` reads,
    read over the consumer instead of over the one cell.

    IF THE CORPUS RECORDS NONE EITHER, this returns None and the cause
    stands unchanged -- the brief's own rule."""
    census = (cells.get("setter_census") or {}).get(mnem)
    if not census:
        return None
    best = None
    counted = {}
    for entry in census:
        counted[entry["mnem"]] = entry.get("ledger_rows") or 0
    for name in sorted(counted):
        if best is None or counted[name] > counted[best]:
            best = name
    if best is not None:
        held["setter_from_the_corpus"] = {
            "mnem": best,
            "ledger_rows": counted[best],
            "why": "this cell's own attestation records no setter, so "
                   "the setter is the one the corpus's flag-pair "
                   "ledger rows record most often before this "
                   "consumer",
        }
    return best


def terms_of_row(row):
    """the row's own z3 terms, per written place, and the flag triple:
    `model_table.places_of_attempt`, called on the row's own fields."""
    attempt = {
        "mnem": row["mnem"],
        "operands": row.get("operands") or [],
        "preseeded": row.get("preseeded", False),
        "flags_in_setter": (row.get("flags_in") or {}).get("mnem"),
        "width": row.get("width"),
    }
    return MTAB.places_of_attempt(attempt)


def a_place_reads_the_arriving_flags(places, flags):
    """whether ANY term of this row reads the flag state the sweep
    seeded -- which is what makes a row a flag CONSUMER and obliges the
    driver to compose it with a setter.

    FIX 2 (task ap3), in the DRIVER, and it is one condition.

    THE DEFECT.  `cell_input` composed the pair for every row the sweep
    marked `preseeded`, and `preseeded` says only that the sweep HANDED
    the builder a flag state, not that the opcode read it.  Task ap1's
    second largest cause -- `no setter row to compose the flag pair
    from: None at width 8`, 128 runs over 6,284 attested ledger rows --
    is 32 x87 cells (`faddl`, `fdivp`, `fucomi` and their like) at
    `key_width` 80, and task ap2 measured the corpus's own answer for
    them: not one of the 25 flag consumers the corpus records is an x87
    mnemonic, so no setter exists to compose with (log_244 section 5).
    Task ap3's lane `ap3_l2` asked the other side of it and the answer
    is the same in the objects: **0 of the 32 rows has any place that
    reads `seed_FLAG_L` or `seed_FLAG_R`**.  They are not flag
    consumers; the driver was demanding a composition for a row with
    nothing to compose.

    THE FIX, one sentence: a preseeded row is composed with a setter
    only where one of its own terms actually reads the arriving flag
    state, and a row that reads neither symbol goes on to the render
    with the places it has.

    WHAT IS NOT TOUCHED.  A row that DOES read the pair takes exactly
    the path it took before -- `cmovne` gpr_gpr 32 and `setne` gpr_one
    8 are the guard, and both still compose with `test`.  The flags
    place of a preseeded row that writes nothing there is still marked
    `CAUSE_PASS_THROUGH` by `places_as_records`, which is a different
    question and is answered where it was."""
    for name in sorted(places or {}):
        if reads_the_arriving_flags(places[name]):
            return True
    if flags is None:
        return False
    pair = z3.Concat(MT.as_bits(flags[1]), MT.as_bits(flags[2]))
    if is_the_arriving_flag_state(pair):
        # the opcode wrote nothing to the flags, so this place IS the
        # arriving state and `places_as_records` records it as such;
        # composing a setter for it would answer a question about the
        # setter and not about this opcode.
        return False
    return reads_the_arriving_flags(pair)


def reads_the_arriving_flags(term):
    """whether a term reads either half of the flag state the sweep
    seeded."""
    for symbol in T.free_symbols_in_order(term):
        if symbol.decl().name() in ("seed_FLAG_L", "seed_FLAG_R"):
            return True
    return False


def compose_the_pair(cells, row, places, setter_cell=None):
    """a flag-reading cell's mapping is a function OF THE FLAGS a
    setter wrote, so the pair is rendered as ONE function: the
    comparison, then the select.

    Mechanically: the sweep hands a flag-reading builder a state whose
    flags are (`the setter's mnem`, `seed_FLAG_L`, `seed_FLAG_R`), so
    the cell's term reads those two symbols.  The setter's OWN row is
    re-run, its builder leaves the same triple with its own two values
    in it, and those two values are substituted for the consumer's two
    flag arrivals.  The setter's own arrivals are renamed onto argument
    registers the consumer does not read, so the composed function's
    inputs are the two values compared and the values selected
    between."""
    setter_mnem = (row.get("flags_in") or {}).get("mnem")
    from_the_corpus = None
    if setter_cell is not None:
        setter_mnem = setter_cell["mnem"]
    if setter_mnem is None:
        # FIX 2 (task ap2): the chosen row is preseeded but names no
        # setter, so the setter is the one the corpus's own flag-pair
        # ledger rows record most often before this consumer.  See
        # `setter_from_the_corpus`.  Where `chosen_row` could pick a
        # row that names one it already has; this is the case where the
        # cell carries no such row at all.
        held = {}
        setter_mnem = setter_from_the_corpus(cells, row["mnem"], held)
        from_the_corpus = held.get("setter_from_the_corpus")
    setter_row = setter_row_for(cells, row, setter_mnem, setter_cell)
    if setter_row is None:
        return {"refusal_cause": CAUSE_NO_SETTER,
                "refusal_detail": "%s at width %s" % (setter_mnem,
                                                      row.get("width"))}
    _setter_places, setter_flags = terms_of_row(setter_row)
    if setter_flags is None:
        return {"refusal_cause": CAUSE_NO_SETTER,
                "refusal_detail": "the setter's own row leaves no flag "
                                  "state"}
    left = MT.as_bits(setter_flags[1])
    right = MT.as_bits(setter_flags[2])
    left, right = renamed_apart(places, left, right)
    arrival_left = z3.BitVec("seed_FLAG_L", row.get("width"))
    arrival_right = z3.BitVec("seed_FLAG_R", row.get("width"))
    if left.size() != arrival_left.size():
        return {"refusal_cause": CAUSE_FLAG_WIDTH,
                "refusal_detail": "the setter's values are %d bits and "
                                  "the arriving flag state is %d"
                                  % (left.size(), arrival_left.size())}
    setter = {
        "mnem": setter_row["mnem"],
        # THE SETTER'S OWN CELL, in machine form, because the pair is
        # what was proved: the same consumer over a setter at another
        # width is another artifact and carries its own certificate.
        "shape": setter_row.get("shape"),
        "key_width": setter_row.get("key_width"),
        "row_id": setter_row["row_id"],
        "line": setter_row.get("text"),
        "why": "the setter this cell's own attestation records the most "
               "ledger rows for",
        "why_this_cell": None,
        "composition": ("seed_FLAG_L := %s ; seed_FLAG_R := %s"
                        % (left, right)),
    }
    if from_the_corpus is not None:
        setter["why"] = from_the_corpus["why"]
        setter["from_the_corpus"] = from_the_corpus
    if setter_cell is not None:
        setter["why"] = ("one of the setter cells the corpus's own "
                         "flag-pair ledger rows attest before this "
                         "consumer")
        setter["why_this_cell"] = {
            "ledger_rows": setter_cell.get("ledger_rows"),
            "how": "the setter's own line, classified by the model "
                   "table's own classifier",
        }
    return {"setter": setter,
            "substitution": [(arrival_left, left),
                             (arrival_right, right)]}


def setter_row_for(cells, row, setter_mnem, setter_cell=None):
    """the setter's own cell: the row at the setter cell this run
    composes over, or -- where the run names none -- the row at the
    consumer's own width, in the two-register operand shape where it
    has one, which is the choice the loop made before 2026-09-10."""
    if setter_cell is not None:
        for candidate in cells["setter_rows"]:
            if candidate["mnem"] != setter_cell["mnem"]:
                continue
            if candidate.get("shape") != setter_cell["shape"]:
                continue
            if candidate.get("key_width") != setter_cell["key_width"]:
                continue
            return candidate
        return None
    best = None
    for candidate in cells["setter_rows"]:
        if candidate["mnem"] != setter_mnem:
            continue
        if candidate.get("width") != row.get("width"):
            continue
        if candidate.get("shape") == "gpr_gpr":
            return candidate
        if best is None:
            best = candidate
    return best


def renamed_apart(places, left, right):
    """the setter's own arrivals moved onto argument registers the
    consumer's own term does not read, so the composed function's
    inputs do not collide.

    The consumer's `cmovne %esi,%edi` reads rdi and rsi and so does a
    setter's `test %esi,%edi`; they are two different pairs of values
    in any real body, so the setter's two are moved to the next
    argument registers the consumer leaves free, in the calling rule's
    own order."""
    taken = set()
    for name in places:
        for symbol in T.free_symbols_in_order(places[name]):
            taken.add(symbol.decl().name())
    free = []
    for family in E.GENERAL_ORDER:
        if "seed_%s" % family in taken:
            continue
        free.append(family)
    moved = {}
    index = 0
    for term in (left, right):
        for symbol in T.free_symbols_in_order(term):
            name = symbol.decl().name()
            if name in moved:
                continue
            if index >= len(free):
                raise E.Refused(E.CAUSE_ARITY,
                                "the setter's arrivals outnumber the "
                                "argument registers the consumer leaves "
                                "free")
            moved[name] = z3.BitVec("seed_%s" % free[index],
                                    symbol.size())
            index = index + 1
    substitution = []
    for name in sorted(moved):
        substitution.append((z3.BitVec(name, moved[name].size()),
                             moved[name]))
    if not substitution:
        return left, right
    return (z3.substitute(left, *substitution),
            z3.substitute(right, *substitution))


def places_as_records(row, places, flags, substitution):
    """one record per written place, in the model table's own order:
    the destination places by name, then the flags."""
    out = []
    for name in sorted(places):
        term = places[name]
        if substitution:
            term = z3.substitute(term, *substitution)
        out.append(place_record(
            name, x87_as_arrivals(memory_as_arrivals(term))))
    if flags is None:
        return out
    pair = z3.Concat(MT.as_bits(flags[1]), MT.as_bits(flags[2]))
    arriving = row.get("preseeded") and is_the_arriving_flag_state(pair)
    if substitution:
        pair = z3.substitute(pair, *substitution)
    record = place_record(
        "flags", x87_as_arrivals(memory_as_arrivals(pair)))
    if arriving:
        record["not_rendered"] = CAUSE_PASS_THROUGH
    out.append(record)
    return out


MEMORY_PREFIX = "seed_MEM_"

MEMORY_ARRIVAL_BITS = 64


def memory_as_arrivals(term):
    """FIX 1 (task ap2), in the DRIVER: A MEMORY OPERAND IS ONE MORE
    ARRIVING VALUE.

    THE DEFECT.  `families_of` refuses any free symbol that is not a
    register family, and the cause it raises --
    `emulate.CAUSE_STATE`, "term reads state that is not an arrival
    register" -- was task ap1's largest, 134 runs over 37,874 attested
    ledger rows (log_243 section 6).  Part of that population is not
    machine state at all: it is a LITERAL MEMORY OPERAND, the cell's
    own `mem_*` and `widen_mem_*` shapes, which
    `reference.memory_symbol_name` gives the symbol `seed_MEM_<the
    mangled operand text>`.  The mapping reads that cell's CONTENTS and
    nothing else about memory -- no address arithmetic, no aliasing --
    so the contents are an arriving value like any other, and task o8's
    own memory rows passed them the same way.

    WHAT THIS FUNCTION DOES, one sentence: every `seed_MEM_*` symbol
    narrower than an arriving value is re-read as the low bits of a
    64-bit arrival of the same name, so the memory cell arrives BY
    VALUE in an argument register exactly as a general register family
    does.

    WHY 64 AND NOT THE OPERAND'S OWN WIDTH.  An arrival is what
    `pool100_entry_equivalence.family_bits` says it is -- 128 bits for
    a vector family and 64 for every other -- and the IN-row alignment
    compares the two sides at that width.  A general register works the
    same way today: `seed_rax` is 64 bits and a 32-bit read of it is
    `Extract(31, 0, seed_rax)`, from which `Renderer.plan_parameters`
    plans a 32-bit holder.  Writing the memory arrival the same way is
    what makes the alignment layer need no change at all: this fix is
    entirely in the driver.

    A symbol already 64 bits is left exactly as it is.

    THE WIDE CASE, and it is 104 of the 134 runs.  The reference gives
    a memory operand ONE symbol per operand text, and it is as wide as
    the widest thing that operand could hold -- 128 bits, so that a
    vector load and a general load name the same cell.  A cell that
    LOADS FROM MEMORY INTO A LANE reads only the low bits of it:
    `cmp mem_gpr 64` reads bits 63..0, `addss mem_xmm 32` reads bits
    31..0.  Where every use of the symbol lies inside the low 64 bits,
    the arrival is those 64 bits and the bits above them are never
    read, so the symbol is replaced by that arrival grown back to its
    own width -- and `z3.simplify` cuts the growth away again at each
    use, leaving a term that reads a 64-bit arriving value and nothing
    else.

    WHERE A USE REACHES ABOVE BIT 63 the symbol is left exactly as it
    is and `families_of` refuses it as before: a whole 128-bit memory
    cell is not an arriving value, for the same reason a whole 128-bit
    vector register is not, and inventing one would be inventing an
    arrival contract.  `Renderer.collect_uses` is the walker that
    answers which it is, called here rather than restated."""
    substitution = []
    for symbol in MT.free_symbols_ordered(term):
        name = symbol.decl().name()
        if not name.startswith(MEMORY_PREFIX):
            continue
        if symbol.sort().kind() != z3.Z3_BV_SORT:
            continue
        if symbol.size() == MEMORY_ARRIVAL_BITS:
            continue
        if symbol.size() < MEMORY_ARRIVAL_BITS:
            arrival = z3.BitVec(name, MEMORY_ARRIVAL_BITS)
            substitution.append(
                (symbol, z3.Extract(symbol.size() - 1, 0, arrival)))
            continue
        if not read_inside_the_low_bits(term, name,
                                        MEMORY_ARRIVAL_BITS):
            continue
        arrival = z3.BitVec(name, MEMORY_ARRIVAL_BITS)
        substitution.append(
            (symbol,
             z3.ZeroExt(symbol.size() - MEMORY_ARRIVAL_BITS, arrival)))
    if not substitution:
        return term
    return z3.simplify(z3.substitute(term, *substitution))


def x87_as_arrivals(term):
    """FIX 2 (task ap3), in the DRIVER: A LITERAL MEMORY OPERAND READ AT
    THE x87 SORT IS ONE MORE ARRIVING VALUE, on the same rule task ap2
    wrote for a memory operand read at a bit-vector sort.

    `reference.x87_symbol` names it `x87_<the mangled operand text>` --
    `faddl (%rsi)` reads `x87__rsi_` at `reference.X87_SORT` -- and
    `families_of` refuses any free symbol that does not begin
    `seed_`.  The mapping reads that memory cell's CONTENTS and nothing
    else about memory, so the contents are an arriving value, and the
    symbol is re-read under the `seed_` spelling every other arrival
    carries.  Nothing about its sort or its width changes: an x87
    arrival is 79 bits as z3 spells it, at every step.

    An x87 STACK POSITION the model table preseeded is already
    `seed_X87_0` / `seed_X87_1` and is left exactly as it is."""
    substitution = []
    for symbol in MT.free_symbols_ordered(term):
        name = symbol.decl().name()
        if name.startswith("seed_"):
            continue
        if symbol.sort() != R.X87_SORT:
            continue
        substitution.append((symbol, z3.FP("seed_%s" % name,
                                           R.X87_SORT)))
    if not substitution:
        return term
    return z3.substitute(term, *substitution)


VECTOR_ARRIVAL_BITS = 128
"""the width of a vector arrival, `pool100_entry_equivalence.
family_bits`'s own number for a family in `reference.XMM_NAMES`."""

VECTOR_HALF_BITS = 64


def vector_arrivals_in_halves(records, key_width):
    """FIX 1 (task ap3), in the DRIVER: A 128-BIT ARRIVING VECTOR
    REGISTER IS TWO 64-BIT ARRIVING VALUES.

    THE DEFECT, and it is the ARRIVAL side of task ap2's fix 3.  That
    fix answered the ANSWER side -- a 128-bit written place is two
    64-bit written places -- and left behind the cause `vector arrival
    used beyond its low lane`, 40 runs over 5,600 attested ledger rows
    on all four targets (log_244 section 11), which is
    `emulate.Renderer.plan_parameters` refusing a vector family whose
    uses reach above bit 63: no target can receive a whole 128-bit
    register as a parameter.  Task ap3's lane `ap3_l2` names the
    population exactly -- ten cells (`andps`, `movaps`, `pxor`,
    `unpckhpd` and their like), every one of them reading
    `Extract(127, 64, seed_xmm<n>)`.

    THE FIX, one sentence: where a place's term reads a 128-bit vector
    arrival above bit 63, that arrival is rewritten as
    `Concat(seed_<family>_high, seed_<family>_low)` -- two 64-bit
    arriving values -- so the place is rendered from two parameters the
    target CAN receive, and the gate aligns them against the arrival's
    own two 64-bit slices, because `pool100_entry_equivalence.
    family_bits` gives a family that is not a vector register 64 bits
    and `align_by_row` puts each half on its own IN row.

    WHY IT IS PER PLACE AND NOT PER CELL, which is the whole of the
    guard.  A vector cell whose place reads only the low lane -- the
    handful's `addss` xmm_xmm 32 and `cvtsi2sd` gpr_xmm 64, and the LOW
    half of every whole-register vector cell task ap2 proved -- is
    rendered from a `float` or `double` parameter arriving in an xmm
    register, and rewriting its arrival would change a contract that
    already proves.  So the test is `emulate.Renderer.collect_uses`, the
    same walker `plan_parameters` refuses on, asked of THIS place's own
    term: a place none of whose uses reaches above bit 63 is passed
    through untouched.

    WHAT THE TWO HALVES ARE NOT.  They are not a new arrival contract
    for the OPCODE: the opcode still receives one 128-bit register, and
    the two halves are how the TARGET's own function receives the same
    128 bits.  Where the body reads them from two general argument
    registers and the cell reads them from one vector register, the two
    sides carry the same values on the same IN rows and that is what
    the gate compares."""
    out = []
    for record in records:
        if is_a_lane_to_project(record, key_width):
            # THE LANE PROJECTION GETS THIS PLACE (log 240's fix 2), and
            # it is the guard the
            # brief names.  A vector cell with a lane narrower than its
            # place -- the handful's `addss` xmm_xmm 32 and `cvtsi2sd`
            # gpr_xmm 64 -- carries the arrival bits ABOVE the lane in
            # its place's term, joined under the answer, so the place
            # does read `seed_xmm0` above bit 63; but `one_place`
            # projects the lane out of it before anything is rendered
            # and the projected term reads only the lane.  Splitting
            # the arrival here would rewrite a contract that already
            # proves, and the guard of lane `ap3_l5` is what caught it.
            out.append(record)
            continue
        rewritten = in_two_halves(record)
        if rewritten is None:
            out.append(record)
            continue
        out.append(rewritten)
    return out


def in_two_halves(record):
    """the record with every wide-read vector arrival rewritten, or None
    when this place reads none."""
    term = record.get("term")
    if term is None:
        return None
    holder = E.Renderer([], None, 0, "vector_arrival")
    holder.collect_uses(term, None)
    substitution = []
    for name in sorted(holder.uses):
        if not name.startswith("seed_"):
            continue
        family = name[len("seed_"):]
        if family not in R.XMM_NAMES:
            continue
        wide = False
        for use in holder.uses[name]:
            if use is None:
                wide = True
            elif use[0] > VECTOR_HALF_BITS - 1:
                wide = True
        if not wide:
            continue
        whole = z3.BitVec(name, VECTOR_ARRIVAL_BITS)
        low = z3.BitVec("seed_%s_low" % family, VECTOR_HALF_BITS)
        high = z3.BitVec("seed_%s_high" % family,
                         VECTOR_ARRIVAL_BITS - VECTOR_HALF_BITS)
        substitution.append((whole, z3.Concat(high, low)))
    if not substitution:
        return None
    rebuilt = place_record(record["writes"],
                           z3.simplify(z3.substitute(term,
                                                     *substitution)))
    rebuilt["home"] = dict(record["home"])
    for carried in ("halved", "not_rendered", "not_rendered_detail"):
        if record.get(carried) is not None:
            rebuilt[carried] = record[carried]
    rebuilt["arrivals_in_halves"] = []
    for whole, _pair in substitution:
        rebuilt["arrivals_in_halves"].append(whole.decl().name())
    return rebuilt


def read_inside_the_low_bits(term, name, bits):
    """whether every use of the free symbol `name` in `term` lies
    inside its low `bits` bits.

    `emulate.Renderer.collect_uses` is the walker -- the same one
    `plan_parameters` uses to decide a holder's width -- and it records
    `None` for a use of the whole symbol and `(high, low)` for a use
    through an `Extract`.  A `None` is a whole read, which is not
    inside anything."""
    holder = E.Renderer([], None, 0, "memory_arrival")
    holder.collect_uses(term, None)
    uses = holder.uses.get(name)
    if not uses:
        return False
    for use in uses:
        if use is None:
            return False
        if use[0] > bits - 1:
            return False
    return True


def is_the_arriving_flag_state(pair):
    """true when the flags term is character-for-character the flag
    state the sweep seeded, so the opcode wrote nothing there."""
    import term as T
    names = []
    for symbol in T.free_symbols_in_order(pair):
        names.append(symbol.decl().name())
    return sorted(names) == ["seed_FLAG_L", "seed_FLAG_R"]


def place_record(name, term):
    """one written place: its name, the z3 term itself, its term
    LITERAL by the pipeline's own layer-5 rule, its width, and the
    arrival families it reads.

    The `term` field holds the z3 object and is dropped before the
    record is written, so the term the renderer walks and the text the
    report prints cannot drift apart."""
    holder = T.Term()
    record = {
        "writes": name,
        "term": term,
        "text": holder.normalize(term),
        "sexpr": term.sexpr(),
        "bits": term.size(),
    }
    try:
        record["families"] = families_of(term)
    except E.Refused as refusal:
        record["families"] = None
        record["not_rendered"] = refusal.cause
        record["not_rendered_detail"] = refusal.detail
    record["home"] = home_of(name)
    return record


def families_of(term):
    """the arrival families the term reads, in the layer-5 print order
    the LITERAL text shows -- so `v0` is the first -- with the general
    registers before the vector ones.

    THE ORDER IS THE CONVENTION THE DRIVER STATES.  The renderer gives
    parameter i the family at position i, and c's and rust's own
    calling rule puts general parameters in rdi, rsi, rdx, rcx, r8, r9
    and float parameters in xmm0 upwards, in declaration order
    (`emulate.expected_c_families`).  Partitioning general before
    vector makes position i the same KIND on both sides, which is what
    the IN-row alignment needs."""
    general = []
    vector = []
    x87 = []
    for symbol in MT.free_symbols_ordered(term):
        name = symbol.decl().name()
        if not name.startswith("seed_"):
            raise E.Refused(E.CAUSE_STATE, name)
        family = name[len("seed_"):]
        if family in R.XMM_NAMES:
            if family not in vector:
                vector.append(family)
            continue
        # THE TWO HALVES OF A VECTOR ARRIVAL (task ap3, fix 1).
        # `vector_arrivals_in_halves` has already rewritten the term, so
        # what is left to say is that each half takes a general
        # argument register like any other 64-bit value.  Admitted here
        # and NOT added to `GENERAL_FAMILIES`, which is
        # `canon.FAMILY_OF`'s own set of register families and stays
        # exactly that.
        if is_a_vector_half(family):
            if symbol.size() != VECTOR_HALF_BITS:
                raise E.Refused(E.CAUSE_STATE,
                                "%s is %d bits, and half a vector "
                                "arrival is %d"
                                % (name, symbol.size(),
                                   VECTOR_HALF_BITS))
            if family not in general:
                general.append(family)
            continue
        # AN x87 ARRIVAL (task ap3, fix 2): a position on the x87
        # register stack the model table preseeded, or a literal memory
        # operand read at the x87 sort and re-read under the `seed_`
        # spelling by `x87_as_arrivals`.  It is neither general nor
        # vector -- c holds it in a `long double` -- so it is kept in
        # its own list and appended after both, and nothing about the
        # existing two groups' positions moves.
        if E.is_an_x87_arrival(family):
            if symbol.sort() != R.X87_SORT:
                raise E.Refused(E.CAUSE_X87,
                                "%s is %s, and an x87 arrival is %s"
                                % (name, symbol.sort(), R.X87_SORT))
            if family not in x87:
                x87.append(family)
            continue
        # A MEMORY OPERAND IS AN ARRIVING VALUE (task ap2, fix 1).
        # `memory_as_arrivals` has already put the symbol at an
        # arrival's own width, so the only thing left to say is that it
        # takes a general argument register like any other value: it is
        # an integer the caller passes, not a register the machine
        # names.  It is admitted here and NOT added to
        # `GENERAL_FAMILIES`, which is `canon.FAMILY_OF`'s own set of
        # register families and stays exactly that.
        if name.startswith(MEMORY_PREFIX):
            if symbol.size() != MEMORY_ARRIVAL_BITS:
                raise E.Refused(E.CAUSE_STATE,
                                "%s is %d bits, and an arriving value "
                                "is %d" % (name, symbol.size(),
                                           MEMORY_ARRIVAL_BITS))
            if family not in general:
                general.append(family)
            continue
        if family not in GENERAL_FAMILIES:
            raise E.Refused(E.CAUSE_STATE, name)
        if family not in general:
            general.append(family)
    return general + vector + x87


def is_a_vector_half(family):
    """whether a family names one half of a vector arrival, which is a
    name `vector_arrivals_in_halves` writes and nothing else does."""
    for half in ("_low", "_high"):
        if not family.endswith(half):
            continue
        if family[:-len(half)] in R.XMM_NAMES:
            return True
    return False


def home_of(name):
    """the answer home a written place names: a register family, or
    the convention this task states for the flags."""
    if name.startswith("reg_"):
        return {"family": name[len("reg_"):],
                "source": "the place the reference's own builder wrote"}
    if E.is_an_x87_arrival(name):
        return {"family": "X87_0",
                "source": "THE CONVENTION (task ap3): a place on the "
                          "x87 register stack has no general register "
                          "home, and the c calling rule leaves a "
                          "`long double` answer in st(0), so the "
                          "rendered function answers there and the "
                          "return type is the 80-bit holder"}
    if name == "flags":
        return {"family": "rax",
                "source": "THE CONVENTION: the flags place has no "
                          "register home, so the rendered function "
                          "answers in the c and rust calling rule's own "
                          "answer register and the return type is the "
                          "term's own width"}
    return {"family": None, "source": "no register home"}


# ------------------------------------------------------------------
# step 2: the render
# ------------------------------------------------------------------

def render_one_place(place, lang, label, how=None, write=True):
    """the place's term written in the target's own operators by the
    existing renderer, unchanged.

    `how` names WHICH TERM the renderer is handed, and is the whole of
    fix 1: task h1 handed it `order_commutative(simplify(term))`, and
    task h2 hands it the term the pipeline's own normaliser leaves
    (`the_normalised_term`, section 2c).  It defaults to the running
    task; `sources_command` passes both, over the same places, to
    measure what the fix changed."""
    ordered = renderer_input(place["term"], how)
    families = place["families"]
    home = place["home"]
    if E.is_an_x87_arrival(home.get("family")):
        if lang not in TARGETS_WITH_AN_80_BIT_HOLDER:
            return {"rendered": False,
                    "refusal_cause": E.CAUSE_X87,
                    "refusal_detail": NO_80_BIT_HOLDER % lang}
        ordered = the_x87_value(ordered)
    renderer = renderer_for(lang, families, home["family"],
                            place["bits"], label)
    try:
        source, symbol = renderer.render(ordered, place["text"])
    except E.Refused as refusal:
        return {"rendered": False,
                "refusal_cause": refusal.cause,
                "refusal_detail": refusal.detail}
    folder = os.path.basename(SRC_DIR)
    if write:
        handle = open(os.path.join(SRC_DIR, label + suffix_of(lang)),
                      "w")
        handle.write(source)
        handle.close()
    return {"rendered": True,
            "renderer": renderer,
            "params": renderer.params,
            "source": source,
            "symbol": symbol,
            "renderer_input_text": T.one_line(ordered),
            "source_path": os.path.join(folder,
                                        label + suffix_of(lang))}


def renderer_for(lang, families, family, bits, label):
    """the ONE renderer of the target, each in its own sub-folder, each
    deriving from task o7's `emulate.Renderer`: c is that class itself,
    rust is task o11's, go and swift are task g1's, cpp is task ex1's
    (c's renderer with cpp's linkage and headers -- the two things
    measured to differ, `cpp/cpp_render.py`'s own header says how)."""
    if lang == "cpp":
        return CPR.CppRenderer(families, family, bits, label)
    if lang == "rust":
        return RR.RustRenderer(families, family, bits, label)
    if lang == "go":
        return GR.GoRenderer(families, family, bits, label)
    if lang == "swift":
        return SR.SwiftRenderer(families, family, bits, label)
    return E.Renderer(families, family, bits, label)


def suffix_of(lang):
    if lang == "cpp":
        return ".cpp"
    if lang == "rust":
        return ".rs"
    if lang == "go":
        return ".go"
    if lang == "swift":
        return ".swift"
    return ".c"


# ------------------------------------------------------------------
# step 3: compile at the ship flags, carve, and the landing
# ------------------------------------------------------------------

def compile_one_place(source, symbol, lang):
    """the corpus's own ship compile and carve for the target: clang
    `-std=c17 -O1 -c`, rustc `--emit=obj -C opt-level=1 -C
    debug-assertions=off`, a plain `go build` in a module directory, or
    `swiftc -O -c` -- each read off `lane_gen.py`'s own branch for that
    language.  Task ex1 adds cpp's, which is
    `clang++ -std=c++20 -O1 -c`, read off the same file's cpp branch."""
    if lang == "cpp":
        return CPR.compile_and_carve(source, symbol)
    if lang == "rust":
        return RR.compile_and_carve(source, symbol)
    if lang == "go":
        return GR.compile_and_carve(source, symbol)
    if lang == "swift":
        return SR.compile_and_carve(source, symbol)
    return E.compile_and_carve(source, symbol)


def expected_families(lang, params):
    """the register each declared parameter arrives in, under the
    TARGET's own calling rule.

    go's differs and nothing else's does: `canon37_gate.sequences_for`
    answers with the SysV sequence (`rdi rsi rdx rcx r8 r9`) for every
    language except go, whose own sequence is `rax rbx rcx rdi rsi r8`
    -- measured on this toolchain by task g1's probe
    `arrival_registers_six`."""
    for param in params:
        if param["bits"] != E.X87_BITS:
            continue
        # THE ARRIVAL CONTRACT, and it is the group awaiting the owner (task
        # ap3, fix 2).  The System V rule classes a `long double`
        # argument X87 and passes it IN MEMORY, on the stack -- the
        # carved body reads it with `fldt 0x8(%rsp)` -- so there is no
        # register family to put on an IN row, and
        # `pool100_entry_equivalence.input_rows` names families.  The
        # cell's own arrival is a position on the x87 register stack.
        # Naming either one a register would be INVENTING an arrival
        # contract, which is exactly the ruling task g1b asked for and
        # log_244's second awaiting-the owner item; so the gate declines and
        # says why.
        raise E.Refused(E.CAUSE_X87,
                        "the %s calling rule passes an 80-bit float "
                        "argument in memory, not in a register, so "
                        "this arrival has no register family to align "
                        "an IN row on" % lang)
    if lang == "go":
        return GR.expected_go_families(params)
    return E.expected_c_families(params)


def attested_of(held, found_row):
    """what task ap4's change 1 reads the relation between the two
    arrival contracts from, and it is three facts off objects that
    already exist: the cell's own triple, the cell's own line as the
    model table spells it, and the body of the corpus row the primitive
    lookup matched.  A term-route place is handed no body, because a
    term-route emulation is rendered FROM the cell's own families and
    the two contracts cannot differ in count."""
    held = held or {}
    return {
        "mnem": held.get("mnem"),
        "shape": held.get("shape"),
        "key_width": held.get("key_width"),
        "cell_line": held.get("line"),
        "body_text": (found_row or {}).get("body_text"),
    }


def landing_of(mnem, cell_mnem):
    """task o8's question: chaff-stripped by task o2's own narrow rule,
    is what remains exactly the cell's own arch opcode?

    AN EMPTY BODY IS THE IDENTITY (log 246): a body that carries no
    instruction at all is
    the IDENTITY, which is a LANDING and not a new outcome name -- the
    compiler emitted nothing because the value asked for is already in
    the register it answers in."""
    import single_opcode_units as SOU
    if the_body_is_empty(mnem):
        return {"stripped_text": "",
                "stripped_count": 0,
                "remaining": [],
                "verdict": "IDENTITY",
                "holds_the_cells_own_opcode": False}
    stripped = SOU.strip_chaff(mnem, "narrow")
    out = {"stripped_text": "; ".join(stripped),
           "stripped_count": len(stripped)}
    remaining = []
    for line in stripped:
        name, _operands = SOU.parse_insn(line)
        remaining.append({"mnem": name})
    out["remaining"] = remaining
    if len(stripped) != 1:
        out["verdict"] = "NOT_COLLAPSED"
        out["holds_the_cells_own_opcode"] = False
        for record in remaining:
            if record["mnem"] == cell_mnem:
                out["holds_the_cells_own_opcode"] = True
        return out
    landed, _operands = SOU.parse_insn(stripped[0])
    out["landed"] = {"mnem": landed}
    if landed == cell_mnem:
        out["verdict"] = "LANDED"
    else:
        out["verdict"] = "LANDED_ELSEWHERE"
    return out


# ------------------------------------------------------------------
# step 4: the check -- the cell's term against the carved body's term
# ------------------------------------------------------------------

# ==================================================================
# THE CONTRACT FOR A VALUE THAT IS NOT IN A FRESH REGISTER (log 246)
# ==================================================================
#
# the owner's ruling of 2026-09-09: "the contract may state a place by a
# CONSTRAINT, not only by a register name.  One extension, in the layer
# that owns each half."  Three changes carry it out and two of them are
# here, in the driver; the third is the ledger's x87 prelude and
# epilogue (`ledger.build_prelude` / `build_epilogue`).
#
#   CHANGE 1, `derived_arrivals`: where the cell reads a different
#   NUMBER of arrivals from the emulation, the two sides are not
#   aligned row by row.  The cell's arrivals are SUBSTITUTED by what
#   the emulation's own attested body leaves in them, read off the
#   reference simulator, and the REGION that substitution names is
#   recorded as a sentence on the run.
#
#   CHANGE 3, `the_identity`: an emulation whose carved body carries no
#   instruction at all is the identity on its arrival, so the
#   obligation is the cell's term against IN-0.  No new outcome name:
#   the gate's own words carry the verdict and `IDENTITY` is a landing,
#   like `LANDED`.
#
# A fourth thing this task changes is not a new rule but the driver's
# OWN rule reaching a name task ap2's halving introduced: a place named
# `flags.low` or `flags.high` is a half of the flags place, and the
# primitive route already refuses a flags place because an operator
# answers with the value it hands back and the flags are a second place
# the opcode writes (`CAUSE_PRIMITIVE_FLAGS`).  See
# `is_the_flags_place`.

RETURN_ONLY = frozenset(["ret", "retq", "repz", "endbr64", "nop",
                         "nopw", "nopl", "hlt"])
"""the mnemonics a carved body may hold and still carry no instruction
of its own (task ap4, change 3).

THIS IS NOT `strip_chaff`, deliberately.  Task o2's narrow rule counts
a register-to-register `mov` as chaff, so `mov %rdi,%rax; ret` strips
to nothing -- and that body is NOT empty: it moves an arrival into the
answer register, which is the identity in c's calling rule and is not
the identity in go's.  The test here is the literal one: the body
spells nothing but a return."""


def the_body_is_empty(mnem):
    """whether the carved body carries no instruction of its own."""
    for line in mnem:
        name = line.split()[0] if line.split() else ""
        if name.startswith("nop"):
            continue
        if name not in RETURN_ONLY:
            return False
    return True


def is_the_flags_place(writes):
    """whether a place name names the flags place or one half of it.

    Task ap2's fix 3 splits a 128-bit place into `<name>.low` and
    `<name>.high`, and the primitive route's own refusal tested the
    whole name against `"flags"`, so the two halves of a 64-bit
    comparison's flags place slipped past it and were put to the gate
    against the operator's answer.  What they then said -- `the IN rows
    cannot be aligned` -- is true about the two row lists and false
    about the objects: the emulation has no answer for a flags place at
    all, which is what the refusal already says."""
    if not writes:
        return False
    return writes.split(".")[0] == "flags"


def the_identity(shared, place, params, lang, out):
    """CHANGE 3: the emulation whose carved body carries no instruction.

    The compiler emitted nothing because the value it was asked for is
    already in the register it answers in, so the emulation IS the
    identity on its arrival and the obligation is the cell's term
    against IN-0.  The arrival is read off the emulation's own
    parameter plan through the target's calling rule, exactly as every
    other run reads it; where that plan names anything but ONE arrival
    the place is refused with the count, because which of two arrivals
    an empty body answers with cannot be read off nothing."""
    import pool100_entry_equivalence as P100
    out["route"]["body"] = ("the carved body carries no instruction, "
                            "so the emulation is the identity on its "
                            "arrival")
    out["route"]["cell"] = ("the cell's own term, as the model table "
                            "holds it")
    out["identity"] = True
    try:
        body_families = expected_families(lang, params)
    except E.Refused as refusal:
        out["outcome"] = "UNDECIDED"
        out["reason"] = "%s: %s" % (refusal.cause, refusal.detail)
        return out
    if len(body_families) != 1:
        out["outcome"] = "UNDECIDED"
        out["reason"] = ("the carved body carries no instruction and "
                         "its arrival contract names %d IN rows, so "
                         "which arrival it answers with cannot be read"
                         % len(body_families))
        return out
    cell_families = place["families"]
    cell_rows = P100.input_rows(cell_families)
    body_rows = P100.input_rows(body_families)
    disagreement = P100.rows_disagree(cell_rows, body_rows)
    if disagreement is not None:
        out["outcome"] = "UNDECIDED"
        out["reason"] = "the IN rows cannot be aligned: %s" % disagreement
        return out
    body_term = z3.BitVec("seed_%s" % body_families[0],
                          body_rows[0]["bits"])
    out["aligned_rows"] = [{
        "row": "IN-0",
        "the cell reads": cell_families[0],
        "the body reads": body_families[0],
    }]
    cell_aligned = P100.align_by_row(place["term"], cell_rows)
    body_aligned = P100.align_by_row(body_term, body_rows)
    out["cell_bits"] = cell_aligned.size()
    out["body_bits"] = body_aligned.size()
    out.update(decided(shared, cell_aligned, body_aligned, params))
    return out


SETUP_RELATIONS = ("the same value", "the sign spread of")
"""the two relations task ap4's change 1 states a REGION with, and both
are read from the reference simulator's own tables rather than named
here: `reference.SPREAD_SIGN` (`cltd`, `cqto`, `cqo`, `cwtd`) and
`reference.ACCUMULATOR_WIDEN` (`cbtw`, `cwtl`, `cltq`) are the
zero-operand setup instructions the corpus produces a derived arrival
with, and equality is what a `gpr_same` operand form binds."""


def derived_arrivals(place, attested, body_families, lang):
    """CHANGE 1: the cell's arrivals written over the EMULATION's.

    THE DEFECT.  The gate aligns two arrival contracts position by
    position and declines when they name different numbers of IN rows
    (`the IN rows cannot be aligned: ... name 3 and 2 IN rows`).  On the
    primitive route the two contracts are different things: the cell's
    arrivals are the registers its own opcode reads, and the
    emulation's are the registers its own parameters arrive in.  A
    corpus body reaches the opcode by putting values in those registers
    first -- `mov %rdi,%rax; cqto; idiv %rsi` -- so an arrival of the
    cell can be a FUNCTION of an arrival of the emulation, or the same
    one twice, or absent.

    THE FIX, and the relation is READ and never named here.  The
    reference simulator steps the emulation's own attested body, on a
    state whose registers are free symbols, up to the line that
    classifies to this cell; what it leaves in each register at that
    moment is what that register holds when the opcode runs.  The
    cell's own operand registers are matched to the body's positionally
    -- position k of the cell's line against position k of the body's
    -- and every other family the cell reads is matched by its own
    name, which is what an implicit register (the accumulator and its
    high half) is.

    Returns a dict with `term` (the cell's term over the emulation's
    arrivals), `region` (the sentence), `substitution` (what each of
    the cell's IN rows became) and `free` (any symbol left over); or a
    dict with `refusal`, naming the arrival it could not place."""
    body_text = (attested or {}).get("body_text")
    cell_line = (attested or {}).get("cell_line")
    cell_families = list(place.get("families") or [])
    if body_text is None:
        return {"refusal": ("the emulation is not a matched corpus "
                            "row, so there is no attested body to "
                            "read the relation between the two "
                            "arrival contracts from")}
    lines = split_body(body_text)
    at = the_cells_own_line(lines, attested)
    if at is None:
        return {"refusal": ("the cell's own instruction is not in the "
                            "matched corpus row's body, so what the "
                            "body leaves in the cell's arrival "
                            "registers cannot be read")}
    state = R.MachineState()
    for line in lines[:at]:
        try:
            R.REFERENCE.step(state, line)
        except Exception as problem:
            return {"refusal": ("the reference stopped on %r of the "
                                "matched corpus row's body (%s: %s), "
                                "so what it leaves in the cell's "
                                "arrival registers cannot be read"
                                % (line, type(problem).__name__,
                                   problem))}
    by_position = operand_families(SOU.parse_insn(lines[at])[1])
    cell_positions = operand_families(SOU.parse_insn(cell_line)[1]
                                      if cell_line else [])
    substitution = []
    record = []
    for index, family in enumerate(cell_families):
        wanted = family
        at_position = None
        for position, named in enumerate(cell_positions):
            if named == family:
                at_position = position
                break
        if at_position is not None:
            if at_position >= len(by_position) or \
                    by_position[at_position] is None:
                return {"refusal": ("the cell reads %s at operand "
                                    "position %d and the matched body "
                                    "names no register there, so the "
                                    "two cannot be matched"
                                    % (family, at_position))}
            wanted = by_position[at_position]
        term = state.registers.get(wanted)
        if term is None:
            term = state.family_value(wanted)
        seed = z3.BitVec("seed_%s" % family, term.size())
        substitution.append((seed, term))
        record.append({"row": "IN-%d" % index,
                       "the cell reads": family,
                       "becomes": T.one_line(term)})
    substituted = place["term"]
    if substitution:
        substituted = z3.substitute(substituted, *substitution)
    free = []
    for symbol in z3.z3util.get_vars(substituted):
        name = symbol.decl().name()
        if not name.startswith("seed_"):
            free.append(name)
            continue
        if name[len("seed_"):] not in body_families:
            free.append(name)
    return {"term": substituted,
            "substitution": record,
            "free": sorted(set(free)),
            "region": the_region(cell_families, substitution,
                                 (attested or {}).get("key_width"))}


def operand_families(operands):
    """the register family each operand position names, or None where
    the operand is not a register."""
    out = []
    for operand in (operands or []):
        if not operand.startswith("%"):
            out.append(None)
            continue
        out.append(canon.FAMILY_OF.get(operand[1:]))
    return out


def split_body(body_text):
    if isinstance(body_text, str):
        raw = body_text.split("; ")
    else:
        raw = list(body_text)
    out = []
    for line in raw:
        line = line.split("!!")[0].strip()
        if line:
            out.append(line)
    return out


def the_cells_own_line(lines, attested):
    """the index of the line of the attested body that classifies to
    this cell, by the model table's own classifier."""
    mnem = (attested or {}).get("mnem")
    shape = (attested or {}).get("shape")
    key_width = (attested or {}).get("key_width")
    for index, line in enumerate(lines):
        name, _operands = SOU.parse_insn(line)
        if name is None:
            continue
        if name != mnem:
            continue
        got_shape, got_width, _cause = MTAB.classify_line(name, line, 0)
        if got_shape == shape and got_width == key_width:
            return index
    return None


def the_region(cell_families, substitution, key_width):
    """THE REGION, as a sentence, in the CELL's own IN-row numbering.

    The substitution says what each of the cell's arrivals becomes over
    the emulation's; the region is what that makes TRUE between two of
    the cell's own rows, and it is asked of z3 rather than asserted.
    Two relations are tested, and both are the ones the corpus's own
    setup produces: a row that is the SAME VALUE as another (`xor
    %eax,%eax` and the other `gpr_same` forms bind both operands to one
    arrival), and a row that is the SIGN SPREAD of another (`cltd` and
    `cqto` fill the high half of the dividend with the low half's sign).
    A row no relation holds of is named as free."""
    became = {}
    for index, family in enumerate(cell_families):
        became[index] = substitution[index][1]
    said = []
    for index in sorted(became):
        for other in sorted(became):
            if other == index:
                continue
            if other < index:
                if proved_equal(became[index], became[other]):
                    said.append("IN-%d = IN-%d" % (index, other))
                    break
            spread = the_sign_spread(became[other], key_width)
            if spread is None:
                continue
            if proved_equal(became[index], spread):
                said.append("IN-%d = SignExt(IN-%d)" % (index, other))
                break
    if not said:
        return ("no constraint: every one of the cell's IN rows is "
                "free over the emulation's own arrivals")
    return "on the region %s" % ", ".join(said)


def proved_equal(left, right):
    """z3 asked whether two terms are the same function of their free
    symbols.  A relation this task PRINTS is a relation z3 proved."""
    if left.size() != right.size():
        return False
    solver = z3.Solver()
    solver.set("timeout", 3000)
    solver.add(left != right)
    return solver.check() == z3.unsat


def the_sign_spread(term, key_width):
    """the term one of `reference.SPREAD_SIGN`'s instructions leaves in
    the data register: the low `key_width` bits are every bit set to the
    sign bit of the source's low `key_width` bits, and the rest of the
    register is untouched -- which for a fresh 32-bit `cltd` is zero.

    Written once, here, and compared against the reference's own result
    by z3 rather than trusted: `the_region` prints a relation only when
    `proved_equal` proves it."""
    if key_width is None:
        return None
    width = min(key_width, term.size())
    if width < 1:
        return None
    sign = z3.Extract(width - 1, width - 1, term)
    spread = z3.SignExt(width - 1, sign)
    if width < term.size():
        spread = z3.ZeroExt(term.size() - width, spread)
    if spread.size() != term.size():
        return None
    return z3.simplify(spread)


X87_STACK_SLOT = re.compile(r"^x87_0x([0-9a-f]+)_rsp_$")
"""the reference's own symbol for an x87 value a body loads off the
machine stack: `reference.x87_symbol` mangles the operand text, so
`fldt 0x18(%rsp)` reads `x87_0x18_rsp_`.  The number in the middle is
the displacement the body itself spells."""


def x87_arrivals(families):
    """whether every arrival of a place is a value on the x87 stack.

    All or none, and the objects say why: the two x87 cell shapes are
    `st_st` (both operands on the stack) and `mem_one` (one on the
    stack, one a literal memory operand read at the x87 sort, which
    `x87_as_arrivals` re-reads as an arrival of the same sort).  A place
    that mixes an x87 arrival with a bitvector one is refused here
    rather than half-aligned."""
    if not families:
        return False
    for family in families:
        if not E.is_an_x87_arrival(family):
            return False
    return True


def x87_aligned(shared, place, params, body_term, out):
    """CHANGE 2's DRIVER HALF: the two sides put on one set of IN rows
    when the arrivals are values on the x87 register stack.

    THE CORRESPONDENCE IS READ OFF THE OBJECTS AND NOTHING ELSE.
      * The CELL's k-th IN row is `params[k]["family"]` -- the family
        the renderer gave parameter k, which is the plan the rendered
        source itself was written from.
      * The EMULATION's k-th IN row is the x87 value its body loads
        from the k-th `long double` argument slot.  The System V rule
        passes such an argument IN MEMORY on the machine stack, the
        body spells that address itself (`fldt 0x8(%rsp)`), and the
        reference names the value it loads after that same address, so
        the row order is the ASCENDING displacement.
    Anything that does not line up -- a count that differs, a symbol
    whose name carries no displacement, a sort that is not the x87
    sort -- is a refusal by name and never a guess."""
    wanted = []
    for param in params:
        family = param.get("family")
        if not E.is_an_x87_arrival(family):
            out["outcome"] = "UNDECIDED"
            out["reason"] = ("the cell's arrivals are values on the "
                             "x87 stack and the emulation's parameter "
                             "%r is %r, so the two contracts name "
                             "different kinds of arrival"
                             % (param.get("name"), family))
            return out
        wanted.append(family)
    slots = []
    for symbol in z3.z3util.get_vars(body_term):
        name = symbol.decl().name()
        hit = X87_STACK_SLOT.match(name)
        if hit is None:
            out["outcome"] = "UNDECIDED"
            out["reason"] = ("the emulation's answer reads %r, which "
                             "is not a value loaded from an argument "
                             "slot of the machine stack, so it cannot "
                             "be put on an IN row" % name)
            return out
        if symbol.sort() != R.X87_SORT:
            out["outcome"] = "UNDECIDED"
            out["reason"] = ("the emulation's answer reads %r at %s, "
                             "and an x87 arrival is %s"
                             % (name, symbol.sort(), R.X87_SORT))
            return out
        slots.append((int(hit.group(1), 16), symbol))
    # THE ORDER IS THE DESCENDING DISPLACEMENT, and it is a MEASURED
    # fact of this toolchain rather than a reading of the System V
    # document: lane `ap4_l9` compiled `a - b` and `b - a` at the
    # corpus's own ship flags and read the two bodies.  `a - b` carves
    # to `fldt 0x18(%rsp); fldt 0x8(%rsp); fsubp %st,%st(1)` and
    # `b - a` to the same two loads in the other order, so under the
    # reference's own model of `fsubp` the FIRST `long double`
    # argument is the one at the HIGHER displacement.  Both sides of
    # this comparison are read by that same reference, so the
    # correspondence is the one the two objects share.
    slots.sort(reverse=True)
    if len(slots) != len(wanted):
        out["outcome"] = "UNDECIDED"
        out["reason"] = ("the cell reads %d arrival(s) on the x87 "
                         "stack and the emulation's answer reads %d "
                         "argument slot(s), so the IN rows cannot be "
                         "aligned" % (len(wanted), len(slots)))
        return out
    # THE CELL SIDE IS THE SHARED ALIGNER'S, task ap5.  Task ap4 built
    # both sides here, because `pool100_entry_equivalence.align_by_row`
    # substituted a BITVECTOR `seed_<family>` per IN row and an x87
    # arrival is an FP value at `reference.X87_SORT`, so the shared
    # aligner silently substituted nothing.  Task ap5's brief names
    # that function: it now aligns an x87 arrival by its IN row like
    # any other, so the cell's side of this comparison is put on the
    # rows by the same call every other place uses.  What stays here
    # is the EMULATION's side, which is not a shared reading at all:
    # its arrivals are named after the machine-stack slots the body
    # itself loads them from, which is c's calling rule for a
    # `long double` argument and is the driver's own business.
    import pool100_entry_equivalence as P100
    out["aligned_rows"] = []
    body_substitution = []
    for index, family in enumerate(wanted):
        common = z3.Const("IN_%d" % index, R.X87_SORT)
        body_substitution.append((slots[index][1], common))
        out["aligned_rows"].append({
            "row": "IN-%d" % index,
            "the cell reads": family,
            "the body reads": "%s, the argument slot at 0x%x(%%rsp)"
                              % (slots[index][1].decl().name(),
                                 slots[index][0]),
        })
    cell_aligned = P100.align_by_row(place["term"],
                                     P100.input_rows(wanted))
    body_aligned = z3.substitute(body_term, *body_substitution)
    out["cell_bits"] = cell_aligned.size()
    out["body_bits"] = body_aligned.size()
    out["x87_rows"] = ("the arrival contract is stated by the argument "
                       "slots the body itself spells, and not by a "
                       "register family, which is the ruling of "
                       "2026-09-09; the cell's side of it is put on "
                       "those rows by the shared aligner "
                       "pool100_entry_equivalence.align_by_row, which "
                       "task ap5 taught to align an x87 arrival")
    out.update(decided(shared, cell_aligned, body_aligned, params))
    return out


def check_one_place(shared, place, params, raw_bytes, mnem, label,
                    lang, attested=None):
    """z3 asked whether the carved body answers as the cell's term says,
    for every input, at the gate's own 3,000 ms ceiling.

    The body is put on the canonical form and answered by the reference
    simulator (`reference.answer_for_unit`), which is route one of the
    pipeline's own walk; where the reference refuses the body, its
    transcribed term stands in and the record says so.  The two sides
    are aligned by IN row: the cell's arrival families in the order
    `families_of` states, the body's in the order the target's calling
    rule fills."""
    import pool100_entry_equivalence as P100
    out = {"route": {}}
    if the_body_is_empty(mnem):
        # CHANGE 3 (task ap4).  Asked BEFORE the canonical form, because
        # a body with no instruction has nothing for the form to wrap
        # and the reference says so by name ("this unit's body has no
        # instruction line").  What the compiler did is not a failure:
        # it emitted nothing because the value asked for is already in
        # the register it answers in.
        return the_identity(shared, place, params, lang, out)
    canon = wrapped_body(shared, raw_bytes, mnem, label, lang)
    out["canon40_outcome"] = canon.get("outcome")
    out["arrival_families_read_off_the_body"] = canon.get(
        "arrival_families")
    body_term, cause = E.body_answer(shared["reference"], canon)
    if body_term is None:
        walked = shared["maker"].transcribe(canon)
        if walked.out_term is None:
            out["outcome"] = "UNDECIDED"
            out["reason"] = ("the carved body: %s; and no term either"
                             % cause)
            return out
        body_term = walked.out_term
        out["route"]["body"] = ("its transcribed term (the reference "
                                "refused: %s)" % cause)
    else:
        out["route"]["body"] = "the reference's answer for the carved body"
    out["route"]["cell"] = "the cell's own term, as the model table holds it"
    cell_term = place["term"]
    cell_families = place["families"]
    if x87_arrivals(cell_families):
        # CHANGE 2's DRIVER HALF (task ap4): an arrival that is a value
        # on the x87 stack is an FP value at `reference.X87_SORT`, and
        # `P100.align_by_row` substitutes a BITVECTOR for each IN row,
        # so the shared aligner has nothing to substitute.  The rows are
        # built in `x87_aligned` instead, off the emulation's own
        # parameter plan and its own stack displacements.  It is asked
        # BEFORE `expected_families`, whose own refusal is that an
        # 80-bit float argument arrives in memory and names no register
        # family -- which is exactly what this branch answers.
        return x87_aligned(shared, place, params, body_term, out)
    try:
        body_families = expected_families(lang, params)
    except E.Refused as refusal:
        out["outcome"] = "UNDECIDED"
        out["reason"] = "%s: %s" % (refusal.cause, refusal.detail)
        return out
    cell_rows = P100.input_rows(cell_families)
    body_rows = P100.input_rows(body_families)
    disagreement = P100.rows_disagree(cell_rows, body_rows)
    if disagreement is not None:
        # CHANGE 1 (task ap4): the two contracts name different numbers
        # of IN rows, so they are not aligned row by row -- the cell's
        # arrivals are substituted by what the emulation's own attested
        # body leaves in them, and the REGION that names is recorded.
        derived = derived_arrivals(place, attested, body_families, lang)
        if derived.get("refusal") is not None:
            out["outcome"] = "UNDECIDED"
            out["reason"] = ("the IN rows cannot be aligned: %s; and "
                             "%s" % (disagreement, derived["refusal"]))
            return out
        out["region"] = derived["region"]
        out["substitution"] = derived["substitution"]
        out["substituted_because"] = ("the IN rows cannot be aligned: "
                                      "%s" % disagreement)
        if derived["free"]:
            out["cell_side_free_state"] = derived["free"]
        cell_term = derived["term"]
        cell_families = list(body_families)
        cell_rows = P100.input_rows(cell_families)
    out["aligned_rows"] = []
    for index in range(len(cell_families)):
        out["aligned_rows"].append({
            "row": "IN-%d" % index,
            "the cell reads": cell_families[index],
            "the body reads": body_families[index],
        })
    _in, shared_body, constants_body, other_body = P100.classify_symbols(
        body_term, body_families)
    body_term, names_body = P100.rename_constants_apart(
        body_term, constants_body, "body")
    out["body_side_free_state"] = shared_body + other_body + names_body
    cell_aligned = P100.align_by_row(cell_term, cell_rows)
    body_aligned = P100.align_by_row(body_term, body_rows)
    out["cell_bits"] = cell_aligned.size()
    out["body_bits"] = body_aligned.size()
    if out["cell_bits"] != out["body_bits"]:
        # `gate.Gate.decide` cuts both sides to the narrower width, which
        # is its own stated rule; the two widths are recorded here so a
        # proof over the low bits is never read as a proof over the whole
        # place.
        out["width_note"] = ("the cell's place is %d bits and the "
                             "carved body answers %d, so the gate's own "
                             "rule cut both to %d"
                             % (out["cell_bits"], out["body_bits"],
                                min(out["cell_bits"], out["body_bits"])))
    out.update(decided(shared, cell_aligned, body_aligned, params))
    return out


def wrapped_body(shared, raw_bytes, mnem, label, lang):
    """the carved body on the canonical form, the pipeline's own way."""
    import canonical_form as CF
    unit = "%s/%s" % (lang, label)
    if lang == "cpp":
        recorded = CPR.recorded_facts(unit, label, raw_bytes, mnem)
    elif lang == "rust":
        recorded = RR.recorded_facts(unit, label, raw_bytes, mnem)
    elif lang == "go":
        recorded = GR.recorded_facts(unit, label, raw_bytes, mnem)
    elif lang == "swift":
        recorded = SR.recorded_facts(unit, label, raw_bytes, mnem)
    else:
        recorded = E.recorded_facts(unit, label, raw_bytes, mnem)
    canon = CF.render_one(shared["form"], shared["gate"], recorded)
    canon["unit"] = "%s/%s" % (lang, label)
    canon["arrival_families"] = recorded["arrival_families"]
    return canon


def decided(shared, cell_aligned, body_aligned, params):
    """the gate's own call, and o7's caller-extension re-pose.

    RESTATED, NOT CALLED, and the docstring at the top of this file
    says why: `emulate.prove_against_x` takes an x unit, and a table
    cell has none.  The obligation, the objects and the substitution
    are the same."""
    import gate as G
    gate = shared["gate"]
    out = {}
    if not gate.comparable(body_aligned, cell_aligned):
        out["outcome"] = "UNDECIDED"
        out["reason"] = ("the two terms are of different z3 sorts (%s "
                         "against %s)" % (body_aligned.sort(),
                                          cell_aligned.sort()))
        return out
    verdict = gate.decide(
        body_aligned, cell_aligned,
        "the carved body's answer against the cell's own term, inputs "
        "aligned by IN row",
        "z3 proved the carved body's answer equal to the cell's term "
        "for every value of every aligned input row")
    out["outcome"] = verdict.outcome
    out["reason"] = verdict.reason
    out["solver_timeout_ms"] = verdict.solver_timeout_ms
    if verdict.counterexample is not None:
        out["counterexample"] = verdict.counterexample
    if verdict.outcome != G.DISPROVED:
        return out
    narrow = []
    substitution = []
    for index, param in enumerate(params):
        if param["kind"] != "bv":
            continue
        if param["bits"] >= 32:
            continue
        row = z3.BitVec("IN_%d" % index, 64)
        narrow.append({"row": "IN-%d" % index,
                       "holder": param["holder"]})
        substitution.append((row, z3.ZeroExt(64 - param["bits"],
                                             z3.Extract(param["bits"] - 1,
                                                        0, row))))
    if not substitution:
        return out
    again = gate.decide(
        z3.substitute(body_aligned, *substitution),
        z3.substitute(cell_aligned, *substitution),
        "the same, with every narrow-holder input row zero-extended "
        "from its holder width (the target's caller-extension rule)",
        "z3 proved the two equal for every input whose narrow "
        "arguments are zero-extended to the register")
    out["under_caller_extension"] = {
        "narrow_rows": narrow,
        "outcome": again.outcome,
        "reason": again.reason,
        "counterexample": again.counterexample,
    }
    return out


# ==================================================================
# section 2c: task h2 -- THE TWO PRINTING FIXES
# ==================================================================
#
# WHAT THIS SECTION IS, one sentence each, in relation.
#   * FIX 1, `the_normalised_term`: the term the renderer is handed is
#     the one the pipeline's own normaliser leaves, rather than the
#     `order_commutative(simplify(term))` task h1 handed it -- so the
#     source the renderer writes is a rendering of the SAME text the
#     model table prints, not of a differently-shaped term with the
#     same meaning.
#   * FIX 2, `projected_lane`: a vector cell's place is the whole
#     128-bit register -- the lane the operation writes, joined under
#     the arrival bits it leaves alone -- so the driver projects the
#     lane out of the place's term and renders THAT, and records what
#     the bits above the lane are.
# Neither renderer is touched by either fix: both are changes to what
# the driver hands the existing renderer.

NORMALISE_BEFORE_RENDER = True
"""whether the renderer is handed the term the pipeline's own
normaliser leaves (task h2's fix 1) or the form task h1 handed it.

ON, which is where task ap2 left it; task ap3 turns it off for ONE
measurement lane and turns it back on.  It is a module-level switch and
NOT a gate on a task name, because a task-name gate is what let this
fix fall out from under three tasks in the first place."""

CAUSE_LANE_IS_THE_PLACE = "the cell's own key_width is not narrower " \
                          "than the place, so there is no lane to " \
                          "project"


THE_SIMPLIFIED_FORM = "order_commutative(simplify(term))"
"""the OTHER form of a term, named by what it is.  It is the form the
renderer was handed before the normaliser's own output replaced it, and
a caller names it to measure the difference; nothing in the route asks
for it."""


def renderer_input(term, how=None):
    """the term the renderer is handed.

    THE NORMALISED TERM IS WHAT THE RENDERER WALKS, for every run.
    It was once written as `how in ("h2", "g1")`, so every pass after
    that silently fell through to the older form -- the one defect the
    driver's first full loop found by reading this file rather than by
    running it (log 243 section 11, item 3).  The normalised term is
    what the model table PRINTS, so it is what the renderer should
    walk, and there is no run for which that is not so.

    THE OTHER FORM HAS A NAME OF ITS OWN, and it is not a task label:
    `THE_SIMPLIFIED_FORM` is `order_commutative(simplify(term))`, which
    the closed tasks' own products are a rendering of.  A caller that
    wants to MEASURE what the two forms differ by passes that constant
    explicitly, over the same places; every call the route makes passes
    nothing and gets the normalised term."""
    if how == THE_SIMPLIFIED_FORM:
        return T.order_commutative(z3.simplify(term))
    if not NORMALISE_BEFORE_RENDER:
        # THE SWITCH, and it is the ONLY thing it does (task ap3, fix
        # 4).  Task h2's fix 1 was measured on 24 places and then moved
        # into task ap2 alongside five other fixes, so what it does at
        # the scale of a thousand runs has never been measured on its
        # own (log_244 section 6, item 4 of its awaiting-the owner list).
        # `autopoly3.py` runs the whole loop once with this False and
        # once True, all else as task ap2 left it, and reports the runs
        # whose rendered source differs and whose verdict differs.  The
        # form it falls back to is task h1's own, which is what every
        # task from `g1b` to task ap1 silently ran.
        return T.order_commutative(z3.simplify(term))
    return the_normalised_term(term)


def the_normalised_term(term):
    """the pipeline's own normaliser applied to the TERM, so the
    renderer walks the term whose text the model table prints.

    RESTATED, NOT CALLED, and said out loud as the law requires, exactly
    as this file already says of `emulate.prove_against_x`.
    `term.Term.normalize` ends by PRINTING its result (`term.one_line`),
    so it hands back TEXT and the renderer walks a z3 term.  The steps
    here are that function's own steps, in its own order, through its
    own module-level functions -- `term.order_commutative`,
    `z3.simplify`, `term.order_commutative`, the positional renaming of
    the free symbols, `z3.simplify`, `term.order_commutative` -- and the
    one thing that differs is why the text is the same: `normalize`
    LEAVES the free symbols renamed `v0`, `v1`, ..., and the renderer
    keys every arrival on its own `seed_<family>` name, so the renaming
    is applied and then UNDONE.  The renaming is a bijection over the
    term's own free symbols, so undoing it changes names and nothing
    else.

    THE GUARD, run in this task's own lane and never asserted here:
    `Term.normalize` over the term this function returns prints
    character-for-character what it prints over the term handed in."""
    ordered = T.order_commutative(term)
    ordered = z3.simplify(ordered)
    ordered = T.order_commutative(ordered)
    symbols = T.ordered_symbols(ordered)
    forward = []
    backward = []
    for index, symbol in enumerate(symbols):
        if symbol.sort().kind() == z3.Z3_BV_SORT:
            fresh = z3.BitVec("v%d" % index, symbol.size())
        else:
            fresh = z3.Const("v%d" % index, symbol.sort())
        forward.append((symbol, fresh))
        backward.append((fresh, symbol))
    if forward:
        ordered = z3.substitute(ordered, *forward)
    ordered = z3.simplify(ordered)
    ordered = T.order_commutative(ordered)
    if backward:
        ordered = z3.substitute(ordered, *backward)
    return ordered


TARGETS_WITH_AN_80_BIT_HOLDER = ("c", "cpp")
"""the targets whose own type system has a holder for the x87 extended
format (task ap3, fix 2).

c has `long double`, and the probe of lane `ap3_l2` is what says so
rather than a reading of a manual: a `long double` add at the corpus's
own ship flags carves to `fldt 0x18(%rsp); fldt 0x8(%rsp);
faddp %st,%st(1); ret`.  rust, go and swift have no 80-bit floating
holder at all -- `f64` / `float64` / `Double` are the widest each
spells -- so their rows are refused BY NATURE and not by a defect.

cpp is the other target the brief names and it is NOT in this loop's
four; adding a fifth target changes what `proved on all four` counts,
which is a structural change and not this task's to make.  It is on the
awaiting-the owner list of log 245."""

NO_80_BIT_HOLDER = ("%s has no 80-bit holder, so an x87 place cannot "
                    "be answered in it")


def the_x87_value(term):
    """the FLOAT under a place's own `fp.to_ieee_bv`, which is what the
    renderer walks for an x87 place (task ap3, fix 2).

    THE SEAM THIS AVOIDS CROSSING, and it is why this is one line in the
    driver rather than a helper in the renderer.  An x87 place's term
    is `fp.to_ieee_bv(<the float the opcode computed>)`, 79 bits as z3
    spells it; the same value in memory is 80 bits, the extra one being
    the explicit integer bit x87 stores and z3 does not.  A renderer
    reaching `fp.to_ieee_bv` writes a `memcpy` helper, and at this
    width that helper would be a DIFFERENT FUNCTION from the node it
    stands for.  So the driver hands the renderer the float itself, and
    the rendered function answers a `long double` in st(0) -- which is
    where the c calling rule leaves it, and where the carved body's own
    answer is read from, so the gate still compares the place's own
    79-bit term against the body's.

    This is the x87 counterpart of task h2's `projected_lane`: the
    driver chooses which term the existing renderer walks and no
    renderer is taught anything new.  A term that is not that shape is
    returned untouched, and the renderer refuses it by cause."""
    if not z3.is_app(term):
        return term
    if term.decl().kind() != z3.Z3_OP_FPA_TO_IEEE_BV:
        return term
    return term.arg(0)


def projected_lane(shared, place, key_width):
    """FIX 2: the lane of a vector place, projected in the driver.

    A cell whose place is an xmm register carries the whole 128-bit
    place in its term, and the cell's own `key_width` (32 for `addss`,
    64 for `cvtsi2sd`) names the lane the operation writes.  This
    function returns the same place with its term projected to
    `Extract(key_width - 1, 0, place)`, its width the lane's width -- so
    the renderer plans a `key_width`-wide float or integer holder for
    the answer by its own rule -- and a `lane` record saying what the
    bits above the lane are.

    WHAT THE UPPER LANES ARE IS MEASURED, not asserted: the term above
    the lane is put to the gate against the same bits of the arrival
    that lives in the place's own register, and the gate's own word for
    that obligation is what the record carries.

    `None` where the place is not a vector place, so no other run is
    touched by this fix."""
    home = place.get("home") or {}
    family = home.get("family")
    if family is None:
        return None
    if family not in R.XMM_NAMES:
        return None
    term = place["term"]
    if key_width is None or key_width >= term.size():
        return {"lane": {"of_bits": term.size(), "lane_bits": key_width},
                "refusal_cause": CAUSE_LANE_IS_THE_PLACE,
                "refusal_detail": "key_width %s, place %d bits"
                                  % (key_width, term.size())}
    holder = T.Term()
    low = z3.simplify(z3.Extract(key_width - 1, 0, term))
    high = z3.simplify(z3.Extract(term.size() - 1, key_width, term))
    lane = {
        "of_bits": term.size(),
        "lane_bits": key_width,
        "projection": "Extract(%d, 0, the cell's own term for this "
                      "place)" % (key_width - 1),
        "lane_text": holder.normalize(low),
        "above_the_lane_text": holder.normalize(high),
    }
    lane["above_the_lane"] = pass_through_verdict(shared, high, family,
                                                  key_width,
                                                  term.size())
    record = dict(place)
    record["term"] = low
    record["bits"] = key_width
    record["text"] = lane["lane_text"]
    record["sexpr"] = low.sexpr()
    try:
        record["families"] = families_of(low)
    except E.Refused as refusal:
        return {"lane": lane,
                "refusal_cause": refusal.cause,
                "refusal_detail": refusal.detail}
    return {"lane": lane, "place": record}


def pass_through_verdict(shared, high, family, key_width, bits):
    """the gate asked whether the bits above the lane are the arrival's
    own bits, passed through: `high` against
    `Extract(bits - 1, key_width, seed_<the place's own register>)`."""
    arrival = z3.BitVec("seed_%s" % family, bits)
    expected = z3.Extract(bits - 1, key_width, arrival)
    verdict = shared["gate"].decide(
        high, expected,
        "the bits of the place above the lane, against the same bits of "
        "the arrival in that register",
        "z3 proved the bits above the lane are the arrival's own bits, "
        "passed through")
    out = {
        "expected": "Extract(%d, %d, seed_%s)" % (bits - 1, key_width,
                                                  family),
        "outcome": verdict.outcome,
        "reason": verdict.reason,
    }
    if verdict.counterexample is not None:
        out["counterexample"] = verdict.counterexample
    return out


# ==================================================================
# section 2d: task g1 -- THE PRIMITIVE ROUTE, tried before the term
# ==================================================================
#
# WHAT THIS SECTION IS, one sentence, in relation.  the owner's model of an
# arch opcode (the arch_unit_oracle CORE's "goal", 2026-09-08) is a
# PRIMITIVE plus its EDGE REGIONS, so `find_emulation(cell, lang)` asks
# first whether `lang` has an OPERATOR whose whole lowered body IS this
# cell -- and where it does, renders that operator on holders of the
# operand types the corpus recorded for it, and nothing else.  The term
# route (section 2, tasks h1 and h2) is the fallback where it does not.
#
# WHERE THE ANSWER COMES FROM, and why it is machine form.  Task o2's
# own artifact `single_opcode_units.json` holds, per language, the units
# whose body with task o2's narrow chaff rule applied is exactly ONE
# instruction, grouped by (mnemonic, distinct machine body bytes).  This
# section re-derives that strip rather than trusting it, classifies the
# one instruction with task m1b's own classifier, and matches the
# resulting (`mnem`, shape, `key_width`) triple against the cell's --
# which the ruling of 2026-09-08 states IS the machine-form key.  The
# OPERATOR TOKEN is read from the chosen row's member afterwards, as the
# display label it is, to reach that member's own probe in the
# language's manifest; it selects nothing, keys nothing, and pairs
# nothing.  Where two rows classify to the same cell the choice is the
# corpus's own attestation -- the row with the most members -- and the
# row's own body text breaks a tie.
#
# WHAT IS RENDERED.  The member's own probe SOURCE, from
# `probe_manifest_<lang>.json`, with its symbol renamed to this run's
# label and nothing else changed: the operator on holders of the types
# the manifest records (`lhs_type`, `rhs_type`, `expression`).  Writing
# the probe's own text rather than re-emitting one from those three
# fields is deliberate -- it is the corpus's own program, so what the
# compiler is handed here is what it was handed when the corpus was
# built.
#
# WHAT THE EDGE REGIONS ARE.  Whatever the compiler puts around the
# instruction: go's `/` carries a branch into `runtime.panicdivide` for
# a zero divisor and, on the signed forms, go's own handling of the
# extreme case.  Those are not hidden.  The gate is asked the same
# question it is always asked -- is the carved body's answer the cell's
# term for every input -- and its own verdict says whether that holds
# everywhere (`unsat`, PROVED_ON_SHIP) or only on a region (`sat`,
# DISPROVED, with the counterexample z3 gives).  `region_of` below is
# the rendering of that, and invents no third answer.

SOU_JSON = os.path.join(ARCH_OPCODES, "single_opcode_units.json")

PRIMITIVE_ROWS = {}
MANIFESTS = {}

CAUSE_NO_PRIMITIVE = "no single-opcode row of this language's own " \
                     "corpus classifies to this cell"
CAUSE_NO_MEMBER = "a single-opcode row classifies to this cell, but " \
                  "none of its members is a probe this language's own " \
                  "manifest holds"
CAUSE_PRIMITIVE_FLAGS = "the primitive route renders the operator's " \
                        "own answer, and the flags place is not a " \
                        "value an operator answers with"

# the manifest's own representation names -> (the kind the renderer's
# parameter plan uses, the width in bits).  `probe_gen.HOLDERS` is where
# these six come from, and the name is the arch campaign's rather than
# the language's spelling, which is why this table is one table and not
# five.
REP_HOLDER = {
    "i32": ("bv", 32),
    "i64": ("bv", 64),
    "u64": ("bv", 64),
    "f32": ("fp", 32),
    "f64": ("fp", 64),
    "bool": ("bv", 8),
}


# ------------------------------------------------------------------
# section 2e (task g1c): THE LOOKUP WIDENED BY ONE STEP
# ------------------------------------------------------------------
#
# WHAT THIS ADDS, one sentence, in relation.  Task g1's lookup accepted
# a language operator only when its whole chaff-stripped body is ONE
# instruction that classifies to the cell; this widens it by exactly one
# step -- the body may ALSO carry zero or more ZERO-OPERAND SETUP
# instructions, and nothing else.
#
# WHY, from what task g1 measured rather than from a guess.  Division in
# every one of the four targets lowers to the cell's own instruction
# PLUS the accumulator setup the instruction requires: `cltd; idiv` for
# the 32-bit signed form, `cqto; idiv` for the 64-bit one.  That is two
# instructions under task o2's narrow rule, so `idiv gpr_one 32` had no
# primitive in c, rust, go or swift and went by the term route in all
# four -- 51 instructions after the strip in c and rust, 85 in go, and
# the gate UNDECIDED at 3,000 ms and again at 300,000 ms on all six of
# its places (log 241 sections 4 and 7.1).  Task g1's own lookup already
# RECORDED that task o2's WIDE rule finds such a row in c
# (`mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret`, unit
# `c/op_246`) and kept it as evidence rather than taking it as a route.
# This section is that evidence turned into a route.
#
# WHAT COUNTS AS SETUP, and it is a closed list read from the reference
# simulator, never a judgement: a line with NO OPERAND AT ALL whose
# mnemonic is a key of `reference.SPREAD_SIGN` (`cltd`, `cqto`, `cqo`,
# `cwtd` -- spread the sign of the accumulator across its partner) or of
# `reference.ACCUMULATOR_WIDEN` (`cltq`, `cwtl` and their like -- widen
# the accumulator in place).  Those are the same two tables task h2's
# zero-operand width rule reads in `model_table.classify_line`, so a
# setup instruction classifies to a cell of the model table like any
# other and is recorded as one.
#
# WHERE THE ROWS COME FROM.  Both of task o2's rule lists are read, and
# each row's body is stripped again under the NARROW rule -- because the
# wide rule counts `cltd` and `cqto` as chaff and would throw away the
# very instructions this route must see.  A row is accepted when what
# remains is some setup instructions plus EXACTLY ONE other instruction,
# and that one classifies to the cell.
#
# WHAT IS RECORDED.  `route` is `primitive` when the accepted row
# carried no setup at all -- which is task g1's own answer, unchanged --
# and `primitive+setup` when it carried one or more.  The setup cells go
# on the lookup record as `setup`, each with its own line, mnemonic and
# (`mnem`, shape, `key_width`) triple, and they appear again in the run's
# `composition` column, which is the carved body's own classification and
# needs no change to hold them.
#
# THE SPELLING BAN IS UNTOUCHED BY THIS.  The widened rule reads a
# mnemonic and an operand count and nothing else; the two tables are
# keyed by arch mnemonic, which is machine form, and no operator token
# enters the match here any more than it did in task g1's rule.

SETUP_MNEMONICS = frozenset(list(R.SPREAD_SIGN.keys())
                            + list(R.ACCUMULATOR_WIDEN.keys()))

CAUSE_NO_PRIMITIVE_WIDE = "no single-opcode row of this language's own " \
                          "corpus is this cell's instruction plus " \
                          "zero-operand setup and nothing else"


def is_setup_line(line):
    """one instruction of a stripped body: is it a ZERO-OPERAND SETUP
    instruction from the reference's own two tables?

    Both halves are required.  The mnemonic must be a key of
    `reference.SPREAD_SIGN` or `reference.ACCUMULATOR_WIDEN`, and the
    line must carry NO OPERAND -- `cltd` is setup, and a hypothetical
    line spelling the same mnemonic with an operand is not, so the rule
    can never widen past the closed list it reads."""
    mnem, operands = SOU.parse_insn(line)
    if mnem is None:
        return False
    if mnem not in SETUP_MNEMONICS:
        return False
    return len(operands) == 0


def split_setup(stripped):
    """a narrow-stripped body -> (its setup instructions, everything
    else), in body order."""
    setup = []
    rest = []
    for line in stripped:
        if is_setup_line(line):
            setup.append(line)
            continue
        rest.append(line)
    return setup, rest


def setup_cell(line):
    """one setup instruction as the model-table cell it is, by task
    m1b's own classifier -- the same call `classify_instruction` makes
    for the composition column."""
    mnem, _operands = SOU.parse_insn(line)
    shape, width, cause = MTAB.classify_line(mnem, line, 0)
    out = {"line": line, "mnem": mnem}
    if shape is None:
        out["cell"] = None
        out["not_classified"] = cause
        return out
    out["cell"] = [mnem, shape, MTAB.key_width(mnem, width)]
    return out


def primitive_rows_with_setup(lang):
    """task o2's single-opcode rows for `lang`, under BOTH of its chaff
    rules, each stripped again under the NARROW rule and accepted when
    what remains is zero or more zero-operand setup instructions plus
    exactly one other instruction.

    Reading both lists is what reaches a divide: the row whose body is
    `mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret` is a
    single-opcode row under the WIDE rule only (the wide rule counts
    `cltd` as chaff), and stripping it under the NARROW rule is what
    puts `cltd` back where this route can see it.  A row is read once:
    the two lists overlap, and `body_text` is the identity."""
    if (lang, "setup") in PRIMITIVE_ROWS:
        return PRIMITIVE_ROWS[(lang, "setup")]
    MTAB._install_gpr_widths()
    document = read_json(SOU_JSON)
    groups = document["single_opcode_groups"].get(lang) or {}
    seen = set()
    out = []
    for rule in ("narrow", "wide"):
        for row in (groups.get(rule) or []):
            if row["body_text"] in seen:
                continue
            seen.add(row["body_text"])
            body = row["body_text"].split("; ")
            stripped = SOU.strip_chaff(body, "narrow")
            setup, rest = split_setup(stripped)
            if len(rest) != 1:
                continue
            line = rest[0]
            mnem, _operands = SOU.parse_insn(line)
            shape, width, cause = MTAB.classify_line(mnem, line, 0)
            entry = {
                "body_text": row["body_text"],
                "instruction": line,
                "mnem": mnem,
                "setup": [setup_cell(one) for one in setup],
                "found_under_rule": rule,
                "member_count": row.get("member_count"),
                "example_unit_id": row.get("example_unit_id"),
                "members": row.get("members") or [],
            }
            if shape is None:
                entry["cell"] = None
                entry["not_classified"] = cause
            else:
                entry["cell"] = [mnem, shape,
                                 MTAB.key_width(mnem, width)]
            out.append(entry)
    PRIMITIVE_ROWS[(lang, "setup")] = out
    return out


def route_changes(cells):
    """the (cell, target) pairs whose ROUTE the widened lookup changes,
    printed as it computes them.

    A pair changes when task g1's narrow lookup found no row and the
    widened one does.  A pair where both find a row cannot change: the
    widened rule is a superset that accepts the same zero-setup rows, and
    the chooser is the same one (most members, body text breaking a tie).
    That is asserted nowhere -- both lookups are run for every pair and
    the two answers compared."""
    say("the (cell, target) pairs the widened lookup changes")
    changed = set()
    total = len(ASKED) * len(targets())
    index = 0
    for asked in ASKED:
        held = cell_input(cells, asked)
        for lang in targets():
            index = index + 1
            if held.get("refusal_cause") is not None:
                continue
            narrow = primitive_lookup(held, lang, widened=False)
            wide = primitive_lookup(held, lang, widened=True)
            was = narrow.get("row") is not None
            now = wide.get("row") is not None
            if was == now and not (now and wide["row"]["setup"]):
                continue
            if not now:
                continue
            changed.add((asked, lang))
            say("   [%d/%d] %s %s %s -> %s: %s becomes %s, on `%s`"
                % (index, total, asked[0], asked[1], asked[2], lang,
                   "term" if not was else "primitive",
                   route_name(wide["row"]), wide["row"]["body_text"]))
    say("   %d of %d pair(s) change" % (len(changed), total))
    return changed


def route_name(row):
    """`primitive` where the accepted row carries no setup at all --
    task g1's own answer, unchanged -- and `primitive+setup` where it
    carries one or more."""
    if row.get("setup"):
        return "primitive+setup"
    return "primitive"


def primitive_rows(lang, rule="narrow"):
    """task o2's own single-opcode rows for `lang` under one of its two
    chaff rules, each with the (`mnem`, shape, `key_width`) triple its
    one instruction classifies to.

    THE ROUTE READS THE NARROW ROWS, which is the brief's own
    instruction.  The WIDE rows are read too, and only reported: task
    o2's wide rule counts a width-changing move or a sign extension
    (`movslq`, `cltd`, `cqto` and their like) as chaff as well, so a
    body that is a sign extension followed by one instruction is a
    single-opcode row under it and is not under the narrow rule.  Where
    the narrow lookup finds nothing, the record says whether the wide
    one would have -- as evidence about the cell, never as a second
    route.

    The strip is re-derived rather than trusted: `single_opcode_units.
    strip_chaff` is run again over the row's own `body_text`, and a row
    that does not come back as exactly one instruction is dropped."""
    if (lang, rule) in PRIMITIVE_ROWS:
        return PRIMITIVE_ROWS[(lang, rule)]
    MTAB._install_gpr_widths()
    document = read_json(SOU_JSON)
    groups = document["single_opcode_groups"].get(lang) or {}
    out = []
    for row in (groups.get(rule) or []):
        body = row["body_text"].split("; ")
        stripped = SOU.strip_chaff(body, rule)
        if len(stripped) != 1:
            continue
        line = stripped[0]
        mnem, _operands = SOU.parse_insn(line)
        shape, width, cause = MTAB.classify_line(mnem, line, 0)
        entry = {
            "body_text": row["body_text"],
            "instruction": line,
            "mnem": mnem,
            "member_count": row.get("member_count"),
            "example_unit_id": row.get("example_unit_id"),
            "members": row.get("members") or [],
        }
        if shape is None:
            entry["cell"] = None
            entry["not_classified"] = cause
        else:
            entry["cell"] = [mnem, shape, MTAB.key_width(mnem, width)]
        out.append(entry)
    PRIMITIVE_ROWS[(lang, rule)] = out
    return out


def manifest_of(lang):
    """the language's own probe manifest: what the corpus compiled, per
    probe number, with the operand types and the expression it was
    written from."""
    if lang not in MANIFESTS:
        path = os.path.join(OP, "probe_manifest_%s.json" % lang)
        if not os.path.exists(path):
            MANIFESTS[lang] = None
        else:
            MANIFESTS[lang] = read_json(path)
    return MANIFESTS[lang]


def probe_of_member(lang, unit):
    """one member of a single-opcode row -> the probe the manifest holds
    for it, or None.

    A member id is `<lang>/op_<n>` for an ORIGINAL probe and
    `<lang>/regen_<n>` for a regenerated one; only the first resolves in
    `probe_manifest_<lang>.json`, which is the file that carries the
    operand types."""
    if not unit:
        return None
    parts = unit.split("/")
    if len(parts) != 2:
        return None
    if not parts[1].startswith("op_"):
        return None
    document = manifest_of(lang)
    if document is None:
        return None
    number = parts[1][len("op_"):]
    row = (document.get("probes") or {}).get(number)
    if row is None:
        return None
    return {
        # A UNIT OBJECT, deliberately: `lang` plus `unit` plus `n`
        # identify one single member, which is the ONE place the
        # spelling ban allows an operator token -- as the display label
        # on the member, read by nothing.  The guard's own except-list
        # names exactly this shape.
        "lang": lang,
        "unit": unit,
        "n": row.get("n"),
        "operator": row.get("operator"),
        "arity": row.get("arity"),
        "position": row.get("position"),
        "lhs_rep": row.get("lhs_rep"),
        "lhs_type": row.get("lhs_type"),
        "rhs_rep": row.get("rhs_rep"),
        "rhs_type": row.get("rhs_type"),
        "expression": row.get("expression"),
        "result_type": row.get("result_type"),
        "symbol": row.get("symbol"),
        "source": row.get("source"),
    }


def primitive_lookup(held, lang, widened=None):
    """does `lang` have an operator whose whole lowered body IS this
    cell?  The answer, with everything the choice rested on.

    `widened` selects WHICH rule answers it.  False is task g1's own:
    the body, stripped by task o2's narrow rule, is exactly ONE
    instruction and it classifies to the cell.  True is task g1c's, one
    step wider: the body may also carry zero-operand setup instructions
    from the reference's own two tables, and nothing else (section 2e).
    `None` means "whatever the running task uses", which is what every
    caller inside a run passes."""
    if widened is None:
        widened = True
    key = [held["mnem"], held["shape"], held["key_width"]]
    if widened:
        rows = primitive_rows_with_setup(lang)
    else:
        rows = primitive_rows(lang)
    matched = []
    for row in rows:
        if row["cell"] == key:
            matched.append(row)
    found = {
        "lang": lang,
        "cell": key,
        "single_opcode_rows_read": len(rows),
        "rows_that_classify_to_this_cell": len(matched),
        "widened": widened,
        "lookup": "single_opcode_units.json, this language's own narrow "
                  "rows, each stripped again by task o2's own rule and "
                  "classified by task m1b's own classifier",
    }
    if widened:
        found["lookup"] = ("single_opcode_units.json, this language's "
                           "own rows under BOTH of task o2's rules, "
                           "each stripped again under the NARROW rule "
                           "and accepted when what remains is the "
                           "cell's instruction plus zero or more "
                           "zero-operand setup instructions from "
                           "reference.SPREAD_SIGN / "
                           "reference.ACCUMULATOR_WIDEN and nothing "
                           "else")
    if not matched:
        found["row"] = None
        if widened:
            found["cause"] = CAUSE_NO_PRIMITIVE_WIDE
        else:
            found["cause"] = CAUSE_NO_PRIMITIVE
            found["under_the_wide_rule"] = wide_rule_evidence(key, lang)
        return found
    ordered = sorted(matched,
                     key=lambda row: (-(row["member_count"] or 0),
                                      row["body_text"]))
    best = ordered[0]
    found["chosen_by"] = ("of the %d single-opcode rows that classify "
                          "to this cell, the one the corpus attests "
                          "with the most members; a tie is broken by "
                          "the row's own body text"
                          % len(matched))
    found["candidate_rows"] = []
    for row in ordered:
        found["candidate_rows"].append({
            "body_text": row["body_text"],
            "member_count": row["member_count"],
            "example_unit_id": row["example_unit_id"],
        })
    probe = None
    tried = 0
    for member in best["members"]:
        tried = tried + 1
        probe = probe_of_member(lang, member.get("unit"))
        if probe is not None:
            break
    found["members_tried_before_one_resolved"] = tried
    if probe is None:
        found["row"] = None
        found["cause"] = CAUSE_NO_MEMBER
        found["row_that_matched"] = {
            "body_text": best["body_text"],
            "instruction": best["instruction"],
            "member_count": best["member_count"],
        }
        return found
    found["row"] = {
        "body_text": best["body_text"],
        "instruction": best["instruction"],
        "member_count": best["member_count"],
        "example_unit_id": best["example_unit_id"],
        # EMPTY under task g1's rule, which accepts no setup at all;
        # one entry per zero-operand setup instruction under task g1c's.
        "setup": best.get("setup") or [],
        "found_under_rule": best.get("found_under_rule"),
    }
    found["probe"] = probe
    return found


def wide_rule_evidence(key, lang):
    """EVIDENCE ONLY, never a route: what task o2's WIDE chaff rule
    would have found at this cell in this language.

    The two rules differ by exactly one thing (task o2's own note in
    `single_opcode_units.json`): the wide rule counts a width-changing
    move or a sign extension as chaff as well.  So a body that is a
    sign extension followed by one instruction -- which is what a signed
    divide looks like -- is a single-opcode row under the wide rule and
    is not under the narrow one.  Recording it here is how the reason a
    cell has no primitive is a fact rather than a guess."""
    rows = primitive_rows(lang, "wide")
    matched = []
    for row in rows:
        if row["cell"] == key:
            matched.append(row)
    out = {
        "rule": "wide",
        "rows_that_classify_to_this_cell": len(matched),
        "note": "evidence about the cell, not a second route: the "
                "route this task runs reads the narrow rows, which is "
                "the brief's own instruction",
    }
    if matched:
        ordered = sorted(matched,
                         key=lambda row: (-(row["member_count"] or 0),
                                          row["body_text"]))
        out["body_text"] = ordered[0]["body_text"]
        out["example_unit_id"] = ordered[0]["example_unit_id"]
        out["member_count"] = ordered[0]["member_count"]
    return out


def primitive_params(probe):
    """the parameter plan of a primitive rendering, from the manifest's
    own representation names rather than from a language spelling."""
    reps = [probe.get("lhs_rep")]
    holders = [probe.get("lhs_type")]
    if probe.get("arity") == "binary":
        reps.append(probe.get("rhs_rep"))
        holders.append(probe.get("rhs_type"))
    params = []
    for index, rep in enumerate(reps):
        if rep not in REP_HOLDER:
            raise E.Refused(E.CAUSE_WIDTH,
                            "the manifest records the representation "
                            "%r, which this task has no holder for"
                            % rep)
        kind, bits = REP_HOLDER[rep]
        params.append({
            "index": index,
            "family": None,
            "name": E.PARAM_NAMES[index],
            "holder": holders[index],
            "kind": kind,
            "bits": bits,
            "used": True,
        })
    return params


def render_primitive(found, lang, label, write=True):
    """the chosen member's OWN probe source, with its symbol renamed to
    this run's label and nothing else changed."""
    import re
    probe = found["probe"]
    source = re.sub(r"\bop_%d\b" % probe["n"], "emu_%s" % label,
                    probe["source"])
    symbol = "emu_%s" % label
    if lang == "go":
        symbol = "main.emu_%s" % label
    folder = os.path.basename(SRC_DIR)
    if write:
        handle = open(os.path.join(SRC_DIR, label + suffix_of(lang)),
                      "w")
        handle.write(source)
        handle.close()
    return {
        "rendered": True,
        "source": source,
        "symbol": symbol,
        "params": primitive_params(probe),
        "renderer_input_text": probe["expression"],
        "source_path": os.path.join(folder, label + suffix_of(lang)),
    }


def run_primitive(shared, held, lang, record, found):
    """the primitive route for one (cell, target): ONE rendering and ONE
    compile for the whole cell, then the gate over every place the cell
    writes.

    WHY ONE RENDERING FOR SEVERAL PLACES: an operator answers with one
    value, so the primitive body is the cell's, not a place's.  Every
    place the cell writes is still put to the gate against that one
    body, which is how a cell that writes two places (`idiv`'s quotient
    and its remainder) shows which of them the operator answers."""
    label = E.sanitize("%s_%s_%d__primitive__%s"
                       % (held["mnem"], held["shape"], held["key_width"],
                          lang))
    try:
        built = render_primitive(found, lang, label)
    except E.Refused as refusal:
        built = {"rendered": False,
                 "refusal_cause": refusal.cause,
                 "refusal_detail": refusal.detail}
    got = None
    refusal = None
    if built.get("rendered"):
        got, refusal = compile_one_place(built["source"],
                                         built["symbol"], lang)
    for place in held["places"]:
        record["places"].append(
            one_place_primitive(shared, held, place, lang, label, built,
                                got, refusal, found["row"]))


def one_place_primitive(shared, held, place, lang, label, built, got,
                        refusal, found_row):
    """one written place of a cell, under the primitive route: the same
    record shape `one_place` writes, so the report walks one kind of
    place and not two."""
    out = {
        "writes": place["writes"],
        "text": place["text"],
        "sexpr": place["sexpr"],
        "bits": place["bits"],
        "families": place.get("families"),
        "home": place.get("home"),
        "route": route_name(found_row),
        "label": label,
    }
    if place.get("not_rendered") is not None:
        out["rendered"] = False
        out["refusal_cause"] = place["not_rendered"]
        out["refusal_detail"] = place.get("not_rendered_detail")
        return out
    if is_the_flags_place(place["writes"]):
        # `is_the_flags_place` and not `== "flags"` (log 246), so a HALF
        # of the flags place is refused by this rule too.  Task ap2's
        # fix 3 splits a 128-bit place into `.low` and `.high`, and the
        # two halves of a 64-bit comparison's flags place slipped past
        # the old test and were put to the gate against the operator's
        # answer -- where they said `the IN rows cannot be aligned`,
        # which is true about the two row lists and false about the
        # objects.
        out["rendered"] = False
        out["refusal_cause"] = CAUSE_PRIMITIVE_FLAGS
        out["refusal_detail"] = ("the operator's own answer is the "
                                 "value it hands back, and this cell's "
                                 "flags place is a second place the "
                                 "opcode writes")
        return out
    working = place
    projected = projected_lane(shared, place, held["key_width"])
    if projected is not None:
        out["lane"] = projected["lane"]
        if projected.get("refusal_cause") is not None:
            out["rendered"] = False
            out["refusal_cause"] = projected["refusal_cause"]
            out["refusal_detail"] = projected.get("refusal_detail")
            return out
        working = projected["place"]
    if not built.get("rendered"):
        out["rendered"] = False
        out["refusal_cause"] = built.get("refusal_cause")
        out["refusal_detail"] = built.get("refusal_detail")
        return out
    out["rendered"] = True
    out["source"] = built["source"]
    out["symbol"] = built["symbol"]
    out["params"] = built["params"]
    out["source_path"] = built["source_path"]
    out["renderer_input_text"] = built["renderer_input_text"]
    if got is None:
        out["compiled"] = False
        out["compile_refusal"] = refusal
        return out
    out["compiled"] = True
    raw_bytes, mnem = got
    out["body_bytes"] = " ".join(raw_bytes)
    out["body_text"] = "; ".join(mnem)
    out["landing"] = landing_of(mnem, held["mnem"])
    out["check"] = check_one_place(shared, working, built["params"],
                                   raw_bytes, mnem, label, lang,
                                   attested=attested_of(held, found_row))
    return out










def region_of(check):
    """THE REGION COLUMN, and it invents no answer of its own: it is a
    rendering of the gate's own verdict.

    `unsat` (PROVED_ON_SHIP) means the carved body answers as the cell's
    term for EVERY value of every aligned input row, so there is no
    region -- the body is the cell everywhere.  `sat` (DISPROVED) means
    it does not, and z3's counterexample is the witness: the body equals
    the cell only on a region, and that row of inputs is outside it.
    Anything else is the solver not answering, and the reason it gives
    is carried through unchanged."""
    if check is None:
        return ""
    outcome = check.get("outcome")
    if outcome == "PROVED_ON_SHIP":
        return "holds on every input of every aligned row"
    if outcome == "DISPROVED":
        text = "holds on a region, not on every input"
        example = check.get("counterexample")
        again = check.get("under_caller_extension")
        if again is not None and again.get("outcome") == \
                "PROVED_ON_SHIP":
            return ("holds on every input once each narrow-holder row "
                    "is zero-extended to the register")
        if example is not None:
            text = "%s; z3's counterexample: %s" % (text, example)
        return text
    return "not decided: %s" % check.get("reason")










# ==================================================================
# section 2b: task h1b -- THE COMPOSITION COLUMN
# ==================================================================
#
# WHAT THIS SECTION ADDS, one sentence, in relation.  A carved body is
# a sequence of arch opcodes, each a cell of the model table, so its
# term is a composition of table cells; `compose_command` reads the
# `handful.json` task h1 already wrote, walks the RAW carved body of
# each run's own destination place, classifies every instruction by
# task m1b's own classifier, and writes the result back as one new
# field, `composition`, on every run -- nothing else in the record
# changes.

IN_TABLE_CAUSE = "not a TRANSLATED row of the model table at this key"


def load_in_table():
    """every (`mnem`, shape, `key_width`) triple that is a TRANSLATED
    row of the arch-opcode model table -- read once from
    `model_table_rows.json`, the lighter of the two files that carry
    it (`model_table.json` also carries the attestation and the edges,
    which this task does not need)."""
    document = read_json(MTAB.ROWS_JSON)
    out = set()
    for row in document["rows"]:
        if row["outcome"] != "TRANSLATED":
            continue
        out.add((row["mnem"], row["shape"], row["key_width"]))
    return out


def chaff_reason(mnem, operands):
    """task o2's own narrow chaff rule
    (`single_opcode_units.is_chaff`, `NARROW_BARE` / `NARROW_PURE_MOVE`),
    read for WHICH of its two kinds one instruction is, so `ret` and a
    calling-convention move are marked as what they are rather than
    reported as an instruction that maps to no table cell.  `None` when
    the instruction is not chaff under the narrow rule."""
    if mnem in SOU.NARROW_BARE:
        if mnem == "ret":
            return "the function's own return, chaff by task o2's " \
                   "narrow rule"
        return "%s, chaff by task o2's narrow rule" % mnem
    if mnem in SOU.NARROW_PURE_MOVE:
        if len(operands) != 2:
            return None
        for operand in operands:
            if not SOU.is_reg_or_slot_operand(operand):
                return None
        return "a calling-convention move (a pure register-to-register " \
               "or register-to-slot copy), chaff by task o2's narrow rule"
    return None


def classify_instruction(line, in_table):
    """one instruction of a carved body, as the table cell it is (or
    named as what it is instead): a table cell, `ret` or a
    calling-convention move (task o2's own chaff rule), or an
    instruction that maps to no table cell, with its own line and the
    classifier's own cause.

    The classifier is task m1b's own: `model_table.classify_line`
    (which calls `model_table.operand_class` and
    `model_table.SHAPE_OF_CLASSES`) and `model_table.key_width`,
    imported and called, never re-implemented.  `operand_class` reads
    general-register widths from `model_table.GPR_WIDTH_OF_NAME`,
    which task m1b's own `attestation()` installs as a side effect and
    this task never runs, so `MTAB._install_gpr_widths()` -- the same
    installer, called the same way -- is primed once by `compose_command`
    before the first instruction is classified."""
    mnem, operands = SOU.parse_insn(line)
    if mnem is None:
        return {"line": line, "cell": False,
                "reason": "an empty instruction"}
    reason = chaff_reason(mnem, operands)
    if reason is not None:
        return {"line": line, "mnem": mnem, "cell": False,
                "reason": reason}
    shape, width, cause = MTAB.classify_line(mnem, line, 0)
    if shape is None:
        return {"line": line, "mnem": mnem, "cell": False,
                "reason": "the classifier could not read it: %s" % cause}
    key_width = MTAB.key_width(mnem, width)
    if (mnem, shape, key_width) not in in_table:
        return {"line": line, "mnem": mnem, "cell": False,
                "reason": "classified as shape %s key_width %d, which "
                          "is %s" % (shape, key_width, IN_TABLE_CAUSE)}
    return {"line": line, "mnem": mnem, "cell": True, "shape": shape,
            "key_width": key_width}


def composition_of_run(run, in_table):
    """the RAW carved body of the run's own destination place
    (`destination_place`, the same place the `landed`/`gate` columns
    already summarize), as the ordered list of what each instruction
    is.  Empty where the run has no carved body at all -- refused
    before any render, refused at render, or refused at compile; the
    run's own `refusal_cause` / place's own `refusal_cause` /
    `compile_refusal` already say why, so nothing is duplicated here."""
    if run.get("refusal_cause") is not None:
        return []
    place = destination_place(run)
    if place is None:
        return []
    if place.get("rendered") is False:
        return []
    if not place.get("compiled"):
        return []
    body = place.get("body_text")
    if not body:
        return []
    lines = body.split("; ")
    if the_body_is_empty(lines):
        # AN EMPTY BODY (log 246): an emulation whose carved body carries no
        # instruction of its own composes the cell out of NOTHING, and
        # the brief's own words for that record are `composition = []`.
        return []
    out = []
    for line in lines:
        out.append(classify_instruction(line, in_table))
    return out




# ==================================================================
# section 3: THE REPORT
# ==================================================================


















def verdict_of_run(run):
    """one run's destination place, as three cells: the gate's verdict,
    the landing, and the cause where it never reached the gate."""
    out = {"gate": "", "landed": "", "cause": ""}
    if run is None:
        out["cause"] = "no run recorded"
        return out
    if run.get("refusal_cause") is not None:
        out["cause"] = run["refusal_cause"]
        return out
    place = destination_place(run)
    if place is None:
        out["cause"] = "no place to render"
        return out
    if place.get("rendered") is False:
        out["cause"] = "%s: %s" % (place.get("refusal_cause"),
                                   place.get("refusal_detail"))
        return out
    if not place.get("compiled"):
        out["cause"] = "the compiler refused: %s" % place.get(
            "compile_refusal")
        return out
    out["gate"] = gate_cell(place["check"])
    out["landed"] = landed_cell(place["landing"])
    return out














def destination_place(run):
    """the run's own destination place: the first place that is not the
    flags, or the flags place when that is all there is."""
    for place in run["places"]:
        if place["writes"] != "flags":
            return place
    if run["places"]:
        return run["places"][0]
    return None



def landed_cell(landing):
    if landing["verdict"] == "LANDED":
        return "LANDED"
    if landing["verdict"] == "LANDED_ELSEWHERE":
        return "LANDED_ELSEWHERE on `%s`" % landing["landed"]["mnem"]
    return "NOT_COLLAPSED (%d)" % landing["stripped_count"]


def gate_cell(check):
    outcome = check.get("outcome")
    again = check.get("under_caller_extension")
    if again is not None:
        return "%s, %s under caller extension" % (outcome,
                                                  again.get("outcome"))
    once_more = check.get("recheck")
    if once_more is not None:
        return "%s, %s at %s ms" % (outcome, once_more.get("outcome"),
                                    once_more.get("ceiling_ms"))
    return "%s" % outcome





if __name__ == "__main__":
    say(__doc__)
    say("This file is the driver, and a driver is a library: the loop's "
        "own entry is `autopoly.py --bank <command>`, which calls what "
        "decides an answer here.  The commands the closed tasks' logs "
        "cite (`report2`, `run3`, `changes3c` and the rest) are those "
        "tasks' own report commands over those tasks' own products, and "
        "they are answered by `handful_frozen.py` -- this file copied "
        "byte for byte on 2026-09-10, before the nine task-name gates "
        "were stripped out of it: `python3 handful_frozen.py <command>`.")
    sys.exit(2)
