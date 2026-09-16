#!/usr/bin/env python3
"""sail_guard.py -- THE GUARD OF THE GENERATED LIFTER: every instruction
the emit defines, checked at points against the Sail model's own C
simulator (task sl1; the successor of `sail_points.py`, whose harness
mechanics it keeps and whose population it replaces).

WHAT THIS FILE DOES, one sentence: for every constructor of the model's
`instruction` type and every assignment of its enum-typed fields, it
asks the model's own encoder for the instruction's WORD, learns from a
symbolic run of the generated lifter which register fields are read and
which is written, runs the C simulator over a bare-metal program that
executes that word at many concrete inputs, evaluates the lifter's term
at the same inputs, and compares value by value.

THIS IS A CHECK AT POINTS, NOT AN EQUALITY.

THE POPULATION, mechanically:
  * the constructors and their field types: the emit's own
    `inductive instruction where | NAME (_ : (T1 × T2 × ...))` lines;
  * an enum-typed field: every member of `inductive T where | A | B`;
  * a Bool field: both values; a `(BitVec n)` field: a few edge values
    folded to n bits; a `Nat` or other field: refused by type;
  * register fields (regidx, fregidx, cregidx): slots x10.. / f10.. in
    field order, then re-assigned by the roles the symbolic run shows.
A row whose roles the harness cannot present (more than two inputs, no
written register, a memory access, a transfer) is refused by cause.

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

HOW THIS FILE OBEYS IT: a row is keyed by the model's constructor and
its concrete fields; `mnem` is llvm-objdump's reading of the word, a
display label.

usage:
  sail_guard.py <out prefix> <work dir> [--points N] [--first N]
"""
import json
import os
import random
import re
import resource
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import z3                                                   # noqa: E402
import lean_reader as LR                                    # noqa: E402
import lifter as GL                                         # noqa: E402
import riscv_reference as RV                                # noqa: E402

MEMORY_CEILING_MB = 6144
ABORT_NAME = "ABORT_MEMORY_SL1"
SIMULATOR = "/usr/local/bin/sail_riscv_sim"
MARCH = "rv64gc_zba_zbb_zbs_zcb_zicond"
RESET_ADDRESS = "0x80000000"
MASK = (1 << 64) - 1

CONSTRUCTOR = re.compile(r"^\s*\|\s*([A-Z][A-Za-z0-9_]*)\s*(?:\(_\s*:\s*(.*)\))?\s*$")
ENUM = re.compile(r"^inductive\s+([A-Za-z_][A-Za-z0-9_]*)\s+where\s*((?:\|\s*[A-Za-z_][A-Za-z0-9_]*\s*)+)\s*$")
ENUM_HEAD = re.compile(r"^inductive\s+([A-Za-z_][A-Za-z0-9_]*)\s+where\s*$")
ENUM_MEMBER = re.compile(r"^\s*\|\s*([A-Za-z_][A-Za-z0-9_]*)\s*$")
STRUCT_HEAD = re.compile(r"^structure\s+([A-Za-z_][A-Za-z0-9_]*)\s+where\s*$")
STRUCT_FIELD = re.compile(r"^\s+([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*?)\s*$")
ABBREV = re.compile(r"^abbrev\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?::\s*[^:]*?)?:=\s*(.*?)\s*$")
BITS = re.compile(r"^\(?BitVec\s+(\d+)\)?$")


def peak_rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def check_memory(where):
    peak = peak_rss_mb()
    if peak > MEMORY_CEILING_MB:
        raise SystemExit("%s: peak RSS %.1f MB passed the %d MB ceiling at %s"
                         % (ABORT_NAME, peak, MEMORY_CEILING_MB, where))
    return peak


# ------------------------------------------------------------------
# the population, read off the emit
# ------------------------------------------------------------------

def split_product(text):
    """`((BitVec 20) × regidx × uop)` -> ['(BitVec 20)', 'regidx', 'uop']"""
    text = text.strip()
    if text.startswith("(") and text.endswith(")"):
        inner = text[1:-1]
        depth = 0
        balanced = True
        for index, char in enumerate(inner):
            if char == "(":
                depth = depth + 1
            if char == ")":
                depth = depth - 1
            if depth < 0:
                balanced = False
        if balanced and depth == 0:
            text = inner
    out = []
    depth = 0
    current = ""
    for char in text:
        if char == "(":
            depth = depth + 1
        if char == ")":
            depth = depth - 1
        if char == "×" and depth == 0:
            out.append(current.strip())
            current = ""
            continue
        current = current + char
    if current.strip():
        out.append(current.strip())
    return out


def constructors_of(emit_dir):
    """[(name, [field types])] from `inductive instruction where`."""
    out = []
    for root, _dirs, files in os.walk(emit_dir):
        for name in sorted(files):
            if not name.endswith(".lean"):
                continue
            inside = False
            for line in open(os.path.join(root, name), encoding="utf-8"):
                if line.startswith("inductive instruction where"):
                    inside = True
                    continue
                if inside:
                    hit = CONSTRUCTOR.match(line)
                    if hit is None:
                        if line.strip() and not line.startswith(" "):
                            inside = False
                        continue
                    types = split_product(hit.group(2)) if hit.group(2) else []
                    out.append((hit.group(1), types))
    return out


def enums_of(emit_dir):
    """{enum name: [members]} from every `inductive T where | A | B`, on
    one line or one member per line; {structure name: [(field, type)]}
    from every `structure T where` whose fields are typed; and the
    abbreviations `abbrev T := U`."""
    out = {}
    structs = {}
    abbrevs = {}
    for root, _dirs, files in os.walk(emit_dir):
        for name in sorted(files):
            if not name.endswith(".lean"):
                continue
            pending = None
            struct = None
            for line in open(os.path.join(root, name), encoding="utf-8"):
                hit = ABBREV.match(line)
                if hit is not None:
                    abbrevs.setdefault(hit.group(1), hit.group(2))
                hit = ENUM.match(line)
                if hit is not None:
                    members = re.findall(r"\|\s*([A-Za-z_][A-Za-z0-9_]*)", hit.group(2))
                    out.setdefault(hit.group(1), members)
                    pending = None
                    continue
                hit = ENUM_HEAD.match(line)
                if hit is not None:
                    pending = hit.group(1)
                    out.setdefault(pending, [])
                    struct = None
                    continue
                hit = STRUCT_HEAD.match(line)
                if hit is not None:
                    struct = hit.group(1)
                    structs.setdefault(struct, [])
                    pending = None
                    continue
                if pending is not None:
                    hit = ENUM_MEMBER.match(line)
                    if hit is not None:
                        out[pending].append(hit.group(1))
                        continue
                    if line.strip():
                        pending = None
                if struct is not None:
                    hit = STRUCT_FIELD.match(line)
                    if hit is not None and not line.strip().startswith("deriving"):
                        structs[struct].append((hit.group(1), hit.group(2)))
                        continue
                    if line.strip() and not line.startswith(" "):
                        struct = None
    out["__structs__"] = structs
    out["__abbrevs__"] = abbrevs
    return out


IMMEDIATE_SHAPES = [0, 1, -1, 2, -2, 0x55, -0x56, 7, 8, -8, 0x7FF, -0x800]


def immediates(width):
    """a few edge values folded to `width` bits, distinct."""
    out = []
    for value in IMMEDIATE_SHAPES:
        folded = value % (1 << width)
        if folded not in out:
            out.append(folded)
    return out[:8]


def field_choices(kind, enums, depth=0):
    """the values one field of type `kind` takes in the population, or None
    when the type has no enumeration here (register fields are slots)."""
    kind = kind.strip()
    if kind.startswith("(") and kind.endswith(")") and "×" not in kind and \
            not kind.startswith("(BitVec"):
        kind = kind[1:-1].strip()
    if kind in ("regidx", "fregidx", "cregidx", "cfregidx"):
        return "register"
    abbrevs = enums.get("__abbrevs__", {})
    if kind in abbrevs and depth < 6:
        return field_choices(abbrevs[kind], enums, depth + 1)
    structs = enums.get("__structs__", {})
    if kind in structs and structs[kind] and depth < 6:
        per_field = []
        for field, ftype in structs[kind]:
            choice = field_choices(ftype, enums, depth + 1)
            if choice is None or choice == "register":
                return None
            per_field.append([(field, v) for v in choice])
        return [dict(items) for items in product(per_field)]
    if kind == "Bool":
        return [z3.BoolVal(False), z3.BoolVal(True)]
    hit = BITS.match(kind)
    if hit is not None:
        width = int(hit.group(1))
        return [z3.BitVecVal(v, width) for v in immediates(width)]
    if kind in enums:
        return [LR.Ctor(member, []) for member in enums[kind]]
    return None


def product(lists):
    out = [[]]
    for items in lists:
        out = [row + [item] for row in out for item in items]
    return out


def rows_of(constructors, enums):
    """[(name, [field values or 'register'])] -- every enum assignment."""
    rows = []
    refused = []
    for name, types in constructors:
        choices = []
        problem = None
        for kind in types:
            choice = field_choices(kind, enums)
            if choice is None:
                problem = "field type %s has no enumeration here" % kind
                break
            choices.append(choice if choice != "register" else ["register"])
        if problem is not None:
            refused.append({"constructor": name, "cause": problem})
            continue
        for assignment in product(choices):
            rows.append((name, types, assignment))
    return rows, refused


# ------------------------------------------------------------------
# one row: slots, roles, word
# ------------------------------------------------------------------

REGISTER_SLOTS = [10, 11, 12, 13, 14]


def make_instruction(name, types, assignment, slots):
    """the model's own instruction value with register fields at `slots`."""
    fields = []
    used = 0
    for kind, value in zip(types, assignment):
        if is_register(value):
            index = slots[used]
            used = used + 1
            if kind == "regidx":
                fields.append(LR.Ctor("Regidx", [z3.BitVecVal(index, 5)]))
            elif kind == "fregidx":
                fields.append(LR.Ctor("Fregidx", [z3.BitVecVal(index, 5)]))
            elif kind == "cregidx":
                fields.append(LR.Ctor("Cregidx", [z3.BitVecVal(index - 8, 3)]))
            else:
                fields.append(LR.Ctor("Cfregidx", [z3.BitVecVal(index - 8, 3)]))
            continue
        fields.append(value)
    if not fields:
        return LR.Ctor(name, [None])
    if len(fields) == 1:
        return LR.Ctor(name, [fields[0]])
    return LR.Ctor(name, [tuple(fields)])


def word_of(lifter, instr):
    """(word, size) from the model's own encoders, or None with the cause."""
    for encoder, size in (("encdec_forwards", 4), ("encdec_compressed_forwards", 2)):
        if encoder not in lifter.definitions:
            continue
        machine = LR.Machine(lifter.widths, dict(lifter.reset_registers))
        try:
            value = lifter.reader.call(encoder, [instr], machine)
        except LR.ReadRefused as problem:
            last = "%s: %s" % (encoder, ("%s" % problem)[:160])
            continue
        simplified = z3.simplify(LR.bv_of(value))
        if not z3.is_bv_value(simplified):
            last = "%s: a symbolic word" % encoder
            continue
        return (simplified.as_long(), size), None
    return None, last


def roles_of(reference, word, size, register_kinds):
    """which register slots the instruction reads and writes, from one
    symbolic run of the generated lifter on the word."""
    state = RV.MachineState({})
    line = ".word 0x%08x" % word if size == 4 else ".hword 0x%04x" % word
    try:
        reference.step(state, line)
    except RV.NotModeled as problem:
        return None, "LIFTER_REFUSED: %s" % ("%s" % problem)[:300]
    except RV.LeavesTheUnit as problem:
        return None, "LEAVES_THE_UNIT: %s" % ("%s" % problem)[:200]
    written = []
    for index, term in state.registers.items():
        if index == 0:
            continue
        seed = "seed_x%d" % index
        if not (z3.is_const(term) and str(term) == seed):
            written.append(("x", index, term))
    for index, term in state.fregisters.items():
        seed = "seed_f%d" % index
        if not (z3.is_const(term) and str(term) == seed):
            written.append(("f", index, term))
    reads = set()
    for _kind, _index, term in written:
        for name in free_symbols(term):
            hit = re.match(r"^seed_([xf])(\d+)$", name)
            if hit is not None:
                reads.add((hit.group(1), int(hit.group(2))))
            elif name.startswith("seed_MEM") or name == "pc":
                return None, "READS_%s" % ("MEMORY" if "MEM" in name else "PC")
    if state.memory:
        return None, "TOUCHES_MEMORY"
    if state.branch_condition is not None:
        return None, "A_BRANCH"
    return {"written": written, "reads": sorted(reads)}, None


def free_symbols(term):
    out = set()
    seen = set()
    stack = [term]
    while stack:
        node = stack.pop()
        if node.get_id() in seen:
            continue
        seen.add(node.get_id())
        if z3.is_const(node) and node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
            out.add(str(node))
            continue
        for child in node.children():
            stack.append(child)
    return out


# ------------------------------------------------------------------
# the harness, one template with four modes
# ------------------------------------------------------------------

PROGRAM = """    .section .text.init, "ax", @progbits
    .globl _start
_start:
    li    t0, 0x6000
    csrs  mstatus, t0
    la    s0, inputs
    la    s1, results
    li    s2, %(count)d
loop:
    ld    a0, 0(s0)
    ld    a1, 8(s0)
%(moves_in)s
    %(instruction)s
%(moves_out)s
    sd    a2, 0(s1)
    addi  s0, s0, 16
    addi  s1, s1, 8
    addi  s2, s2, -1
    bnez  s2, loop
    la    t0, tohost
    li    t1, 1
    sd    t1, 0(t0)
spin:
    j     spin

    .section .data
    .align 3
inputs:
%(inputs)s
    .align 6
    .globl tohost
tohost:
    .dword 0
    .globl fromhost
fromhost:
    .dword 0
    .align 3
    .globl begin_signature
begin_signature:
results:
    .space %(space)d
    .globl end_signature
end_signature:
"""

LINKER = """OUTPUT_ARCH(riscv)
ENTRY(_start)
SECTIONS
{
  . = %(reset)s;
  .text.init : { *(.text.init) }
  .text : { *(.text) }
  . = ALIGN(0x1000);
  .data : { *(.data) }
}
"""


def sh(cmd, timeout=900):
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              timeout=timeout)
        return proc.returncode, proc.stdout.decode("utf-8", "replace"), \
            proc.stderr.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT after %ds" % timeout
    except OSError as exc:
        return 125, "", "OSError %s" % exc


def run_word(word, size, moves_in, moves_out, points, work):
    lines = []
    for left, right in points:
        lines.append("    .dword 0x%016x" % (left & MASK))
        lines.append("    .dword 0x%016x" % (right & MASK))
    instruction = ".word 0x%08x" % word if size == 4 else ".hword 0x%04x" % word
    body = PROGRAM % {"count": len(points), "instruction": instruction,
                      "moves_in": "\n".join("    " + m for m in moves_in),
                      "moves_out": "\n".join("    " + m for m in moves_out),
                      "inputs": "\n".join(lines), "space": 8 * len(points)}
    source = os.path.join(work, "one.S")
    script = os.path.join(work, "link.ld")
    elf = os.path.join(work, "one.elf")
    signature = os.path.join(work, "sig.txt")
    open(source, "w").write(body)
    open(script, "w").write(LINKER % {"reset": RESET_ADDRESS})
    if os.path.exists(signature):
        os.remove(signature)
    rc, out, err = sh(["clang", "--target=riscv64-unknown-elf", "-march=" + MARCH,
                       "-mabi=lp64d", "-nostdlib", "-fuse-ld=lld", "-T", script,
                       source, "-o", elf])
    if rc != 0:
        return None, "ASSEMBLE_REFUSED: %s" % (err or out).strip()[:300]
    limit = 60 * len(points) + 2000
    rc, out, err = sh([SIMULATOR, "--inst-limit", str(limit), "--test-signature",
                       signature, elf])
    if rc != 0:
        return None, "SIMULATOR_REFUSED: %s" % (err or out).strip()[:300]
    if not os.path.exists(signature):
        return None, "NO_SIGNATURE: %s" % out.strip()[:300]
    words = []
    for line in open(signature):
        text = line.strip()
        if text:
            words.append(int(text, 16))
    if len(words) < 2 * len(points):
        return None, "SHORT_SIGNATURE: %d words for %d points" % (len(words), len(points))
    values = []
    for index in range(len(points)):
        values.append((words[2 * index + 1] << 32) | words[2 * index])
    return values, None


# ------------------------------------------------------------------
# the points
# ------------------------------------------------------------------

def edge_values():
    seen = []

    def add(value):
        folded = value & MASK
        if folded not in seen:
            seen.append(folded)
    for base in (0, 1, 2, 3):
        add(base)
        add(-base)
    add(1 << 63)
    add((1 << 63) - 1)
    add(MASK)
    for power in range(0, 64):
        value = 1 << power
        add(value - 1)
        add(value)
        add(value + 1)
    return seen


EDGES = edge_values()


def paired_points(count, seed):
    """edge pairs first (a deterministic sample of the edge product), then
    random pairs, `count` in all."""
    generator = random.Random(seed)
    out = []
    edge_pairs = [(a, b) for a in EDGES for b in EDGES]
    generator.shuffle(edge_pairs)
    for pair in edge_pairs[:count // 2]:
        out.append(pair)
    while len(out) < count:
        out.append((generator.getrandbits(64), generator.getrandbits(64)))
    return out


def single_points(count, seed):
    generator = random.Random(seed)
    out = [(value, 0) for value in EDGES[:count]]
    while len(out) < count:
        out.append((generator.getrandbits(64), 0))
    return out


def evaluate(term, substitution):
    substituted = z3.substitute(term, *substitution)
    simplified = z3.simplify(substituted)
    if z3.is_bv_value(simplified):
        return simplified.as_long() & MASK
    # the simplifier does not fold every floating-point operation on
    # constants (fp.to_ieee_bv among them): a solver model does, the free
    # symbols left (softfloat flags) completed arbitrarily
    solver = z3.Solver()
    solver.set("timeout", 2000)
    if solver.check() != z3.sat:
        return None
    value = solver.model().eval(simplified, model_completion=True)
    if z3.is_bv_value(value):
        return value.as_long() & MASK
    return None


# ------------------------------------------------------------------
# one row, end to end
# ------------------------------------------------------------------

def label_of(word, size, work):
    """llvm-objdump's reading of the word: a display label only."""
    obj = os.path.join(work, "label.S")
    out = os.path.join(work, "label.o")
    open(obj, "w").write(".text\n.option rvc\n%s\n" % (".word 0x%08x" % word if size == 4 else ".hword 0x%04x" % word))
    rc, _o, _e = sh(["clang", "--target=riscv64-unknown-elf", "-march=" + MARCH, "-c", obj, "-o", out])
    if rc != 0:
        return "?"
    rc, text, _e = sh(["llvm-objdump", "-d", "-M", "no-aliases",
                       "--mattr=+m,+a,+f,+d,+c,+zba,+zbb,+zbs,+zicond", out])
    for line in text.splitlines():
        hit = re.match(r"^\s*[0-9a-f]+:\s+(?:(?:[0-9a-f]{2} )+|[0-9a-f]{4,8})\s*(.*)$", line)
        if hit is not None and hit.group(1).strip():
            return hit.group(1).strip()
    return "?"


def check_row(reference, lifter, name, types, assignment, points_per_row, work):
    row = {"constructor": name, "fields": [render(v) for v in assignment],
           "points": 0, "agree": 0, "disagree": 0, "unevaluated": 0,
           "examples": []}
    register_kinds = [k for k, v in zip(types, assignment) if is_register(v)]
    if len(register_kinds) > len(REGISTER_SLOTS):
        row["outcome"] = "REFUSED"
        row["cause"] = "%d register fields, more than the harness has slots" % len(register_kinds)
        return row
    instr = make_instruction(name, types, assignment, REGISTER_SLOTS)
    got, cause = word_of(lifter, instr)
    if got is None:
        row["outcome"] = "REFUSED"
        row["cause"] = "NO_WORD: %s" % cause
        return row
    word, size = got
    row["word"] = "0x%0*x" % (size * 2, word)
    row["mnem"] = label_of(word, size, work)
    roles, cause = roles_of(reference, word, size, register_kinds)
    if roles is None:
        row["outcome"] = "REFUSED"
        row["cause"] = cause
        return row
    written = roles["written"]
    reads = roles["reads"]
    if len(written) != 1:
        row["outcome"] = "REFUSED"
        row["cause"] = "%d registers written; the harness stores one" % len(written)
        return row
    if len(reads) > 2:
        row["outcome"] = "REFUSED"
        row["cause"] = "%d register inputs; the harness presents two" % len(reads)
        return row
    kind, index, term = written[0]
    row["writes"] = "%s%d" % (kind, index)
    row["reads"] = ["%s%d" % (k, i) for k, i in reads]
    # the harness: inputs arrive in a0, a1; a float input is moved into
    # the f slot, a float answer moved back to a2
    moves_in = []
    substitution = []
    inputs = []
    for slot, (rkind, rindex) in enumerate(reads[:2]):
        source = "a%d" % slot
        inputs.append((rkind, rindex))
        if rkind == "f":
            moves_in.append("fmv.d.x f%d, %s" % (rindex, source))
        elif rindex != 10 + slot:
            moves_in.append("mv x%d, %s" % (rindex, source))
    moves_out = []
    if kind == "f":
        moves_out.append("fmv.x.d a2, f%d" % index)
    elif index != 12:
        moves_out.append("mv a2, x%d" % index)
    # a read register that is also the written one must be loaded before
    # the write: the moves above run before the instruction, in order
    if len(inputs) == 2:
        points = paired_points(points_per_row, name + row["word"])
    elif len(inputs) == 1:
        points = single_points(points_per_row, name + row["word"])
    else:
        points = [(0, 0)]
    values, problem = run_word(word, size, moves_in, moves_out, points, work)
    if problem is not None:
        row["outcome"] = "REFUSED"
        row["cause"] = problem
        return row
    for pindex, (left, right) in enumerate(points):
        row["points"] = row["points"] + 1
        substitution = []
        for slot, (rkind, rindex) in enumerate(inputs):
            symbol = z3.BitVec("seed_%s%d" % (rkind, rindex), 64)
            value = left if slot == 0 else right
            substitution.append((symbol, z3.BitVecVal(value & MASK, 64)))
        ours = evaluate(term, substitution) if substitution else evaluate(term, [(z3.BitVec("seed_x0", 64), z3.BitVecVal(0, 64))])
        theirs = values[pindex]
        if ours is None:
            row["unevaluated"] = row["unevaluated"] + 1
            continue
        if ours == theirs:
            row["agree"] = row["agree"] + 1
            continue
        row["disagree"] = row["disagree"] + 1
        if len(row["examples"]) < 6:
            row["examples"].append({"first_input": "0x%016x" % (left & MASK),
                                    "second_input": "0x%016x" % (right & MASK),
                                    "our_reading": "0x%016x" % ours,
                                    "the_model": "0x%016x" % theirs})
    if row["disagree"] == 0 and row["unevaluated"] == 0:
        row["outcome"] = "AGREES_AT_EVERY_POINT"
    elif row["disagree"] == 0:
        row["outcome"] = "AGREES_WHERE_EVALUATED"
    else:
        row["outcome"] = "DISAGREES"
    return row


def is_register(value):
    return isinstance(value, str) and value == "register"


def render(value):
    if isinstance(value, LR.Ctor):
        return value.name
    if isinstance(value, dict):
        return "{" + ", ".join("%s := %s" % (k, render(v)) for k, v in sorted(value.items())) + "}"
    if is_register(value):
        return "register"
    simplified = z3.simplify(value)
    if z3.is_bool(simplified):
        return "true" if z3.is_true(simplified) else "false"
    return "0x%x" % simplified.as_long()


def main():
    out_prefix = sys.argv[1]
    work = sys.argv[2]
    points_per_row = 2000
    first = None
    args = sys.argv[3:]
    while args:
        if args[0] == "--points":
            points_per_row = int(args[1])
            args = args[2:]
            continue
        if args[0] == "--first":
            first = int(args[1])
            args = args[2:]
            continue
        raise SystemExit("unknown argument %r" % args[0])
    if not os.path.isdir(work):
        os.makedirs(work)
    os.environ["SL1_WORK"] = os.path.join(work, "lifter")
    reference = RV.RiscvReference()
    lifter = reference.lifter
    constructors = constructors_of(lifter.emit_dir)
    enums = enums_of(lifter.emit_dir)
    rows_in, refused_types = rows_of(constructors, enums)
    print("constructors %d, enums %d, rows %d, constructors refused by field type %d"
          % (len(constructors), len(enums), len(rows_in), len(refused_types)))
    if first is not None:
        rows_in = rows_in[:first]
    rows = []
    started = time.time()
    for index, (name, types, assignment) in enumerate(rows_in, 1):
        row = check_row(reference, lifter, name, types, assignment, points_per_row, work)
        row["peak_rss_mb"] = round(check_memory(name), 1)
        rows.append(row)
        print("[%d/%d] %-22s %-28s %-24s points %5d agree %5d disagree %4d  %s"
              % (index, len(rows_in), name, row.get("mnem", "-")[:28], row["outcome"],
                 row["points"], row["agree"], row["disagree"],
                 row.get("cause", "")[:230]))
        for example in row.get("examples", [])[:2]:
            print("      first=%s second=%s ours=%s model=%s" % (
                example["first_input"], example["second_input"],
                example["our_reading"], example["the_model"]))
        sys.stdout.flush()
    census = {}
    for row in rows:
        census[row["outcome"]] = census.get(row["outcome"], 0) + 1
    document = {
        "meta": {"task": "sl1",
                 "what": "every instruction the generated lifter defines, checked at points against the Sail model's own C simulator",
                 "this_is": "A CHECK AT POINTS, NOT AN EQUALITY",
                 "sail_model_commit": lifter.commit, "simulator": SIMULATOR,
                 "march": MARCH, "points_per_row": points_per_row,
                 "memory_ceiling_mb": MEMORY_CEILING_MB, "abort_name": ABORT_NAME,
                 "peak_rss_mb": round(peak_rss_mb(), 1), "seconds": round(time.time() - started, 1),
                 "census": census, "reset_report": lifter.reset_report + lifter.prologue_report},
        "rows": rows, "refused_by_field_type": refused_types}
    fh = open(out_prefix + ".json", "w")
    json.dump(document, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()
    print("rows %d, census %s, points %d, peak RSS %.1f MB (ceiling %d, abort %s), %.0f s"
          % (len(rows), census, sum(r["points"] for r in rows), peak_rss_mb(),
             MEMORY_CEILING_MB, ABORT_NAME, time.time() - started))


if __name__ == "__main__":
    main()
