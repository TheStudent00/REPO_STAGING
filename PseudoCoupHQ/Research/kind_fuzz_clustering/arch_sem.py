#!/usr/bin/env python3
"""arch_sem.py -- the `sem` column: a DERIVED semantic reading of an
arch-unit's machine bytes.

`bytes` and `mnem` are raw and are never touched, here or anywhere.
`canon` strips three fixed layout facts off a COPY of them.  `sem` goes
one level further down and asks a different question entirely: not
"what did the compiler write" but "what does what it wrote COMPUTE".

Why a lifter and not a table
----------------------------
Two compilers asked for the same operation on the same two machine
words will not agree at the byte level, and usually will not agree at
the mnemonic level either, for two reasons that have nothing to do with
the operation:

  INSTRUCTION SELECTION.  `lea (%rdi,%rsi,1),%eax` and `add %ebx,%eax`
  are the same addition.  One of them also sets the flags, and where
  nothing reads the flags that is not a difference in what was
  computed.

  REGISTER ALLOCATION.  The C convention hands arguments in %rdi and
  %rsi; go's register ABI hands them in %rax and %rbx.  Which physical
  register a value sits in is a fact about the calling convention, not
  about the operator.

A hand-written table of equivalent instruction pairs would answer both,
badly: it would have to be extended for every new pattern, and every
entry in it would be a judgement this file made rather than a fact the
machine bytes state.  Instead the bytes are LIFTED into VEX -- libVEX's
intermediate representation, reached through pyvex, the same lifter
angr uses -- and the comparison is made on the lifted form.  VEX states
what each instruction does to the machine's state as a small pure
dataflow, so both differences above become ordinary algebra.

What survives the normalization, and what must
----------------------------------------------
The whole risk of this file is over-reach.  A normalization aggressive
enough to make everything equal is worse than none, so the three things
that are genuinely different STAY different, by construction:

  a TRAP.  swift's `imul; jo; ud2` overflow check ends in an
  undecodable byte pair.  It is recorded as a `trap` event and nothing
  removes it.

  a GUARD BRANCH.  rust's `/` tests the divisor and jumps to
  `panic_const_div_by_zero`.  The branch is recorded as a `branch`
  event carrying its CONDITION as a lifted expression, and the panic
  path's call is recorded as a `call` event carrying the callee's name.
  c++'s bare `idiv` has neither.

  a CALL to a runtime function.  The callee's name comes from `canon`,
  which already resolved it out of the relocation or the symbol
  annotation, and it is carried verbatim.

Only two classes of thing are deliberately erased, and each has a stated
rule below: the IDENTITY of a physical register, and a value that
nothing in the unit goes on to use.

The pipeline
------------
    stripped instructions   <- arch_read's own three normalizations
    per-instruction lift    <- pyvex, one instruction at a time
    symbolic sweep          <- an interpreter over VEX statements
    algebraic normalization <- a fixpoint of standard identities
    register anonymization  <- by canonical traversal order
    serialization           <- one deterministic string, `sem.key`

usage:
  arch_sem.py <lang> [<lang> ...]      add `sem` to arch_units_<lang>.json
  arch_sem.py --selfcheck              the guard tests, run and printed
"""

import argparse
import json
import logging
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import arch_read as AR                                       # noqa: E402

logging.getLogger("pyvex").setLevel(logging.CRITICAL)
import archinfo                                              # noqa: E402
import pyvex                                                 # noqa: E402

ARCH = archinfo.ArchAMD64()
LIFTER_ID = "pyvex %s / archinfo %s / libVEX via ArchAMD64" % (
    getattr(pyvex, "__version__", "?"), getattr(archinfo, "__version__", "?"))


# ===================================================== the guest state map
#
# VEX addresses the guest state by byte offset.  A 32-bit read of %eax
# is a 4-byte read at rax's own offset, and a partial write of %al is a
# 1-byte write there.  The table below turns an (offset, size) pair back
# into "which architectural register, at which bit within it", so that
# sub-register access is modelled as extraction and insertion rather
# than as access to some separate location that would not alias.

_BASES = sorted((r.vex_offset, r.size, r.name)
                for r in ARCH.register_list
                if r.vex_offset is not None)

# Registers that hold a value the operator produced or consumed.  The
# rest -- VEX's lazy condition-code slots, the instruction pointer, the
# direction flag, the x87 and SSE control words -- are machinery.
PSEUDO = {"cc_op", "cc_dep1", "cc_dep2", "cc_ndep", "rip", "d", "ac", "id",
          "fs_const", "gs_const", "sseround", "ftop", "fptag", "fpround",
          "fc3210", "emnote", "cmstart", "cmlen", "nraddr", "sc_class",
          "ip_at_syscall", "tistart", "tilen"}

# Named leaves.  The stack pointer and the instruction pointer are NOT
# anonymized with the rest: both calling conventions use %rsp for the
# same structural purpose, and a unit that addresses through the stack
# is saying something about the stack, not about which register the ABI
# picked for an argument.
FIXED_LEAF = {"rsp": "SP", "rip": "PC"}


def _locate(offset, size):
    """(base register name, bit offset within it, base width in bits)."""
    for off, sz, name in _BASES:
        if off <= offset and offset + size <= off + sz:
            return name, (offset - off) * 8, sz * 8
    return "guest_%d" % offset, 0, size * 8


TYPE_BITS = {}


def _bits(ty):
    if ty not in TYPE_BITS:
        TYPE_BITS[ty] = pyvex.const.get_type_size(ty)
    return TYPE_BITS[ty]


# ============================================================ expressions
#
# A value is an immutable tuple whose first element is its kind and
# whose second is its width in bits.  Nothing here is a class: tuples
# hash and compare structurally, which is the whole point -- two
# separately lifted instruction streams that compute the same thing
# produce the same tuple.
#
#   ('c',   w, value)              a constant
#   ('r',   w, name)               a register's value on entry
#   ('ex',  w, lo, x)              w bits of x starting at bit lo
#   ('zx',  w, x) / ('sx', w, x)   widened, zero- or sign-filled
#   ('ins', w, old, val, lo)       old with val written in at bit lo
#   ('b',   w, op, a, b)           a VEX binary operation
#   ('u',   w, op, a)              unary
#   ('t',   w, op, a, b, c)        ternary (rounded floating point)
#   ('q',   w, op, a, b, c, d)     quaternary
#   ('ite', w, cond, then, else)
#   ('ld',  w, gen, addr)          a load from memory generation `gen`
#   ('cc',  w, name, args tuple)   a VEX helper call: a pure function
#   ('op',  w, tag)                opaque -- a value this file refuses
#                                  to claim it knows

def W(e):
    return e[1]


def const(w, v):
    return ("c", w, v & ((1 << w) - 1))


# ---- the algebraic rules ------------------------------------------------
#
# Every rule below is an identity that holds for every input, stated in
# one line.  None of them is specific to an instruction, an operator or
# a language.

# Operations congruent modulo any power of two, so that truncating the
# result is the same as truncating the operands.  This is the single
# rule that makes an addition selected as `lea` compare equal to an
# addition selected as `add`: `lea` computes the full 64-bit sum and
# keeps 32 bits of it, `add` computes a 32-bit sum, and pushing the
# truncation down through the sum turns the first into the second.
CONGRUENT = re.compile(r"^(Add|Sub|Mul|And|Or|Xor|Not)\d+$")

# Commutative, so operand order is not information.  Restricted to the
# integer operations on purpose: IEEE addition and multiplication are
# commutative in value but this file does not want to assert anything
# about NaN payload propagation, and nothing here needs it.
COMMUTATIVE = re.compile(r"^(Add|Mul|And|Or|Xor|CmpEQ|CmpNE)\d+$"
                         r"|^(And|Or|Xor)V\d+$")

FOLDABLE = {
    "Add": lambda w, a, b: a + b,
    "Sub": lambda w, a, b: a - b,
    "Mul": lambda w, a, b: a * b,
    "And": lambda w, a, b: a & b,
    "Or": lambda w, a, b: a | b,
    "Xor": lambda w, a, b: a ^ b,
    "Shl": lambda w, a, b: a << b if b < w else 0,
    "Shr": lambda w, a, b: a >> b if b < w else 0,
    "CmpEQ": lambda w, a, b: int(a == b),
    "CmpNE": lambda w, a, b: int(a != b),
}
BINWIDTH = re.compile(r"^([A-Za-z]+)(\d+)$")


def _fold_bin(w, op, a, b):
    m = BINWIDTH.match(op)
    if not m or m.group(1) not in FOLDABLE:
        return None
    if a[0] != "c" or b[0] != "c":
        return None
    return const(w, FOLDABLE[m.group(1)](int(m.group(2)), a[2], b[2]))


def mk_ex(w, lo, x):
    """w bits of x at bit lo, normalized."""
    if lo == 0 and W(x) == w:
        return x
    if x[0] == "c":
        return const(w, x[2] >> lo)
    if x[0] == "ex":                      # extract of an extract
        return mk_ex(w, lo + x[2], x[3])
    if lo == 0:
        if x[0] in ("zx", "sx"):
            inner = x[2]
            if W(inner) >= w:
                return mk_ex(w, 0, inner)
            # widening then truncating shorter still widens
            return mk_zx(w, inner) if x[0] == "zx" else mk_sx(w, inner)
        if x[0] == "ins":
            old, val, ilo = x[2], x[3], x[4]
            if ilo == 0 and W(val) >= w:
                return mk_ex(w, 0, val)
            if ilo >= w:
                return mk_ex(w, 0, old)
        if x[0] == "b" and CONGRUENT.match(x[2]):
            head = BINWIDTH.match(x[2]).group(1)
            return mk_bin("%s%d" % (head, w), mk_ex(w, 0, x[3]),
                          mk_ex(w, 0, x[4]))
        if x[0] == "u" and CONGRUENT.match(x[2]):
            head = BINWIDTH.match(x[2]).group(1)
            return mk_un("%s%d" % (head, w), mk_ex(w, 0, x[3]))
        if x[0] == "ite":
            return ("ite", w, x[2], mk_ex(w, 0, x[3]), mk_ex(w, 0, x[4]))
    return ("ex", w, lo, x)


def mk_zx(w, x):
    if W(x) == w:
        return x
    if x[0] == "c":
        return const(w, x[2])
    if x[0] == "zx":
        return mk_zx(w, x[2])
    return ("zx", w, x)


def mk_sx(w, x):
    if W(x) == w:
        return x
    if x[0] == "c":
        v = x[2]
        if v >> (W(x) - 1):
            v |= ~((1 << W(x)) - 1)
        return const(w, v)
    return ("sx", w, x)


def mk_ins(old, val, lo):
    """old with val written into it at bit lo."""
    w = W(old)
    if lo == 0 and W(val) == w:
        return val
    if old[0] == "ins" and old[4] == lo and W(old[3]) == W(val):
        old = old[2]                       # an overwritten insert is dead
    return ("ins", w, old, val, lo)


def mk_un(op, a):
    w = _un_width(op, a)
    if a[0] == "c":
        m = BINWIDTH.match(op)
        if m and m.group(1) == "Not":
            return const(w, ~a[2])
    return ("u", w, op, a)


WIDTH_UNOP = re.compile(r"^V?(\d+)(HIto|Uto|Sto|to|UtoV|StoV)V?(\d+)$")


def _width_unop(op, a):
    """RULE.  VEX spells width changes as ordinary unary operators --
    `64to32`, `32Uto64`, `64HIto32`.  They are not operations the
    program performed; they are how one value is read out of another,
    and keeping them as opaque operators would block every algebraic
    rule below them.  Each becomes the extraction or the widening it
    IS, so that `64to32(Add64(x,y))` can become `Add32` of the truncated
    operands -- which is the identity that makes an addition selected as
    `lea` equal to an addition selected as `add`."""
    m = WIDTH_UNOP.match(op)
    if not m:
        return mk_un(op, a)
    src, how, dst = int(m.group(1)), m.group(2), int(m.group(3))
    if how == "HIto":
        return mk_ex(dst, src - dst, a)
    if how == "to":
        return mk_ex(dst, 0, a) if dst <= src else mk_zx(dst, a)
    if how in ("Uto", "UtoV"):
        return mk_zx(dst, a) if dst >= src else mk_ex(dst, 0, a)
    return mk_sx(dst, a) if dst >= src else mk_ex(dst, 0, a)


def _un_width(op, a):
    m = re.match(r"^(\d+)(?:Uto|Sto|HIto|to)(\d+)$", op)
    if m:
        return int(m.group(2))
    m = re.match(r"^(\d+)UtoV(\d+)$", op)
    if m:
        return int(m.group(2))
    m = BINWIDTH.match(op)
    if m:
        return int(m.group(2))
    return W(a)


def mk_bin(op, a, b):
    w = _bin_width(op, a, b)
    folded = _fold_bin(w, op, a, b)
    if folded is not None:
        return folded
    m = BINWIDTH.match(op)
    head = m.group(1) if m else op
    if head in ("And", "Or") and a == b:
        return a
    if head == "Xor" and a == b:
        return const(w, 0)
    if head == "Sub" and a == b:
        return const(w, 0)
    if head in ("Add", "Or", "Xor", "Sub") and b[0] == "c" and b[2] == 0:
        return a
    if head in ("Add", "Or", "Xor") and a[0] == "c" and a[2] == 0:
        return b
    if COMMUTATIVE.match(op) and _key(b) < _key(a):
        a, b = b, a
    return ("b", w, op, a, b)


def _bin_width(op, a, b):
    if op.startswith("Cmp") and not op.startswith("CmpF"):
        return 1
    if op == "CmpF64":
        return 32
    m = re.match(r"^(\d+)HLto(\d+)$", op)
    if m:
        return int(m.group(2))
    m = re.match(r"^(\d+)HLtoV(\d+)$", op)
    if m:
        return int(m.group(2))
    m = BINWIDTH.match(op)
    if m and not op.startswith("Cmp"):
        return int(m.group(2)) if m.group(1) not in ("Sh",) else W(a)
    return W(a)


# ---- serialization, and the name-blind key ------------------------------

def _ser(e, names):
    """the canonical text of an expression.  `names` maps a physical
    register to the token that stands for it; a register absent from
    the map is rendered `REG`, which is what makes the key NAME-BLIND
    and is how commutative operands are ordered without their order
    depending on which registers the ABI happened to choose."""
    k = e[0]
    if k == "c":
        return "%d:%d" % (e[2], e[1])
    if k == "r":
        return "%s:%d" % (names.get(e[2], "REG"), e[1])
    if k == "ex":
        return "ex%d@%d(%s)" % (e[1], e[2], _ser(e[3], names))
    if k in ("zx", "sx"):
        return "%s%d(%s)" % (k, e[1], _ser(e[2], names))
    if k == "ins":
        return "ins@%d(%s,%s)" % (e[4], _ser(e[2], names), _ser(e[3], names))
    if k == "b":
        return "%s(%s,%s)" % (e[2], _ser(e[3], names), _ser(e[4], names))
    if k == "u":
        return "%s(%s)" % (e[2], _ser(e[3], names))
    if k in ("t", "q"):
        return "%s(%s)" % (e[2], ",".join(_ser(x, names) for x in e[3:]))
    if k == "ite":
        return "ite(%s,%s,%s)" % (_ser(e[2], names), _ser(e[3], names),
                                  _ser(e[4], names))
    if k == "ld":
        return "ld%d/g%d(%s)" % (e[1], e[2], _ser(e[3], names))
    if k == "cc":
        return "%s(%s)" % (e[2], ",".join(_ser(x, names) for x in e[3]))
    if k == "op":
        return "opaque[%s]:%d" % (e[2], e[1])
    raise KeyError(k)


_KEYCACHE = {}


def _key(e):
    """the name-blind key, memoized -- these trees are shared heavily."""
    v = _KEYCACHE.get(e)
    if v is None:
        v = _ser(e, {})
        _KEYCACHE[e] = v
    return v


_KIDS = {"ex": (3,), "zx": (2,), "sx": (2,), "ins": (2, 3), "b": (3, 4),
         "u": (3,), "ite": (2, 3, 4), "ld": (3,)}


def _kids(e):
    k = e[0]
    if k in _KIDS:
        return [e[i] for i in _KIDS[k]]
    if k in ("t", "q"):
        return list(e[3:])
    if k == "cc":
        return list(e[3])
    return []


def _leaves(e, out):
    """physical register names, in canonical traversal order."""
    if e[0] == "r":
        if e[2] not in out:
            out.append(e[2])
        return
    for x in _kids(e):
        _leaves(x, out)


# ============================================== the symbolic sweep itself

RIPREL = re.compile(r"\(%rip\)")
CALLTXT = re.compile(r"^call\s+(\S.*)$")
JMPTXT = re.compile(r"^(j[a-z]+|loop[a-z]*)\s+(\S+)$")


class State(object):
    """the machine's state as this file understands it.  Everything not
    understood becomes an opaque value with a tag, never a guess."""

    def __init__(self):
        self.reg = {}                      # base register name -> value
        self.written = set()
        self.stores = []                   # (addr, width, value) live
        self.gen = 0                       # memory generation
        self.events = []
        self.tmp = {}
        self.opaques = 0

    def entry(self, name, w):
        return ("r", w, name)

    def get(self, offset, size):
        name, lo, bw = _locate(offset, size)
        cur = self.reg.get(name) or self.entry(name, bw)
        return mk_ex(size * 8, lo, cur)

    def put(self, offset, val):
        name, lo, bw = _locate(offset, W(val) // 8 or 1)
        cur = self.reg.get(name) or self.entry(name, bw)
        self.reg[name] = mk_ins(cur, val, lo)
        self.written.add(name)

    def fresh(self, w, tag):
        self.opaques += 1
        return ("op", w, tag)

    def load(self, w, addr):
        for a, aw, v in reversed(self.stores):
            if a == addr and aw == w:
                return v
            if a == addr:
                break
        return ("ld", w, self.gen, addr)

    def store(self, addr, val):
        self.stores = [s for s in self.stores if s[0] != addr]
        self.stores.append((addr, W(val), val))


def _expr(e, st):
    """one VEX expression, evaluated into a value tuple."""
    if isinstance(e, pyvex.expr.Const):
        if isinstance(e.con.value, float):
            return st.fresh(_bits(e.con.type), "float_const")
        return const(_bits(e.con.type), e.con.value)
    if isinstance(e, pyvex.expr.RdTmp):
        return st.tmp.get(e.tmp) or st.fresh(64, "tmp")
    if isinstance(e, pyvex.expr.Get):
        return st.get(e.offset, _bits(e.ty) // 8 or 1)
    if isinstance(e, pyvex.expr.Load):
        return st.load(_bits(e.ty), _expr(e.addr, st))
    if isinstance(e, pyvex.expr.Unop):
        return _width_unop(e.op[4:], _expr(e.args[0], st))
    if isinstance(e, pyvex.expr.Binop):
        return mk_bin(e.op[4:], _expr(e.args[0], st), _expr(e.args[1], st))
    if isinstance(e, pyvex.expr.Triop):
        a = tuple(_expr(x, st) for x in e.args)
        return ("t", W(a[1]), e.op[4:]) + a
    if isinstance(e, pyvex.expr.Qop):
        a = tuple(_expr(x, st) for x in e.args)
        return ("q", W(a[1]), e.op[4:]) + a
    if isinstance(e, pyvex.expr.ITE):
        c = _expr(e.cond, st)
        t, f = _expr(e.iftrue, st), _expr(e.iffalse, st)
        if c[0] == "c":
            return t if c[2] else f
        if t == f:
            return t
        return ("ite", W(t), c, t, f)
    if isinstance(e, pyvex.expr.CCall):
        return ("cc", _bits(e.retty), e.cee.name,
                tuple(_expr(x, st) for x in e.args))
    return st.fresh(64, "expr:%s" % type(e).__name__)


TERMINATOR = re.compile(r"^(jmp|j[a-z]+|loop[a-z]*|ret|ud2)\b")


def blocks_of(insns, texts, addr_index):
    """RULE.  A unit is cut into straight-line blocks before anything is
    swept.  A block ends after a jump, a branch, a return or a trap; a
    block begins at instruction zero and at every instruction some
    branch inside the unit can land on.  A call does NOT end a block:
    it returns to the next instruction.

    This exists because a rust `/` and a go `<<` both put their panic
    path AFTER the return, at the end of the unit.  Swept as one
    straight line, that trailing call would clobber every register and
    erase the value the operator actually computed -- the tail would
    eat the answer.  Blocks keep the paths apart, so the branch, the
    computation and the panic each get recorded where they happen."""
    starts = {0}
    for k, ins in enumerate(insns):
        text = texts[k] if k < len(texts) else ins["text"]
        j = JMPTXT.match(text)
        if TERMINATOR.match(text):
            if k + 1 < len(insns):
                starts.add(k + 1)
        if j:
            m = re.match(r"^\.([+-])0x([0-9a-f]+)$", j.group(2))
            if m:
                d = int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
                t = addr_index.get(ins["addr"] + d)
                if t is not None:
                    starts.add(t)
    cuts = sorted(starts)
    out, index = [], {}
    for b, s in enumerate(cuts):
        e = cuts[b + 1] if b + 1 < len(cuts) else len(insns)
        for k in range(s, e):
            index[k] = b
        out.append((s, e))
    return out, index


def _sweep(insns, texts, addr_index, block_index, lo, hi):
    """sweep ONE block, from a state in which every register holds the
    value it holds on entry to that block.

    A control transfer is not followed.  It is RECORDED as an event, so
    a guard branch, a trap and a call each leave a mark that no later
    normalization can remove.  This is a summary of the unit, not an
    execution of it, and it is one because the question being asked is
    whether two compilers produced the same unit -- not what the unit
    returns for some input."""
    st = State()
    for k in range(lo, hi):
        ins = insns[k]
        text = texts[k] if k < len(texts) else ins["text"]
        b = bytes(int(x, 16) for x in ins["bytes"])
        try:
            irsb = pyvex.lift(b, ins["addr"], ARCH, opt_level=1, max_inst=1,
                              cross_insn_opt=False)
        except Exception:
            st.events.append(("undecoded", text.split()[0]))
            st.reg = {}
            st.written.add("*")
            continue
        if irsb.jumpkind == "Ijk_NoDecode":
            # ud2 and friends.  swift's overflow check ends here and the
            # whole point of `sem` is that this is not erasable.
            st.events.append(("trap", text.split()[0]))
            continue
        st.tmp = {}
        guard = None
        for s in irsb.statements:
            if isinstance(s, (pyvex.stmt.IMark, pyvex.stmt.AbiHint,
                              pyvex.stmt.MBE, pyvex.stmt.NoOp)):
                continue
            if isinstance(s, pyvex.stmt.WrTmp):
                st.tmp[s.tmp] = _expr(s.data, st)
            elif isinstance(s, pyvex.stmt.Put):
                name, _lo, _bw = _locate(s.offset, 1)
                if name == "rip":
                    continue               # the sweep owns control flow
                st.put(s.offset, _expr(s.data, st))
            elif isinstance(s, pyvex.stmt.Store):
                st.store(_expr(s.addr, st), _expr(s.data, st))
            elif isinstance(s, pyvex.stmt.Exit):
                guard = _expr(s.guard, st)
            else:
                # CAS, LLSC, Dirty, PutI, LoadG, StoreG: not modelled.
                # Every register becomes opaque rather than stale.
                st.events.append(("unmodelled", type(s).__name__))
                st.reg = {}
                st.written.add("*")
        # ------- control flow, read off the canonical text -------------
        c = CALLTXT.match(text)
        j = JMPTXT.match(text)
        if RIPREL.search(text):
            st.events.append(("riprel", text.split()[0]))
        if c:
            st.events.append(("call", c.group(1).split()[0]))
            st.gen += 1
            st.stores = []
            tag = "call%d" % len([e for e in st.events if e[0] == "call"])
            for name in list(st.reg) + ["rax"]:
                if name not in FIXED_LEAF:
                    st.reg[name] = ("op", W(st.reg.get(name)
                                            or st.entry(name, 64)), tag)
            st.written.add("rax")
        elif j:
            head, tgt = j.group(1), j.group(2)
            where = "EXT"
            m = re.match(r"^\.([+-])0x([0-9a-f]+)$", tgt)
            if m:
                d = int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
                t = addr_index.get(ins["addr"] + d)
                where = "EXT" if t is None else "B%d" % block_index[t]
            elif not re.match(r"^(ADDR|.*\(%rip\))$", tgt):
                where = tgt
            if head == "jmp":
                st.events.append(("jmp", where))
            else:
                st.events.append(("branch", head, where, guard))
        elif irsb.jumpkind == "Ijk_Ret":
            st.events.append(("ret",))
    return st


# =========================================================== the summary

def _riprel_mask(e):
    """RULE.  A `%rip`-relative address is a link-time layout slot.
    `canon` already replaces the displacement with a placeholder in the
    mnemonic; the same fact has to be erased from the lifted value, or
    two identical operations linked at two addresses would disagree on
    a constant nobody chose.  Any expression rooted at the instruction
    pointer collapses to one opaque token."""
    if e[0] == "r" and e[2] == "rip":
        return ("op", e[1], "riprel")
    if e[0] == "b" and e[3][0] == "r" and e[3][2] == "rip":
        return ("op", e[1], "riprel")
    if e[0] == "b" and e[4][0] == "r" and e[4][2] == "rip":
        return ("op", e[1], "riprel")
    return e


def _map(e, f):
    e = f(e)
    k = e[0]
    if k in ("c", "r", "op"):
        return e
    if k == "ex":
        return ("ex", e[1], e[2], _map(e[3], f))
    if k in ("zx", "sx"):
        return (k, e[1], _map(e[2], f))
    if k == "ins":
        return ("ins", e[1], _map(e[2], f), _map(e[3], f), e[4])
    if k == "b":
        return ("b", e[1], e[2], _map(e[3], f), _map(e[4], f))
    if k == "u":
        return ("u", e[1], e[2], _map(e[3], f))
    if k in ("t", "q"):
        return (k, e[1], e[2]) + tuple(_map(x, f) for x in e[3:])
    if k == "ite":
        return ("ite", e[1], _map(e[2], f), _map(e[3], f), _map(e[4], f))
    if k == "ld":
        return ("ld", e[1], e[2], _map(e[3], f))
    if k == "cc":
        return ("cc", e[1], e[2], tuple(_map(x, f) for x in e[3]))
    raise KeyError(k)


def _subexprs(e, out):
    out.add(e)
    k = e[0]
    if k in ("c", "r", "op"):
        return
    kids = {"ex": (3,), "zx": (2,), "sx": (2,), "ins": (2, 3), "b": (3, 4),
            "u": (3,), "ite": (2, 3, 4), "ld": (3,)}.get(k)
    if kids:
        for i in kids:
            _subexprs(e[i], out)
    elif k in ("t", "q"):
        for x in e[3:]:
            _subexprs(x, out)
    elif k == "cc":
        for x in e[3]:
            _subexprs(x, out)


def _frame_private(addr):
    """RULE.  A store whose address is a CONSTANT offset below the stack
    pointer as it stood on entry names memory this call created and
    this call destroys.  It is a spill slot; the caller cannot observe
    it, and which values a compiler chose to spill is register
    allocation by another name.  Nothing above entry %rsp is touched --
    that is the caller's, and a write there would be a real effect."""
    if addr[0] == "r" and addr[2] == "rsp":
        return True
    if addr[0] != "b" or addr[4][0] != "c":
        return False
    if addr[3][0] != "r" or addr[3][2] != "rsp":
        return False
    c = addr[4][2]
    signed = c - (1 << W(addr[4])) if c >> (W(addr[4]) - 1) else c
    if addr[2].startswith("Add"):
        return signed < 0
    if addr[2].startswith("Sub"):
        return signed > 0
    return False


def _untouched_slice(v, name):
    """RULE.  `setne %al` writes one byte of %rax and leaves the other
    seven holding whatever the caller left there.  The rule that drops a
    register whose final value is its entry value says nothing happened
    to it; the same rule applied to a PART of a register says nothing
    happened to that part.  So an insertion whose background is the
    register's own entry value is reduced to the slice that was
    actually written.  Only a slice sitting at bit zero is reduced: a
    write to %ah sits at bit eight and that offset is information, so
    such a value is left exactly as it stands rather than quietly
    slid down to zero."""
    while v[0] == "ins" and v[4] == 0 \
            and v[2][0] == "r" and v[2][2] == name:
        v = v[3]
    return v


def summarize(st):
    """the comparable form.  Three parts, each with its own rule.

    VALUES.  For every register the unit wrote, its final value, unless
    (a) the register is one of VEX's condition-code slots or another
    piece of machinery -- a flag nobody reads is not a computation, and
    a flag somebody DOES read appears inside that reader's condition
    instead, so nothing is lost; (b) the final value is the value the
    register already held on entry, so nothing happened; (c) the
    expression is a proper subexpression of another surviving value, so
    it is an intermediate a different register allocator would have
    kept somewhere else or nowhere; or (d) the register is %rsp, whose
    movement is the call protocol rather than the operation -- a `push`
    to realign before a call, a `ret` popping the return address.  %rsp
    is still a leaf everywhere it is USED, so a stack address is never
    mistaken for an argument; only its final value is not an answer.

    STORES.  Every surviving store except a spill into this call's own
    frame.

    EVENTS.  Every call, branch, unconditional jump, trap and return,
    in address order, untouched."""
    vals = []
    for name in sorted(st.written):
        if name in PSEUDO or name == "*" or name == "rsp":
            continue
        v = st.reg.get(name)
        if v is None:
            continue
        if v[0] == "r" and v[2] == name:
            continue
        v = _untouched_slice(v, name)
        vals.append(_map(v, _riprel_mask))
    sub = set()
    for v in vals:
        s = set()
        _subexprs(v, s)
        sub |= (s - {v})
    vals = [v for v in vals if v not in sub]

    stores = [(_map(a, _riprel_mask), w, _map(v, _riprel_mask))
              for a, w, v in st.stores if not _frame_private(a)]

    events = []
    for ev in st.events:
        if ev[0] == "branch":
            g = ev[3]
            events.append(("branch", ev[1], ev[2],
                           _map(g, _riprel_mask) if g else None))
        else:
            events.append(ev)
    return vals, stores, events


def render(summaries):
    """anonymize the registers across the WHOLE unit, then write every
    block down once, in address order.

    The naming is global, not per block: a register that carries a value
    from one block into the next is the same `inK` in both, so the fact
    that they are the same register survives even though its name does
    not.

    RULE.  A physical register's NAME is a fact about the calling
    convention.  %rdi and %rsi carry the C convention's first two
    arguments; %rax and %rbx carry go's.  Two units that read their two
    operands and add them are the same unit whichever pair they read
    from, so a register is named by WHEN IT IS FIRST MET in a traversal
    whose own order was fixed without looking at any register name --
    `in0`, `in1`, and so on.

    Position is kept, identity is dropped.  A subtraction's minuend
    stays the minuend, because the traversal reaches the left operand
    of a non-commutative operation first.  What is NOT kept is any way
    to tell `a - b` from `b - a` in the abstract; within this campaign
    every unit is the source expression `a op b`, so the two never both
    occur, but the limitation is real and is stated rather than hidden.

    %rsp and %rip are exempt: both conventions use them for the same
    structural purpose and anonymizing them would let a stack address
    pass for an argument."""
    ordered = []
    for b, (vals, stores, events) in enumerate(summaries):
        vals = sorted(vals, key=_key)
        stores = sorted(stores, key=lambda s: (_key(s[0]), s[1], _key(s[2])))
        ordered.append((vals, stores, events))
    order = []
    for vals, stores, events in ordered:
        for v in vals:
            _leaves(v, order)
        for a, _w, v in stores:
            _leaves(a, order)
            _leaves(v, order)
        for ev in events:
            if ev[0] == "branch" and ev[3] is not None:
                _leaves(ev[3], order)
    names, n = dict(FIXED_LEAF), 0
    for r in order:
        if r not in names:
            names[r] = "in%d" % n
            n += 1
    out = []
    for b, (vals, stores, events) in enumerate(ordered):
        v = [_ser(x, names) for x in vals]
        s = ["st%d(%s)=%s" % (w, _ser(a, names), _ser(x, names))
             for a, w, x in stores]
        e = []
        for ev in events:
            if ev[0] == "branch":
                e.append("branch %s %s [%s]"
                         % (ev[1], ev[2],
                            _ser(ev[3], names) if ev[3] else "?"))
            else:
                e.append(" ".join(str(x) for x in ev))
        out.append(dict(block=b, values=v, stores=s, events=e,
                        text="B%d V[%s] S[%s] E[%s]"
                             % (b, " ".join(v), " ".join(s), " | ".join(e))))
    return out


def semantics(rec):
    """the `sem` column for one raw record, or None when the record
    cannot support one."""
    insns = AR.instructions(rec)
    if insns is None:
        return None
    insns, _endbr = AR.strip_entry_endbr64(insns)
    insns, _go, unmatched = AR.strip_go_stack_growth(insns)
    texts, _masked = AR.normalize_addresses(insns)
    index = dict((ins["addr"], k) for k, ins in enumerate(insns))
    spans, block_index = blocks_of(insns, texts, index)
    summaries = []
    for lo, hi in spans:
        st = _sweep(insns, texts, index, block_index, lo, hi)
        summaries.append(summarize(st))
    parts = render(summaries)
    key = "  ".join(p["text"] for p in parts)
    values = [x for p in parts for x in p["values"]]
    stores = [x for p in parts for x in p["stores"]]
    events = [x for p in parts for x in p["events"]]
    return dict(blocks=parts, values=values, stores=stores, events=events,
                key=key,
                inputs=len(set(re.findall(r"\bin\d+\b", key))),
                instructions=len(insns), block_count=len(parts),
                go_stack_growth_unmatched=unmatched)


# ================================================================== drive

def annotate(lang, verbose=True):
    path = os.path.join(HERE, "arch_units_%s.json" % lang)
    if not os.path.exists(path):
        print("!! no %s" % path)
        return None
    doc = json.load(open(path))
    keys, failed = Counter(), 0
    for n, u in doc["units"].items():
        if u.get("state") != "OK":
            continue
        try:
            sem = semantics(u)
        except Exception as exc:                        # noqa: BLE001
            sem = None
            failed += 1
            u["sem_error"] = "%s: %s" % (type(exc).__name__, exc)
        if sem is None:
            continue
        u["sem"] = sem
        keys[sem["key"]] += 1
    doc["distinct_sem_keys"] = len(keys)
    doc["sem_lifter"] = LIFTER_ID
    doc["sem_failures"] = failed
    json.dump(doc, open(path, "w"), indent=1)
    if verbose:
        print("== %s: %d OK units, %d distinct sem keys, %d lift failures"
              % (lang, doc["ok"], len(keys), failed))
        print("   canon distinct instruction texts %d"
              % doc["distinct_canonical_instruction_texts"])
    return doc


# ---------------------------------------------------------- guard tests

SELFCHECK = [
    ("lea (%rdi,%rsi,1),%eax  vs  add %ebx,%eax", "EQ",
     [("8d 04 37", "lea (%rdi,%rsi,1),%eax"), ("c3", "ret")],
     [("01 d8", "add %ebx,%eax"), ("c3", "ret")]),
    ("lea (%rdi,%rsi,1),%rax  vs  add %rbx,%rax", "EQ",
     [("48 8d 04 37", "lea (%rdi,%rsi,1),%rax"), ("c3", "ret")],
     [("48 01 d8", "add %rbx,%rax"), ("c3", "ret")]),
    ("add   vs   sub", "NE",
     [("01 d8", "add %ebx,%eax"), ("c3", "ret")],
     [("29 d8", "sub %ebx,%eax"), ("c3", "ret")]),
    ("imul alone  vs  imul + jo + ud2", "NE",
     [("0f af c3", "imul %ebx,%eax"), ("c3", "ret")],
     [("0f af c3", "imul %ebx,%eax"), ("70 01", "jo .+0x3"),
      ("c3", "ret"), ("0f 0b", "ud2")]),
]


# The guard tests above are hand-built byte sequences, which proves the
# rules but not that they behave on the campaign's own records.  These
# are read out of the folded files and are the real thing.  Each names a
# difference that MUST survive `sem`, and says why.
CORPUS_GUARDS = [
    ("rust checked `/` vs cpp bare `/` on i64",
     ("rust", "54"), ("cpp", "392"), "NE",
     "rust tests the divisor for zero and for the INT_MIN/-1 overflow "
     "and calls panic_const_div_by_zero; cpp emits the bare idiv"),
    ("rust checked `/` vs cpp bare `/` on i32",
     ("rust", "29"), ("cpp", "236"), "NE",
     "same guard, 32 bits wide"),
    ("go guarded `<<` vs cpp bare `<<` on i32",
     ("go", "52"), ("cpp", "247"), "NE",
     "go defines a shift wider than the operand as zero and panics on a "
     "negative count; cpp lets the hardware mask the count"),
    ("swift trapping `*` vs cpp bare `*` on i64",
     ("swift", "5"), ("cpp", "391"), "NE",
     "swift checks the overflow flag and traps on ud2"),
]


def corpus_guards():
    docs, bad, seen = {}, 0, 0
    for label, left, right, want, why in CORPUS_GUARDS:
        pair = []
        for lang, n in (left, right):
            if lang not in docs:
                p = os.path.join(HERE, "arch_units_%s.json" % lang)
                docs[lang] = json.load(open(p)) if os.path.exists(p) else None
            d = docs[lang]
            u = (d or {}).get("units", {}).get(n)
            pair.append(u)
        if not all(pair) or any(u.get("state") != "OK" for u in pair):
            print("   [skip] %-42s a unit is missing or not OK" % label)
            continue
        seen += 1
        a, b = (semantics(u) for u in pair)
        got = "EQ" if a["key"] == b["key"] else "NE"
        ok = "ok " if got == want else "FAIL"
        if got != want:
            bad += 1
        print("   [%s] %-42s want %s got %s" % (ok, label, want, got))
        print("        why %s" % why)
        print("        %-5s af_%-6s %s" % (left[0], left[1], a["key"][:220]))
        print("        %-5s af_%-6s %s" % (right[0], right[1], b["key"][:220]))
    return bad, seen


def _unit_from(pairs, base=0x1000):
    by, mn, lay, a = [], [], [], base
    for hexs, text in pairs:
        bs = hexs.split()
        by.extend(bs)
        mn.append(text)
        lay.append((a, len(bs)))
        a += len(bs)
    return dict(state="OK", bytes=by, mnem=mn, layout=lay)


def selfcheck():
    print("== arch_sem selfcheck   (%s)" % LIFTER_ID)
    bad = 0
    for label, want, left, right in SELFCHECK:
        a = semantics(_unit_from(left))
        b = semantics(_unit_from(right))
        got = "EQ" if a["key"] == b["key"] else "NE"
        ok = "ok " if got == want else "FAIL"
        if got != want:
            bad += 1
        print("   [%s] %-40s want %s got %s" % (ok, label, want, got))
        print("        L  %s" % a["key"])
        print("        R  %s" % b["key"])
    print("   -- against the campaign's own records --")
    cbad, seen = corpus_guards()
    print("   %d failures over %d synthetic and %d corpus guards"
          % (bad + cbad, len(SELFCHECK), seen))
    return bad + cbad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("langs", nargs="*")
    ap.add_argument("--selfcheck", action="store_true")
    args = ap.parse_args()
    if args.selfcheck:
        return 1 if selfcheck() else 0
    for lang in args.langs:
        annotate(lang)
    return 0


if __name__ == "__main__":
    sys.exit(main())
