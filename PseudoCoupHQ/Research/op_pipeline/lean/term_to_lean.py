#!/usr/bin/env python3
"""term_to_lean.py -- one printed layer-5 term text, to one Lean 4 BitVec expression.

WHAT A LAYER-5 TEXT IS
  A unit's computation is its layer-4 term: the arch-unit as a z3 expression,
  read off its ledger from OUT-0 downward.  Layer 5 is that expression printed
  by one fixed rule -- simplified once, free symbols renamed positionally v0,
  v1, ..., on one line.  This program reads that one line and writes the same
  computation as a Lean 4 expression over `BitVec w`.

THE FOUR STAGES, and why the third exists
  1. TOKENIZE and PARSE the text into a tree, with z3's own operator
     precedence.
  2. INFER WIDTHS.  The printed form drops them: `Concat(0, Extract(31, 0,
     v0))` never says the `0` is 32 bits wide.  The widths are recovered by
     unification, seeded with the arrival rows' widths (from the pair record's
     own `inputs`) and the term's result width.
  3. REBUILD THE TERM IN Z3 AND PRINT IT.  If z3's printer reproduces the
     input text character for character, then the tree this program built IS
     the tree z3 printed -- the parse is confirmed rather than trusted.  A
     mismatch is a REFUSAL, never a warning: a parser that reads a term
     differently from z3 would silently hand Lean a different theorem.
  4. EMIT LEAN.

REFUSAL CAUSES (this program refuses by cause; it never guesses)
  FLOATING_POINT     a floating-point node; Lean's bv_decide bit-blasts
                     bit-vectors and has no floating-point theory
  UNKNOWN_NODE       a function name with no rule in OPERATOR_TABLE
  WIDTH_UNRESOLVED   a numeral or sub-term whose width the constraints do
                     not determine
  ROUNDTRIP_MISMATCH z3's printing of the rebuilt term differs from the input
  PARSE_ERROR        the text does not parse
  UNGUARDED_DIVISION the `bvudiv_i` family.  z3's simplifier splits a division
                     into a zero test and this UNGUARDED symbol, whose value at
                     a zero divisor is not specified.  Lean's `/` answers zero
                     there (measured), so the two are different functions and
                     translating one to the other would state a theorem the
                     corpus never proved.

A SEAM THIS PROGRAM RECORDS RATHER THAN HIDES
  z3's `bvudiv` answers all-ones when the divisor is zero; Lean's `BitVec./`
  answers zero (measured, lane 5: `#eval ((7#8) / (0#8))` prints `0x00#8`).
  `bvurem`/`%` and `bvsrem`/`srem` agree (both answer the dividend), and the
  shifts agree.  So a term carrying a DIVISION is translated with the
  divide-by-zero difference named on the record; a caller that needs the two
  systems to agree there must add the guard explicitly.
"""

import re
import sys


# ---------------------------------------------------------------- the table

# THE OPERATOR TABLE.  Left: the name or symbol z3's printer emits in a
# layer-5 text.  Right: what this program emits in Lean 4.24, and the arity.
# `bv` = a BitVec-valued node, `bool` = a Bool-valued node.
OPERATOR_TABLE = [
    # printed form        arity   result  Lean form
    ("Extract(hi, lo, x)", 3, "bv", "x.extractLsb hi lo"),
    ("Concat(a, b, ...)", -1, "bv", "a ++ b"),
    ("If(c, a, b)", 3, "bv", "if c = true then a else b"),
    ("ZeroExt(n, x)", 2, "bv", "x.zeroExtend (n + width x)"),
    ("SignExt(n, x)", 2, "bv", "x.signExtend (n + width x)"),
    ("a + b", 2, "bv", "a + b"),
    ("a - b", 2, "bv", "a - b"),
    ("a*b", 2, "bv", "a * b"),
    ("a & b", 2, "bv", "a &&& b"),
    ("a | b", 2, "bv", "a ||| b"),
    ("a ^ b", 2, "bv", "a ^^^ b"),
    ("~a", 1, "bv", "~~~a"),
    ("-a", 1, "bv", "-a"),
    ("a << b", 2, "bv", "a <<< b"),
    ("LShR(a, b)", 2, "bv", "a >>> b"),
    ("a >> b", 2, "bv", "a.sshiftRight' b"),
    ("bvudiv_i(a, b)", 2, "bv", "REFUSED, cause UNGUARDED_DIVISION"),
    ("bvsdiv_i(a, b)", 2, "bv", "REFUSED, cause UNGUARDED_DIVISION"),
    ("bvurem_i(a, b)", 2, "bv", "REFUSED, cause UNGUARDED_DIVISION"),
    ("bvsrem_i(a, b)", 2, "bv", "REFUSED, cause UNGUARDED_DIVISION"),
    ("bvsmod_i(a, b)", 2, "bv", "REFUSED, cause UNGUARDED_DIVISION"),
    ("UDiv(a, b)", 2, "bv", "a / b"),
    ("URem(a, b)", 2, "bv", "a % b"),
    ("SRem(a, b)", 2, "bv", "a.srem b"),
    ("a == b", 2, "bool", "a == b"),
    ("a != b", 2, "bool", "!(a == b)"),
    ("a <= b", 2, "bool", "a.sle b"),
    ("a < b", 2, "bool", "a.slt b"),
    ("a >= b", 2, "bool", "b.sle a"),
    ("a > b", 2, "bool", "b.slt a"),
    ("ULE(a, b)", 2, "bool", "a.ule b"),
    ("ULT(a, b)", 2, "bool", "a.ult b"),
    ("UGE(a, b)", 2, "bool", "b.ule a"),
    ("UGT(a, b)", 2, "bool", "b.ult a"),
    ("And(a, b, ...)", -1, "bool", "a && b"),
    ("Or(a, b, ...)", -1, "bool", "a || b"),
    ("Not(a)", 1, "bool", "!a"),
    ("<numeral>", 0, "bv", "n#w"),
    ("v0, v1, ...", 0, "bv", "the theorem's bound variable"),
]

FLOAT_NAMES = {"fpToFP", "fpIsNaN", "fpEQ", "fpLT", "fpLEQ", "fpAdd", "fpSub",
               "fpMul", "fpDiv", "fpNeg", "fpAbs", "fpIsInf", "fpIsZero",
               "fpToUBV", "fpToSBV", "fpRoundToIntegral", "RNE", "RTZ", "RTP",
               "RTN", "RNA", "fp.to_ieee_bv", "fp"}


class Refused(Exception):
    def __init__(self, cause, detail):
        Exception.__init__(self, "%s: %s" % (cause, detail))
        self.cause = cause
        self.detail = detail


# ---------------------------------------------------------------- tokenizer

TOK = re.compile(r"""
    (?P<space>\s+)
  | (?P<name>[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)*)
  | (?P<num>[0-9]+)
  | (?P<op><<|>>|<=|>=|==|!=|[-+*/%&|^~<>()!,])
""", re.X)


def tokenize(text):
    out = []
    i = 0
    while i < len(text):
        m = TOK.match(text, i)
        if not m:
            raise Refused("PARSE_ERROR", "no token at offset %d: %r" % (i, text[i:i + 20]))
        i = m.end()
        if m.lastgroup == "space":
            continue
        out.append((m.lastgroup, m.group(0)))
    out.append(("end", ""))
    return out


# ------------------------------------------------------------------- parser

# z3's printer uses this precedence, tightest first.  A parser whose table
# disagrees would read a printed term differently from the printer that wrote
# it, which is exactly what stage 3's round-trip check catches.
BINARY = [
    (["*", "/", "%"], "left"),
    (["+", "-"], "left"),
    (["<<", ">>"], "left"),
    (["<", "<=", ">", ">="], "left"),
    (["==", "!="], "left"),
    (["&"], "left"),
    (["^"], "left"),
    (["|"], "left"),
]


class Node(object):
    __slots__ = ("kind", "name", "kids", "value", "width", "sort")

    def __init__(self, kind, name=None, kids=None, value=None):
        self.kind = kind          # "app" | "var" | "num"
        self.name = name
        self.kids = kids or []
        self.value = value
        self.width = None         # int, once inferred
        self.sort = None          # "bv" | "bool"


class Parser(object):
    def __init__(self, toks):
        self.toks = toks
        self.i = 0

    def peek(self):
        return self.toks[self.i]

    def take(self):
        t = self.toks[self.i]
        self.i += 1
        return t

    def expect(self, text):
        k, v = self.take()
        if v != text:
            raise Refused("PARSE_ERROR", "expected %r, saw %r" % (text, v))

    def parse(self):
        n = self.expr(len(BINARY) - 1)
        k, v = self.peek()
        if k != "end":
            raise Refused("PARSE_ERROR", "trailing %r" % v)
        return n

    def expr(self, level):
        if level < 0:
            return self.unary()
        ops, _assoc = BINARY[level]
        left = self.expr(level - 1)
        while self.peek()[1] in ops and self.peek()[0] == "op":
            op = self.take()[1]
            right = self.expr(level - 1)
            left = Node("app", op, [left, right])
        return left

    def unary(self):
        k, v = self.peek()
        if k == "op" and v in ("~", "-", "!"):
            self.take()
            return Node("app", "u" + v, [self.unary()])
        return self.atom()

    def atom(self):
        k, v = self.take()
        if k == "op" and v == "(":
            n = self.expr(len(BINARY) - 1)
            self.expect(")")
            return n
        if k == "num":
            return Node("num", value=int(v))
        if k == "name":
            if self.peek()[1] == "(" and self.peek()[0] == "op":
                self.take()
                kids = []
                if self.peek()[1] != ")":
                    while True:
                        kids.append(self.expr(len(BINARY) - 1))
                        if self.peek()[1] == ",":
                            self.take()
                            continue
                        break
                self.expect(")")
                return Node("app", v, kids)
            if re.fullmatch(r"v[0-9]+", v):
                return Node("var", name=v)
            raise Refused("UNKNOWN_NODE", "bare name %r" % v)
        raise Refused("PARSE_ERROR", "unexpected %r" % v)


# ------------------------------------------------------- width inference

class Widths(object):
    """Union-find over width slots, plus a worklist for the additive
    constraint `Concat`'s result is the sum of its arguments' widths."""

    def __init__(self):
        self.up = {}
        self.val = {}
        self.next = 0
        self.sums = []            # (result slot, [argument slots])

    def fresh(self):
        s = self.next
        self.next += 1
        self.up[s] = s
        return s

    def find(self, s):
        while self.up[s] != s:
            self.up[s] = self.up[self.up[s]]
            s = self.up[s]
        return s

    def same(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        va, vb = self.val.get(ra), self.val.get(rb)
        if va is not None and vb is not None and va != vb:
            raise Refused("WIDTH_UNRESOLVED",
                          "two widths forced onto one slot: %d and %d" % (va, vb))
        self.up[rb] = ra
        if self.val.get(ra) is None and vb is not None:
            self.val[ra] = vb

    def fix(self, s, w):
        r = self.find(s)
        old = self.val.get(r)
        if old is not None and old != w:
            raise Refused("WIDTH_UNRESOLVED",
                          "slot already %d, now forced to %d" % (old, w))
        self.val[r] = w

    def get(self, s):
        return self.val.get(self.find(s))

    def settle(self):
        changed = True
        while changed:
            changed = False
            for res, args in self.sums:
                rv = self.get(res)
                avs = [self.get(a) for a in args]
                known = [v for v in avs if v is not None]
                if rv is None and len(known) == len(avs):
                    self.fix(res, sum(avs))
                    changed = True
                elif rv is not None and avs.count(None) == 1:
                    j = avs.index(None)
                    rest = sum(v for v in avs if v is not None)
                    self.fix(args[j], rv - rest)
                    changed = True


BOOL_RESULT = {"==", "!=", "<", "<=", ">", ">=", "ULE", "ULT", "UGE", "UGT",
               "And", "Or", "Not", "u!"}
BV_SAME_ALL = {"+", "-", "*", "&", "|", "^", "<<", ">>", "u~", "u-",
               "LShR", "UDiv", "URem", "SRem", "SDiv", "SMod"}
UNGUARDED_DIVISION_NAMES = {"bvudiv_i", "bvsdiv_i", "bvurem_i", "bvsrem_i",
                            "bvsmod_i"}
BV_COMPARE_SAME = {"==", "!=", "<", "<=", ">", ">=", "ULE", "ULT", "UGE", "UGT"}


def infer(node, free_widths, result_width):
    W = Widths()

    def walk(n):
        if n.kind == "app" and (n.name in FLOAT_NAMES or n.name.split(".")[0] in FLOAT_NAMES):
            raise Refused("FLOATING_POINT", "node %r" % n.name)
        if n.kind == "app" and n.name in UNGUARDED_DIVISION_NAMES:
            raise Refused("UNGUARDED_DIVISION", "node %r" % n.name)
        slot = W.fresh()
        n.width = slot
        if n.kind == "var":
            w = free_widths.get(n.name)
            if w is None:
                raise Refused("WIDTH_UNRESOLVED", "no width given for %r" % n.name)
            n.sort = "bv"
            W.fix(slot, w)
            return slot
        if n.kind == "num":
            n.sort = "bv"
            return slot
        name = n.name
        kids = [walk(k) for k in n.kids]
        if name in BOOL_RESULT:
            n.sort = "bool"
        else:
            n.sort = "bv"
        if name in BV_SAME_ALL:
            for k in kids:
                W.same(slot, k)
        elif name in BV_COMPARE_SAME:
            for k in kids[1:]:
                W.same(kids[0], k)
        elif name in ("And", "Or", "Not", "u!"):
            pass
        elif name == "If":
            if len(kids) != 3:
                raise Refused("PARSE_ERROR", "If with %d arguments" % len(kids))
            W.same(slot, kids[1])
            W.same(slot, kids[2])
        elif name == "Extract":
            if len(kids) != 3:
                raise Refused("PARSE_ERROR", "Extract with %d arguments" % len(kids))
            hi, lo = n.kids[0], n.kids[1]
            if hi.kind != "num" or lo.kind != "num":
                raise Refused("UNKNOWN_NODE", "Extract with non-literal bounds")
            # The first two arguments are BIT POSITIONS, not bit-vector values.
            # They carry no width of their own and must be kept out of the
            # width constraints entirely, or the resolver asks what width the
            # literal 31 has and refuses a term that is perfectly well formed.
            hi.sort = lo.sort = "index"
            W.fix(slot, hi.value - lo.value + 1)
        elif name == "Concat":
            W.sums.append((slot, list(kids)))
        elif name in ("ZeroExt", "SignExt"):
            if len(kids) != 2 or n.kids[0].kind != "num":
                raise Refused("UNKNOWN_NODE", "%s with a non-literal amount" % name)
            n.kids[0].sort = "index"     # a COUNT of added bits, not a value
            W.sums.append((slot, [kids[1], W.fresh()]))
            W.fix(W.sums[-1][1][1], n.kids[0].value)
        else:
            raise Refused("UNKNOWN_NODE", "no rule for %r" % name)
        return slot

    top = walk(node)
    if result_width is not None and node.sort == "bv":
        W.fix(top, result_width)
    W.settle()

    def resolve(n):
        if n.sort == "index":
            n.width = None
        elif n.sort == "bv":
            w = W.get(n.width)
            if w is None:
                raise Refused("WIDTH_UNRESOLVED",
                              "%s node" % (n.name or ("numeral %d" % n.value)))
            if w <= 0:
                raise Refused("WIDTH_UNRESOLVED", "non-positive width %d" % w)
            n.width = w
        else:
            n.width = None
        for k in n.kids:
            resolve(k)

    resolve(node)
    return node


# ---------------------------------------------- stage 3: rebuild in z3

def to_z3(n, env):
    import z3
    if n.kind == "var":
        return env[n.name]
    if n.kind == "num":
        return z3.BitVecVal(n.value, n.width)
    name = n.name
    # Extract's first two arguments and ZeroExt/SignExt's first are bit
    # POSITIONS and COUNTS, not bit-vector values; they have no width and are
    # never rebuilt as terms. Handle them before the generic recursion.
    if name == "Extract":
        return z3.Extract(n.kids[0].value, n.kids[1].value, to_z3(n.kids[2], env))
    if name == "ZeroExt":
        return z3.ZeroExt(n.kids[0].value, to_z3(n.kids[1], env))
    if name == "SignExt":
        return z3.SignExt(n.kids[0].value, to_z3(n.kids[1], env))
    k = [to_z3(c, env) for c in n.kids]
    two = {"+": lambda a, b: a + b, "-": lambda a, b: a - b,
           "*": lambda a, b: a * b, "&": lambda a, b: a & b,
           "|": lambda a, b: a | b, "^": lambda a, b: a ^ b,
           "<<": lambda a, b: a << b, ">>": lambda a, b: a >> b,
           "==": lambda a, b: a == b, "!=": lambda a, b: a != b,
           "<": lambda a, b: a < b, "<=": lambda a, b: a <= b,
           ">": lambda a, b: a > b, ">=": lambda a, b: a >= b}
    if name in two:
        return two[name](k[0], k[1])
    if name == "u~":
        return ~k[0]
    if name == "u-":
        return -k[0]
    if name == "u!":
        return z3.Not(k[0])
    if name == "Not":
        return z3.Not(k[0])
    if name == "And":
        return z3.And(*k)
    if name == "Or":
        return z3.Or(*k)
    if name == "If":
        return z3.If(k[0], k[1], k[2])
    if name == "Concat":
        return z3.Concat(*k) if len(k) > 1 else k[0]
    if name == "LShR":
        return z3.LShR(k[0], k[1])
    if name == "UDiv":
        return z3.UDiv(k[0], k[1])
    if name == "URem":
        return z3.URem(k[0], k[1])
    if name == "SRem":
        return z3.SRem(k[0], k[1])
    if name == "SDiv":
        return k[0] / k[1]
    if name == "SMod":
        return k[0] % k[1]
    if name in ("ULE",):
        return z3.ULE(k[0], k[1])
    if name in ("ULT",):
        return z3.ULT(k[0], k[1])
    if name in ("UGE",):
        return z3.UGE(k[0], k[1])
    if name in ("UGT",):
        return z3.UGT(k[0], k[1])
    raise Refused("UNKNOWN_NODE", "no z3 rebuild for %r" % name)


def roundtrip(node, text, free_widths):
    """Print the rebuilt term with z3's own printer and demand the input back.

    z3's simplifier turns a guarded division into the unguarded `bvudiv_i`
    family, and there is no public constructor for those symbols, so a term
    carrying one cannot be rebuilt and reprinted; such a term is reported as
    NOT round-tripped rather than silently passed.
    """
    import z3
    env = {name: z3.BitVec(name, w) for name, w in free_widths.items()}
    printed = str(to_z3(node, env))
    ok = " ".join(printed.split()) == " ".join(text.split())
    return ok, printed


# --------------------------------------------------------- stage 4: Lean

def lean_of(n, top=True):
    if n.kind == "var":
        return n.name
    if n.kind == "num":
        return "(%d#%d)" % (n.value, n.width)
    name = n.name
    if name == "Extract":
        return "(%s.extractLsb %d %d)" % (lean_of(n.kids[2], False),
                                          n.kids[0].value, n.kids[1].value)
    if name == "ZeroExt":
        return "(%s.zeroExtend %d)" % (lean_of(n.kids[1], False), n.width)
    if name == "SignExt":
        return "(%s.signExtend %d)" % (lean_of(n.kids[1], False), n.width)
    K = [lean_of(c, False) for c in n.kids]
    infix2 = {"+": "+", "-": "-", "*": "*", "&": "&&&", "|": "|||", "^": "^^^",
              "<<": "<<<"}
    if name in infix2:
        return "(%s %s %s)" % (K[0], infix2[name], K[1])
    if name == ">>":
        return "(%s.sshiftRight' %s)" % (K[0], K[1])
    if name == "LShR":
        return "(%s >>> %s)" % (K[0], K[1])
    if name == "u~":
        return "(~~~%s)" % K[0]
    if name == "u-":
        return "(-%s)" % K[0]
    if name in ("u!", "Not"):
        return "(!%s)" % K[0]
    if name == "==":
        return "(%s == %s)" % (K[0], K[1])
    if name == "!=":
        return "(!(%s == %s))" % (K[0], K[1])
    if name == "<=":
        return "(%s.sle %s)" % (K[0], K[1])
    if name == "<":
        return "(%s.slt %s)" % (K[0], K[1])
    if name == ">=":
        return "(%s.sle %s)" % (K[1], K[0])
    if name == ">":
        return "(%s.slt %s)" % (K[1], K[0])
    if name == "ULE":
        return "(%s.ule %s)" % (K[0], K[1])
    if name == "ULT":
        return "(%s.ult %s)" % (K[0], K[1])
    if name == "UGE":
        return "(%s.ule %s)" % (K[1], K[0])
    if name == "UGT":
        return "(%s.ult %s)" % (K[1], K[0])
    if name == "And":
        return "(" + " && ".join(K) + ")"
    if name == "Or":
        return "(" + " || ".join(K) + ")"
    if name == "If":
        return "(if %s = true then %s else %s)" % (K[0], K[1], K[2])
    if name == "Concat":
        out = K[0]
        for k in K[1:]:
            out = "(%s ++ %s)" % (out, k)
        return out
    if name == "UDiv":
        return "(%s / %s)" % (K[0], K[1])
    if name == "URem":
        return "(%s %% %s)" % (K[0], K[1])
    if name == "SDiv":
        return "(%s.sdiv %s)" % (K[0], K[1])
    if name == "SRem":
        return "(%s.srem %s)" % (K[0], K[1])
    if name == "SMod":
        return "(%s.smod %s)" % (K[0], K[1])
    raise Refused("UNKNOWN_NODE", "no Lean rule for %r" % name)


DIVIDE_NAMES = {"UDiv", "SDiv"}


def uses_divide(n):
    if n.kind == "app" and n.name in DIVIDE_NAMES:
        return True
    return any(uses_divide(k) for k in n.kids)


def translate(text, free_widths, result_width, check_roundtrip=True):
    """text -> {'lean': ..., 'refused': None} or {'refused': (cause, detail)}."""
    out = {"text": text, "free_symbol_widths": dict(free_widths),
           "result_width": result_width}
    try:
        node = Parser(tokenize(text)).parse()
        infer(node, free_widths, result_width)
        out["divide_by_zero_seam"] = uses_divide(node)
        if check_roundtrip:
            ok, printed = roundtrip(node, text, free_widths)
            out["z3_reprint"] = printed
            out["roundtrip_ok"] = ok
            if not ok:
                raise Refused("ROUNDTRIP_MISMATCH",
                              "z3 reprints it as %r" % printed)
        out["lean"] = lean_of(node)
        out["refused"] = None
    except Refused as r:
        out["refused"] = [r.cause, r.detail]
        out.setdefault("lean", None)
    return out


def print_operator_table():
    print("| printed layer-5 form | arity | result | Lean 4.24 form |")
    print("|---|---|---|---|")
    for printed, arity, res, lean in OPERATOR_TABLE:
        print("| `%s` | %s | %s | `%s` |"
              % (printed, "n" if arity < 0 else arity, res, lean))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "table":
        print_operator_table()
    else:
        sys.stderr.write("usage: term_to_lean.py table   (otherwise imported)\n")
