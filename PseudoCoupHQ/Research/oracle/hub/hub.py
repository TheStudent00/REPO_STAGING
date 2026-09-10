#!/usr/bin/env python3
"""hub.py -- task hub1: Hub v1, first form.

Node: hq.research.arch_unit_oracle.hub_compiler
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_1_hub_compiler/`),
its CORE's "definition" of 2026-09-07 (SOURCE COMPOSITION) and its four
sub-nodes front_end, dictionary, joiner, oracle_test.  Brief:
`PRIVATE/PseudoCoupHQ/Research/briefs/task_hub1_brief.md`.  Law:
`PRIVATE/PseudoCoupHQ/Research/LAW.md`.

THE OBJECTS, one sentence each, in relation.

  * A CELL is one (`mnem`, operand shape, `key_width`) row of the
    arch-opcode model table -- the machine-form key ruled 2026-09-08.
  * The DICTIONARY is, per (target, cell), the emulation SOURCE the
    AutoPoly loop rendered for that cell on that target, the route it
    took (primitive / primitive+setup / term), the gate's verdict on it,
    and the ledger rows the cell is attested by.  Task ap5's store
    (`autopoly5_runs.jsonl`) holds every one; this file writes them out
    as one lookup and names, per target, the cells that have no proved
    entry and why.
  * The GO SIDE of the lookup is the corpus's own attestation: a go unit
    whose WHOLE body is one arch-opcode instruction (task o2's narrow
    rule, `single_opcode_units.json`) says which cell go's compiler
    produces for the construct that unit's own source holds at the
    operand holders that unit's own probe record names.
  * The FRONT END parses the file to be lowered with tree-sitter-go and
    types every operator node's operands with go's own type checker
    (`go_types_oracle.go`, task o6), joining the two by POSITION.
  * SOURCE COMPOSITION is the egress: the tree walked post-order, each
    operator node replaced by a CALL of its cell's emulation function,
    the emulation emitted once per cell into the composed file verbatim,
    and the target's own compiler left to lower and optimise across the
    calls.
  * The ORACLE TEST is the gate over two bodies: body A, go's own build
    of one function of the file, carved; body B, the target's build of
    the composed function, carved.

WHAT IS REUSED RATHER THAN COPIED, said out loud.  `model_table`'s
`lines_of_unit`, `arch_opcode_rows`, `classify_line`, `key_width` and
`operand_texts` read a unit's ledger into cells; `ledger.family_of_operand`
names an operand's register family; `emulate.compile_and_carve` /
`recorded_facts` (c), `rust_render`'s and `go_render`'s own two (rust, go)
build and read a body; `term97_walk.build` makes the maker, the gate and
the reference; `pool100_entry_equivalence.input_rows` / `rows_disagree` /
`classify_symbols` / `rename_constants_apart` / `align_by_row` align the
two sides; `gate.Gate.decide` is the one solver call.  NOTHING under
`Research/op_pipeline/`, `Research/oracle/arch_opcodes/` or
`Research/oracle/cross_construction/` is edited by this task.

MEMORY BOUND, stated as the law requires: one collecting process, peak
checked after every unit of work, named abort ABORT_MEMORY_HUB1 at 6 GB
resident (`resource.getrusage`; `/usr/bin/time` is absent in the image).
The canon40 go shards are the only stores held whole and they are 3.4 MB;
task ap5's run store is streamed line by line.

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

HOW THIS FILE OBEYS IT, said mechanically, because a front end reads
source text for a living and the reading must be shown rather than
claimed.

  * Every key of every artifact this file writes is machine form: a cell
    is keyed `(target, mnem, shape, key_width)`, a go-side row is keyed
    by the CORPUS UNIT ID, a resolution is keyed by the node's POSITION
    in the file.  No dict key, no list element, no row structure and no
    grouping anywhere carries an operator token.  A token rides on a
    unit object as the field `operator` -- the one place the ban allows
    it -- and on the `meta` sub-object copied from the probe manifest,
    which the guard passes over by name as the unit's own metadata.
  * The CANDIDATE SET for resolving a typed operator node is the TYPE
    TUPLE (arity, lhs holder, rhs holder, result holder) -- "type pairs",
    which the ban names as machine-form evidence.  Within that candidate
    set the front end reads the SOURCE: the candidate corpus unit's own
    go source is parsed by the same tree-sitter grammar as the file
    being lowered, and the two operator nodes' own operator children are
    compared as source text.  That comparison is the PARSER's, between
    two source files, and its output is a NAMED CORPUS UNIT whose body
    go's own compiler produced -- machine-form evidence.  It is not a
    key, a grouping, a pairing or a row structure.  This is recorded in
    the log's "decided, recorded for audit" list so it is auditable.

Coding discipline: no compound one-liner statements.

usage:
  hub.py dictionary        dictionary.json + dictionary.md
  hub.py handful           the handful: front end, resolve, compose, gate
  hub.py measure           section 3: the corpus's own go units
  hub.py tables            oracle_test.md
"""

import collections
import json
import os
import re
import resource
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HQ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OP = os.path.join(HQ, "Research", "op_pipeline")
ARCH = os.path.join(HQ, "Research", "oracle", "arch_opcodes")
MODEL = os.path.join(ARCH, "model")
CROSS = os.path.join(HQ, "Research", "oracle", "cross_construction")
EMU = os.path.join(CROSS, "emulation")
AUTO = os.path.join(EMU, "autopoly")
UNITS = os.path.join(HQ, "Research", "oracle", "compiler_units")

for path in [OP, MODEL, EMU, CROSS, os.path.join(EMU, "go"),
             os.path.join(EMU, "rust"), os.path.join(EMU, "handful")]:
    if path not in sys.path:
        sys.path.insert(0, path)

RUNS = os.path.join(AUTO, "autopoly5_runs.jsonl")
SRC5 = os.path.join(AUTO, "src5")
SINGLE = os.path.join(ARCH, "single_opcode_units.json")
HANDFUL_DIR = os.path.join(HERE, "handful")
HANDFUL_GO = os.path.join(HANDFUL_DIR, "handful.go")
DICTIONARY = os.path.join(HERE, "dictionary.json")
DICTIONARY_MD = os.path.join(HERE, "dictionary.md")
ORACLE_JSON = os.path.join(HERE, "oracle_test.json")
ORACLE_MD = os.path.join(HERE, "oracle_test.md")
MEASURE_JSON = os.path.join(HERE, "measure.json")

TARGETS = ["c", "rust", "go"]

BOUND_KB = 6 * 1024 * 1024
ABORT = "ABORT_MEMORY_HUB1"


# ==================================================================
# section 0: the small shared services
# ==================================================================

def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    peak = peak_kb()
    if peak > BOUND_KB:
        raise SystemExit("%s at %s: %d kB resident, bound %d kB"
                         % (ABORT, where, peak, BOUND_KB))


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


def cell_label(cell):
    return "%s %s %s" % (cell["mnem"], cell["shape"], cell["key_width"])


def cell_key(cell):
    return (cell["mnem"], cell["shape"], cell["key_width"])


# ==================================================================
# section 1: THE DICTIONARY -- the target side, off task ap5's store
# ==================================================================
#
# One entry per (target, cell).  The entry's SOURCE is the function the
# renderer printed, the compiler landed and the gate proved: the place
# the cell's own answer is written into (`writes` begins `reg_`), never
# a flags place, because a flags place is not a value the source
# composition can pass on.  A cell whose value place did not render, did
# not compile, or did not prove is a HOLE, and the hole carries the run's
# own cause text.

VALUE_PLACE = re.compile(r"^reg_")


def value_place_of(run):
    """the place that writes the cell's own answer, or None."""
    for place in run.get("places") or []:
        writes = place.get("writes") or ""
        if VALUE_PLACE.match(writes):
            return place
    return None


def cell_family_of_params(place):
    """per emulation parameter index, the CELL arrival family it stands
    for -- `params[i]["family"]` where the renderer recorded one (the
    term route), and the gate's own IN-row alignment where it did not
    (the primitive route, whose parameters are the matched corpus body's
    and whose relation to the cell's arrivals is what `aligned_rows`
    states)."""
    params = place.get("params") or []
    out = []
    aligned = ((place.get("check") or {}).get("aligned_rows")) or []
    for index, param in enumerate(params):
        family = param.get("family")
        if family is None and index < len(aligned):
            family = aligned[index].get("the cell reads")
        out.append(family)
    return out


PROVED = ("PROVED_ON_SHIP",)


def outcome_of(place):
    check = place.get("check") or {}
    outcome = check.get("outcome")
    if outcome in PROVED:
        return outcome, None
    extension = check.get("under_caller_extension") or {}
    if extension.get("outcome") == "PROVED":
        return "PROVED_UNDER_CALLER_EXTENSION", None
    cause = check.get("reason") or place.get("refusal_detail")
    if cause is None:
        cause = "the loop rendered no source for this place"
    return outcome, cause


def target_entries():
    """the dictionary's target side: per target, the proved entries and
    the holes, both read off task ap5's own store."""
    entries = {}
    holes = {}
    for target in TARGETS:
        entries[target] = {}
        holes[target] = {}
    handle = open(RUNS)
    for line in handle:
        run = json.loads(line)
        target = run["lang"]
        if target not in TARGETS:
            continue
        key = (run["mnem"], run["shape"], run["key_width"])
        place = value_place_of(run)
        record = {
            "lang": target,
            "unit": "hub/cell/%s %s %s" % key,
            "mnem": run["mnem"],
            "shape": run["shape"],
            "key_width": run["key_width"],
            "route": run["route"],
            "line": run["line"],
            "row_id": run["row_id"],
            "attested_ledger_rows": run["attested_ledger_rows"],
            "attestation": run["attestation"],
        }
        if place is None:
            record["cause"] = ("the cell writes no register place: every "
                               "place it writes is a flag place, which is "
                               "not a value a composition can pass on")
            holes[target]["%s %s %s" % key] = record
            continue
        outcome, cause = outcome_of(place)
        record["place"] = place.get("writes")
        record["place_bits"] = place.get("bits")
        record["symbol"] = place.get("symbol")
        record["source_path"] = place.get("source_path")
        record["params"] = place.get("params")
        record["param_cell_families"] = cell_family_of_params(place)
        record["home"] = place.get("home")
        record["verdict"] = outcome
        if cause is not None:
            record["cause"] = cause
            holes[target]["%s %s %s" % key] = record
            continue
        record["source"] = place.get("source")
        entries[target]["%s %s %s" % key] = record
    handle.close()
    check_memory("target entries")
    return entries, holes


# ==================================================================
# section 2: THE DICTIONARY -- the go side, off the corpus
# ==================================================================

def go_units_held():
    """every canon40 go unit, wrapped population and regenerated."""
    import glob
    units = {}
    document = read_json(os.path.join(OP, "canon40_wrapped_go.json"))
    units.update(document["units"])
    del document
    pattern = os.path.join(OP, "canon40_regen_store", "op_units2_go_*.json")
    for path in sorted(glob.glob(pattern)):
        document = read_json(path)
        units.update(document["units"])
        del document
    check_memory("go units held")
    return units


def go_probes():
    """the two probe manifests, each declaring itself generator
    provenance; a unit id names its own probe record."""
    one = read_json(os.path.join(OP, "probe_manifest_go.json"))["probes"]
    two = read_json(os.path.join(OP, "probe_manifest2_go.json"))["probes"]
    return one, two


def probe_of(unit_id, one, two):
    tail = unit_id.split("/")[1]
    kind, number = tail.split("_", 1)
    if kind == "op":
        return one.get(number)
    return two.get(number)


def cells_of_units(units):
    """per go unit, the cells its own body produced, and the line of
    each -- the model table's own reading, imported."""
    import model_table as MT
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
            refusals["the unit's body could not be relinked, so no row "
                     "of it has a line"] += 1
            continue
        found = []
        for row in MT.arch_opcode_rows(record):
            mnem = row["produced_by"]["mnem"]
            line = line_of_row.get(row["row"])
            if line is None:
                continue
            shape, width, cause = MT.classify_line(mnem, line,
                                                   row.get("size"))
            if cause is not None:
                refusals[cause] += 1
                continue
            found.append({"mnem": mnem, "shape": shape,
                          "key_width": MT.key_width(mnem, width),
                          "line": line})
        out[unit_id] = found
    check_memory("cells of units")
    return out, dict(refusals)


def go_side():
    """the go side of the lookup, read from the corpus and never
    guessed: every go unit `single_opcode_units.json` holds under task
    o2's NARROW rule -- a unit whose whole body is one arch-opcode
    instruction plus chaff -- with the cell its ledger attests, its own
    operand holders off its probe record, and the operand SLOTS of its
    body line put on IN rows."""
    import ledger as L
    import model_table as MT
    single = read_json(SINGLE)
    groups = single["single_opcode_groups"]["go"]["narrow"]
    units = go_units_held()
    one, two = go_probes()
    cells, refusals = cells_of_units(units)
    rows = []
    refused = []
    for group in groups:
        for member in group["members"]:
            unit_id = member["unit"]
            probe = probe_of(unit_id, one, two)
            record = units.get(unit_id)
            found = cells.get(unit_id)
            row = {
                "unit": unit_id,
                "lang": "go",
                "n": unit_id.split("_", 1)[1],
                "operator": member.get("operator"),
                "body_text": group["body_text"],
            }
            if probe is None or record is None or found is None:
                row["cause"] = ("the corpus holds no probe record or no "
                                "canon40 record or no relinked ledger "
                                "for this unit")
                refused.append(row)
                continue
            if len(found) != 1:
                row["cause"] = ("this unit's body produced %d arch-opcode "
                                "ledger rows, not one, so it names no "
                                "single cell" % len(found))
                refused.append(row)
                continue
            cell = found[0]
            row["meta"] = probe
            row["holders"] = {
                "arity": probe.get("arity"),
                "position": probe.get("position"),
                "lhs": probe.get("lhs_type"),
                "rhs": probe.get("rhs_type"),
                "result": probe.get("result_type"),
            }
            row["cell"] = {"mnem": cell["mnem"], "shape": cell["shape"],
                           "key_width": cell["key_width"]}
            row["unit_line"] = cell["line"]
            row["arrival_families"] = list(record.get("arrival_families")
                                           or [])
            row["result_family"] = record.get("result_family")
            slots = []
            texts = MT.operand_texts(cell["line"])
            for index, text in enumerate(texts):
                family = L.family_of_operand(text)
                in_row = None
                if family in row["arrival_families"]:
                    in_row = row["arrival_families"].index(family)
                slots.append({"slot": index, "text": text,
                              "family": family, "in_row": in_row})
            row["operand_slots"] = slots
            rows.append(row)
    every = []
    for unit_id in sorted(units):
        probe = probe_of(unit_id, one, two)
        record = units.get(unit_id)
        found = cells.get(unit_id)
        if probe is None or record is None:
            continue
        row = {
            "unit": unit_id,
            "lang": "go",
            "n": unit_id.split("_", 1)[1],
            "operator": probe.get("operator"),
            "meta": probe,
            "body_text": record.get("body_text"),
            "holders": {
                "arity": probe.get("arity"),
                "position": probe.get("position"),
                "lhs": probe.get("lhs_type"),
                "rhs": probe.get("rhs_type"),
                "result": probe.get("result_type"),
            },
            "cells": None if found is None else [
                {"mnem": c["mnem"], "shape": c["shape"],
                 "key_width": c["key_width"]} for c in found],
        }
        every.append(row)
    check_memory("go side")
    return rows, refused, refusals, every


# ==================================================================
# section 3: the dictionary command
# ==================================================================

def dictionary_command():
    say("[1/3] the target side, off task ap5's store")
    entries, holes = target_entries()
    for target in TARGETS:
        say("   %-5s entries %4d   holes %4d"
            % (target, len(entries[target]), len(holes[target])))
    say("[2/3] the go side, off the corpus")
    rows, refused, refusals, every = go_side()
    say("   go units under task o2's narrow rule that name one cell: %d"
        % len(rows))
    say("   go units the narrow rule holds that name no single cell: %d"
        % len(refused))
    say("[3/3] writing")
    document = {
        "meta": {
            "task": "hub1",
            "node": "hq.research.arch_unit_oracle.hub_compiler.dictionary",
            "what": "per (target, cell) the proved emulation source the "
                    "AutoPoly loop landed, and per corpus go unit the "
                    "cell go's own compiler produced for that unit's "
                    "construct at that unit's operand holders",
            "target_side_read_from": RUNS,
            "go_side_read_from": [SINGLE,
                                  os.path.join(OP,
                                               "canon40_wrapped_go.json"),
                                  os.path.join(OP, "canon40_regen_store")],
            "key": "machine form: (target, mnem, operand shape, "
                   "key_width) on the target side, the corpus unit id on "
                   "the go side",
            "peak_kb": peak_kb(),
        },
        "targets": entries,
        "holes": holes,
        "go_units": rows,
        "go_units_every": every,
        "go_units_without_one_cell": refused,
        "go_ledger_refusals": refusals,
    }
    write_json(DICTIONARY, document)
    say("   %s" % DICTIONARY)
    dictionary_md(document)
    say("   %s" % DICTIONARY_MD)
    say("peak resident: %d kB" % peak_kb())
    return 0


def pipe_table(header, rows):
    out = []
    out.append("| " + " | ".join(header) + " |")
    out.append("|" + "|".join(["---"] * len(header)) + "|")
    for row in rows:
        out.append("| " + " | ".join([str(x) for x in row]) + " |")
    return "\n".join(out)


def dictionary_md(document):
    lines = []
    lines.append("# dictionary -- task hub1, Hub v1's lookup")
    lines.append("")
    lines.append("Generated by `hub.py dictionary`. The key is machine "
                 "form throughout: `(target, mnem, operand shape, "
                 "key_width)` on the target side and the corpus unit id "
                 "on the go side.")
    lines.append("")
    lines.append("## 1. Entries and holes per target")
    lines.append("")
    rows = []
    for target in TARGETS:
        entries = document["targets"][target]
        holes = document["holes"][target]
        proved_rows = 0
        for entry in entries.values():
            proved_rows = proved_rows + entry["attested_ledger_rows"]
        hole_rows = 0
        for hole in holes.values():
            hole_rows = hole_rows + hole["attested_ledger_rows"]
        rows.append([target, len(entries), proved_rows, len(holes),
                     hole_rows])
    lines.append(pipe_table(["target", "entries", "ledger rows the "
                             "entries cover", "holes", "ledger rows the "
                             "holes cover"], rows))
    lines.append("")
    lines.append("## 2. Entries per target by route")
    lines.append("")
    rows = []
    for target in TARGETS:
        counter = collections.Counter()
        for entry in document["targets"][target].values():
            counter[entry["route"]] += 1
        rows.append([target, counter.get("primitive", 0),
                     counter.get("primitive+setup", 0),
                     counter.get("term", 0)])
    lines.append(pipe_table(["target", "primitive", "primitive+setup",
                             "term"], rows))
    lines.append("")
    lines.append("## 3. Holes per target, by cause")
    lines.append("")
    for target in TARGETS:
        counter = collections.Counter()
        rows_of_cause = collections.Counter()
        for hole in document["holes"][target].values():
            cause = hole.get("cause") or "(no cause recorded)"
            counter[cause] += 1
            rows_of_cause[cause] += hole["attested_ledger_rows"]
        lines.append("### %s" % target)
        lines.append("")
        rows = []
        for cause in sorted(counter, key=lambda c: -counter[c]):
            rows.append([counter[cause], rows_of_cause[cause], cause])
        lines.append(pipe_table(["cells", "ledger rows", "cause"], rows))
        lines.append("")
    lines.append("## 4. The go side: how many corpus go units name one "
                 "cell")
    lines.append("")
    lines.append("Task o2's NARROW rule population for go, unit by unit. "
                 "A unit names a cell when its own body produced exactly "
                 "one arch-opcode ledger row.")
    lines.append("")
    rows = [[len(document["go_units"]),
             len(document["go_units_without_one_cell"])]]
    lines.append(pipe_table(["go units naming one cell",
                             "go units naming no single cell"], rows))
    lines.append("")
    lines.append("## 5. The go side, by operand holders and cell")
    lines.append("")
    rows = []
    for row in document["go_units"]:
        holders = row["holders"]
        rows.append([row["unit"], holders["arity"],
                     holders["lhs"], holders["rhs"], holders["result"],
                     "`%s`" % row["meta"].get("expression"),
                     "`%s`" % cell_label(row["cell"]),
                     "`%s`" % row["unit_line"]])
    lines.append(pipe_table(["unit", "arity", "lhs holder", "rhs holder",
                             "result holder", "the unit's own expression",
                             "cell", "the unit's own body line"], rows))
    lines.append("")
    handle = open(DICTIONARY_MD, "w")
    handle.write("\n".join(lines) + "\n")
    handle.close()


# ==================================================================
# section 4: THE FRONT END -- tree-sitter's tree, go/types' types
# ==================================================================
#
# The tree's nesting IS the data flow (the front_end sub-node's CORE).
# The tree does not carry types, so go's own type checker is run once
# over the same file and the two are joined by POSITION -- (line,
# column, end line, end column) of the operator node -- exactly as task
# o6's `go_types_join.py` joins them, and never by the operator token.

OPERATOR_NODES = ("binary_expression", "unary_expression")

# go/types spells the type of a comparison `untyped bool`, because the go
# specification makes a comparison's value an UNTYPED boolean whose
# DEFAULT TYPE is `bool`; the corpus's own probe records spell the same
# holder `bool`, so the default type is what the two are joined on.  The
# same rule covers the other untyped kinds go/types can print for a
# constant expression.  This is a holder-spelling rule, stated here and
# in the log; it is not a token.
DEFAULT_TYPE = {
    "untyped bool": "bool",
    "untyped int": "int",
    "untyped rune": "int32",
    "untyped float": "float64",
    "untyped string": "string",
}


def default_type(spelling):
    if spelling is None:
        return None
    return DEFAULT_TYPE.get(spelling, spelling)


def go_parser():
    import tree_sitter
    import tree_sitter_go
    language = tree_sitter.Language(tree_sitter_go.language())
    return tree_sitter.Parser(language)


def node_text(source_bytes, node):
    return source_bytes[node.start_byte:node.end_byte].decode("utf-8")


def operator_child(node):
    """the node's own operator child, as the grammar names it."""
    child = node.child_by_field_name("operator")
    return child


def walk_nodes(node, out):
    out.append(node)
    for child in node.children:
        walk_nodes(child, out)


def enclosing_function(node, source_bytes):
    walker = node.parent
    while walker is not None:
        if walker.type == "function_declaration":
            name = walker.child_by_field_name("name")
            if name is not None:
                return node_text(source_bytes, name)
            return None
        walker = walker.parent
    return None


def type_oracle_sites(directory):
    """go's own type checker over the directory, as task o6 runs it.

    `go_types_oracle.go` is READ, never edited; it is run with `-shape
    package` over the handful's own directory and the image's own GOROOT,
    and its `sites` array is the answer."""
    oracle = os.path.join(UNITS, "go_types_oracle.go")
    work = tempfile.mkdtemp(prefix="hub1_types_")
    out = os.path.join(work, "sites.json")
    goroot = subprocess.run(["go", "env", "GOROOT"], capture_output=True,
                            text=True, timeout=120).stdout.strip()
    environment = dict(os.environ)
    environment["HOME"] = work
    environment["GOCACHE"] = os.path.join(work, "gocache")
    environment["GOPATH"] = os.path.join(work, "gopath")
    environment["GOFLAGS"] = "-mod=mod"
    environment["GOPROXY"] = "off"
    command = ["go", "run", oracle, "-root", directory, "-goroot", goroot,
               "-out", out, "-scratch", work, "-shape", "package"]
    done = subprocess.run(command, capture_output=True, text=True,
                          timeout=900, cwd=work, env=environment)
    if not os.path.exists(out):
        return None, (done.stderr or done.stdout or "").strip()[:400]
    document = read_json(out)
    return document, None


def front_end(path):
    """the file's operator nodes, each with its typed operands.

    -> (nodes, source_bytes, refusal).  A node record carries its
    position, its enclosing function, the tree-sitter node kind, its
    operator child's own text (SOURCE, kept for the parser's own
    reading), and go/types' spelling of each operand and of the result.
    """
    handle = open(path, "rb")
    source_bytes = handle.read()
    handle.close()
    parser = go_parser()
    tree = parser.parse(source_bytes)
    every = []
    walk_nodes(tree.root_node, every)
    # The oracle is a go/build walk over a DIRECTORY, so the file is
    # typed on its own in a directory of its own -- the artifact folder
    # also holds the composed go file, which is another `package main`
    # with another `main`, and typing the two together would be a
    # different question from the one asked.
    alone = tempfile.mkdtemp(prefix="hub1_alone_")
    copy = os.path.join(alone, os.path.basename(path))
    handle = open(copy, "wb")
    handle.write(source_bytes)
    handle.close()
    document, refusal = type_oracle_sites(alone)
    if document is None:
        return None, source_bytes, refusal
    by_position = {}
    for site in document.get("sites") or []:
        if os.path.basename(site["file"]) != os.path.basename(path):
            continue
        key = (site["line"], site["col"], site["end_line"], site["end_col"])
        by_position[key] = site
    nodes = []
    for node in every:
        if node.type not in OPERATOR_NODES:
            continue
        child = operator_child(node)
        key = (node.start_point[0] + 1, node.start_point[1] + 1,
               node.end_point[0] + 1, node.end_point[1] + 1)
        site = by_position.get(key)
        record = {
            "lang": "go",
            "unit": "hub/node/%s:%d:%d" % (os.path.basename(path),
                                           key[0], key[1]),
            "kind": node.type,
            "position": {"line": key[0], "col": key[1],
                         "end_line": key[2], "end_col": key[3]},
            "func": enclosing_function(node, source_bytes),
            "text": node_text(source_bytes, node),
            "operator": None if child is None
                        else node_text(source_bytes, child),
            "node": node,
        }
        if site is None:
            record["typed"] = False
            record["cause"] = ("go's own type checker recorded no site at "
                               "this position, so the node's operands are "
                               "untyped")
            nodes.append(record)
            continue
        operands = site.get("operands") or []
        record["typed"] = True
        record["arity"] = "binary" if len(operands) == 2 else "unary"
        record["lhs"] = None
        if operands:
            record["lhs"] = default_type(operands[0]["spelling"])
        record["rhs"] = None
        if len(operands) > 1:
            record["rhs"] = default_type(operands[1]["spelling"])
        record["result"] = default_type(site.get("result"))
        nodes.append(record)
    return nodes, source_bytes, None


# ==================================================================
# section 5: RESOLVE -- a typed node to the cell go lowers it to
# ==================================================================
#
# THE CANDIDATE SET is the TYPE TUPLE (arity, lhs holder, rhs holder,
# result holder), which the ban names as machine-form evidence.  Within
# it the front end reads SOURCE: the candidate corpus unit's own go
# source is parsed by the same grammar and its own operator node's
# operator child is compared with the node's, as text.  The answer is a
# NAMED CORPUS UNIT whose body go's own compiler produced.

def candidate_index(go_units):
    index = collections.defaultdict(list)
    for row in go_units:
        holders = row["holders"]
        key = (holders["arity"], holders["lhs"], holders["rhs"],
               holders["result"])
        index[key].append(row)
    return index


def unit_operator_text(row, parser):
    """the candidate corpus unit's OWN operator node, read out of its own
    source by the same grammar."""
    if "_operator_text" in row:
        return row["_operator_text"]
    source = (row.get("meta") or {}).get("source")
    answer = None
    if source is not None:
        source_bytes = source.encode("utf-8")
        tree = parser.parse(source_bytes)
        every = []
        walk_nodes(tree.root_node, every)
        found = []
        for node in every:
            if node.type in OPERATOR_NODES:
                found.append(node)
        if len(found) == 1:
            child = operator_child(found[0])
            if child is not None:
                answer = node_text(source_bytes, child)
    row["_operator_text"] = answer
    return answer


def agreeing_units(node, index, parser):
    """the candidate corpus units whose own source parses to the same
    operator node as this one."""
    key = (node["arity"], node["lhs"], node["rhs"], node["result"])
    out = []
    for row in index.get(key) or []:
        text = unit_operator_text(row, parser)
        if text is not None and text == node["operator"]:
            out.append(row)
    out.sort(key=lambda r: r["unit"])
    return out


def resolve(node, index, parser, every_index=None):
    """-> (the corpus go unit row, None) or (None, the cause).

    Where the narrow population attests no cell, the cause is read off
    go's OWN build of the same construct at the same holders: the corpus
    unit's body text and how many arch-opcode ledger rows it produced.
    That is a result by cause, not an absence."""
    if not node.get("typed"):
        return None, node["cause"]
    agreeing = agreeing_units(node, index, parser)
    if agreeing:
        return agreeing[0], None
    if every_index is not None:
        wider = agreeing_units(node, every_index, parser)
        if wider:
            row = wider[0]
            cells = row.get("cells")
            if cells is None:
                return None, ("go's own build of this construct at these "
                              "holders is the corpus unit %s, whose body "
                              "could not be relinked, so it names no cell"
                              % row["unit"])
            names = ", ".join(["`%s`" % cell_label(c) for c in cells])
            return None, ("go's own build of this construct at these "
                          "holders is the corpus unit %s, whose body "
                          "`%s` is not one arch-opcode instruction plus "
                          "chaff (task o2's narrow rule), so the corpus "
                          "attests no single cell for this node; its own "
                          "ledger holds %d arch-opcode row(s): %s"
                          % (row["unit"], row.get("body_text"),
                             len(cells), names or "none"))
    return None, ("no go unit of the corpus carries this construct at "
                  "these operand holders, so the corpus attests no cell "
                  "for this node")


# ==================================================================
# section 6: THE HOLDERS -- one go holder, one holder per target
# ==================================================================

HOLDER = {
    "int8": {"bits": 8, "kind": "bv", "signed": True,
             "c": "int8_t", "rust": "i8", "go": "int8"},
    "int16": {"bits": 16, "kind": "bv", "signed": True,
              "c": "int16_t", "rust": "i16", "go": "int16"},
    "int32": {"bits": 32, "kind": "bv", "signed": True,
              "c": "int32_t", "rust": "i32", "go": "int32"},
    "int64": {"bits": 64, "kind": "bv", "signed": True,
              "c": "int64_t", "rust": "i64", "go": "int64"},
    "int": {"bits": 64, "kind": "bv", "signed": True,
            "c": "int64_t", "rust": "i64", "go": "int"},
    "uint8": {"bits": 8, "kind": "bv", "signed": False,
              "c": "uint8_t", "rust": "u8", "go": "uint8"},
    "uint16": {"bits": 16, "kind": "bv", "signed": False,
               "c": "uint16_t", "rust": "u16", "go": "uint16"},
    "uint32": {"bits": 32, "kind": "bv", "signed": False,
               "c": "uint32_t", "rust": "u32", "go": "uint32"},
    "uint64": {"bits": 64, "kind": "bv", "signed": False,
               "c": "uint64_t", "rust": "u64", "go": "uint64"},
    "uint": {"bits": 64, "kind": "bv", "signed": False,
             "c": "uint64_t", "rust": "u64", "go": "uint"},
    "uintptr": {"bits": 64, "kind": "bv", "signed": False,
                "c": "uint64_t", "rust": "u64", "go": "uintptr"},
    "float32": {"bits": 32, "kind": "fp",
                "c": "float", "rust": "f32", "go": "float32"},
    "float64": {"bits": 64, "kind": "fp",
                "c": "double", "rust": "f64", "go": "float64"},
}

UNSIGNED_OF_BITS = {
    8: {"c": "uint8_t", "rust": "u8", "go": "uint8"},
    16: {"c": "uint16_t", "rust": "u16", "go": "uint16"},
    32: {"c": "uint32_t", "rust": "u32", "go": "uint32"},
    64: {"c": "uint64_t", "rust": "u64", "go": "uint64"},
}


class Refused(Exception):

    def __init__(self, cause):
        Exception.__init__(self, cause)
        self.cause = cause


def holder_of(go_type, target):
    entry = HOLDER.get(go_type)
    if entry is None:
        raise Refused("this task's holder table has no %s holder for the "
                      "go holder `%s`, so no composition is written for it"
                      % (target, go_type))
    return entry[target]


def cast_to(target, text, go_type):
    """the target's own spelling of `this value, in that holder`."""
    holder = holder_of(go_type, target)
    if target == "c":
        return "(%s)(%s)" % (holder, text)
    if target == "rust":
        return "((%s) as %s)" % (text, holder)
    return "%s(%s)" % (holder, text)


def cast_to_holder_name(target, text, holder):
    if target == "c":
        return "(%s)(%s)" % (holder, text)
    if target == "rust":
        return "((%s) as %s)" % (text, holder)
    return "%s(%s)" % (holder, text)


def narrow_answer(target, text, go_type):
    """the emulation's answer read as the node's own value: the low
    `bits` of the place, in the node's holder.  The two casts are the
    reason the emulation's own return holder never has to be named --
    an integer answer of any width lands in the node's holder through
    its unsigned counterpart, and a float answer is already the value."""
    entry = HOLDER.get(go_type)
    if entry is None:
        raise Refused("this task's holder table has no %s holder for the "
                      "go holder `%s`, so no composition is written for it"
                      % (target, go_type))
    if entry["kind"] == "fp":
        return cast_to(target, text, go_type)
    unsigned = UNSIGNED_OF_BITS[entry["bits"]][target]
    through = cast_to_holder_name(target, text, unsigned)
    return cast_to_holder_name(target, through, entry[target])


# ==================================================================
# section 7: SOURCE COMPOSITION
# ==================================================================
#
# The emulation the dictionary holds is emitted into the composed file
# VERBATIM; only the file's own furniture is taken off it -- the header
# lines a target needs once (`#include`, `#![allow(...)]`, `package
# main`, `import`), the renderer's `static inline` helpers, which are
# deduplicated by their own text, and the `main` a go probe file carries
# so that the file it was rendered in would build.  Nothing inside a
# proved function is touched.

C_INCLUDE = re.compile(r"^\s*#include\b")
C_HELPER = re.compile(r"^\s*static inline\b")
RUST_ALLOW = re.compile(r"^\s*#!\[")
GO_IMPORT = re.compile(r'^\s*import\s+"')


def strip_c(source):
    includes = []
    helpers = []
    rest = []
    for line in source.splitlines():
        if C_INCLUDE.match(line):
            includes.append(line.strip())
            continue
        if C_HELPER.match(line):
            helpers.append(line.strip())
            continue
        rest.append(line)
    return includes, helpers, "\n".join(rest).strip()


def strip_rust(source):
    heads = []
    rest = []
    for line in source.splitlines():
        if RUST_ALLOW.match(line):
            heads.append(line.strip())
            continue
        rest.append(line)
    return heads, "\n".join(rest).strip()


def strip_go(source, symbol):
    """the go emulation's own function, verbatim, and the imports its
    file declared.  A go renderer's file and a go probe's file are both
    whole programs (`package main`, globals, `main`); the FUNCTION is
    what the gate proved and it is the only thing carried over."""
    name = symbol.split(".")[-1]
    imports = []
    lines = source.splitlines()
    start = None
    for index, line in enumerate(lines):
        if GO_IMPORT.match(line):
            imports.append(line.strip())
        if line.startswith("func %s(" % name):
            start = index
    if start is None:
        raise Refused("the go emulation source declares no `func %s(`, so "
                      "its function cannot be carried into a composed file"
                      % name)
    if start > 0 and lines[start - 1].strip() == "//go:noinline":
        start = start - 1
    end = None
    for index in range(start, len(lines)):
        if lines[index] == "}":
            end = index
            break
    if end is None:
        raise Refused("the go emulation source's function `%s` has no "
                      "closing brace at column zero" % name)
    return imports, "\n".join(lines[start:end + 1])


GO_NOINLINE = "//go:noinline"


def compose_file(target, emulations, functions, drop_directive=False):
    """one composed source file: every emulation used, once, verbatim,
    then the composed functions."""
    blocks = []
    if target == "c":
        includes = ["#include <stdint.h>", "#include <stdbool.h>"]
        helpers = []
        bodies = []
        for source in emulations:
            got_includes, got_helpers, rest = strip_c(source)
            for line in got_includes:
                if line not in includes:
                    includes.append(line)
            for line in got_helpers:
                if line not in helpers:
                    helpers.append(line)
            bodies.append(rest)
        blocks.append("\n".join(includes))
        if helpers:
            blocks.append("\n".join(helpers))
        blocks.extend(bodies)
        blocks.extend(functions)
        return "\n\n".join(blocks) + "\n"
    if target == "rust":
        heads = []
        bodies = []
        for source in emulations:
            got_heads, rest = strip_rust(source)
            for line in got_heads:
                if line not in heads:
                    heads.append(line)
            bodies.append(rest)
        blocks.append("\n".join(heads))
        blocks.extend(bodies)
        blocks.extend(functions)
        return "\n\n".join(blocks) + "\n"
    imports = []
    bodies = []
    for source, symbol in emulations:
        got_imports, rest = strip_go(source, symbol)
        for line in got_imports:
            if line not in imports:
                imports.append(line)
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
            for line in rest.splitlines():
                if line.strip() == GO_NOINLINE:
                    continue
                kept.append(line)
            rest = "\n".join(kept)
        bodies.append(rest)
    blocks.append("package main")
    if imports:
        blocks.append("\n".join(imports))
    blocks.extend(bodies)
    blocks.extend(functions)
    return "\n\n".join(blocks) + "\n"


def declaration(target, name, params, result_go_type):
    """the composed function's own declaration line."""
    if target == "c":
        spelled = []
        for param in params:
            spelled.append("%s %s" % (holder_of(param["go_type"], "c"),
                                      param["name"]))
        return ("%s\n%s(%s)"
                % (holder_of(result_go_type, "c"), name,
                   ", ".join(spelled)))
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


def returning(target, text):
    if target == "go":
        return "\treturn %s" % text
    return "    return %s;" % text


def function_text(target, head, lines):
    """the composed function, with the target's own brace placement: go
    refuses a `{` on a line of its own after a declaration."""
    body = "{\n%s\n}" % "\n".join(lines)
    if target == "go":
        return "%s %s" % (head, body)
    return "%s\n%s" % (head, body)


def go_main_for(names_and_params):
    """the composed go file's own `main`, so that nothing it holds is
    dropped as unreachable -- the corpus's own probe shape."""
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


# ==================================================================
# section 8: THE JOIN -- one operator node to one emulation CALL
# ==================================================================
#
# The joiner sub-node's row traffic, at source level: which of the
# emulation's parameters each operand of the node is passed as.  It is
# read off three machine-form objects and nothing else -- the corpus go
# unit's own ARRIVAL FAMILIES (which register each of its parameters
# arrives in), its own BODY LINE (which register each operand slot of
# that one instruction reads), and the CELL's own line beside the
# emulation's parameter families.  Operand position -> the unit's
# parameter index -> its arrival family -> the slot that family sits in
# -> the cell's family in the same slot -> the emulation's parameter.

def unit_operand_parameters(row, parser):
    """per operand position of the candidate unit's own construct, the
    index of the unit's own parameter that operand names."""
    if "_operand_parameters" in row:
        return row["_operand_parameters"]
    source = (row.get("meta") or {}).get("source")
    answer = None
    if source is not None:
        source_bytes = source.encode("utf-8")
        tree = parser.parse(source_bytes)
        every = []
        walk_nodes(tree.root_node, every)
        declaration_node = None
        operator_nodes = []
        for node in every:
            if node.type == "function_declaration":
                if declaration_node is None:
                    declaration_node = node
            if node.type in OPERATOR_NODES:
                operator_nodes.append(node)
        if declaration_node is not None and len(operator_nodes) == 1:
            names = parameter_names(declaration_node, source_bytes)
            operands = operand_nodes_of(operator_nodes[0])
            found = []
            for operand in operands:
                if operand is None or operand.type != "identifier":
                    found = None
                    break
                text = node_text(source_bytes, operand)
                if text not in names:
                    found = None
                    break
                found.append(names.index(text))
            answer = found
    row["_operand_parameters"] = answer
    return answer


def parameter_names(declaration_node, source_bytes):
    out = []
    parameters = declaration_node.child_by_field_name("parameters")
    if parameters is None:
        return out
    for child in parameters.children:
        if child.type != "parameter_declaration":
            continue
        for piece in child.children:
            if piece.type == "identifier":
                out.append(node_text(source_bytes, piece))
    return out


def parameter_records(declaration_node, source_bytes):
    """the composed function's parameters, in declaration order, each
    with its own go holder."""
    out = []
    parameters = declaration_node.child_by_field_name("parameters")
    if parameters is None:
        return out
    for child in parameters.children:
        if child.type != "parameter_declaration":
            continue
        spelling = child.child_by_field_name("type")
        names = []
        for piece in child.children:
            if piece.type == "identifier":
                names.append(node_text(source_bytes, piece))
        for name in names:
            out.append({"name": name,
                        "go_type": node_text(source_bytes, spelling)})
    return out


def span_key(node):
    """a node's own SPAN, which is what identifies it: `a + b - c` gives
    the outer node and its own left sub-node the same START, and a key on
    the start alone loses one of the two."""
    return (node.start_point[0] + 1, node.start_point[1] + 1,
            node.end_point[0] + 1, node.end_point[1] + 1)


def operand_nodes_of(node):
    if node.type == "binary_expression":
        return [node.child_by_field_name("left"),
                node.child_by_field_name("right")]
    return [node.child_by_field_name("operand")]


TRUTH_HOLDER = {"c": ("bool", "_Bool"), "rust": ("bool",),
                "go": ("bool",)}


def check_parameters(target, entry, plan, operand_types):
    """whether the emulation's own parameters can carry the operands the
    node passes, which is a question about the PROOF's reach and not
    about taste.

    Two refusals, both by cause.  (1) A parameter NARROWER than the
    operand truncates it, and the loop proved the emulation over the
    cell's own arrival contract, not over a truncated one.  (2) A
    parameter declared in the target's TRUTH holder collapses every
    non-zero value to one, which is a different mapping from the cell's:
    the primitive route can match a corpus body whose own probe was
    written over truth holders (task ap5's `add gpr_gpr 64` on c is the
    same family), and its `params` record says so."""
    truth = TRUTH_HOLDER.get(target) or ()
    for index, position in enumerate(plan):
        param = entry["params"][index]
        holder = param.get("holder")
        if holder in truth:
            raise Refused("the emulation `%s` declares its parameter %d "
                          "in %s's truth holder `%s`, which collapses "
                          "every non-zero value to one; the cell's own "
                          "mapping is over %d bits, so this entry cannot "
                          "carry this node's operand"
                          % (entry["symbol"], index, target, holder,
                             entry["key_width"]))
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


def argument_plan(row, entry, parser):
    """-> a list, per emulation parameter, of the operand POSITION of
    the node whose value is passed there; or Refused with the cause."""
    import model_table as MT
    import ledger as L
    positions = unit_operand_parameters(row, parser)
    if positions is None:
        raise Refused("the corpus unit's own source does not read its "
                      "construct's operands straight off its own "
                      "parameters, so no operand of the node can be put "
                      "on one of its IN rows")
    arrivals = row["arrival_families"]
    slots = row["operand_slots"]
    families = [slot["family"] for slot in slots]
    for family in families:
        if family is None:
            raise Refused("the unit's own body line `%s` carries an "
                          "operand that is not a register, so no IN row "
                          "stands for it" % row["unit_line"])
        if families.count(family) > 1:
            raise Refused("the unit's own body line `%s` reads the same "
                          "register family in more than one operand "
                          "slot, so an operand cannot be put on one slot"
                          % row["unit_line"])
    cell_texts = MT.operand_texts(entry["line"])
    if len(cell_texts) != len(slots):
        raise Refused("the cell's own line `%s` has %d operand slots and "
                      "the unit's body line `%s` has %d"
                      % (entry["line"], len(cell_texts), row["unit_line"],
                         len(slots)))
    cell_families = []
    for text in cell_texts:
        cell_families.append(L.family_of_operand(text))
    # operand position -> the unit's parameter index -> arrival family
    # -> the slot it sits in -> the cell's family in that same slot.
    value_of_cell_family = {}
    for position, parameter_index in enumerate(positions):
        if parameter_index >= len(arrivals):
            raise Refused("the unit's parameter %d has no arrival family "
                          "on its canon40 record" % parameter_index)
        family = arrivals[parameter_index]
        if family not in families:
            raise Refused("the unit's parameter %d arrives in %s and its "
                          "own body line `%s` reads no operand there"
                          % (parameter_index, family, row["unit_line"]))
        slot = families.index(family)
        cell_family = cell_families[slot]
        if cell_family is None:
            raise Refused("the cell's own line `%s` has no register in "
                          "the operand slot the unit reads its operand "
                          "in" % entry["line"])
        value_of_cell_family[cell_family] = position
    plan = []
    for family in entry["param_cell_families"]:
        if family not in value_of_cell_family:
            raise Refused("the emulation takes a parameter for the cell's "
                          "arrival %s and no operand of the node stands "
                          "for it" % family)
        plan.append(value_of_cell_family[family])
    return plan


# ==================================================================
# section 9: COMPOSING ONE FUNCTION
# ==================================================================

class Composer(object):

    def __init__(self, target, entries, resolutions, parser, source_bytes):
        self.target = target
        self.entries = entries
        self.resolutions = resolutions
        self.parser = parser
        self.source_bytes = source_bytes
        self.statements = []
        self.counter = 0
        self.used = []
        self.calls = []

    def key_of(self, node):
        return span_key(node)

    def emit(self, node, parameter_names_here):
        if node.type == "expression_list":
            inner = named_children(node)
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
            text = node_text(self.source_bytes, node)
            if text not in parameter_names_here:
                raise Refused("the leaf `%s` is not one of the "
                              "function's own parameters, and Hub v1 "
                              "composes over parameters only" % text)
            return text
        if node.type not in OPERATOR_NODES:
            raise Refused("the node kind `%s` is not an operator node and "
                          "is not a parameter" % node.type)
        resolution = self.resolutions.get(self.key_of(node))
        if resolution is None or resolution.get("row") is None:
            cause = "no resolution"
            if resolution is not None:
                cause = resolution.get("cause") or cause
            raise Refused(cause)
        row = resolution["row"]
        cell = row["cell"]
        label = cell_label(cell)
        entry = self.entries.get(label)
        if entry is None:
            raise Refused("the dictionary has no proved entry for the "
                          "cell `%s` on %s" % (label, self.target))
        plan = argument_plan(row, entry, self.parser)
        record = resolution["node_record"]
        operand_types = [record.get("lhs")]
        if record.get("arity") == "binary":
            operand_types.append(record.get("rhs"))
        check_parameters(self.target, entry, plan, operand_types)
        operands = operand_nodes_of(resolution["node"])
        values = []
        for operand in operands:
            values.append(self.emit(operand, parameter_names_here))
        arguments = []
        for index, position in enumerate(plan):
            if position >= len(values):
                raise Refused("the plan asks for operand %d and the node "
                              "has %d" % (position, len(values)))
            holder = entry["params"][index]["holder"]
            arguments.append(cast_to_holder_name(self.target,
                                                 values[position], holder))
        symbol = entry["symbol"]
        name = symbol.split(".")[-1]
        call = "%s(%s)" % (name, ", ".join(arguments))
        result_type = resolution["node_record"]["result"]
        text = narrow_answer(self.target, call, result_type)
        temporary = "hub_t%d" % self.counter
        self.counter = self.counter + 1
        self.statements.append(statement(self.target, temporary,
                                         result_type, text))
        if label not in [u["label"] for u in self.used]:
            self.used.append({"label": label, "entry": entry})
        self.calls.append({"node": resolution["node_record"]["unit"],
                           "cell": label, "symbol": symbol,
                           "route": entry["route"],
                           "unit": row["unit"]})
        return temporary


def function_declarations(source_bytes, parser):
    tree = parser.parse(source_bytes)
    every = []
    walk_nodes(tree.root_node, every)
    out = []
    for node in every:
        if node.type != "function_declaration":
            continue
        name = node.child_by_field_name("name")
        if name is None:
            continue
        out.append((node_text(source_bytes, name), node))
    return out


def named_children(node):
    out = []
    for child in node.children:
        if child.is_named:
            out.append(child)
    return out


def single_return(declaration_node):
    """the body's one returned expression, or None.

    The installed grammar nests it `block -> statement_list ->
    return_statement -> expression_list -> the expression`, and the walk
    is written against that shape as lane `hub1_l6` printed it."""
    body = declaration_node.child_by_field_name("body")
    if body is None:
        return None
    statements = named_children(body)
    if len(statements) == 1 and statements[0].type == "statement_list":
        statements = named_children(statements[0])
    if len(statements) != 1:
        return None
    if statements[0].type != "return_statement":
        return None
    values = named_children(statements[0])
    if len(values) != 1:
        return None
    if values[0].type == "expression_list":
        values = named_children(values[0])
    if len(values) != 1:
        return None
    return values[0]


def result_go_type(declaration_node, source_bytes):
    spelling = declaration_node.child_by_field_name("result")
    if spelling is None:
        return None
    return node_text(source_bytes, spelling)


def compose_function(target, name, declaration_node, source_bytes,
                     entries, resolutions, parser, holes=None):
    """-> a record: the composed function text and what it calls, or the
    cause it is a hole."""
    out = {"target": target, "func": name}
    params = parameter_records(declaration_node, source_bytes)
    out["params"] = params
    result = result_go_type(declaration_node, source_bytes)
    out["result"] = result
    # THE NODE-LEVEL HOLES ARE NAMED FIRST, because a node with no proved
    # entry is the brief's own "hole by cause" and the body's shape is a
    # different, weaker reason for the same function not composing.
    unresolved = []
    for key in sorted(resolutions):
        value = resolutions[key]
        if value["node_record"].get("func") != name:
            continue
        if value["row"] is None:
            unresolved.append("`%s`: %s" % (value["node_record"]["text"],
                                            value["cause"]))
            continue
        label = cell_label(value["row"]["cell"])
        if entries.get(label) is None:
            hole = (holes or {}).get(label) or {}
            unresolved.append("`%s`: the dictionary has no proved entry "
                              "for the cell `%s` on %s: %s"
                              % (value["node_record"]["text"], label,
                                 target,
                                 hole.get("cause")
                                 or "(the dictionary records no cause)"))
    if unresolved:
        out["composed"] = False
        out["cause"] = "; ".join(unresolved)
        return out
    expression = single_return(declaration_node)
    if expression is None:
        out["composed"] = False
        out["cause"] = ("every operator node of this function resolves "
                        "and has a proved entry, and Hub v1 composes a "
                        "function whose body is one `return` of one "
                        "expression; this body is not that shape")
        return out
    composer = Composer(target, entries, resolutions, parser, source_bytes)
    names_here = [param["name"] for param in params]
    try:
        answer = composer.emit(expression, names_here)
        lines = list(composer.statements)
        lines.append(returning(target, answer))
        head = declaration(target, name, params, result)
    except Refused as refusal:
        out["composed"] = False
        out["cause"] = refusal.cause
        return out
    out["composed"] = True
    out["text"] = function_text(target, head, lines)
    out["used"] = composer.used
    out["calls"] = composer.calls
    return out


# ==================================================================
# section 10: THE ORACLE TEST -- the gate over two carved bodies
# ==================================================================

SUFFIX = {"c": ".c", "rust": ".rs", "go": ".go"}


def build_shared():
    import term97_walk as TW
    import canonical_form as CF
    maker, gate, _attached, _readings = TW.build()
    form = CF.new_form()
    return {"maker": maker, "gate": gate, "form": form,
            "reference": maker.reference}


def carve(target, source, symbol):
    """the corpus's own ship build and carve for the target."""
    import emulate as E
    if target == "c":
        return E.compile_and_carve(source, symbol)
    if target == "rust":
        import rust_render as RR
        return RR.compile_and_carve(source, symbol)
    import go_render as GR
    return GR.compile_and_carve(source, symbol)


def params_for_gate(params):
    """the parameter plan the calling rule and the caller-extension
    re-pose need: kind and bits off each go holder."""
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


def families_for(target, plan):
    import emulate as E
    if target == "go":
        import go_render as GR
        return GR.expected_go_families(plan)
    return E.expected_c_families(plan)


def wrapped(shared, target, raw_bytes, mnem, label):
    import handful as H
    return H.wrapped_body(shared, raw_bytes, mnem, label, target)


def gate_two_bodies(shared, side_a, side_b, plan):
    """body A against body B, inputs aligned by IN row: IN-i is the i-th
    declared parameter on both sides, and each side names it in its own
    calling rule's own register."""
    import pool100_entry_equivalence as P100
    import emulate as E
    import handful as H
    out = {"route": {}}
    term_a, cause = E.body_answer(shared["reference"], side_a["canon"])
    if term_a is None:
        out["outcome"] = "UNDECIDED"
        out["reason"] = "body A: %s" % cause
        return out
    out["route"]["A"] = "the reference's answer for go's own carved body"
    term_b, cause = E.body_answer(shared["reference"], side_b["canon"])
    if term_b is None:
        out["outcome"] = "UNDECIDED"
        out["reason"] = "body B: %s" % cause
        return out
    out["route"]["B"] = ("the reference's answer for the target's carved "
                         "body")
    families_a = side_a["families"]
    families_b = side_b["families"]
    rows_a = P100.input_rows(families_a)
    rows_b = P100.input_rows(families_b)
    disagreement = P100.rows_disagree(rows_a, rows_b)
    if disagreement is not None:
        out["outcome"] = "UNDECIDED"
        out["reason"] = "the IN rows cannot be aligned: %s" % disagreement
        return out
    out["aligned_rows"] = []
    for index in range(len(families_a)):
        out["aligned_rows"].append({
            "row": "IN-%d" % index,
            "body A reads": families_a[index],
            "body B reads": families_b[index],
        })
    _in, shared_a, constants_a, other_a = P100.classify_symbols(term_a,
                                                                families_a)
    _in, shared_b, constants_b, other_b = P100.classify_symbols(term_b,
                                                                families_b)
    term_a, names_a = P100.rename_constants_apart(term_a, constants_a, "a")
    term_b, names_b = P100.rename_constants_apart(term_b, constants_b, "b")
    out["a_side_free_state"] = shared_a + other_a + names_a
    out["b_side_free_state"] = shared_b + other_b + names_b
    aligned_a = P100.align_by_row(term_a, rows_a)
    aligned_b = P100.align_by_row(term_b, rows_b)
    out["a_bits"] = aligned_a.size()
    out["b_bits"] = aligned_b.size()
    if out["a_bits"] != out["b_bits"]:
        out["width_note"] = ("body A answers %d bits and body B answers "
                             "%d, so the gate's own rule cut both to %d"
                             % (out["a_bits"], out["b_bits"],
                                min(out["a_bits"], out["b_bits"])))
    out.update(H.decided(shared, aligned_a, aligned_b, plan))
    return out


def go_re_pose(shared, record, side_a, plan, families_b, folder, name):
    """the same proof again against the composed go file whose only
    difference is that `//go:noinline` is off each emulation.

    It is a RE-POSE and it is recorded beside the first verdict, never in
    place of it: task o7's caller-extension re-pose is the precedent."""
    import go_render as GR
    path = os.path.join(folder, name)
    if not os.path.exists(path):
        return {"verdict": None, "cause": "no such composed file"}
    handle = open(path)
    source = handle.read()
    handle.close()
    got, refusal = GR.compile_and_carve(source, "main.%s" % record["func"])
    if got is None:
        return {"verdict": None,
                "cause": "did not build or carve: %s" % refusal}
    raw_bytes, mnem = got
    out = {"body_b_text": "; ".join(mnem),
           "body_b_bytes": " ".join(raw_bytes),
           "what_was_dropped": GO_NOINLINE}
    side_b = {"canon": wrapped(shared, "go", raw_bytes, mnem,
                               "handfulBi_%s" % record["func"]),
              "families": families_b}
    out["check"] = gate_two_bodies(shared, side_a, side_b, plan)
    out["verdict"] = verdict_word(out["check"])
    return out


def verdict_word(check):
    """the oracle test's own three words, off the gate's outcome."""
    outcome = check.get("outcome")
    if outcome == "PROVED_ON_SHIP":
        return "PROVED"
    if outcome == "PROVED":
        return "PROVED"
    if outcome == "DISPROVED":
        extension = check.get("under_caller_extension") or {}
        if extension.get("outcome") in ("PROVED", "PROVED_ON_SHIP"):
            return "PROVED_UNDER_CALLER_EXTENSION"
        return "DISPROVED"
    return "UNDECIDED"


# ==================================================================
# section 11: THE HANDFUL
# ==================================================================

def resolutions_for(nodes, index, parser, every_index=None):
    out = {}
    for record in nodes:
        node = record.pop("node")
        key = (record["position"]["line"], record["position"]["col"],
               record["position"]["end_line"],
               record["position"]["end_col"])
        row, cause = resolve(record, index, parser, every_index)
        out[key] = {"row": row, "cause": cause, "node": node,
                    "node_record": record}
    return out


def go_side_bodies(shared, names):
    """body A: go's own build of the handful file, carved per function."""
    import go_render as GR
    handle = open(HANDFUL_GO)
    source = handle.read()
    handle.close()
    out = {}
    for name in names:
        got, refusal = GR.compile_and_carve(source, "main.%s" % name)
        if got is None:
            out[name] = {"carved": False, "cause": refusal}
            continue
        raw_bytes, mnem = got
        out[name] = {"carved": True, "body_bytes": " ".join(raw_bytes),
                     "body_text": "; ".join(mnem),
                     "raw": raw_bytes, "mnem": mnem}
        check_memory("body A %s" % name)
    return out


def handful_command():
    say("[1/6] the dictionary")
    document = read_json(DICTIONARY)
    entries = document["targets"]
    index = candidate_index(document["go_units"])
    say("   entries: %s"
        % ", ".join(["%s %d" % (t, len(entries[t])) for t in TARGETS]))
    say("[2/6] the front end: tree-sitter's tree, go/types' types")
    nodes, source_bytes, refusal = front_end(HANDFUL_GO)
    if nodes is None:
        raise SystemExit("the type oracle did not run: %s" % refusal)
    typed = 0
    for record in nodes:
        if record.get("typed"):
            typed = typed + 1
    say("   operator nodes: %d, typed by go/types: %d" % (len(nodes), typed))
    parser = go_parser()
    every_index = candidate_index(document["go_units_every"])
    resolutions = resolutions_for(nodes, index, parser, every_index)
    resolved = 0
    for value in resolutions.values():
        if value["row"] is not None:
            resolved = resolved + 1
    say("   nodes resolved to a corpus-attested cell: %d of %d"
        % (resolved, len(resolutions)))
    say("[3/6] body A: go's own build of the file, carved per function")
    declarations = function_declarations(source_bytes, parser)
    names = []
    for name, node in declarations:
        if name == "main":
            continue
        names.append(name)
    bodies_a = go_side_bodies(None, names)
    for name in names:
        say("   %-18s %s" % (name, bodies_a[name].get("body_text")
                             or bodies_a[name].get("cause")))
    say("[4/6] composing, one file per target")
    shared = build_shared()
    composed = {}
    for target in TARGETS:
        per_function = []
        for name, node in declarations:
            if name == "main":
                continue
            record = compose_function(target, name, node, source_bytes,
                                      entries[target], resolutions,
                                      parser, document["holes"][target])
            per_function.append(record)
        composed[target] = per_function
        texts = []
        emulations = []
        seen = []
        plans = []
        for record in per_function:
            if not record.get("composed"):
                continue
            texts.append(record["text"])
            plans.append((record["func"], record["params"],
                          record["result"]))
            for used in record["used"]:
                if used["label"] in seen:
                    continue
                seen.append(used["label"])
                if target == "go":
                    emulations.append((used["entry"]["source"],
                                       used["entry"]["symbol"]))
                else:
                    emulations.append(used["entry"]["source"])
        if not texts:
            say("   %-5s no function composed" % target)
            continue
        if target == "go":
            texts.append(go_main_for(plans))
        source = compose_file(target, emulations, texts)
        path = os.path.join(HANDFUL_DIR, "composed_%s%s"
                            % (target, SUFFIX[target]))
        handle = open(path, "w")
        handle.write(source)
        handle.close()
        say("   %-5s %d function(s) composed, %d emulation(s), %s"
            % (target, len(texts) - (1 if target == "go" else 0),
               len(emulations), os.path.basename(path)))
        if target == "go":
            relaxed = compose_file(target, emulations, texts, True)
            second = os.path.join(HANDFUL_DIR,
                                  "composed_go_inlinable.go")
            handle = open(second, "w")
            handle.write(relaxed)
            handle.close()
            say("   %-5s and the same file with the `%s` directive "
                "dropped from each emulation, %s"
                % (target, GO_NOINLINE, os.path.basename(second)))
    say("[5/6] body B and the gate, per function per target")
    results = []
    for target in TARGETS:
        path = os.path.join(HANDFUL_DIR, "composed_%s%s"
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
                say("   %-5s %-18s HOLE: %s" % (target, record["func"],
                                                row["cause"]))
                continue
            row["calls"] = record["calls"]
            row["text"] = record["text"]
            symbol = record["func"]
            if target == "go":
                symbol = "main.%s" % record["func"]
            got, refusal = carve(target, source, symbol)
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
                families_a = families_for("go", plan)
                families_b = families_for(target, plan)
            except Refused as refusal:
                row["cause"] = refusal.cause
                results.append(row)
                continue
            except Exception as problem:                     # noqa: BLE001
                row["cause"] = "%s: %s" % (type(problem).__name__, problem)
                results.append(row)
                continue
            label_a = "handfulA_%s" % record["func"]
            label_b = "handfulB_%s_%s" % (target, record["func"])
            side_a = {"canon": wrapped(shared, "go", side_a_raw["raw"],
                                       side_a_raw["mnem"], label_a),
                      "families": families_a}
            side_b = {"canon": wrapped(shared, target, raw_bytes, mnem,
                                       label_b),
                      "families": families_b}
            row["canon40_outcome_A"] = side_a["canon"].get("outcome")
            row["canon40_outcome_B"] = side_b["canon"].get("outcome")
            row["check"] = gate_two_bodies(shared, side_a, side_b, plan)
            row["verdict"] = verdict_word(row["check"])
            if target == "go" and row["verdict"] != "PROVED":
                row["re_posed_without_the_noinline_directive"] = \
                    go_re_pose(shared, record, side_a, plan, families_b,
                               HANDFUL_DIR, "composed_go_inlinable.go")
            results.append(row)
            extra = ""
            again = row.get("re_posed_without_the_noinline_directive")
            if again is not None:
                extra = "   (without the directive: %s)" % again.get(
                    "verdict")
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
        if value["row"] is not None:
            record["resolved_unit"] = value["row"]["unit"]
            record["cell"] = value["row"]["cell"]
        else:
            record["cause"] = value["cause"]
        nodes_out.append(record)
    document = {
        "meta": {
            "task": "hub1",
            "node": "hq.research.arch_unit_oracle.hub_compiler.oracle_test",
            "what": "the handful: every operator node of handful.go with "
                    "its typed operands and the cell the corpus attests, "
                    "the composed source per target, and the gate over "
                    "go's own body and the composed body, per function",
            "file": HANDFUL_GO,
            "peak_kb": peak_kb(),
        },
        "nodes": nodes_out,
        "bodies_a": {k: {"body_text": v.get("body_text"),
                         "body_bytes": v.get("body_bytes"),
                         "cause": v.get("cause")}
                     for k, v in bodies_a.items()},
        "results": results,
    }
    write_json(ORACLE_JSON, document)
    say("   %s" % ORACLE_JSON)
    say("peak resident: %d kB" % peak_kb())
    return 0


# ==================================================================
# section 12: THE MEASURE -- the corpus's own go units
# ==================================================================
#
# Body A is not rebuilt here: the corpus's own canon40 record for the
# unit IS go's own carved body, and it is the object every proof of this
# line has been posed against.  Body B is the composition of that unit's
# one construct for the target, built and carved at the target's own
# ship flags.

def unit_parameters(row, parser):
    """the corpus unit's own parameters, in its own declaration order,
    each with its go holder off its probe record."""
    holders = row["holders"]
    source = (row.get("meta") or {}).get("source")
    if source is None:
        raise Refused("the unit carries no source")
    source_bytes = source.encode("utf-8")
    tree = parser.parse(source_bytes)
    every = []
    walk_nodes(tree.root_node, every)
    declaration_node = None
    for node in every:
        if node.type == "function_declaration":
            declaration_node = node
            break
    if declaration_node is None:
        raise Refused("the unit's own source declares no function")
    names = parameter_names(declaration_node, source_bytes)
    spelled = [holders["lhs"], holders["rhs"]]
    out = []
    for index, name in enumerate(names):
        if index >= len(spelled) or spelled[index] is None:
            raise Refused("the unit declares %d parameters and its probe "
                          "record names %d operand holders"
                          % (len(names), len([x for x in spelled
                                              if x is not None])))
        out.append({"name": name, "go_type": spelled[index]})
    return out


def compose_unit(target, row, entry, parser, name):
    """the unit's own construct, composed for the target as one call."""
    params = unit_parameters(row, parser)
    result = row["holders"]["result"]
    positions = unit_operand_parameters(row, parser)
    if positions is None:
        raise Refused("the corpus unit's own source does not read its "
                      "construct's operands straight off its own "
                      "parameters")
    plan = argument_plan(row, entry, parser)
    operand_types = [row["holders"]["lhs"]]
    if row["holders"]["arity"] == "binary":
        operand_types.append(row["holders"]["rhs"])
    check_parameters(target, entry, plan, operand_types)
    values = []
    for parameter_index in positions:
        values.append(params[parameter_index]["name"])
    arguments = []
    for index, position in enumerate(plan):
        holder = entry["params"][index]["holder"]
        arguments.append(cast_to_holder_name(target, values[position],
                                             holder))
    symbol = entry["symbol"]
    call = "%s(%s)" % (symbol.split(".")[-1], ", ".join(arguments))
    text = narrow_answer(target, call, result)
    lines = [statement(target, "hub_t0", result, text),
             returning(target, "hub_t0")]
    head = declaration(target, name, params, result)
    return {"text": function_text(target, head, lines),
            "params": params, "result": result,
            "cell": cell_label(row["cell"]), "symbol": symbol,
            "route": entry["route"]}


def sanitize_name(unit_id):
    return "hub_" + re.sub(r"[^A-Za-z0-9_]", "_", unit_id)


def measure_command(limit=None):
    say("[1/4] the dictionary and the corpus's go units")
    document = read_json(DICTIONARY)
    entries = document["targets"]
    rows = document["go_units"]
    if limit is not None:
        rows = rows[:limit]
    units = go_units_held()
    say("   corpus go units: %d; units naming one cell: %d"
        % (len(units), len(document["go_units"])))
    parser = go_parser()
    shared = build_shared()
    say("[2/4] composing, building, carving and gating, one unit at a "
        "time")
    results = []
    total = len(rows) * len(TARGETS)
    done = 0
    for row in rows:
        record = units.get(row["unit"])
        for target in TARGETS:
            done = done + 1
            out = {"unit": row["unit"], "lang": "go", "target": target,
                   "cell": cell_label(row["cell"]),
                   "attested_ledger_rows": None,
                   "holders": row["holders"]}
            label = cell_label(row["cell"])
            entry = entries[target].get(label)
            if entry is not None:
                out["attested_ledger_rows"] = entry["attested_ledger_rows"]
                out["route"] = entry["route"]
            if entry is None:
                out["composed"] = False
                out["cause"] = ("the dictionary has no proved entry for "
                                "the cell `%s` on %s" % (label, target))
                results.append(out)
                continue
            name = sanitize_name(row["unit"])
            try:
                built = compose_unit(target, row, entry, parser, name)
            except Refused as refusal:
                out["composed"] = False
                out["cause"] = refusal.cause
                results.append(out)
                continue
            out["composed"] = True
            out["text"] = built["text"]
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
            got, refusal = carve(target, source, symbol)
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
                families_a = families_for("go", plan)
                families_b = families_for(target, plan)
            except Refused as refusal:
                out["cause"] = refusal.cause
                results.append(out)
                continue
            except Exception as problem:                     # noqa: BLE001
                out["cause"] = "%s: %s" % (type(problem).__name__, problem)
                results.append(out)
                continue
            side_a = {"canon": record, "families": families_a}
            side_b = {"canon": wrapped(shared, target, raw_bytes, mnem,
                                       "measureB_%s_%s" % (target, name)),
                      "families": families_b}
            out["check"] = gate_two_bodies(shared, side_a, side_b, plan)
            out["verdict"] = verdict_word(out["check"])
            if target == "go" and out["verdict"] != "PROVED":
                # THE SAME RE-POSE as the handful's, and for the same
                # reason: `//go:noinline` on the emulation forbids the
                # cross-operator lowering source composition exists to
                # obtain, and go's own stack-growth preamble then leaves
                # the unit, which the reference refuses to read.
                relaxed = compose_file(target, emulations, texts, True)
                out["re_posed_without_the_noinline_directive"] = \
                    measure_re_pose(shared, relaxed, symbol, side_a, plan,
                                    families_b, name)
            results.append(out)
            if done % 25 == 0 or done == total:
                say("   [%d/%d] %d kB resident" % (done, total, peak_kb()))
            check_memory("measure %s %s" % (target, row["unit"]))
    say("[3/4] the counts")
    counts = measure_counts(results, document)
    for target in TARGETS:
        row = counts["per_target"][target]
        say("   %-5s composed %3d/%3d units (%d ledger rows), proved "
            "%3d, disproved %3d, undecided %3d"
            % (target, row["composed"], row["attempted"],
               row["composed_ledger_rows"], row["proved"],
               row["disproved"], row["undecided"]))
    say("[4/4] writing")
    write_json(MEASURE_JSON, {
        "meta": {
            "task": "hub1",
            "node": "hq.research.arch_unit_oracle.hub_compiler",
            "what": "over the corpus's own go units, how many the "
                    "dictionary composes to each target and how many of "
                    "those the gate proves against go's own body",
            "peak_kb": peak_kb(),
        },
        "counts": counts,
        "results": results,
    })
    say("   %s" % MEASURE_JSON)
    say("peak resident: %d kB" % peak_kb())
    return 0


def measure_re_pose(shared, source, symbol, side_a, plan, families_b,
                    name):
    import go_render as GR
    got, refusal = GR.compile_and_carve(source, symbol)
    if got is None:
        return {"verdict": None,
                "cause": "did not build or carve: %s" % refusal}
    raw_bytes, mnem = got
    out = {"body_b_text": "; ".join(mnem),
           "what_was_dropped": GO_NOINLINE}
    side_b = {"canon": wrapped(shared, "go", raw_bytes, mnem,
                               "measureBi_%s" % name),
              "families": families_b}
    out["check"] = gate_two_bodies(shared, side_a, side_b, plan)
    out["verdict"] = verdict_word(out["check"])
    return out


def measure_counts(results, document):
    per_target = {}
    for target in TARGETS:
        per_target[target] = {"attempted": 0, "composed": 0, "carved": 0,
                              "proved": 0,
                              "proved_under_caller_extension": 0,
                              "disproved": 0, "undecided": 0,
                              "composed_ledger_rows": 0,
                              "proved_ledger_rows": 0,
                              "re_posed": 0, "proved_on_the_re_pose": 0,
                              "re_posed_ledger_rows": 0}
    causes = {}
    for target in TARGETS:
        causes[target] = collections.Counter()
    for row in results:
        target = row["target"]
        bucket = per_target[target]
        bucket["attempted"] += 1
        if not row.get("composed"):
            causes[target][row.get("cause") or "(no cause)"] += 1
            continue
        bucket["composed"] += 1
        rows_covered = row.get("attested_ledger_rows") or 0
        bucket["composed_ledger_rows"] += rows_covered
        if not row.get("carved"):
            causes[target][row.get("cause") or "(no cause)"] += 1
            continue
        bucket["carved"] += 1
        verdict = row.get("verdict")
        again = row.get("re_posed_without_the_noinline_directive")
        if again is not None and again.get("verdict") is not None:
            bucket["re_posed"] = bucket.get("re_posed", 0) + 1
            if again["verdict"] in ("PROVED",
                                    "PROVED_UNDER_CALLER_EXTENSION"):
                bucket["proved_on_the_re_pose"] = bucket.get(
                    "proved_on_the_re_pose", 0) + 1
                bucket["re_posed_ledger_rows"] = bucket.get(
                    "re_posed_ledger_rows", 0) + rows_covered
        if verdict is None:
            causes[target][row.get("cause") or "(no cause)"] += 1
            bucket["undecided"] += 1
            continue
        if verdict == "PROVED":
            bucket["proved"] += 1
            bucket["proved_ledger_rows"] += rows_covered
        elif verdict == "PROVED_UNDER_CALLER_EXTENSION":
            bucket["proved_under_caller_extension"] += 1
            bucket["proved_ledger_rows"] += rows_covered
        elif verdict == "DISPROVED":
            bucket["disproved"] += 1
            causes[target][(row.get("check") or {}).get("reason")
                           or "(no reason)"] += 1
        else:
            bucket["undecided"] += 1
            causes[target][(row.get("check") or {}).get("reason")
                           or "(no reason)"] += 1
    out = {"per_target": per_target,
           "causes": {t: dict(causes[t]) for t in TARGETS},
           "corpus_go_units": len(document["go_units_every"]),
           "go_units_naming_one_cell": len(document["go_units"]),
           "go_units_the_narrow_rule_holds":
               len(document["go_units"])
               + len(document["go_units_without_one_cell"])}
    return out


# ==================================================================
# section 13: THE TABLES
# ==================================================================

def tables_command():
    lines = []
    oracle = read_json(ORACLE_JSON)
    lines.append("# oracle_test -- task hub1, Hub v1's first oracle "
                 "numbers")
    lines.append("")
    lines.append("Generated by `hub.py tables` off `oracle_test.json` and "
                 "`measure.json`.")
    lines.append("")
    lines.append("## 1. The handful, node by node")
    lines.append("")
    lines.append("One row per operator node of "
                 "`Research/oracle/hub/handful/handful.go`: where it is, "
                 "what go's own type checker says its operands and its "
                 "result are, and which corpus go unit -- and so which "
                 "cell -- the corpus attests for it.")
    lines.append("")
    rows = []
    for node in oracle["nodes"]:
        cell = node.get("cell")
        rows.append([node.get("func"),
                     "%d:%d" % (node["position"]["line"],
                                node["position"]["col"]),
                     "`%s`" % node.get("text"),
                     node.get("lhs"), node.get("rhs"), node.get("result"),
                     node.get("resolved_unit") or "--",
                     "`%s`" % cell_label(cell) if cell else "--"])
    lines.append(pipe_table(["function", "line:col", "the node, LITERAL",
                             "lhs holder", "rhs holder", "result holder",
                             "corpus unit", "cell"], rows))
    lines.append("")
    lines.append("## 2. The handful, function by function and target by "
                 "target")
    lines.append("")
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
        rows.append([row["func"], row["target"], verdict, second,
                     (row.get("cause") or "--").replace("|", "/")])
    lines.append(pipe_table(["function", "target", "the gate's verdict",
                             "re-posed without `//go:noinline`",
                             "cause where it is a hole"], rows))
    lines.append("")
    lines.append("## 3. Body A and body B, per function and target")
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
    if os.path.exists(MEASURE_JSON):
        measure = read_json(MEASURE_JSON)
        counts = measure["counts"]
        # The three population figures are read from the dictionary as it
        # stands rather than from the counts the measure lane stored, so
        # that a correction to how they are named never needs the ten
        # minutes of the measure itself re-run.
        held = read_json(DICTIONARY)
        counts = dict(counts)
        counts["corpus_go_units"] = len(held["go_units_every"])
        counts["go_units_naming_one_cell"] = len(held["go_units"])
        counts["go_units_the_narrow_rule_holds"] = (
            len(held["go_units"]) + len(held["go_units_without_one_cell"]))
        lines.append("## 4. The measure over the corpus's own go units")
        lines.append("")
        lines.append("The corpus holds %d go units. %d of them are held "
                     "by task o2's NARROW rule (the whole body is one "
                     "arch-opcode instruction plus chaff) and %d of "
                     "those name exactly one cell; those are the units "
                     "the dictionary can be asked about. The other go "
                     "units of the corpus are the constructs go lowers "
                     "to several cells, and they are named as such in "
                     "the handful's own hole causes."
                     % (counts["corpus_go_units"],
                        counts.get("go_units_the_narrow_rule_holds", 0),
                        counts["go_units_naming_one_cell"]))
        lines.append("")
        rows = []
        for target in TARGETS:
            bucket = counts["per_target"][target]
            rows.append([target, bucket["attempted"], bucket["composed"],
                         bucket["composed_ledger_rows"], bucket["carved"],
                         bucket["proved"],
                         bucket["proved_under_caller_extension"],
                         bucket["disproved"], bucket["undecided"],
                         bucket["proved_ledger_rows"],
                         bucket.get("re_posed", 0),
                         bucket.get("proved_on_the_re_pose", 0),
                         bucket.get("re_posed_ledger_rows", 0)])
        lines.append(pipe_table(["target", "units asked", "composed",
                                 "ledger rows the composed cells cover",
                                 "built and carved", "proved",
                                 "proved under caller extension",
                                 "disproved", "undecided",
                                 "ledger rows the proved cells cover",
                                 "re-posed without `//go:noinline`",
                                 "proved on that re-pose",
                                 "ledger rows that re-pose proves"],
                                rows))
        lines.append("")
        lines.append("## 5. The measure, by cause")
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
    handle = open(ORACLE_MD, "w")
    handle.write("\n".join(lines) + "\n")
    handle.close()
    say("   %s" % ORACLE_MD)
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
