#!/usr/bin/env python3
"""mode.py -- task o13: render the MODE (the guard) into the emulation,
so a trapping operator traps.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly
(`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/CORE_0_3_2_2_3_autopoly.md`),
its "what is next" item 1.  The ledger's guard-outcome block is
`hq.research.compiler_graph.ledger` and its `row` / `producer`
sub-nodes.

THE OBJECTS, one sentence each, in relation.
  * An X UNIT is a pool member whose entry has no member in the target
    language, together with its canon40 record -- the body verbatim,
    the arrival contract, the answer home, and THE LEDGER, one row per
    value the body moves.
  * A GUARD ROW is a ledger row in the GUARD block: a flag-derived
    value whose producer is the PAIR (the arch opcode that set the
    flags, the arch opcode that read them).  When the reader is a
    conditional transfer the pair is a BRANCH, and a branch is what
    makes a body partial; when the reader is a conditional set or move
    the row is an ordinary value the term already carries.
  * A DEPARTING PATH is a path through the body that transfers OUT of
    the unit -- `ud2`, or a `call` to a routine that does not come
    back.  `reference.Reference.walk_body` already finds them and
    writes one guard row per departure carrying the condition the path
    is taken under; the derivation below keeps that condition as a z3
    term rather than only as the string the base class writes.
  * THE MODE RENDERING is the emulation with those conditions emitted
    before the operation, each with the same OUTCOME its own departing
    path has -- a trap, or a call that does not return -- read off the
    guard row and never assumed.
  * THE GUARDED READING is the proof posing that makes a guard mean
    something to the solver: each side's answer is replaced, where that
    side's own guard fires, by ONE SHARED value `left_the_unit`, so two
    units that leave on the same inputs and agree on the rest are
    proved equal, and two that leave on DIFFERENT inputs are disproved
    with a counterexample in the region where one leaves and the other
    answers.

WHAT IS REUSED RATHER THAN COPIED, said out loud.  Nothing under
`Research/op_pipeline/` is edited, and neither `emulate.py` nor
`rust/rust_render.py` is edited: this module IMPORTS both and DERIVES
from their renderers.
  `emulate.Renderer` and `rust_render.RustRenderer` render the term;
  the two classes below override `render` and `plan_parameters` alone,
  to put the guard in front of the answer.  `emulate.collect` /
  `fork_one` run the jobs, bound to this module's worker by
  `install_worker`, the same assignment `rust_render.install_worker`
  makes.  `emulate.build_shared` and `rust_render.build_shared` build
  the shared objects.  `emulate.compile_and_carve` /
  `rust_render.compile_and_carve` compile at each corpus's own ship
  flags and carve with `lane_gen.extract`.  `canonical_form.render_one`
  wraps and gates; `term66_run.one_unit` transcribes; `gate.Gate.decide`
  is the one solver call; `pool100_entry_equivalence` aligns the two
  sides.  `emulate.prove_against_x` is the UNCHANGED first posing, so
  this task's `q3` column is task o7's own column.

MEMORY BOUND, stated as the law requires: one collecting process, its
peak resident size checked after every emulation, named abort
ABORT_MEMORY_O13 at 4 GB resident; one forked sub-process per
emulation under RLIMIT_AS 2,048 MB and a wall clock of 240 s (a
sub-process that passes either is recorded as a runner limit, never as
a verdict); at most 3 sub-processes at once.  The population is 95
emulations over 80 distinct x units, so both held stores are read --
5.8 MB and 7.7 MB of json -- and the canon40 shards are never
re-streamed.

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

No operator token appears in this file.  The population is the set of
pool entry ids whose emulation the two earlier runs recorded DISPROVED
-- a machine-form selection over a recorded verdict.  The guard
vocabulary is keyed by ARCH MNEMONIC PAIRS read off the ledger's typed
producer objects (`{"kind": "flag_pair", "mnem": ["test", "je"]}`),
which is the same machine form the ledger itself is keyed by; no record
this file writes carries an operator field at all.

Coding discipline: no compound one-liner statements.

usage:
  mode.py vocabulary          the disproved population, the ledgers'
                              guard rows, the kinds by outcome table
  mode.py facts               what each candidate outcome spelling
                              emits, measured in c and in rust
  mode.py run c               re-render the 36 disproved c emulations
  mode.py run rust            re-render the 59 disproved rust ones
  mode.py run <target> <ms>   the same, with the gate's solver ceiling
                              raised to <ms>, written to its own file
  mode.py diagnose <target> <entry id> ...
                              the values in motion at the solver's own
                              model, for an emulation the guarded
                              posing does not prove
  mode.py report              mode_results.json + mode_report.md
"""

import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EMULATION = os.path.normpath(os.path.join(HERE, ".."))
RUST = os.path.join(EMULATION, "rust")
CROSS = os.path.normpath(os.path.join(HERE, "..", ".."))
OP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                   "op_pipeline"))
sys.path.insert(0, OP)
sys.path.insert(0, CROSS)
sys.path.insert(0, EMULATION)
sys.path.insert(0, RUST)

import z3                                                        # noqa: E402
import emulate as E                                              # noqa: E402
import rust_render as RR                                         # noqa: E402

SRC_DIR = os.path.join(HERE, "src")
POPULATION = os.path.join(HERE, "mode_population.json")
FACTS = os.path.join(HERE, "mode_facts.json")
RUN_C = os.path.join(HERE, "mode_run_c.json")
RUN_RUST = os.path.join(HERE, "mode_run_rust.json")
RESULTS = os.path.join(HERE, "mode_results.json")
REPORT = os.path.join(HERE, "mode_report.md")
HOST_FOLDER = ("~/Programming/PseudoCoupHQ/Research/oracle/"
               "cross_construction/emulation/mode")

COLLECTOR_CAP_KB = 4 * 1024 * 1024

# the two runs this task re-runs, and where each one's records live
EARLIER = {
    "c": {"results": os.path.join(EMULATION, "emulation_results.json"),
          "key": "results",
          "population": os.path.join(EMULATION,
                                     "emulation_population.json"),
          "held": os.path.join(EMULATION, "emulation_held.json"),
          "log": "log_218 (task o7)"},
    "rust": {"results": os.path.join(RUST, "rust_results.json"),
             "key": "run",
             "population": os.path.join(RUST, "rust_population.json"),
             "held": os.path.join(RUST, "rust_held.json"),
             "log": "log_226 (task o11)"},
}

# the conditional-transfer stems, so a guard row that is a BRANCH is
# told from a guard row that is a flag-derived VALUE (`setcc` and
# `cmovcc` also make GUARD-block rows and are inside the term already)
BRANCH_READERS = ("je", "jne", "jz", "jnz", "jl", "jle", "jg", "jge",
                  "jb", "jbe", "ja", "jae", "js", "jns", "jo", "jno",
                  "jp", "jnp")

TRAP_OUTCOME = "a trap"
TRAP_KIND = "trap"
CALL_KIND = "call that does not return"

CAUSE_GUARD_SORT = "the guard condition is not a truth value"
CAUSE_GUARD_REFUSED = "the reference refused the x body's guard walk"

MODE_NONE = "no departing path: the x body is total"
MODE_RENDERED = "the guard is rendered"


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_collector_memory():
    used = peak_kb()
    if used > COLLECTOR_CAP_KB:
        raise SystemExit(
            "ABORT_MEMORY_O13: the collecting process's peak resident "
            "%d kB passed the stated bound of %d kB" % (used,
                                                        COLLECTOR_CAP_KB))
    return used


def write_json(path, document):
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()


def read_json(path):
    handle = open(path)
    document = json.load(handle)
    handle.close()
    return document


# ==================================================================
# section 1: THE GUARD   read off the body, kept as a term
# ==================================================================

def make_mode_reference(base):
    """`reference.Reference` with ONE addition, made by derivation and
    not by an edit: `record_guard` keeps the z3 CONDITION TERM beside
    the string the base class writes, so this task emits the departing
    path's own condition rather than rebuilding one by hand.

    The derivation is off the class of `base` -- the walker
    `term97_walk.build` already made -- and `base`'s own state is
    carried over, so the reference is the one the corpus was proved
    with and nothing about it is rebuilt."""
    import reference as R

    class ReferenceKeepingGuardTerms(base.__class__):
        def record_guard(self, state, line, target, condition=None):
            R.Reference.record_guard(self, state, line, target,
                                     condition)
            state.guard_rows[-1]["condition_term"] = condition

    derived = ReferenceKeepingGuardTerms()
    derived.__dict__.update(base.__dict__)
    return derived


def departing_paths(reference, unit):
    """one body -> the list of paths that transfer OUT of it, each with
    the z3 condition it is taken under, the line that left, and where
    it went.  `reference.Reference.walk_body` writes these rows itself;
    this function runs the walk and reads them off the state."""
    state = reference.simulate(unit.get("body_verbatim"),
                               unit.get("arrival_contract_bindings"),
                               callees=reference.callees_for(unit))
    rows = []
    for row in state.guard_rows:
        rows.append({
            "line": row.get("line"),
            "went_to": row.get("went_to"),
            "condition": row.get("condition"),
            "condition_term": row.get("condition_term"),
        })
    return rows


def outcome_of_path(row):
    """one departing path's OUTCOME, read off the row and never
    assumed: a trap when the departing line is `ud2`, otherwise a call
    to the routine the transfer names."""
    went = row.get("went_to")
    line = (row.get("line") or "").split(" ")[0]
    if went == TRAP_OUTCOME:
        return {"kind": TRAP_KIND, "mnem": line, "callee": None}
    return {"kind": CALL_KIND, "mnem": line, "callee": went}


def guard_condition_of(rows):
    """the departing paths' conditions, joined: the unit leaves down
    SOME departing path exactly when one of them holds.  A row whose
    condition is `always` carries no term -- the body leaves on every
    input, which is not a mode -- and is returned beside the term."""
    terms = []
    always = []
    for row in rows:
        term = row.get("condition_term")
        if term is None:
            always.append(row.get("line"))
            continue
        terms.append(term)
    if not terms:
        return None, always
    if len(terms) == 1:
        return terms[0], always
    return z3.Or(*terms), always


def branch_guard_rows(record):
    """the LEDGER's own guard-outcome rows for one unit, kept to the
    ones whose producer pair reads a conditional transfer.  This is the
    vocabulary's row: the pair of arch mnemonics, and the rows the
    flag-setting opcode read."""
    ledger = record.get("ledger") or []
    by_name = {}
    for row in ledger:
        by_name[row.get("row")] = row
    out = []
    for row in ledger:
        if row.get("block") != "GUARD":
            continue
        producer = row.get("produced_by") or {}
        mnem = producer.get("mnem")
        if not isinstance(mnem, list):
            continue
        if len(mnem) != 2:
            continue
        if mnem[1] not in BRANCH_READERS:
            continue
        operands = row.get("operands") or []
        flag_row = {}
        if operands:
            flag_row = by_name.get(operands[0]) or {}
        out.append({
            "row": row.get("row"),
            "setter": mnem[0],
            "reader": mnem[1],
            "flag_row": operands[0] if operands else None,
            "flag_operands": list(flag_row.get("operands") or []),
        })
    return out


def kind_of(guard_row):
    """the vocabulary key for one branch guard row: the pair of arch
    mnemonics, and the BLOCKS of the rows the setter read.  Machine
    form throughout -- the mnemonics come from the ledger's typed
    producer object and the row names from its operand list."""
    blocks = []
    for name in guard_row.get("flag_operands") or []:
        blocks.append(str(name).split("-")[0])
    shape = " ".join(blocks) if blocks else "none"
    return "%s %s on %s" % (guard_row["setter"], guard_row["reader"],
                            shape)


# ==================================================================
# section 2: THE POPULATION   the 95 emulations the two runs disproved
# ==================================================================

def disproved_of(target):
    """the entry ids whose emulation the earlier run recorded
    DISPROVED, each with the job plan it was run from."""
    where = EARLIER[target]
    document = read_json(where["results"])
    population = read_json(where["population"])
    plans = population["entries"]
    jobs = []
    for record in document[where["key"]]:
        verdict = (record.get("q3") or {}).get("outcome")
        if verdict != "DISPROVED":
            continue
        entry_id = record["entry_id"]
        plan = dict(plans[entry_id])
        plan["control"] = False
        plan["earlier"] = {
            "q3_outcome": verdict,
            "counterexample": (record.get("q3") or {}).get(
                "counterexample"),
            "under_caller_extension": ((record.get("q3") or {}).get(
                "under_caller_extension") or {}).get("outcome"),
            "q1_verdict": (record.get("q1") or {}).get("verdict"),
            "q2_verdict": (record.get("q2") or {}).get("verdict"),
            "body_bytes": record.get("body_bytes"),
            "body_text": record.get("body_text"),
            "source_path": record.get("source_path"),
        }
        jobs.append(plan)
    return jobs


def vocabulary():
    """deliverable 1: the guard-outcome vocabulary read off the ledgers
    of the disproved units."""
    say("-- VOCABULARY: the guard rows of the disproved units")
    jobs = {}
    step = 0
    for target in ("c", "rust"):
        step = step + 1
        jobs[target] = disproved_of(target)
        say("[%d/4] %s: %d disproved emulations"
            % (step, target, len(jobs[target])))
    held = {}
    for target in ("c", "rust"):
        held.update(read_json(EARLIER[target]["held"])["held"])
        check_collector_memory()
    units = {}
    for target in ("c", "rust"):
        for job in jobs[target]:
            unit = job["x_unit"]
            units.setdefault(unit, {"x_unit": unit,
                                    "x_lang": job["x_lang"],
                                    "emulations": []})
            units[unit]["emulations"].append({"target": target,
                                              "entry_id":
                                                  job["entry_id"]})
    step = step + 1
    say("[%d/4] %d distinct x units under the %d emulations"
        % (step, len(units), len(jobs["c"]) + len(jobs["rust"])))
    shared = E.build_shared()
    reference = make_mode_reference(shared["reference"])
    del shared
    counts = {}
    for unit in sorted(units):
        record = held.get(unit)
        row = units[unit]
        if record is None:
            row["ledger_guard_rows"] = []
            row["walk"] = "no canon40 record held"
            continue
        row["ledger_guard_rows"] = branch_guard_rows(record)
        row["body_verbatim"] = record.get("body_verbatim")
        try:
            paths = departing_paths(reference, dict(record, unit=unit))
            row["departing_paths"] = [
                {"line": p["line"], "went_to": p["went_to"],
                 "condition": p["condition"]} for p in paths]
            row["outcomes"] = [outcome_of_path(p) for p in paths]
            row["walk"] = "walked"
        except Exception as problem:                     # noqa: BLE001
            row["departing_paths"] = []
            row["outcomes"] = []
            row["walk"] = "%s: %s" % (type(problem).__name__, problem)
        outcome_kinds = sorted(set(o["kind"] for o in row["outcomes"]))
        if outcome_kinds:
            outcome_text = " and ".join(outcome_kinds)
        else:
            outcome_text = "none: no path leaves the unit"
        row["outcome_kinds"] = outcome_text
        if not row["ledger_guard_rows"]:
            key = ("none: no branch guard row in this ledger",
                   outcome_text)
            counts[key] = counts.get(key, 0) + 1
            continue
        for guard_row in row["ledger_guard_rows"]:
            key = (kind_of(guard_row), outcome_text)
            counts[key] = counts.get(key, 0) + 1
        check_collector_memory()
    table = []
    for key in sorted(counts):
        table.append({"guard_kind": key[0], "outcome": key[1],
                      "how_many": counts[key]})
    document = {
        "task": "o13",
        "node": ("hq.research.arch_unit_oracle.cross_construction."
                 "autopoly"),
        "disproved": {"c": jobs["c"], "rust": jobs["rust"]},
        "units": units,
        "kinds_by_outcome": table,
        "collector_peak_kb": peak_kb(),
    }
    write_json(POPULATION, document)
    step = step + 1
    say("[%d/4] wrote %s" % (step, POPULATION))
    for entry in table:
        say("   %4d  %-46s -> %s" % (entry["how_many"],
                                     entry["guard_kind"],
                                     entry["outcome"]))
    return 0


# ==================================================================
# section 3: THE OUTCOME SPELLINGS   measured, not assumed
# ==================================================================

# Each candidate carries the source it needs.  `%s` in `declares` and
# in `text` is the ROUTINE NAME, filled in from the guard row's own
# callee for a call outcome; a trap outcome names no routine.
CANDIDATES = {
    "c": [
        {"name": "builtin_trap", "kind": TRAP_KIND,
         "declares": "", "text": "__builtin_trap();"},
        {"name": "a_call_to_a_routine_that_does_not_return",
         "kind": CALL_KIND,
         "declares": "void %s(void) __attribute__((noreturn));",
         "text": "%s();"},
    ],
    "rust": [
        {"name": "process_abort", "kind": TRAP_KIND,
         "declares": "", "text": "std::process::abort();"},
        {"name": "inline_ud2", "kind": TRAP_KIND, "declares": "",
         "text": "unsafe { core::arch::asm!(\"ud2\", "
                 "options(noreturn)) };"},
        {"name": "a_call_to_a_routine_that_does_not_return",
         "kind": CALL_KIND,
         "declares": "extern \"C\" { fn %s() -> !; }",
         "text": "unsafe { %s() };"},
    ],
}

PROBE_ROUTINE = "o13_probe_routine"

# the same probe with NO guard in it, so the cost of each spelling is
# the count of instructions it adds over this baseline, measured rather
# than judged
BASELINE = {"name": "no_guard_at_all", "kind": "baseline",
            "declares": "", "text": ""}

C_PROBE = """#include <stdint.h>
%s

uint32_t
probe_%s(uint32_t a, uint32_t b)
{
    if (b == 0) { %s }
    return a / b;
}
"""

RUST_PROBE = """%s
%s

#[no_mangle]
pub extern "C" fn probe_%s(a: u32, b: u32) -> u32
{
    if b == 0 { %s }
    { let n: u32 = a; let d: u32 = b;
      unsafe { if d == 0 { core::hint::unreachable_unchecked(); } }
      n / d }
}
"""


def probe_source(target, candidate):
    declares = candidate["declares"]
    text = candidate["text"]
    if "%s" in declares:
        declares = declares % PROBE_ROUTINE
    if "%s" in text:
        text = text % PROBE_ROUTINE
    if target == "c":
        return C_PROBE % (declares, candidate["name"], text)
    return RUST_PROBE % (RR.RUST_PRELUDE, declares, candidate["name"],
                         text)


def opcodes_of(mnem):
    """the body's arch opcodes as TYPED OBJECTS, the shape the ledger's
    producer uses.  A bare mnemonic in a list is a spelling-keyed place
    -- the unmodified guard says so, and `xor` is both an arch mnemonic
    and an operator token -- and the answer to a spelling collision is
    a shape change, never an exemption (producer CORE; log_147 13.7)."""
    names = sorted(set(one.split(" ")[0] for one in mnem))
    return [{"kind": "arch_opcode", "mnem": name} for name in names]


def carries(row, mnemonic):
    for opcode in row.get("opcodes") or []:
        if opcode.get("mnem") == mnemonic:
            return True
    return False


def facts():
    """what each candidate outcome spelling ACTUALLY emits, at each
    corpus's own ship flags, carved with the pipeline's own reader.
    The renderer reads this file and picks by the rule stated in it;
    nothing here is recalled."""
    say("-- FACTS: what each outcome spelling emits")
    measured = {"c": [], "rust": []}
    total = 2 + len(CANDIDATES["c"]) + len(CANDIDATES["rust"])
    step = 0
    for target in ("c", "rust"):
        for candidate in [BASELINE] + CANDIDATES[target]:
            step = step + 1
            source = probe_source(target, candidate)
            symbol = "probe_" + candidate["name"]
            if target == "c":
                got, refusal = E.compile_and_carve(source, symbol)
            else:
                got, refusal = RR.compile_and_carve(source, symbol)
            row = {"name": candidate["name"], "kind": candidate["kind"],
                   "source": source, "refusal": refusal}
            if got is not None:
                raw_bytes, mnem = got
                row["body_text"] = "; ".join(mnem)
                row["opcodes"] = opcodes_of(mnem)
                row["body_line_count"] = len(mnem)
            measured[target].append(row)
            say("[%d/%d] %s %s -> %s"
                % (step, total, target, candidate["name"],
                   row.get("body_text") or refusal))
    document = {
        "task": "o13",
        "measured": measured,
        "rule": ("the renderer picks, per target and per departing "
                 "path, among the candidates of that path's OUTCOME "
                 "KIND whose emitted body carries the arch mnemonic "
                 "the path's own departing line carries, the one whose "
                 "emitted body is SHORTEST -- the same probe function "
                 "is compiled for every candidate and for a baseline "
                 "with no guard at all, so the instruction counts are "
                 "directly comparable and the pick is measured"),
        "clang": E.SHIP_FLAGS_SOURCE,
        "rustc": RR.SHIP_FLAGS_SOURCE,
        "collector_peak_kb": peak_kb(),
    }
    write_json(FACTS, document)
    say("   wrote %s" % FACTS)
    return 0


MEASURED = {}


def measured_spellings():
    if "rows" not in MEASURED:
        MEASURED["rows"] = read_json(FACTS)["measured"]
    return MEASURED["rows"]


def spelling_for(target, outcome):
    """the source this target uses for one departing path's outcome:
    among the measured candidates of that outcome's KIND whose emitted
    body carries the mnemonic the departing line carries, the one whose
    emitted body is shortest."""
    fits = []
    for row in measured_spellings()[target]:
        if row.get("refusal"):
            continue
        if row.get("kind") != outcome["kind"]:
            continue
        if not carries(row, outcome["mnem"]):
            continue
        fits.append(row)
    if not fits:
        return None
    fits.sort(key=lambda one: one.get("body_line_count") or 0)
    chosen = fits[0]
    for candidate in CANDIDATES[target]:
        if candidate["name"] != chosen["name"]:
            continue
        declares = candidate["declares"]
        text = candidate["text"]
        callee = outcome.get("callee")
        if "%s" in declares:
            declares = declares % callee
        if "%s" in text:
            text = text % callee
        return {"name": candidate["name"], "declares": declares,
                "text": text,
                "body_line_count": chosen.get("body_line_count")}
    return None


# ==================================================================
# section 4: THE TWO MODE RENDERERS   two overrides each
# ==================================================================

class ModeRendererC(E.Renderer):
    """task o7's `emulate.Renderer` with the guard in front of the
    answer.  Everything else -- the width plan, the free-symbol check,
    the refusal causes, every `emit_*` -- is inherited unchanged, so an
    x unit with no departing path renders exactly the source task o7
    rendered.

    attributes:
        guard_paths     one entry per departing path: its z3 condition
                        and the source text of its outcome
        guard_declares  the file-scope declarations those outcomes need
    methods:
        plan_parameters the base plan, over the guard's reads as well
        guard_lines     the source lines the mode adds
        render          -> (source text, function symbol)
    """

    def __init__(self, families, result_family, result_width, label):
        E.Renderer.__init__(self, families, result_family, result_width,
                            label)
        self.guard_paths = []
        self.guard_declares = []

    def plan_parameters(self, term):
        for path in self.guard_paths:
            self.collect_uses(path["condition"], None)
        E.Renderer.plan_parameters(self, term)

    def guard_lines(self):
        lines = []
        for path in self.guard_paths:
            text, kind, _width = self.emit(path["condition"])
            if kind != "bool":
                raise E.Refused(CAUSE_GUARD_SORT, kind)
            lines.append("    if (%s) { %s }" % (text, path["text"]))
        return lines

    def render(self, term, text):
        self.plan_parameters(term)
        self.check_symbols(term)
        for path in self.guard_paths:
            self.check_symbols(path["condition"])
        root_text, root_kind, root_width = self.emit(term)
        return_type, body = self.answer(root_text, root_kind, root_width)
        guard = self.guard_lines()
        symbol = "emu_%s" % self.label
        lines = []
        lines.append("/* task o13 emulation WITH THE MODE -- rendered "
                     "by mode.py ModeRendererC from the layer-4 term")
        lines.append("   of %s, and from the guard the reference read "
                     "off the x unit's own body." % self.label)
        lines.append("   The term's layer-5 text, LITERAL:")
        lines.append("   %s */" % text)
        lines.append("#include <stdint.h>")
        if self.helpers:
            lines.append("#include <string.h>")
        for declaration in self.guard_declares:
            lines.append(declaration)
        for helper in sorted(self.helpers):
            lines.append(self.helper_text(helper))
        params = []
        for param in self.params:
            params.append("%s %s" % (param["holder"], param["name"]))
        if not params:
            params.append("void")
        lines.append("")
        lines.append("%s" % return_type)
        lines.append("%s(%s)" % (symbol, ", ".join(params)))
        lines.append("{")
        for line in guard:
            lines.append(line)
        lines.append("    return %s;" % body)
        lines.append("}")
        lines.append("")
        return "\n".join(lines), symbol


class ModeRendererRust(RR.RustRenderer):
    """task o11's `rust_render.RustRenderer` with the guard in front of
    the answer: the same two overrides, in rust's own spelling.

    attributes:
        (every one of `ModeRendererC`, plus `RustRenderer.blocks`)
    methods:
        plan_parameters the base plan, over the guard's reads as well
        guard_lines     the source lines the mode adds
        render          -> (source text, function symbol)
    """

    def __init__(self, families, result_family, result_width, label):
        RR.RustRenderer.__init__(self, families, result_family,
                                 result_width, label)
        self.guard_paths = []
        self.guard_declares = []

    def plan_parameters(self, term):
        for path in self.guard_paths:
            self.collect_uses(path["condition"], None)
        RR.RustRenderer.plan_parameters(self, term)

    def guard_lines(self):
        lines = []
        for path in self.guard_paths:
            text, kind, _width = self.emit(path["condition"])
            if kind != "bool":
                raise E.Refused(CAUSE_GUARD_SORT, kind)
            lines.append("    if %s { %s }" % (text, path["text"]))
        return lines

    def render(self, term, text):
        self.plan_parameters(term)
        self.check_symbols(term)
        for path in self.guard_paths:
            self.check_symbols(path["condition"])
        root_text, root_kind, root_width = self.emit(term)
        return_type, body = self.answer(root_text, root_kind, root_width)
        guard = self.guard_lines()
        symbol = "emu_%s" % self.label
        params = []
        for param in self.params:
            params.append("%s: %s" % (param["name"], param["holder"]))
        lines = []
        lines.append(RR.RUST_PRELUDE)
        for declaration in self.guard_declares:
            lines.append(declaration)
        lines.append("")
        lines.append("// task o13 emulation WITH THE MODE -- rendered "
                     "by mode.py")
        lines.append("// ModeRendererRust from the layer-4 term of %s,"
                     % self.label)
        lines.append("// and from the guard the reference read off the "
                     "x unit's own body.")
        lines.append("// The term's layer-5 text, LITERAL:")
        lines.append("//   %s" % " ".join(text.split()))
        lines.append("#[no_mangle]")
        lines.append("pub extern \"C\" fn %s(%s) -> %s"
                     % (symbol, ", ".join(params), return_type))
        lines.append("{")
        for line in guard:
            lines.append(line)
        lines.append("    %s" % body)
        lines.append("}")
        lines.append("")
        return "\n".join(lines), symbol


def dress_renderer(renderer, target, paths, record):
    """put the mode on a renderer: one guard line per departing path,
    each with its own condition and its own outcome, and the
    declarations those outcomes need."""
    outcomes = [outcome_of_path(path) for path in paths]
    record["departing_paths"] = [
        {"line": p["line"], "went_to": p["went_to"],
         "condition": p["condition"]} for p in paths]
    record["guard_outcomes"] = outcomes
    usable = []
    unspelled = []
    declares = []
    for index, path in enumerate(paths):
        if path.get("condition_term") is None:
            unspelled.append("%s leaves on every input"
                             % (path.get("line"),))
            continue
        spelling = spelling_for(target, outcomes[index])
        if spelling is None:
            unspelled.append("no measured spelling emits %r for %s"
                             % (outcomes[index]["mnem"],
                                outcomes[index]["kind"]))
            continue
        usable.append({"condition": path["condition_term"],
                       "text": spelling["text"],
                       "spelling": spelling["name"],
                       "outcome": outcomes[index]})
        if spelling["declares"] and spelling["declares"] not in declares:
            declares.append(spelling["declares"])
    record["guard_unspelled"] = unspelled
    if not usable:
        if not paths:
            record["mode"] = MODE_NONE
        else:
            record["mode"] = ("the guard could not be rendered: %s"
                              % "; ".join(unspelled))
        return renderer
    renderer.guard_paths = usable
    renderer.guard_declares = declares
    record["mode"] = MODE_RENDERED
    record["guard_conditions"] = ["%s" % one["condition"]
                                  for one in usable]
    record["guard_spellings_used"] = [one["spelling"] for one in usable]
    return renderer


# ==================================================================
# section 5: THE GUARDED READING   the posing a guard means something to
# ==================================================================

def left_the_unit_like(answer):
    """the ONE shared value that stands for "this side did not answer:
    it left down its guard path".  One symbol, the same on both sides,
    so two units that leave on the same inputs agree there by
    construction and two that leave on different inputs do not."""
    if z3.is_bv(answer):
        whole = z3.BitVec("left_the_unit", 128)
        return z3.Extract(answer.size() - 1, 0, whole)
    return z3.Const("left_the_unit_of_%s" % answer.sort(), answer.sort())


def guarded_answer(answer, condition):
    if condition is None:
        return answer
    return z3.If(condition, left_the_unit_like(answer), answer)


KEEP = {}


def prove_under_the_guard(gate, maker, reference, canon, x_record,
                          params, x_term, x_families, emu_paths,
                          x_paths, P100, G):
    """THE SECOND POSING.  Both sides' answers are the reference's, as
    in the first posing; each is then replaced, where that side's own
    guard fires, by the one shared `left_the_unit` value, and the two
    guarded answers go to `gate.decide` unchanged."""
    out = {"route": {}, "outcome": None}
    emu_answer, cause = E.body_answer(reference, canon)
    if emu_answer is None:
        walked = maker.transcribe(canon)
        if walked.out_term is None:
            out["outcome"] = "UNDECIDED"
            out["cause"] = ("emulation side: %s; and no term either"
                            % cause)
            return out
        emu_answer = walked.out_term
        out["route"]["emulation"] = ("its transcribed term (the "
                                     "reference refused: %s)" % cause)
    else:
        out["route"]["emulation"] = "the reference's answer for its body"
    x_answer, cause = E.body_answer(reference, x_record)
    if x_answer is None:
        x_answer = x_term
        out["route"]["x"] = ("its transcribed term, proved by route two "
                             "(the reference refused: %s)" % cause)
    else:
        out["route"]["x"] = "the reference's answer for its body"
    emu_condition, _always = guard_condition_of(emu_paths)
    x_condition, _always = guard_condition_of(x_paths)
    if emu_condition is None:
        out["emulation_guard"] = None
    else:
        out["emulation_guard"] = "%s" % emu_condition
    if x_condition is None:
        out["x_guard"] = None
    else:
        out["x_guard"] = "%s" % x_condition
    emu_answer = guarded_answer(emu_answer, emu_condition)
    x_answer = guarded_answer(x_answer, x_condition)
    c_families = E.expected_c_families(params)
    x_rows = P100.input_rows(x_families)
    c_rows = P100.input_rows(c_families)
    disagreement = P100.rows_disagree(x_rows, c_rows)
    if disagreement is not None:
        out["outcome"] = "UNDECIDED"
        out["cause"] = "the IN rows cannot be aligned: %s" % disagreement
        return out
    _in, _shared, constants_x, _other = P100.classify_symbols(
        x_answer, x_families)
    _in, _shared, constants_c, _other = P100.classify_symbols(
        emu_answer, c_families)
    x_answer, _names = P100.rename_constants_apart(x_answer, constants_x,
                                                  "x")
    emu_answer, _names = P100.rename_constants_apart(emu_answer,
                                                     constants_c, "c")
    x_aligned = P100.align_by_row(x_answer, x_rows)
    c_aligned = P100.align_by_row(emu_answer, c_rows)
    KEEP["x_aligned"] = x_aligned
    KEEP["c_aligned"] = c_aligned
    KEEP["x_condition"] = x_condition
    KEEP["emulation_condition"] = emu_condition
    if not gate.comparable(c_aligned, x_aligned):
        out["outcome"] = "UNDECIDED"
        out["cause"] = ("the two answers are of different z3 sorts (%s "
                        "against %s)" % (c_aligned.sort(),
                                         x_aligned.sort()))
        return out
    verdict = gate.decide(
        c_aligned, x_aligned,
        "the emulation's guarded answer against the x unit's guarded "
        "answer, inputs aligned by IN row",
        "z3 proved the two sides leave the unit on the same inputs and "
        "answer alike on every other input")
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
        narrow.append({"row": "IN-%d" % index, "holder": param["holder"]})
        substitution.append((row, z3.ZeroExt(64 - param["bits"],
                                             z3.Extract(param["bits"] - 1,
                                                        0, row))))
    if not substitution:
        return out
    again = gate.decide(
        z3.substitute(c_aligned, *substitution),
        z3.substitute(x_aligned, *substitution),
        "the same guarded posing, with every narrow-holder input row "
        "zero-extended from its holder width (the caller-extension "
        "rule task o7 measured)",
        "z3 proved the two guarded answers equal for every input whose "
        "narrow arguments are zero-extended to the register")
    out["under_caller_extension"] = {
        "narrow_rows": narrow,
        "outcome": again.outcome,
        "reason": again.reason,
        "counterexample": again.counterexample,
    }
    return out


# ==================================================================
# section 6: THE WORKER   one entry's whole work, inside the fork
# ==================================================================

TARGET = {"name": "c"}


def install_worker(target):
    """bind this task's worker and memory ceiling into task o7's
    collector.  `emulate.fork_one` calls the module-global
    `one_emulation` and `emulate.collect` calls the module-global
    `check_collector_memory`; these two assignments are the ONLY way
    the imported collector is changed, and neither emulate.py nor
    rust_render.py is edited on disk."""
    TARGET["name"] = target
    E.one_emulation = one_mode_emulation
    E.check_collector_memory = check_collector_memory


def one_mode_emulation(shared, job):
    """the whole of one entry's work with the mode: read the x body's
    departing paths, render the term WITH the guard, compile, carve,
    wrap, transcribe, then both postings of the proof.  Runs inside the
    fork."""
    import term as T
    import term66_run as TR
    import canonical_form as CF
    import pool100_entry_equivalence as P100
    import gate as G
    target = TARGET["name"]
    maker = shared["maker"]
    gate = shared["gate"]
    form = shared["form"]
    reference = shared["reference"]
    held = shared["held"]
    entry_id = job["entry_id"]
    x_unit = job["x_unit"]
    record = {
        "entry_id": entry_id,
        "target": target,
        "x_lang": job["x_lang"],
        "x_unit": x_unit,
        "x_text": job["text"],
        "entry_texts": job["entry_texts"],
        "type_key": job["type_key"],
        "earlier": job.get("earlier"),
        "control": False,
    }
    x_record = held.get(x_unit)
    if x_record is None:
        record["rendered"] = False
        record["refusal_cause"] = E.CAUSE_NO_TERM
        record["refusal_detail"] = "no canon40 record held for %s" % x_unit
        return record
    unit = dict(x_record)
    unit["unit"] = x_unit
    record["x_body_text"] = x_record.get("body_text")
    record["x_body_bytes"] = x_record.get("body_bytes")
    record["x_body_verbatim"] = x_record.get("body_verbatim")
    record["x_result_family"] = x_record.get("result_family")
    record["x_result_width"] = x_record.get("result_width")
    walked = maker.transcribe(unit)
    if walked.refused is not None or walked.out_term is None:
        record["rendered"] = False
        record["refusal_cause"] = E.CAUSE_NO_TERM
        record["refusal_detail"] = "the x unit carries no term today"
        return record
    x_term = walked.out_term
    try:
        x_paths = departing_paths(reference, unit)
    except Exception as problem:                         # noqa: BLE001
        record["rendered"] = False
        record["refusal_cause"] = CAUSE_GUARD_REFUSED
        record["refusal_detail"] = "%s: %s" % (type(problem).__name__,
                                               problem)
        return record
    ordered = T.order_commutative(z3.simplify(x_term))
    families, omitted = E.families_the_term_reads(x_record, x_term)
    record["x_in_rows"] = families
    record["x_contract_omits"] = omitted
    label = "%s__%s__%s" % (target, entry_id, E.sanitize(x_unit))
    if target == "c":
        renderer = ModeRendererC(families, x_record.get("result_family"),
                                 x_record.get("result_width"), label)
    else:
        renderer = ModeRendererRust(families,
                                    x_record.get("result_family"),
                                    x_record.get("result_width"), label)
    dress_renderer(renderer, target, x_paths, record)
    try:
        source, symbol = renderer.render(ordered, job["text"])
    except E.Refused as refusal:
        record["rendered"] = False
        record["refusal_cause"] = refusal.cause
        record["refusal_detail"] = refusal.detail
        return record
    record["rendered"] = True
    record["params"] = renderer.params
    suffix = ".c" if target == "c" else ".rs"
    record["source_path"] = os.path.join("src", label + suffix)
    record["source"] = source
    handle = open(os.path.join(SRC_DIR, label + suffix), "w")
    handle.write(source)
    handle.close()
    if target == "c":
        got, refusal = E.compile_and_carve(source, symbol)
    else:
        got, refusal = RR.compile_and_carve(source, symbol)
    if got is None:
        record["compiled"] = False
        record["compile_refusal"] = refusal
        return record
    record["compiled"] = True
    raw_bytes, mnem = got
    record["body_bytes"] = " ".join(raw_bytes)
    record["body_text"] = "; ".join(mnem)
    record["body_byte_count"] = len(raw_bytes)
    record["body_opcodes"] = opcodes_of(mnem)
    emu_label = "%s/%s" % (target, label)
    if target == "c":
        recorded = E.recorded_facts(emu_label, label, raw_bytes, mnem)
    else:
        recorded = RR.recorded_facts(emu_label, label, raw_bytes, mnem)
    canon = CF.render_one(form, gate, recorded)
    canon["unit"] = emu_label
    record["canon40_outcome"] = canon.get("outcome")
    term_record = TR.one_unit(maker, gate, emu_label, canon)
    record["term_state"] = term_record.get("term_state")
    record["layer5_text"] = term_record.get("layer5_normalized_text")
    try:
        emu_paths = departing_paths(reference, canon)
    except Exception as problem:                         # noqa: BLE001
        emu_paths = []
        record["emulation_walk"] = "%s: %s" % (type(problem).__name__,
                                               problem)
    record["emulation_departing_paths"] = [
        {"line": p["line"], "went_to": p["went_to"],
         "condition": p["condition"]} for p in emu_paths]
    record["q3"] = E.prove_against_x(reference, gate, maker, canon,
                                     x_record, renderer.params, x_term,
                                     walked, P100, G, families)
    record["q3_guarded"] = prove_under_the_guard(
        gate, maker, reference, canon, x_record, renderer.params, x_term,
        families, emu_paths, x_paths, P100, G)
    return record


def build_shared(target):
    if target == "c":
        shared = E.build_shared()
    else:
        shared = RR.build_shared()
    shared["reference"] = make_mode_reference(shared["reference"])
    return shared


def run(target, solver_ms=None):
    """the re-run.  `solver_ms` raises the gate's own solver ceiling and
    writes to its own file, so an UNDECIDED that is a TIME LIMIT can be
    re-posed with more room and the two answers compared -- the limit is
    a flag, never an answer."""
    say("-- RUN %s: the emulations %s recorded DISPROVED"
        % (target, EARLIER[target]["log"]))
    install_worker(target)
    measured_spellings()
    population = read_json(POPULATION)
    jobs = population["disproved"][target]
    say("   %d jobs" % len(jobs))
    shared = build_shared(target)
    path = RUN_C if target == "c" else RUN_RUST
    if solver_ms is not None:
        shared["gate"].solver_timeout_ms = int(solver_ms)
        path = os.path.join(HERE, "mode_run_%s_%s_ms.json"
                            % (target, solver_ms))
        say("   the gate's solver ceiling is raised to %s ms for this "
            "run" % solver_ms)
    say("   shared objects built; collector peak %d kB" % peak_kb())
    results = E.collect(shared, jobs, "mode " + target)
    write_json(path, {"task": "o13", "target": target,
                      "solver_timeout_ms": solver_ms,
                      "results": results,
                      "collector_peak_kb": peak_kb()})
    say("   wrote %s" % path)
    return 0


def diagnose(target, entry_ids):
    """the values in motion for one emulation the guarded posing does
    not prove: the two guarded answers, the two guard conditions, and
    every one of them evaluated at the solver's own model."""
    say("-- DIAGNOSE %s: %s" % (target, ", ".join(entry_ids)))
    install_worker(target)
    measured_spellings()
    population = read_json(POPULATION)
    plans = {}
    for job in population["disproved"][target]:
        plans[job["entry_id"]] = job
    shared = build_shared(target)
    out = []
    step = 0
    for entry_id in entry_ids:
        step = step + 1
        say("[%d/%d] %s" % (step, len(entry_ids), entry_id))
        KEEP.clear()
        record = one_mode_emulation(shared, plans[entry_id])
        row = {"entry_id": entry_id, "target": target,
               "x_unit": record["x_unit"],
               "x_body_text": record.get("x_body_text"),
               "body_text": record.get("body_text"),
               "mode": record.get("mode"),
               "guarded_outcome": (record.get("q3_guarded") or {}).get(
                   "outcome")}
        x_aligned = KEEP.get("x_aligned")
        c_aligned = KEEP.get("c_aligned")
        if x_aligned is None:
            row["walk"] = "the guarded posing never reached two aligned "\
                          "answers"
            out.append(row)
            continue
        substitution = []
        for index, param in enumerate(record["params"]):
            if param["kind"] != "bv":
                continue
            if param["bits"] >= 32:
                continue
            whole = z3.BitVec("IN_%d" % index, 64)
            substitution.append((whole,
                                 z3.ZeroExt(64 - param["bits"],
                                            z3.Extract(param["bits"] - 1,
                                                       0, whole))))
        if substitution:
            x_aligned = z3.substitute(x_aligned, *substitution)
            c_aligned = z3.substitute(c_aligned, *substitution)
            row["posing"] = "with the caller-extension rule applied"
        else:
            row["posing"] = "as posed"
        solver = z3.Solver()
        solver.set("timeout", 60000)
        solver.add(x_aligned != c_aligned)
        answer = solver.check()
        row["solver"] = "%s" % answer
        if answer != z3.sat:
            out.append(row)
            continue
        model = solver.model()
        row["model"] = "%s" % model
        row["at_the_model"] = {
            "the x unit's guarded answer": "%s" % model.eval(x_aligned,
                                                             True),
            "the emulation's guarded answer": "%s"
            % model.eval(c_aligned, True),
        }
        for name, condition in (("the x unit's guard",
                                 KEEP.get("x_condition")),
                                ("the emulation's guard",
                                 KEEP.get("emulation_condition"))):
            if condition is None:
                row["at_the_model"][name] = "none"
                continue
            if substitution:
                condition = z3.substitute(condition, *substitution)
            row["at_the_model"][name] = "%s" % model.eval(condition, True)
        say("   %s" % json.dumps(row["at_the_model"], sort_keys=True))
        out.append(row)
    path = os.path.join(HERE, "mode_diagnose_%s.json" % target)
    write_json(path, {"task": "o13", "target": target, "rows": out,
                      "collector_peak_kb": peak_kb()})
    say("   wrote %s" % path)
    return 0


# ==================================================================
# section 7: THE REPORT
# ==================================================================

def outcome_word(record):
    """the re-run's verdict for one emulation, in the gate's own three
    words.  The posing that proved it is named beside it, never instead
    of it."""
    guarded = record.get("q3_guarded") or {}
    plain = record.get("q3") or {}
    pairs = ((plain, "the first posing"),
             (guarded, "the guarded posing"))
    for source, name in pairs:
        if source.get("outcome") == "PROVED_ON_SHIP":
            return "PROVED_ON_SHIP", name
    for source, name in pairs:
        extension = source.get("under_caller_extension") or {}
        if extension.get("outcome") == "PROVED_ON_SHIP":
            return "PROVED_ON_SHIP", name + ", under caller extension"
    if guarded.get("outcome") == "UNDECIDED":
        return "UNDECIDED", "the guarded posing"
    if plain.get("outcome") == "UNDECIDED":
        return "UNDECIDED", "the first posing"
    return "DISPROVED", "both postings"


def pipe_table(header, rows):
    lines = ["| " + " | ".join(header) + " |",
             "|" + "|".join(["---"] * len(header)) + "|"]
    for row in rows:
        lines.append("| " + " | ".join("%s" % cell for cell in row)
                     + " |")
    return lines


def per_target_row(target, records):
    rendered = [r for r in records if r.get("rendered")]
    with_mode = [r for r in rendered if r.get("mode") == MODE_RENDERED]
    compiled = [r for r in rendered if r.get("compiled")]
    proved = []
    disproved = []
    undecided = []
    for record in records:
        if not record.get("compiled"):
            continue
        word, _why = outcome_word(record)
        if word == "PROVED_ON_SHIP":
            proved.append(record)
            continue
        if word == "UNDECIDED":
            undecided.append(record)
            continue
        disproved.append(record)
    return [target, len(records), len(rendered), len(with_mode),
            len(compiled), len(proved), len(disproved), len(undecided)]


def cause_of(record):
    """why this emulation is still disproved, by cause, read off the
    record and never guessed."""
    if record.get("mode") == MODE_RENDERED:
        return ("the mode is rendered and the two sides still differ "
                "off the guarded region")
    if record.get("mode") == MODE_NONE:
        return "the x body has no departing path: there is no mode"
    return "the mode could not be rendered: %s" % record.get("mode")


def report():
    say("-- REPORT")
    population = read_json(POPULATION)
    document = {
        "task": "o13",
        "node": ("hq.research.arch_unit_oracle.cross_construction."
                 "autopoly"),
        "kinds_by_outcome": population["kinds_by_outcome"],
        "facts": read_json(FACTS)["measured"],
        "runs": {},
    }
    for target, path in (("c", RUN_C), ("rust", RUN_RUST)):
        if not os.path.exists(path):
            continue
        document["runs"][target] = read_json(path)["results"]
    write_json(RESULTS, document)
    lines = []
    lines.append("# task o13 -- the mode rendered into the emulation")
    lines.append("")
    lines.append("Generated by `mode.py report`; never hand-edited. "
                 "Folder: `%s`." % HOST_FOLDER)
    lines.append("")
    lines.append("## 1. The guard-outcome vocabulary, off the ledgers "
                 "of the disproved units")
    lines.append("")
    rows = []
    for entry in population["kinds_by_outcome"]:
        rows.append([entry["guard_kind"], entry["outcome"],
                     entry["how_many"]])
    lines.extend(pipe_table(["guard kind: setter reader, on the blocks "
                             "the setter read", "outcome",
                             "how many"], rows))
    lines.append("")
    lines.append("## 2. The outcome spellings, measured")
    lines.append("")
    rows = []
    for target in ("c", "rust"):
        for row in document["facts"][target]:
            body = row.get("body_text")
            if body is None:
                body = "REFUSED: %s" % row.get("refusal")
            rows.append([target, row["name"], row["kind"], body])
    lines.extend(pipe_table(["target", "spelling", "outcome kind",
                             "the emitted body"], rows))
    lines.append("")
    lines.append("## 3. The re-run")
    lines.append("")
    rows = []
    for target in ("c", "rust"):
        records = document["runs"].get(target)
        if records is None:
            continue
        rows.append(per_target_row(target, records))
    lines.extend(pipe_table(["target", "disproved before", "rendered",
                             "rendered with a mode", "compiled",
                             "proved after", "still disproved",
                             "undecided"], rows))
    lines.append("")
    lines.append("## 4. Proved after, by which posing")
    lines.append("")
    counts = {}
    for target in ("c", "rust"):
        for record in document["runs"].get(target) or []:
            if not record.get("compiled"):
                continue
            word, why = outcome_word(record)
            if word != "PROVED_ON_SHIP":
                continue
            key = (target, why)
            counts[key] = counts.get(key, 0) + 1
    rows = []
    for key in sorted(counts):
        rows.append([key[0], key[1], counts[key]])
    lines.extend(pipe_table(["target", "the posing that proved it",
                             "how many"], rows))
    lines.append("")
    lines.append("## 5. Still disproved, by cause")
    lines.append("")
    causes = {}
    for target in ("c", "rust"):
        for record in document["runs"].get(target) or []:
            if not record.get("compiled"):
                continue
            word, _why = outcome_word(record)
            if word != "DISPROVED":
                continue
            key = (target, cause_of(record))
            causes.setdefault(key, [])
            causes[key].append("%s (%s)" % (record["entry_id"],
                                            record["x_unit"]))
    rows = []
    for key in sorted(causes):
        members = causes[key]
        shown = ", ".join(members[:6])
        if len(members) > 6:
            shown = shown + ", and %d more" % (len(members) - 6)
        rows.append([key[0], key[1], len(members), shown])
    lines.extend(pipe_table(["target", "cause", "how many", "which"],
                            rows))
    lines.append("")
    lines.append("## 6. Undecided, by cause")
    lines.append("")
    causes = {}
    for target in ("c", "rust"):
        for record in document["runs"].get(target) or []:
            if not record.get("compiled"):
                continue
            word, _why = outcome_word(record)
            if word != "UNDECIDED":
                continue
            source = record.get("q3_guarded") or {}
            key = (target, source.get("cause") or source.get("reason"))
            causes[key] = causes.get(key, 0) + 1
    rows = []
    for key in sorted(causes, key=lambda one: "%s" % (one,)):
        rows.append([key[0], key[1], causes[key]])
    lines.extend(pipe_table(["target", "cause", "how many"], rows))
    lines.append("")
    lines.append("## 7. Per pool entry touched: its modes")
    lines.append("")
    rows = []
    seen = []
    for target in ("c", "rust"):
        for record in document["runs"].get(target) or []:
            key = (record["entry_id"], record["x_unit"])
            if key in seen:
                continue
            seen.append(key)
            unit = population["units"].get(record["x_unit"]) or {}
            kinds = []
            for guard_row in unit.get("ledger_guard_rows") or []:
                kinds.append(kind_of(guard_row))
            if not kinds:
                continue
            rows.append([record["entry_id"], record["x_unit"],
                         record["type_key"], "; ".join(kinds),
                         unit.get("outcome_kinds")])
    lines.extend(pipe_table(["pool entry", "x unit", "type key",
                             "its modes: the guard kinds",
                             "the outcome"], rows))
    lines.append("")
    lines.append("## 8. The pool entries with no mode")
    lines.append("")
    with_mode = set(row[0] for row in rows)
    without = []
    for target in ("c", "rust"):
        for record in document["runs"].get(target) or []:
            if record["entry_id"] in with_mode:
                continue
            without.append(record["entry_id"])
    lines.append("- %d of the %d emulations re-run are of an x unit "
                 "whose ledger carries no branch guard row, so there is "
                 "no mode to render and the mode renderer writes task "
                 "o7's and task o11's own source."
                 % (len(without), sum(len(document["runs"].get(t) or [])
                                      for t in ("c", "rust"))))
    lines.append("")
    lines.append("## 9. Bounds")
    lines.append("")
    lines.append("- The stated bound: one collecting process, its peak "
                 "resident size checked after every emulation, named "
                 "abort `ABORT_MEMORY_O13` at %d kB (4 GB)."
                 % COLLECTOR_CAP_KB)
    for target, path in (("c", RUN_C), ("rust", RUN_RUST)):
        if not os.path.exists(path):
            continue
        peak = read_json(path)["collector_peak_kb"]
        lines.append("- Collector peak resident size, "
                     "`resource.getrusage(RUSAGE_SELF).ru_maxrss`, the "
                     "%s run: %d kB." % (target, peak))
    lines.append("- Each emulation ran in its own forked sub-process "
                 "under `RLIMIT_AS` %d MB and a wall clock of %d s, at "
                 "most %d at once."
                 % (E.SUB_CEILING_MB, E.SUB_SECONDS, E.WORKERS))
    lines.append("")
    handle = open(REPORT, "w")
    handle.write("\n".join(lines))
    handle.close()
    say("   wrote %s and %s" % (RESULTS, REPORT))
    return 0


def main(argv):
    if len(argv) < 2:
        say(__doc__)
        return 2
    command = argv[1]
    if command == "vocabulary":
        return vocabulary()
    if command == "facts":
        return facts()
    if command == "run":
        if len(argv) > 3:
            return run(argv[2], argv[3])
        return run(argv[2])
    if command == "diagnose":
        return diagnose(argv[2], argv[3:])
    if command == "report":
        return report()
    say("unknown command %r" % command)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
