#!/usr/bin/env python3
"""canon.py -- THE CANONICAL RUNNABLE FORM (ratified by the owner 2026-08-25).

What this program does
----------------------
It reads `sem_anchored_<lang>.json` -- which carries, per unit, the
anchored register map (`sem.anchor_registers`: `in0` is the memory home
of the first argument, `in1` of the second), the ship build's bytes and
its instruction text -- and rewrites each unit's instruction text into
the CANONICAL RUNNABLE FORM:

    argument a -> %rdi (%edi/%di/%dil), float %xmm0
    argument b -> %rsi (%esi/%si/%sil), float %xmm1
    result     -> %rax (%eax/%ax/%al),  float %xmm0
    temps      -> %r10, %r11

TRACED-VARIABLES-PRIORITY.  A traced value owns its designated
register.  An untraced value that sits in a designated register is
EVICTED to a temp.  Two values never share a register.  When both temps
are already taken by live untraced values, the unit is refused with
`canon_refused: temps exhausted`.  Refusal is loud and counted; it is
never silent.

Why the rewrite is per VALUE and not a flat permutation of register
names
------------------------------------------------------------------
go's calling rule puts the first argument in %rax and also returns in
%rax.  Those are TWO values in ONE register at two different times.  No
permutation of register NAMES can send %rax to %rdi (for the argument)
and to %rax (for the result) at once.  So the rewrite tracks VALUES:
each definition starts a new value, each value gets a home, and every
register mention is rewritten to the home of the value that lives there
at that point.  A flat permutation is the special case where each
register holds one value.

Pinned registers
----------------
Some encodings require a specific register: `idiv`/`div`/`mul` and
`cqto`/`cltd` use %rax and %rdx, shifts take their count in %cl.  A
value that any instruction pins keeps that register.  If a TRACED value
is pinned to a register that is not its designated one, the unit is
refused (`canon_refused: traced value pinned ...`) rather than rewritten
into something that would not run.

Control flow
------------
Units are tiny (over 90% are five instructions or fewer).  The walk is
linear over the instruction list in address order.  A unit that carries
a branch is marked `flow: "multi-block; linear walk"` so the
approximation is visible on the record rather than hidden.

THE SPELLING BAN.  No operator token takes part in any key, grouping,
pairing, candidate selection or comparison scope here.  The token is
copied once per unit, as the display label `operator` on a unit object.
Run check_no_spelling_keys.py on the output.

usage:
  canon.py [--in DIR] [--out DIR]
"""

import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))

LANGS = ["c", "cpp", "go", "rust", "swift"]

# ------------------------------------------------------------ registers

GP_NAMES = {
    "rax": ["rax", "eax", "ax", "al"],
    "rbx": ["rbx", "ebx", "bx", "bl"],
    "rcx": ["rcx", "ecx", "cx", "cl"],
    "rdx": ["rdx", "edx", "dx", "dl"],
    "rsi": ["rsi", "esi", "si", "sil"],
    "rdi": ["rdi", "edi", "di", "dil"],
    "rbp": ["rbp", "ebp", "bp", "bpl"],
    "rsp": ["rsp", "esp", "sp", "spl"],
}

for _i in range(8, 16):
    _base = "r%d" % _i
    GP_NAMES[_base] = [_base, _base + "d", _base + "w", _base + "b"]

FAMILY_OF = {}
WIDTH_OF = {}

for _fam, _names in GP_NAMES.items():
    for _w, _name in enumerate(_names):
        FAMILY_OF[_name] = _fam
        WIDTH_OF[_name] = _w

for _i in range(0, 16):
    FAMILY_OF["xmm%d" % _i] = "xmm%d" % _i
    WIDTH_OF["xmm%d" % _i] = 0
    FAMILY_OF["ymm%d" % _i] = "xmm%d" % _i
    WIDTH_OF["ymm%d" % _i] = 0

NEVER_RENAME = set(["rip", "rsp", "rbp"])

TEMPS = ["r10", "r11"]

# the ruling names %r10 and %r11, which are general-purpose registers.
# A floating-point value cannot live in one.  The two temps for values
# that live in the vector file are the two vector registers the
# canonical form does not designate.  Stated here because it is an
# EXTENSION of the ratified text, not the ratified text itself.
VECTOR_TEMPS = ["xmm2", "xmm3"]


def is_vector(family):
    return family.startswith("xmm")


def render(family, width):
    """the register NAME for this family at the width the original
    mention used."""
    if is_vector(family):
        return family
    names = GP_NAMES[family]
    return names[width]


# --------------------------------------------------------- instructions

REG = re.compile(r"%([a-z0-9]+)")

SETCC = re.compile(r"^set[a-z]+$")

CMOV = re.compile(r"^cmov[a-z]+$")

JUMP = re.compile(r"^(jmp|j[a-z]+)$")

# every operand is read; nothing is written (flags are not a value here)
USE_ONLY = set([
    "cmp", "cmpl", "cmpq", "cmpb", "cmpw",
    "test", "testl", "testq", "testb",
    "ucomiss", "ucomisd", "comiss", "comisd",
    "push", "pushq", "call", "callq", "ret", "retq",
    "nop", "nopl", "nopw", "ud2", "hlt", "leave", "cld",
])

# the last operand is written and NOT read; the others are read
DEF_LAST = set([
    "mov", "movl", "movq", "movb", "movw", "movabs", "movabsq",
    "movd", "lea", "leaq", "leal",
    "movzbl", "movzbq", "movzwl", "movzwq", "movsbl", "movsbq",
    "movswl", "movslq", "movsxd",
    "movss", "movsd", "movaps", "movapd", "movdqa", "movdqu",
    "cvtsi2ss", "cvtsi2sd", "cvtsi2ssl", "cvtsi2sdl",
    "cvtsi2ssq", "cvtsi2sdq",
    "cvtss2sd", "cvtsd2ss",
    "cvttss2si", "cvttsd2si", "cvtss2si", "cvtsd2si",
])

# the last operand is read AND written; the others are read
RMW_LAST = set([
    "add", "addl", "addq", "addb", "sub", "subl", "subq",
    "and", "andl", "andq", "andb", "or", "orl", "orq", "orb",
    "xor", "xorl", "xorq", "xorb",
    "imul", "imull", "imulq", "sbb", "adc",
    "shl", "shll", "shlq", "shr", "shrl", "shrq",
    "sar", "sarl", "sarq", "rol", "ror",
    "addss", "addsd", "subss", "subsd", "mulss", "mulsd",
    "divss", "divsd", "minss", "minsd", "maxss", "maxsd",
    "sqrtss", "sqrtsd",
    "xorps", "xorpd", "orps", "orpd", "andps", "andpd",
    "andnps", "andnpd", "pxor", "por", "pand",
    "punpckldq", "punpcklqdq", "unpckhpd", "unpcklpd",
    "unpckhps", "unpcklps",
    "subpd", "subps", "addpd", "addps", "mulpd", "mulps",
    "cmpeqss", "cmpeqsd", "cmpneqss", "cmpneqsd",
    "cmpltss", "cmpltsd", "cmpless", "cmplesd",
    "cmpunordss", "cmpunordsd", "cmpordss", "cmpordsd",
])

# one operand, read and written
UNARY_RMW = set([
    "not", "notl", "notq", "neg", "negl", "negq",
    "inc", "incl", "incq", "dec", "decl", "decq",
    "bswap",
])

# these pin %rax and %rdx by the encoding
PIN_AX_DX = set([
    "idiv", "idivl", "idivq", "idivb",
    "div", "divl", "divq",
    "mul", "mull", "mulq",
    "cqto", "cltd", "cwtl", "cltq", "cqo",
])


class Refusal(Exception):

    def __init__(self, reason):
        Exception.__init__(self, reason)
        self.reason = reason


def split_operands(text):
    """split an AT&T operand list on top-level commas."""
    out = []
    depth = 0
    cur = ""
    for ch in text:
        if ch == "(":
            depth = depth + 1
        if ch == ")":
            depth = depth - 1
        if ch == "," and depth == 0:
            out.append(cur.strip())
            cur = ""
            continue
        cur = cur + ch
    if cur.strip():
        out.append(cur.strip())
    return out


def parse(line):
    """-> (mnemonic, [operand text, ...]).  A trailing objdump comment
    (`jo 7 <op_12+0x7>`) is not an operand list we rewrite; the branch
    target is kept verbatim."""
    text = line.strip()
    parts = text.split(None, 1)
    mnem = parts[0]
    if len(parts) == 1:
        return mnem, []
    rest = parts[1]
    hashed = rest.find("#")
    if hashed >= 0:
        rest = rest[:hashed]
    return mnem, split_operands(rest.strip())


def registers_in(operand):
    """every register NAME mentioned by one operand, in order."""
    return REG.findall(operand)


def is_plain_register(operand):
    if not operand.startswith("%"):
        return False
    if "(" in operand:
        return False
    return True


# ------------------------------------------------------------- the walk

class Value(object):

    def __init__(self, vid, tag, family, born):
        self.vid = vid
        self.tag = tag
        self.family = family
        self.first = born
        self.last = born
        self.pinned = None
        self.pinned_by = None
        self.home = None
        self.modified = False

    def touch(self, index):
        if index > self.last:
            self.last = index


class Walk(object):
    """one unit's value-by-value reading of its own instruction text."""

    def __init__(self, mnem_lines, anchor, result_family):
        self.lines = mnem_lines
        self.anchor = anchor
        self.result_family = result_family
        self.values = []
        self.live = {}
        self.next_id = 0
        self.branches = False
        self.role_log = {}

    def fresh(self, tag, family, index):
        v = Value(self.next_id, tag, family, index)
        self.next_id = self.next_id + 1
        self.values.append(v)
        self.live[family] = v
        return v

    def occupant(self, family, index):
        """the value living in this register right now.  A register read
        before anything defined it, and that the anchor did not name, is
        an incoming value we did not trace."""
        if family in self.live:
            v = self.live[family]
            v.touch(index)
            return v
        return self.fresh("incoming", family, index)

    def start(self):
        first = self.anchor.get("in0")
        second = self.anchor.get("in1")
        if first is not None:
            fam = FAMILY_OF.get(first)
            if fam is None:
                raise Refusal("canon_refused: the anchor names a register "
                              "this builder does not know (%s)" % first)
            self.fresh("a", fam, -1)
        if second is not None:
            fam = FAMILY_OF.get(second)
            if fam is None:
                raise Refusal("canon_refused: the anchor names a register "
                              "this builder does not know (%s)" % second)
            self.fresh("b", fam, -1)

    def run(self):
        self.start()
        for index, line in enumerate(self.lines):
            self.one(index, line)
        self.name_the_result()
        return self.values

    def pin(self, family, index, mnem):
        v = self.occupant(family, index)
        v.pinned = family
        v.pinned_by = mnem
        return v

    def one(self, index, line):
        mnem, operands = parse(line)
        bare = mnem
        if JUMP.match(bare):
            self.branches = True
        if bare in PIN_AX_DX:
            self.pin("rax", index, bare)
            self.pin("rdx", index, bare)
            # rax and rdx are redefined by the division itself
            self.redefine("rax", index, bare)
            self.redefine("rdx", index, bare)
        role = self.roles(bare, operands)
        role = self.settle(role, operands)
        self.role_log[index] = role
        for slot, kind in enumerate(role):
            operand = operands[slot]
            names = registers_in(operand)
            for name in names:
                fam = FAMILY_OF.get(name)
                if fam is None:
                    continue
                if name in NEVER_RENAME:
                    continue
                if fam in NEVER_RENAME:
                    continue
                if kind == "def" and is_plain_register(operand):
                    continue
                held = self.occupant(fam, index)
                if kind == "rw" and is_plain_register(operand):
                    held.modified = True
            if bare in ("shl", "shr", "sar", "shll", "shrl", "shrq",
                        "sarl", "sarq", "shlq", "rol", "ror"):
                if operand == "%cl":
                    self.pin("rcx", index, bare)
        written = []
        for slot, kind in enumerate(role):
            if kind != "def":
                continue
            operand = operands[slot]
            if not is_plain_register(operand):
                continue
            name = registers_in(operand)[0]
            fam = FAMILY_OF.get(name)
            if fam is None:
                continue
            if fam in NEVER_RENAME:
                continue
            if fam in written:
                continue
            written.append(fam)
            self.redefine(fam, index, bare)

    def redefine(self, family, index, mnem):
        v = self.fresh("temp", family, index)
        if mnem in PIN_AX_DX:
            v.pinned = family
            v.pinned_by = mnem
        return v

    def settle(self, roles, operands):
        """an 8-bit or 16-bit write leaves the rest of the register
        alone, so it does not always start a new value.  `setl %al`
        after `xor %eax,%eax` finishes the value the xor started.  The
        same `setl %al` over an argument that arrived in %rax (go's
        calling rule) DOES start a new value: an argument being
        partially overwritten is an argument that is dead there.  So a
        partial write continues the value in place unless that value is
        a traced argument.  A 32-bit write zero-extends and always
        starts a new value."""
        out = list(roles)
        for slot, kind in enumerate(out):
            if kind != "def":
                continue
            operand = operands[slot]
            if not is_plain_register(operand):
                continue
            names = registers_in(operand)
            if not names:
                continue
            width = WIDTH_OF.get(names[0])
            if width is None:
                continue
            if width < 2:
                continue
            fam = FAMILY_OF[names[0]]
            sitting = self.live.get(fam)
            if sitting is None:
                continue
            if sitting.tag == "a":
                continue
            if sitting.tag == "b":
                continue
            out[slot] = "rw"
        return out

    def roles(self, mnem, operands):
        """per operand: "use", "def", or "rw"."""
        count = len(operands)
        out = []
        for _i in range(count):
            out.append("use")
        if count == 0:
            return out
        if mnem in USE_ONLY:
            return out
        if JUMP.match(mnem):
            return out
        if SETCC.match(mnem):
            out[count - 1] = "def"
            return out
        if mnem in ("pop", "popq"):
            out[count - 1] = "def"
            return out
        if mnem in UNARY_RMW:
            out[count - 1] = "rw"
            return out
        if mnem in PIN_AX_DX:
            return out
        if CMOV.match(mnem):
            out[count - 1] = "rw"
            return out
        if mnem in DEF_LAST:
            out[count - 1] = "def"
            return out
        if mnem in RMW_LAST:
            if self.self_zeroing(mnem, operands):
                # both mentions name the destination, so both must be
                # rewritten to the destination's home
                out[0] = "def"
                out[count - 1] = "def"
                return out
            out[count - 1] = "rw"
            return out
        raise Refusal("canon_refused: this builder has no read/write "
                      "model for the instruction `%s`" % mnem)

    def self_zeroing(self, mnem, operands):
        """`xor %eax,%eax` and its vector cousins produce a constant;
        the old contents of the register are not read."""
        zeroers = ("xor", "xorl", "xorq", "xorb", "xorps", "xorpd",
                   "pxor")
        if mnem not in zeroers:
            return False
        if len(operands) != 2:
            return False
        if operands[0] != operands[1]:
            return False
        return True

    def a_is_vector(self):
        for v in self.values:
            if v.tag != "a":
                continue
            return is_vector(v.family)
        return False

    def name_the_result(self):
        """the value the unit hands back.  All five calling rules here
        return an integer in %rax and a floating-point number in %xmm0.
        WHICH of the two applies is read off the unit's own code rather
        than guessed from the operand types: the return register is the
        one of the two that holds a value the unit itself computed, and
        when both do, the one computed last.  A unit that hands back an
        argument untouched (`ret` alone) names no separate result."""
        best = None
        for fam in ("rax", "xmm0"):
            v = self.live.get(fam)
            if v is None:
                continue
            if v.tag in ("a", "b") and v.modified:
                # the unit changed an argument where it lay and handed
                # that register back.  Harmless when the argument's
                # designated register IS the result's -- a float
                # argument and a float result both live in %xmm0.  When
                # the two differ (go hands its first argument in %rax
                # and returns in %rax), the canonical form would need
                # the argument and the result in different registers,
                # and one read-and-write operand cannot name two.  A
                # rename alone cannot express that unit.
                mine = designated(v.tag, v.family, self.a_is_vector())
                theirs = designated("result", v.family, False)
                if mine == theirs:
                    continue
                raise Refusal("canon_refused: the unit modifies an "
                              "argument in place and returns it, which "
                              "a rename cannot express (the argument's "
                              "register %%%s is not the result's %%%s)"
                              % (mine, theirs))
            if v.tag == "a":
                continue
            if v.tag == "b":
                continue
            if v.first < 0:
                continue
            if best is None:
                best = v
                continue
            if v.first > best.first:
                best = v
        if best is None:
            return None
        best.tag = "result"
        self.result_family = best.family
        return best


# ------------------------------------------------------------ the homes

def designated(tag, family, a_is_vector):
    """the canonical home of a traced value.

    The ruling reads a -> %rdi (%xmm0 for floating point), b -> %rsi
    (%xmm1).  That is the both-arguments-in-one-register-file case.  The
    ruling also says the C calling rule is what was promoted to canon,
    and under that rule the register files are counted SEPARATELY: in
    `(int a, float b)` the float argument is the first floating-point
    argument and so takes %xmm0, not %xmm1.  So b takes %xmm1 only when
    a is also a floating-point value; otherwise b takes %xmm0.  For
    two integers, and for two floats, this is exactly the ruling's
    text."""
    if tag == "a":
        if is_vector(family):
            return "xmm0"
        return "rdi"
    if tag == "b":
        if is_vector(family):
            if a_is_vector:
                return "xmm1"
            return "xmm0"
        if a_is_vector:
            return "rdi"
        return "rsi"
    if tag == "result":
        if is_vector(family):
            return "xmm0"
        return "rax"
    return None


def overlaps(one, other):
    """do the two values need to be in different registers?

    The comparison is STRICT at the touching point: one instruction may
    read the last use of one value and write the first definition of the
    next in the same register (`idiv %esi` reads the dividend in %rax
    and writes the quotient there).  That is a handover, not two values
    alive at once."""
    if one.last <= other.first:
        return False
    if other.last <= one.first:
        return False
    return True


def assign_homes(values):
    """traced values take their designated register.  Every other value
    is evicted to a temp, and a temp is reused only when the two live
    ranges do not overlap."""
    evictions = []
    traced = []
    untraced = []
    a_is_vector = False
    for v in values:
        if v.tag != "a":
            continue
        a_is_vector = is_vector(v.family)
    for v in values:
        want = designated(v.tag, v.family, a_is_vector)
        if want is None:
            untraced.append(v)
            continue
        traced.append((v, want))
    for v, want in traced:
        if v.pinned is not None and v.pinned != want:
            raise Refusal("canon_refused: a traced value is pinned to "
                          "%%%s by `%s`, but its designated register is "
                          "%%%s" % (v.pinned, v.pinned_by, want))
        v.home = want
    claimed = []
    for v, want in traced:
        if want not in claimed:
            claimed.append(want)
    for v in untraced:
        if v.pinned is not None:
            v.home = v.pinned
            continue
        if v.family not in claimed:
            # nothing traced owns this register, so there is nothing to
            # evict it for; it stays where the compiler put it
            v.home = v.family
            continue
        v.home = None
    for v in untraced:
        if v.home is not None:
            continue
        chosen = None
        bench = TEMPS
        if is_vector(v.family):
            bench = VECTOR_TEMPS
        for temp in bench:
            clash = False
            for other in values:
                if other is v:
                    continue
                if other.home != temp:
                    continue
                if overlaps(v, other):
                    clash = True
                    break
            if clash:
                continue
            chosen = temp
            break
        if chosen is None:
            raise Refusal("canon_refused: temps exhausted")
        v.evicted_from = v.family
        v.home = chosen
        if v.family != chosen:
            note = {}
            note["value"] = v.vid
            note["occupied"] = v.family
            note["moved_to"] = chosen
            note["why"] = "an untraced value sat in a register the "\
                          "canonical form designates for a traced "\
                          "value or for another temp; traced variables "\
                          "have priority, so it was evicted"
            evictions.append(note)
    check_no_sharing(values)
    return evictions


def check_no_sharing(values):
    """two values never share a register.  Two values pinned to the same
    register by the encoding (the quotient and the dividend copy both
    live in %rax) are the one case the architecture forces; they are
    allowed only when their live ranges do not overlap."""
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            one = values[i]
            other = values[j]
            if one.home != other.home:
                continue
            if not overlaps(one, other):
                continue
            if one.pinned == one.home and other.pinned == other.home:
                # the encoding, not this builder, put them there
                continue
            raise Refusal("canon_refused: two values would share %%%s "
                          "over the same range" % one.home)


# --------------------------------------------------------- the rewrite

def rewrite(lines, values, role_log):
    """replay the walk, this time writing each register mention as the
    home of the value that lives there."""
    live = {}
    order = {}
    for v in values:
        if v.tag == "a":
            live[v.family] = v
        if v.tag == "b":
            live[v.family] = v
    pending = []
    for v in values:
        if v.first < 0:
            continue
        pending.append(v)
    out = []
    for index, line in enumerate(lines):
        mnem, operands = parse(line)
        role = role_log[index]
        pieces = []
        for slot, operand in enumerate(operands):
            kind = role[slot]
            defines = kind == "def" and is_plain_register(operand)
            pieces.append(swap(operand, live, defines, index, pending,
                               values))
        for slot, operand in enumerate(operands):
            if role[slot] != "def" and role[slot] != "rw":
                continue
            if not is_plain_register(operand):
                continue
            name = registers_in(operand)[0]
            fam = FAMILY_OF.get(name)
            if fam is None:
                continue
            if fam in NEVER_RENAME:
                continue
            if role[slot] == "rw":
                continue
            born = take(pending, fam, index)
            if born is not None:
                live[fam] = born
        if mnem in PIN_AX_DX:
            for fam in ("rax", "rdx"):
                born = take(pending, fam, index)
                if born is not None:
                    live[fam] = born
        if pieces:
            out.append("%s %s" % (mnem, ",".join(pieces)))
        else:
            out.append(mnem)
    return out


def take(pending, family, index):
    """the value this instruction defined in this register."""
    for v in pending:
        if v.family != family:
            continue
        if v.first != index:
            continue
        pending.remove(v)
        return v
    return None


def swap(operand, live, defines, index, pending, values):
    """rewrite every register mention in one operand."""
    text = operand
    out = ""
    i = 0
    while i < len(text):
        if text[i] != "%":
            out = out + text[i]
            i = i + 1
            continue
        j = i + 1
        while j < len(text) and text[j].isalnum():
            j = j + 1
        name = text[i + 1:j]
        out = out + "%" + swap_one(name, live, defines, index, pending,
                                   values)
        i = j
    return out


def swap_one(name, live, defines, index, pending, values):
    fam = FAMILY_OF.get(name)
    if fam is None:
        return name
    if name in NEVER_RENAME:
        return name
    if fam in NEVER_RENAME:
        return name
    width = WIDTH_OF[name]
    if defines:
        target = None
        for v in pending:
            if v.family != fam:
                continue
            if v.first != index:
                continue
            target = v
            break
        if target is None:
            target = live.get(fam)
        if target is None:
            return name
        return render(target.home, width)
    v = live.get(fam)
    if v is None:
        return name
    return render(v.home, width)


# ------------------------------------------------------------- per unit

def result_register_family(lang, meta, mnem_lines):
    """the register the calling rule hands the answer back in.  All five
    languages here return integers in %rax and floating point in %xmm0;
    which one applies is read off the unit's recorded result type where
    the language states one, and off the operand types where it does
    not."""
    rt = meta.get("result_type")
    if rt is not None:
        low = str(rt).lower()
        if "float" in low or "double" in low:
            return "xmm0"
        if low in ("f32", "f64"):
            return "xmm0"
        return "rax"
    lhs = meta.get("lhs_rep")
    if lhs in ("f32", "f64"):
        return "xmm0"
    return "rax"


def canon_one(lang, n, rec):
    sem = rec.get("sem", {})
    anchor = sem.get("anchor_registers")
    lines = rec.get("mnem")
    meta = rec.get("meta", {})
    out = {}
    out["lang"] = lang
    out["n"] = n
    out["unit"] = "%s/op_%s" % (lang, n)
    out["operator"] = meta.get("operator")
    out["meta"] = meta
    out["anchor_registers"] = anchor
    out["mnem"] = lines
    out["bytes"] = rec.get("bytes")
    if anchor is None:
        out["canon_ok"] = False
        out["canon_refused"] = "canon_refused: the unit carries no "\
                               "anchored register map"
        return out
    if not lines:
        out["canon_ok"] = False
        out["canon_refused"] = "canon_refused: the unit carries no "\
                               "instruction text"
        return out
    fam = result_register_family(lang, meta, lines)
    out["result_register"] = fam
    try:
        walker = Walk(lines, anchor, fam)
        values = walker.run()
        evictions = assign_homes(values)
        text = rewrite(lines, values, walker.role_log)
    except Refusal as bad:
        out["canon_ok"] = False
        out["canon_refused"] = bad.reason
        return out
    if walker.branches and text != list(lines):
        # the walk names values in address order.  Inside one block that
        # is the execution order; across blocks it is not, so a rename
        # that CHANGES a branching unit could move a value the other
        # path depends on.  Refuse rather than emit something that might
        # not run.
        out["canon_ok"] = False
        out["canon_refused"] = "canon_refused: the unit branches, and "\
                               "this builder's linear walk cannot name "\
                               "values across blocks"
        return out
    out["canon_ok"] = True
    out["canon_mnem"] = text
    out["canon_text"] = "; ".join(text)
    out["already_canonical"] = text == list(lines)
    out["multi_block"] = walker.branches
    out["flow"] = "single block"
    if walker.branches:
        out["flow"] = "multi-block; linear walk"
    out["rename_map"] = rename_map(values)
    out["evictions"] = evictions
    out["value_count"] = len(values)
    return out


def rename_map(values):
    out = []
    for v in values:
        rec = {}
        rec["value"] = v.vid
        rec["role"] = v.tag
        rec["was"] = v.family
        rec["now"] = v.home
        rec["pinned_by_encoding"] = v.pinned
        rec["first_seen_at"] = v.first
        rec["last_seen_at"] = v.last
        out.append(rec)
    return out


# ------------------------------------------------------------- the pass

def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def run_language(lang, indir, outdir, every):
    path = os.path.join(indir, "sem_anchored_%s.json" % lang)
    doc = json.load(open(path))
    units = doc["units"]
    keys = sorted(units.keys(), key=lambda x: int(x))
    rows = {}
    ok = 0
    refused = 0
    evicted = 0
    already = 0
    reasons = {}
    done = 0
    for n in keys:
        rec = canon_one(lang, n, units[n])
        rows[n] = rec
        if rec["canon_ok"]:
            ok = ok + 1
            if rec["evictions"]:
                evicted = evicted + 1
            if rec["already_canonical"]:
                already = already + 1
        else:
            refused = refused + 1
            why = rec["canon_refused"]
            reasons[why] = reasons.get(why, 0) + 1
        done = done + 1
        if done % every == 0:
            log("  %s: [%d/%d] units canonicalised" % (lang, done,
                                                     len(keys)))
    log("  %s: [%d/%d] units canonicalised" % (lang, done, len(keys)))
    out = {}
    out["language"] = lang
    out["form"] = "a -> %rdi (%xmm0 for floating point), b -> %rsi "\
                  "(%xmm1), result -> %rax (%xmm0), temps -> %r10, %r11"
    out["priority"] = "traced variables have priority: an untraced "\
                      "occupant of a designated register is evicted to "\
                      "a temp; two values never share a register; both "\
                      "temps taken is a loud refusal"
    out["spelling"] = "the operator token appears once per unit, as the "\
                      "display label `operator` on a unit object."
    out["units_read"] = len(keys)
    out["canonical"] = ok
    out["refused"] = refused
    out["refusal_reasons"] = reasons
    out["units_with_an_eviction"] = evicted
    out["units_unchanged_by_the_rename"] = already
    out["units"] = rows
    name = os.path.join(outdir, "canon_units_%s.json" % lang)
    fh = open(name, "w")
    json.dump(out, fh, indent=1)
    fh.close()
    log("wrote %s (%d canonical, %d refused, %d with an eviction, "
        "%d unchanged)" % (name, ok, refused, evicted, already))
    return out


def main(argv):
    indir = HERE
    outdir = HERE
    every = 200
    i = 1
    while i < len(argv):
        if argv[i] == "--in":
            indir = argv[i + 1]
            i = i + 2
            continue
        if argv[i] == "--out":
            outdir = argv[i + 1]
            i = i + 2
            continue
        if argv[i] == "--every":
            every = int(argv[i + 1])
            i = i + 2
            continue
        print(__doc__)
        return 2
    started = time.time()
    log("the canonical runnable form")
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    for lang in LANGS:
        run_language(lang, indir, outdir, every)
    log("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
