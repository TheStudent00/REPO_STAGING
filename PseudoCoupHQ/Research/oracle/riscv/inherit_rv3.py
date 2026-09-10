#!/usr/bin/env python3
"""inherit_rv3.py -- THE INHERITANCE RE-RUN, on the image task rv2's flags
2, 3 and 7 asked for.

Node: hq.research.arch_unit_oracle.  Task rv3, brief section 1 row 3,
`PRIVATE/PseudoCoupHQ/Research/briefs/task_rv3_brief.md`.

WHAT THIS FILE IS, one sentence, in relation: task rv2's `inherit.py`
called unchanged for everything it already decided, with ONLY the four
compile routes replaced -- because the three refusals rv2 recorded
(`rust` for want of a standard library, `c` for want of `string.h`, `cpp`
never attempted) were refusals of the IMAGE and the image has since
gained what each of them wanted.

WHAT CHANGED FROM rv2's ROUTES, each with the flag it closes.
  * `c`: `--target=riscv64-linux-gnu --gcc-toolchain=/usr` instead of
    `--target=riscv64-unknown-linux-gnu -nostdlibinc`.  The image now
    carries `g++-riscv64-linux-gnu`, whose glibc headers sit at
    `/usr/riscv64-linux-gnu/include`, so `string.h` resolves and the 15
    certificates whose renderer moves bits with `memcpy` compile.  THE
    OPTIMISATION LEVEL IS THE CORPUS'S OWN AND IS NOT TOUCHED (`-O1`).
  * `cpp`: `/usr/bin/clang++ -std=c++20 -O1` with the same two target
    flags -- the corpus's own cpp ship line (`lane_gen.py`) with the
    target added and nothing else changed.  rv2 attempted none.
  * `rust`: `--target=riscv64gc-unknown-linux-gnu` instead of
    `...-none-elf`, and `--emit=obj`, which needs NO LINKER: the object
    is carved directly, so a missing riscv64 linker cannot refuse a
    source that compiled.
  * `go`: unchanged.
  * `swift`: still not attempted; the image carries no `swiftc` at all
    (lane rv3_l1 quotes the shell's own words), let alone a riscv64 one.

WHAT DID NOT CHANGE, and this matters for reading the two runs side by
side: the twins read, the bank records chosen, the alignment (an
ARGUMENT'S POSITION), the gate, the two widths reported, and the record
shape.  Every one of those is `inherit.py`'s and is called, not copied.

THE ARGUMENT SEQUENCES for `cpp` and `rust`, stated rather than implied:
both render `extern "C"` functions, so both arrive under the System V
AMD64 C sequence on x86-64 (`rdi, rsi, rdx, rcx, r8, r9`; `xmm0..`) and
the RISC-V psABI's own (`a0..a7`; `fa0..fa7`) -- the same sequences
`claim_check.py` already states for `c`.  They are added to that file's
own tables at import time here; nothing in it is rewritten.

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

HOW THIS FILE OBEYS IT.  Which certificates are attempted is decided by
`twins.json` -- a term-identity join -- and by the bank's own `kind`.
Nothing reads an operator token; every mnemonic rides on `mnem`.

MEMORY, as the law requires: the bank is STREAMED by `inherit.py` and
never held whole.  Bound 6 GB, named abort ABORT_MEMORY_RV3, peak
resident printed.

Coding discipline (the owner's ruling): no complex/compound one-liner statements.

usage:
  inherit_rv3.py census <ref dir> <op dir> <twins.json> <bank.jsonl>
                        <src root> <out prefix> <work dir> [limit]
  inherit_rv3.py run    <ref dir> <op dir> <x86 rows json> <twins.json>
                        <bank.jsonl> <src root> <out prefix> <work dir>
                        [limit]
"""

import hashlib
import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import riscv_reference as RV                                 # noqa: E402
import riscv_carve as CARVE                                  # noqa: E402
import claim_check as CC                                     # noqa: E402
import twins as TW                                           # noqa: E402
import inherit as IN                                         # noqa: E402


ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_RV3"

# the corpus's own ship optimisation levels, per `op_pipeline/lane_gen.py`,
# with the riscv64 target added and NOTHING ELSE CHANGED.
SHIP_C = ["-std=c17", "-O1", "--target=riscv64-linux-gnu",
          "--gcc-toolchain=/usr"]
SHIP_CPP = ["-std=c++20", "-O1", "--target=riscv64-linux-gnu",
            "--gcc-toolchain=/usr"]
RUST_SHIP = ["--crate-type=lib", "--emit=obj", "-C", "opt-level=1",
             "-C", "debug-assertions=off",
             "--target=riscv64gc-unknown-linux-gnu"]

CLANGXX = "/usr/bin/clang++"

COMPILED_TARGETS = ("c", "cpp", "rust", "go")
NOT_ATTEMPTED = ("swift",)

TRIPLES = {
    "c": "riscv64-linux-gnu (clang --target, --gcc-toolchain=/usr)",
    "cpp": "riscv64-linux-gnu (clang++ --target, --gcc-toolchain=/usr)",
    "rust": "riscv64gc-unknown-linux-gnu (rustc --target, --emit=obj)",
    "go": "GOARCH=riscv64 GOOS=linux",
}


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
# section 1: the four compile routes, and nothing else replaced
# ==================================================================

def compile_and_carve(source, target, work):
    """(the carved body, the compile command, the diagnostic) for one
    rendered source aimed at riscv64 at the corpus's own ship flags."""
    if not os.path.isdir(work):
        os.makedirs(work)
    name = IN.symbol_of(source)
    if name is None:
        return None, "", "no emu_ symbol found in the rendered source"
    if target == "c":
        return _clang_route(source, work, name, "unit.c", CARVE.CLANG,
                            SHIP_C)
    if target == "cpp":
        return _clang_route(source, work, name, "unit.cpp", CLANGXX,
                            SHIP_CPP)
    if target == "rust":
        path = os.path.join(work, "unit.rs")
        obj = os.path.join(work, "unit_rs.o")
        open(path, "w").write(source)
        command = ["rustc"] + RUST_SHIP + ["-o", obj, path]
        rc, out, err = CARVE.sh(command)
        if rc != 0:
            return None, " ".join(command), (err or out)
        got, err = CARVE.disassemble(obj, name, False)
        if got is None:
            return None, " ".join(command), err
        return got, " ".join(command), ""
    if target == "go":
        return IN.original_compile_and_carve(source, target, work)
    return None, "", "no riscv64 route for target %r" % target


def _clang_route(source, work, name, filename, driver, flags):
    path = os.path.join(work, filename)
    obj = os.path.join(work, filename + ".o")
    open(path, "w").write(source)
    command = [driver] + flags + ["-c", path, "-o", obj]
    rc, out, err = CARVE.sh(command)
    if rc != 0:
        return None, " ".join(command), (err or out)
    got, err = CARVE.disassemble(obj, name, True)
    if got is None:
        return None, " ".join(command), err
    return got, " ".join(command), ""


def triple_of(target):
    return TRIPLES.get(target)


def install():
    """put the four routes, the two target lists and the two argument
    sequences in place, and leave everything else of `inherit.py` alone."""
    IN.original_compile_and_carve = IN.compile_and_carve
    IN.compile_and_carve = compile_and_carve
    IN.triple_of = triple_of
    IN.NOT_ATTEMPTED = NOT_ATTEMPTED
    IN.ABORT_NAME = ABORT_NAME
    for target in ("cpp", "rust"):
        CC.X86_INTEGER[target] = list(CC.X86_INTEGER["c"])
        CC.X86_FLOAT[target] = list(CC.X86_FLOAT["c"])
        CC.RISCV_INTEGER[target] = list(CC.RISCV_INTEGER["c"])
        CC.RISCV_FLOAT[target] = list(CC.RISCV_FLOAT["c"])


# ==================================================================
# section 2: the census -- which mnemonics the four compilers write that
# the lifter has no entry for
# ==================================================================
#
# THIS IS EVIDENCE, NOT A VOCABULARY DECISION.  The x86 table's own rule
# is that no entry is invented for an opcode no body contains; this census
# is how the RISC-V table learns which opcodes the bodies DO contain, so
# the reference gains exactly those and no more.

def census_command(ref_dir, op_dir, twins_path, bank_path, src_root,
                   prefix, work_root, limit):
    say("[0/4] the reference's own opcode table")
    table = RV.OpcodeTable()
    say("   %d mnemonics have an entry" % len(table.entries))

    say("[1/4] the twinned x86 cells")
    wanted = IN.twinned_cells(twins_path)
    say("   %d (x86 cell, place) pairs a RISC-V cell twins" % len(wanted))

    say("[2/4] the bank, streamed")
    records = IN.bank_lines(bank_path, wanted)
    attempted = []
    for record in records:
        if record["target"] in COMPILED_TARGETS:
            attempted.append(record)
    say("   %d certificates on those pairs, %d on a compiled target"
        % (len(records), len(attempted)))
    check_memory("after the bank")

    say("[3/4] compile, carve, and read every mnemonic")
    rows = []
    unknown = {}
    per_target = {}
    started = time.time()
    total = len(attempted)
    if limit is not None:
        total = min(total, limit)
    for number, record in enumerate(attempted, 1):
        if limit is not None and number > limit:
            break
        row = one_census(record, src_root, work_root, number, table,
                         unknown)
        rows.append(row)
        held = per_target.setdefault(record["target"], {})
        held[row["outcome"]] = held.get(row["outcome"], 0) + 1
        if number % 25 == 0 or number == total:
            say("   [%d/%d] sources, %.0f s, peak %.0f MB"
                % (number, total, time.time() - started,
                   check_memory("source %d" % number) / 1024.0))

    say("[4/4] writing")
    for target in sorted(per_target):
        say("   %-6s %s" % (target, json.dumps(per_target[target],
                                               sort_keys=True)))
    say("   mnemonics with no entry in the riscv opcode table:")
    for mnemonic in sorted(unknown, key=lambda m: -unknown[m]["lines"]):
        held = unknown[mnemonic]
        say("     %-14s lines %4d  sources %4d  targets %s"
            % (mnemonic, held["lines"], held["sources"],
               ",".join(sorted(held["targets"]))))
    shaped = {}
    for mnemonic in unknown:
        held = dict(unknown[mnemonic])
        held["targets"] = sorted(held["targets"])
        shaped[mnemonic] = held
    document = {
        "meta": {
            "task": "rv3",
            "what": "every certificate source on a compiled target, "
                    "built for riscv64 on the new image and carved, with "
                    "the mnemonics the lifter has no entry for tallied; "
                    "no gate is asked and no term is built",
            "why": "the x86 table's own rule is that no entry is "
                   "invented for an opcode no body contains, so this is "
                   "the evidence that decides which rows the RISC-V "
                   "reference gains",
            "bank_read": bank_path,
            "twins_read": twins_path,
            "compiled_targets": list(COMPILED_TARGETS),
            "per_target": per_target,
            "peak_kb": peak_kb(),
            "memory_bound_kb": ABORT_KB,
            "memory_abort": ABORT_NAME,
            "seconds": round(time.time() - started, 1),
        },
        "per_target": per_target,
        "no_entry_in_the_opcode_table": shaped,
        "rows": rows,
    }
    write_json(prefix + ".json", document)
    say("peak RSS: %d kB" % peak_kb())
    return 0


def one_census(record, src_root, work_root, number, table, unknown):
    cell = record["cell"]
    row = {
        "cell": {"mnem": cell["mnem"], "shape": cell["shape"],
                 "key_width": cell["key_width"]},
        "place": record["place"],
        "target": record["target"],
    }
    relative = (record.get("source") or {}).get("path") or ""
    source_path = os.path.join(src_root, relative)
    if not os.path.isfile(source_path):
        row["outcome"] = "SOURCE_NOT_ON_DISK"
        row["diagnostic"] = source_path
        return row
    source = open(source_path).read()
    work = os.path.join(work_root, "run%06d" % number)
    got, command, diagnostic = compile_and_carve(source, record["target"],
                                                 work)
    row["compile_command"] = command
    if got is None:
        row["outcome"] = "BUILD_REFUSED"
        row["diagnostic"] = (diagnostic or "").strip()[:600]
        return row
    raw, body = got
    row["outcome"] = "CARVED"
    row["instruction_count"] = len(body)
    seen = set()
    for line in body:
        text = line.strip()
        if not text:
            continue
        mnemonic = text.split()[0]
        base = mnemonic
        held_compressed = RV.COMPRESSED.get(mnemonic)
        if held_compressed is not None:
            base = held_compressed[0]
        entry = table.entry_for(base)
        if entry is not None and entry.build is not None:
            continue
        held = unknown.setdefault(mnemonic, {"lines": 0, "sources": 0,
                                             "targets": set()})
        held["lines"] = held["lines"] + 1
        held["targets"].add(record["target"])
        if mnemonic not in seen:
            held["sources"] = held["sources"] + 1
            seen.add(mnemonic)
    row["mnemonics_with_no_entry"] = sorted(seen)
    return row


# ==================================================================
# section 3: the run -- inherit.py's own, with the four routes in place
# ==================================================================

def run_command(ref_dir, op_dir, rows_path, twins_path, bank_path,
                src_root, prefix, work_root, limit):
    say("[0/5] the x86 reference this run uses")
    X86, TERMS, MT, MTAB, digest = TW.bring_in(ref_dir, op_dir)
    IN.X86_REFERENCE[0] = X86.Reference()
    holder = TERMS.Term(IN.X86_REFERENCE[0])
    reference = RV.RiscvReference()
    say("   %s sha256 %s" % (X86.__file__, digest))

    say("[1/5] the twinned x86 cells")
    wanted = IN.twinned_cells(twins_path)
    say("   %d (x86 cell, place) pairs a RISC-V cell twins" % len(wanted))

    say("[2/5] the bank, streamed")
    records = IN.bank_lines(bank_path, wanted)
    say("   %d preferred proved/agreed certificates on those pairs"
        % len(records))
    check_memory("after the bank")

    say("[3/5] the x86 cells' terms, rebuilt as z3 objects")
    cells = TW.x86_cells(rows_path)
    terms = {}
    for record in records:
        cell = record["cell"]
        key = (cell["mnem"], cell["shape"], cell["key_width"])
        if key in terms:
            continue
        held = cells.get(key)
        if held is None:
            terms[key] = None
            continue
        try:
            places = TW.rebuild(MT, MTAB, held)
        except Exception:
            terms[key] = None
            continue
        shaped = {}
        for place in places:
            shaped[place] = {
                "raw": places[place],
                "term": TW.positional(TERMS, places[place]),
                "text": holder.normalize(places[place]),
            }
        terms[key] = shaped
    del cells
    say("   %d distinct x86 cells rebuilt" % len(terms))
    check_memory("after the terms")

    say("[4/5] the inheritance, one certificate at a time")
    rows = []
    started = time.time()
    total = len(records)
    if limit is not None:
        total = min(total, limit)
    for number, record in enumerate(records, 1):
        if limit is not None and number > limit:
            break
        rows.append(IN.one_certificate(reference, TERMS, MT, holder,
                                       terms, wanted, record, src_root,
                                       work_root, number))
        if number % 25 == 0 or number == total:
            say("   [%d/%d] certificates, %.0f s, peak %.0f MB"
                % (number, total, time.time() - started,
                   check_memory("certificate %d" % number) / 1024.0))

    say("[5/5] writing")
    census = {}
    per_target = {}
    per_target_outcome = {}
    for row in rows:
        census[row["kind"]] = census.get(row["kind"], 0) + 1
        held = per_target.setdefault(row["target"], {})
        held[row["kind"]] = held.get(row["kind"], 0) + 1
        outcome = (row.get("verdict") or {}).get("outcome")
        shaped = per_target_outcome.setdefault(row["target"], {})
        shaped[outcome] = shaped.get(outcome, 0) + 1
    for kind in sorted(census):
        say("   %-28s %d" % (kind, census[kind]))
    for target in sorted(per_target_outcome):
        say("   %-8s %s" % (target,
                            json.dumps(per_target_outcome[target],
                                       sort_keys=True)))
    fh = open(prefix + ".jsonl", "w")
    for row in rows:
        fh.write(json.dumps(row, sort_keys=True) + "\n")
    fh.close()
    proved = set()
    for row in rows:
        if row["kind"] != "proved":
            continue
        cell = row["cell"]
        proved.add((cell.get("mnem"), cell.get("shape"),
                    cell.get("key_width")))
    say("   distinct RISC-V cells with an inherited PROVED certificate: "
        "%d" % len(proved))
    document = {
        "meta": {
            "task": "rv3",
            "what": "task rv2's inheritance re-run on the image that "
                    "carries the rust riscv64 LINUX target, the riscv64 "
                    "glibc and libstdc++ headers, and clang++ aimed "
                    "through them; the twins read, the bank records "
                    "chosen, the alignment, the gate and the record "
                    "shape are rv2's own and are called, not copied",
            "routes_replaced": TRIPLES,
            "not_attempted": list(NOT_ATTEMPTED),
            "bank_read": bank_path,
            "bank_sha256": IN.sha256_of(bank_path),
            "twins_read": twins_path,
            "twins_sha256": IN.sha256_of(twins_path),
            "x86_rows_read": rows_path,
            "x86_reference_file": X86.__file__,
            "x86_reference_sha256": digest,
            "riscv_reference_sha256": sha256_of_file(RV.__file__),
            "gate_width": "the cell's own key_width is the headline; "
                          "the whole written place is recorded beside "
                          "it on every row as "
                          "verdict_at_the_whole_place",
            "solver_timeout_ms": IN.SOLVER_MS,
            "census": census,
            "per_target": per_target,
            "per_target_outcome": per_target_outcome,
            "cells_with_a_proved_inherited_certificate": len(proved),
            "peak_kb": peak_kb(),
            "memory_bound_kb": ABORT_KB,
            "memory_abort": ABORT_NAME,
            "seconds": round(time.time() - started, 1),
            "certificates_out": prefix + ".jsonl",
        },
        "census": census,
        "per_target": per_target,
        "per_target_outcome": per_target_outcome,
        "cells_with_a_proved_inherited_certificate": len(proved),
    }
    write_json(prefix + ".json", document)
    say("peak RSS: %d kB" % peak_kb())
    return 0


def sha256_of_file(path):
    digest = hashlib.sha256()
    fh = open(path, "rb")
    while True:
        chunk = fh.read(1 << 20)
        if not chunk:
            break
        digest.update(chunk)
    fh.close()
    return digest.hexdigest()


def main():
    install()
    command = sys.argv[1]
    if command == "census":
        limit = None
        if len(sys.argv) > 9:
            limit = int(sys.argv[9])
        return census_command(sys.argv[2], sys.argv[3], sys.argv[4],
                              sys.argv[5], sys.argv[6], sys.argv[7],
                              sys.argv[8], limit)
    if command == "run":
        limit = None
        if len(sys.argv) > 10:
            limit = int(sys.argv[10])
        return run_command(sys.argv[2], sys.argv[3], sys.argv[4],
                           sys.argv[5], sys.argv[6], sys.argv[7],
                           sys.argv[8], sys.argv[9], limit)
    raise SystemExit("unknown command %r" % command)


if __name__ == "__main__":
    sys.exit(main())
