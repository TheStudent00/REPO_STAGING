#!/usr/bin/env python3
"""entry_contract3.py -- TASK 31: the entry contract with THREE SEATS.

WHAT CHANGED, in one sentence: the entry contract used to name two
seats (`a`, `b`) plus a result register; it now names an ordered list
of SEATS, one of which may carry the designation "result-destination",
and the anchoring layer knows that when that seat is occupied the
integer seats of `a` and `b` SHIFT ONE PLACE TO THE RIGHT.

DEE'S RULING THIS ROUND, the authority for this file
(log_115_claude_code_task_briefs_round6.md, "DEE'S RULINGS THIS
SESSION"):

  "THE ENTRY CONTRACT GAINS A RESULT-DESTINATION SEAT. The
   struct-return units anchor with %rdi designated "result
   destination"; a/b shift to their designated seats. This also
   begins relaxing the fixed-arity ceiling the owner has objected to."

WHY THE OLD ANCHORING LAYER GOT THESE UNITS WRONG. `sem_anchored.py`'s
`argument_registers(lang, reps)` walks the parameter list and hands
out ABI seats from index 0:

    SYSV_INT = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
    ...
    ni = 0
    for rep in reps:
        ...
        out.append(ints[ni]); ni += 1

Nothing in that walk knows about the hidden pointer the System V
convention inserts BEFORE the declared parameters when the answer is
returned in memory. So for rust/op_786 it answered `a -> %rdi,
b -> %rsi`, and the record `canon4_units_rust.json` carries says
exactly that. The unit's own ship text says otherwise:

    mov %rdi,%rax ; mov %esi,(%rdi) ; mov %edx,0x4(%rdi) ;
    movb $0x0,0x8(%rdi) ; ret

%rdi is a destination address that gets stored THROUGH, never read as
data; the two values written into the image arrive in %rsi and %rdx.
canon4's erasure then read %rdx, which its own contract never named,
and refused "value w0 is read before it is defined".

THE DETECTION IS MACHINE FORM, NOT A TYPE NAME AND NOT A TOKEN. A
unit is anchored with a result-destination seat when its OWN SHIP
TEXT satisfies all four tests below, and for no other reason:

  1. every store in the unit writes through ONE base register B;
  2. B is never written by any instruction of the unit (so its value
     arrived from outside);
  3. some instruction copies B into the answer register (%rax);
  4. B is never read as data -- it appears only as a store base and
     as the source of that copy.

No operator token, no `result_type` string, no source expression takes
part in the test. THE SPELLING BAN applies here as everywhere: the
token is a display label on the member, never a selector.

WHAT THIS FILE DOES NOT DO. It does not touch `sem_anchored.py`,
`canon4.py`, or any recorded artifact. It is a new module; the driver
`canon32_sret.py` uses it, and the existing pipeline is unchanged.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

Coding discipline: no complex/compound one-liner statements.
"""

import re


class NotAnchorable(Exception):
    """raised by name whenever the evidence does not force an answer.
    Never a guess, never a default."""
    pass


# ---------------------------------------------------------------
# the ABI seat lists -- copied by value from sem_anchored.py so this
# module reads no mutable state of another file, and quoted here so a
# reader can see exactly what is assumed.
# ---------------------------------------------------------------

SYSV_INT = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
SYSV_SSE = ["xmm0", "xmm1", "xmm2", "xmm3",
            "xmm4", "xmm5", "xmm6", "xmm7"]

GO_INT = ["rax", "rbx", "rcx", "rdi", "rsi", "r8", "r9", "r10", "r11"]
GO_SSE = ["xmm%d" % k for k in range(15)]

ABI = {
    "c": ("sysv", SYSV_INT, SYSV_SSE),
    "cpp": ("sysv", SYSV_INT, SYSV_SSE),
    "rust": ("sysv", SYSV_INT, SYSV_SSE),
    "swift": ("sysv", SYSV_INT, SYSV_SSE),
    "go": ("goabi", GO_INT, GO_SSE),
}

FLOAT_REPS = set(["f32", "f64", "float", "double", "float32",
                  "float64", "Float", "Double"])

# the register the System V convention returns the destination
# address in, and the register the canonical form calls the answer
# home. They are the same register, which is exactly why an sret unit
# looks like "the answer never entered a tracked register".
ANSWER_REGISTER = "rax"

RAX_FAMILY = set(["rax", "eax", "ax", "al", "ah"])


# ---------------------------------------------------------------
# reading the ship text
# ---------------------------------------------------------------

STORE_RE = re.compile(
    r"^(mov|movb|movw|movl|movq|movss|movsd)\s+"
    r"(\S+),(?:(-?0x[0-9a-f]+))?\(%(r[a-z0-9]+)\)$")

COPY_TO_ANSWER_RE = re.compile(r"^mov\s+%(r[a-z0-9]+),%rax$")

# a general "what does this instruction write" reader, used only to
# answer test 2 (was B ever written?) and test 4 (was B ever read as
# data?). Deliberately conservative: an instruction this table does
# not recognise makes the unit UNANCHORABLE by name rather than
# silently passing the tests.
KNOWN_SHAPES = set(["mov", "movb", "movw", "movl", "movq",
                    "movss", "movsd", "ret"])

WIDTH_OF_REGISTER = {}
for _name in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp",
              "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]:
    WIDTH_OF_REGISTER[_name] = 64
for _name in ["eax", "ebx", "ecx", "edx", "esi", "edi", "ebp", "esp",
              "r8d", "r9d", "r10d", "r11d", "r12d", "r13d", "r14d",
              "r15d"]:
    WIDTH_OF_REGISTER[_name] = 32
for _name in ["ax", "bx", "cx", "dx", "si", "di", "bp", "sp",
              "r8w", "r9w", "r10w", "r11w"]:
    WIDTH_OF_REGISTER[_name] = 16
for _name in ["al", "bl", "cl", "dl", "sil", "dil", "bpl", "spl",
              "r8b", "r9b", "r10b", "r11b"]:
    WIDTH_OF_REGISTER[_name] = 8
for _k in range(16):
    WIDTH_OF_REGISTER["xmm%d" % _k] = 128

FAMILY_OF_REGISTER = {}
_FAMILIES = [
    ("rax", ["rax", "eax", "ax", "al"]),
    ("rbx", ["rbx", "ebx", "bx", "bl"]),
    ("rcx", ["rcx", "ecx", "cx", "cl"]),
    ("rdx", ["rdx", "edx", "dx", "dl"]),
    ("rsi", ["rsi", "esi", "si", "sil"]),
    ("rdi", ["rdi", "edi", "di", "dil"]),
    ("rbp", ["rbp", "ebp", "bp", "bpl"]),
    ("rsp", ["rsp", "esp", "sp", "spl"]),
]
for _k in range(8, 16):
    _FAMILIES.append(("r%d" % _k,
                      ["r%d" % _k, "r%dd" % _k, "r%dw" % _k,
                       "r%db" % _k]))
for _k in range(16):
    _FAMILIES.append(("xmm%d" % _k, ["xmm%d" % _k]))
for _fam, _members in _FAMILIES:
    for _m in _members:
        FAMILY_OF_REGISTER[_m] = _fam


WIDTH_OF_STORE_MNEM = {
    "movb": 8,
    "movw": 16,
    "movl": 32,
    "movq": 64,
    "movss": 32,
    "movsd": 64,
}


def clean(line):
    text = line.strip()
    if "!!" in text:
        text = text.split("!!", 1)[0].strip()
    return text


def store_width(mnem, source_operand):
    """the number of bits one store writes, read off the instruction's
    own spelling: the mnemonic suffix when it carries one, otherwise
    the width of the source register."""
    if mnem in WIDTH_OF_STORE_MNEM:
        return WIDTH_OF_STORE_MNEM[mnem]
    if source_operand.startswith("%"):
        name = source_operand[1:]
        width = WIDTH_OF_REGISTER.get(name)
        if width is None:
            raise NotAnchorable(
                "store source %r is a register spelling this module "
                "has no width for" % source_operand)
        return width
    raise NotAnchorable(
        "store `%s %s` states no width -- neither a mnemonic suffix "
        "nor a source register" % (mnem, source_operand))


def read_stores(mnem_lines):
    """[{offset, width_bits, source, base, text}] in text order."""
    out = []
    for raw in mnem_lines:
        text = clean(raw)
        m = STORE_RE.match(text)
        if m is None:
            continue
        mnem = m.group(1)
        source = m.group(2)
        offset_text = m.group(3)
        base = m.group(4)
        if offset_text is None:
            offset = 0
        else:
            offset = int(offset_text, 16)
        out.append({
            "offset": offset,
            "width_bits": store_width(mnem, source),
            "source": source,
            "base": base,
            "mnem": mnem,
            "text": text,
        })
    return out


def registers_written(mnem_lines):
    """the set of register FAMILIES any instruction of this text
    writes. Refuses by name on an instruction shape this module does
    not recognise, so a silent pass is impossible."""
    written = set()
    for raw in mnem_lines:
        text = clean(raw)
        if text == "":
            continue
        parts = text.split(" ", 1)
        mnem = parts[0]
        if mnem not in KNOWN_SHAPES:
            raise NotAnchorable(
                "instruction %r is outside this module's recognised "
                "shapes %r -- the unit is not anchored rather than "
                "guessed at" % (text, sorted(KNOWN_SHAPES)))
        if mnem == "ret":
            continue
        rest = parts[1]
        operands = rest.split(",")
        destination = operands[-1].strip()
        if not destination.startswith("%"):
            continue
        name = destination[1:]
        family = FAMILY_OF_REGISTER.get(name)
        if family is None:
            raise NotAnchorable(
                "destination register %r has no family in this "
                "module's table" % destination)
        written.add(family)
    return written


def base_read_as_data(mnem_lines, base):
    """True when the base register is read as a VALUE somewhere other
    than as a store base or as the source of the copy into the answer
    register. A destination pointer that is also read as data is not
    a plain destination pointer, and this module refuses it."""
    marker = "%" + base
    for raw in mnem_lines:
        text = clean(raw)
        if text == "":
            continue
        if COPY_TO_ANSWER_RE.match(text) is not None:
            continue
        m = STORE_RE.match(text)
        if m is not None:
            if m.group(4) == base:
                if marker not in m.group(2):
                    continue
            return True
        if marker in text:
            return True
    return False


def detect_memory_return(mnem_lines):
    """(True, evidence) when the four machine-form tests all hold;
    (False, reason) otherwise. `evidence` carries the destination
    register, the stores, and the copy instruction."""
    stores = read_stores(mnem_lines)
    if not stores:
        return False, {"test": "t1-no-store",
                       "reason": "test 1 fails: the unit contains no "
                                 "store through a register base"}
    bases = set()
    for s in stores:
        bases.add(s["base"])
    if len(bases) != 1:
        return False, {"test": "t1-many-bases",
                       "reason": "test 1 fails: the unit's stores use "
                                 "%d different base registers %r, not "
                                 "one" % (len(bases), sorted(bases))}
    base = sorted(bases)[0]
    if base in ("rsp", "rbp"):
        return False, {"test": "t1-own-frame",
                       "reason": "test 1 fails: the store base is the "
                                 "stack pointer or frame pointer "
                                 "%%%s, which is this unit's own "
                                 "frame, not a caller-provided "
                                 "destination" % base}
    written = registers_written(mnem_lines)
    family = FAMILY_OF_REGISTER.get(base)
    if family in written:
        return False, {"test": "t2-base-written",
                       "reason": "test 2 fails: the store base %%%s is "
                                 "WRITTEN by this unit, so its value "
                                 "did not arrive from outside (the go "
                                 "runtime.newobject shape is this "
                                 "case)" % base}
    copy_line = None
    for raw in mnem_lines:
        text = clean(raw)
        m = COPY_TO_ANSWER_RE.match(text)
        if m is None:
            continue
        if m.group(1) != base:
            continue
        copy_line = text
    if copy_line is None:
        return False, {"test": "t3-no-copy-to-answer",
                       "reason": "test 3 fails: no instruction copies "
                                 "the store base %%%s into the answer "
                                 "register %%rax" % base}
    if base_read_as_data(mnem_lines, base):
        return False, {"test": "t4-base-read-as-data",
                       "reason": "test 4 fails: the store base %%%s is "
                                 "read as a data value somewhere, so "
                                 "it is not a plain destination "
                                 "pointer" % base}
    return True, {
        "destination_register": base,
        "stores": stores,
        "exit_copy": copy_line,
    }


# ---------------------------------------------------------------
# the seats
# ---------------------------------------------------------------

def seat_list(lang, lhs_rep, rhs_rep, has_result_destination):
    """the ordered seats of the entry contract.

    THE DISPLACED ABI, stated as a rule: when a result-destination
    seat is present it takes the FIRST INTEGER SEAT, and every
    declared integer parameter shifts one place to the right. Floating
    parameters are unaffected, because the destination pointer is an
    integer-class argument and consumes an integer seat only."""
    if lang not in ABI:
        raise NotAnchorable(
            "language %r has no ABI seat list in this module" % lang)
    _family, ints, sses = ABI[lang]
    seats = []
    next_int = 0
    next_sse = 0
    if has_result_destination:
        seats.append({
            "designation": "result-destination",
            "register": ints[next_int],
            "class": "integer",
            "role": "the address of the caller-allocated answer "
                    "image; stored through, never read as data",
        })
        next_int = next_int + 1
    designations = ["a", "b"]
    reps = [lhs_rep, rhs_rep]
    for k, rep in enumerate(reps):
        if rep is None:
            continue
        if rep in FLOAT_REPS:
            if next_sse >= len(sses):
                raise NotAnchorable(
                    "the floating seat list is exhausted")
            seats.append({
                "designation": designations[k],
                "register": sses[next_sse],
                "class": "float",
            })
            next_sse = next_sse + 1
            continue
        if next_int >= len(ints):
            raise NotAnchorable("the integer seat list is exhausted")
        seats.append({
            "designation": designations[k],
            "register": ints[next_int],
            "class": "integer",
        })
        next_int = next_int + 1
    return seats


def build_contract(lang, meta, mnem_lines):
    """the three-seat entry contract for one unit, plus the exit
    contract the memory-return convention forces.

    Returns (contract, evidence). Raises NotAnchorable by name when
    the evidence does not force an answer."""
    is_sret, evidence = detect_memory_return(mnem_lines)
    lhs_rep = meta.get("lhs_rep")
    rhs_rep = None
    if meta.get("arity") == "binary":
        rhs_rep = meta.get("rhs_rep")
    seats = seat_list(lang, lhs_rep, rhs_rep, is_sret)
    if not is_sret:
        contract = {
            "abi": "sysv" if lang != "go" else "goabi",
            "displaced": False,
            "seats": seats,
            "exit": {
                "answer": "a value in the answer register",
                "register": ANSWER_REGISTER,
            },
        }
        return contract, evidence
    fields = []
    for s in evidence["stores"]:
        fields.append({
            "offset": s["offset"],
            "width_bits": s["width_bits"],
        })
    last = evidence["stores"][-1]
    image_bytes = 0
    for s in evidence["stores"]:
        end = s["offset"] + s["width_bits"] // 8
        if end > image_bytes:
            image_bytes = end
    contract = {
        "abi": "sysv-displaced",
        "displaced": True,
        "seats": seats,
        "exit": {
            "answer": "the %d-byte image at the result destination"
                      % image_bytes,
            "image_bytes": image_bytes,
            "fields": fields,
            "register": ANSWER_REGISTER,
            "register_holds": "the result destination address, "
                              "returned unchanged",
        },
    }
    del last
    return contract, evidence


def seat_of(contract, designation):
    for s in contract["seats"]:
        if s["designation"] == designation:
            return s
    return None


def designation_of_register(contract, register_name):
    """the designation whose seat is the FAMILY of `register_name`, or
    None. `register_name` is spelled without the leading %."""
    family = FAMILY_OF_REGISTER.get(register_name)
    if family is None:
        return None
    for s in contract["seats"]:
        if s["register"] == family:
            return s["designation"]
    return None
