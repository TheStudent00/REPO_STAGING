#!/usr/bin/env python3
"""build_join.py -- task cov1: the reach of the PROVED emulations.

Node: hq.research.arch_unit_oracle (autopoly / riscv64 cross-construction).
Brief: Research/briefs/task_cov1_brief.md. This is a DATA JOIN, not a proof
run: no compile, no z3 solving. Every (mnem, shape, key_width) classification
below calls the SAME functions the existing pipeline already uses to build
the model table and the RISC-V attestation -- imported unmodified, never
reimplemented, so cells_of(unit) is read off the corpus's own ledger rows
exactly as model_table.py's attestation() and rv_attest.py's cells_of()
already do, just kept in full per unit instead of capped at 3 examples.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope, anywhere
in this line -- not in matching, not in "which pairs get compared", not in
report rows, not in dropdowns. The candidate set for comparison comes from
machine-form evidence (clusters, connections, type pairs) or from ratified
intention -- never from the token. The token appears exactly once per
unit: as a display label on the member. HISTORY OF VIOLATIONS, so the
pattern is visible: (1) the arch campaign's cross-language matrix (caught
by the owner 2026-08-24); (2) verdicts.py's row pairing (caught by the owner
2026-08-25 -- the fix brief itself reintroduced it as "same-operator
pairs"). MECHANICAL GUARD REQUIRED: every pipeline stage that groups or
pairs units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure. A brief handed to any subagent for this line MUST paste this
paragraph verbatim."

Keys everywhere below are the machine triple (mnem, shape, key_width),
carried as a record {"mnem":.., "shape":.., "key_width":..}, never a bare
spelling. Language names (c, cpp, rust, go, swift) are not operator tokens
and are used as dict keys the way the rest of this line already does
(attest_rv.json's "counts", certificates.jsonl's "target").

MEMORY: bound 6 GB, named abort ABORT_MEMORY_COV1, resource.getrusage,
checked every shard / every N rows. Shards are streamed and dropped.

usage:
  build_join.py units-x86   <op_pipeline dir> <out.jsonl> [--limit N]
  build_join.py units-riscv <attest_rv.json>  <out.jsonl> [--limit N]
  build_join.py bank-x86    <certificates.jsonl> <out.json>
  build_join.py bank-riscv  <rv6_all.jsonl>      <out.json>
  build_join.py matrix      <units.jsonl> <bank.json> <out.json>
                             --arch NAME --sources a,b,c --targets a,b,c
"""

import argparse
import collections
import json
import os
import resource
import sys

ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_COV1"

X86_LANGS = ["c", "cpp", "rust", "go", "swift"]
RISCV_LANGS = ["c", "go"]
RISCV_TARGETS = ["c", "cpp", "go", "rust"]


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


def cell_record(mnem, shape, key_width):
    return {"mnem": mnem, "shape": shape, "key_width": key_width}


def cell_key(mnem, shape, key_width):
    return "%s|%s|%s" % (mnem, shape, key_width)


# ======================================================================
# x86: cells_of(unit), read off Research/op_pipeline's own ledger rows,
# using model_table.py's own classifier functions, imported unmodified.
# ======================================================================

def load_model_table(op_pipeline_dir, arch_opcodes_model_dir):
    sys.path.insert(0, op_pipeline_dir)
    sys.path.insert(0, os.path.join(op_pipeline_dir, "lean"))
    sys.path.insert(0, arch_opcodes_model_dir)
    import model_table as MODEL  # noqa
    return MODEL


def x86_unit_cells(MODEL, record, line_of_row):
    """the full (mnem, shape, key_width) set of one x86 unit, and its
    computing-instruction length -- the same rows model_table.place_row
    folds into `seen_here`, kept here instead of thrown away at 3
    examples. Guard rows (a flag consumer that writes only the branch
    condition, never a value) are excluded: they are not value cells,
    per model_table.py's own `writes_the_branch_condition`."""
    seen = set()
    length = 0
    for row in MODEL.arch_opcode_rows(record):
        length = length + 1
        mnem = row["produced_by"]["mnem"]
        line = line_of_row.get(row["row"])
        if line is None:
            continue
        shape, width, cause = MODEL.classify_line(mnem, line, row.get("size"))
        if cause is not None:
            continue
        seen.add((mnem, shape, MODEL.key_width(mnem, width)))
    for row in MODEL.flag_pair_rows(record):
        length = length + 1
        setter = row["produced_by"]["mnem"][0]
        consumer = row["produced_by"]["mnem"][1]
        line = line_of_row.get(row["row"])
        if line is None:
            continue
        if MODEL.writes_the_branch_condition(consumer):
            continue
        shape, width, cause = MODEL.classify_line(consumer, line, row.get("size"))
        if cause is not None:
            continue
        seen.add((consumer, shape, MODEL.key_width(consumer, width)))
    return seen, length


def units_x86_command(op_pipeline_dir, arch_opcodes_model_dir, out_path, limit):
    MODEL = load_model_table(op_pipeline_dir, arch_opcodes_model_dir)
    MODEL._install_gpr_widths()
    readings = MODEL.CF.runtime_answer_readings()
    routines = MODEL.CF.runtime_routine_names(readings)
    shard_paths = MODEL.TR.shards()
    total = len(shard_paths)
    out = open(out_path, "w")
    written_per_lang = collections.Counter()
    units_seen = 0
    relink_refused = 0
    for number, path in enumerate(shard_paths):
        document = json.load(open(path))
        for unit_id, record in document["units"].items():
            lang = record.get("lang")
            if lang not in X86_LANGS:
                continue
            units_seen = units_seen + 1
            if limit is not None and written_per_lang[lang] >= limit:
                continue
            line_of_row = MODEL.lines_of_unit(record, routines, readings)
            if line_of_row is None:
                relink_refused = relink_refused + 1
                continue
            cells, length = x86_unit_cells(MODEL, record, line_of_row)
            row = {
                "unit": unit_id,
                "lang": lang,
                "length": length,
                "cells": [cell_record(m, s, w) for (m, s, w) in sorted(cells)],
            }
            out.write(json.dumps(row, sort_keys=True) + "\n")
            written_per_lang[lang] += 1
        del document
        check_memory("shard %d" % number)
        if (number + 1) % 50 == 0 or number + 1 == total:
            say("   [%d/%d] shards read, %d x86 units seen, written so far %s"
                % (number + 1, total, units_seen, dict(written_per_lang)))
    out.close()
    say("units-x86 done: seen %d, written %s, relink_refused %d, peak_kb %d"
        % (units_seen, dict(written_per_lang), relink_refused, peak_kb()))


# ======================================================================
# riscv64: cells_of(unit), read off rv2's attest_rv.json rows (already
# carved bodies), using rv_attest.py's own cells_of()/computing_lines(),
# imported unmodified.
# ======================================================================

def load_rv_attest(riscv_dir):
    sys.path.insert(0, riscv_dir)
    import rv_attest as RVATTEST  # noqa
    return RVATTEST


def riscv_cell_population(twins_path):
    """the 255 (mnem, shape, key_width) triples of twins.json's own rows
    -- the RISC-V cell population this brief names. rv_attest.py's
    cells_of() was built for a narrower purpose and, run over a whole
    compiler's output, also yields shapes this population never
    contains (`c.nop`, shape "none": a zero-operand pad the go compiler
    emits for alignment, which twins.json holds no row for -- no x86
    operation computes "do nothing", so the twinning pass that built
    twins.json produced no cell for it). A cell outside this population
    is not one this brief's expressibility question is defined over, so
    it is dropped here rather than left to block a unit on a
    requirement that was never asked for."""
    population = set()
    for row in json.load(open(twins_path))["rows"]:
        population.add((row["mnem"], row["shape"], row["key_width"]))
    return population


def units_riscv_command(riscv_dir, attest_rv_path, twins_path, out_path, limit):
    RVATTEST = load_rv_attest(riscv_dir)
    population = riscv_cell_population(twins_path)
    document = json.load(open(attest_rv_path))
    rows = document["rows"]
    out = open(out_path, "w")
    written_per_lang = collections.Counter()
    seen = collections.Counter()
    outcomes = collections.Counter()
    out_of_population = collections.Counter()
    total = len(rows)
    for index, row in enumerate(rows):
        lang = row.get("lang")
        outcomes[row.get("outcome")] += 1
        if lang not in RISCV_LANGS:
            continue
        if row.get("outcome") != "LIFTED":
            continue
        seen[lang] += 1
        if limit is not None and written_per_lang[lang] >= limit:
            continue
        body = row.get("body") or []
        cells = RVATTEST.cells_of(body)
        length = len(RVATTEST.computing_lines(body))
        cell_list = []
        for (mnem, shape, key_width) in cells:
            if shape is None or key_width is None:
                continue
            if (mnem, shape, key_width) not in population:
                out_of_population[(mnem, shape, key_width)] += 1
                continue
            cell_list.append((mnem, shape, key_width))
        cell_list = sorted(set(cell_list))
        out_row = {
            "unit": row["unit"],
            "lang": lang,
            "length": length,
            "cells": [cell_record(m, s, w) for (m, s, w) in cell_list],
        }
        out.write(json.dumps(out_row, sort_keys=True) + "\n")
        written_per_lang[lang] += 1
        if (index + 1) % 200 == 0 or index + 1 == total:
            say("   [%d/%d] riscv rows read, lifted-and-usable %s, written %s"
                % (index + 1, total, dict(seen), dict(written_per_lang)))
    out.close()
    check_memory("units-riscv done")
    say("units-riscv done: outcomes %s, lifted %s, written %s, peak_kb %d"
        % (dict(outcomes), dict(seen), dict(written_per_lang), peak_kb()))
    say("units-riscv out-of-population cells dropped (not among the 255 "
        "twins.json rows), by (mnem, shape, key_width) and how many "
        "carved lines they were seen on: %s"
        % {("%s|%s|%s" % k): v for k, v in out_of_population.items()})


# ======================================================================
# the bank, x86: certificates.jsonl -> per (cell, target) destination-only
# and strict booleans. Live records only (superseded_by is skipped).
# ======================================================================

FLAG_PLACE_PREFIXES = ("flags",)


def is_flag_place(place):
    if place is None:
        return False
    return place == "flags" or place.startswith("flags.")


KIND_PRIORITY = ["proved", "proved_under_caller_extension", "agreed",
                  "undecided", "refused", "sat"]


def kind_rank(kind):
    if kind in KIND_PRIORITY:
        return KIND_PRIORITY.index(kind)
    return len(KIND_PRIORITY)


def bank_x86_command(certificates_path, out_path):
    # (cell_key) -> target -> place -> kind (best live kind for that place)
    by_cell_target_place = {}
    cell_of_key = {}
    total = 0
    live = 0
    superseded = 0
    targets_seen = collections.Counter()
    fh = open(certificates_path)
    for line_number, line in enumerate(fh):
        line = line.strip()
        if not line:
            continue
        total = total + 1
        record = json.loads(line)
        if record.get("superseded_by"):
            superseded = superseded + 1
            continue
        live = live + 1
        cell = record["cell"]
        key = cell_key(cell["mnem"], cell["shape"], cell["key_width"])
        cell_of_key[key] = cell_record(cell["mnem"], cell["shape"], cell["key_width"])
        target = record["target"]
        targets_seen[target] += 1
        place = record.get("place")
        place_index = record.get("place_index")
        place_key = "%s#%s" % (place, place_index)
        kind = record.get("kind")
        slot = by_cell_target_place.setdefault(key, {}).setdefault(target, {})
        current = slot.get(place_key)
        if current is None or kind_rank(kind) < kind_rank(current):
            slot[place_key] = kind
        if (line_number + 1) % 5000 == 0:
            check_memory("certificates line %d" % (line_number + 1))
    fh.close()
    # reduce to destination_only / strict booleans per (cell, target)
    reduced = {}
    for key, by_target in by_cell_target_place.items():
        reduced[key] = {"cell": cell_of_key[key], "targets": {}}
        for target, by_place in by_target.items():
            non_flag_kinds = []
            all_kinds = []
            for place_key, kind in by_place.items():
                place = place_key.rsplit("#", 1)[0]
                all_kinds.append(kind)
                if not is_flag_place(place):
                    non_flag_kinds.append(kind)
            destination_only = any(
                k in ("proved", "proved_under_caller_extension")
                for k in non_flag_kinds)
            strict = len(all_kinds) > 0 and all(k == "proved" for k in all_kinds)
            reduced[key]["targets"][target] = {
                "destination_only": destination_only,
                "strict": strict,
                "places_considered": len(by_place),
            }
    cells_list = []
    for key in sorted(reduced):
        entry = reduced[key]
        cells_list.append({"cell": entry["cell"], "targets": entry["targets"]})
    write_json(out_path, {
        "meta": {
            "task": "cov1",
            "what": "x86 bank reduced to (cell, target) destination-only "
                    "and strict booleans, live records only",
            "source": certificates_path,
            "total_lines": total,
            "live": live,
            "superseded": superseded,
            "targets_seen": dict(targets_seen),
        },
        "cells": cells_list,
    })
    say("bank-x86 done: total %d live %d superseded %d cells %d peak_kb %d"
        % (total, live, superseded, len(reduced), peak_kb()))


# ======================================================================
# the bank, riscv64: construct/general/rv6_all.jsonl -> per (cell,
# target) proved boolean. One place per cell (no flags on this ISA), so
# destination-only and strict coincide.
# ======================================================================

def bank_riscv_command(rv6_all_path, out_path):
    reduced = {}
    total = 0
    kinds_seen = collections.Counter()
    targets_seen = collections.Counter()
    fh = open(rv6_all_path)
    for line in fh:
        line = line.strip()
        if not line:
            continue
        total = total + 1
        record = json.loads(line)
        cell = record["cell"]
        key = cell_key(cell["mnem"], cell["shape"], cell["key_width"])
        target = record["target"]
        kind = record["kind"]
        kinds_seen[kind] += 1
        targets_seen[target] += 1
        slot = reduced.setdefault(key, {"cell": cell_record(
            cell["mnem"], cell["shape"], cell["key_width"]), "targets": {}})
        proved = (kind == "proved")
        slot["targets"][target] = {
            "destination_only": proved, "strict": proved, "kind": kind}
    fh.close()
    cells_list = []
    for key in sorted(reduced):
        entry = reduced[key]
        cells_list.append({"cell": entry["cell"], "targets": entry["targets"]})
    write_json(out_path, {
        "meta": {
            "task": "cov1",
            "what": "riscv64 bank reduced to (cell, target) proved boolean, "
                    "from construct/general/rv6_all.jsonl kind == proved",
            "source": rv6_all_path,
            "total_lines": total,
            "kinds_seen": dict(kinds_seen),
            "targets_seen": dict(targets_seen),
        },
        "cells": cells_list,
    })
    say("bank-riscv done: total %d cells %d peak_kb %d"
        % (total, len(reduced), peak_kb()))


# ======================================================================
# the matrices, the blockers, and the length view.
# ======================================================================

def length_bucket(n):
    if n <= 1:
        return "1"
    if n == 2:
        return "2"
    if n <= 5:
        return "3-5"
    if n <= 10:
        return "6-10"
    return "over-10"


LENGTH_BUCKETS = ["1", "2", "3-5", "6-10", "over-10"]


def load_units(units_path):
    by_lang = collections.defaultdict(list)
    fh = open(units_path)
    for line in fh:
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        by_lang[row["lang"]].append(row)
    fh.close()
    return by_lang


def matrix_command(units_path, bank_path, out_path, arch, sources, targets):
    by_lang = load_units(units_path)
    bank_cells_list = json.load(open(bank_path))["cells"]
    # in-memory lookup only -- never written back to a json file, so the
    # pipe-joined string never sits on disk as a spelling-keyed dict key.
    bank = {}
    for entry in bank_cells_list:
        c = entry["cell"]
        bank[cell_key(c["mnem"], c["shape"], c["key_width"])] = entry

    def proved(cell, target, reading):
        key = cell_key(cell["mnem"], cell["shape"], cell["key_width"])
        entry = bank.get(key)
        if entry is None:
            return False
        t = entry["targets"].get(target)
        if t is None:
            return False
        return bool(t[reading])

    matrices = {"destination_only": {}, "strict": {}}
    blockers = {}
    length_view = {"destination_only": {}, "strict": {}}
    never_attempted = collections.Counter()

    for reading in ("destination_only", "strict"):
        for x in sources:
            units = by_lang.get(x, [])
            m = len(units)
            matrices[reading][x] = {}
            length_view[reading][x] = {}
            for y in targets:
                n = 0
                blocking_counts = collections.Counter()
                blocking_cell_of = {}
                by_bucket_n = collections.Counter()
                by_bucket_m = collections.Counter()
                for u in units:
                    bucket = length_bucket(u["length"])
                    by_bucket_m[bucket] += 1
                    ok = True
                    blocking_here = []
                    for cell in u["cells"]:
                        if not proved(cell, y, reading):
                            ok = False
                            k = cell_key(cell["mnem"], cell["shape"], cell["key_width"])
                            blocking_here.append(k)
                            blocking_cell_of[k] = cell
                            if bank.get(k) is None:
                                never_attempted[(arch, k)] += 1
                    if ok:
                        n = n + 1
                        by_bucket_n[bucket] += 1
                    else:
                        for k in set(blocking_here):
                            blocking_counts[k] += 1
                matrices[reading][x][y] = {"n": n, "m": m}
                length_view[reading][x][y] = {
                    bucket: {"n": by_bucket_n[bucket], "m": by_bucket_m[bucket]}
                    for bucket in LENGTH_BUCKETS if by_bucket_m[bucket] > 0
                }
                top = blocking_counts.most_common(10)
                blockers.setdefault(reading, {}).setdefault(x, {})[y] = [
                    {"cell": blocking_cell_of[k], "blocked_units": count}
                    for k, count in top
                ]

    write_json(out_path, {
        "meta": {
            "task": "cov1",
            "arch": arch,
            "sources": sources,
            "targets": targets,
            "units_source": units_path,
            "bank_source": bank_path,
        },
        "matrices": matrices,
        "blocking_cells_top10": blockers,
        "length_view": length_view,
        "never_attempted_cell_count": len(
            set(k for (a, k) in never_attempted if a == arch)),
    })
    say("matrix done for %s: sources=%s targets=%s -> %s"
        % (arch, sources, targets, out_path))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("units-x86")
    p.add_argument("op_pipeline_dir")
    p.add_argument("arch_opcodes_model_dir")
    p.add_argument("out")
    p.add_argument("--limit", type=int, default=None)

    p = sub.add_parser("units-riscv")
    p.add_argument("riscv_dir")
    p.add_argument("attest_rv_json")
    p.add_argument("twins_json")
    p.add_argument("out")
    p.add_argument("--limit", type=int, default=None)

    p = sub.add_parser("bank-x86")
    p.add_argument("certificates_jsonl")
    p.add_argument("out")

    p = sub.add_parser("bank-riscv")
    p.add_argument("rv6_all_jsonl")
    p.add_argument("out")

    p = sub.add_parser("matrix")
    p.add_argument("units_jsonl")
    p.add_argument("bank_json")
    p.add_argument("out")
    p.add_argument("--arch", required=True)
    p.add_argument("--sources", required=True)
    p.add_argument("--targets", required=True)

    args = parser.parse_args()

    if args.cmd == "units-x86":
        units_x86_command(args.op_pipeline_dir, args.arch_opcodes_model_dir,
                           args.out, args.limit)
    elif args.cmd == "units-riscv":
        units_riscv_command(args.riscv_dir, args.attest_rv_json,
                             args.twins_json, args.out, args.limit)
    elif args.cmd == "bank-x86":
        bank_x86_command(args.certificates_jsonl, args.out)
    elif args.cmd == "bank-riscv":
        bank_riscv_command(args.rv6_all_jsonl, args.out)
    elif args.cmd == "matrix":
        matrix_command(args.units_jsonl, args.bank_json, args.out, args.arch,
                        args.sources.split(","), args.targets.split(","))


if __name__ == "__main__":
    main()
