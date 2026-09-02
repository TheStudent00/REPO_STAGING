#!/usr/bin/env python3
"""verdicts.py -- step 7 of the ratified pipeline: the three verdicts.

Every CROSS-LANGUAGE pair of ship units that share an operator
intention and an operand type pair is given exactly one verdict:

  MATCHED             the two units are the same unit.  Either their
                      machine bytes are identical -- a fact needing no
                      argument at all -- or their anchored lifted forms
                      are identical, which is a statement about every
                      input, not about one run.

  DIFFERS-BY-DESIGN   one side carries a guard the other does not: a
                      conditional branch into a block that traps or
                      calls a panic, with the arithmetic core otherwise
                      the same.  The finding is not "they differ"; the
                      finding is the DIVERGENCE CONDITION, which is the
                      branch's own comparison, read out of the lifted
                      form and printed in words.

  UNMATCHED           neither.  The pair is handed to z3 over the two
                      lifted forms.  z3 either PROVES them equal for
                      every input, or returns a counterexample -- an
                      assignment of the two arguments on which the two
                      units disagree -- or does not decide, and then
                      the pair is UNDECIDED with the reason.

  UNDECIDED           the solver could not be asked, or could not
                      answer.  Every one of these carries the reason in
                      the tool's own words.  Nothing is dropped
                      silently.

What "operator intention" means here, and what it does not
----------------------------------------------------------
The standing rule is that spelling is never a comparison KEY.  It is
not one here either: the verdict is decided by bytes, by the lifted
form, or by z3, and never by the operator's name.  The spelling is used
for one thing only -- to decide which pairs are WORTH comparing, so the
run does not compare 1779 units against each other pairwise.  A pair
put together by its spelling can still come back UNMATCHED, and does.

Excluded, and counted
---------------------
  * `fallback_lhs` probes.  Where no result-type rule was known the
    probe generator used the left operand's type.  That result type is
    the pipeline's guess and not the language's answer, so those probes
    cannot carry a verdict.
  * probes whose anchor the DWARF table CONTRADICTS.  If the debug
    table says the first parameter did not arrive in the register the
    ABI rule predicted, the operand identity is not established and
    nothing downstream of it may be asserted.

usage:
  verdicts.py            write verdicts.json and verdicts.md
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sem_anchored as SA                                    # noqa: E402
import arch_sem as AS                                        # noqa: E402

import z3                                                    # noqa: E402

LANGS = SA.LANGS
Z3_TIMEOUT_MS = 10000


# ================================================== guards, mechanically
#
# A guard is not recognized by reading the source of a language.  It is
# recognized in the lifted form: a block that TRAPS or that CALLS a
# panic, and a conditional branch elsewhere in the unit that targets it.
# Nothing about `rust` or `swift` appears in the test.

PANIC = re.compile(r"panic|abort|trap|__stack_chk_fail|fatalError"
                   r"|unwind|Unwind", re.I)


def guard_blocks(blocks):
    """{block number: why} for every block that traps or panics."""
    out = {}
    for b in blocks:
        for ev in b["events"]:
            if ev.startswith("trap "):
                out[b["block"]] = ev
                break
            if ev.startswith("call "):
                callee = ev.split(None, 1)[1]
                if PANIC.search(callee):
                    out[b["block"]] = ev
                    break
    return out


BRANCH = re.compile(r"^branch (\S+) (\S+) \[(.*)\]$")


def guard_branches(blocks, targets):
    """[(mnemonic condition, target block, lifted condition text)] for
    every conditional branch that lands in a guard block."""
    out = []
    for b in blocks:
        for ev in b["events"]:
            m = BRANCH.match(ev)
            if not m:
                continue
            tgt = m.group(2)
            if not tgt.startswith("B"):
                continue
            if int(tgt[1:]) in targets:
                out.append((m.group(1), tgt, m.group(3)))
    return out


PASSTHROUGH = re.compile(r"^(?:zx\d+\(|sx\d+\(|ex\d+@\d+\()*"
                         r"(?:in\d+|u\d+|SP|PC):\d+\)*$")


WRAP = re.compile(r"^(?:zx\d+|sx\d+|ex\d+@0)\(")


def peel_text(s):
    """the same value with its width changes taken off the outside.  A
    32-bit result zero-extended into a 64-bit register is the same
    computation as the 32-bit result."""
    while True:
        m = WRAP.match(s)
        if not m:
            return s
        depth = 0
        end = None
        for i, ch in enumerate(s):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end != len(s) - 1:
            return s
        s = s[m.end():-1]


def core_values(blocks, guards):
    """the arithmetic core: every value computed in a block that is not
    a guard block, minus the values that compute nothing.

    Three kinds of value are not part of it, each for a stated reason.

    A PASS-THROUGH.  A value that is nothing but a register read,
    however many width changes are wrapped round it, is a value this
    block RECEIVED.  The sweep summarizes each block from a fresh entry
    state, so it cannot see where such a value came from, and counting
    it would make a unit whose answer crosses a block boundary look
    different from the same answer computed in one block.

    A value that MENTIONS NO OPERAND.  A constant, or something derived
    only from the stack pointer -- `push`, `pop`, a frame adjustment.
    That is call protocol, not arithmetic.

    GUARD MACHINERY.  A value the guard's own branch condition is built
    out of.  rust tests `!b | (a + 0x80000000)` before it divides; that
    test is the guard, so counting it as arithmetic would say rust's
    division computes something c's does not, when what it actually
    does is decide whether to divide at all."""
    conds = []
    for b in blocks:
        for ev in b["events"]:
            m = BRANCH.match(ev)
            if m and m.group(2).startswith("B") \
                    and int(m.group(2)[1:]) in guards:
                conds.append(m.group(3))
    out = []
    for b in blocks:
        if b["block"] in guards:
            continue
        for v in b["values"]:
            if PASSTHROUGH.match(v):
                continue
            if "in" not in v or not re.search(r"\bin\d+\b", v):
                continue
            inner = peel_text(v)
            if any(inner in c for c in conds):
                continue
            out.append(v)
        for s in b["stores"]:
            out.append(s)
    return sorted(out)


# ================================ the condition, in words rather than VEX
#
# amd64's condition codes and libVEX's lazy flag machinery, decoded.
# The numbers are libVEX's own (guest_amd64_defs.h): the condition in
# the first argument of amd64g_calculate_condition, the flag-producing
# operation in the second.

COND = {0: "O", 1: "NO", 2: "B", 3: "NB", 4: "Z", 5: "NZ", 6: "BE",
        7: "NBE", 8: "S", 9: "NS", 10: "P", 11: "NP", 12: "L", 13: "NL",
        14: "LE", 15: "NLE"}

CC_OP = {}
for _base, _name in [(1, "ADD"), (5, "SUB"), (9, "ADC"), (13, "SBB"),
                     (17, "LOGIC"), (21, "INC"), (25, "DEC"),
                     (29, "SHL"), (33, "SHR"), (37, "ROL"), (41, "ROR"),
                     (45, "UMUL"), (49, "SMUL")]:
    for _k, _w in enumerate((8, 16, 32, 64)):
        CC_OP[_base + _k] = (_name, _w)
CC_OP[0] = ("COPY", 64)

# how each condition reads when the flags came from a subtraction of
# argR from argL -- which is what `cmp` and `sub` leave behind.
SUB_WORDS = {
    "Z": "%(L)s == %(R)s", "NZ": "%(L)s != %(R)s",
    "L": "%(L)s < %(R)s (signed)", "NL": "%(L)s >= %(R)s (signed)",
    "LE": "%(L)s <= %(R)s (signed)", "NLE": "%(L)s > %(R)s (signed)",
    "B": "%(L)s < %(R)s (unsigned)", "NB": "%(L)s >= %(R)s (unsigned)",
    "BE": "%(L)s <= %(R)s (unsigned)", "NBE": "%(L)s > %(R)s (unsigned)",
    "S": "%(L)s - %(R)s is negative", "NS": "%(L)s - %(R)s is not negative",
    "O": "%(L)s - %(R)s overflows %(W)d bits (signed)",
    "NO": "%(L)s - %(R)s does not overflow %(W)d bits (signed)",
}
ADD_WORDS = {
    "Z": "%(L)s + %(R)s == 0", "NZ": "%(L)s + %(R)s != 0",
    "O": "%(L)s + %(R)s overflows %(W)d bits (signed)",
    "NO": "%(L)s + %(R)s does not overflow %(W)d bits (signed)",
    "B": "%(L)s + %(R)s carries out of %(W)d bits (unsigned)",
    "NB": "%(L)s + %(R)s does not carry out of %(W)d bits (unsigned)",
    "S": "%(L)s + %(R)s is negative", "NS": "%(L)s + %(R)s is not negative",
}
MUL_WORDS = {
    "O": "%(L)s * %(R)s overflows %(W)d bits (signed)",
    "NO": "%(L)s * %(R)s does not overflow %(W)d bits (signed)",
    "Z": "%(L)s * %(R)s == 0", "NZ": "%(L)s * %(R)s != 0",
    "S": "%(L)s * %(R)s is negative",
    "NS": "%(L)s * %(R)s is not negative",
}
LOGIC_WORDS = {
    "Z": "%(L)s == 0", "NZ": "%(L)s != 0",
    "S": "%(L)s is negative", "NS": "%(L)s is not negative",
    "LE": "%(L)s <= 0 (signed)", "NLE": "%(L)s > 0 (signed)",
    "L": "%(L)s < 0 (signed)", "NL": "%(L)s >= 0 (signed)",
}


def _peel(e):
    """drop the width changes wrapped round a value, to reach the thing
    the value IS."""
    while e[0] in ("zx", "sx"):
        e = e[2]
    while e[0] == "ex" and e[2] == 0:
        e = e[3]
    return e


def _signed(e):
    v = e[2]
    w = e[1]
    if v >> (w - 1):
        v -= 1 << w
    return v


def term(e, names, width=None):
    """one operand, printed as a person would read it.

    A constant is re-signed at the width of the operation that used it,
    not at the width the lifter happened to widen it to: a `cmp`
    against a 32-bit -1 reaches the lifted form as 4294967295 sitting
    in a 64-bit slot, and printing that number would be printing the
    widening rather than the comparison."""
    e = _peel(e)
    if e[0] == "c":
        if width is not None and width < e[1]:
            e = ("c", width, e[2] & ((1 << width) - 1))
        return str(_signed(e))
    if e[0] == "r":
        return names.get(e[2], "%%%s" % e[2])
    if e[0] == "b":
        m = AS.BINWIDTH.match(e[2])
        head = m.group(1) if m else e[2]
        sign = {"Add": "+", "Sub": "-", "Mul": "*", "And": "&", "Or": "|",
                "Xor": "^"}.get(head)
        if sign:
            return "(%s %s %s)" % (term(e[3], names), sign,
                                   term(e[4], names))
    if e[0] == "u":
        m = AS.BINWIDTH.match(e[2])
        if m and m.group(1) == "Not":
            return "~%s" % term(e[3], names)
    return AS._ser(e, names)


def describe(e, names):
    """the divergence condition in words, or the lifted form when this
    file cannot read it -- never a guess."""
    e = _peel(e)
    if e[0] != "cc" or e[2] != "amd64g_calculate_condition":
        return AS._ser(e, names)
    args = e[3]
    cond = _peel(args[0])
    op = _peel(args[1])
    if cond[0] != "c" or op[0] != "c":
        return AS._ser(e, names)
    cname = COND.get(cond[2] & 0xF)
    oname, width = CC_OP.get(op[2], (None, 64))
    if cname is None or oname is None:
        return AS._ser(e, names)
    sub = dict(L=term(args[2], names, width),
               R=term(args[3], names, width), W=width)
    table = {"SUB": SUB_WORDS, "ADD": ADD_WORDS, "LOGIC": LOGIC_WORDS,
             "SMUL": MUL_WORDS, "UMUL": MUL_WORDS}.get(oname)
    if table is None or cname not in table:
        return "%s after %s%d(%s, %s)" % (cname, oname, width, sub["L"],
                                          sub["R"])
    return table[cname] % sub


# ==================================================== z3 over the forms

class Unsupported(Exception):
    pass


def _bv(e, names, env):
    """one lifted value, as a z3 bitvector."""
    k = e[0]
    if k == "c":
        return z3.BitVecVal(e[2], e[1])
    if k == "r":
        tok = names.get(e[2])
        if tok is None:
            raise Unsupported("a register with no anchored name: %s" % e[2])
        key = "%s_%d" % (tok, e[1])
        if key not in env:
            env[key] = z3.BitVec(key, e[1])
        return env[key]
    if k == "ex":
        return z3.Extract(e[2] + e[1] - 1, e[2], _bv(e[3], names, env))
    if k == "zx":
        return z3.ZeroExt(e[1] - AS.W(e[2]), _bv(e[2], names, env))
    if k == "sx":
        return z3.SignExt(e[1] - AS.W(e[2]), _bv(e[2], names, env))
    if k == "ins":
        old = _bv(e[2], names, env)
        val = _bv(e[3], names, env)
        lo = e[4]
        w = e[1]
        parts = []
        if lo + AS.W(e[3]) < w:
            parts.append(z3.Extract(w - 1, lo + AS.W(e[3]), old))
        parts.append(val)
        if lo > 0:
            parts.append(z3.Extract(lo - 1, 0, old))
        return parts[0] if len(parts) == 1 else z3.Concat(*parts)
    if k == "ite":
        c = _bv(e[2], names, env)
        return z3.If(c == z3.BitVecVal(1, AS.W(e[2])),
                     _bv(e[3], names, env), _bv(e[4], names, env))
    if k == "b":
        return _binop(e, names, env)
    if k == "u":
        m = AS.BINWIDTH.match(e[2])
        if m and m.group(1) == "Not":
            return ~_bv(e[3], names, env)
        raise Unsupported("unary VEX op not modelled: %s" % e[2])
    if k == "cc":
        return _ccall(e, names, env)
    if k == "op":
        raise Unsupported("the lifted form carries an opaque value [%s]"
                          % e[2])
    if k == "ld":
        raise Unsupported("the unit reads memory")
    raise Unsupported("expression kind not modelled: %s" % k)


ARITH = {"Add": lambda a, b: a + b, "Sub": lambda a, b: a - b,
         "Mul": lambda a, b: a * b, "And": lambda a, b: a & b,
         "Or": lambda a, b: a | b, "Xor": lambda a, b: a ^ b}


def _binop(e, names, env):
    op = e[2]
    a = _bv(e[3], names, env)
    b = _bv(e[4], names, env)
    m = AS.BINWIDTH.match(op)
    head = m.group(1) if m else op
    if head in ARITH:
        return ARITH[head](a, b)
    if head in ("Shl", "Shr", "Sar"):
        amount = z3.ZeroExt(AS.W(e[3]) - AS.W(e[4]), b) \
            if AS.W(e[4]) < AS.W(e[3]) else z3.Extract(AS.W(e[3]) - 1, 0, b)
        if head == "Shl":
            return a << amount
        if head == "Shr":
            return z3.LShR(a, amount)
        return a >> amount
    bit = None
    if op.startswith("CmpEQ"):
        bit = a == b
    elif op.startswith("CmpNE"):
        bit = a != b
    elif re.match(r"^CmpLT\d+S$", op):
        bit = a < b
    elif re.match(r"^CmpLT\d+U$", op):
        bit = z3.ULT(a, b)
    elif re.match(r"^CmpLE\d+S$", op):
        bit = a <= b
    elif re.match(r"^CmpLE\d+U$", op):
        bit = z3.ULE(a, b)
    if bit is not None:
        return z3.If(bit, z3.BitVecVal(1, 1), z3.BitVecVal(0, 1))
    raise Unsupported("binary VEX op not modelled: %s" % op)


def _flag(cname, oname, width, L, R):
    """the amd64 condition, as a z3 boolean, from the operation that
    produced the flags."""
    if oname == "SUB":
        res = L - R
        table = {
            "Z": L == R, "NZ": L != R,
            "L": L < R, "NL": L >= R, "LE": L <= R, "NLE": L > R,
            "B": z3.ULT(L, R), "NB": z3.UGE(L, R),
            "BE": z3.ULE(L, R), "NBE": z3.UGT(L, R),
            "S": res < 0, "NS": res >= 0,
            "O": z3.Not(z3.And(z3.BVSubNoOverflow(L, R),
                               z3.BVSubNoUnderflow(L, R, True))),
        }
        table["NO"] = z3.Not(table["O"])
        if cname in table:
            return table[cname]
    if oname == "ADD":
        res = L + R
        of = z3.Not(z3.And(z3.BVAddNoOverflow(L, R, True),
                           z3.BVAddNoUnderflow(L, R)))
        table = {
            "Z": res == 0, "NZ": res != 0,
            "S": res < 0, "NS": res >= 0,
            "O": of, "NO": z3.Not(of),
            "B": z3.Not(z3.BVAddNoOverflow(L, R, False)),
            "NB": z3.BVAddNoOverflow(L, R, False),
        }
        if cname in table:
            return table[cname]
    if oname == "LOGIC":
        res = L
        table = {
            "Z": res == 0, "NZ": res != 0,
            "S": res < 0, "NS": res >= 0,
            "L": res < 0, "NL": res >= 0,
            "LE": res <= 0, "NLE": res > 0,
            "B": z3.BoolVal(False), "NB": z3.BoolVal(True),
            "BE": res == 0, "NBE": res != 0,
            "O": z3.BoolVal(False), "NO": z3.BoolVal(True),
        }
        if cname in table:
            return table[cname]
    raise Unsupported("condition %s after %s%d is not modelled"
                      % (cname, oname, width))


def _ccall(e, names, env):
    if e[2] != "amd64g_calculate_condition":
        raise Unsupported("VEX helper call not modelled: %s" % e[2])
    args = e[3]
    cond = _peel(args[0])
    op = _peel(args[1])
    if cond[0] != "c" or op[0] != "c":
        raise Unsupported("the condition or the flag operation is not a "
                          "constant in the lifted form")
    cname = COND.get(cond[2] & 0xF)
    oname, width = CC_OP.get(op[2], (None, 64))
    if cname is None or oname is None:
        raise Unsupported("flag operation %s is not modelled" % op[2])
    L = _bv(args[2], names, env)
    R = _bv(args[3], names, env)
    L = z3.Extract(width - 1, 0, L) if AS.W(args[2]) > width else L
    R = z3.Extract(width - 1, 0, R) if AS.W(args[3]) > width else R
    bit = _flag(cname, oname, width, L, R)
    return z3.If(bit, z3.BitVecVal(1, e[1]), z3.BitVecVal(0, e[1]))


PURE_EVENT = re.compile(r"^ret$")


def z3_pair(left, right):
    """(verdict, detail).  Bounded: pure scalar dataflow only."""
    forms = []
    for side in (left, right):
        blocks = side["sem"]["blocks"]
        if len(blocks) != 1:
            return "UNDECIDED", ("%s op_%s is not straight-line: %d blocks"
                                 % (side["lang"], side["n"], len(blocks)))
        events = blocks[0]["events"]
        bad = [ev for ev in events if not PURE_EVENT.match(ev)]
        if bad:
            return "UNDECIDED", ("%s op_%s is not pure scalar dataflow: %s"
                                 % (side["lang"], side["n"], "; ".join(bad)))
        if blocks[0]["stores"]:
            return "UNDECIDED", ("%s op_%s writes memory"
                                 % (side["lang"], side["n"]))
        summaries, names, reason = SA.raw_summaries(
            dict(bytes=side["bytes"].split(), mnem=side["mnem"]),
            side["lang"], side["meta"])
        if summaries is None:
            return "UNDECIDED", "the lift was refused: %s" % reason
        _parts, names = SA.render_anchored(summaries, names)
        vals = summaries[0][0]
        forms.append((side, vals, names))

    (ls, lv, lnames), (rs, rv, rnames) = forms
    if len(lv) != len(rv):
        return "UNDECIDED", ("the two units leave a different number of "
                             "live results (%d and %d)" % (len(lv), len(rv)))
    lv = sorted(lv, key=lambda x: (AS.W(x), AS._ser(x, lnames)))
    rv = sorted(rv, key=lambda x: (AS.W(x), AS._ser(x, rnames)))

    env = {}
    claims = []
    widths = []
    try:
        for a, b in zip(lv, rv):
            # RULE.  Two units may DEFINE different amounts of the same
            # register: `xor %eax,%eax; cmp; setl %al` defines 64 bits,
            # `cmp; setl %al` defines 8.  The bits both units define are
            # the low ones, and the question asked is about those.  The
            # difference is not swept under the rug -- it is recorded on
            # the verdict, so a reader can see the claim's width.
            n = min(AS.W(a), AS.W(b))
            widths.append((AS.W(a), AS.W(b), n))
            av = _bv(a, lnames, env)
            bv = _bv(b, rnames, env)
            if AS.W(a) > n:
                av = z3.Extract(n - 1, 0, av)
            if AS.W(b) > n:
                bv = z3.Extract(n - 1, 0, bv)
            claims.append(av == bv)
    except Unsupported as exc:
        return "UNDECIDED", "z3 was not asked: %s" % exc
    narrowed = [w for w in widths if w[0] != w[1]]
    scope = ""
    if narrowed:
        scope = ("; the claim is over the low %s bits -- the two units "
                 "define %s and %s bits of that result and only the low "
                 "bits are common to both"
                 % (",".join(str(w[2]) for w in narrowed),
                    ",".join(str(w[0]) for w in narrowed),
                    ",".join(str(w[1]) for w in narrowed)))

    loose = [k for k in env if k.startswith("u")]
    if loose:
        return "UNDECIDED", ("an unanchored register value reaches the "
                             "result (%s); the two units cannot be "
                             "compared on it" % ", ".join(sorted(loose)))

    s = z3.Solver()
    s.set("timeout", Z3_TIMEOUT_MS)
    s.add(z3.Not(z3.And(*claims)) if len(claims) > 1
          else z3.Not(claims[0]))
    got = s.check()
    if got == z3.unsat:
        return "MATCHED", ("z3 proved the two lifted forms equal for every "
                           "input (negation unsat)%s" % scope)
    if got == z3.sat:
        model = s.model()
        shown = ", ".join("%s = %s" % (d.name(), model[d])
                          for d in sorted(model.decls(),
                                          key=lambda d: d.name()))
        return "UNMATCHED", "z3 counterexample: %s" % shown
    return "UNDECIDED", "z3 returned %s (timeout %d ms)" % (got,
                                                            Z3_TIMEOUT_MS)


# ============================================================== the pass

def load_units():
    units = []
    excluded = Counter()
    excluded_rows = []
    for lang in LANGS:
        path = os.path.join(HERE, "sem_anchored_%s.json" % lang)
        doc = json.load(open(path))
        source = SA.load(lang)
        for n, u in doc["units"].items():
            meta = u["meta"]
            if meta.get("result_rule") == "fallback_lhs":
                excluded["fallback_lhs"] += 1
                excluded_rows.append(dict(lang=lang, n=n,
                                          why="fallback_lhs"))
                continue
            verdict, detail = SA.dwarf_check(source["probes"][n], lang)
            if verdict == "CONTRADICTED":
                excluded["dwarf_contradicts_the_anchor"] += 1
                excluded_rows.append(dict(lang=lang, n=n,
                                          why="DWARF contradicts the "
                                              "anchor: %s" % detail))
                continue
            if not u["sem"]["ok"]:
                excluded["no_anchored_sem"] += 1
                excluded_rows.append(dict(lang=lang, n=n,
                                          why=u["sem"]["reason"]))
                continue
            units.append(dict(lang=lang, n=n, meta=meta, bytes=u["bytes"],
                              mnem=u["mnem"], sem=u["sem"],
                              dwarf=verdict))
    return units, excluded, excluded_rows


def intention(meta):
    """the grouping label.  Spelling plus arity plus position, and the
    operand type pair.  This decides WHICH pairs are compared and never
    what the comparison answers."""
    return (meta.get("operator"), meta.get("arity"), meta.get("position"),
            meta.get("lhs_rep"), meta.get("rhs_rep"))


def judge(left, right):
    """the verdict for one cross-language pair."""
    if left["bytes"] == right["bytes"]:
        return dict(verdict="MATCHED", ground="byte identity",
                    detail="the two units are the same machine bytes")
    if left["sem"]["key"] == right["sem"]["key"]:
        return dict(verdict="MATCHED", ground="sem identity (anchored)",
                    detail="the two anchored lifted forms are identical")

    lg = guard_blocks(left["sem"]["blocks"])
    rg = guard_blocks(right["sem"]["blocks"])
    if bool(lg) != bool(rg):
        guarded, bare = (left, right) if lg else (right, left)
        gmap = lg or rg
        lcore = core_values(left["sem"]["blocks"], lg)
        rcore = core_values(right["sem"]["blocks"], rg)
        if lcore == rcore:
            conds = divergence_conditions(guarded, gmap)
            return dict(verdict="DIFFERS-BY-DESIGN",
                        ground="a guard on one side, the same core on both",
                        guarded=guarded["lang"], bare=bare["lang"],
                        guard_events=sorted(gmap.values()),
                        divergence_conditions=conds,
                        detail="%s op_%s guards; %s op_%s does not; the "
                               "arithmetic core is sem-equal"
                               % (guarded["lang"], guarded["n"],
                                  bare["lang"], bare["n"]))
        return dict(verdict="UNDECIDED",
                    ground="one side guards but the cores are not equal",
                    detail="core of %s op_%s is %s; core of %s op_%s is %s"
                           % (left["lang"], left["n"], lcore,
                              right["lang"], right["n"], rcore))
    if lg and rg:
        return dict(verdict="UNDECIDED",
                    ground="both sides carry a guard",
                    detail="both units trap or panic, and their lifted "
                           "forms differ; this pass classifies only a "
                           "one-sided guard")

    verdict, detail = z3_pair(left, right)
    return dict(verdict=verdict, ground="z3 over the two lifted forms",
                detail=detail)


def divergence_conditions(unit, gmap):
    """the guard's own comparison, in words."""
    summaries, names, reason = SA.raw_summaries(
        dict(bytes=unit["bytes"].split(), mnem=unit["mnem"]),
        unit["lang"], unit["meta"])
    out = []
    if summaries is None:
        return [dict(text="the lift was refused: %s" % reason)]
    _parts, names = SA.render_anchored(summaries, names)
    for b, (_vals, _stores, events) in enumerate(summaries):
        for ev in events:
            if ev[0] != "branch" or ev[2] is None:
                continue
            if not ev[2].startswith("B"):
                continue
            if int(ev[2][1:]) not in gmap:
                continue
            cond = ev[3]
            out.append(dict(
                branch="%s -> %s" % (ev[1], ev[2]),
                lands_in=gmap[int(ev[2][1:])],
                condition=describe(cond, names) if cond else "?",
                lifted=AS._ser(cond, names) if cond else "?"))
    if not out:
        out.append(dict(text="the guard block is reached, but by no "
                             "conditional branch this pass recognized",
                        lands_in=sorted(gmap.values())))
    return out


def main():
    units, excluded, excluded_rows = load_units()
    groups = defaultdict(list)
    for u in units:
        groups[intention(u["meta"])].append(u)

    rows = []
    tally = Counter()
    for key, members in sorted(groups.items(), key=lambda kv: str(kv[0])):
        by_lang = defaultdict(list)
        for m in members:
            by_lang[m["lang"]].append(m)
        langs = sorted(by_lang)
        if len(langs) < 2:
            continue
        pairs = []
        for i, la in enumerate(langs):
            for lb in langs[i + 1:]:
                for ua in by_lang[la]:
                    for ub in by_lang[lb]:
                        try:
                            v = judge(ua, ub)
                        except Exception as exc:           # noqa: BLE001
                            v = dict(verdict="UNDECIDED",
                                     ground="the pass raised",
                                     detail="%s: %s" % (type(exc).__name__,
                                                        exc))
                        v.update(left="%s/op_%s" % (la, ua["n"]),
                                 right="%s/op_%s" % (lb, ub["n"]))
                        pairs.append(v)
                        tally[v["verdict"]] += 1
        rows.append(dict(
            operator=key[0], arity=key[1], position=key[2],
            type_pair="%s,%s" % (key[3], key[4]),
            languages=langs, pairs=pairs))

    doc = dict(
        languages=LANGS,
        units_considered=len(units),
        excluded=dict(excluded),
        excluded_rows=excluded_rows,
        rows=rows,
        tally=dict(tally),
        z3=z3.get_version_string(),
        lifter=AS.LIFTER_ID,
    )
    json.dump(doc, open(os.path.join(HERE, "verdicts.json"), "w"), indent=1)
    write_md(doc)

    print("== step 7: three verdicts")
    print("   units considered   %d" % doc["units_considered"])
    for why, count in sorted(excluded.items()):
        print("   excluded %-32s %d" % (why, count))
    print("   comparable groups  %d" % len(rows))
    print()
    for v in ("MATCHED", "DIFFERS-BY-DESIGN", "UNMATCHED", "UNDECIDED"):
        print("   %-20s %d" % (v, tally.get(v, 0)))
    return 0


SHORT = {"MATCHED": "M", "DIFFERS-BY-DESIGN": "D", "UNMATCHED": "X",
         "UNDECIDED": "?"}


def write_md(doc):
    out = []
    out.append("# the three verdicts")
    out.append("")
    out.append("Every row is one operator intention on one operand type "
               "pair.  Every cell is one cross-language pair of ship "
               "units.")
    out.append("")
    out.append("**What each verdict is evidence of.**")
    out.append("")
    out.append("- `MATCHED (byte)` is a FACT about these two artifacts: "
               "the same machine bytes.  It needs no lifter and no "
               "solver.")
    out.append("- `MATCHED (sem)` and `MATCHED (z3)` are bounds over "
               "ALL RUNS: the lifted forms are equal as expressions, or "
               "z3 proved them equal for every input.  They rest on the "
               "lifter being right about what the instructions do.")
    out.append("- `DIFFERS-BY-DESIGN` is an all-runs bound too, and the "
               "divergence condition printed with it is read out of the "
               "guard's own lifted comparison.")
    out.append("- `UNMATCHED` carries a counterexample: an assignment of "
               "the arguments on which the two units disagree.")
    out.append("- `UNDECIDED` carries the reason, in the tool's own "
               "words.")
    out.append("")
    out.append("**One limit on `UNMATCHED`, stated rather than hidden.** "
               "z3 is asked about every bit pattern the registers can "
               "hold.  A language's ABI promises less than that -- a "
               "`bool` arrives as 0 or 1 and never as 0xFFFFFF00 -- and "
               "this pass does NOT put the ABI's promise into the query "
               "as a precondition.  A counterexample that only exists "
               "outside what the ABI can produce is therefore a real "
               "difference between the two BIT FUNCTIONS and not "
               "necessarily a difference between the two OPERATORS.  "
               "Read the counterexample before reading the verdict.")
    out.append("")
    out.append("The OPERAND ANCHOR under all of it -- which register "
               "carried `a` -- rests on the ABI rule, on the anchor "
               "build's DWARF table (per-artifact testimony, checked "
               "probe by probe), and on the forced `a - b` probe.  See "
               "`sem_anchored.py --anchor-report`.")
    out.append("")
    out.append("lifter: %s   solver: z3 %s" % (doc["lifter"], doc["z3"]))
    out.append("")
    out.append("## excluded")
    out.append("")
    for why, count in sorted(doc["excluded"].items()):
        out.append("- `%s`: %d units" % (why, count))
    out.append("")
    out.append("## tally")
    out.append("")
    out.append("| verdict | pairs |")
    out.append("| --- | --- |")
    for v in ("MATCHED", "DIFFERS-BY-DESIGN", "UNMATCHED", "UNDECIDED"):
        out.append("| %s | %d |" % (v, doc["tally"].get(v, 0)))
    out.append("")
    out.append("## the table")
    out.append("")
    out.append("| operator | arity | type pair | MATCHED | "
               "DIFFERS-BY-DESIGN | UNMATCHED | UNDECIDED |")
    out.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in doc["rows"]:
        buckets = defaultdict(list)
        for p in row["pairs"]:
            buckets[p["verdict"]].append("%s~%s"
                                         % (p["left"].split("/")[0],
                                            p["right"].split("/")[0]))
        cells = []
        for v in ("MATCHED", "DIFFERS-BY-DESIGN", "UNMATCHED", "UNDECIDED"):
            cells.append(" ".join(sorted(set(buckets[v]))) or "-")
        out.append("| `%s` | %s | %s | %s |"
                   % (row["operator"], row["arity"], row["type_pair"],
                      " | ".join(cells)))
    out.append("")
    out.append("## divergence conditions")
    out.append("")
    seen = set()
    for row in doc["rows"]:
        for p in row["pairs"]:
            if p["verdict"] != "DIFFERS-BY-DESIGN":
                continue
            for c in p.get("divergence_conditions", []):
                key = (p["guarded"], row["operator"], row["type_pair"],
                       c.get("condition"))
                if key in seen:
                    continue
                seen.add(key)
                out.append("- **%s `%s` on %s** guards where **%s** does "
                           "not.  Branch `%s` lands in `%s`.  "
                           "Divergence condition: **%s**"
                           % (p["guarded"], row["operator"],
                              row["type_pair"], p["bare"],
                              c.get("branch", "?"), c.get("lands_in", "?"),
                              c.get("condition", c.get("text", "?"))))
                out.append("  - lifted: `%s`" % c.get("lifted", "?"))
    out.append("")
    out.append("## every pair")
    out.append("")
    for row in doc["rows"]:
        out.append("### `%s` %s on (%s)" % (row["operator"], row["arity"],
                                            row["type_pair"]))
        out.append("")
        out.append("| left | right | verdict | ground | detail |")
        out.append("| --- | --- | --- | --- | --- |")
        for p in row["pairs"]:
            out.append("| %s | %s | %s | %s | %s |"
                       % (p["left"], p["right"], p["verdict"], p["ground"],
                          str(p["detail"]).replace("|", "/")[:300]))
        out.append("")
    open(os.path.join(HERE, "verdicts.md"), "w").write("\n".join(out))


if __name__ == "__main__":
    sys.exit(main())
