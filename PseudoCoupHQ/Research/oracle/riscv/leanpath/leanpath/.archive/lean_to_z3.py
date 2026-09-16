"""lean_to_z3 -- a Sail pure form (the Lean text of one instruction's
meaning, as `SailModel.strip` proposes it) read into a z3 term, so the
construction printer that already exists (task t4's `render_general`)
can print it in a language.

Plan leaf hq...lean_proof_path.emulation (log 274 §4): the emulation of
an arch-opcode is printed from the arch's own definition. The definition
is Sail's; this file only reads it.

What is written once here, and is the whole of what a person typed:

  * a tokenizer and a parser for the Lean subset the emit uses in a
    pure form: application by juxtaposition, the infix operators,
    `if/then/else`, `match .. with | .K => ..`, named arguments
    `(m := 64)`, type ascriptions `(x : Bool)`, numerals `0x3#12`;
  * the meaning of each lean-sail PRIMITIVE the pure forms call
    (`sign_extend`, `Sail.BitVec.extractLsb`, `shift_bits_left`, the
    Int-level `BitVec.toInt` / `Int.tdiv` / `to_bits_truncate`, ...),
    each as one z3 construction. These are the library's helpers, a
    finite set, the same set the widening leaf names; not one of them
    is an instruction.

Int values are carried as 128-bit two's complement bit-vectors, wide
enough for every product and quotient a 64-bit instruction forms.
"""
import re
import z3

INT_BITS = 128
CONSTANTS = {"xlen": 64, "xlen_bytes": 8, "log2_xlen": 6, "xlen_max": 64}


class Unknown(Exception):
    """a construct this reader does not know; the caller records it"""


# ------------------------------------------------------------------ tokens
TOKEN = re.compile(r"""
    (?P<num>0x[0-9a-fA-F_]+\#\d+|0b[01_]+\#\d+|\d+\#\d+|\d+)
  | (?P<op>\+\+\+|<<<|>>>|&&&|\|\|\||\^\^\^|~~~|==|!=|:=|←|≤b|≥b|<b|>b|&&|\|\||\^i|\*i|-i|\+i|≤|≥|\+|-|\*|/|%|<|>|:|=>|\||\(|\)|\{|\}|,)
  | (?P<id>\.?[A-Za-z_][A-Za-z0-9_'.!?]*)
  | (?P<ws>\s+)
  | (?P<str>"[^"]*")
""", re.X)


def tokens(text):
    out = []
    pos = 0
    while pos < len(text):
        m = TOKEN.match(text, pos)
        if not m:
            raise Unknown("cannot tokenize at: %r" % text[pos:pos + 30])
        pos = m.end()
        if m.lastgroup in ("ws", "str"):
            continue
        out.append((m.lastgroup, m.group(0)))
    return out


# ------------------------------------------------------------------ the tree
# node forms: ("num", text) ("id", name) ("app", f, [args]) ("bin", op, a, b)
#             ("un", op, a) ("if", c, a, b) ("match", scrutinee, [(ctor, expr)])
#             ("named", name, expr) ("ascribe", expr, type_text)
INFIX = {  # precedence: higher binds tighter
    "||": 1, "&&": 2,
    "==": 3, "!=": 3, "<b": 3, ">b": 3, "≤b": 3, "≥b": 3, "<": 3, ">": 3, "≤": 3, "≥": 3,
    "|||": 4, "^^^": 5, "&&&": 6,
    "<<<": 7, ">>>": 7,
    "+": 8, "-": 8, "+i": 8, "-i": 8, "+++": 8,
    "*": 9, "/": 9, "%": 9, "*i": 9,
    "^i": 10,
}


class Parser(object):
    def __init__(self, text):
        self.t = tokens(text)
        self.i = 0

    def peek(self, k=0):
        return self.t[self.i + k] if self.i + k < len(self.t) else (None, None)

    def take(self):
        tok = self.t[self.i]
        self.i += 1
        return tok

    def expect(self, val):
        tok = self.take()
        if tok[1] != val:
            raise Unknown("expected %r, found %r" % (val, tok[1]))

    def parse(self):
        e = self.block()
        if self.i != len(self.t):
            raise Unknown("trailing tokens: %r" % [t[1] for t in self.t[self.i:self.i + 6]])
        return e

    def block(self):
        """`let x := e` lines (a type ascription allowed) followed by the expression"""
        lets = []
        while self.peek()[1] == "let":
            self.take()
            name = self.take()[1]
            if self.peek()[1] == ":":
                self.take()
                while self.peek()[1] != ":=":
                    self.take()
            self.expect(":=")
            lets.append((name, self.expr(0)))
        e = self.expr(0)
        return ("let", lets, e) if lets else e

    def expr(self, min_prec):
        if self.peek()[1] == "let":
            return self.block()
        left = self.application()
        while True:
            kind, val = self.peek()
            if kind != "op" or val not in INFIX or INFIX[val] < min_prec:
                break
            prec = INFIX[val]
            self.take()
            right = self.expr(prec + 1)
            left = ("bin", val, left, right)
        return left

    def application(self):
        head = self.atom()
        args = []
        while True:
            kind, val = self.peek()
            if kind in ("num", "id") or (kind == "op" and val in ("(", "~~~")):
                if kind == "id" and val in ("then", "else", "with"):
                    break
                args.append(self.atom())
            else:
                break
        return ("app", head, args) if args else head

    def atom(self):
        kind, val = self.peek()
        if kind == "num":
            self.take()
            return ("num", val)
        if kind == "op" and val == "~~~":
            self.take()
            return ("un", "~~~", self.atom())
        if kind == "op" and val == "-":
            self.take()
            return ("un", "-", self.atom())
        if kind == "op" and val == "(":
            self.take()
            # a named argument (m := 64), or an ascription (e : T), or a parenthesized expression
            k2, v2 = self.peek()
            k3, v3 = self.peek(1)
            if k2 == "id" and k3 == "op" and v3 == ":=":
                self.take(); self.take()
                e = self.expr(0)
                self.expect(")")
                return ("named", v2, e)
            e = self.expr(0)
            k2, v2 = self.peek()
            if k2 == "op" and v2 == ":":
                self.take()
                depth = 0
                ty = []
                while True:
                    k3, v3 = self.peek()
                    if k3 is None:
                        raise Unknown("unclosed ascription")
                    if v3 == "(":
                        depth += 1
                    if v3 == ")":
                        if depth == 0:
                            break
                        depth -= 1
                    ty.append(v3)
                    self.take()
                self.expect(")")
                return ("ascribe", e, " ".join(ty))
            self.expect(")")
            return e
        if kind == "id":
            if val == "if":
                self.take()
                c = self.expr(0)
                self.expect("then")
                a = self.expr(0)
                self.expect("else")
                b = self.expr(0)
                return ("if", c, a, b)
            if val == "match":
                self.take()
                s = self.expr(0)
                self.expect("with")
                arms = []
                while self.peek()[1] == "|":
                    self.take()
                    ctor = self.take()[1]
                    self.expect("=>")
                    arms.append((ctor.lstrip("."), self.expr(0)))
                return ("match", s, arms)
            self.take()
            return ("id", val)
        raise Unknown("unexpected token %r" % (val,))


def parse(text):
    return Parser(text).parse()


# ------------------------------------------------------------------ values
# a value is (kind, payload): ("bv", z3 BitVec), ("int", z3 128-bit BitVec), ("nat", python int),
# ("bool", z3 Bool), ("enum", ctor name)
def bv(x):
    return ("bv", x)


def as_int_bits(v):
    """an Int value as the 128-bit two's complement bit-vector"""
    k, p = v
    if k == "int":
        return p
    if k == "nat":
        return z3.BitVecVal(p, INT_BITS)
    if k == "bv":
        return z3.ZeroExt(INT_BITS - p.size(), p)      # a bit-vector read as Int is its unsigned value
    raise Unknown("not an Int: %s" % k)


def nat_of(v):
    k, p = v
    if k == "nat":
        return p
    if k == "int" and z3.is_bv_value(p):
        return p.as_signed_long()
    if k == "bv" and z3.is_bv_value(p):
        return p.as_long()
    raise Unknown("not a static Nat: %s" % (v,))


def same_width(a, b, op):
    if a.size() != b.size():
        raise Unknown("%s over widths %d and %d" % (op, a.size(), b.size()))


class Reader(object):
    """evaluates a parsed pure form to a z3 term over the given inputs"""

    def __init__(self, env, enum_ctor_of=None):
        self.env = dict(env)                 # name -> value
        self.enum_ctor_of = enum_ctor_of or (lambda name: None)

    def value(self, node):
        kind = node[0]
        if kind == "num":
            return self.numeral(node[1])
        if kind == "id":
            return self.identifier(node[1])
        if kind == "named":
            return self.value(node[2])
        if kind == "ascribe":
            v = self.value(node[1])
            ty = node[2].replace(" ", "")
            m = re.match(r"^BitVec(\d+)$", ty)
            if m and v[0] == "nat":
                return bv(z3.BitVecVal(v[1], int(m.group(1))))
            if ty == "xlenbits" and v[0] == "nat":
                return bv(z3.BitVecVal(v[1], 64))
            return v
        if kind == "un":
            v = self.value(node[2])
            if node[1] == "~~~":
                return bv(~v[1]) if v[0] == "bv" else ("int", ~as_int_bits(v))
            if node[1] == "-":
                return ("nat", -v[1]) if v[0] == "nat" else ("int", -as_int_bits(v))
        if kind == "if":
            c = self.value(node[1])
            a = self.value(node[2])
            b = self.value(node[3])
            if c[0] != "bool":
                raise Unknown("if over a non-Bool")
            if a[0] == "nat" and b[0] != "nat":
                a = (b[0], self.lift(a, b))
            if b[0] == "nat" and a[0] != "nat":
                b = (a[0], self.lift(b, a))
            if a[0] != b[0]:
                raise Unknown("if arms of kinds %s and %s" % (a[0], b[0]))
            if a[0] == "nat":
                raise Unknown("if over static Nats with a dynamic condition")
            return (a[0], z3.If(c[1], a[1], b[1]))
        if kind == "match":
            s = self.value(node[1])
            if s[0] != "enum":
                raise Unknown("match over a non-enum value")
            for ctor, e in node[2]:
                if ctor == s[1] or ctor.split(".")[-1] == s[1].split(".")[-1]:
                    return self.value(e)
            raise Unknown("no arm for %s" % s[1])
        if kind == "let":
            saved = dict(self.env)
            for name, e in node[1]:
                self.env[name] = self.value(e)
            v = self.value(node[2])
            self.env = saved
            return v
        if kind == "bin":
            return self.binary(node[1], self.value(node[2]), self.value(node[3]))
        if kind == "app":
            return self.apply(node[1], node[2])
        raise Unknown("node %s" % kind)

    def lift(self, nat_v, like):
        if like[0] == "bv":
            return z3.BitVecVal(nat_v[1], like[1].size())
        if like[0] == "int":
            return z3.BitVecVal(nat_v[1], INT_BITS)
        raise Unknown("cannot lift a Nat to %s" % like[0])

    def numeral(self, text):
        if "#" in text:
            lit, width = text.split("#")
            return bv(z3.BitVecVal(int(lit.replace("_", ""), 0), int(width)))
        return ("nat", int(text))

    def identifier(self, name):
        if name in self.env:
            return self.env[name]
        if "." in name and name.split(".")[0] in self.env and self.env[name.split(".")[0]][0] == "struct":
            fields = self.env[name.split(".")[0]][1]
            field = name.split(".", 1)[1]
            if field in fields:
                return ("enum", fields[field].split(".")[-1])
            raise Unknown("no field %s" % field)
        if name in CONSTANTS:
            return ("nat", CONSTANTS[name])
        if name in ("true", "false"):
            return ("bool", z3.BoolVal(name == "true"))
        if name.startswith("."):
            return ("enum", name[1:])
        ctor = self.enum_ctor_of(name)
        if ctor is not None:
            return ("enum", ctor)
        if name in ("zeros", "ones"):
            raise Unknown("%s without a width" % name)
        raise Unknown("free name %s" % name)

    # ---------------------------------------------------------- operators
    def binary(self, op, a, b):
        if op in ("&&", "||"):
            return ("bool", (z3.And if op == "&&" else z3.Or)(a[1], b[1]))
        if op in ("==", "!="):
            x, y = self.align(a, b, op)
            return ("bool", x == y if op == "==" else x != y)
        if op in ("<b", ">b", "≤b", "≥b", "<", ">", "≤", "≥"):
            x, y = self.align(a, b, op, prefer_int=True)
            f = {"<b": lambda p, q: p < q, "<": lambda p, q: p < q,
                 ">b": lambda p, q: p > q, ">": lambda p, q: p > q,
                 "≤b": lambda p, q: p <= q, "≤": lambda p, q: p <= q,
                 "≥b": lambda p, q: p >= q, "≥": lambda p, q: p >= q}[op]
            return ("bool", f(x, y))
        if op in ("+i", "-i", "*i", "^i"):
            if a[0] == "nat" and b[0] == "nat":
                return ("nat", {"+i": a[1] + b[1], "-i": a[1] - b[1], "*i": a[1] * b[1], "^i": a[1] ** b[1]}[op])
            x, y = as_int_bits(a), as_int_bits(b)
            if op == "^i":
                raise Unknown("a dynamic power")
            return ("int", {"+i": x + y, "-i": x - y, "*i": x * y}[op])
        if op == "+++":
            return bv(z3.Concat(a[1], b[1]))
        if op in ("<<<", ">>>"):
            if a[0] != "bv":
                raise Unknown("shift of a non bit-vector")
            n = b[1] if b[0] == "bv" else z3.BitVecVal(nat_of(b), a[1].size())
            if n.size() != a[1].size():
                n = z3.ZeroExt(a[1].size() - n.size(), n) if n.size() < a[1].size() else z3.Extract(a[1].size() - 1, 0, n)
            return bv(a[1] << n if op == "<<<" else z3.LShR(a[1], n))
        if op in ("&&&", "|||", "^^^"):
            x, y = self.align(a, b, op)
            return bv({"&&&": x & y, "|||": x | y, "^^^": x ^ y}[op])
        if op in ("+", "-", "*", "/", "%"):
            if a[0] == "nat" and b[0] == "nat":
                return ("nat", {"+": a[1] + b[1], "-": a[1] - b[1], "*": a[1] * b[1], "/": a[1] // b[1], "%": a[1] % b[1]}[op])
            kind = "int" if "int" in (a[0], b[0]) else "bv"
            x, y = self.align(a, b, op, prefer_int=(kind == "int"))
            if op == "/":
                return (kind, x / y if kind == "int" else z3.UDiv(x, y))
            if op == "%":
                return (kind, x % y if kind == "int" else z3.URem(x, y))
            return (kind, {"+": x + y, "-": x - y, "*": x * y}[op])
        raise Unknown("operator %s" % op)

    def align(self, a, b, op, prefer_int=False):
        """two operands as z3 terms of one width"""
        if a[0] == "bool" and b[0] == "bool":
            return a[1], b[1]
        if a[0] == "enum" and b[0] == "enum":
            return z3.BoolVal(a[1] == b[1]), z3.BoolVal(True)
        if "int" in (a[0], b[0]) or (prefer_int and "bv" not in (a[0], b[0])):
            return as_int_bits(a), as_int_bits(b)
        if a[0] == "nat" and b[0] == "bv":
            return z3.BitVecVal(a[1], b[1].size()), b[1]
        if b[0] == "nat" and a[0] == "bv":
            return a[1], z3.BitVecVal(b[1], a[1].size())
        if a[0] == "bv" and b[0] == "bv":
            same_width(a[1], b[1], op)
            return a[1], b[1]
        raise Unknown("%s over kinds %s and %s" % (op, a[0], b[0]))

    # ---------------------------------------------------------- applications
    def apply(self, head, args):
        if head[0] != "id":
            raise Unknown("application of a non-identifier")
        f = head[1]
        named = {a[1]: self.value(a[2]) for a in args if a[0] == "named"}
        pos = [self.value(a) for a in args if a[0] != "named"]
        short = f.split(".")[-1]
        # --- widths
        if f in ("sign_extend", "zero_extend", "Sail.BitVec.signExtend", "Sail.BitVec.zeroExtend"):
            x = pos[0][1] if pos else None
            m = nat_of(named["m"]) if "m" in named else nat_of(pos[1])
            ext = z3.SignExt if "sign" in f.lower() else z3.ZeroExt
            if m < x.size():
                raise Unknown("extend to a narrower width")
            return bv(ext(m - x.size(), x) if m > x.size() else x)
        if f in ("Sail.BitVec.extractLsb", "extractLsb"):
            x = pos[0][1]
            hi, lo = nat_of(pos[1]), nat_of(pos[2])
            return bv(z3.Extract(hi, lo, x))
        if f in ("truncate", "Sail.BitVec.truncate"):
            x = pos[0][1]
            m = nat_of(named["m"]) if "m" in named else nat_of(pos[1])
            return bv(z3.Extract(m - 1, 0, x))
        if f in ("to_bits", "to_bits_truncate", "to_bits_unsafe", "to_bits_checked"):
            n = nat_of(named["l"]) if "l" in named else nat_of(pos[0]) if len(pos) > 1 else None
            v = pos[-1]
            if n is None:
                raise Unknown("to_bits without a width")
            if v[0] == "nat":
                return bv(z3.BitVecVal(v[1], n))
            return bv(z3.Extract(n - 1, 0, as_int_bits(v)))
        if f in ("BitVec.toInt", "toInt"):
            x = pos[0][1]
            return ("int", z3.SignExt(INT_BITS - x.size(), x))
        if f in ("BitVec.toNatInt", "BitVec.toNat", "toNatInt", "toNat", "Sail.BitVec.toNatInt"):
            x = pos[0][1]
            return ("int", z3.ZeroExt(INT_BITS - x.size(), x))
        if f in ("Int.tdiv", "tdiv"):
            return ("int", as_int_bits(pos[0]) / as_int_bits(pos[1]))     # z3 `/` on BitVec is signed division, truncating
        if f in ("Int.tmod", "tmod"):
            return ("int", z3.SRem(as_int_bits(pos[0]), as_int_bits(pos[1])))
        if f in ("Neg.neg",):
            v = pos[0]
            return ("nat", -v[1]) if v[0] == "nat" else ("int", -as_int_bits(v))
        if f in ("not",):
            v = pos[0]
            if v[0] == "bool":
                return ("bool", z3.Not(v[1]))
            return bv(~v[1])
        if f in ("bool_to_bit",):
            return bv(z3.If(pos[0][1], z3.BitVecVal(1, 1), z3.BitVecVal(0, 1)))
        if f in ("bool_to_bits",):
            return bv(z3.If(pos[0][1], z3.BitVecVal(1, 1), z3.BitVecVal(0, 1)))
        if f in ("bit_to_bool",):
            return ("bool", pos[0][1] == z3.BitVecVal(1, 1))
        if f in ("zeros", "ones"):
            n = nat_of(named["n"]) if "n" in named else nat_of(pos[0]) if pos else 64
            return bv(z3.BitVecVal(0 if f == "zeros" else (1 << n) - 1, n))
        # --- shifts by a bit-vector amount
        if f in ("shift_bits_left", "shift_bits_right", "shift_bits_right_arith", "Sail.shift_bits_left", "Sail.shift_bits_right"):
            x, sh = pos[0][1], pos[1]
            n = sh[1] if sh[0] == "bv" else z3.BitVecVal(nat_of(sh), x.size())
            if n.size() < x.size():
                n = z3.ZeroExt(x.size() - n.size(), n)
            elif n.size() > x.size():
                n = z3.Extract(x.size() - 1, 0, n)
            if short == "shift_bits_left":
                return bv(x << n)
            if short == "shift_bits_right":
                return bv(z3.LShR(x, n))
            return bv(x >> n)
        if f in ("shiftl", "shiftr", "arith_shiftr"):
            x = pos[0][1]
            n = z3.BitVecVal(nat_of(pos[1]), x.size()) if pos[1][0] == "nat" else pos[1][1]
            return bv(x << n if f == "shiftl" else z3.LShR(x, n) if f == "shiftr" else x >> n)
        if f in ("rotate_bits_left", "rotate_bits_right", "rotatel", "rotater"):
            x, sh = pos[0][1], pos[1]
            n = sh[1] if sh[0] == "bv" else z3.BitVecVal(nat_of(sh), x.size())
            if n.size() != x.size():
                n = z3.ZeroExt(x.size() - n.size(), n) if n.size() < x.size() else z3.Extract(x.size() - 1, 0, n)
            return bv(z3.RotateLeft(x, n) if "left" in f or f == "rotatel" else z3.RotateRight(x, n))
        # --- comparisons in Sail's mangled spelling: zopz0zI_s is <_s, zopz0zK_s is >_s, zopz0zIzJ is <=, zopz0zKzJ is >=
        m = re.match(r"^zopz0z(I|K|IzJ|KzJ)_(s|u)$", f)
        if m:
            x, y = pos[0][1], pos[1][1]
            same_width(x, y, f)
            signed = m.group(2) == "s"
            table = {"I": (lambda: x < y, lambda: z3.ULT(x, y)), "K": (lambda: x > y, lambda: z3.UGT(x, y)),
                     "IzJ": (lambda: x <= y, lambda: z3.ULE(x, y)), "KzJ": (lambda: x >= y, lambda: z3.UGE(x, y))}
            return ("bool", table[m.group(1)][0 if signed else 1]())
        if f in ("mult_to_bits_half",):
            # mult_to_bits_half (l := L) sign1 sign2 a b half : the 2L-bit product's half
            L = nat_of(named["l"]) if "l" in named else 64
            s1, s2, a, b, half = pos[0], pos[1], pos[2][1], pos[3][1], pos[4]
            ext = lambda s, x: z3.SignExt(L, x) if s[1].split(".")[-1] == "Signed" else z3.ZeroExt(L, x)
            prod = ext(s1, a) * ext(s2, b)
            return bv(z3.Extract(2 * L - 1, L, prod) if half[1].split(".")[-1] == "High" else z3.Extract(L - 1, 0, prod))
        if f in ("extend_value",):
            un, data = pos[0], pos[1][1]
            if un[0] != "bool" or not z3.is_true(z3.simplify(un[1])) and not z3.is_false(z3.simplify(un[1])):
                raise Unknown("extend_value with a dynamic signedness")
            return bv(z3.ZeroExt(64 - data.size(), data) if z3.is_true(z3.simplify(un[1])) else z3.SignExt(64 - data.size(), data))
        if f in ("Complement.complement",):
            return bv(~pos[0][1])
        if f in ("BitVec.update",):
            x, i, b = pos[0][1], nat_of(pos[1]), pos[2][1]
            parts = []
            if i + 1 <= x.size() - 1:
                parts.append(z3.Extract(x.size() - 1, i + 1, x))
            parts.append(b)
            if i >= 1:
                parts.append(z3.Extract(i - 1, 0, x))
            return bv(z3.Concat(*parts) if len(parts) > 1 else parts[0])
        if f in ("rev8",):                        # the bytes reversed
            x = pos[0][1]
            n = x.size() // 8
            return bv(z3.Concat(*[z3.Extract(8 * k + 7, 8 * k, x) for k in range(n)]))
        if f in ("brev8",):                       # the bits of every byte reversed
            x = pos[0][1]
            n = x.size() // 8
            bytes_ = [z3.Concat(*[z3.Extract(8 * k + j, 8 * k + j, x) for j in range(8)]) for k in range(n)]
            return bv(z3.Concat(*reversed(bytes_)) if n > 1 else bytes_[0])
        if f in ("BitVec.countTrailingZeros", "BitVec.countLeadingZeros"):
            x = pos[0][1]
            w = x.size()
            count = z3.BitVecVal(w, w)          # all zero -> the width
            order = range(w - 1, -1, -1) if "Trailing" in f else range(w)
            for i in order:                     # the innermost If is the bit nearest the counted end
                found = z3.Extract(i, i, x) == z3.BitVecVal(1, 1)
                position = i if "Trailing" in f else (w - 1 - i)
                count = z3.If(found, z3.BitVecVal(position, w), count)
            return ("int", z3.ZeroExt(INT_BITS - w, count))
        if f == "count_ones":
            # Sail: count_ones x : Nat, the number of set bits (a loop in the emit; monadic only for its mutable counter)
            x = pos[0][1]
            w = x.size()
            count = z3.BitVecVal(0, INT_BITS)
            for i in range(w):
                count = count + z3.ZeroExt(INT_BITS - 1, z3.Extract(i, i, x))
            return ("int", count)
        if f in ("carryless_mul", "carryless_mulr"):
            # Sail: carryless_mul a b : BitVec (2n), the xor of a shifted by each set bit of b;
            #       carryless_mulr a b : BitVec n, the same with a shifted right by (n-1-i)
            a, b = pos[0][1], pos[1][1]
            w = a.size()
            if f == "carryless_mul":
                wide = z3.ZeroExt(w, a)
                acc = z3.BitVecVal(0, 2 * w)
                for i in range(w):
                    bit = z3.Extract(i, i, b) == z3.BitVecVal(1, 1)
                    acc = z3.If(bit, acc ^ (wide << i), acc)
                return bv(acc)
            acc = z3.BitVecVal(0, w)
            for i in range(w):
                bit = z3.Extract(i, i, b) == z3.BitVecVal(1, 1)
                acc = z3.If(bit, acc ^ z3.LShR(a, w - 1 - i), acc)
            return bv(acc)
        if f in ("bits_of_int", "get_slice_int"):
            raise Unknown("%s" % f)
        raise Unknown("primitive %s" % f)


# ------------------------------------------------------------------ the pure form
def read_pure_form(inputs, lets, value_text, enums, choice, slot_width=None):
    """inputs: [(name, kind, width)] with kind 'bv' | 'bool' | 'enum' | 'nat';
    lets: [(name, text)] in order; value_text: the result's text;
    enums: {type: [ctors]}; choice: {param: concrete value} for the
    enumerated parameters. Returns the z3 term of the value.
    slot_width: when given, a bit-vector input narrower than it is carried
    in a slot of that width and its low bits are used (an emulation
    receives an immediate or a loaded byte in a register)."""
    env = {}
    for name, kind, width in inputs:
        if name in choice:
            v = choice[name]
            if isinstance(v, str) and v.strip().startswith("{"):
                fields = dict(re.findall(r"(\w+)\s*:=\s*([\w.]+)", v))
                env[name] = ("struct", fields)
            else:
                env[name] = ("bool", z3.BoolVal(v)) if kind == "bool" else ("nat", v) if kind == "nat" else ("enum", v)
        elif kind == "bv":
            if slot_width and width < slot_width:
                env[name] = bv(z3.Extract(width - 1, 0, z3.BitVec(name, slot_width)))
            else:
                env[name] = bv(z3.BitVec(name, width))
        elif kind == "bool":
            raise Unknown("Bool parameter %s not chosen" % name)
        elif kind == "enum":
            raise Unknown("enum parameter %s not chosen" % name)
        elif kind == "nat":
            raise Unknown("Nat parameter %s not chosen" % name)
    ctors = {}
    for t, cs in enums.items():
        for c in cs:
            ctors[c] = c
            ctors["%s.%s" % (t, c)] = c
    reader = Reader(env, lambda n: ctors.get(n))
    for name, text in lets:
        name = name.split(":")[0].strip()          # `result32 : (BitVec 32)` binds `result32`
        reader.env[name] = reader.value(parse(text))
    return reader.value(parse(value_text))
