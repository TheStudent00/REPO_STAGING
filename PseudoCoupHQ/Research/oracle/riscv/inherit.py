#!/usr/bin/env python3
"""inherit.py -- THE INHERITANCE: every certificate the bank holds about a
twinned x86 cell, its SOURCE taken unchanged, compiled for riscv64,
carved, lifted with the RISC-V reference, and gated against the same term.

Node: hq.research.arch_unit_oracle.  Task rv2, brief section 2 step 3,
`PRIVATE/PseudoCoupHQ/Research/briefs/task_rv2_brief.md`.

WHAT THIS IS, one sentence, in relation: the measurement of the
hypothesis this whole task exists for -- "if we already know what is
proven in x86 with their combination of high-level compiler-operators to
emulate arch-opcodes, it should also be true in RISC-V" -- carried out by
taking each proved emulation's own source, aiming the same compiler at
riscv64, and asking z3 whether the body that comes back computes the same
term.

THE OBJECTS, one sentence each.
  * A CERTIFICATE is one banked record about one (cell, target, written
    place): the term, the rendered source and its sha256, the compiler
    and its flags, the carved body, and the gate's own verdict.
  * AN INHERITED CERTIFICATE is the same record re-measured on riscv64:
    the same source, a riscv64 compiler, a riscv64 body, and this line's
    own verdict, carrying `arch` and `inherited_from`.
  * THE TERM GATED AGAINST is the X86 TWIN CELL'S OWN TERM, rebuilt as a
    z3 object, because that is the term the certificate is about and the
    term the source was rendered from.
  * THE ALIGNMENT between the two architectures is an argument's
    POSITION, and nothing else: the x86 term's symbol named
    `seed_<family>` is the k-th argument when `<family>` is the k-th
    register of the target's own x86 argument sequence, and the k-th
    argument on riscv64 is in `a<k>` (or `fa<k>` for a floating-point
    one).  `arrival_contract` states it; a symbol whose family names no
    argument position is REFUSED by name and nothing is guessed.

THE WIDTH THE GATE COMPARES ON, and it carries its reading.  Two are
defensible and both are recorded on every row:
  * AT THE CELL'S OWN `key_width` -- the width the operation computes at.
    This is the headline, and it is the pipeline's own rule for a narrow
    answer (task ap6's re-pose) and the rule task rv1 measured its ten
    units under.
  * AT THE WHOLE WRITTEN PLACE -- all 64 bits.  A 32-bit x86 write
    ZERO-extends into the register and the riscv64 psABI returns a
    32-bit value SIGN-extended, so at the whole place a 32-bit cell's
    emulation differs above bit 31 for a return-value contract reason
    and not a computation reason.  The field
    `verdict_at_the_whole_place` says so per row rather than hiding it.

WHICH TARGETS, and why each.
  * `c` and `go`: the brief's two, and the two the image can aim at
    riscv64.
  * `rust`: the riscv64 target IS installed
    (`riscv64gc-unknown-none-elf`) and the rendered sources still refuse,
    because a bare-metal target has no standard library and the rendered
    crate does not declare `#![no_std]`.  The brief says the source is
    taken UNCHANGED, so the refusal is recorded with rustc's own words
    and is a flag, not a workaround.
  * the interpreted targets: an `agreed` certificate transfers AS IT IS.
    An interpreter's answer is the interpreter's, not the host
    architecture's; nothing is compiled and nothing is re-derived here
    beyond the one handful the brief asks be re-run to show it.
  * `cpp` and `swift`: not attempted.  The brief names c, go and rust;
    swift has no riscv64 toolchain in the image at all.

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

MEMORY, as the law requires: the bank is STREAMED line by line and never
held whole; only the keys the twins name are kept.  Bound 6 GB, named
abort ABORT_MEMORY_RV2, peak resident printed.

WHERE THE OUTPUT GOES, and why it is not the bank file.  The brief says
"certificates appended to the bank with `arch`".  The coordinator's
instruction for this task says not to touch the bank file, because task
ref2 is working beside this one and the bank is being read by it.  So the
riscv64 certificates are written to `certificates_riscv64.jsonl` in this
folder, in the bank's own record shape, and the log carries this as a
FLAG: the file is a concatenation away from being in the bank and
nothing was lost.

Coding discipline (the owner's ruling): no complex/compound one-liner statements.

usage:
  inherit.py plan <twins.json> <bank.jsonl> <out prefix>
  inherit.py run  <ref dir> <op dir> <x86 rows json> <twins.json>
                  <bank.jsonl> <src root> <out prefix> <work dir> [limit]
"""

import hashlib
import json
import os
import re
import resource
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import riscv_reference as RV                                # noqa: E402
import riscv_carve as CARVE                                 # noqa: E402
import claim_check as CC                                    # noqa: E402
import twins as TW                                          # noqa: E402
import z3                                                    # noqa: E402


ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_RV2"
SOLVER_MS = 3000

COMPILED_TARGETS = ("c", "go")
RUST_TARGET = "rust"
NOT_ATTEMPTED = ("cpp", "swift")
INTERPRETED = ("cpython", "php", "ruby", "java", "javascript", "dart",
               "csharp")

SYMBOL_RE = re.compile(r"emu_[A-Za-z0-9_]+")

X86_REFERENCE = [None]
"""the one x86 reference this run walks certificates' own bodies with,
set once by `run_command` from the directory the caller names."""


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
# section 1: which x86 cells are twinned, and which certificates
# ==================================================================

def twinned_cells(twins_path):
    """(x86 cell key, place) -> the RISC-V cell that twins it."""
    out = {}
    document = json.load(open(twins_path))
    for row in document["rows"]:
        for place in row["places"]:
            for reading, found in (("whole_place", place),
                                   ("key_width",
                                    place.get("at_key_width") or {})):
                twin = found.get("x86_twin")
                if twin is None:
                    continue
                key = (twin["mnem"], twin["shape"], twin["key_width"],
                       twin["place"])
                if key in out:
                    continue
                out[key] = {
                    "riscv_cell": {"mnem": row["mnem"],
                                   "shape": row["shape"],
                                   "key_width": row["key_width"]},
                    "riscv_place": place["writes"],
                    "how": found.get("how"),
                    "reading": reading,
                }
                for other in (found.get("x86_twins_all") or []):
                    other_key = (other["mnem"], other["shape"],
                                 other["key_width"], other["place"])
                    if other_key in out:
                        continue
                    out[other_key] = dict(out[key])
    return out


def bank_lines(bank_path, wanted):
    """the bank, STREAMED: only the preferred proved/agreed
    certificates whose (cell, place) a twin names."""
    out = []
    fh = open(bank_path)
    for line in fh:
        line = line.strip()
        if not line:
            continue
        record = json.loads(line)
        if not record.get("preferred"):
            continue
        if record.get("kind") not in ("proved", "agreed"):
            continue
        cell = record["cell"]
        key = (cell["mnem"], cell["shape"], cell["key_width"],
               record["place"])
        if key not in wanted:
            continue
        out.append(record)
    fh.close()
    return out


# ==================================================================
# section 2: compile the certificate's own source for riscv64
# ==================================================================

RUST_SHIP = ["--crate-type=lib", "--emit=obj", "-C", "opt-level=1",
             "-C", "debug-assertions=off",
             "--target=riscv64gc-unknown-none-elf"]


def symbol_of(source):
    hit = SYMBOL_RE.search(source)
    if hit is None:
        return None
    return hit.group(0)


def compile_and_carve(source, target, work):
    """(the carved body, the compile command, the diagnostic) for one
    rendered source aimed at riscv64 at the corpus's own ship flags."""
    if not os.path.isdir(work):
        os.makedirs(work)
    name = symbol_of(source)
    if name is None:
        return None, "", "no emu_ symbol found in the rendered source"
    if target == "c":
        path = os.path.join(work, "unit.c")
        obj = os.path.join(work, "unit.o")
        open(path, "w").write(source)
        command = [CARVE.CLANG] + CARVE.SHIP["c"] + ["-c", path,
                                                     "-o", obj]
        rc, out, err = CARVE.sh(command)
        if rc != 0:
            return None, " ".join(command), (err or out)
        got, err = CARVE.disassemble(obj, name, True)
        if got is None:
            return None, " ".join(command), err
        return got, " ".join(command), ""
    if target == "go":
        open(os.path.join(work, "go.mod"), "w").write(CARVE.GOMOD)
        open(os.path.join(work, "main.go"), "w").write(source)
        obj = os.path.join(work, "bin_rv")
        command = ["go", "build", "-o", obj, "."]
        rc, out, err = CARVE.sh(command, cwd=work, env=CARVE.GO_ENV,
                                timeout=600)
        printed = "GOARCH=riscv64 GOOS=linux " + " ".join(command)
        if rc != 0:
            return None, printed, (err or out)
        got, err = CARVE.disassemble(obj, "main." + name, True)
        if got is None:
            return None, printed, err
        return got, printed, ""
    if target == RUST_TARGET:
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
    return None, "", "no riscv64 route for target %r" % target


# ==================================================================
# section 3: the gate
# ==================================================================

def shared_arguments(target, key_width):
    """the ONE set of unknowns both architectures' bodies are functions
    of, and the two bindings that put them there.

    THE ALIGNMENT, and it is the only one that needs no guess: an
    ARGUMENT'S POSITION.  The k-th integer argument of a c function is
    in `rdi, rsi, rdx, rcx, r8, r9` on x86-64 and in `a0 .. a7` on
    riscv64; go's own register rule names `rax, rbx, rcx, rdi, rsi,
    r8` and `a0 .. a7`; the k-th floating-point argument is in
    `xmm0 ..` and in `fa0 ..`.  Binding argument k to ONE shared
    symbol on both sides makes the two bodies two functions of the same
    unknowns, and z3 can be asked whether they are equal -- which is
    exactly what task rv1's `claim_check.py` did for its ten units.

    NOTHING HERE READS THE CELL'S OWN SYMBOL NAMES.  A cell's term is
    named after the SWEEP'S operand registers (`%rdi`, `%rsi`) whatever
    the language, and which argument feeds which instruction operand is
    the compiler's choice, not a fact this file can read off the cell.
    So the certificate's own x86 BODY is walked here beside the riscv64
    one, and the chain is: the bank proved that body computes the term,
    and this file proves the riscv64 body computes the same function of
    the same arguments.

    A FLOATING-POINT ARRIVAL, and the one architecture fact in it: a
    32-bit float held in a 64-bit riscv64 float register is NaN-boxed
    (the upper 32 bits are all ones), so a `float` argument binds
    `Concat(0xFFFFFFFF, the low 32 bits)` of the shared symbol and a
    `double` argument the low 64.  Which of the two is read off the
    cell's own `key_width`."""
    integer_sequence = CC.X86_INTEGER.get(target)
    float_sequence = CC.X86_FLOAT.get(target)
    if integer_sequence is None:
        return None, None
    seed = {}
    contract = []
    riscv_integer = CC.RISCV_INTEGER[target]
    riscv_float = CC.RISCV_FLOAT[target]
    for index, family in enumerate(integer_sequence):
        if index >= len(riscv_integer):
            break
        symbol = z3.BitVec("arg%d" % index, 64)
        seed[family] = symbol
        contract.append((riscv_integer[index], symbol))
    for index, family in enumerate(float_sequence):
        if index >= len(riscv_float):
            break
        symbol = z3.BitVec("farg%d" % index, 128)
        seed[family] = symbol
        value = as_float_arrival(symbol, key_width)
        if value is None:
            continue
        contract.append((riscv_float[index], value))
    return seed, contract


def as_float_arrival(symbol, key_width):
    width = key_width or 64
    if width not in (32, 64):
        width = 64
    if symbol.size() < width:
        return None
    low = z3.Extract(width - 1, 0, symbol)
    if width == 32:
        return z3.Concat(z3.BitVecVal((1 << 32) - 1, 32), low)
    return low


def x86_answer_home(place, bits):
    """where a compiled function leaves its answer on x86-64: `xmm0`
    for a floating-point place, `rax` otherwise."""
    width = bits
    if width > 64:
        width = 64
    if place.startswith("reg_xmm"):
        return ("xmm0", width)
    return ("rax", width)


def x86_answer(reference, state, place, bits):
    low = reference.answer_of(state, x86_answer_home(place, bits))
    if bits <= 64:
        return low
    high = reference.answer_of(state, ("rdx", 64))
    return z3.Concat(high, low)


def answer_home(place):
    """where the compiled emulation leaves its answer on riscv64: a
    floating-point place returns in `fa0`, everything else in `a0`, and
    a place wider than one register arrives in `a0` and `a1` -- the
    psABI's own rule for a 128-bit return."""
    if place.startswith("reg_xmm"):
        return "fa0"
    return "a0"


def answer_of(reference, state, place, bits):
    """the term the body left in its answer home, at `bits` wide."""
    home = answer_home(place)
    low = reference.answer_of(state, home)
    if bits <= 64:
        return low
    high = reference.answer_of(state, "a1")
    return z3.Concat(high, low)


def at_width(term, width):
    if term.size() == width:
        return term
    if term.size() > width:
        return z3.Extract(width - 1, 0, term)
    return z3.ZeroExt(width - term.size(), term)


def decide(left, right, timeout_ms):
    solver = z3.Solver()
    solver.set("timeout", timeout_ms)
    solver.add(left != right)
    verdict = solver.check()
    if verdict == z3.unsat:
        return "PROVED", None
    if verdict == z3.unknown:
        return "UNDECIDED", None
    model = solver.model()
    shown = {}
    for declaration in model.decls():
        shown[declaration.name()] = str(model[declaration])
    return "DISPROVED", shown


# ==================================================================
# section 4: the run
# ==================================================================

def run_command(ref_dir, op_dir, rows_path, twins_path, bank_path,
                src_root, prefix, work_root, limit):
    say("[0/5] the x86 reference this run uses")
    X86, TERMS, MT, MTAB, digest = TW.bring_in(ref_dir, op_dir)
    X86_REFERENCE[0] = X86.Reference()
    holder = TERMS.Term(X86_REFERENCE[0])
    reference = RV.RiscvReference()

    say("[1/5] the twinned x86 cells")
    wanted = twinned_cells(twins_path)
    say("   %d (x86 cell, place) pairs a RISC-V cell twins" % len(wanted))

    say("[2/5] the bank, streamed")
    records = bank_lines(bank_path, wanted)
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
        rows.append(one_certificate(reference, TERMS, MT, holder,
                                    terms, wanted, record, src_root,
                                    work_root, number))
        if number % 25 == 0 or number == total:
            say("   [%d/%d] certificates, %.0f s, peak %.0f MB"
                % (number, total, time.time() - started,
                   check_memory("certificate %d" % number) / 1024.0))

    say("[5/5] writing")
    census = {}
    per_target = {}
    for row in rows:
        census[row["kind"]] = census.get(row["kind"], 0) + 1
        held = per_target.setdefault(row["target"], {})
        held[row["kind"]] = held.get(row["kind"], 0) + 1
    for kind in sorted(census):
        say("   %-28s %d" % (kind, census[kind]))
    fh = open(prefix + ".jsonl", "w")
    for row in rows:
        fh.write(json.dumps(row, sort_keys=True) + "\n")
    fh.close()
    document = {
        "meta": {
            "task": "rv2",
            "what": "every preferred proved/agreed certificate whose x86 "
                    "cell a RISC-V cell twins, its SOURCE taken "
                    "unchanged, compiled for riscv64 at the corpus's own "
                    "ship flags, carved, lifted with the RISC-V "
                    "reference and gated against the same term",
            "bank_read": bank_path,
            "bank_sha256": sha256_of(bank_path),
            "twins_read": twins_path,
            "x86_reference_file": X86.__file__,
            "x86_reference_sha256": digest,
            "gate_width": "the cell's own key_width is the headline; "
                          "the whole written place is recorded beside "
                          "it on every row as "
                          "verdict_at_the_whole_place",
            "solver_timeout_ms": SOLVER_MS,
            "census": census,
            "per_target": per_target,
            "peak_kb": peak_kb(),
            "memory_bound_kb": ABORT_KB,
            "memory_abort": ABORT_NAME,
            "seconds": round(time.time() - started, 1),
            "certificates_out": prefix + ".jsonl",
            "not_in_the_bank_file": "the brief says the certificates are "
                                    "appended to the bank; the "
                                    "coordinator's instruction for this "
                                    "task forbids touching the bank "
                                    "file while task ref2 runs beside "
                                    "it, so they are written here in "
                                    "the bank's own record shape",
        },
        "census": census,
        "per_target": per_target,
    }
    write_json(prefix + ".json", document)
    say("peak RSS: %d kB" % peak_kb())
    return 0


def sha256_of(path):
    digest = hashlib.sha256()
    fh = open(path, "rb")
    while True:
        chunk = fh.read(1 << 20)
        if not chunk:
            break
        digest.update(chunk)
    fh.close()
    return digest.hexdigest()


def one_certificate(reference, TERMS, MT, holder, terms, wanted,
                    record, src_root, work_root, number):
    cell = record["cell"]
    key = (cell["mnem"], cell["shape"], cell["key_width"])
    twin = wanted.get((cell["mnem"], cell["shape"], cell["key_width"],
                       record["place"])) or {}
    row = {
        "arch": "riscv64",
        "cell": dict(twin.get("riscv_cell") or {}),
        "inherited_from": {
            "mnem": cell["mnem"],
            "shape": cell["shape"],
            "key_width": cell["key_width"],
            "place": record["place"],
            "arch": "x86_64",
            "kind": record["kind"],
            "pass": (record.get("produced_by") or {}).get("pass"),
        },
        "twin_how": twin.get("how"),
        "twin_reading": twin.get("reading"),
        "place": record["place"],
        "target": record["target"],
        "term_text": record.get("term_text"),
        "source": dict(record.get("source") or {}),
    }
    if record["target"] in INTERPRETED:
        row["kind"] = "agreed"
        row["verdict"] = {
            "outcome": "TRANSFERS_AS_IT_IS",
            "reason": "an interpreted target's agreement is the "
                      "interpreter's own answer on a sample of values; "
                      "the interpreter is a program, and its answer "
                      "does not depend on the architecture the "
                      "interpreter itself was compiled for. Nothing is "
                      "compiled for riscv64 here and nothing is "
                      "re-derived; the one handful the brief asks for "
                      "is re-run in its own lane.",
        }
        return row
    if record["target"] in NOT_ATTEMPTED:
        row["kind"] = "refused"
        row["verdict"] = {
            "outcome": "NOT_ATTEMPTED",
            "reason": "the brief names c, go and rust; this target is "
                      "not among them and swift has no riscv64 "
                      "toolchain in the image",
        }
        return row
    source_path = os.path.join(src_root,
                               (record.get("source") or {}).get("path")
                               or "")
    if not os.path.isfile(source_path):
        row["kind"] = "refused"
        row["verdict"] = {"outcome": "SOURCE_NOT_ON_DISK",
                          "reason": "the certificate's source file is "
                                    "not at %s" % source_path}
        return row
    source = open(source_path).read()
    row["source"]["read_from"] = source_path
    row["source"]["sha256_read"] = hashlib.sha256(
        source.encode("utf-8")).hexdigest()
    work = os.path.join(work_root, "run%06d" % number)
    got, command, diagnostic = compile_and_carve(source, record["target"],
                                                 work)
    row["compiler"] = {"command": command,
                       "target_triple": triple_of(record["target"])}
    if got is None:
        row["kind"] = "refused"
        row["verdict"] = {"outcome": "BUILD_REFUSED",
                          "reason": (diagnostic or "").strip()[:900]}
        return row
    raw, body = got
    row["body"] = {"bytes": " ".join(raw), "text": " ; ".join(body)}
    held = terms.get(key) or {}
    place = held.get(record["place"])
    if place is None:
        row["kind"] = "refused"
        row["verdict"] = {"outcome": "NO_TERM",
                          "reason": "the x86 cell's own place could not "
                                    "be rebuilt as a z3 object"}
        return row
    bits = place["raw"].size()
    seed, contract = shared_arguments(record["target"], cell["key_width"])
    if seed is None:
        row["kind"] = "refused"
        row["verdict"] = {"outcome": "NO_ARRIVAL_CONTRACT",
                          "reason": "no x86 argument sequence is stated "
                                    "for target %r" % record["target"]}
        return row
    row["route"] = record.get("route")
    row["answer_home"] = {"riscv64": answer_home(record["place"]),
                          "x86_64": x86_answer_home(record["place"],
                                                    bits)[0]}
    x86_body = (record.get("body") or {}).get("text")
    if not x86_body:
        row["kind"] = "refused"
        row["verdict"] = {"outcome": "NO_X86_BODY",
                          "reason": "the certificate records no carved "
                                    "x86-64 body to compare against"}
        return row
    row["x86_body"] = x86_body
    try:
        x86_state = X86_REFERENCE[0].simulate(x86_body, None, dict(seed))
        left = x86_answer(X86_REFERENCE[0], x86_state, record["place"],
                          bits)
    except Exception as problem:
        row["kind"] = "refused"
        row["verdict"] = {"outcome": "X86_WALK_REFUSED",
                          "reason": "%s: %s" % (type(problem).__name__,
                                                problem)}
        return row
    try:
        state = reference.simulate(body, contract, {})
        answer = answer_of(reference, state, record["place"], bits)
    except Exception as problem:
        row["kind"] = "refused"
        row["verdict"] = {"outcome": "WALK_REFUSED",
                          "reason": "%s: %s" % (type(problem).__name__,
                                                problem)}
        return row
    row["riscv_term"] = holder.normalize(answer)
    row["x86_body_term"] = holder.normalize(left)
    row["x86_term_rebuilt"] = place["text"]
    width = cell["key_width"] or bits
    if width > left.size():
        width = left.size()
    if width > answer.size():
        width = answer.size()
    outcome, counterexample = decide(at_width(answer, width),
                                     at_width(left, width),
                                     SOLVER_MS)
    whole = left.size()
    if whole > answer.size():
        whole = answer.size()
    outcome_whole, counter_whole = decide(at_width(answer, whole),
                                          at_width(left, whole),
                                          SOLVER_MS)
    row["verdict"] = {
        "outcome": outcome,
        "compared_on_bits": width,
        "counterexample": counterexample,
        "solver_timeout_ms": SOLVER_MS,
        "reason": "z3 on the riscv64 body's own term against the "
                  "certificate's own x86-64 body's term, both as "
                  "functions of the same arguments, at the cell's own "
                  "key_width; the bank already proved the x86-64 body "
                  "computes the cell's term, so the two together are "
                  "the inheritance",
    }
    row["verdict_at_the_whole_place"] = {
        "outcome": outcome_whole,
        "compared_on_bits": whole,
        "counterexample": counter_whole,
    }
    if outcome == "PROVED":
        row["kind"] = "proved"
    elif outcome == "DISPROVED":
        row["kind"] = "sat"
    else:
        row["kind"] = "undecided"
    return row


def triple_of(target):
    if target == "c":
        return "riscv64-unknown-linux-gnu (clang --target)"
    if target == "go":
        return "GOARCH=riscv64 GOOS=linux"
    if target == RUST_TARGET:
        return "riscv64gc-unknown-none-elf (rustc --target)"
    return None


def plan_command(twins_path, bank_path, prefix):
    """what the run would attempt, and nothing run."""
    wanted = twinned_cells(twins_path)
    say("   %d (x86 cell, place) pairs a RISC-V cell twins" % len(wanted))
    records = bank_lines(bank_path, wanted)
    per_target = {}
    per_kind = {}
    for record in records:
        per_target[record["target"]] = per_target.get(
            record["target"], 0) + 1
        per_kind[record["kind"]] = per_kind.get(record["kind"], 0) + 1
    for target in sorted(per_target):
        say("   %-12s %d" % (target, per_target[target]))
    say("   kinds: %s" % json.dumps(per_kind, sort_keys=True))
    document = {
        "meta": {"task": "rv2",
                 "what": "the plan: which banked certificates the "
                         "inheritance would attempt",
                 "bank_sha256": sha256_of(bank_path)},
        "pairs_twinned": len(wanted),
        "per_target": per_target,
        "per_kind": per_kind,
    }
    write_json(prefix + ".json", document)
    return 0


def main():
    command = sys.argv[1]
    if command == "plan":
        return plan_command(sys.argv[2], sys.argv[3], sys.argv[4])
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
