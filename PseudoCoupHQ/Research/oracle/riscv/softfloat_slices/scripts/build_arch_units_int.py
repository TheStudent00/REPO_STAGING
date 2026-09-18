#!/usr/bin/env python3
"""Compose every RISC-V arch-unit that contains NO float instruction into
source in c, c++, rust and go.

Input
  Research/oracle/riscv/attest_rv.json     1,244 arch-units from task rv2;
                                           474 are LIFTED, 156 of those carry
                                           a float instruction (done by
                                           build_arch_units.py), the other
                                           318 are this script's population.
Output
  softfloat_slices/arch_units/{c,cpp,rust,go}/   one file per (arch-unit, lang)
  softfloat_slices/arch_units/_units_int.json    the decomposition record

An arch-unit is a list of arch-opcodes.  Every arch-opcode here is an ordinary
RISC-V integer instruction, and each is mapped one of five ways:

  * ARITHMETIC / LOGIC / COMPARE / SHIFT -> the target language's own integer
    operator, on uint64 locals threaded in SSA order.  The word-width forms
    (addw, subw, addiw, mulw, sraw, ...) are written out as "operate on the
    low 32 bits, then sign-extend into 64", which is what RV64 does and is the
    usual source of error.
  * DIVIDE / REMAINDER -> a written-out restoring long division
    (au_divrem_u), never the language's own `/` or `%`: RISC-V's div/divu/
    rem/remu do not trap, division by zero gives an all-ones quotient and the
    dividend back as the remainder, and the signed most-negative over minus
    one gives the most-negative back.  Every language's own `/` differs from
    that, and three of the four have no defined answer at all for those
    inputs.
  * THE STACK-GROWTH PROLOGUE go puts on a function (ld the bound, bltu,
    spill, jal runtime.morestack_noctxt, reload, jal back to the entry) ->
    elided: it re-enters the function with the same arguments and cannot
    change the answer.
  * FRAME BOOKKEEPING (sd/ld of ra, sp adjustment) -> elided.
  * A GUARD BRANCH to a runtime panic (beq b, zero -> runtime.panicdivide;
    blt b, zero -> runtime.panicshift) -> a separate `_trap` predicate
    function per arch-unit, so the trap condition is VERIFIED against go's
    own panic rather than assumed.

`&a` yields an address, which is not a function of the operand bits; those
arch-units are emulated under the stated reduction `*(&a)`, exactly as the
float layer does.
"""

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)                       # softfloat_slices
RV = os.path.dirname(BASE)                         # riscv
ATTEST = os.path.join(RV, "attest_rv.json")
OUT = os.path.join(BASE, "arch_units")
sys.path.insert(0, HERE)
import rv_int_spec as S                                        # noqa: E402

FIRST_INDEX = 174           # the float layer holds 0..173


# --------------------------------------------------------------- selection --
def is_float_mnemonic(m):
    return (m.startswith("f") and not m.startswith("fence")) or \
        m.startswith("c.f")


def select(rows):
    out = []
    for r in rows:
        if r.get("outcome") != "LIFTED":
            continue
        if any(is_float_mnemonic(i.split()[0]) for i in r["body"]):
            continue
        out.append(r)
    return out


# ------------------------------------------------------------------ naming --
BASE_SLUG = {
    "!": "not", "&&": "land", "||": "lor",
    "==": "eq", "!=": "ne", "<": "lt", "<=": "le", ">": "gt", ">=": "ge",
    "|": "bor", "&^": "andnot", "*": "mul", "/": "div", "%": "rem",
    "<<": "shl", ">>": "shr",
    "sizeof": "sizeof", "_Alignof": "alignof_c11", "__alignof": "alignof_gnu",
    "__alignof__": "alignof_gnu2", "__extension__": "ext",
}


def op_slug(r):
    op = r["operator"]
    unary = r["rhs_type"] is None
    if op in BASE_SLUG:
        return BASE_SLUG[op]
    if op == "&":
        return "addr" if unary else "band"
    if op == "^":
        return "cmpl" if unary else "bxor"
    if op == "+":
        return "pos" if unary else "add"
    if op == "-":
        return "neg" if unary else "sub"
    if op in ("++", "--"):
        pre = r["expression"].strip().startswith(op)
        base = "inc" if op == "++" else "dec"
        return ("pre" if pre else "post") + base
    raise KeyError(op)


def unit_name(i, r):
    ty = S.SLUG[S.SRC_TAG[r["lhs_type"]]]
    if r["rhs_type"] is not None:
        ty += "_" + S.SLUG[S.SRC_TAG[r["rhs_type"]]]
    return "au_%03d_%s_%s_%s" % (i, r["lang"], op_slug(r), ty)


# --------------------------------------------------------------- backends ---
class Backend(object):
    line_comment = "//"          # the file-header prefix; c overrides with " *"

    def entry(self, name):
        return name

    def comment(self, s):
        return "    /* %s */" % s


class C(Backend):
    lang, ext = "c", "c"
    line_comment = " *"
    U = "UINT64_C(0x%x)"

    def head(self, name=None):
        return ['#include "arch_units_int.h"', ""]

    def tail(self):
        return []

    def fn_open(self, name, nparams):
        args = ", ".join("uint64_t p%d" % i for i in range(nparams)) or "void"
        return ["uint64_t %s(%s)" % (name, args), "{"]

    def fn_close(self):
        return ["}"]

    def let(self, v, e):
        return "    const uint64_t %s = %s;" % (v, e)

    def ret(self, e):
        return "    return %s;" % e

    def lit(self, v):
        return self.U % v

    def call(self, fn, *args):
        return "%s(%s)" % (fn, ", ".join(args))


class Cpp(C):
    lang, ext = "cpp", "cpp"
    line_comment = "//"

    def head(self, name=None):
        return ['#include "arch_units_int.hpp"', "",
                "namespace archunits {", ""]

    def tail(self):
        return ["", "}  // namespace archunits"]


class Rust(Backend):
    lang, ext = "rust", "rs"

    def comment(self, s):
        return "    // %s" % s

    def head(self, name=None):
        return ["#![allow(unused_parens, unused_variables, unused_imports,"
                " clippy::all)]",
                "use crate::au_int::*;", ""]

    def tail(self):
        return []

    def fn_open(self, name, nparams):
        args = ", ".join("p%d: u64" % i for i in range(nparams))
        return ["pub fn %s(%s) -> u64 {" % (name, args)]

    def fn_close(self):
        return ["}"]

    def let(self, v, e):
        return "    let %s: u64 = %s;" % (v, e)

    def ret(self, e):
        return "    %s" % e

    def lit(self, v):
        return "0x%xu64" % v

    def call(self, fn, *args):
        return "%s(%s)" % (fn, ", ".join(args))


class Go(Backend):
    lang, ext = "go", "go"

    def entry(self, name):
        return "Au" + name[2:]        # exported out of package archunits

    def comment(self, s):
        return "\t// %s" % s

    def head(self, name=None):
        return ["package archunits", ""]

    def tail(self):
        return []

    def fn_open(self, name, nparams):
        args = ", ".join("p%d uint64" % i for i in range(nparams))
        return ["func %s(%s) uint64 {" % (name, args)]

    def fn_close(self):
        return ["}"]

    def let(self, v, e):
        # go makes an unused local a compile error; some arch-opcodes feed
        # only the guard, so every local is explicitly discarded as well
        return "\tvar %s uint64 = %s; _ = %s" % (v, e, v)

    def ret(self, e):
        return "\treturn %s" % e

    def lit(self, v):
        return "uint64(0x%x)" % v

    def call(self, fn, *args):
        return "%s(%s)" % (fn, ", ".join(args))




# --------------------------------------------- the four added 2026-09-16 ----
# Every arch-opcode in this builder goes through an `au_*` helper, so a
# language is its backend plus its helper library and nothing else.  java's
# `long` is exactly 64 bits and carries the pattern directly; python, ruby and
# javascript hold it in an unbounded integer and the helper library masks.


class Java(Backend):
    lang, ext = "java", "java"

    def comment(self, s):
        return "        // %s" % s

    def head(self, name=None):
        # only a PUBLIC top-level class must match the file name, and this one
        # does: both are the arch-unit's name.  A method may share its class's
        # name so long as it declares a return type, which is why the entry
        # keeps the spelling every other language uses.
        return ["public final class %s {" % name, ""]

    def tail(self):
        return ["}"]

    def fn_open(self, name, nparams):
        args = ", ".join("long p%d" % i for i in range(nparams))
        return ["    public static long %s(%s) {" % (name, args)]

    def fn_close(self):
        return ["    }"]

    def let(self, v, e):
        return "        final long %s = %s;" % (v, e)

    def ret(self, e):
        return "        return %s;" % e

    def lit(self, v):
        return "0x%xL" % v

    def call(self, fn, *args):
        return "AuInt.%s(%s)" % (fn, ", ".join(args))


class Python(Backend):
    line_comment = "#"
    lang, ext = "python", "py"

    def comment(self, s):
        return "    # %s" % s

    def head(self, name=None):
        return ["from au_int import *        # noqa: F401,F403", ""]

    def tail(self):
        return []

    def fn_open(self, name, nparams):
        args = ", ".join("p%d" % i for i in range(nparams))
        return ["def %s(%s):" % (name, args)]

    def fn_close(self):
        return []

    def let(self, v, e):
        return "    %s = %s" % (v, e)

    def ret(self, e):
        return "    return %s" % e

    def lit(self, v):
        return "0x%x" % v

    def call(self, fn, *args):
        return "%s(%s)" % (fn, ", ".join(args))


class Ruby(Backend):
    line_comment = "#"
    lang, ext = "ruby", "rb"

    def comment(self, s):
        return "  # %s" % s

    def head(self, name=None):
        return ["require_relative 'au_int'", ""]

    def tail(self):
        return []

    def fn_open(self, name, nparams):
        args = ", ".join("p%d" % i for i in range(nparams))
        return ["def %s(%s)" % (name, args)]

    def fn_close(self):
        return ["end"]

    def let(self, v, e):
        return "  %s = %s" % (v, e)

    def ret(self, e):
        return "  %s" % e

    def lit(self, v):
        return "0x%x" % v

    def call(self, fn, *args):
        return "%s(%s)" % (fn, ", ".join(args))


class Js(Backend):
    lang, ext = "js", "js"

    def comment(self, s):
        return "  // %s" % s

    def head(self, name=None):
        self._fn = []
        return ["'use strict';",
                "const AU = require('./au_int.js');", ""]

    def tail(self):
        return ["", "module.exports = { %s };" % ", ".join(self._fn)]

    def fn_open(self, name, nparams):
        self._fn.append(name)
        args = ", ".join("p%d" % i for i in range(nparams))
        return ["function %s(%s) {" % (name, args)]

    def fn_close(self):
        return ["}"]

    def let(self, v, e):
        return "  const %s = %s;" % (v, e)

    def ret(self, e):
        return "  return %s;" % e

    def lit(self, v):
        return "0x%xn" % v

    def call(self, fn, *args):
        return "AU.%s(%s)" % (fn, ", ".join(args))


BACKENDS = [C(), Cpp(), Rust(), Go(), Java(), Python(), Ruby(), Js()]

MASK64 = 0xFFFFFFFFFFFFFFFF


# ------------------------------------------------------------- composition --
class Blocked(Exception):
    def __init__(self, opcode, why):
        Exception.__init__(self, "%s: %s" % (opcode, why))
        self.opcode = opcode
        self.why = why


def parse(line):
    if " " in line:
        m, rest = line.split(None, 1)
        ops = [x.strip() for x in rest.split(",")]
    else:
        m, ops = line, []
    return m, ops


def imm(text):
    """an immediate, sign-extended into 64 bits."""
    return int(text, 0) & MASK64


def base_of(text):
    """`0x8(sp)` -> ('sp', 8)"""
    off, _, rest = text.partition("(")
    return rest.rstrip(")"), int(off, 0)


# how each integer arch-opcode maps, for the record
MAPPED = {
    "add": "operator:+", "c.add": "operator:+", "addi": "operator:+",
    "c.addi": "operator:+", "c.addi16sp": "frame",
    "addw": "operator:+ then sign-extend the low 32 bits",
    "c.addw": "operator:+ then sign-extend the low 32 bits",
    "addiw": "operator:+ then sign-extend the low 32 bits",
    "c.addiw": "operator:+ then sign-extend the low 32 bits",
    "sub": "operator:-", "c.sub": "operator:-",
    "subw": "operator:- then sign-extend the low 32 bits",
    "c.subw": "operator:- then sign-extend the low 32 bits",
    "and": "operator:&", "c.and": "operator:&", "andi": "operator:&",
    "andn": "operator:& with operator:~",
    "or": "operator:|", "c.or": "operator:|", "ori": "operator:|",
    "xor": "operator:^", "c.xor": "operator:^", "xori": "operator:^",
    "sll": "operator:<< (count masked to 6 bits)",
    "slli": "operator:<<",
    "sllw": "operator:<< on the low 32 bits then sign-extend",
    "srl": "operator:>> unsigned (count masked to 6 bits)",
    "srli": "operator:>> unsigned",
    "sra": "arithmetic right shift, written out in unsigned bit operations",
    "sraw": "arithmetic right shift of the low 32 bits, written out",
    "slt": "operator:< signed", "slti": "operator:< signed",
    "sltu": "operator:< unsigned", "sltiu": "operator:< unsigned",
    "mul": "operator:*",
    "mulw": "operator:* then sign-extend the low 32 bits",
    "div": "written-out restoring division (NOT the language's /)",
    "divu": "written-out restoring division (NOT the language's /)",
    "divw": "written-out restoring division (NOT the language's /)",
    "divuw": "written-out restoring division (NOT the language's /)",
    "rem": "written-out restoring division (NOT the language's %)",
    "remu": "written-out restoring division (NOT the language's %)",
    "remw": "written-out restoring division (NOT the language's %)",
    "remuw": "written-out restoring division (NOT the language's %)",
    "czero.eqz": "conditional select",
    "czero.nez": "conditional select",
    "c.li": "constant", "lui": "constant", "c.mv": "register move",
    "c.nop": "no-op",
    "c.jr": "return", "jalr": "return",
    "beq": "guard branch -> a `_trap` predicate",
    "blt": "guard branch -> a `_trap` predicate",
    "bltu": "stack-growth check -> elided",
    "ld": "stack-growth check -> elided",
    "jal": "stack-growth call / restart / panic tail -> elided",
    "sd": "frame bookkeeping -> elided",
    "c.sdsp": "frame bookkeeping -> elided",
    "c.ldsp": "frame bookkeeping -> elided",
    "c.swsp": "stack-growth spill -> elided",
    "c.lwsp": "stack-growth reload -> elided",
    "sb": "stack-growth spill -> elided",
    "lbu": "stack-growth reload -> elided",
    "lb": "stack-growth reload -> elided",
    "auipc": "address of a heap type descriptor -- not a bit function",
}

W32 = {"addw", "c.addw", "addiw", "c.addiw", "subw", "c.subw", "sllw", "srlw",
       "sraw", "mulw", "divw", "divuw", "remw", "remuw"}


class Composer(object):
    """Walk one arch-unit's arch-opcodes, threading the machine's registers as
    ordinary unsigned 64-bit locals in SSA order."""

    def __init__(self, be, unit, mode="value", mask_answer=True):
        self.be = be
        self.unit = unit
        self.mode = mode            # "value" | "trap"
        self.mask_answer = mask_answer
        self.n = 0
        self.reg = {}
        self.lines = []
        self.steps = []
        self.trap = None            # the guard condition expression, if any

    # -- plumbing ------------------------------------------------------------
    def fresh(self, e):
        self.n += 1
        v = "v%d" % self.n
        self.lines.append(self.be.let(v, e))
        return v

    def rd(self, name):
        if name == "zero":
            return self.be.lit(0)
        if name not in self.reg:
            raise Blocked(name, "read of a register this arch-unit never "
                                "wrote and the ABI does not define")
        return self.reg[name]

    def wr(self, name, e):
        self.reg[name] = self.fresh(e)

    def note(self, s):
        self.lines.append(self.be.comment(s))

    # -- the ABI presentation of each source operand --------------------------
    def prologue(self):
        be = self.be
        fi = ii = 0
        for i, (nm, ty) in enumerate(params_of(self.unit)):
            tag = S.SRC_TAG[ty]
            p = "p%d" % i
            if S.kind(tag) == "f":
                reg = "fa%d" % fi
                fi += 1
                e = "((%s) & %s)" % (p, be.lit(0xFFFFFFFF)) \
                    if S.width(tag) == 32 else p
                why = "arrives in %s as a bit pattern" % reg
            else:
                reg = "a%d" % ii
                ii += 1
                if S.kind(tag) == "b":
                    e = "((%s) & %s)" % (p, be.lit(1))
                    why = "zero-extended to XLEN"
                elif S.width(tag) == 32 and S.signed(tag):
                    e = be.call("au_sext32", p)
                    why = "sign-extended to XLEN, as the ABI presents it"
                elif S.width(tag) == 32:
                    e = "((%s) & %s)" % (p, be.lit(0xFFFFFFFF))
                    why = "zero-extended to XLEN"
                else:
                    e = p
                    why = "arrives in %s" % reg
            self.note("%s: operand `%s` (%s) %s" % (reg, nm, ty, why))
            self.reg[reg] = self.fresh(e)

    # -- one arch-opcode ------------------------------------------------------
    def step(self, line):
        be = self.be
        m, o = parse(line)
        rec = {"arch_opcode": line, "mnemonic": m, "kind": "integer",
               "mapped_to": MAPPED.get(m, "?")}

        # ---- frame bookkeeping ---------------------------------------------
        if (m in ("c.addi", "addi", "c.addi16sp") and o and o[0] == "sp") or \
           (m in ("sd", "c.sdsp", "c.ldsp", "ld") and o and o[0] == "ra") or \
           m == "c.nop":
            rec["kind"] = "frame"
            rec["mapped_to"] = "frame bookkeeping -> elided"
            self.steps.append(rec)
            return

        # ---- the guard branch ----------------------------------------------
        if m in ("beq", "blt", "bne", "bge"):
            if len(o) != 3 or o[1] != "zero":
                raise Blocked(line, "a branch this composer does not model")
            v = self.rd(o[0])
            if m == "beq":
                cond = be.call("au_eqz", v)
            elif m == "bne":
                cond = be.call("au_nez", v)
            elif m == "blt":
                cond = be.call("au_ltz", v)
            else:
                cond = be.call("au_gez", v)
            rec["kind"] = "guard"
            self.trap = cond
            self.steps.append(rec)
            return

        self.steps.append(rec)

        # ---- the ordinary integer arch-opcodes ------------------------------
        def bin_(fmt, *regs):
            self.wr(o[0], fmt % tuple(self.rd(r) for r in regs))

        if m in ("add", "sub", "and", "or", "xor", "mul", "sll", "srl",
                 "slt", "sltu", "sra", "addw", "subw", "sllw", "srlw",
                 "sraw", "mulw", "div", "divu", "divw", "divuw", "rem",
                 "remu", "remw", "remuw"):
            a, b = self.rd(o[1]), self.rd(o[2])
            self.wr(o[0], self.alu(m, a, b))
        elif m in ("c.add", "c.sub", "c.and", "c.or", "c.xor", "c.addw",
                   "c.subw", "c.mul"):
            a, b = self.rd(o[0]), self.rd(o[1])
            self.wr(o[0], self.alu(m[2:], a, b))
        elif m in ("addi", "addiw", "andi", "ori", "xori", "slti", "sltiu",
                   "slli", "srli", "srai", "slliw", "srliw", "sraiw"):
            a = self.rd(o[1])
            self.wr(o[0], self.alu_i(m, a, imm(o[2])))
        elif m in ("c.addi", "c.addiw", "c.andi"):
            a = self.rd(o[0])
            self.wr(o[0], self.alu_i(m[2:], a, imm(o[1])))
        elif m == "c.li":
            self.wr(o[0], be.lit(imm(o[1])))
        elif m == "lui":
            self.wr(o[0], be.lit((imm(o[1]) << 12) & MASK64))
        elif m == "c.mv":
            self.wr(o[0], self.rd(o[1]))
        elif m == "andn":
            self.wr(o[0], be.call("au_andn", self.rd(o[1]), self.rd(o[2])))
        elif m == "czero.eqz":
            self.wr(o[0], be.call("au_czeqz", self.rd(o[1]), self.rd(o[2])))
        elif m == "czero.nez":
            self.wr(o[0], be.call("au_cznez", self.rd(o[1]), self.rd(o[2])))
        else:
            raise Blocked(line, "no rule for this integer arch-opcode")

    def alu(self, m, a, b):
        be = self.be
        T = {"add": "au_add", "sub": "au_sub", "and": "au_and",
             "or": "au_or", "xor": "au_xor", "mul": "au_mul",
             "sll": "au_sll", "srl": "au_srl", "sra": "au_sra",
             "slt": "au_slt", "sltu": "au_sltu",
             "addw": "au_addw", "subw": "au_subw", "sllw": "au_sllw",
             "srlw": "au_srlw", "sraw": "au_sraw", "mulw": "au_mulw",
             "div": "au_div", "divu": "au_divu", "divw": "au_divw",
             "divuw": "au_divuw", "rem": "au_rem", "remu": "au_remu",
             "remw": "au_remw", "remuw": "au_remuw"}
        return be.call(T[m], a, b)

    def alu_i(self, m, a, v):
        be = self.be
        T = {"addi": "au_add", "andi": "au_and", "ori": "au_or",
             "xori": "au_xor", "slti": "au_slt", "sltiu": "au_sltu",
             "slli": "au_sll", "srli": "au_srl", "srai": "au_sra",
             "addiw": "au_addw", "slliw": "au_sllw", "srliw": "au_srlw",
             "sraiw": "au_sraw"}
        return be.call(T[m], a, be.lit(v))

    # -- the whole arch-unit --------------------------------------------------
    def run(self):
        pro, val, ret, tail = split_body(self.unit["body"])
        for line in pro:
            m = line.split()[0]
            self.steps.append({"arch_opcode": line, "mnemonic": m,
                               "kind": "prologue",
                               "mapped_to": MAPPED.get(m, "?")})
        self.prologue()
        for line in val:
            self.step(line)
            if self.mode == "trap" and self.trap is not None:
                self.lines.append(self.be.ret(self.trap))
                return self.lines
        if ret is not None:
            m = ret.split()[0]
            self.steps.append({"arch_opcode": ret, "mnemonic": m,
                               "kind": "integer", "mapped_to": "return"})
        for line in tail:
            m = line.split()[0]
            self.steps.append({"arch_opcode": line, "mnemonic": m,
                               "kind": "trap-tail",
                               "mapped_to": "the runtime panic the guard "
                                            "branches to -> the `_trap` "
                                            "predicate"})
        if self.mode == "trap":
            self.lines.append(self.be.ret(self.be.lit(0)))
            return self.lines
        tag = S.result_tag(self.unit)
        e = self.rd(S.answer_register(self.unit))
        self.note("the answer is %s, %d bits"
                  % (S.C_TYPE[tag] if self.unit["lang"] == "c"
                     else S.GO_TYPE[tag], S.width(tag)))
        w = S.width(tag)
        if self.mask_answer:
            if w == 1:
                e = "((%s) & %s)" % (e, self.be.lit(1))
            elif w == 32:
                e = "((%s) & %s)" % (e, self.be.lit(0xFFFFFFFF))
        self.lines.append(self.be.ret(e))
        return self.lines


def split_body(body):
    """-> (stack-growth prologue, the value region, the return, the trap tail)

    The go stack-growth prologue is
        ld t1, <bound>(s11) | bltu t1, sp, <entry> | <spill> |
        jal t0, runtime.morestack_noctxt | <reload> | jal zero, <this function>
    It re-enters the function at its real entry with the same arguments, so it
    cannot change the answer.  Everything after the first return is the tail
    the guard branch jumps to.
    """
    i, pro = 0, []
    if len(body) >= 2 and body[0].startswith("ld t1,") \
            and body[1].startswith("bltu t1, sp,"):
        for j in range(2, len(body)):
            if body[j].startswith("jal zero,"):
                pro, i = body[:j + 1], j + 1
                break
        else:
            raise Blocked(body[1], "a stack-growth check with no restart")
    val, ret, at = [], None, None
    for j in range(i, len(body)):
        if body[j].split()[0] in ("c.jr", "jalr"):
            ret, at = body[j], j
            break
        val.append(body[j])
    tail = body[at + 1:] if at is not None else []
    return pro, val, ret, tail


def params_of(r):
    out = [("a", r["lhs_type"])]
    if r["rhs_type"] is not None:
        out.append(("b", r["rhs_type"]))
    return out


# ---------------------------------------------- the address-of reduction ----
MEM = {"sd", "sw", "sb", "ld", "lw", "lb", "lbu", "c.sdsp", "c.ldsp",
       "c.swsp", "c.lwsp"}


def describe(r, reduced=False):
    """Decompose a body for the record without composing it."""
    out = []
    for line in r["body"]:
        m, o = parse(line)
        rec = {"arch_opcode": line, "mnemonic": m, "kind": "integer",
               "mapped_to": MAPPED.get(m, "?")}
        if reduced:
            if m == "auipc" or "newobject" in line:
                rec["kind"] = "address"
                rec["mapped_to"] = "the heap allocator -- not a bit function"
            elif m in ("addi", "c.addi", "c.addi4spn", "c.addi16sp") \
                    and len(o) > 1 and "sp" in o[:2]:
                rec["kind"] = "address"
                rec["mapped_to"] = ("a stack address / frame adjustment -- "
                                    "not a bit function")
            elif m in MEM:
                rec["kind"] = "memory"
                rec["mapped_to"] = "the store/load the reduction *(&a) reads"
            elif m in ("c.jr", "jalr"):
                rec["mapped_to"] = "return"
            elif m == "jal":
                rec["kind"] = "address"
                rec["mapped_to"] = "a call into the go runtime"
        out.append(rec)
    return out


def decisive(r):
    for line in r["body"]:
        if "newobject" in line:
            return {"opcode": line,
                    "why": "the answer is a heap address handed back by the "
                           "go runtime allocator, not a function of the "
                           "operand bits"}
        if line.startswith("addi a0, sp") or line.startswith("c.addi4spn"):
            return {"opcode": line,
                    "why": "the answer is the address of a stack slot, not a "
                           "function of the operand bits"}
    return {"opcode": r["body"][0], "why": "the answer is an address"}


def compose_addr(be, r):
    tag = S.result_tag(r)
    w = S.width(tag)
    e = "p0"
    if w == 1:
        e = "((p0) & %s)" % be.lit(1)
    elif w == 32:
        e = "((p0) & %s)" % be.lit(0xFFFFFFFF)
    return [be.comment("REDUCED: the emulated function is *(&a) -- the bit "
                       "pattern the store/load moves"), be.ret(e)]


# --------------------------------------------------------------- emission ---
def header_lines(be, i, r, steps, reduced, has_trap):
    tag = S.result_tag(r)
    ln = []
    c = be.line_comment
    if be.lang == "c":
        ln.append("/*")

    def put(s):
        ln.append(("%s %s" % (c, s)).rstrip())

    put("arch-unit %d  --  %s  `%s`  lhs=%s rhs=%s"
        % (i, r["lang"], r["expression"], r["lhs_type"], r["rhs_type"]))
    put("symbol %s   outcome %s   %d arch-opcodes"
        % (r["symbol"], r["outcome"], len(r["body"])))
    put("")
    put("the arch-unit, arch-opcode by arch-opcode:")
    for s in steps:
        put("  %-36s %-10s %s" % (s["arch_opcode"], s["kind"],
                                  s.get("mapped_to", "")))
    put("")
    put("answer: %s, %d bits.  parameters are operand bit patterns."
        % (S.C_TYPE[tag] if r["lang"] == "c" else S.GO_TYPE[tag],
           S.width(tag)))
    if has_trap:
        put("")
        put("GUARDED: this arch-unit branches to a go runtime panic.  The "
            "function")
        put("below is the fall-through; the companion `_trap` predicate is 1 "
            "exactly")
        put("when the arch-unit takes the branch instead.")
    if reduced:
        put("")
        put("REDUCED: `&a` yields an address, which is not a function of the")
        put("operand bits.  What is emulated and verified here is *(&a).")
    if be.lang == "c":
        ln.append(" */")
    return ln


def main():
    rows = json.load(open(ATTEST))["rows"]
    units = select(rows)
    assert len(units) == 318, len(units)

    for be in BACKENDS:
        os.makedirs(os.path.join(OUT, be.lang), exist_ok=True)

    names = set()
    record = []
    failures = []
    for k, r in enumerate(units):
        i = FIRST_INDEX + k
        name = unit_name(i, r)
        assert name not in names, name
        names.add(name)
        reduced = S.is_reduced(r)
        nparams = len(params_of(r))

        blocked, steps, has_trap = None, None, False
        if not reduced:
            try:
                probe = Composer(C(), r)
                probe.run()
                steps = probe.steps
                has_trap = probe.trap is not None
            except Blocked as e:
                blocked = {"opcode": e.opcode, "why": e.why}
                steps = describe(r, True)
                failures.append((name, e.opcode, e.why))
        else:
            steps = describe(r, True)
            blocked = decisive(r)

        files = {}
        for be in BACKENDS:
            body, trap_body = None, None
            if reduced or blocked:
                body = compose_addr(be, r)
            else:
                body = Composer(be, r).run()
                if has_trap:
                    trap_body = Composer(be, r, "trap").run()
            L = (header_lines(be, i, r, steps, bool(reduced or blocked),
                              has_trap)
                 + be.head(name)
                 + be.fn_open(be.entry(name), nparams) + body + be.fn_close())
            if trap_body is not None:
                L += [""] + be.fn_open(be.entry(name) + "_trap", nparams) \
                    + trap_body + be.fn_close()
            L += be.tail()
            text = "\n".join(L) + "\n"
            p = os.path.join(OUT, be.lang, "%s.%s" % (name, be.ext))
            open(p, "w").write(text)
            files[be.lang] = {"file": os.path.relpath(p, BASE),
                              "entry": be.entry(name),
                              "trap_entry": (be.entry(name) + "_trap")
                              if has_trap else None,
                              "lines": text.count("\n")}
        tag = S.result_tag(r)
        record.append({
            "index": i, "name": name, "lang": r["lang"],
            "operator": r["operator"], "expression": r["expression"],
            "lhs_type": r["lhs_type"], "rhs_type": r["rhs_type"],
            "symbol": r["symbol"], "unit": r["unit"], "outcome": r["outcome"],
            "body": r["body"], "arch_opcodes": steps,
            "result_tag": tag, "result_bits": S.width(tag),
            "result_type": S.C_TYPE[tag] if r["lang"] == "c"
            else S.GO_TYPE[tag],
            "n_params": nparams, "reduced": bool(reduced or blocked),
            "blocked": blocked, "guarded": has_trap,
            "languages": files,
        })
        print("%3d %-46s %s%s" % (i, name,
                                  "REDUCED " if (reduced or blocked) else "",
                                  "GUARDED" if has_trap else ""))

    write_helpers()
    write_glue(record)
    json.dump({"units": record}, open(os.path.join(OUT, "_units_int.json"),
                                      "w"), indent=1)

    opc = collections.Counter()
    ukinds = collections.defaultdict(set)
    for u in record:
        for s in u["arch_opcodes"]:
            opc[s["mnemonic"]] += 1
            ukinds[s["mnemonic"]].add(u["index"])
    print("\n%d arch-units x 4 languages, %d distinct arch-opcodes"
          % (len(record), len(opc)))
    if failures:
        print("FAILED TO COMPOSE:")
        for f in failures:
            print("  ", f)


# ------------------------------------------------------------- the helpers --
C_HELPERS = r"""/* generated by scripts/build_arch_units_int.py
 *
 * The RV64 integer arch-opcodes, each written as the language's own integer
 * operators over unsigned 64-bit values.  Two things here are not a plain
 * operator:
 *
 *   au_sra / au_sraw   an arithmetic right shift written out in UNSIGNED bit
 *                      operations, so it does not lean on C's
 *                      implementation-defined `>>` of a negative value, and
 *                      so all four languages compute it the same way.
 *   au_divrem_u        restoring long division.  NO `/` or `%` of the host
 *                      language appears anywhere in this file, because RISC-V
 *                      div/divu/rem/remu do not trap: b == 0 gives an
 *                      all-ones quotient and the dividend back as the
 *                      remainder, and the signed most-negative over minus one
 *                      gives the most-negative back with a zero remainder.
 *
 * Every shift count is masked to the width RISC-V actually uses (6 bits for
 * the doubleword forms, 5 for the word forms) before it reaches a `<<` or
 * `>>`, so no shift here is ever undefined in C or C++.
 */
#ifndef AU_INT_H
#define AU_INT_H

#include <stdint.h>
#include <stdbool.h>

#define AU_ONES UINT64_C(0xffffffffffffffff)
#define AU_MIN64 UINT64_C(0x8000000000000000)

AU_INLINE uint64_t au_b2u(bool b) { return b ? UINT64_C(1) : UINT64_C(0); }
AU_INLINE uint64_t au_sext32(uint64_t x)
{
    return (uint64_t)(int64_t)(int32_t)(uint32_t)x;
}
AU_INLINE uint64_t au_add(uint64_t a, uint64_t b) { return a + b; }
AU_INLINE uint64_t au_sub(uint64_t a, uint64_t b) { return a - b; }
AU_INLINE uint64_t au_and(uint64_t a, uint64_t b) { return a & b; }
AU_INLINE uint64_t au_or(uint64_t a, uint64_t b)  { return a | b; }
AU_INLINE uint64_t au_xor(uint64_t a, uint64_t b) { return a ^ b; }
AU_INLINE uint64_t au_andn(uint64_t a, uint64_t b) { return a & ~b; }
AU_INLINE uint64_t au_mul(uint64_t a, uint64_t b) { return a * b; }
AU_INLINE uint64_t au_addw(uint64_t a, uint64_t b) { return au_sext32(a + b); }
AU_INLINE uint64_t au_subw(uint64_t a, uint64_t b) { return au_sext32(a - b); }
AU_INLINE uint64_t au_mulw(uint64_t a, uint64_t b) { return au_sext32(a * b); }
AU_INLINE uint64_t au_sll(uint64_t a, uint64_t s) { return a << (s & 63); }
AU_INLINE uint64_t au_srl(uint64_t a, uint64_t s) { return a >> (s & 63); }
AU_INLINE uint64_t au_sra(uint64_t a, uint64_t n)
{
    uint64_t s = n & 63;
    uint64_t r = a >> s;
    uint64_t m = UINT64_C(0) - (a >> 63);        /* all ones if negative */
    return r | ((m << (63 - s)) << 1);           /* s == 0 shifts it out */
}
AU_INLINE uint64_t au_sllw(uint64_t a, uint64_t n)
{
    return au_sext32((a << (n & 31)) & UINT64_C(0xffffffff));
}
AU_INLINE uint64_t au_srlw(uint64_t a, uint64_t n)
{
    return au_sext32((a & UINT64_C(0xffffffff)) >> (n & 31));
}
AU_INLINE uint64_t au_sraw(uint64_t a, uint64_t n)
{
    uint64_t s = n & 31;
    uint64_t r = (a & UINT64_C(0xffffffff)) >> s;
    uint64_t m = UINT64_C(0) - ((a >> 31) & UINT64_C(1));
    r |= ((m << (31 - s)) << 1) & UINT64_C(0xffffffff);
    return au_sext32(r);
}
AU_INLINE uint64_t au_slt(uint64_t a, uint64_t b)
{
    return au_b2u((int64_t)a < (int64_t)b);
}
AU_INLINE uint64_t au_sltu(uint64_t a, uint64_t b) { return au_b2u(a < b); }
AU_INLINE uint64_t au_eqz(uint64_t a) { return au_b2u(a == 0); }
AU_INLINE uint64_t au_nez(uint64_t a) { return au_b2u(a != 0); }
AU_INLINE uint64_t au_ltz(uint64_t a) { return au_b2u((int64_t)a < 0); }
AU_INLINE uint64_t au_gez(uint64_t a) { return au_b2u((int64_t)a >= 0); }
AU_INLINE uint64_t au_czeqz(uint64_t v, uint64_t c) { return c == 0 ? 0 : v; }
AU_INLINE uint64_t au_cznez(uint64_t v, uint64_t c) { return c != 0 ? 0 : v; }

/* restoring long division: 64 steps, no / and no % */
AU_INLINE void au_divrem_u(uint64_t a, uint64_t b, uint64_t *qo, uint64_t *ro)
{
    uint64_t q = 0, r = 0;
    int i;
    for (i = 63; i >= 0; i--) {
        uint64_t carry = r >> 63;
        r = (r << 1) | ((a >> i) & UINT64_C(1));
        if (carry != 0 || r >= b) { r -= b; q |= UINT64_C(1) << i; }
    }
    *qo = q; *ro = r;
}
AU_INLINE uint64_t au_divu(uint64_t a, uint64_t b)
{
    uint64_t q, r;
    if (b == 0) return AU_ONES;                  /* RISC-V divu by zero */
    au_divrem_u(a, b, &q, &r);
    return q;
}
AU_INLINE uint64_t au_remu(uint64_t a, uint64_t b)
{
    uint64_t q, r;
    if (b == 0) return a;                        /* RISC-V remu by zero */
    au_divrem_u(a, b, &q, &r);
    return r;
}
AU_INLINE uint64_t au_div(uint64_t a, uint64_t b)
{
    uint64_t na, nb, q, r;
    if (b == 0) return AU_ONES;
    if (a == AU_MIN64 && b == AU_ONES) return AU_MIN64;
    na = a >> 63; nb = b >> 63;
    au_divrem_u(na ? (UINT64_C(0) - a) : a, nb ? (UINT64_C(0) - b) : b,
                &q, &r);
    return (na ^ nb) ? (UINT64_C(0) - q) : q;
}
AU_INLINE uint64_t au_rem(uint64_t a, uint64_t b)
{
    uint64_t na, nb, q, r;
    if (b == 0) return a;
    if (a == AU_MIN64 && b == AU_ONES) return 0;
    na = a >> 63; nb = b >> 63;
    au_divrem_u(na ? (UINT64_C(0) - a) : a, nb ? (UINT64_C(0) - b) : b,
                &q, &r);
    return na ? (UINT64_C(0) - r) : r;           /* sign of the dividend */
}
AU_INLINE uint64_t au_divw(uint64_t a, uint64_t b)
{
    return au_sext32(au_div(au_sext32(a), au_sext32(b)));
}
AU_INLINE uint64_t au_remw(uint64_t a, uint64_t b)
{
    return au_sext32(au_rem(au_sext32(a), au_sext32(b)));
}
AU_INLINE uint64_t au_divuw(uint64_t a, uint64_t b)
{
    return au_sext32(au_divu(a & UINT64_C(0xffffffff),
                             b & UINT64_C(0xffffffff)));
}
AU_INLINE uint64_t au_remuw(uint64_t a, uint64_t b)
{
    return au_sext32(au_remu(a & UINT64_C(0xffffffff),
                             b & UINT64_C(0xffffffff)));
}

#endif
"""

RUST_HELPERS = r"""// generated by scripts/build_arch_units_int.py
// The RV64 integer arch-opcodes as rust.  Every add/sub/mul is wrapping and
// every shift count is masked to the width RISC-V uses, so nothing here can
// panic.  au_sra / au_sraw are written out in unsigned bit operations and
// au_divrem_u is restoring long division -- no `/` or `%` appears at all.
pub const AU_ONES: u64 = 0xffffffffffffffffu64;
pub const AU_MIN64: u64 = 0x8000000000000000u64;

#[inline(always)]
pub fn au_b2u(b: bool) -> u64 { if b { 1u64 } else { 0u64 } }
#[inline(always)]
pub fn au_sext32(x: u64) -> u64 { ((x as u32) as i32 as i64) as u64 }
#[inline(always)]
pub fn au_add(a: u64, b: u64) -> u64 { a.wrapping_add(b) }
#[inline(always)]
pub fn au_sub(a: u64, b: u64) -> u64 { a.wrapping_sub(b) }
#[inline(always)]
pub fn au_and(a: u64, b: u64) -> u64 { a & b }
#[inline(always)]
pub fn au_or(a: u64, b: u64) -> u64 { a | b }
#[inline(always)]
pub fn au_xor(a: u64, b: u64) -> u64 { a ^ b }
#[inline(always)]
pub fn au_andn(a: u64, b: u64) -> u64 { a & !b }
#[inline(always)]
pub fn au_mul(a: u64, b: u64) -> u64 { a.wrapping_mul(b) }
#[inline(always)]
pub fn au_addw(a: u64, b: u64) -> u64 { au_sext32(a.wrapping_add(b)) }
#[inline(always)]
pub fn au_subw(a: u64, b: u64) -> u64 { au_sext32(a.wrapping_sub(b)) }
#[inline(always)]
pub fn au_mulw(a: u64, b: u64) -> u64 { au_sext32(a.wrapping_mul(b)) }
#[inline(always)]
pub fn au_sll(a: u64, s: u64) -> u64 { a << (s & 63) }
#[inline(always)]
pub fn au_srl(a: u64, s: u64) -> u64 { a >> (s & 63) }
#[inline(always)]
pub fn au_sra(a: u64, n: u64) -> u64 {
    let s = n & 63;
    let r = a >> s;
    let m = 0u64.wrapping_sub(a >> 63);
    r | ((m << (63 - s)) << 1)
}
#[inline(always)]
pub fn au_sllw(a: u64, n: u64) -> u64 {
    au_sext32((a << (n & 31)) & 0xffffffffu64)
}
#[inline(always)]
pub fn au_srlw(a: u64, n: u64) -> u64 {
    au_sext32((a & 0xffffffffu64) >> (n & 31))
}
#[inline(always)]
pub fn au_sraw(a: u64, n: u64) -> u64 {
    let s = n & 31;
    let mut r = (a & 0xffffffffu64) >> s;
    let m = 0u64.wrapping_sub((a >> 31) & 1u64);
    r |= ((m << (31 - s)) << 1) & 0xffffffffu64;
    au_sext32(r)
}
#[inline(always)]
pub fn au_slt(a: u64, b: u64) -> u64 { au_b2u((a as i64) < (b as i64)) }
#[inline(always)]
pub fn au_sltu(a: u64, b: u64) -> u64 { au_b2u(a < b) }
#[inline(always)]
pub fn au_eqz(a: u64) -> u64 { au_b2u(a == 0) }
#[inline(always)]
pub fn au_nez(a: u64) -> u64 { au_b2u(a != 0) }
#[inline(always)]
pub fn au_ltz(a: u64) -> u64 { au_b2u((a as i64) < 0) }
#[inline(always)]
pub fn au_gez(a: u64) -> u64 { au_b2u((a as i64) >= 0) }
#[inline(always)]
pub fn au_czeqz(v: u64, c: u64) -> u64 { if c == 0 { 0 } else { v } }
#[inline(always)]
pub fn au_cznez(v: u64, c: u64) -> u64 { if c != 0 { 0 } else { v } }

#[inline(always)]
pub fn au_divrem_u(a: u64, b: u64) -> (u64, u64) {
    let (mut q, mut r) = (0u64, 0u64);
    let mut i: i32 = 63;
    while i >= 0 {
        let carry = r >> 63;
        r = (r << 1) | ((a >> (i as u32)) & 1u64);
        if carry != 0 || r >= b { r = r.wrapping_sub(b); q |= 1u64 << (i as u32); }
        i -= 1;
    }
    (q, r)
}
#[inline(always)]
pub fn au_divu(a: u64, b: u64) -> u64 {
    if b == 0 { return AU_ONES; }
    au_divrem_u(a, b).0
}
#[inline(always)]
pub fn au_remu(a: u64, b: u64) -> u64 {
    if b == 0 { return a; }
    au_divrem_u(a, b).1
}
#[inline(always)]
pub fn au_div(a: u64, b: u64) -> u64 {
    if b == 0 { return AU_ONES; }
    if a == AU_MIN64 && b == AU_ONES { return AU_MIN64; }
    let (na, nb) = (a >> 63, b >> 63);
    let (q, _r) = au_divrem_u(if na != 0 { 0u64.wrapping_sub(a) } else { a },
                              if nb != 0 { 0u64.wrapping_sub(b) } else { b });
    if (na ^ nb) != 0 { 0u64.wrapping_sub(q) } else { q }
}
#[inline(always)]
pub fn au_rem(a: u64, b: u64) -> u64 {
    if b == 0 { return a; }
    if a == AU_MIN64 && b == AU_ONES { return 0; }
    let (na, nb) = (a >> 63, b >> 63);
    let (_q, r) = au_divrem_u(if na != 0 { 0u64.wrapping_sub(a) } else { a },
                              if nb != 0 { 0u64.wrapping_sub(b) } else { b });
    if na != 0 { 0u64.wrapping_sub(r) } else { r }
}
#[inline(always)]
pub fn au_divw(a: u64, b: u64) -> u64 {
    au_sext32(au_div(au_sext32(a), au_sext32(b)))
}
#[inline(always)]
pub fn au_remw(a: u64, b: u64) -> u64 {
    au_sext32(au_rem(au_sext32(a), au_sext32(b)))
}
#[inline(always)]
pub fn au_divuw(a: u64, b: u64) -> u64 {
    au_sext32(au_divu(a & 0xffffffffu64, b & 0xffffffffu64))
}
#[inline(always)]
pub fn au_remuw(a: u64, b: u64) -> u64 {
    au_sext32(au_remu(a & 0xffffffffu64, b & 0xffffffffu64))
}
"""

GO_HELPERS = r"""package archunits

// generated by scripts/build_arch_units_int.py
// The RV64 integer arch-opcodes as go.  Shift counts are masked to the width
// RISC-V uses; au_sra / au_sraw are written out in unsigned bit operations;
// au_divrem_u is restoring long division, so no `/` or `%` appears at all and
// nothing here can panic.

const auOnes uint64 = 0xffffffffffffffff
const auMin64 uint64 = 0x8000000000000000

func au_b2u(b bool) uint64 {
	if b {
		return 1
	}
	return 0
}
func au_sext32(x uint64) uint64  { return uint64(int64(int32(uint32(x)))) }
func au_add(a, b uint64) uint64  { return a + b }
func au_sub(a, b uint64) uint64  { return a - b }
func au_and(a, b uint64) uint64  { return a & b }
func au_or(a, b uint64) uint64   { return a | b }
func au_xor(a, b uint64) uint64  { return a ^ b }
func au_andn(a, b uint64) uint64 { return a &^ b }
func au_mul(a, b uint64) uint64  { return a * b }
func au_addw(a, b uint64) uint64 { return au_sext32(a + b) }
func au_subw(a, b uint64) uint64 { return au_sext32(a - b) }
func au_mulw(a, b uint64) uint64 { return au_sext32(a * b) }
func au_sll(a, s uint64) uint64  { return a << (s & 63) }
func au_srl(a, s uint64) uint64  { return a >> (s & 63) }
func au_sra(a, n uint64) uint64 {
	s := n & 63
	r := a >> s
	m := uint64(0) - (a >> 63)
	return r | ((m << (63 - s)) << 1)
}
func au_sllw(a, n uint64) uint64 { return au_sext32((a << (n & 31)) & 0xffffffff) }
func au_srlw(a, n uint64) uint64 { return au_sext32((a & 0xffffffff) >> (n & 31)) }
func au_sraw(a, n uint64) uint64 {
	s := n & 31
	r := (a & 0xffffffff) >> s
	m := uint64(0) - ((a >> 31) & 1)
	r |= ((m << (31 - s)) << 1) & 0xffffffff
	return au_sext32(r)
}
func au_slt(a, b uint64) uint64   { return au_b2u(int64(a) < int64(b)) }
func au_sltu(a, b uint64) uint64  { return au_b2u(a < b) }
func au_eqz(a uint64) uint64      { return au_b2u(a == 0) }
func au_nez(a uint64) uint64      { return au_b2u(a != 0) }
func au_ltz(a uint64) uint64      { return au_b2u(int64(a) < 0) }
func au_gez(a uint64) uint64      { return au_b2u(int64(a) >= 0) }
func au_czeqz(v, c uint64) uint64 {
	if c == 0 {
		return 0
	}
	return v
}
func au_cznez(v, c uint64) uint64 {
	if c != 0 {
		return 0
	}
	return v
}

func au_divrem_u(a, b uint64) (uint64, uint64) {
	var q, r uint64
	for i := 63; i >= 0; i-- {
		carry := r >> 63
		r = (r << 1) | ((a >> uint(i)) & 1)
		if carry != 0 || r >= b {
			r -= b
			q |= uint64(1) << uint(i)
		}
	}
	return q, r
}
func au_divu(a, b uint64) uint64 {
	if b == 0 {
		return auOnes
	}
	q, _ := au_divrem_u(a, b)
	return q
}
func au_remu(a, b uint64) uint64 {
	if b == 0 {
		return a
	}
	_, r := au_divrem_u(a, b)
	return r
}
func au_div(a, b uint64) uint64 {
	if b == 0 {
		return auOnes
	}
	if a == auMin64 && b == auOnes {
		return auMin64
	}
	na, nb := a>>63, b>>63
	ua, ub := a, b
	if na != 0 {
		ua = uint64(0) - a
	}
	if nb != 0 {
		ub = uint64(0) - b
	}
	q, _ := au_divrem_u(ua, ub)
	if (na ^ nb) != 0 {
		return uint64(0) - q
	}
	return q
}
func au_rem(a, b uint64) uint64 {
	if b == 0 {
		return a
	}
	if a == auMin64 && b == auOnes {
		return 0
	}
	na, nb := a>>63, b>>63
	ua, ub := a, b
	if na != 0 {
		ua = uint64(0) - a
	}
	if nb != 0 {
		ub = uint64(0) - b
	}
	_, r := au_divrem_u(ua, ub)
	if na != 0 {
		return uint64(0) - r
	}
	return r
}
func au_divw(a, b uint64) uint64  { return au_sext32(au_div(au_sext32(a), au_sext32(b))) }
func au_remw(a, b uint64) uint64  { return au_sext32(au_rem(au_sext32(a), au_sext32(b))) }
func au_divuw(a, b uint64) uint64 { return au_sext32(au_divu(a&0xffffffff, b&0xffffffff)) }
func au_remuw(a, b uint64) uint64 { return au_sext32(au_remu(a&0xffffffff, b&0xffffffff)) }
"""


def write_helpers():
    c = C_HELPERS.replace("AU_INLINE", "static inline")
    c = c.replace("#ifndef AU_INT_H", "#ifndef AU_INT_H")
    open(os.path.join(OUT, "c", "au_int.h"), "w").write(c)
    cp = C_HELPERS.replace("AU_INLINE", "inline")
    cp = cp.replace("#include <stdint.h>\n#include <stdbool.h>",
                    "#include <cstdint>\n\nnamespace archunits {")
    cp = cp.replace("#ifndef AU_INT_H\n#define AU_INT_H",
                    "#ifndef AU_INT_HPP\n#define AU_INT_HPP")
    cp = cp.replace("\n#endif\n", "\n}  // namespace archunits\n\n#endif\n")
    cp = cp.replace("au_b2u(bool b)", "au_b2u(bool b)")
    open(os.path.join(OUT, "cpp", "au_int.hpp"), "w").write(cp)
    open(os.path.join(OUT, "rust", "au_int.rs"), "w").write(RUST_HELPERS)
    open(os.path.join(OUT, "go", "helpers_int.go"), "w").write(GO_HELPERS)
    for lang, fname, text in (("java", "AuInt.java", JAVA_HELPERS),
                              ("python", "au_int.py", PY_HELPERS),
                              ("ruby", "au_int.rb", RB_HELPERS),
                              ("js", "au_int.js", JS_HELPERS)):
        d = os.path.join(OUT, lang)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, fname), "w").write(text)



JAVA_HELPERS = r'''// generated by scripts/build_arch_units_int.py
// The RV64 integer arch-opcodes as java.  A `long` is exactly 64 bits and
// two's complement, so it carries the pattern directly; unsignedness lives in
// the operations -- `>>>` for the logical shift, `Long.compareUnsigned` for
// the unsigned compare.  Shift counts are masked to the width RISC-V uses;
// au_sra / au_sraw are written out in unsigned bit operations; signed divide
// and remainder go through unsigned magnitudes so the sign rule is RISC-V's
// (truncate toward zero) and not the host language's.
public final class AuInt {
    private AuInt() { }

    static final long ONES  = -1L;                    // 0xffffffffffffffff
    static final long MIN64 = Long.MIN_VALUE;         // 0x8000000000000000
    static final long M32   = 0xffffffffL;

    public static long au_b2u(boolean b)       { return b ? 1L : 0L; }
    public static long au_sext32(long x)       { return (long) (int) x; }
    public static long au_add(long a, long b)  { return a + b; }
    public static long au_sub(long a, long b)  { return a - b; }
    public static long au_and(long a, long b)  { return a & b; }
    public static long au_or(long a, long b)   { return a | b; }
    public static long au_xor(long a, long b)  { return a ^ b; }
    public static long au_andn(long a, long b) { return a & ~b; }
    public static long au_mul(long a, long b)  { return a * b; }
    public static long au_addw(long a, long b) { return au_sext32(a + b); }
    public static long au_subw(long a, long b) { return au_sext32(a - b); }
    public static long au_mulw(long a, long b) { return au_sext32(a * b); }

    public static long au_sll(long a, long s)  { return a << (int) (s & 63L); }
    public static long au_srl(long a, long s)  { return a >>> (int) (s & 63L); }
    public static long au_sra(long a, long n) {
        int s = (int) (n & 63L);
        long r = a >>> s;
        long m = -(a >>> 63);
        return r | ((m << (63 - s)) << 1);
    }
    public static long au_sllw(long a, long n) {
        return au_sext32((a << (int) (n & 31L)) & M32);
    }
    public static long au_srlw(long a, long n) {
        return au_sext32((a & M32) >>> (int) (n & 31L));
    }
    public static long au_sraw(long a, long n) {
        int s = (int) (n & 31L);
        long r = (a & M32) >>> s;
        long m = -((a >>> 31) & 1L);
        r |= ((m << (31 - s)) << 1) & M32;
        return au_sext32(r);
    }

    public static long au_slt(long a, long b)  { return au_b2u(a < b); }
    public static long au_sltu(long a, long b) {
        return au_b2u(Long.compareUnsigned(a, b) < 0);
    }
    public static long au_eqz(long a) { return au_b2u(a == 0L); }
    public static long au_nez(long a) { return au_b2u(a != 0L); }
    public static long au_ltz(long a) { return au_b2u(a < 0L); }
    public static long au_gez(long a) { return au_b2u(a >= 0L); }
    public static long au_czeqz(long v, long c) { return c == 0L ? 0L : v; }
    public static long au_cznez(long v, long c) { return c != 0L ? 0L : v; }

    public static long au_divu(long a, long b) {
        return b == 0L ? ONES : Long.divideUnsigned(a, b);
    }
    public static long au_remu(long a, long b) {
        return b == 0L ? a : Long.remainderUnsigned(a, b);
    }
    public static long au_div(long a, long b) {
        if (b == 0L) return ONES;
        if (a == MIN64 && b == ONES) return MIN64;
        long na = a >>> 63, nb = b >>> 63;
        long ua = na != 0L ? -a : a, ub = nb != 0L ? -b : b;
        long q = Long.divideUnsigned(ua, ub);
        return (na ^ nb) != 0L ? -q : q;
    }
    public static long au_rem(long a, long b) {
        if (b == 0L) return a;
        if (a == MIN64 && b == ONES) return 0L;
        long na = a >>> 63, nb = b >>> 63;
        long ua = na != 0L ? -a : a, ub = nb != 0L ? -b : b;
        long r = Long.remainderUnsigned(ua, ub);
        return na != 0L ? -r : r;
    }
    public static long au_divw(long a, long b) {
        return au_sext32(au_div(au_sext32(a), au_sext32(b)));
    }
    public static long au_remw(long a, long b) {
        return au_sext32(au_rem(au_sext32(a), au_sext32(b)));
    }
    public static long au_divuw(long a, long b) {
        return au_sext32(au_divu(a & M32, b & M32));
    }
    public static long au_remuw(long a, long b) {
        return au_sext32(au_remu(a & M32, b & M32));
    }
}
'''

PY_HELPERS = r'''"""generated by scripts/build_arch_units_int.py

The RV64 integer arch-opcodes as python.  A python int is unbounded, so the
64-bit width is carried by an EXPLICIT MASK on every result that can leave it;
`au_s` reads a pattern signed.  Shift counts are masked to the width RISC-V
uses; au_sra / au_sraw are written out in unsigned bit operations; signed
divide and remainder go through unsigned magnitudes so the sign rule is
RISC-V's (truncate toward zero) and not python's (which floors).
"""

M64 = 0xffffffffffffffff
M32 = 0xffffffff
ONES = M64
MIN64 = 0x8000000000000000


def au_s(x):                       # the signed reading of a 64-bit pattern
    x &= M64
    return x - (1 << 64) if x >> 63 else x


def au_b2u(b):       return 1 if b else 0
def au_sext32(x):    return (x & M32) - (1 << 32) & M64 if (x >> 31) & 1 else x & M32
def au_add(a, b):    return (a + b) & M64
def au_sub(a, b):    return (a - b) & M64
def au_and(a, b):    return a & b
def au_or(a, b):     return a | b
def au_xor(a, b):    return a ^ b
def au_andn(a, b):   return a & (~b & M64)
def au_mul(a, b):    return (a * b) & M64
def au_addw(a, b):   return au_sext32((a + b) & M64)
def au_subw(a, b):   return au_sext32((a - b) & M64)
def au_mulw(a, b):   return au_sext32((a * b) & M64)
def au_sll(a, s):    return (a << (s & 63)) & M64
def au_srl(a, s):    return (a >> (s & 63)) & M64


def au_sra(a, n):
    s = n & 63
    r = a >> s
    m = (0 - (a >> 63)) & M64
    return (r | ((m << (63 - s) << 1) & M64)) & M64


def au_sllw(a, n):   return au_sext32(((a << (n & 31)) & M32))
def au_srlw(a, n):   return au_sext32(((a & M32) >> (n & 31)))


def au_sraw(a, n):
    s = n & 31
    r = (a & M32) >> s
    m = (0 - ((a >> 31) & 1)) & M64
    r |= ((m << (31 - s) << 1) & M32)
    return au_sext32(r & M32)


def au_slt(a, b):    return au_b2u(au_s(a) < au_s(b))
def au_sltu(a, b):   return au_b2u((a & M64) < (b & M64))
def au_eqz(a):       return au_b2u((a & M64) == 0)
def au_nez(a):       return au_b2u((a & M64) != 0)
def au_ltz(a):       return au_b2u(au_s(a) < 0)
def au_gez(a):       return au_b2u(au_s(a) >= 0)
def au_czeqz(v, c):  return 0 if (c & M64) == 0 else v
def au_cznez(v, c):  return 0 if (c & M64) != 0 else v


def au_divu(a, b):   return ONES if b == 0 else (a // b) & M64
def au_remu(a, b):   return a if b == 0 else (a % b) & M64


def au_div(a, b):
    if b == 0:
        return ONES
    if a == MIN64 and b == ONES:
        return MIN64
    na, nb = a >> 63, b >> 63
    ua = (0 - a) & M64 if na else a
    ub = (0 - b) & M64 if nb else b
    q = ua // ub
    return ((0 - q) & M64) if (na ^ nb) else (q & M64)


def au_rem(a, b):
    if b == 0:
        return a
    if a == MIN64 and b == ONES:
        return 0
    na, nb = a >> 63, b >> 63
    ua = (0 - a) & M64 if na else a
    ub = (0 - b) & M64 if nb else b
    r = ua % ub
    return ((0 - r) & M64) if na else (r & M64)


def au_divw(a, b):   return au_sext32(au_div(au_sext32(a), au_sext32(b)))
def au_remw(a, b):   return au_sext32(au_rem(au_sext32(a), au_sext32(b)))
def au_divuw(a, b):  return au_sext32(au_divu(a & M32, b & M32))
def au_remuw(a, b):  return au_sext32(au_remu(a & M32, b & M32))
'''

RB_HELPERS = r'''# generated by scripts/build_arch_units_int.py
#
# The RV64 integer arch-opcodes as ruby.  A ruby Integer is unbounded, so the
# 64-bit width is carried by an EXPLICIT MASK on every result that can leave
# it; +au_s+ reads a pattern signed.  Shift counts are masked to the width
# RISC-V uses; au_sra / au_sraw are written out in unsigned bit operations;
# signed divide and remainder go through unsigned magnitudes so the sign rule
# is RISC-V's (truncate toward zero) and not ruby's (which floors).

M64   = 0xffffffffffffffff
M32   = 0xffffffff
ONES  = M64
MIN64 = 0x8000000000000000

def au_s(x)                        # the signed reading of a 64-bit pattern
  x &= M64
  (x >> 63) == 1 ? x - (1 << 64) : x
end

def au_b2u(b)      = b ? 1 : 0
def au_sext32(x)   = ((x >> 31) & 1) == 1 ? (((x & M32) - (1 << 32)) & M64) : (x & M32)
def au_add(a, b)   = (a + b) & M64
def au_sub(a, b)   = (a - b) & M64
def au_and(a, b)   = a & b
def au_or(a, b)    = a | b
def au_xor(a, b)   = a ^ b
def au_andn(a, b)  = a & (~b & M64)
def au_mul(a, b)   = (a * b) & M64
def au_addw(a, b)  = au_sext32((a + b) & M64)
def au_subw(a, b)  = au_sext32((a - b) & M64)
def au_mulw(a, b)  = au_sext32((a * b) & M64)
def au_sll(a, s)   = (a << (s & 63)) & M64
def au_srl(a, s)   = (a >> (s & 63)) & M64

def au_sra(a, n)
  s = n & 63
  r = a >> s
  m = (0 - (a >> 63)) & M64
  (r | (((m << (63 - s)) << 1) & M64)) & M64
end

def au_sllw(a, n)  = au_sext32(((a << (n & 31)) & M32))
def au_srlw(a, n)  = au_sext32(((a & M32) >> (n & 31)))

def au_sraw(a, n)
  s = n & 31
  r = (a & M32) >> s
  m = (0 - ((a >> 31) & 1)) & M64
  r |= (((m << (31 - s)) << 1) & M32)
  au_sext32(r & M32)
end

def au_slt(a, b)   = au_b2u(au_s(a) < au_s(b))
def au_sltu(a, b)  = au_b2u((a & M64) < (b & M64))
def au_eqz(a)      = au_b2u((a & M64) == 0)
def au_nez(a)      = au_b2u((a & M64) != 0)
def au_ltz(a)      = au_b2u(au_s(a) < 0)
def au_gez(a)      = au_b2u(au_s(a) >= 0)
def au_czeqz(v, c) = (c & M64) == 0 ? 0 : v
def au_cznez(v, c) = (c & M64) != 0 ? 0 : v

def au_divu(a, b)  = b == 0 ? ONES : (a / b) & M64
def au_remu(a, b)  = b == 0 ? a : (a % b) & M64

def au_div(a, b)
  return ONES if b == 0
  return MIN64 if a == MIN64 && b == ONES
  na = a >> 63; nb = b >> 63
  ua = na == 1 ? ((0 - a) & M64) : a
  ub = nb == 1 ? ((0 - b) & M64) : b
  q = ua / ub
  (na ^ nb) == 1 ? ((0 - q) & M64) : (q & M64)
end

def au_rem(a, b)
  return a if b == 0
  return 0 if a == MIN64 && b == ONES
  na = a >> 63; nb = b >> 63
  ua = na == 1 ? ((0 - a) & M64) : a
  ub = nb == 1 ? ((0 - b) & M64) : b
  r = ua % ub
  na == 1 ? ((0 - r) & M64) : (r & M64)
end

def au_divw(a, b)  = au_sext32(au_div(au_sext32(a), au_sext32(b)))
def au_remw(a, b)  = au_sext32(au_rem(au_sext32(a), au_sext32(b)))
def au_divuw(a, b) = au_sext32(au_divu(a & M32, b & M32))
def au_remuw(a, b) = au_sext32(au_remu(a & M32, b & M32))
'''

JS_HELPERS = r''''use strict';
// generated by scripts/build_arch_units_int.py
//
// The RV64 integer arch-opcodes as javascript.  Every value is a BigInt and
// the 64-bit width is carried by an EXPLICIT MASK on every result that can
// leave it; `au_s` reads a pattern signed.  BigInt and not Number: a Number
// is an IEEE double and would lose the low bits.  Shift counts are masked to
// the width RISC-V uses; au_sra / au_sraw are written out in unsigned bit
// operations; signed divide and remainder go through unsigned magnitudes so
// the sign rule is RISC-V's (truncate toward zero).

const M64 = 0xffffffffffffffffn;
const M32 = 0xffffffffn;
const ONES = M64;
const MIN64 = 0x8000000000000000n;

function au_s(x) { x &= M64; return (x >> 63n) ? x - (1n << 64n) : x; }

const au_b2u = (b) => (b ? 1n : 0n);
const au_sext32 = (x) =>
  ((x >> 31n) & 1n) ? (((x & M32) - (1n << 32n)) & M64) : (x & M32);
const au_add = (a, b) => (a + b) & M64;
const au_sub = (a, b) => (a - b) & M64;
const au_and = (a, b) => a & b;
const au_or = (a, b) => a | b;
const au_xor = (a, b) => a ^ b;
const au_andn = (a, b) => a & (~b & M64);
const au_mul = (a, b) => (a * b) & M64;
const au_addw = (a, b) => au_sext32((a + b) & M64);
const au_subw = (a, b) => au_sext32((a - b) & M64);
const au_mulw = (a, b) => au_sext32((a * b) & M64);
const au_sll = (a, s) => (a << (s & 63n)) & M64;
const au_srl = (a, s) => (a >> (s & 63n)) & M64;

function au_sra(a, n) {
  const s = n & 63n;
  const r = a >> s;
  const m = (0n - (a >> 63n)) & M64;
  return (r | (((m << (63n - s)) << 1n) & M64)) & M64;
}

const au_sllw = (a, n) => au_sext32((a << (n & 31n)) & M32);
const au_srlw = (a, n) => au_sext32((a & M32) >> (n & 31n));

function au_sraw(a, n) {
  const s = n & 31n;
  let r = (a & M32) >> s;
  const m = (0n - ((a >> 31n) & 1n)) & M64;
  r |= ((m << (31n - s)) << 1n) & M32;
  return au_sext32(r & M32);
}

const au_slt = (a, b) => au_b2u(au_s(a) < au_s(b));
const au_sltu = (a, b) => au_b2u((a & M64) < (b & M64));
const au_eqz = (a) => au_b2u((a & M64) === 0n);
const au_nez = (a) => au_b2u((a & M64) !== 0n);
const au_ltz = (a) => au_b2u(au_s(a) < 0n);
const au_gez = (a) => au_b2u(au_s(a) >= 0n);
const au_czeqz = (v, c) => ((c & M64) === 0n ? 0n : v);
const au_cznez = (v, c) => ((c & M64) !== 0n ? 0n : v);

const au_divu = (a, b) => (b === 0n ? ONES : (a / b) & M64);
const au_remu = (a, b) => (b === 0n ? a : (a % b) & M64);

function au_div(a, b) {
  if (b === 0n) return ONES;
  if (a === MIN64 && b === ONES) return MIN64;
  const na = a >> 63n, nb = b >> 63n;
  const ua = na ? (0n - a) & M64 : a, ub = nb ? (0n - b) & M64 : b;
  const q = ua / ub;
  return (na ^ nb) ? (0n - q) & M64 : q & M64;
}

function au_rem(a, b) {
  if (b === 0n) return a;
  if (a === MIN64 && b === ONES) return 0n;
  const na = a >> 63n, nb = b >> 63n;
  const ua = na ? (0n - a) & M64 : a, ub = nb ? (0n - b) & M64 : b;
  const r = ua % ub;
  return na ? (0n - r) & M64 : r & M64;
}

const au_divw = (a, b) => au_sext32(au_div(au_sext32(a), au_sext32(b)));
const au_remw = (a, b) => au_sext32(au_rem(au_sext32(a), au_sext32(b)));
const au_divuw = (a, b) => au_sext32(au_divu(a & M32, b & M32));
const au_remuw = (a, b) => au_sext32(au_remu(a & M32, b & M32));

module.exports = {
  au_s, au_b2u, au_sext32, au_add, au_sub, au_and, au_or, au_xor, au_andn,
  au_mul, au_addw, au_subw, au_mulw, au_sll, au_srl, au_sra, au_sllw,
  au_srlw, au_sraw, au_slt, au_sltu, au_eqz, au_nez, au_ltz, au_gez,
  au_czeqz, au_cznez, au_divu, au_remu, au_div, au_rem, au_divw, au_remw,
  au_divuw, au_remuw,
};
'''


def write_glue(record):
    names = [(u["name"], u["n_params"], u["guarded"]) for u in record]

    h = ["/* generated by scripts/build_arch_units_int.py */",
         "#ifndef ARCH_UNITS_INT_H", "#define ARCH_UNITS_INT_H", "",
         "#include <stdint.h>", "#include <stdbool.h>",
         '#include "au_int.h"', ""]
    for n, np, g in names:
        a = ", ".join(["uint64_t"] * np) or "void"
        h.append("uint64_t %s(%s);" % (n, a))
        if g:
            h.append("uint64_t %s_trap(%s);" % (n, a))
    h += ["", "#endif"]
    open(os.path.join(OUT, "c", "arch_units_int.h"),
         "w").write("\n".join(h) + "\n")

    hp = ["// generated by scripts/build_arch_units_int.py",
          "#ifndef ARCH_UNITS_INT_HPP", "#define ARCH_UNITS_INT_HPP", "",
          "#include <cstdint>", '#include "au_int.hpp"', "",
          "namespace archunits {", ""]
    for n, np, g in names:
        a = ", ".join(["uint64_t"] * np)
        hp.append("uint64_t %s(%s);" % (n, a))
        if g:
            hp.append("uint64_t %s_trap(%s);" % (n, a))
    hp += ["", "}  // namespace archunits", "", "#endif"]
    open(os.path.join(OUT, "cpp", "arch_units_int.hpp"),
         "w").write("\n".join(hp) + "\n")

    lib = ["//! The integer-only RISC-V arch-units as rust.",
           "//! Generated by scripts/build_arch_units_int.py.",
           "#![allow(non_snake_case, dead_code)]", "",
           '#[path = "au_int.rs"]', "mod au_int;", "pub use au_int::*;", ""]
    for n, np, g in names:
        lib.append('#[path = "%s.rs"]' % n)
        lib.append("pub mod %s;" % n)
    open(os.path.join(OUT, "rust", "lib_int.rs"),
         "w").write("\n".join(lib) + "\n")

    idx = {u["name"]: {l: u["languages"][l]["entry"]
                       for l in ("c", "cpp", "rust", "go")}
           for u in record}
    json.dump({"entries": idx},
              open(os.path.join(OUT, "_index_int.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
