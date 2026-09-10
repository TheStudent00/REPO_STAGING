#!/usr/bin/env python3
"""hub2.py -- task hub2: Hub v2, the dictionary at two levels.

Node: hq.research.arch_unit_oracle.hub_compiler
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_1_hub_compiler/`)
and its four sub-nodes front_end, dictionary, joiner, oracle_test.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_hub2_brief.md`.
Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`.

THE OBJECTS, one sentence each, in relation.  The first three are task
hub1's and are restated because this file is read beside it.

  * A CELL is one (`mnem`, operand shape, `key_width`) row of the
    arch-opcode model table -- the machine-form key ruled 2026-09-08.
  * A WRITTEN PLACE is one destination an opcode writes (`reg_rdi`,
    `flags`, `x87_7`); the gate answers per place, and only a place
    whose name begins `reg_` is a value a composition can pass on.
  * A CERTIFICATE is task bank1's record about ONE artifact: one
    (cell, target, written place) with the term it was posed on, the
    rendered source and its sha256, the compiler and its flags, the
    carved body and the gate's verdict.  THE BANK
    (`.../autopoly/certificates.jsonl`) holds every certificate of every
    pass, the strongest per key marked `preferred`.  From this task on
    the dictionary is READ FROM THE BANK.
  * A PAIR is (setter cell, consumer cell): the arch opcode that writes
    a flag state and the arch opcode that reads it, which the corpus's
    own ledgers record as one row whose `produced_by.mnem` is the two of
    them.  The loop renders a consumer's emulation over ONE setter and
    the rendered function is the comparison then the select, so no flag
    state crosses a node: the pair IS the node.
  * A POOL ENTRY is one distinct computation of `the_pool5.json`, the
    units proved equal collapsed to one entry.  Task o7 rendered an
    emulation of an entry in c, task o11 in rust, task o13 re-rendered
    the disproved ones with the MODE (the guard) in place.
  * THE DICTIONARY, at two levels: level one is per (target, cell) --
    task hub1's -- and level two is per (target, pool entry).  Between
    them sits the PAIR, which is level one keyed by the pair rather than
    by the consumer alone.  A node resolves to a cell, else to a pair,
    else to its unit's pool entry.
  * THE HOLDERS: every entry records the parameter holders the proof was
    made over, and the composition refuses a mismatch BY CAUSE.

WHAT IS REUSED RATHER THAN COPIED, said out loud.  `hub.py` is task
hub1's file, in this same folder, and is IMPORTED and never edited: its
corpus reader (`go_units_held`, `go_probes`, `cells_of_units`), its front
end (tree-sitter's tree joined to go/types' types by position), its
candidate index and its source-to-source agreement, its composed-file
furniture, and its gate call (`build_shared`, `carve`, `wrapped`,
`gate_two_bodies`, `verdict_word`).  `model_table`, `ledger`,
`canonical_form`, `emulate`, `rust_render`, `go_render`, `handful`,
`term97_walk`, `pool100_entry_equivalence` and `gate` are imported as
task hub1 imports them.  NOTHING outside this file is edited.

THE HOLDER TABLE IS THIS FILE'S OWN, and it is task hub1's table with
one holder added: `bool`, go's truth holder, which a comparison's own
result sits in.  Task hub1 never met it because no node it composed
answered with one.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections, type
pairs) or from ratified intention -- never from the token.  The token
appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse its
own output on failure.  A brief handed to any subagent for this line MUST
paste this paragraph verbatim."

HOW THIS FILE OBEYS IT, said mechanically, and the PAIR is the place to
look because a pair is a pairing and the ban names pairings.

  * A pair's key is TWO CELLS -- (setter mnem, setter shape, setter
    key_width, consumer mnem, consumer shape, consumer key_width) -- and
    a cell is the machine-form key ruled 2026-09-08, whose `mnem` field
    the guard passes over by name as machine form.  Which two cells make
    a pair is
    read off the CORPUS's own ledger row, whose `produced_by.mnem` is
    the setter then the consumer as the ledgerer wrote it from the
    unit's own body.  No source operator token enters it.
  * A body-level key is a POOL ENTRY ID (`E00316`).
  * The CANDIDATE SET for resolving a typed operator node is task hub1's
    and is unchanged: the TYPE TUPLE (arity, lhs holder, rhs holder,
    result holder), which the ban names as machine-form evidence; within
    it the front end parses the candidate corpus unit's own go source
    with the same grammar and compares the two operator nodes as a
    parser does, between two source files.  The answer is a NAMED CORPUS
    UNIT.  WHICH LEVEL serves that unit is decided by what the
    dictionary holds for it, never by anything about the node.

MEMORY BOUND, stated as the law requires: one collecting process, peak
checked after every unit of work, named abort ABORT_MEMORY_HUB2 at 6 GB
resident (`resource.getrusage`; `/usr/bin/time` is absent in the image).
The pool is the largest store held whole (32 MB of json) and is dropped
as soon as the unit-to-entry index is built; the bank and the run stores
are streamed line by line.

Coding discipline: no compound one-liner statements.

usage:
  hub2.py dictionary       dictionary2.json + dictionary2.md
  hub2.py handful          the handful: front end, resolve, compose, gate
  hub2.py measure [n]      the measure over the corpus's own go units
  hub2.py tables           oracle_test2.md
"""

import collections
import hashlib
import json
import os
import re
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import hub as HUB1                                          # noqa: E402

HQ = HUB1.HQ
OP = HUB1.OP
ARCH = HUB1.ARCH
EMU = HUB1.EMU
AUTO = HUB1.AUTO

CERTIFICATES = os.path.join(AUTO, "certificates.jsonl")
AP5_RUNS = os.path.join(AUTO, "autopoly5_runs.jsonl")
POOL = os.path.join(OP, "the_pool5.json")
O7 = os.path.join(EMU, "emulation_results.json")
O7_POPULATION = os.path.join(EMU, "emulation_population.json")
O11 = os.path.join(EMU, "rust", "rust_run.json")
O11_POPULATION = os.path.join(EMU, "rust", "rust_population.json")
O13 = os.path.join(EMU, "mode", "mode_results.json")
SINGLE = HUB1.SINGLE

HANDFUL_DIR = HUB1.HANDFUL_DIR
HANDFUL_GO = HUB1.HANDFUL_GO
DICTIONARY2 = os.path.join(HERE, "dictionary2.json")
DICTIONARY2_MD = os.path.join(HERE, "dictionary2.md")
ORACLE2_JSON = os.path.join(HERE, "oracle_test2.json")
ORACLE2_MD = os.path.join(HERE, "oracle_test2.md")
MEASURE2_JSON = os.path.join(HERE, "measure2.json")

TARGETS = ["c", "rust", "go"]
PROVED_WORDS = ("PROVED", "PROVED_ON_SHIP")
CERTIFIED = ("proved", "proved_under_caller_extension")

BOUND_KB = 6 * 1024 * 1024
ABORT = "ABORT_MEMORY_HUB2"

say = HUB1.say
read_json = HUB1.read_json
write_json = HUB1.write_json
pipe_table = HUB1.pipe_table
cell_label = HUB1.cell_label
peak_kb = HUB1.peak_kb
Refused = HUB1.Refused


def check_memory(where):
    peak = peak_kb()
    if peak > BOUND_KB:
        raise SystemExit("%s at %s: %d kB resident, bound %d kB"
                         % (ABORT, where, peak, BOUND_KB))


def pair_label(setter, consumer):
    """a pair's own display label: two cells, each machine form."""
    return "%s + %s" % (cell_label(setter), cell_label(consumer))


# ==================================================================
# section 0: the holder table, task hub1's with the truth holder added
# ==================================================================
#
# `bool` is go's truth holder and a comparison's own result sits in it.
# The three targets spell it differently and only c can be reached by a
# cast: rust and go refuse `x as bool` / `bool(x)`, so the conversion
# from the emulation's 8-bit answer is written as the target's own test
# against zero.  WHICH conversion is used is decided by the node's
# RESULT HOLDER -- machine form -- and never by anything about the node's
# own text.

HOLDER = dict(HUB1.HOLDER)
HOLDER["bool"] = {"bits": 8, "kind": "bv", "signed": False, "truth": True,
                  "c": "bool", "rust": "bool", "go": "bool"}

UNSIGNED_OF_BITS = HUB1.UNSIGNED_OF_BITS


def holder_of(go_type, target):
    entry = HOLDER.get(go_type)
    if entry is None:
        raise Refused("this task's holder table has no %s holder for the "
                      "go holder `%s`, so no composition is written for it"
                      % (target, go_type))
    return entry[target]


def cast_to_holder_name(target, text, holder):
    return HUB1.cast_to_holder_name(target, text, holder)


def narrow_answer(target, text, go_type):
    """the emulation's answer read as the node's own value, in the node's
    holder."""
    entry = HOLDER.get(go_type)
    if entry is None:
        raise Refused("this task's holder table has no %s holder for the "
                      "go holder `%s`, so no composition is written for it"
                      % (target, go_type))
    if entry.get("truth"):
        # the answer is the 8-bit 0/1 the set instruction leaves; the
        # target's own truth holder is reached by its own test against
        # zero, because rust and go both refuse a cast into it.
        through = cast_to_holder_name(target, text,
                                      UNSIGNED_OF_BITS[8][target])
        if target == "c":
            return "(bool)(%s)" % through
        if target == "rust":
            return "((%s) != 0)" % through
        return "(%s != 0)" % through
    if entry["kind"] == "fp":
        return cast_to_holder_name(target, text, entry[target])
    unsigned = UNSIGNED_OF_BITS[entry["bits"]][target]
    through = cast_to_holder_name(target, text, unsigned)
    return cast_to_holder_name(target, through, entry[target])


def declaration(target, name, params, result_go_type):
    if target == "c":
        spelled = []
        for param in params:
            spelled.append("%s %s" % (holder_of(param["go_type"], "c"),
                                      param["name"]))
        return ("%s\n%s(%s)"
                % (holder_of(result_go_type, "c"), name, ", ".join(spelled)))
    if target == "rust":
        spelled = []
        for param in params:
            spelled.append("%s: %s" % (param["name"],
                                       holder_of(param["go_type"], "rust")))
        return ('#[no_mangle]\npub extern "C" fn %s(%s) -> %s'
                % (name, ", ".join(spelled),
                   holder_of(result_go_type, "rust")))
    spelled = []
    for param in params:
        spelled.append("%s %s" % (param["name"],
                                  holder_of(param["go_type"], "go")))
    return ("//go:noinline\nfunc %s(%s) %s"
            % (name, ", ".join(spelled), holder_of(result_go_type, "go")))


def statement(target, name, go_type, text):
    if target == "c":
        return "    %s %s = %s;" % (holder_of(go_type, "c"), name, text)
    if target == "rust":
        return "    let %s: %s = %s;" % (name, holder_of(go_type, "rust"),
                                         text)
    return "\t%s := %s" % (name, text)


def go_main_for(names_and_params):
    """the composed go file's own `main`, task hub1's, re-spelled here
    because it declares a global per parameter through the holder
    table and this file's table carries one more holder."""
    globals_lines = []
    calls = []
    counter = 0
    for name, params, _result in names_and_params:
        arguments = []
        for param in params:
            spelling = holder_of(param["go_type"], "go")
            variable = "hub_g%d" % counter
            counter = counter + 1
            globals_lines.append("var %s %s" % (variable, spelling))
            arguments.append(variable)
        calls.append("\thub_sink = %s(%s)" % (name, ", ".join(arguments)))
    text = "\n".join(globals_lines)
    text = text + "\nvar hub_sink interface{}\n\nfunc main() {\n"
    text = text + "\n".join(calls) + "\n\t_ = hub_sink\n}"
    return text


def params_for_gate(params):
    out = []
    for index, param in enumerate(params):
        entry = HOLDER.get(param["go_type"])
        if entry is None:
            raise Refused("this task's holder table has no entry for the "
                          "go holder `%s`" % param["go_type"])
        out.append({"index": index, "name": param["name"],
                    "kind": entry["kind"], "bits": entry["bits"],
                    "holder": param["go_type"]})
    return out


TRUTH_HOLDER = HUB1.TRUTH_HOLDER


def check_parameters(target, entry, plan, operand_types):
    """whether the emulation's own parameters can carry the operands the
    node passes -- task hub1's two refusals, unchanged, and stated here
    because the brief's third hole is exactly this question: the entry
    records the holders the proof was made over, and a mismatch is
    refused BY CAUSE rather than called."""
    truth = TRUTH_HOLDER.get(target) or ()
    for index, position in enumerate(plan):
        param = entry["params"][index]
        holder = param.get("holder")
        if holder in truth:
            raise Refused("the emulation `%s` declares its parameter %d "
                          "in %s's truth holder `%s`, which collapses "
                          "every non-zero value to one; the proof was "
                          "made over that holder and this node's operand "
                          "is not in it"
                          % (entry["symbol"], index, target, holder))
        go_type = operand_types[position]
        wanted = HOLDER.get(go_type)
        if wanted is None:
            raise Refused("this task's holder table has no entry for the "
                          "go holder `%s`" % go_type)
        bits = param.get("bits")
        if bits is None or bits < wanted["bits"]:
            raise Refused("the emulation `%s` declares its parameter %d "
                          "%s bits wide and the operand this node passes "
                          "there is %d bits (`%s`), so the call would "
                          "truncate it"
                          % (entry["symbol"], index, bits, wanted["bits"],
                             go_type))


# ==================================================================
# section 1: THE DICTIONARY, level one -- the cells, READ FROM THE BANK
# ==================================================================
#
# Task hub1 read one pass's store (`autopoly5_runs.jsonl`) and so held
# only what the last pass reached.  Task bank1's finding is that a proof
# is a certificate about one artifact and cannot regress, so from here
# the dictionary is read from `certificates.jsonl`: the PREFERRED
# certificate of each (cell, target, written place) whose kind is
# `proved` or `proved_under_caller_extension` and whose place is the
# cell's own answer (its name begins `reg_`).
#
# A certificate names its artifact -- source path and sha256 -- but not
# the emulation's PARAMETERS, and the parameters are what the brief's
# third hole is about.  So each certificate is joined back to the RUN
# that produced it, in the store the certificate itself names, and the
# join is CHECKED: the run's rendered source is hashed and the hash must
# be the certificate's.  A certificate whose run cannot be found, or
# whose source does not hash to the certificate's sha256, is not an
# entry; it is a hole with that as its cause.

VALUE_PLACE = re.compile(r"^reg_")


def sha256_of(text):
    if text is None:
        return None
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def bank_preferred():
    """-> {(target, cell key): the preferred certificate of the cell's
    own answer place}, and the preferred certificates of every other
    kind, kept so a hole can carry the bank's own cause."""
    entries = {}
    others = {}
    handle = open(CERTIFICATES)
    for line in handle:
        record = json.loads(line)
        if not record.get("preferred"):
            continue
        target = record["target"]
        if target not in TARGETS:
            continue
        cell = record["cell"]
        key = (target, (cell["mnem"], cell["shape"], cell["key_width"]))
        place = record.get("place") or ""
        if record["kind"] in CERTIFIED and VALUE_PLACE.match(place):
            entries[key] = record
            continue
        held = others.get(key)
        if held is None:
            others[key] = record
    handle.close()
    check_memory("bank preferred")
    return entries, others


def runs_of_stores(wanted):
    """-> {(store, target, cell key, place): the run's own place record,
    with the run's own fields beside it}.

    `wanted` is the set of (store, target, cell key, place) the bank
    named; every store is streamed once and only those are kept."""
    by_store = collections.defaultdict(set)
    for store, target, key, place in wanted:
        by_store[store].add((target, key, place))
    out = {}
    for store in sorted(by_store):
        path = os.path.join(HQ, store)
        if not os.path.exists(path):
            continue
        handle = open(path)
        for line in handle:
            run = json.loads(line)
            key = (run["mnem"], run["shape"], run["key_width"])
            for place in run.get("places") or []:
                writes = place.get("writes")
                if (run["lang"], key, writes) not in by_store[store]:
                    continue
                out[(store, run["lang"], key, writes)] = (run, place)
        handle.close()
        check_memory("runs of %s" % store)
    return out


def cell_entries(outer):
    """-> (entries, holes) per target, at the cell level.

    An entry carries the emulation's SOURCE, its symbol, its route, the
    place it writes, the PARAMETER HOLDERS the proof was made over, the
    certificate's own kind and pass, and the ledger rows the cell is
    attested by."""
    preferred, others = bank_preferred()
    wanted = set()
    for (target, key), record in preferred.items():
        wanted.add((record["produced_by"]["store"], target, key,
                    record["place"]))
    runs = runs_of_stores(wanted)
    entries = {}
    holes = {}
    joined = collections.Counter()
    for target in TARGETS:
        entries[target] = {}
        holes[target] = {}
    for (target, key), record in sorted(preferred.items()):
        label = "%s %s %s" % key
        store = record["produced_by"]["store"]
        found = runs.get((store, target, key, record["place"]))
        attested = outer.get(key) or {}
        base = {
            "lang": target,
            "unit": "hub2/cell/%s" % label,
            "level": "cell",
            "mnem": key[0],
            "shape": key[1],
            "key_width": key[2],
            "kind": record["kind"],
            "place": record["place"],
            "certificate": {
                "pass": record["produced_by"]["pass"],
                "store": store,
                "source_path": record["source"]["path"],
                "source_sha256": record["source"]["sha256"],
                "term_text": record["term_text"],
                "verdict": record["verdict"]["outcome"],
                "verdict_reason": record["verdict"].get("reason"),
                "compiler_version": record["compiler"]["version"],
                "compiler_flags": record["compiler"]["flags"],
            },
            "attested_ledger_rows": record.get("attested_ledger_rows")
                                    or attested.get("attested_ledger_rows")
                                    or 0,
            "line": attested.get("line"),
            "row_id": attested.get("row_id"),
            "attestation": attested.get("attestation"),
        }
        if found is None:
            base["cause"] = ("the bank's preferred certificate names the "
                             "run store `%s`, and no run of that store "
                             "writes this cell's place `%s`, so the "
                             "emulation's own source and parameters "
                             "cannot be read"
                             % (store, record["place"]))
            holes[target][label] = base
            joined["no run found"] += 1
            continue
        run, place = found
        digest = sha256_of(place.get("source"))
        base["source_sha256_of_the_run"] = digest
        base["matches_the_certificate"] = (digest ==
                                           record["source"]["sha256"])
        if not base["matches_the_certificate"]:
            base["cause"] = ("the run this certificate names renders a "
                             "source whose sha256 is %s and the "
                             "certificate's is %s, so the run is not the "
                             "artifact the certificate is about"
                             % (digest, record["source"]["sha256"]))
            holes[target][label] = base
            joined["source does not match"] += 1
            continue
        joined["joined"] += 1
        base["route"] = run["route"]
        base["symbol"] = place["symbol"]
        base["source"] = place["source"]
        base["source_path"] = place.get("source_path")
        base["params"] = place.get("params")
        base["holders"] = [
            {"index": param.get("index"), "holder": param.get("holder"),
             "bits": param.get("bits"), "family": param.get("family"),
             "kind": param.get("kind")}
            for param in (place.get("params") or [])]
        base["param_cell_families"] = HUB1.cell_family_of_params(place)
        base["place_bits"] = place.get("bits")
        base["home"] = place.get("home")
        base["line"] = run.get("line") or base["line"]
        base["row_id"] = run.get("row_id") or base["row_id"]
        base["attestation"] = run.get("attestation") or base["attestation"]
        base["attested_ledger_rows"] = (run.get("attested_ledger_rows")
                                        or base["attested_ledger_rows"])
        base["setter"] = run.get("setter")
        entries[target][label] = base
    # the holes: every cell of the outer set with no entry
    for target in TARGETS:
        for key in sorted(outer):
            label = "%s %s %s" % key
            if label in entries[target]:
                continue
            if label in holes[target]:
                continue
            attested = outer[key]
            record = others.get((target, key))
            hole = {
                "lang": target,
                "unit": "hub2/cell/%s" % label,
                "level": "cell",
                "mnem": key[0],
                "shape": key[1],
                "key_width": key[2],
                "attested_ledger_rows": attested.get("attested_ledger_rows")
                                        or 0,
                "line": attested.get("line"),
                "row_id": attested.get("row_id"),
            }
            if record is None:
                hole["cause"] = ("the bank holds no preferred certificate "
                                 "for this cell on this target")
            elif not VALUE_PLACE.match(record.get("place") or ""):
                hole["cause"] = ("the cell writes no register place: every "
                                 "place it writes is a flag place, which "
                                 "is not a value a composition can pass on")
                hole["kind"] = record["kind"]
            else:
                hole["kind"] = record["kind"]
                hole["cause"] = (record.get("cause")
                                 or (record.get("verdict") or {}).get("reason")
                                 or "the bank's preferred certificate for "
                                    "this place is of kind `%s`"
                                    % record["kind"])
            holes[target][label] = hole
    check_memory("cell entries")
    return entries, holes, dict(joined)


def outer_cells():
    """the outer set: every cell task ap5's pass walked, with the ledger
    rows the corpus attests it by.  It is the same outer set task hub1
    reported over, so the two dictionaries' counts sit beside each
    other."""
    out = {}
    handle = open(AP5_RUNS)
    for line in handle:
        run = json.loads(line)
        key = (run["mnem"], run["shape"], run["key_width"])
        if key in out:
            continue
        out[key] = {
            "attested_ledger_rows": run["attested_ledger_rows"],
            "line": run["line"],
            "row_id": run["row_id"],
            "attestation": run["attestation"],
        }
    handle.close()
    check_memory("outer cells")
    return out


# ==================================================================
# section 2: THE DICTIONARY, level one keyed by the PAIR
# ==================================================================
#
# A cell entry whose run carries a `setter` is an emulation of the PAIR:
# the rendered function is the comparison then the select, over the flag
# state that ONE setter writes.  Its key is therefore two cells, not one,
# and the setter's own cell is classified from the setter's own LINE by
# the model table's own classifier -- the same reading that gives the
# consumer its cell.
#
# The setter's WIDTH is part of the key and this is where the pair level
# stands or falls: the loop renders each consumer over exactly one setter,
# the one that consumer's own attestation records the most ledger rows
# for, at that setter's own width.  A pair the corpus attests at another
# width is a different pair and the dictionary says so.

def setter_cell_of(setter):
    """-> the setter's own cell, or (None, cause).

    `_install_gpr_widths` is the model table's own preparation of the
    register-width table its classifier reads; without it the classifier
    refuses every general-register operand, which is what the first run
    of this lane measured."""
    import model_table as MT
    MT._install_gpr_widths()
    shape, width, cause = MT.classify_line(setter["mnem"],
                                           setter.get("line"), None)
    if cause is not None:
        return None, cause
    return {"mnem": setter["mnem"], "shape": shape,
            "key_width": MT.key_width(setter["mnem"], width),
            "line": setter.get("line")}, None


def pair_entries(cells):
    """-> {target: {pair label: entry}} off the cell entries that carry a
    setter."""
    out = {}
    refusals = collections.Counter()
    for target in TARGETS:
        out[target] = {}
        for label in sorted(cells[target]):
            entry = cells[target][label]
            setter = entry.get("setter")
            if setter is None:
                continue
            cell, cause = setter_cell_of(setter)
            if cell is None:
                refusals[cause] += 1
                continue
            consumer = {"mnem": entry["mnem"], "shape": entry["shape"],
                        "key_width": entry["key_width"]}
            record = dict(entry)
            record["level"] = "pair"
            record["unit"] = "hub2/pair/%s" % pair_label(cell, consumer)
            record["setter_cell"] = cell
            record["consumer_cell"] = consumer
            out[target][pair_label(cell, consumer)] = record
    check_memory("pair entries")
    return out, dict(refusals)


# ==================================================================
# section 3: THE DICTIONARY, level two -- the OPERATOR BODIES
# ==================================================================
#
# A pool entry is one distinct computation; task o7 rendered an emulation
# of an entry in c and task o11 in rust, each proved against the x unit's
# own carved body, and task o13 re-rendered the disproved ones with the
# MODE -- the guard the x body carries -- in place.  Where go lowers a
# construct to a SEQUENCE of cells rather than to one, the node's unit
# still belongs to exactly one pool entry, and that entry's emulation is
# the whole body as one function.  There is no go column at this level:
# task o7 renders c and task o11 renders rust, and no renderer of the
# body level was run for go.

SYMBOL = re.compile(r"\bemu_[A-Za-z0-9_]+\b")


def symbol_of(source):
    found = SYMBOL.search(source or "")
    if found is None:
        return None
    return found.group(0)


def proof_word(check):
    """-> ("proved" | "proved_under_caller_extension" | None) off one q3
    record, in the bank's own kind vocabulary."""
    if not check:
        return None
    if check.get("outcome") in PROVED_WORDS:
        return "proved"
    extension = check.get("under_caller_extension") or {}
    if extension.get("outcome") in PROVED_WORDS:
        return "proved_under_caller_extension"
    return None


def body_record(row, target, kind, posing, mode):
    """one body-level entry, keyed by the pool entry id."""
    width = row.get("c_result_width")
    if width is None:
        width = row.get("target_result_width")
    family = row.get("c_result_family")
    if family is None:
        family = row.get("target_result_family")
    return {
        "lang": target,
        "unit": "hub2/body/%s" % row["entry_id"],
        "level": "body",
        "entry_id": row["entry_id"],
        "kind": kind,
        "proved_by": posing,
        "mode": mode,
        "symbol": symbol_of(row.get("source")),
        "source": row.get("source"),
        "source_path": row.get("source_path"),
        "params": row.get("params"),
        "holders": [
            {"index": param.get("index"), "holder": param.get("holder"),
             "bits": param.get("bits"), "family": param.get("family"),
             "kind": param.get("kind")}
            for param in (row.get("params") or [])],
        "result_width": width,
        "result_family": family,
        "type_key": row.get("type_key"),
        "layer5_text": row.get("layer5_text"),
        "x_unit": row.get("x_unit"),
        "x_lang": row.get("x_lang"),
        "x_body_text": row.get("x_body_text"),
        "verdict_reason": (row.get("q3") or {}).get("reason"),
    }


def body_entries():
    """-> ({target: {entry id: entry}}, {target: {entry id: the run that
    did not prove}}).

    Task o13's rows are read after task o7's and task o11's and win where
    they carry a proof the first pass did not, because task o13's own
    emulation is the one with the mode rendered into it."""
    entries = {}
    unproved = {}
    for target in TARGETS:
        entries[target] = {}
        unproved[target] = {}
    for target, path in [("c", O7), ("rust", O11)]:
        document = read_json(path)
        for row in document["results"]:
            if row.get("control"):
                continue
            kind = proof_word(row.get("q3"))
            if kind is None:
                unproved[target][row["entry_id"]] = {
                    "entry_id": row["entry_id"],
                    "x_unit": row.get("x_unit"),
                    "cause": ("the emulation of this entry was rendered "
                              "and built and the gate answered: %s"
                              % ((row.get("q3") or {}).get("reason")
                                 or "no reason recorded")),
                }
                continue
            posing = "the first posing"
            if kind == "proved_under_caller_extension":
                posing = "the first posing, under caller extension"
            entries[target][row["entry_id"]] = body_record(row, target,
                                                           kind, posing,
                                                           None)
        del document
        check_memory("body entries %s" % target)
    mode = read_json(O13)
    for target in sorted(mode["runs"]):
        if target not in TARGETS:
            continue
        for row in mode["runs"][target]:
            if row.get("control"):
                continue
            first = proof_word(row.get("q3"))
            guarded = proof_word(row.get("q3_guarded"))
            kind = first
            posing = "the first posing"
            if first == "proved_under_caller_extension":
                posing = "the first posing, under caller extension"
            if first is None and guarded is not None:
                kind = guarded
                posing = "the guarded posing"
                if guarded == "proved_under_caller_extension":
                    posing = "the guarded posing, under caller extension"
            if kind is None:
                if row["entry_id"] not in unproved[target]:
                    unproved[target][row["entry_id"]] = {
                        "entry_id": row["entry_id"],
                        "x_unit": row.get("x_unit"),
                        "cause": ("the mode was rendered and the gate "
                                  "answered: %s"
                                  % ((row.get("q3_guarded") or {}).get("reason")
                                     or "no reason recorded")),
                    }
                continue
            held = entries[target].get(row["entry_id"])
            if held is not None and held["kind"] == "proved":
                continue
            entries[target][row["entry_id"]] = body_record(
                row, target, kind, posing, row.get("mode"))
            unproved[target].pop(row["entry_id"], None)
    del mode
    check_memory("body entries with the mode")
    return entries, unproved


def pool_index():
    """-> ({unit: entry id}, {entry id: the entry's own facts}).

    The pool is the largest store this task holds whole and it is dropped
    as soon as the index is built."""
    document = read_json(POOL)
    entry_of_unit = {}
    facts = {}
    for entry in document["entries"]:
        languages = set()
        for member in entry["members"]:
            unit = member["unit"] if isinstance(member, dict) else member
            entry_of_unit[unit] = entry["entry_id"]
            languages.add(unit.split("/")[0])
        facts[entry["entry_id"]] = {
            "entry_id": entry["entry_id"],
            "member_count": entry["member_count"],
            "type_key": entry["type_key"],
            "languages": sorted(languages),
            "distinct_wrapped_text_count":
                entry.get("distinct_wrapped_text_count"),
            "distinct_layer5_text_count":
                entry.get("distinct_layer5_text_count"),
            "layer5_texts": len(entry.get("layer5_normalized_texts") or []),
            "representative": entry.get("representative"),
            "representative_rule": entry.get("representative_rule"),
        }
    del document
    check_memory("pool index")
    return entry_of_unit, facts


def body_holes(entries, unproved, facts, wanted):
    """the pool entries a go corpus unit belongs to and the dictionary
    cannot serve, per target, each with the cause off the emulation
    study's OWN population file."""
    populations = {}
    run_sets = {}
    for target, path in [("c", O7_POPULATION), ("rust", O11_POPULATION)]:
        document = read_json(path)
        populations[target] = set(document["entries"].keys())
        run_set = document.get("run_set")
        if run_set is None:
            run_sets[target] = None
        else:
            run_sets[target] = set(run_set)
        del document
    out = {}
    for target in TARGETS:
        out[target] = {}
        for entry_id in sorted(wanted):
            if entry_id in entries[target]:
                continue
            fact = facts.get(entry_id) or {}
            hole = {"entry_id": entry_id, "lang": target, "level": "body",
                    "type_key": fact.get("type_key"),
                    "member_count": fact.get("member_count"),
                    "languages": fact.get("languages")}
            if target == "go":
                hole["cause"] = ("no renderer of the body level was run "
                                 "for go: task o7 renders c and task o11 "
                                 "renders rust, and this task renders "
                                 "nothing new")
                out[target][entry_id] = hole
                continue
            if entry_id not in populations[target]:
                if target in (fact.get("languages") or []):
                    hole["cause"] = ("the emulation study's filter P1 "
                                     "keeps only an entry the target has "
                                     "NO member of, and this entry has %d "
                                     "member(s) in %s"
                                     % (fact.get("member_count"), target))
                elif not fact.get("layer5_texts"):
                    hole["cause"] = ("the emulation study's filter P2 "
                                     "keeps only an entry that carries a "
                                     "layer-5 text, and this entry carries "
                                     "none")
                else:
                    hole["cause"] = ("the entry is outside the emulation "
                                     "study's population and its filters "
                                     "P1 and P2 both hold for it, so its "
                                     "chosen member's text does not "
                                     "round-trip through task o1's parser "
                                     "(filter P3)")
                out[target][entry_id] = hole
                continue
            if run_sets[target] is not None and entry_id not in run_sets[target]:
                hole["cause"] = ("the entry is in the emulation study's "
                                 "population and was not in the run set "
                                 "the pass on record walked")
                out[target][entry_id] = hole
                continue
            failed = unproved[target].get(entry_id)
            if failed is not None:
                hole["cause"] = failed["cause"]
                hole["x_unit"] = failed.get("x_unit")
                out[target][entry_id] = hole
                continue
            hole["cause"] = ("the entry is in the emulation study's "
                             "population and the store on record holds no "
                             "run of it")
            out[target][entry_id] = hole
    check_memory("body holes")
    return out


# ==================================================================
# section 4: THE GO SIDE -- every corpus go unit at all three levels
# ==================================================================
#
# Task hub1's go side is called and its rows are kept EXACTLY as it built
# them, so the cell level's own resolutions are the same object beside
# the same object.  What this task adds to each unit is two more
# readings of the same corpus record: the PAIR its own ledger attests,
# and the POOL ENTRY it belongs to.
#
# THE PAIR RULE, stated mechanically and decided here as a mechanical
# detail: a unit is ONE PAIR PLUS CHAFF when its own ledger holds
# exactly one flag_pair row whose consumer line the model table's own
# classifier reads, and every arch-opcode row of the body outside the OUT
# block is that pair's setter and there is exactly one of them.  It is
# the pair analogue of task o2's NARROW rule (the whole body is one
# arch-opcode instruction plus chaff), and it is written against the same
# classifier.

def pairs_of_units(units):
    """-> ({unit: the pair its ledger attests}, the refusal counter)."""
    import model_table as MT
    import ledger as L
    import canonical_form as CF
    MT._install_gpr_widths()
    readings = CF.runtime_answer_readings()
    routines = CF.runtime_routine_names(readings)
    out = {}
    refusals = collections.Counter()
    for unit_id in sorted(units):
        record = units[unit_id]
        line_of_row = MT.lines_of_unit(record, routines, readings)
        if line_of_row is None:
            refusals["the unit's body could not be relinked"] += 1
            continue
        rows = MT.flag_pair_rows(record)
        if not rows:
            refusals["no flag pair row: the body reads no arriving flag "
                     "state"] += 1
            continue
        if len(rows) != 1:
            refusals["the body holds %d flag pair rows, not one"
                     % len(rows)] += 1
            continue
        row = rows[0]
        setter_mnem, consumer_mnem = row["produced_by"]["mnem"]
        line = line_of_row.get(row["row"])
        if line is None:
            refusals["the pair's consumer row has no line"] += 1
            continue
        shape, width, cause = MT.classify_line(consumer_mnem, line,
                                               row.get("size"))
        if cause is not None:
            refusals["the consumer's own line is not one the classifier "
                     "reads: %s" % cause] += 1
            continue
        setter_rows = []
        other = []
        for arch_row in MT.arch_opcode_rows(record):
            if arch_row.get("block") == "OUT":
                continue
            if arch_row["produced_by"]["mnem"] == setter_mnem:
                setter_rows.append(arch_row)
            else:
                other.append(arch_row["produced_by"]["mnem"])
        if len(setter_rows) != 1 or other:
            refusals["the body holds %d arch-opcode row(s) that are not "
                     "the pair's setter" % len(other)] += 1
            continue
        setter_line = line_of_row.get(setter_rows[0]["row"])
        s_shape, s_width, s_cause = MT.classify_line(setter_mnem,
                                                     setter_line,
                                                     setter_rows[0].get("size"))
        if s_cause is not None:
            refusals["the setter's own line is not one the classifier "
                     "reads: %s" % s_cause] += 1
            continue
        arrivals = list(record.get("arrival_families") or [])
        slots = []
        for index, text in enumerate(MT.operand_texts(setter_line)):
            family = L.family_of_operand(text)
            in_row = None
            if family in arrivals:
                in_row = arrivals.index(family)
            slots.append({"slot": index, "text": text, "family": family,
                          "in_row": in_row})
        out[unit_id] = {
            "setter": {"mnem": setter_mnem, "shape": s_shape,
                       "key_width": MT.key_width(setter_mnem, s_width)},
            "setter_line": setter_line,
            "setter_operand_slots": slots,
            "consumer": {"mnem": consumer_mnem, "shape": shape,
                         "key_width": MT.key_width(consumer_mnem, width)},
            "consumer_line": line,
        }
        refusals["ONE PAIR PLUS CHAFF"] += 1
    check_memory("pairs of units")
    return out, dict(refusals)


def go_side():
    """-> (rows, the cell-level refusals, the pair-level counter).

    One row per corpus go unit, carrying the three readings of it: the
    CELL its body names under task o2's narrow rule (task hub1's own
    row, kept whole), the PAIR its ledger attests, and the POOL ENTRY it
    belongs to."""
    narrow_rows, refused, refusals, every = HUB1.go_side()
    by_unit = {}
    for row in narrow_rows:
        by_unit[row["unit"]] = row
    units = HUB1.go_units_held()
    pairs, pair_counter = pairs_of_units(units)
    entry_of_unit, facts = pool_index()
    out = []
    for row in every:
        record = dict(row)
        unit_id = row["unit"]
        held = units.get(unit_id) or {}
        record["arrival_families"] = list(held.get("arrival_families") or [])
        record["result_family"] = held.get("result_family")
        narrow = by_unit.get(unit_id)
        record["cell"] = None
        record["unit_line"] = None
        record["operand_slots"] = None
        if narrow is not None:
            record["cell"] = narrow["cell"]
            record["unit_line"] = narrow["unit_line"]
            record["operand_slots"] = narrow["operand_slots"]
        record["pair"] = pairs.get(unit_id)
        record["entry_id"] = entry_of_unit.get(unit_id)
        record["entry"] = facts.get(entry_of_unit.get(unit_id))
        out.append(record)
    check_memory("go side")
    return out, refused, refusals, pair_counter, facts, entry_of_unit


# ==================================================================
# section 5: the dictionary command
# ==================================================================

def dictionary_command():
    say("[1/5] the outer set of cells, off task ap5's own pass")
    outer = outer_cells()
    say("   cells in the outer set: %d" % len(outer))
    say("[2/5] level one: the cells, READ FROM THE BANK")
    cells, cell_hole, joined = cell_entries(outer)
    say("   the join to the run that produced each certificate: %s" % joined)
    for target in TARGETS:
        say("   %-5s entries %4d   holes %4d"
            % (target, len(cells[target]), len(cell_hole[target])))
    say("[3/5] level one keyed by the pair")
    pairs, pair_refusals = pair_entries(cells)
    for target in TARGETS:
        say("   %-5s pair entries %4d" % (target, len(pairs[target])))
    if pair_refusals:
        say("   setter lines the classifier does not read: %s"
            % pair_refusals)
    say("[4/5] level two: the operator bodies")
    bodies, unproved = body_entries()
    for target in TARGETS:
        say("   %-5s body entries %4d" % (target, len(bodies[target])))
    say("[5/5] the go side, and the holes")
    rows, refused, refusals, pair_counter, facts, entry_of_unit = go_side()
    say("   corpus go units: %d" % len(rows))
    named_cell = 0
    named_pair = 0
    named_entry = 0
    entries_wanted = set()
    for row in rows:
        if row["cell"] is not None:
            named_cell = named_cell + 1
        if row["pair"] is not None:
            named_pair = named_pair + 1
        if row["entry_id"] is not None:
            named_entry = named_entry + 1
            entries_wanted.add(row["entry_id"])
    say("   naming one cell %d, one pair %d, a pool entry %d (%d entries)"
        % (named_cell, named_pair, named_entry, len(entries_wanted)))
    body_hole = body_holes(bodies, unproved, facts, entries_wanted)
    pair_hole = attested_pair_holes(rows, pairs)
    document = {
        "meta": {
            "task": "hub2",
            "node": "hq.research.arch_unit_oracle.hub_compiler.dictionary",
            "what": "the Hub's lookup at two levels: per (target, cell) "
                    "the proved emulation the bank certifies, keyed also "
                    "by the (setter cell, consumer cell) PAIR where the "
                    "emulation is one; and per (target, pool entry) the "
                    "proved emulation of the whole operator body",
            "cells_read_from": CERTIFICATES,
            "cells_joined_to": "the run store each certificate names, for "
                               "the emulation's own source and parameters",
            "outer_set_read_from": AP5_RUNS,
            "bodies_read_from": [O7, O11, O13],
            "pool_read_from": POOL,
            "go_side_read_from": [SINGLE,
                                  os.path.join(OP, "canon40_wrapped_go.json"),
                                  os.path.join(OP, "canon40_regen_store")],
            "key": "machine form throughout: (target, mnem, operand "
                   "shape, key_width) at the cell level; the two cells of "
                   "the pair at the pair level; the pool entry id at the "
                   "body level; the corpus unit id on the go side",
            "the_join_to_the_runs": joined,
            "peak_kb": peak_kb(),
        },
        "cells": cells,
        "cell_holes": cell_hole,
        "pairs": pairs,
        "pair_holes": pair_hole,
        "bodies": bodies,
        "body_holes": body_hole,
        "go_units": rows,
        "go_units_without_one_cell": refused,
        "go_ledger_refusals": refusals,
        "go_pair_refusals": pair_counter,
    }
    write_json(DICTIONARY2, document)
    say("   %s" % DICTIONARY2)
    dictionary_md(document)
    say("   %s" % DICTIONARY2_MD)
    say("peak resident: %d kB" % peak_kb())
    return 0


def attested_pair_holes(rows, pairs):
    """the pairs the go corpus attests that the dictionary cannot serve,
    per target, with the cause."""
    attested = {}
    for row in rows:
        pair = row.get("pair")
        if pair is None:
            continue
        label = pair_label(pair["setter"], pair["consumer"])
        record = attested.get(label)
        if record is None:
            record = {"label": label, "setter": pair["setter"],
                      "consumer": pair["consumer"], "units": 0}
            attested[label] = record
        record["units"] = record["units"] + 1
    out = {}
    for target in TARGETS:
        out[target] = {}
        for label in sorted(attested):
            if label in pairs[target]:
                continue
            record = dict(attested[label])
            record["lang"] = target
            record["level"] = "pair"
            same_consumer = []
            for held in pairs[target].values():
                if cell_label(held["consumer_cell"]) == \
                        cell_label(record["consumer"]):
                    same_consumer.append(cell_label(held["setter_cell"]))
            if same_consumer:
                record["cause"] = ("the loop renders each consumer over "
                                   "ONE setter -- the one that consumer's "
                                   "own attestation records the most "
                                   "ledger rows for -- and for this "
                                   "consumer that setter is `%s`, which is "
                                   "not the setter this pair is over"
                                   % ", ".join(sorted(same_consumer)))
            else:
                record["cause"] = ("the dictionary has no proved entry for "
                                   "the consumer cell `%s` on %s at all"
                                   % (cell_label(record["consumer"]),
                                      target))
            out[target][label] = record
    return out


def dictionary_md(document):
    lines = []
    lines.append("# dictionary2 -- task hub2, Hub v2's lookup at two "
                 "levels")
    lines.append("")
    lines.append("Generated by `hub2.py dictionary`. The key is machine "
                 "form throughout: `(target, mnem, operand shape, "
                 "key_width)` at the cell level, the two cells of the "
                 "pair at the pair level, the pool entry id at the body "
                 "level, and the corpus unit id on the go side. The cell "
                 "level is read from task bank1's `certificates.jsonl` "
                 "and joined to the run that produced each certificate "
                 "for the emulation's own source and parameter holders.")
    lines.append("")
    lines.append("## 1. Entries and holes per target, per level")
    lines.append("")
    rows = []
    for target in TARGETS:
        cells = document["cells"][target]
        holes = document["cell_holes"][target]
        proved_rows = 0
        for entry in cells.values():
            proved_rows = proved_rows + (entry.get("attested_ledger_rows") or 0)
        hole_rows = 0
        for hole in holes.values():
            hole_rows = hole_rows + (hole.get("attested_ledger_rows") or 0)
        rows.append([target, "cell", len(cells), proved_rows, len(holes),
                     hole_rows])
        rows.append([target, "pair", len(document["pairs"][target]), "--",
                     len(document["pair_holes"][target]), "--"])
        rows.append([target, "body", len(document["bodies"][target]), "--",
                     len(document["body_holes"][target]), "--"])
    lines.append(pipe_table(["target", "level", "entries",
                             "ledger rows the entries cover", "holes",
                             "ledger rows the holes cover"], rows))
    lines.append("")
    lines.append("## 2. Cell entries per target by route and by the "
                 "certificate's kind")
    lines.append("")
    rows = []
    for target in TARGETS:
        route = collections.Counter()
        kind = collections.Counter()
        pas = collections.Counter()
        for entry in document["cells"][target].values():
            route[entry.get("route")] += 1
            kind[entry["kind"]] += 1
            pas[entry["certificate"]["pass"]] += 1
        rows.append([target, route.get("primitive", 0),
                     route.get("primitive+setup", 0), route.get("term", 0),
                     kind.get("proved", 0),
                     kind.get("proved_under_caller_extension", 0),
                     ", ".join(["%s %d" % (p, pas[p]) for p in sorted(pas)])])
    lines.append(pipe_table(["target", "primitive", "primitive+setup",
                             "term", "`proved`",
                             "`proved_under_caller_extension`",
                             "the passes the certificates come from"], rows))
    lines.append("")
    lines.append("## 3. Cell holes per target, by cause")
    lines.append("")
    for target in TARGETS:
        counter = collections.Counter()
        rows_of_cause = collections.Counter()
        for hole in document["cell_holes"][target].values():
            cause = hole.get("cause") or "(no cause recorded)"
            counter[cause] += 1
            rows_of_cause[cause] += hole.get("attested_ledger_rows") or 0
        lines.append("### %s" % target)
        lines.append("")
        rows = []
        for cause in sorted(counter, key=lambda c: -counter[c]):
            rows.append([counter[cause], rows_of_cause[cause], cause])
        lines.append(pipe_table(["cells", "ledger rows", "cause"], rows))
        lines.append("")
    lines.append("## 4. The pair level: the pairs the loop proved")
    lines.append("")
    lines.append("One row per (setter cell, consumer cell) the loop "
                 "rendered as one function -- the comparison then the "
                 "select -- and proved. The setter's own width is part of "
                 "the key.")
    lines.append("")
    rows = []
    seen = []
    for target in TARGETS:
        for label in sorted(document["pairs"][target]):
            entry = document["pairs"][target][label]
            rows.append([target, "`%s`" % cell_label(entry["setter_cell"]),
                         "`%s`" % cell_label(entry["consumer_cell"]),
                         entry["kind"],
                         len(entry.get("params") or []),
                         entry.get("attested_ledger_rows")])
    lines.append(pipe_table(["target", "setter cell", "consumer cell",
                             "the certificate's kind",
                             "the emulation's parameters",
                             "ledger rows the consumer cell is attested by"],
                            rows))
    lines.append("")
    lines.append("## 5. The pair level: the pairs go's own corpus attests")
    lines.append("")
    counter = collections.Counter()
    for row in document["go_units"]:
        pair = row.get("pair")
        if pair is None:
            continue
        counter[pair_label(pair["setter"], pair["consumer"])] += 1
    rows = []
    for label in sorted(counter):
        marks = []
        for target in TARGETS:
            if label in document["pairs"][target]:
                marks.append(document["pairs"][target][label]["kind"])
            else:
                marks.append("--")
        rows.append([label, counter[label]] + marks)
    lines.append(pipe_table(["the pair go's corpus attests",
                             "go units that are one pair plus chaff"]
                            + TARGETS, rows))
    lines.append("")
    lines.append("## 6. The body level: the pool entries a go corpus unit "
                 "belongs to")
    lines.append("")
    entries_wanted = collections.Counter()
    for row in document["go_units"]:
        if row.get("entry_id") is not None:
            entries_wanted[row["entry_id"]] += 1
    rows = []
    for entry_id in sorted(entries_wanted):
        marks = []
        for target in TARGETS:
            entry = document["bodies"][target].get(entry_id)
            if entry is None:
                marks.append("--")
            else:
                marks.append("%s (%s)" % (entry["kind"], entry["proved_by"]))
        rows.append([entry_id, entries_wanted[entry_id]] + marks)
    lines.append(pipe_table(["pool entry", "go corpus units in it"]
                            + TARGETS, rows))
    lines.append("")
    lines.append("## 7. Body holes per target, by cause")
    lines.append("")
    for target in TARGETS:
        counter = collections.Counter()
        for hole in document["body_holes"][target].values():
            counter[hole.get("cause") or "(no cause recorded)"] += 1
        lines.append("### %s" % target)
        lines.append("")
        rows = []
        for cause in sorted(counter, key=lambda c: -counter[c]):
            rows.append([counter[cause], cause])
        lines.append(pipe_table(["pool entries", "cause"], rows))
        lines.append("")
    lines.append("## 8. The go side: how each corpus go unit is named")
    lines.append("")
    named = collections.Counter()
    for row in document["go_units"]:
        levels = []
        if row.get("cell") is not None:
            levels.append("cell")
        if row.get("pair") is not None:
            levels.append("pair")
        if row.get("entry_id") is not None:
            levels.append("body")
        named[", ".join(levels) or "none"] += 1
    rows = []
    for key in sorted(named, key=lambda k: -named[k]):
        rows.append([key, named[key]])
    lines.append(pipe_table(["the levels the corpus names this unit at",
                             "go units"], rows))
    lines.append("")
    lines.append("## 9. The parameter holders every entry records")
    lines.append("")
    lines.append("The brief's third hole: an entry records the holders "
                 "the proof was made over, and the composition refuses a "
                 "mismatch by cause. One row per distinct holder tuple.")
    lines.append("")
    counter = collections.Counter()
    for target in TARGETS:
        for level in ["cells", "pairs", "bodies"]:
            for entry in document[level][target].values():
                holders = tuple((h.get("holder"), h.get("bits"))
                                for h in (entry.get("holders") or []))
                counter[(target, level, holders)] += 1
    rows = []
    for key in sorted(counter, key=lambda k: (k[0], k[1], str(k[2]))):
        rows.append([key[0], key[1],
                     ", ".join(["`%s` (%s bits)" % h for h in key[2]])
                     or "(no parameters recorded)",
                     counter[key]])
    lines.append(pipe_table(["target", "level", "the holders the proof was "
                             "made over", "entries"], rows))
    lines.append("")
    lines.append("## 10. The go side, unit by unit, at all three levels")
    lines.append("")
    rows = []
    for row in document["go_units"]:
        holders = row["holders"]
        pair = row.get("pair")
        rows.append([row["unit"], holders["arity"], holders["lhs"],
                     holders["rhs"], holders["result"],
                     "`%s`" % (row.get("meta") or {}).get("expression"),
                     "`%s`" % cell_label(row["cell"]) if row.get("cell")
                     else "--",
                     "`%s`" % pair_label(pair["setter"], pair["consumer"])
                     if pair else "--",
                     row.get("entry_id") or "--"])
    lines.append(pipe_table(["unit", "arity", "lhs holder", "rhs holder",
                             "result holder", "the unit's own expression",
                             "cell", "pair", "pool entry"], rows))
    lines.append("")
    handle = open(DICTIONARY2_MD, "w")
    handle.write("\n".join(lines) + "\n")
    handle.close()


# ==================================================================
# section 6: RESOLVE -- one node to one corpus unit, then to a level
# ==================================================================
#
# The resolution is task hub1's and is unchanged: the candidate set is
# the TYPE TUPLE, and within it the candidate corpus unit's own go source
# is parsed by the same grammar and the two operator nodes compared as a
# parser does.  What this task adds is the ORDER a resolved unit is
# served in -- cell, else pair, else pool entry -- and that order is
# decided by what the dictionary holds for the unit, never by the node.

def resolve(node, index, parser):
    """-> (the corpus go unit row, None) or (None, the cause)."""
    if not node.get("typed"):
        return None, node["cause"]
    agreeing = HUB1.agreeing_units(node, index, parser)
    if not agreeing:
        return None, ("no go unit of the corpus carries this construct at "
                      "these operand holders, so the corpus attests "
                      "nothing for this node")
    with_cell = []
    with_pair = []
    for row in agreeing:
        if row.get("cell") is not None:
            with_cell.append(row)
        if row.get("pair") is not None:
            with_pair.append(row)
    if with_cell:
        return with_cell[0], None
    if with_pair:
        return with_pair[0], None
    return agreeing[0], None


def resolutions_for(nodes, index, parser):
    out = {}
    for record in nodes:
        node = record.pop("node")
        key = (record["position"]["line"], record["position"]["col"],
               record["position"]["end_line"],
               record["position"]["end_col"])
        row, cause = resolve(record, index, parser)
        out[key] = {"row": row, "cause": cause, "node": node,
                    "node_record": record}
    return out


def pair_argument_plan(row, entry, parser):
    """-> a list, per emulation parameter, of the operand POSITION whose
    value is passed there, for a PAIR entry.

    It is read off four machine-form objects: the unit's own parameters
    (which operand each names), its ARRIVAL FAMILIES (which register each
    parameter arrives in), the SETTER's own line in the unit's body
    (which register each operand slot of the comparison reads), and the
    loop setter's own line beside the emulation's parameter families."""
    import model_table as MT
    import ledger as L
    positions = HUB1.unit_operand_parameters(row, parser)
    if positions is None:
        raise Refused("the corpus unit's own source does not read its "
                      "construct's operands straight off its own "
                      "parameters, so no operand of the node can be put "
                      "on one of its IN rows")
    pair = row["pair"]
    arrivals = row["arrival_families"]
    slots = pair["setter_operand_slots"]
    families = [slot["family"] for slot in slots]
    for family in families:
        if family is None:
            raise Refused("the unit's own setter line `%s` carries an "
                          "operand that is not a register, so no IN row "
                          "stands for it" % pair["setter_line"])
        if families.count(family) > 1:
            raise Refused("the unit's own setter line `%s` reads the same "
                          "register family in more than one operand slot, "
                          "so an operand cannot be put on one slot"
                          % pair["setter_line"])
    setter = entry.get("setter") or {}
    loop_line = setter.get("line")
    if loop_line is None:
        raise Refused("the dictionary's pair entry records no setter line")
    loop_families = []
    for text in MT.operand_texts(loop_line):
        loop_families.append(L.family_of_operand(text))
    if len(loop_families) != len(families):
        raise Refused("the loop's setter line `%s` has %d operand slots "
                      "and the unit's setter line `%s` has %d"
                      % (loop_line, len(loop_families),
                         pair["setter_line"], len(families)))
    value_of_family = {}
    for position, parameter_index in enumerate(positions):
        if parameter_index >= len(arrivals):
            raise Refused("the unit's parameter %d has no arrival family "
                          "on its canon40 record" % parameter_index)
        family = arrivals[parameter_index]
        if family not in families:
            raise Refused("the unit's parameter %d arrives in %s and its "
                          "own setter line `%s` reads no operand there"
                          % (parameter_index, family, pair["setter_line"]))
        slot = families.index(family)
        loop_family = loop_families[slot]
        if loop_family is None:
            raise Refused("the loop's setter line `%s` has no register in "
                          "the operand slot the unit reads its operand in"
                          % loop_line)
        value_of_family[loop_family] = position
    plan = []
    for param in entry["params"]:
        family = param.get("family")
        if family not in value_of_family:
            raise Refused("the emulation takes a parameter for the "
                          "arrival %s and no operand of the node stands "
                          "for it" % family)
        plan.append(value_of_family[family])
    return plan


def body_argument_plan(row, entry, parser):
    """-> a list, per emulation parameter, of the operand POSITION whose
    value is passed there, for a BODY entry.

    The pool entry's type key IS its arrival families, so the emulation's
    parameters carry the same family names the unit's own canon40 record
    carries, and the plan is read straight off them."""
    positions = HUB1.unit_operand_parameters(row, parser)
    if positions is None:
        raise Refused("the corpus unit's own source does not read its "
                      "construct's operands straight off its own "
                      "parameters, so no operand of the node can be put "
                      "on one of its IN rows")
    arrivals = row["arrival_families"]
    value_of_family = {}
    for position, parameter_index in enumerate(positions):
        if parameter_index >= len(arrivals):
            raise Refused("the unit's parameter %d has no arrival family "
                          "on its canon40 record" % parameter_index)
        value_of_family[arrivals[parameter_index]] = position
    plan = []
    for param in entry["params"]:
        family = param.get("family")
        if family not in value_of_family:
            raise Refused("the emulation of the pool entry takes a "
                          "parameter that arrives in %s and no operand of "
                          "the node arrives there: the unit's own "
                          "arrivals are %s"
                          % (family, ", ".join(arrivals)))
        plan.append(value_of_family[family])
    return plan


PLAN_OF_LEVEL = {
    "cell": lambda row, entry, parser: HUB1.argument_plan(row, entry, parser),
    "pair": pair_argument_plan,
    "body": body_argument_plan,
}


def levels_for(target, row, dictionary):
    """-> (the levels the dictionary can serve this unit at, in order,
    each with its entry; the causes of the levels it cannot)."""
    found = []
    causes = []
    cell = row.get("cell")
    if cell is None:
        cells = row.get("cells")
        if cells is None:
            causes.append("cell: the unit's own body could not be "
                          "relinked, so it names no cell")
        else:
            causes.append("cell: go's own build of this construct is `%s`, "
                          "which is not one arch-opcode instruction plus "
                          "chaff (task o2's narrow rule), so the corpus "
                          "attests no single cell for it; its own ledger "
                          "holds %d arch-opcode row(s): %s"
                          % (row.get("body_text"), len(cells),
                             ", ".join(["`%s`" % cell_label(c)
                                        for c in cells]) or "none"))
    else:
        label = cell_label(cell)
        entry = dictionary["cells"][target].get(label)
        if entry is None:
            hole = dictionary["cell_holes"][target].get(label) or {}
            causes.append("cell: the dictionary has no proved entry for "
                          "the cell `%s` on %s: %s"
                          % (label, target,
                             hole.get("cause")
                             or "(the dictionary records no cause)"))
        else:
            found.append(("cell", entry))
    pair = row.get("pair")
    if pair is None:
        causes.append("pair: the unit's own ledger attests no single "
                      "(setter, consumer) pair")
    else:
        label = pair_label(pair["setter"], pair["consumer"])
        entry = dictionary["pairs"][target].get(label)
        if entry is None:
            hole = dictionary["pair_holes"][target].get(label) or {}
            causes.append("pair: the dictionary has no proved entry for "
                          "the pair `%s` on %s: %s"
                          % (label, target,
                             hole.get("cause")
                             or "(the dictionary records no cause)"))
        else:
            found.append(("pair", entry))
    entry_id = row.get("entry_id")
    if entry_id is None:
        causes.append("body: the unit is in no pool entry")
    else:
        entry = dictionary["bodies"][target].get(entry_id)
        if entry is None:
            hole = dictionary["body_holes"][target].get(entry_id) or {}
            causes.append("body: the dictionary has no proved emulation of "
                          "the pool entry %s on %s: %s"
                          % (entry_id, target,
                             hole.get("cause")
                             or "(the dictionary records no cause)"))
        else:
            found.append(("body", entry))
    return found, causes


# A target whose own conversion rules have no conversion from its truth
# holder into an integer holder: go refuses `uint32(a)` for a `bool` a,
# where c and rust both accept the conversion and the gate proves what
# comes out of it.  Read as a holder mismatch and refused by cause, which
# is the brief's third answer applied on the node's side.
NO_CONVERSION_FROM_TRUTH = {
    "go": "go's own conversion rules have no conversion from its truth "
          "holder `bool` into an integer holder",
}


def check_operand_holders(target, entry, plan, operand_types):
    """whether the target can spell `this node's operand, in the holder
    the proof was made over`."""
    reason = NO_CONVERSION_FROM_TRUTH.get(target)
    if reason is None:
        return
    for index, position in enumerate(plan):
        go_type = operand_types[position]
        entry_holder = HOLDER.get(go_type) or {}
        if not entry_holder.get("truth"):
            continue
        holder = entry["params"][index].get("holder")
        if holder in (TRUTH_HOLDER.get(target) or ()):
            continue
        raise Refused("this node's operand %d is in go's truth holder "
                      "`%s` and the emulation `%s` declares its parameter "
                      "%d in `%s`: %s"
                      % (position, go_type, entry["symbol"], index, holder,
                         reason))


def one_call(target, level, row, entry, parser, values, operand_types):
    """-> the call text, or Refused with the cause."""
    plan = PLAN_OF_LEVEL[level](row, entry, parser)
    check_parameters(target, entry, plan, operand_types)
    check_operand_holders(target, entry, plan, operand_types)
    arguments = []
    for index, position in enumerate(plan):
        if position >= len(values):
            raise Refused("the plan asks for operand %d and the node has "
                          "%d" % (position, len(values)))
        holder = entry["params"][index]["holder"]
        arguments.append(cast_to_holder_name(target, values[position],
                                             holder))
    symbol = entry["symbol"]
    if symbol is None:
        raise Refused("the dictionary's entry records no symbol, so no "
                      "call can be written")
    name = symbol.split(".")[-1]
    return "%s(%s)" % (name, ", ".join(arguments))


# ==================================================================
# section 7: COMPOSING ONE FUNCTION, at whichever level serves the node
# ==================================================================

class Composer(object):

    def __init__(self, target, dictionary, resolutions, parser,
                 source_bytes):
        self.target = target
        self.dictionary = dictionary
        self.resolutions = resolutions
        self.parser = parser
        self.source_bytes = source_bytes
        self.statements = []
        self.counter = 0
        self.used = []
        self.calls = []

    def emit(self, node, parameter_names_here):
        if node.type == "expression_list":
            inner = HUB1.named_children(node)
            if len(inner) != 1:
                raise Refused("an expression list of %d expressions"
                              % len(inner))
            return self.emit(inner[0], parameter_names_here)
        if node.type == "parenthesized_expression":
            inner = None
            for child in node.children:
                if child.is_named:
                    inner = child
            if inner is None:
                raise Refused("a parenthesized expression with no inner "
                              "expression")
            return self.emit(inner, parameter_names_here)
        if node.type == "identifier":
            text = HUB1.node_text(self.source_bytes, node)
            if text not in parameter_names_here:
                raise Refused("the leaf `%s` is not one of the function's "
                              "own parameters, and this task composes "
                              "over parameters only" % text)
            return text
        if node.type not in HUB1.OPERATOR_NODES:
            raise Refused("the node kind `%s` is not an operator node and "
                          "is not a parameter" % node.type)
        resolution = self.resolutions.get(HUB1.span_key(node))
        if resolution is None or resolution.get("row") is None:
            cause = "no resolution"
            if resolution is not None:
                cause = resolution.get("cause") or cause
            raise Refused(cause)
        row = resolution["row"]
        record = resolution["node_record"]
        operand_types = [record.get("lhs")]
        if record.get("arity") == "binary":
            operand_types.append(record.get("rhs"))
        values = []
        for operand in HUB1.operand_nodes_of(resolution["node"]):
            values.append(self.emit(operand, parameter_names_here))
        found, causes = levels_for(self.target, row, self.dictionary)
        call = None
        level = None
        entry = None
        for candidate_level, candidate in found:
            try:
                call = one_call(self.target, candidate_level, row,
                                candidate, self.parser, values,
                                operand_types)
                level = candidate_level
                entry = candidate
                break
            except Refused as refusal:
                causes.append("%s: %s" % (candidate_level, refusal.cause))
        if call is None:
            raise Refused("; ".join(causes))
        result_type = record["result"]
        text = narrow_answer(self.target, call, result_type)
        temporary = "hub_t%d" % self.counter
        self.counter = self.counter + 1
        self.statements.append(statement(self.target, temporary,
                                         result_type, text))
        label = entry["unit"]
        if label not in [u["label"] for u in self.used]:
            self.used.append({"label": label, "entry": entry,
                              "level": level})
        self.calls.append({"node": record["unit"], "level": level,
                           "entry": label, "symbol": entry["symbol"],
                           "route": entry.get("route"),
                           "kind": entry.get("kind"),
                           "unit": row["unit"]})
        return temporary


def compose_function(target, name, declaration_node, source_bytes,
                     dictionary, resolutions, parser):
    """-> a record: the composed function text and what it calls, or the
    cause it is a hole."""
    out = {"target": target, "func": name}
    params = HUB1.parameter_records(declaration_node, source_bytes)
    out["params"] = params
    result = HUB1.result_go_type(declaration_node, source_bytes)
    out["result"] = result
    unresolved = []
    for key in sorted(resolutions):
        value = resolutions[key]
        if value["node_record"].get("func") != name:
            continue
        if value["row"] is None:
            unresolved.append("`%s`: %s" % (value["node_record"]["text"],
                                            value["cause"]))
            continue
        found, causes = levels_for(target, value["row"], dictionary)
        if not found:
            unresolved.append("`%s`: the corpus names this node the unit "
                              "%s, and the dictionary serves it at no "
                              "level -- %s"
                              % (value["node_record"]["text"],
                                 value["row"]["unit"], "; ".join(causes)))
    if unresolved:
        out["composed"] = False
        out["cause"] = "; ".join(unresolved)
        return out
    expression = HUB1.single_return(declaration_node)
    if expression is None:
        out["composed"] = False
        out["cause"] = ("every operator node of this function resolves "
                        "and the dictionary serves each of them, and this "
                        "task composes a function whose body is one "
                        "`return` of one expression; this body is not "
                        "that shape")
        return out
    composer = Composer(target, dictionary, resolutions, parser,
                        source_bytes)
    names_here = [param["name"] for param in params]
    try:
        answer = composer.emit(expression, names_here)
        lines = list(composer.statements)
        lines.append(HUB1.returning(target, answer))
        head = declaration(target, name, params, result)
    except Refused as refusal:
        out["composed"] = False
        out["cause"] = refusal.cause
        return out
    out["composed"] = True
    out["text"] = HUB1.function_text(target, head, lines)
    out["used"] = composer.used
    out["calls"] = composer.calls
    return out


GO_FUNC = re.compile(r"^func\s+([A-Za-z0-9_]+)\s*\(")
GO_IMPORT = re.compile(r'^\s*import\s+"')


def go_blocks(source):
    """-> (the imports the file declares, {function name: its own text}).

    A go emulation file is a whole program: `package main`, the
    emulation, `main`, and -- where the renderer needed one -- HELPER
    functions the emulation calls.  Task hub1's reader took the
    emulation's own function and nothing else, and a composed file whose
    emulation calls a helper then did not build; the helpers are carried
    over here for the same reason c's `static inline` helpers are, and
    they are deduplicated by their own text."""
    imports = []
    blocks = {}
    lines = source.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if GO_IMPORT.match(line):
            imports.append(line.strip())
        found = GO_FUNC.match(line)
        if found is None:
            index = index + 1
            continue
        start = index
        while start > 0 and lines[start - 1].strip().startswith("//go:"):
            start = start - 1
        end = None
        for walker in range(index, len(lines)):
            if lines[walker] == "}":
                end = walker
                break
        if end is None:
            index = index + 1
            continue
        blocks[found.group(1)] = "\n".join(lines[start:end + 1])
        index = end + 1
    return imports, blocks


def strip_go(source, symbol):
    """-> (the imports, the emulation's own function, its helpers)."""
    name = symbol.split(".")[-1]
    imports, blocks = go_blocks(source)
    if name not in blocks:
        raise Refused("the go emulation source declares no `func %s(`, so "
                      "its function cannot be carried into a composed file"
                      % name)
    helpers = []
    for other in sorted(blocks):
        if other == name or other == "main":
            continue
        helpers.append(blocks[other])
    return imports, blocks[name], helpers


def compose_file(target, emulations, functions, drop_directive=False):
    """one composed source file.  c and rust are task hub1's own reader;
    go is this task's, because a go emulation may call a helper its own
    file declares and task hub1's reader dropped it."""
    if target != "go":
        return HUB1.compose_file(target, emulations, functions,
                                 drop_directive)
    imports = []
    helpers = []
    bodies = []
    for source, symbol in emulations:
        got_imports, body, got_helpers = strip_go(source, symbol)
        for line in got_imports:
            if line not in imports:
                imports.append(line)
        for helper in got_helpers:
            if helper not in helpers:
                helpers.append(helper)
        if drop_directive:
            # THE ONE LINE DROPPED, and nothing else: `//go:noinline` is
            # the directive the corpus's own probe shape puts on a probe
            # so the compiler leaves it as its own carvable function.  In
            # a COMPOSED file the emulation is not the unit being carved
            # -- the composed function is -- and the directive forbids
            # exactly the cross-operator lowering source composition
            # exists to obtain.  Both files are built and both verdicts
            # are recorded; nothing inside a proved function is touched.
            kept = []
            for line in body.splitlines():
                if line.strip() == GO_NOINLINE:
                    continue
                kept.append(line)
            body = "\n".join(kept)
        bodies.append(body)
    blocks = ["package main"]
    if imports:
        blocks.append("\n".join(imports))
    blocks.extend(helpers)
    blocks.extend(bodies)
    blocks.extend(functions)
    return "\n\n".join(blocks) + "\n"


def emulations_of(target, records):
    """the emulation sources every composed function of this file uses,
    once each, in the shape the target's own file wants them."""
    out = []
    seen = []
    for record in records:
        if not record.get("composed"):
            continue
        for used in record["used"]:
            if used["label"] in seen:
                continue
            seen.append(used["label"])
            if target == "go":
                out.append((used["entry"]["source"],
                            used["entry"]["symbol"]))
            else:
                out.append(used["entry"]["source"])
    return out


# ==================================================================
# section 8: THE HANDFUL -- the same eight functions task hub1 composed
# ==================================================================

SUFFIX = HUB1.SUFFIX
GO_NOINLINE = HUB1.GO_NOINLINE


def handful_command():
    say("[1/6] the dictionary")
    document = read_json(DICTIONARY2)
    index = HUB1.candidate_index(document["go_units"])
    for target in TARGETS:
        say("   %-5s cells %d, pairs %d, bodies %d"
            % (target, len(document["cells"][target]),
               len(document["pairs"][target]),
               len(document["bodies"][target])))
    say("[2/6] the front end: tree-sitter's tree, go/types' types")
    nodes, source_bytes, refusal = HUB1.front_end(HANDFUL_GO)
    if nodes is None:
        raise SystemExit("the type oracle did not run: %s" % refusal)
    typed = 0
    for record in nodes:
        if record.get("typed"):
            typed = typed + 1
    say("   operator nodes: %d, typed by go/types: %d" % (len(nodes), typed))
    parser = HUB1.go_parser()
    resolutions = resolutions_for(nodes, index, parser)
    resolved = 0
    for value in resolutions.values():
        if value["row"] is not None:
            resolved = resolved + 1
    say("   nodes resolved to a corpus unit: %d of %d"
        % (resolved, len(resolutions)))
    say("[3/6] body A: go's own build of the file, carved per function")
    declarations = HUB1.function_declarations(source_bytes, parser)
    names = []
    for name, node in declarations:
        if name == "main":
            continue
        names.append(name)
    bodies_a = HUB1.go_side_bodies(None, names)
    for name in names:
        say("   %-18s %s" % (name, bodies_a[name].get("body_text")
                             or bodies_a[name].get("cause")))
    say("[4/6] composing, one file per target")
    shared = HUB1.build_shared()
    composed = {}
    for target in TARGETS:
        per_function = []
        for name, node in declarations:
            if name == "main":
                continue
            record = compose_function(target, name, node, source_bytes,
                                      document, resolutions, parser)
            per_function.append(record)
        composed[target] = per_function
        texts = []
        plans = []
        for record in per_function:
            if not record.get("composed"):
                continue
            texts.append(record["text"])
            plans.append((record["func"], record["params"],
                          record["result"]))
        emulations = emulations_of(target, per_function)
        if not texts:
            say("   %-5s no function composed" % target)
            continue
        if target == "go":
            texts.append(go_main_for(plans))
        source = compose_file(target, emulations, texts)
        path = os.path.join(HANDFUL_DIR, "composed2_%s%s"
                            % (target, SUFFIX[target]))
        handle = open(path, "w")
        handle.write(source)
        handle.close()
        say("   %-5s %d function(s) composed, %d emulation(s), %s"
            % (target, len(texts) - (1 if target == "go" else 0),
               len(emulations), os.path.basename(path)))
        if target == "go":
            relaxed = compose_file(target, emulations, texts, True)
            second = os.path.join(HANDFUL_DIR, "composed2_go_inlinable.go")
            handle = open(second, "w")
            handle.write(relaxed)
            handle.close()
            say("   %-5s and the same file with the `%s` directive "
                "dropped from each emulation, %s"
                % (target, GO_NOINLINE, os.path.basename(second)))
    say("[5/6] body B and the gate, per function per target")
    results = []
    for target in TARGETS:
        path = os.path.join(HANDFUL_DIR, "composed2_%s%s"
                            % (target, SUFFIX[target]))
        source = None
        if os.path.exists(path):
            handle = open(path)
            source = handle.read()
            handle.close()
        for record in composed[target]:
            row = {"target": target, "func": record["func"],
                   "composed": record.get("composed", False)}
            if not record.get("composed"):
                row["cause"] = record.get("cause")
                results.append(row)
                say("   %-5s %-18s HOLE" % (target, record["func"]))
                continue
            row["calls"] = record["calls"]
            row["levels"] = sorted(set(c["level"] for c in record["calls"]))
            row["text"] = record["text"]
            symbol = record["func"]
            if target == "go":
                symbol = "main.%s" % record["func"]
            got, refusal = HUB1.carve(target, source, symbol)
            if got is None:
                row["carved"] = False
                row["cause"] = "body B did not build or carve: %s" % refusal
                results.append(row)
                say("   %-5s %-18s HOLE: %s" % (target, record["func"],
                                                row["cause"]))
                continue
            raw_bytes, mnem = got
            row["carved"] = True
            row["body_b_text"] = "; ".join(mnem)
            row["body_b_bytes"] = " ".join(raw_bytes)
            side_a_raw = bodies_a[record["func"]]
            if not side_a_raw.get("carved"):
                row["cause"] = ("body A did not carve: %s"
                                % side_a_raw.get("cause"))
                results.append(row)
                continue
            row["body_a_text"] = side_a_raw["body_text"]
            row["body_a_bytes"] = side_a_raw["body_bytes"]
            try:
                plan = params_for_gate(record["params"])
                families_a = HUB1.families_for("go", plan)
                families_b = HUB1.families_for(target, plan)
            except Refused as refusal:
                row["cause"] = refusal.cause
                results.append(row)
                continue
            except Exception as problem:                     # noqa: BLE001
                row["cause"] = "%s: %s" % (type(problem).__name__, problem)
                results.append(row)
                continue
            label_a = "handful2A_%s" % record["func"]
            label_b = "handful2B_%s_%s" % (target, record["func"])
            side_a = {"canon": HUB1.wrapped(shared, "go", side_a_raw["raw"],
                                            side_a_raw["mnem"], label_a),
                      "families": families_a}
            side_b = {"canon": HUB1.wrapped(shared, target, raw_bytes,
                                            mnem, label_b),
                      "families": families_b}
            row["canon40_outcome_A"] = side_a["canon"].get("outcome")
            row["canon40_outcome_B"] = side_b["canon"].get("outcome")
            row["check"] = HUB1.gate_two_bodies(shared, side_a, side_b, plan)
            row["verdict"] = HUB1.verdict_word(row["check"])
            if target == "go" and row["verdict"] != "PROVED":
                row["re_posed_without_the_noinline_directive"] = \
                    HUB1.go_re_pose(shared, record, side_a, plan, families_b,
                                    HANDFUL_DIR, "composed2_go_inlinable.go")
            results.append(row)
            extra = ""
            again = row.get("re_posed_without_the_noinline_directive")
            if again is not None:
                extra = "   (without the directive: %s)" % again.get("verdict")
            say("   %-5s %-18s %s%s" % (target, record["func"],
                                        row["verdict"], extra))
            check_memory("gate %s %s" % (target, record["func"]))
    say("[6/6] writing")
    nodes_out = []
    for key in sorted(resolutions):
        value = resolutions[key]
        record = dict(value["node_record"])
        record["resolved_unit"] = None
        record["cell"] = None
        record["pair"] = None
        record["entry_id"] = None
        if value["row"] is not None:
            record["resolved_unit"] = value["row"]["unit"]
            record["cell"] = value["row"].get("cell")
            record["pair"] = value["row"].get("pair")
            record["entry_id"] = value["row"].get("entry_id")
            record["levels"] = {}
            for target in TARGETS:
                found, causes = levels_for(target, value["row"], document)
                record["levels"][target] = {
                    "served_at": [level for level, _entry in found],
                    "causes": causes,
                }
        else:
            record["cause"] = value["cause"]
        nodes_out.append(record)
    write_json(ORACLE2_JSON, {
        "meta": {
            "task": "hub2",
            "node": "hq.research.arch_unit_oracle.hub_compiler.oracle_test",
            "what": "the same handful task hub1 composed, resolved at the "
                    "dictionary's two levels: every operator node with "
                    "its typed operands, the corpus unit the corpus "
                    "attests, the level the dictionary serves it at, the "
                    "composed source per target, and the gate over go's "
                    "own body and the composed body",
            "file": HANDFUL_GO,
            "peak_kb": peak_kb(),
        },
        "nodes": nodes_out,
        "bodies_a": {k: {"body_text": v.get("body_text"),
                         "body_bytes": v.get("body_bytes"),
                         "cause": v.get("cause")}
                     for k, v in bodies_a.items()},
        "results": results,
    })
    say("   %s" % ORACLE2_JSON)
    say("peak resident: %d kB" % peak_kb())
    return 0


# ==================================================================
# section 9: THE MEASURE -- the corpus's own go units
# ==================================================================
#
# Body A is not rebuilt: the corpus's own canon40 record for the unit IS
# go's own carved body, and it is the object every proof of this line has
# been posed against.  Body B is the composition of that unit's own
# construct for the target, built and carved at the target's own ship
# flags.  Task hub1 asked the 134 units that name one cell; this task
# asks EVERY corpus go unit, and the 134 are flagged so the two tasks'
# numbers sit beside each other.

def compose_unit(target, row, level, entry, parser, name):
    """the unit's own construct, composed for the target as one call at
    the level the dictionary serves it at."""
    params = HUB1.unit_parameters(row, parser)
    result = row["holders"]["result"]
    positions = HUB1.unit_operand_parameters(row, parser)
    if positions is None:
        raise Refused("the corpus unit's own source does not read its "
                      "construct's operands straight off its own "
                      "parameters")
    values = []
    for parameter_index in positions:
        if parameter_index >= len(params):
            raise Refused("the unit's own construct reads its parameter "
                          "%d and the unit declares %d"
                          % (parameter_index, len(params)))
        values.append(params[parameter_index]["name"])
    operand_types = [row["holders"]["lhs"]]
    if row["holders"]["arity"] == "binary":
        operand_types.append(row["holders"]["rhs"])
    call = one_call(target, level, row, entry, parser, values,
                    operand_types)
    text = narrow_answer(target, call, result)
    lines = [statement(target, "hub_t0", result, text),
             HUB1.returning(target, "hub_t0")]
    head = declaration(target, name, params, result)
    return {"text": HUB1.function_text(target, head, lines),
            "params": params, "result": result, "level": level,
            "entry": entry["unit"], "symbol": entry["symbol"],
            "route": entry.get("route"), "kind": entry.get("kind")}


def measure_command(limit=None):
    say("[1/4] the dictionary and the corpus's go units")
    document = read_json(DICTIONARY2)
    rows = document["go_units"]
    if limit is not None:
        rows = rows[:limit]
    units = HUB1.go_units_held()
    say("   corpus go units: %d; asked here: %d" % (len(document["go_units"]),
                                                    len(rows)))
    parser = HUB1.go_parser()
    shared = HUB1.build_shared()
    say("[2/4] composing, building, carving and gating, one unit at a time")
    results = []
    total = len(rows) * len(TARGETS)
    done = 0
    for row in rows:
        record = units.get(row["unit"])
        for target in TARGETS:
            done = done + 1
            out = {"unit": row["unit"], "lang": "go", "target": target,
                   "asked_by_hub1": row.get("cell") is not None,
                   "cell": None if not row.get("cell")
                           else cell_label(row["cell"]),
                   "entry_id": row.get("entry_id"),
                   "holders": row["holders"],
                   "attested_ledger_rows": None,
                   "pool_members": None}
            found, causes = levels_for(target, row, document)
            if not found:
                out["composed"] = False
                out["cause"] = "; ".join(causes)
                results.append(out)
                continue
            name = HUB1.sanitize_name(row["unit"])
            built = None
            for level, entry in found:
                try:
                    built = compose_unit(target, row, level, entry, parser,
                                         name)
                    out["level"] = level
                    out["route"] = entry.get("route")
                    out["kind"] = entry.get("kind")
                    out["attested_ledger_rows"] = \
                        entry.get("attested_ledger_rows")
                    if level == "body":
                        out["pool_members"] = (row.get("entry") or {}).get(
                            "member_count")
                    break
                except Refused as refusal:
                    causes.append("%s: %s" % (level, refusal.cause))
                except Exception as problem:                 # noqa: BLE001
                    causes.append("%s: %s: %s"
                                  % (level, type(problem).__name__, problem))
            if built is None:
                out["composed"] = False
                out["cause"] = "; ".join(causes)
                results.append(out)
                continue
            out["composed"] = True
            out["text"] = built["text"]
            out["symbol"] = built["symbol"]
            entry = None
            for level, candidate in found:
                if level == out["level"]:
                    entry = candidate
            plans = [(name, built["params"], built["result"])]
            texts = [built["text"]]
            if target == "go":
                emulations = [(entry["source"], entry["symbol"])]
                texts.append(go_main_for(plans))
            else:
                emulations = [entry["source"]]
            source = compose_file(target, emulations, texts)
            symbol = name
            if target == "go":
                symbol = "main.%s" % name
            got, refusal = HUB1.carve(target, source, symbol)
            if got is None:
                out["carved"] = False
                out["cause"] = ("body B did not build or carve: %s"
                                % refusal)
                results.append(out)
                continue
            raw_bytes, mnem = got
            out["carved"] = True
            out["body_b_text"] = "; ".join(mnem)
            if record is None:
                out["cause"] = "the corpus holds no canon40 record"
                results.append(out)
                continue
            out["body_a_text"] = record.get("body_text")
            try:
                plan = params_for_gate(built["params"])
                families_a = HUB1.families_for("go", plan)
                families_b = HUB1.families_for(target, plan)
            except Refused as refusal:
                out["cause"] = refusal.cause
                results.append(out)
                continue
            except Exception as problem:                     # noqa: BLE001
                out["cause"] = "%s: %s" % (type(problem).__name__, problem)
                results.append(out)
                continue
            side_a = {"canon": record, "families": families_a}
            side_b = {"canon": HUB1.wrapped(shared, target, raw_bytes, mnem,
                                            "measure2B_%s_%s"
                                            % (target, name)),
                      "families": families_b}
            out["check"] = HUB1.gate_two_bodies(shared, side_a, side_b, plan)
            out["verdict"] = HUB1.verdict_word(out["check"])
            if target == "go" and out["verdict"] != "PROVED":
                relaxed = compose_file(target, emulations, texts, True)
                out["re_posed_without_the_noinline_directive"] = \
                    HUB1.measure_re_pose(shared, relaxed, symbol, side_a,
                                         plan, families_b, name)
            results.append(out)
            if done % 25 == 0 or done == total:
                say("   [%d/%d] %d kB resident" % (done, total, peak_kb()))
            check_memory("measure %s %s" % (target, row["unit"]))
    say("[3/4] the counts")
    counts = measure_counts(results)
    for target in TARGETS:
        bucket = counts["per_target"][target]
        say("   %-5s composed %3d/%3d, proved %3d, disproved %3d, "
            "undecided %3d" % (target, bucket["composed"],
                               bucket["attempted"], bucket["proved"],
                               bucket["disproved"], bucket["undecided"]))
        for level in ["cell", "pair", "body"]:
            inner = counts["per_target_level"][target][level]
            say("      %-5s composed %3d, proved %3d"
                % (level, inner["composed"], inner["proved"]))
    say("[4/4] writing")
    write_json(MEASURE2_JSON, {
        "meta": {
            "task": "hub2",
            "node": "hq.research.arch_unit_oracle.hub_compiler",
            "what": "over every corpus go unit, at which of the "
                    "dictionary's levels the unit is served, whether the "
                    "composition builds, and whether the gate proves it "
                    "against go's own body",
            "peak_kb": peak_kb(),
        },
        "counts": counts,
        "results": results,
    })
    say("   %s" % MEASURE2_JSON)
    say("peak resident: %d kB" % peak_kb())
    return 0


def empty_bucket():
    return {"attempted": 0, "composed": 0, "carved": 0, "proved": 0,
            "proved_under_caller_extension": 0, "disproved": 0,
            "undecided": 0, "composed_ledger_rows": 0,
            "proved_ledger_rows": 0, "composed_pool_members": 0,
            "re_posed": 0, "proved_on_the_re_pose": 0,
            "re_posed_ledger_rows": 0}


def count_into(bucket, row):
    bucket["attempted"] += 1
    if not row.get("composed"):
        return
    bucket["composed"] += 1
    rows_covered = row.get("attested_ledger_rows") or 0
    bucket["composed_ledger_rows"] += rows_covered
    bucket["composed_pool_members"] += row.get("pool_members") or 0
    if not row.get("carved"):
        return
    bucket["carved"] += 1
    verdict = row.get("verdict")
    again = row.get("re_posed_without_the_noinline_directive")
    if again is not None and again.get("verdict") is not None:
        bucket["re_posed"] += 1
        if again["verdict"] in ("PROVED", "PROVED_UNDER_CALLER_EXTENSION"):
            bucket["proved_on_the_re_pose"] += 1
            bucket["re_posed_ledger_rows"] += rows_covered
    if verdict is None:
        bucket["undecided"] += 1
        return
    if verdict == "PROVED":
        bucket["proved"] += 1
        bucket["proved_ledger_rows"] += rows_covered
    elif verdict == "PROVED_UNDER_CALLER_EXTENSION":
        bucket["proved_under_caller_extension"] += 1
        bucket["proved_ledger_rows"] += rows_covered
    elif verdict == "DISPROVED":
        bucket["disproved"] += 1
    else:
        bucket["undecided"] += 1


def measure_counts(results):
    per_target = {}
    per_target_level = {}
    hub1_population = {}
    causes = {}
    for target in TARGETS:
        per_target[target] = empty_bucket()
        hub1_population[target] = empty_bucket()
        per_target_level[target] = {}
        for level in ["cell", "pair", "body"]:
            per_target_level[target][level] = empty_bucket()
        causes[target] = collections.Counter()
    for row in results:
        target = row["target"]
        count_into(per_target[target], row)
        if row.get("asked_by_hub1"):
            count_into(hub1_population[target], row)
        level = row.get("level")
        if level is not None:
            count_into(per_target_level[target][level], row)
        if not row.get("composed") or not row.get("carved"):
            causes[target][row.get("cause") or "(no cause)"] += 1
            continue
        verdict = row.get("verdict")
        if verdict in ("PROVED", "PROVED_UNDER_CALLER_EXTENSION"):
            continue
        causes[target][(row.get("check") or {}).get("reason")
                       or row.get("cause") or "(no reason)"] += 1
    return {"per_target": per_target,
            "per_target_level": per_target_level,
            "over_task_hub1s_own_population": hub1_population,
            "causes": {t: dict(causes[t]) for t in TARGETS}}


# ==================================================================
# section 10: THE TABLES -- hub1 beside hub2, everywhere
# ==================================================================

def hub1_handful():
    """task hub1's own verdicts, off its own artifact, READ."""
    path = os.path.join(HERE, "oracle_test.json")
    if not os.path.exists(path):
        return {}
    document = read_json(path)
    out = {}
    for row in document["results"]:
        verdict = row.get("verdict")
        if verdict is None:
            verdict = "HOLE"
        again = row.get("re_posed_without_the_noinline_directive")
        second = None
        if again is not None:
            second = again.get("verdict")
        out[(row["func"], row["target"])] = (verdict, second)
    return out


def hub1_measure():
    path = os.path.join(HERE, "measure.json")
    if not os.path.exists(path):
        return {}
    document = read_json(path)
    return document["counts"]["per_target"]


def tables_command():
    lines = []
    oracle = read_json(ORACLE2_JSON)
    lines.append("# oracle_test2 -- task hub2, Hub v2's numbers beside "
                 "task hub1's")
    lines.append("")
    lines.append("Generated by `hub2.py tables` off `oracle_test2.json` "
                 "and `measure2.json`, with task hub1's own "
                 "`oracle_test.json` and `measure.json` READ beside them.")
    lines.append("")
    lines.append("## 1. The handful, node by node, and the level the "
                 "dictionary serves each node at")
    lines.append("")
    lines.append("One row per operator node of "
                 "`Research/oracle/hub/handful/handful.go`: where it is, "
                 "what go's own type checker says its operands and its "
                 "result are, the corpus unit the corpus attests for it, "
                 "and -- per target -- the level the dictionary serves "
                 "that unit at.")
    lines.append("")
    rows = []
    for node in oracle["nodes"]:
        cell = node.get("cell")
        pair = node.get("pair")
        served = []
        for target in TARGETS:
            levels = ((node.get("levels") or {}).get(target) or {})
            got = levels.get("served_at") or []
            served.append(", ".join(got) or "--")
        rows.append([node.get("func"),
                     "%d:%d" % (node["position"]["line"],
                                node["position"]["col"]),
                     "`%s`" % node.get("text"),
                     node.get("lhs"), node.get("rhs"), node.get("result"),
                     node.get("resolved_unit") or "--",
                     "`%s`" % cell_label(cell) if cell else "--",
                     "`%s`" % pair_label(pair["setter"], pair["consumer"])
                     if pair else "--",
                     node.get("entry_id") or "--"] + served)
    lines.append(pipe_table(["function", "line:col", "the node, LITERAL",
                             "lhs holder", "rhs holder", "result holder",
                             "corpus unit", "cell", "pair", "pool entry",
                             "served on c", "served on rust",
                             "served on go"], rows))
    lines.append("")
    lines.append("## 2. The handful, function by function and target by "
                 "target: task hub1 then task hub2")
    lines.append("")
    before = hub1_handful()
    rows = []
    for row in oracle["results"]:
        verdict = row.get("verdict")
        if verdict is None:
            verdict = "HOLE"
        again = row.get("re_posed_without_the_noinline_directive")
        second = "--"
        if again is not None:
            second = again.get("verdict") or ("not carved: %s"
                                              % again.get("cause"))
        was = before.get((row["func"], row["target"]))
        was_word = "--"
        was_second = "--"
        if was is not None:
            was_word = was[0]
            was_second = was[1] or "--"
        rows.append([row["func"], row["target"], was_word, was_second,
                     verdict, second,
                     ", ".join(row.get("levels") or []) or "--"])
    lines.append(pipe_table(["function", "target",
                             "hub1: the gate's verdict",
                             "hub1: re-posed without `//go:noinline`",
                             "hub2: the gate's verdict",
                             "hub2: re-posed without `//go:noinline`",
                             "hub2: the levels it composed at"], rows))
    lines.append("")
    lines.append("## 3. The handful's holes, by cause")
    lines.append("")
    rows = []
    for row in oracle["results"]:
        if row.get("verdict") is not None:
            continue
        rows.append([row["func"], row["target"],
                     (row.get("cause") or "--").replace("|", "/")])
    lines.append(pipe_table(["function", "target", "cause"], rows))
    lines.append("")
    lines.append("## 4. Body A and body B, per function and target")
    lines.append("")
    rows = []
    for row in oracle["results"]:
        if not row.get("carved"):
            continue
        rows.append([row["func"], row["target"],
                     "`%s`" % row.get("body_a_text"),
                     "`%s`" % row.get("body_b_text")])
    lines.append(pipe_table(["function", "target",
                             "body A, go's own, LITERAL",
                             "body B, the composition, LITERAL"], rows))
    lines.append("")
    if os.path.exists(MEASURE2_JSON):
        measure = read_json(MEASURE2_JSON)
        counts = measure["counts"]
        earlier = hub1_measure()
        lines.append("## 5. The measure over task hub1's own population: "
                     "hub1 then hub2")
        lines.append("")
        lines.append("The 134 corpus go units task hub1 asked about -- the "
                     "ones task o2's narrow rule holds and that name "
                     "exactly one cell. Same units, same measure, so the "
                     "two rows are the same object twice.")
        lines.append("")
        rows = []
        for target in TARGETS:
            was = earlier.get(target) or {}
            now = counts["over_task_hub1s_own_population"][target]
            rows.append([target, "hub1", was.get("attempted"),
                         was.get("composed"),
                         was.get("composed_ledger_rows"),
                         was.get("carved"), was.get("proved"),
                         was.get("proved_under_caller_extension"),
                         was.get("disproved"), was.get("undecided"),
                         was.get("proved_ledger_rows"),
                         was.get("proved_on_the_re_pose")])
            rows.append([target, "hub2", now["attempted"], now["composed"],
                         now["composed_ledger_rows"], now["carved"],
                         now["proved"],
                         now["proved_under_caller_extension"],
                         now["disproved"], now["undecided"],
                         now["proved_ledger_rows"],
                         now["proved_on_the_re_pose"]])
        lines.append(pipe_table(["target", "task", "units asked",
                                 "composed",
                                 "ledger rows the composed cells cover",
                                 "built and carved", "proved",
                                 "proved under caller extension",
                                 "disproved", "undecided",
                                 "ledger rows the proved cells cover",
                                 "proved on the re-pose without "
                                 "`//go:noinline`"], rows))
        lines.append("")
        lines.append("## 6. The measure over EVERY corpus go unit, per "
                     "target")
        lines.append("")
        rows = []
        for target in TARGETS:
            bucket = counts["per_target"][target]
            rows.append([target, bucket["attempted"], bucket["composed"],
                         bucket["carved"], bucket["proved"],
                         bucket["proved_under_caller_extension"],
                         bucket["disproved"], bucket["undecided"],
                         bucket["composed_ledger_rows"],
                         bucket["proved_ledger_rows"],
                         bucket["composed_pool_members"],
                         bucket["proved_on_the_re_pose"]])
        lines.append(pipe_table(["target", "units asked", "composed",
                                 "built and carved", "proved",
                                 "proved under caller extension",
                                 "disproved", "undecided",
                                 "ledger rows the composed cells cover",
                                 "ledger rows the proved cells cover",
                                 "pool members the composed body entries "
                                 "cover",
                                 "proved on the re-pose without "
                                 "`//go:noinline`"], rows))
        lines.append("")
        lines.append("## 7. The measure by level")
        lines.append("")
        rows = []
        for target in TARGETS:
            for level in ["cell", "pair", "body"]:
                bucket = counts["per_target_level"][target][level]
                rows.append([target, level, bucket["composed"],
                             bucket["carved"], bucket["proved"],
                             bucket["proved_under_caller_extension"],
                             bucket["disproved"], bucket["undecided"],
                             bucket["proved_on_the_re_pose"]])
        lines.append(pipe_table(["target", "level", "composed",
                                 "built and carved", "proved",
                                 "proved under caller extension",
                                 "disproved", "undecided",
                                 "proved on the re-pose without "
                                 "`//go:noinline`"], rows))
        lines.append("")
        lines.append("## 8. The measure, by cause")
        lines.append("")
        for target in TARGETS:
            lines.append("### %s" % target)
            lines.append("")
            rows = []
            causes = counts["causes"][target]
            for cause in sorted(causes, key=lambda c: -causes[c]):
                rows.append([causes[cause], cause.replace("|", "/")])
            lines.append(pipe_table(["units", "cause"], rows))
            lines.append("")
    handle = open(ORACLE2_MD, "w")
    handle.write("\n".join(lines) + "\n")
    handle.close()
    say("   %s" % ORACLE2_MD)
    return 0


def main(argv):
    if len(argv) < 2:
        say(__doc__)
        return 2
    command = argv[1]
    if command == "dictionary":
        return dictionary_command()
    if command == "handful":
        return handful_command()
    if command == "measure":
        limit = None
        if len(argv) > 2:
            limit = int(argv[2])
        return measure_command(limit)
    if command == "tables":
        return tables_command()
    say("unknown command %r" % command)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
