#!/usr/bin/env python3
"""rv_attest.py -- THE CORPUS'S ATTESTATION ON riscv64: which RISC-V cells
the probe corpus's own units actually produce, and which of them a single
instruction of a single unit IS.

Node: hq.research.arch_unit_oracle.  Task rv2, brief section 2 step 1's
attestation clause and step 4's "RISC-V's attested singletons",
`PRIVATE/PseudoCoupHQ/Research/briefs/task_rv2_brief.md`.

WHAT THIS IS, one sentence, in relation: the riscv64 twin of the x86
model table's own attestation section -- the corpus's c and go probe
sources compiled for riscv64 at the corpus's own ship flags, carved at
the function symbol, walked by the RISC-V reference, and counted per
(`mnem`, operand shape, `key_width`) cell.

THE OBJECTS, one sentence each.
  * A PROBE is one (operator, holder pair) source the corpus generated
    and a compiler accepted; its x86 body is the arch-unit the pipeline
    already holds, and its riscv64 body is what this file produces.
  * AN ATTESTED CELL is a cell some carved riscv64 body spells: the
    cell's own instruction appears as a line of that body.
  * A SINGLETON is a probe whose whole riscv64 body is ONE computing
    instruction and the return -- so the probe's own source IS the
    target language's primitive for that cell, and the loop can render
    that source instead of the cell's term.

WHY THE SINGLETONS MATTER, in one sentence: the x86 loop's primitive
lookup asks "which corpus body is exactly this cell's own opcode", and
on riscv64 that question can only be answered by compiling the corpus
for riscv64, which is what this file does.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope, anywhere
in this line -- not in matching, not in "which pairs get compared", not in
report rows, not in dropdowns.  The candidate set for comparison comes from
machine-form evidence (clusters, connections, type pairs) or from ratified
intention -- never from the token.  The token appears exactly once per
unit: as a display label on the member.  HISTORY OF VIOLATIONS, so the
pattern is visible: (1) the arch campaign's cross-language matrix (caught
by the owner 2026-08-24); (2) verdicts.py's row pairing (caught by the owner
2026-08-25 -- the fix brief itself reintroduced it as "same-operator
pairs").  MECHANICAL GUARD REQUIRED: every pipeline stage that groups or
pairs units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste this
paragraph verbatim."

HOW THIS FILE OBEYS IT.  A unit lands on a cell because a LINE OF ITS OWN
CARVED BODY spells that cell's instruction at that operand form -- machine
form read off the disassembler.  The probe's source operator rides on the
row as `operator`, on a row that also carries `lang` and `unit`, which is
the guard's one allowed place for a display label, and nothing reads it.

MEMORY, as the law requires: one probe at a time, nothing accumulated but
the per-cell counts and at most three example unit ids per cell; bound
6 GB, named abort ABORT_MEMORY_RV2, peak resident printed.

Coding discipline (the owner's ruling): no complex/compound one-liner statements.

usage:
  rv_attest.py sample <op dir> <out prefix> <work dir> <n>
  rv_attest.py run    <op dir> <out prefix> <work dir> <c sample> <go sample>
"""

import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import riscv_reference as RV                                # noqa: E402
import riscv_carve as CARVE                                 # noqa: E402
import model_table_rv as MRV                                # noqa: E402


ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_RV2"


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    peak = peak_kb()
    if peak > ABORT_KB:
        raise SystemExit("%s: %d kB at %s" % (ABORT_NAME, peak, where))
    return peak


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def write_json(path, document):
    fh = open(path, "w")
    json.dump(document, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()


# ==================================================================
# section 1: the operand classes, so a body line lands on a cell
# ==================================================================

def operand_class(text, first_text):
    """the class of one operand of a carved line, by the reference's own
    readers and nothing else."""
    reader = RV.Operands(None, "", [text])
    if reader.is_memory(text):
        return "mem"
    if reader.is_integer_register(text):
        if first_text is not None and text == first_text:
            return "same"
        return "gpr"
    if reader.is_float_register(text):
        return "fpr"
    if reader.is_immediate(text):
        return "imm"
    return None


def shape_of(texts):
    """the operand shape of one carved line, in `model_table_rv.SHAPES`'
    own spelling, or nothing when a slot is unclassifiable."""
    if not texts:
        return "none"
    classes = []
    for index, text in enumerate(texts):
        first = None
        if index == 2:
            first = texts[1]
        got = operand_class(text, first)
        if got is None:
            return None
        classes.append(got)
    shape = "_".join(classes)
    if shape in SHAPE_NAMES:
        return shape
    return None


SHAPE_NAMES = {}
for _name, _texts in MRV.SHAPES:
    SHAPE_NAMES[_name] = True


# ==================================================================
# section 2: one probe -- compile, carve, walk
# ==================================================================

RETURN_LINES = RV.RETURN_LINES


def walk(reference, body, lang, kinds):
    """the term the carved body leaves in its answer place, under the
    psABI's arrival contract, or the refusal."""
    contract = []
    integers = 0
    floats = 0
    for kind in kinds:
        if kind == "float":
            contract.append(("fa%d" % floats, None))
            floats = floats + 1
            continue
        contract.append(("a%d" % integers, None))
        integers = integers + 1
    home = "a0"
    if kinds and kinds[0] == "float":
        home = "fa0"
    state = reference.simulate(body, None, {})
    return reference.answer_of(state, home)


FLOAT_TYPES = frozenset(["float", "double", "float32", "float64",
                         "long double"])


def kind_of(type_name):
    if type_name is None:
        return None
    if type_name in FLOAT_TYPES:
        return "float"
    return "integer"


def one_probe(reference, lang, number, probe, work_root,
              x86_has_a_body):
    """(the record for this probe) -- compiled, carved and walked."""
    row = {
        "lang": lang,
        "unit": "%s/op_%s" % (lang, number),
        "operator": probe.get("operator"),
        "expression": probe.get("expression"),
        "lhs_type": probe.get("lhs_type"),
        "rhs_type": probe.get("rhs_type"),
        "symbol": probe["symbol"],
        "x86_ship_body_in_the_store": x86_has_a_body,
        "probe_source": probe["source"],
    }
    carve_row = {
        "unit": row["unit"],
        "lang": lang,
        "source": probe["source"],
        "symbol": probe["symbol"],
        "symbol_exact": probe.get("symbol_exact", True),
    }
    got = CARVE.carve_one(carve_row, work_root)
    row["outcome"] = got["outcome"]
    if got["outcome"] != "CARVED":
        row["diagnostic"] = (got.get("diagnostic") or "")[:300]
        return row
    row["body"] = got["body"]
    row["instruction_count"] = got["instruction_count"]
    kinds = []
    for name in (probe.get("lhs_type"), probe.get("rhs_type")):
        kind = kind_of(name)
        if kind is not None:
            kinds.append(kind)
    try:
        term = walk(reference, got["body"], lang, kinds)
        row["outcome"] = "LIFTED"
        row["answer_bits"] = term.size()
    except Exception as problem:
        row["outcome"] = "WALK_REFUSED"
        row["cause"] = "%s: %s" % (type(problem).__name__, problem)
    return row


# ==================================================================
# section 3: the cells a carved body spells
# ==================================================================

def cells_of(body):
    """[(mnem, shape, key_width)] for the computing lines of one carved
    body, with the compressed spellings expanded first: a compressed
    form is a spelling and the table is keyed by the machine form."""
    out = []
    for line in body:
        if line in RETURN_LINES:
            continue
        stripped = line.strip()
        parts = stripped.split(None, 1)
        if not parts:
            continue
        mnem = parts[0]
        texts = []
        if len(parts) > 1:
            texts = RV.split_operands(parts[1])
        expansion = RV.expand_compressed(mnem, texts)
        if expansion is not None:
            mnem, texts = expansion
        shape = shape_of(texts)
        if shape is None:
            out.append((mnem, None, None))
            continue
        out.append((mnem, shape, MRV.key_width(mnem)))
    return out


THE_RETURN = "the return"


def computing_lines(body):
    out = []
    for line in body:
        if line in RETURN_LINES:
            continue
        out.append(line)
    return out


# ==================================================================
# section 4: the run
# ==================================================================

def read_manifest(op_dir, lang):
    path = os.path.join(op_dir, "probe_manifest_%s.json" % lang)
    return json.load(open(path))["probes"]


def read_units(op_dir, lang):
    path = os.path.join(op_dir, "op_units_%s.json" % lang)
    return json.load(open(path))["probes"]


def numbers_for(op_dir, lang, wanted):
    """the probe numbers this run walks, in numeric order, the first
    `wanted` of them.

    THE POPULATION IS THE PROBE MANIFEST, and it is stated rather than
    assumed: a probe is a SOURCE the corpus generated and the compiler
    accepted, and a source is all this file needs to aim the same
    compiler at riscv64.  The second number reported beside it is how
    many of those probes the x86 unit store holds a ship body for --
    smaller for go, and named in the log as a flag rather than papered
    over."""
    manifest = read_manifest(op_dir, lang)
    units = read_units(op_dir, lang)
    have = []
    with_a_ship_body = 0
    for number in manifest:
        have.append(number)
        record = units.get(number) or {}
        if (record.get("ship") or {}).get("mnem"):
            with_a_ship_body = with_a_ship_body + 1
    have.sort(key=int)
    if wanted is None or wanted >= len(have):
        return have, len(have), with_a_ship_body
    return have[:wanted], len(have), with_a_ship_body


def run_command(op_dir, prefix, work_root, c_sample, go_sample):
    reference = RV.RiscvReference()
    if not os.path.isdir(work_root):
        os.makedirs(work_root)
    rows = []
    cells = {}
    singletons = {}
    counts = {}
    plan = [("c", c_sample), ("go", go_sample)]
    started = time.time()
    for lang, wanted in plan:
        manifest = read_manifest(op_dir, lang)
        units = read_units(op_dir, lang)
        numbers, population, with_ship = numbers_for(op_dir, lang,
                                                     wanted)
        counts[lang] = {"probes_in_the_manifest": population,
                        "probes_the_x86_store_holds_a_ship_body_for":
                            with_ship,
                        "attempted": len(numbers)}
        total = len(numbers)
        for index, number in enumerate(numbers, 1):
            probe = manifest.get(number)
            if probe is None:
                continue
            has_body = False
            record = units.get(number) or {}
            if (record.get("ship") or {}).get("mnem"):
                has_body = True
            row = one_probe(reference, lang, number, probe, work_root,
                            has_body)
            rows.append(row)
            hold(cells, singletons, row)
            if index % 50 == 0 or index == total:
                say("   [%d/%d] %s probes, %.0f s, peak %.0f MB"
                    % (index, total, lang, time.time() - started,
                       check_memory("%s %d" % (lang, index)) / 1024.0))
        say("   %s: %d attempted of %d probes in the manifest; the "
            "x86 unit store holds a ship body for %d of them"
            % (lang, total, population, with_ship))
    census = {}
    for row in rows:
        census[row["outcome"]] = census.get(row["outcome"], 0) + 1
    agreement = {}
    for row in rows:
        built = row["outcome"] in ("LIFTED", "WALK_REFUSED")
        key = "%s|x86_body=%s|riscv64_built=%s" % (
            row["lang"], row["x86_ship_body_in_the_store"], built)
        agreement[key] = agreement.get(key, 0) + 1
    say("   the two builds' agreement, per language:")
    for key in sorted(agreement):
        say("      %-40s %d" % (key, agreement[key]))
    for lang in counts:
        counts[lang]["carved_or_lifted"] = 0
    for row in rows:
        if row["outcome"] in ("LIFTED", "WALK_REFUSED"):
            counts[row["lang"]]["carved_or_lifted"] += 1
    document = {
        "meta": {
            "task": "rv2",
            "what": "the corpus's c and go probe sources compiled for "
                    "riscv64 at the corpus's own ship flags, carved at "
                    "the function symbol, walked by the RISC-V "
                    "reference, and counted per cell",
            "compile_c": "clang " + " ".join(CARVE.SHIP["c"]) + " -c",
            "compile_go": "GOARCH=riscv64 GOOS=linux go build",
            "disassembler": "llvm-objdump -dr -M no-aliases --mattr="
                            + CARVE.MATTR,
            "census": census,
            "counts": counts,
            "the_two_builds_agree": agreement,
            "agreement_note": "a probe the x86 build refused is a probe "
                              "the corpus's COMPILE-OR-REFUSE gate "
                              "already recorded as refused; this "
                              "cross-tab says whether the riscv64 build "
                              "refuses exactly the same probes",
            "peak_kb": peak_kb(),
            "memory_bound_kb": ABORT_KB,
            "memory_abort": ABORT_NAME,
            "seconds": round(time.time() - started, 1),
        },
        "cells": cell_records(cells),
        "singletons": singleton_records(singletons),
        "rows": rows,
    }
    write_json(prefix + ".json", document)
    say("outcomes: %s" % json.dumps(census, sort_keys=True))
    say("attested cells: %d ; singleton cells: %d"
        % (len(cells), len(singletons)))
    say("peak RSS: %d kB" % peak_kb())
    return 0


def hold(cells, singletons, row):
    """the per-cell counts, streamed: nothing but counts and at most
    three example unit ids is kept."""
    if row["outcome"] not in ("LIFTED", "WALK_REFUSED"):
        return
    body = row.get("body") or []
    seen_here = {}
    for key in cells_of(body):
        if key[1] is None:
            continue
        entry = cells.get(key)
        if entry is None:
            entry = {"units": 0, "lines": 0, "examples": []}
            cells[key] = entry
        entry["lines"] = entry["lines"] + 1
        if key not in seen_here:
            seen_here[key] = True
            entry["units"] = entry["units"] + 1
            if len(entry["examples"]) < 3:
                entry["examples"].append(row["unit"])
    lines = computing_lines(body)
    if len(lines) != 1:
        return
    keys = cells_of(body)
    if len(keys) != 1:
        return
    key = keys[0]
    if key[1] is None:
        return
    if key in singletons:
        return
    singletons[key] = {
        "unit": row["unit"],
        "lang": row["lang"],
        "source": row.get("probe_source"),
        "operator": row.get("operator"),
        "expression": row.get("expression"),
        "lhs_type": row.get("lhs_type"),
        "rhs_type": row.get("rhs_type"),
        "line": lines[0],
    }


def cell_records(cells):
    out = []
    for key in sorted(cells):
        entry = cells[key]
        out.append({
            "mnem": key[0],
            "shape": key[1],
            "key_width": key[2],
            "units": entry["units"],
            "lines": entry["lines"],
            "example_units": list(entry["examples"]),
        })
    return out


def singleton_records(singletons):
    out = []
    for key in sorted(singletons):
        entry = dict(singletons[key])
        entry["mnem"] = key[0]
        entry["shape"] = key[1]
        entry["key_width"] = key[2]
        out.append(entry)
    return out


def sample_command(op_dir, prefix, work_root, wanted):
    """the memory sample the law asks for: `wanted` probes per language,
    with the peak resident printed."""
    return run_command(op_dir, prefix, work_root, wanted, wanted)


def main():
    command = sys.argv[1]
    if command == "sample":
        return sample_command(sys.argv[2], sys.argv[3], sys.argv[4],
                              int(sys.argv[5]))
    if command == "run":
        c_sample = None
        go_sample = None
        if sys.argv[5] != "all":
            c_sample = int(sys.argv[5])
        if sys.argv[6] != "all":
            go_sample = int(sys.argv[6])
        return run_command(sys.argv[2], sys.argv[3], sys.argv[4],
                           c_sample, go_sample)
    raise SystemExit("unknown command %r" % command)


if __name__ == "__main__":
    sys.exit(main())
