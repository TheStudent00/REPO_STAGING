"""lean_tree -- Sail's Lean text (a pure form, a let, a subterm) parsed
into a tree; the reader `operator_for` and `render` walk. Node forms:
("num", text) ("id", name) ("app", f, [args]) ("bin", op, a, b)
("un", op, x) ("named", name, e) ("ascribe", e, type) ("if", c, a, b)
("match", s, [(ctor, e)]) ("let", [(name, e)], body).

Nothing here evaluates: Lean types and proves what these trees say.
(The parser was carried out of a retired file whose other half fed the
earlier renderer; that half is archived.)
"""
import re


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
