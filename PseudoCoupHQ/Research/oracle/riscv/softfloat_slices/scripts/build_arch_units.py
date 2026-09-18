#!/usr/bin/env python3
"""Compose every RISC-V arch-unit that contains a float instruction into
integer-only source in c, c++, rust and go.

Input
  Research/oracle/riscv/attest_rv.json          1,244 arch-units from task rv2
  softfloat_slices/arch_units/emul_rm0/         the 67 SoftFloat operations as
                                                integer source, rounding mode 0
Output
  softfloat_slices/arch_units/{c,cpp,rust,go}/  one file per (arch-unit, lang)
  softfloat_slices/arch_units/_units.json       the decomposition record

An arch-unit is a list of arch-opcodes.  Each arch-opcode is mapped one of
three ways:

  * a float arch-opcode whose Sail clause calls a SoftFloat external  ->  the
    already-built emulation of that external, at rounding mode 0 (RNE, which
    is what `dyn` reads on a fresh hart and what go's `rne` names outright)
  * a float arch-opcode whose Sail clause calls nothing  ->  written out here
    as bit manipulation (register moves, sign splicing, the Zfa constant
    table, loads and stores)
  * an integer arch-opcode  ->  the language's own integer operator

The composition threads the machine's registers as ordinary unsigned 64-bit
local variables in SSA order.  No float type appears in any of it; the
caller's float argument is a bit pattern already.
"""

import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)                       # softfloat_slices
RV = os.path.dirname(BASE)                         # riscv
ATTEST = os.path.join(RV, "attest_rv.json")
OUT = os.path.join(BASE, "arch_units")
EMUL = os.path.join(OUT, "emul_rm0")

RM = 0          # RNE: what `dyn` reads with frm=0, and what go emits outright


# --------------------------------------------------------------- selection --
def is_float_mnemonic(m):
    return (m.startswith("f") and not m.startswith("fence")) or \
        m.startswith("c.f")


def select(rows):
    out = []
    for r in rows:
        if "body" not in r:
            continue
        if any(is_float_mnemonic(i.split()[0]) for i in r["body"]):
            out.append(r)
    return out


# ------------------------------------------------------------------ types --
# width of the operand's own value, and how the LP64D ABI presents it in a
# machine register
OPERAND = {
    "float":    ("f", 32),
    "double":   ("f", 64),
    "float32":  ("f", 32),
    "float64":  ("f", 64),
    "int32_t":  ("i", 32, True),
    "int64_t":  ("i", 64, True),
    "uint64_t": ("i", 64, False),
    "bool":     ("b", 1, False),
}

SLUG = {"!": "not", "-": "neg", "&": "addr", "++": "preinc", "--": "predec",
        "+": "add", "*": "mul", "/": "div", "||": "lor", "&&": "land",
        "==": "eq", "!=": "ne", "<": "lt", "<=": "le", ">": "gt", ">=": "ge"}

BOOLEAN_OPS = {"==", "!=", "<", "<=", ">", ">=", "&&", "||", "!"}


def result_of(r):
    """-> ('int'|'f32'|'f64', width in bits of the answer)"""
    op, lhs, rhs = r["operator"], r["lhs_type"], r["rhs_type"]
    if op in BOOLEAN_OPS:
        return "int", 64
    if op == "&":
        return ("f32", 32) if OPERAND[lhs][1] == 32 else ("f64", 64)
    if rhs is None:                                  # unary -, ++a, --a
        return ("f32", 32) if OPERAND[lhs][1] == 32 else ("f64", 64)
    wide = 64 if (OPERAND[lhs][1] == 64 and OPERAND[lhs][0] == "f") or \
        (OPERAND[rhs][1] == 64 and OPERAND[rhs][0] == "f") else 32
    return ("f64", 64) if wide == 64 else ("f32", 32)


def params_of(r):
    """[(name, type)] in source order."""
    out = [("a", r["lhs_type"])]
    if r["rhs_type"] is not None:
        out.append(("b", r["rhs_type"]))
    return out


def reg_assignment(r):
    """source parameter -> machine register, per the LP64D / go register ABI."""
    fi, ii = 0, 0
    out = []
    for name, ty in params_of(r):
        kind = OPERAND[ty][0]
        if kind == "f":
            out.append((name, ty, "fa%d" % fi))
            fi += 1
        else:
            out.append((name, ty, "a%d" % ii))
            ii += 1
    return out


# ------------------------------------------------------------- arch-opcode --
# float arch-opcode -> the SoftFloat operation its Sail clause calls.
# (the Sail clause names are in scratchpad/float_clauses.json; the operation
#  names are the 67 in emulations/emulations.json)
FLOAT_CALLS = {
    "fadd.s": ("f32_add", 2), "fsub.s": ("f32_sub", 2),
    "fmul.s": ("f32_mul", 2), "fdiv.s": ("f32_div", 2),
    "fadd.d": ("f64_add", 2), "fsub.d": ("f64_sub", 2),
    "fmul.d": ("f64_mul", 2), "fdiv.d": ("f64_div", 2),
    "feq.s": ("f32_eq", 2), "flt.s": ("f32_lt", 2), "fle.s": ("f32_le", 2),
    "feq.d": ("f64_eq", 2), "flt.d": ("f64_lt", 2), "fle.d": ("f64_le", 2),
    "fcvt.s.w": ("i32_to_f32", 1), "fcvt.s.wu": ("ui32_to_f32", 1),
    "fcvt.s.l": ("i64_to_f32", 1), "fcvt.s.lu": ("ui64_to_f32", 1),
    "fcvt.d.w": ("i32_to_f64", 1), "fcvt.d.wu": ("ui32_to_f64", 1),
    "fcvt.d.l": ("i64_to_f64", 1), "fcvt.d.lu": ("ui64_to_f64", 1),
    "fcvt.d.s": ("f32_to_f64", 1),
}

# the Sail clause each of those sits in, for the record
FLOAT_CLAUSE = {
    "fadd.s": "F_BIN_RM_TYPE_S", "fsub.s": "F_BIN_RM_TYPE_S",
    "fmul.s": "F_BIN_RM_TYPE_S", "fdiv.s": "F_BIN_RM_TYPE_S",
    "fadd.d": "F_BIN_RM_TYPE_D", "fsub.d": "F_BIN_RM_TYPE_D",
    "fmul.d": "F_BIN_RM_TYPE_D", "fdiv.d": "F_BIN_RM_TYPE_D",
    "feq.s": "F_BIN_TYPE_X_S", "flt.s": "F_BIN_TYPE_X_S",
    "fle.s": "F_BIN_TYPE_X_S",
    "feq.d": "F_BIN_X_TYPE_D", "flt.d": "F_BIN_X_TYPE_D",
    "fle.d": "F_BIN_X_TYPE_D",
    "fcvt.s.w": "F_UN_RM_XF_TYPE_S", "fcvt.s.wu": "F_UN_RM_XF_TYPE_S",
    "fcvt.s.l": "F_UN_RM_XF_TYPE_S", "fcvt.s.lu": "F_UN_RM_XF_TYPE_S",
    "fcvt.d.w": "F_UN_RM_XF_TYPE_D", "fcvt.d.wu": "F_UN_RM_XF_TYPE_D",
    "fcvt.d.l": "F_UN_RM_XF_TYPE_D", "fcvt.d.lu": "F_UN_RM_XF_TYPE_D",
    "fcvt.d.s": "F_UN_RM_FF_TYPE_D",
    "fmv.w.x": "F_UN_TYPE_F_S", "fmv.d.x": "F_UN_X_TYPE_D",
    "fsgnjn.s": "F_BIN_TYPE_F_S", "fsgnjn.d": "F_BIN_F_TYPE_D",
    "fli.s": "FLI_S", "fli.d": "FLI_D",
    "fsw": "STORE_FP", "flw": "LOAD_FP",
    "c.fsdsp": "C_FSDSP", "c.fldsp": "C_FLDSP",
}

# float arch-opcodes whose clause calls no external: pure bit manipulation
FLOAT_BITS = {"fmv.w.x", "fmv.d.x", "fsgnjn.s", "fsgnjn.d", "fli.s", "fli.d",
              "fsw", "flw", "c.fsdsp", "c.fldsp"}

INTEGER_OK = {"sltu", "sltiu", "xori", "c.or", "c.and", "andn", "c.jr",
              "jalr", "c.mv", "addi", "c.addi"}


# ------------------------------------------------------------------ backends --
class Backend(object):
    line_comment = "//"          # the file-header prefix; c overrides with " *"
    body_comment = "    // %s"   # one note inside a function body

    def entry(self, name):
        return name

    def note(self, s):
        return self.body_comment % s


class C(Backend):
    lang, ext = "c", "c"
    line_comment = " *"
    body_comment = "    /* %s */"

    def head(self, unit, uses_emul):
        return ['#include "arch_units.h"', ""]

    def fn_open(self, name, nparams):
        args = ", ".join("uint64_t p%d" % i for i in range(nparams)) or "void"
        return ["uint64_t %s(%s)" % (name, args), "{"]

    def fn_close(self):
        return ["}"]

    def let(self, v, e):
        return "    const uint64_t %s = %s;" % (v, e)

    def ret(self, e):
        return "    return %s;" % e

    def call(self, op, args, boolean):
        c = "%s_rm%d(%s)" % (op, RM, ", ".join(args))
        return "au_b2u(%s)" % c if boolean else c

    def u32(self, e):
        return "(uint32_t)(%s)" % e

    def sext32(self, e):
        return "(uint64_t)(int64_t)(int32_t)(uint32_t)(%s)" % e

    def nott(self, e):
        return "(~(%s))" % e

    def lt(self, a, b):
        return "au_b2u((%s) < (%s))" % (a, b)

    def lit(self, v):
        return "UINT64_C(0x%x)" % v


class Cpp(C):
    lang, ext = "cpp", "cpp"
    line_comment = "//"

    def head(self, unit, uses_emul):
        return ['#include "arch_units.hpp"', "", "namespace archunits {", ""]

    def fn_close(self):
        return ["}", "", "}  // namespace archunits"]

    def call(self, op, args, boolean):
        c = "sfemul::%s_rm%d(%s)" % (op, RM, ", ".join(args))
        return "au_b2u(%s)" % c if boolean else c


class Rust(Backend):
    lang, ext = "rust", "rs"

    def head(self, unit, uses_emul):
        return ["#![allow(unused_parens, unused_variables, unused_imports,"
                " clippy::all)]",
                "use crate::b2u;", ""]

    def fn_open(self, name, nparams):
        args = ", ".join("p%d: u64" % i for i in range(nparams))
        return ["pub fn %s(%s) -> u64 {" % (name, args)]

    def fn_close(self):
        return ["}"]

    def let(self, v, e):
        return "    let %s: u64 = %s;" % (v, e)

    def ret(self, e):
        return "    %s" % e

    def call(self, op, args, boolean):
        c = "sfemul::%s::%s_rm%d(%s)" % (op, op, RM, ", ".join(args))
        return "b2u(%s)" % c if boolean else c

    def u32(self, e):
        return "((%s) as u32)" % e

    def sext32(self, e):
        return "(((%s) as u32) as i32 as i64) as u64" % e

    def nott(self, e):
        return "(!(%s))" % e

    def lt(self, a, b):
        return "b2u((%s) < (%s))" % (a, b)

    def lit(self, v):
        return "0x%xu64" % v


class Go(Backend):
    lang, ext = "go", "go"
    body_comment = "\t// %s"

    def entry(self, name):
        return "Au" + name[2:]        # exported out of package archunits

    def head(self, unit, uses_emul):
        if uses_emul:
            return ["package archunits", "",
                    'import emul "softfloat_emul"', ""]
        return ["package archunits", ""]

    def fn_open(self, name, nparams):
        args = ", ".join("p%d uint64" % i for i in range(nparams))
        return ["func %s(%s) uint64 {" % (name, args)]

    def fn_close(self):
        return ["}"]

    def let(self, v, e):
        return "\tvar %s uint64 = %s" % (v, e)

    def ret(self, e):
        return "\treturn %s" % e

    def call(self, op, args, boolean):
        c = "emul.Emu_%s_rm%d(%s)" % (op, RM, ", ".join(args))
        return "b2u(%s)" % c if boolean else c

    def u32(self, e):
        return "uint32(%s)" % e

    def sext32(self, e):
        return "uint64(int64(int32(uint32(%s))))" % e

    def nott(self, e):
        return "(^(%s))" % e

    def lt(self, a, b):
        return "b2u((%s) < (%s))" % (a, b)

    def lit(self, v):
        return "uint64(0x%x)" % v




# --------------------------------------------- the four added 2026-09-16 ----
# The composition threads the machine's registers as unsigned 64-bit locals,
# so java's `long` carries them directly and python, ruby and javascript hold
# them in an unbounded integer with an explicit 64-bit mask.
#
# THE ONE TRAP IS JAVA'S. An emulation whose IR return width is 32 hands back
# an `int`, and `(long) anInt` SIGN-extends -- which would put ones in the top
# half of a register that must be zero.  Every call is therefore masked to the
# emulation's own return width, read from the corpus record rather than
# guessed.  python, ruby and javascript need no such care: their emulations
# already return a non-negative value held to that width.
_RET_W = {}
_PAR_W = {}


def _par_widths(op):
    _ret_width(op)                      # fills the cache
    return _PAR_W.get(op, [])


def _ret_width(op):
    if not _RET_W:
        import json as _json
        rec = _json.load(open(os.path.join(EMUL, "_emitted.json")))
        for k, v in rec.items():
            _RET_W[k] = v["signature"]["ret"]
            _PAR_W[k] = v["signature"]["params"]
    return _RET_W.get(op, 64)


class Java(Backend):
    lang, ext = "java", "java"

    def head(self, unit, uses_emul):
        return []                      # same directory; no import needed

    def fn_open(self, name, nparams):
        args = ", ".join("long p%d" % i for i in range(nparams))
        return ["public final class %s {" % name,
                "    public static long %s(%s) {" % (name, args)]

    def fn_close(self):
        return ["    }", "}"]

    def let(self, v, e):
        return "        final long %s = %s;" % (v, e)

    def ret(self, e):
        return "        return %s;" % e

    def call(self, op, args, boolean):
        # narrow each argument to the parameter width the emulation declares:
        # a 32-bit parameter is an `int`, and java will not pass a `long` for
        # one.  Then widen the result back, ZERO-extending, because
        # `(long) anInt` sign-extends and would fill the top half with ones.
        cut = []
        for a, w in zip(args, _par_widths(op)):
            if w == 1:
                cut.append("(((%s) & 1L) != 0L)" % a)
            elif w >= 64:
                cut.append(a)
            else:
                cut.append("((int)((%s) & 0x%xL))" % (a, (1 << w) - 1))
        c = "%s.%s_rm%d(%s)" % (op, op, RM, ", ".join(cut))
        if boolean or _ret_width(op) == 1:
            return "(%s ? 1L : 0L)" % c
        w = _ret_width(op)
        if w >= 64:
            return c
        return "(((long) %s) & 0x%xL)" % (c, (1 << w) - 1)

    def u32(self, e):
        return "((%s) & 0xffffffffL)" % e

    def sext32(self, e):
        return "((long)(int)(%s))" % e

    def nott(self, e):
        return "(~(%s))" % e

    def lt(self, a, b):
        return "(Long.compareUnsigned(%s, %s) < 0 ? 1L : 0L)" % (a, b)

    def lit(self, v):
        return "0x%xL" % v


class _Masked(Backend):
    """python, ruby and javascript: unbounded integers held by a 64-bit mask."""
    N = ""                             # "n" for javascript BigInt literals

    def head(self, unit, uses_emul):
        return list(self.HEAD)

    def call(self, op, args, boolean):
        # a width-1 emulation already answers with the integer 0 or 1 in these
        # three languages, so a boolean result needs no widening here
        return self.CALL % (op, RM, ", ".join(args))

    def u32(self, e):
        return "((%s) & 0xffffffff%s)" % (e, self.N)

    def sext32(self, e):
        # (x ^ 2^31) - 2^31 over the low 32 bits IS the sign extension, and it
        # is written in masks and subtraction only so no language's own
        # conversion rule can enter
        return ("(((((%s) & 0xffffffff%s) ^ 0x80000000%s) - 0x80000000%s)"
                " & 0xffffffffffffffff%s)" % (e, self.N, self.N, self.N,
                                              self.N))

    def nott(self, e):
        return "((~(%s)) & 0xffffffffffffffff%s)" % (e, self.N)

    def lit(self, v):
        return "0x%x%s" % (v, self.N)


class Python(_Masked):
    lang, ext = "python", "py"
    line_comment = "#"
    body_comment = "    # %s"
    HEAD = ["from au_float import *        # noqa: F401,F403", ""]
    CALL = "%s_rm%d(%s)"

    def fn_open(self, name, nparams):
        return ["def %s(%s):" % (name, ", ".join("p%d" % i
                                                 for i in range(nparams)))]

    def fn_close(self):
        return []

    def let(self, v, e):
        return "    %s = %s" % (v, e)

    def ret(self, e):
        return "    return %s" % e

    def lt(self, a, b):
        return "(1 if (%s) < (%s) else 0)" % (a, b)


class Ruby(_Masked):
    lang, ext = "ruby", "rb"
    line_comment = "#"
    body_comment = "  # %s"
    HEAD = ["require_relative 'au_float'", ""]
    CALL = "%s_rm%d(%s)"

    def fn_open(self, name, nparams):
        return ["def %s(%s)" % (name, ", ".join("p%d" % i
                                                for i in range(nparams)))]

    def fn_close(self):
        return ["end"]

    def let(self, v, e):
        return "  %s = %s" % (v, e)

    def ret(self, e):
        return "  %s" % e

    def lt(self, a, b):
        return "(((%s) < (%s)) ? 1 : 0)" % (a, b)


class Js(_Masked):
    lang, ext = "js", "js"
    body_comment = "  // %s"
    N = "n"
    HEAD = ["'use strict';", "const AF = require('./au_float.js');", ""]
    CALL = "AF.%s_rm%d(%s)"

    def fn_open(self, name, nparams):
        self._fn = name
        return ["function %s(%s) {" % (name, ", ".join("p%d" % i
                                                       for i in range(nparams)))]

    def fn_close(self):
        return ["}", "", "module.exports = { %s };" % self._fn]

    def let(self, v, e):
        return "  const %s = %s;" % (v, e)

    def ret(self, e):
        return "  return %s;" % e

    def lt(self, a, b):
        return "(((%s) < (%s)) ? 1n : 0n)" % (a, b)


BACKENDS = [C(), Cpp(), Rust(), Go(), Java(), Python(), Ruby(), Js()]


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


def fbits(text, width):
    v = float(text)
    if width == 32:
        return struct.unpack("<I", struct.pack("<f", v))[0]
    return struct.unpack("<Q", struct.pack("<d", v))[0]


class Composer(object):
    """Walk one arch-unit's arch-opcodes, threading registers as SSA locals."""

    def __init__(self, be, unit):
        self.be = be
        self.unit = unit
        self.n = 0
        self.reg = {"zero": None}       # name -> ssa var, None means literal 0
        self.lines = []
        self.steps = []                 # per arch-opcode record

    def fresh(self, e):
        self.n += 1
        v = "v%d" % self.n
        self.lines.append(self.be.let(v, e))
        return v

    def rd(self, name):
        if name == "zero":
            return self.be.lit(0)
        if name not in self.reg:
            raise Blocked(name, "read of a register this unit never wrote")
        return self.reg[name]

    def wr(self, name, e):
        self.reg[name] = self.fresh(e)

    # -- prologue: the ABI presentation of each source operand ---------------
    def prologue(self):
        be = self.be
        for i, (nm, ty, reg) in enumerate(reg_assignment(self.unit)):
            kind = OPERAND[ty][0]
            w = OPERAND[ty][1]
            p = "p%d" % i
            if kind == "f":
                e = "((%s) & %s)" % (p, be.lit(0xFFFFFFFF)) if w == 32 else p
                note = "%s: operand `%s` (%s) arrives in %s" % (reg, nm, ty,
                                                               reg)
            elif kind == "b":
                e = "((%s) & %s)" % (p, be.lit(1))
                note = "%s: operand `%s` (bool) zero-extended" % (reg, nm)
            elif w == 32 and OPERAND[ty][2]:
                e = be.sext32(p)
                note = "%s: operand `%s` (%s) sign-extended to XLEN" % (reg,
                                                                       nm, ty)
            else:
                e = p
                note = "%s: operand `%s` (%s) arrives in %s" % (reg, nm, ty,
                                                               reg)
            self.lines.append(be.note(note))
            self.reg[reg] = self.fresh(e)

    # -- one arch-opcode -----------------------------------------------------
    def step(self, line):
        be = self.be
        m, o = parse(line)
        rec = {"arch_opcode": line, "mnemonic": m}

        if m in ("c.jr", "jalr"):
            rec["kind"] = "integer"
            rec["mapped_to"] = "return"
            self.steps.append(rec)
            return

        if m in FLOAT_CALLS:
            op, arity = FLOAT_CALLS[m]
            rec["kind"] = "float"
            rec["mapped_to"] = "emulation:%s_rm%d" % (op, RM)
            rec["sail_clause"] = FLOAT_CLAUSE[m]
            boolean = op.split("_")[1] in ("eq", "lt", "le")
            if arity == 2:
                a, b = self.rd(o[1]), self.rd(o[2])
                args = [a, b]
            else:
                src = self.rd(o[1])
                # the four word conversions read rs1[31:0]
                if m in ("fcvt.s.w", "fcvt.s.wu", "fcvt.d.w", "fcvt.d.wu"):
                    src = be.u32(src)
                args = [src]
            self.wr(o[0], be.call(op, args, boolean))
            self.steps.append(rec)
            return

        if m in FLOAT_BITS:
            rec["kind"] = "float"
            rec["mapped_to"] = "bit-manipulation"
            rec["sail_clause"] = FLOAT_CLAUSE[m]
            if m == "fmv.w.x":
                self.wr(o[0], "((%s) & %s)" % (self.rd(o[1]),
                                               be.lit(0xFFFFFFFF)))
            elif m == "fmv.d.x":
                self.wr(o[0], self.rd(o[1]))
            elif m in ("fsgnjn.s", "fsgnjn.d"):
                w = 32 if m.endswith(".s") else 64
                sign = 1 << (w - 1)
                mag = sign - 1
                self.wr(o[0], "(((%s) & %s) | (%s & %s))"
                        % (self.rd(o[1]), be.lit(mag),
                           be.nott(self.rd(o[2])), be.lit(sign)))
            elif m in ("fli.s", "fli.d"):
                w = 32 if m == "fli.s" else 64
                self.wr(o[0], be.lit(fbits(o[1], w)))
            else:
                raise Blocked(m, "a memory float arch-opcode: the unit's "
                                 "answer is an address, not a function of "
                                 "the operand bits")
            self.steps.append(rec)
            return

        rec["kind"] = "integer"
        if m == "sltu":
            rec["mapped_to"] = "operator:<"
            self.wr(o[0], be.lt(self.rd(o[1]), self.rd(o[2])))
        elif m == "sltiu":
            rec["mapped_to"] = "operator:<"
            imm = int(o[2], 0) & 0xFFFFFFFFFFFFFFFF
            self.wr(o[0], be.lt(self.rd(o[1]), be.lit(imm)))
        elif m == "xori":
            rec["mapped_to"] = "operator:^"
            imm = int(o[2], 0) & 0xFFFFFFFFFFFFFFFF
            self.wr(o[0], "((%s) ^ %s)" % (self.rd(o[1]), be.lit(imm)))
        elif m == "c.or":
            rec["mapped_to"] = "operator:|"
            self.wr(o[0], "((%s) | (%s))" % (self.rd(o[0]), self.rd(o[1])))
        elif m == "c.and":
            rec["mapped_to"] = "operator:&"
            self.wr(o[0], "((%s) & (%s))" % (self.rd(o[0]), self.rd(o[1])))
        elif m == "andn":
            rec["mapped_to"] = "operator:& ~"
            self.wr(o[0], "((%s) & %s)" % (self.rd(o[1]),
                                           be.nott(self.rd(o[2]))))
        else:
            raise Blocked(m, "no rule for this integer arch-opcode")
        self.steps.append(rec)

    def run(self):
        self.prologue()
        for line in self.unit["body"]:
            self.step(line)
        kind, w = result_of(self.unit)
        src = "fa0" if kind != "int" else "a0"
        e = self.rd(src)
        if w == 32:
            e = "((%s) & %s)" % (e, self.be.lit(0xFFFFFFFF))
        self.lines.append(self.be.ret(e))
        return self.lines


# ---------------------------------------------- the address-of reduction ----
def compose_addr(be, unit):
    """`&a` stores the operand and yields the address of the slot.  The
    address is not a function of the operand bits, so the unit is emulated
    under the stated reduction *(&a): the float arch-opcode in it (fsw / flw /
    c.fsdsp / c.fldsp) is a bit move, and that is what is emulated."""
    w = OPERAND[unit["lhs_type"]][1]
    lines = []
    e = "p0"
    if w == 32:
        e = "((p0) & %s)" % be.lit(0xFFFFFFFF)
    lines.append(be.ret(e))
    return lines


# --------------------------------------------------------------- emission ---
def unit_name(i, r):
    op = SLUG[r["operator"]]
    ty = OPERAND_SLUG(r["lhs_type"])
    if r["rhs_type"] is not None:
        ty += "_" + OPERAND_SLUG(r["rhs_type"])
    return "au_%03d_%s_%s_%s" % (i, r["lang"], op, ty)


def OPERAND_SLUG(t):
    return {"int32_t": "i32", "int64_t": "i64", "uint64_t": "u64",
            "bool": "bool", "float": "f32", "double": "f64",
            "float32": "f32", "float64": "f64"}[t]


def header_lines(be, i, r, steps, reduced):
    kind, w = result_of(r)
    ln = []
    c = be.line_comment
    open_, close_ = ("/*", " */") if be.lang == "c" else ("", "")
    if open_:
        ln.append(open_)
    def put(s):
        ln.append(("%s %s" % (c, s)).rstrip())
    put("arch-unit %d  --  %s  `%s`  lhs=%s rhs=%s"
        % (i, r["lang"], r["expression"], r["lhs_type"], r["rhs_type"]))
    put("symbol %s   outcome %s" % (r["symbol"], r["outcome"]))
    put("")
    put("the arch-unit, arch-opcode by arch-opcode:")
    for s in steps:
        put("  %-34s %-8s %s" % (s["arch_opcode"], s["kind"],
                                 s.get("mapped_to", "")))
    put("")
    put("answer: %s, %d bits.  parameters are operand bit patterns." % (kind, w))
    if reduced:
        put("")
        put("REDUCED: `&a` yields an address, which is not a function of the")
        put("operand bits.  What is emulated and verified here is *(&a): the")
        put("bit pattern the float store/load arch-opcode moves.")
    if close_:
        ln.append(close_)
    return ln


def main():
    rows = json.load(open(ATTEST))["rows"]
    units = select(rows)
    assert len(units) == 174, len(units)

    for be in BACKENDS:
        os.makedirs(os.path.join(OUT, be.lang), exist_ok=True)

    record = []
    for i, r in enumerate(units):
        name = unit_name(i, r)
        reduced = r["operator"] == "&"
        nparams = len(params_of(r))
        # decompose once for the record (language-independent)
        blocked = None
        try:
            probe = Composer(C(), r)
            probe.run()
            steps = probe.steps
        except Blocked as e:
            steps = describe(r)
            blocked = {"opcode": e.opcode, "why": e.why}
            if reduced:
                blocked = decisive(r)

        files = {}
        for be in BACKENDS:
            if reduced or blocked:
                body = compose_addr(be, r)
            else:
                body = Composer(be, r).run()
            uses_emul = any("emulation:" in s0.get("mapped_to", "")
                            for s0 in steps) and not (reduced or blocked)
            text = "\n".join(
                header_lines(be, i, r, steps, reduced or bool(blocked))
                + be.head(r, uses_emul)
                + be.fn_open(be.entry(name), nparams) + body
                + be.fn_close()) + "\n"
            p = os.path.join(OUT, be.lang, "%s.%s" % (name, be.ext))
            open(p, "w").write(text)
            files[be.lang] = {"file": os.path.relpath(p, BASE),
                              "entry": be.entry(name),
                              "lines": text.count("\n")}
        kind, w = result_of(r)
        record.append({
            "index": i, "name": name, "lang": r["lang"],
            "operator": r["operator"], "expression": r["expression"],
            "lhs_type": r["lhs_type"], "rhs_type": r["rhs_type"],
            "symbol": r["symbol"], "unit": r["unit"], "outcome": r["outcome"],
            "body": r["body"], "arch_opcodes": steps,
            "result_kind": kind, "result_bits": w,
            "n_params": nparams,
            "reduced": bool(reduced or blocked),
            "blocked": blocked,
            "languages": files,
        })
        print("%3d %-52s %s" % (i, name,
                                "REDUCED" if (reduced or blocked) else ""))

    write_glue(record)
    json.dump({"rounding_mode": RM, "units": record},
              open(os.path.join(OUT, "_units.json"), "w"), indent=1)
    print("%d arch-units x 4 languages" % len(record))


def decisive(r):
    """For `&a`: the arch-opcode that makes the answer an address rather than
    a function of the operand bits."""
    for line in r["body"]:
        if line.startswith("c.addi4spn"):
            return {"opcode": line,
                    "why": "the answer is the address of a stack slot, not a "
                           "function of the operand bits"}
        if "newobject" in line:
            return {"opcode": line,
                    "why": "the answer is a heap address handed back by the "
                           "go runtime allocator, not a function of the "
                           "operand bits"}
    return {"opcode": r["body"][0], "why": "the answer is an address"}


def describe(r):
    """Decompose a body for the record without composing it."""
    out = []
    for line in r["body"]:
        m, o = parse(line)
        rec = {"arch_opcode": line, "mnemonic": m}
        if m in FLOAT_CALLS:
            rec["kind"] = "float"
            rec["mapped_to"] = "emulation:%s_rm%d" % (FLOAT_CALLS[m][0], RM)
            rec["sail_clause"] = FLOAT_CLAUSE[m]
        elif m in FLOAT_BITS:
            rec["kind"] = "float"
            rec["mapped_to"] = "bit-manipulation"
            rec["sail_clause"] = FLOAT_CLAUSE[m]
        elif m in ("c.jr", "jalr"):
            rec["kind"] = "integer"
            rec["mapped_to"] = "return"
        elif m in ("sltu", "sltiu", "xori", "c.or", "c.and", "andn"):
            rec["kind"] = "integer"
            rec["mapped_to"] = "operator"
        else:
            rec["kind"] = "integer"
            rec["mapped_to"] = "address/stack/runtime -- not a bit function"
        out.append(rec)
    return out


def write_glue(record):
    names = [u["name"] for u in record]
    npar = {u["name"]: u["n_params"] for u in record}

    h = ["/* generated by scripts/build_arch_units.py */",
         "#ifndef ARCH_UNITS_H", "#define ARCH_UNITS_H", "",
         "#include <stdint.h>", "#include <stdbool.h>",
         '#include "sfemul.h"', '#include "sfemul_decls.h"', "",
         "static inline uint64_t au_b2u(bool b) { return b ? UINT64_C(1) :"
         " UINT64_C(0); }", ""]
    for n in names:
        h.append("uint64_t %s(%s);"
                 % (n, ", ".join(["uint64_t"] * npar[n]) or "void"))
    h += ["", "#endif"]
    open(os.path.join(OUT, "c", "arch_units.h"), "w").write("\n".join(h) + "\n")

    hp = ["// generated by scripts/build_arch_units.py",
          "#ifndef ARCH_UNITS_HPP", "#define ARCH_UNITS_HPP", "",
          "#include <cstdint>", '#include "sfemul.hpp"',
          '#include "sfemul_decls.hpp"', "", "namespace archunits {", "",
          "inline uint64_t au_b2u(bool b) { return b ? UINT64_C(1) :"
          " UINT64_C(0); }", ""]
    for n in names:
        hp.append("uint64_t %s(%s);"
                  % (n, ", ".join(["uint64_t"] * npar[n])))
    hp += ["", "}  // namespace archunits", "", "#endif"]
    open(os.path.join(OUT, "cpp", "arch_units.hpp"),
         "w").write("\n".join(hp) + "\n")

    # rust: one crate, the emulation crate is an --extern
    lib = ["//! RISC-V float arch-units as integer-only rust.",
           "//! Generated by scripts/build_arch_units.py.",
           "#![allow(non_snake_case)]", "",
           "#[inline(always)]",
           "pub fn b2u(b: bool) -> u64 { if b { 1u64 } else { 0u64 } }", ""]
    for n in names:
        lib.append('#[path = "%s.rs"]' % n)
        lib.append("pub mod %s;" % n)
    open(os.path.join(OUT, "rust", "lib.rs"), "w").write("\n".join(lib) + "\n")

    # the three script languages reach the rm0 emulations through one
    # re-export apiece, so an arch-unit file names the operation and nothing
    # about where it lives
    import json as _json
    _ops = sorted(_json.load(open(os.path.join(EMUL, "_index.json")))["entries"])

    py = ["\"\"\"The rm0 emulations, re-exported for the arch-units. Generated.\"\"\"",
          "import os", "import sys", "",
          "sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),",
          "                               '..', 'emul_rm0', 'python'))", ""]
    for _o in _ops:
        py.append("from %s import %s_rm%d" % (_o, _o, RM))
    d = os.path.join(OUT, "python"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "au_float.py"), "w").write("\n".join(py) + "\n")

    rb = ["# The rm0 emulations, re-exported for the arch-units. Generated.", ""]
    for _o in _ops:
        rb.append("require_relative '../emul_rm0/ruby/%s'" % _o)
    d = os.path.join(OUT, "ruby"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "au_float.rb"), "w").write("\n".join(rb) + "\n")

    js = ["'use strict';",
          "// The rm0 emulations, re-exported for the arch-units. Generated.",
          "module.exports = Object.assign({},"]
    for _o in _ops:
        js.append("  require('../emul_rm0/js/%s.js')," % _o)
    js += [");", ""]
    d = os.path.join(OUT, "js"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "au_float.js"), "w").write("\n".join(js) + "\n")

    open(os.path.join(OUT, "go", "go.mod"), "w").write(
        "module archunits\n\ngo 1.21\n\n"
        "require softfloat_emul v0.0.0\n\n"
        "replace softfloat_emul => ../emul_rm0/go\n")
    open(os.path.join(OUT, "go", "helpers.go"), "w").write(
        "package archunits\n\n"
        "// generated by scripts/build_arch_units.py\n\n"
        "func b2u(b bool) uint64 {\n\tif b {\n\t\treturn 1\n\t}\n"
        "\treturn 0\n}\n")

    idx = {u["name"]: {lang: u["languages"][lang]["entry"]
                       for lang in ("c", "cpp", "rust", "go")}
           for u in record}
    json.dump({"rounding_mode": RM, "entries": idx},
              open(os.path.join(OUT, "_index.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
