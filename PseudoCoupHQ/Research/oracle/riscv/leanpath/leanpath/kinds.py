"""kinds -- LeanExpr.kinds: DISCOVERY of the primitive kinds.

the owner's one universal numeric type is (sign, mant, expo); every primitive
kind is a constraint on it. This file asks how much of that by-hand
declaration a compiler-operator's OWN MEANING already states, and
answers it with rules over the arch-unit's Lean expression alone.

The kinds are data, never prose:

    ("unsigned", n)   sign 0, expo 0, mant <= n; wrap mod 2^n
    ("signed", n)     expo 0, mant <= n with the top bit the sign; wrap mod 2^n
    ("bool",)         mant <= 1
    ("ieee", e, m)    an IEEE binary holder of e exponent and m mantissa bits
    ("width", n)      n bits, SIGNEDNESS UNDETERMINED -- what the meaning
                      says when it never reads the top bit as a sign
    None              the meaning never reads this parameter at all

The rule, in one sentence: a compiler-operator's meaning tells the kind
of each of its parameters and of its result BY WHAT IT DOES AT THE
EDGES -- how many low bits it reads, and how it reads the top one.

Nothing here is keyed by an instruction name or by an operator token.
The rule's whole vocabulary is Sail's own primitive vocabulary
(`sign_extend`, `zero_extend`, `Sail.BitVec.extractLsb`,
`to_bits_truncate`, `BitVec.toInt`, `BitVec.toNatInt`, `bool_to_bit`,
the shifts, `Int.tdiv`, `Int.tmod`) plus the shape of the expression.
An instruction's enumeration constructor (`.ADD`, `.SLTU`) is used for
one thing only: to pick Sail's OWN match arm by textual identity with
the argument -- iota reduction, the step Lean itself takes. No table in
this file is keyed by such a name, and the declared holders and the
operator token of a unit are never read by `discover`.

  discover(meaning_text, pure_forms) -> {param: kind, "result": kind}

The command, registered in `__main__`:

  python3 -m leanpath kinds <units.json> <walk.json[,...]> <out.json> [LeanIM dir]
"""

import json
import os
import re

from . import lean_tree as LZ
from . import strip as ST


# --------------------------------------------------------------- the kinds
IEEE_BY_WIDTH = {16: (5, 10), 32: (8, 23), 64: (11, 52), 128: (15, 112)}


def normalise(kind):
    """one bit of mantissa IS the owner's truth constraint, however it was reached"""
    if kind and kind[0] in ("unsigned", "signed", "width") and kind[1] == 1:
        return ("bool",)
    return kind


def kind_width(kind):
    if kind is None:
        return None
    if kind[0] == "bool":
        return 1
    if kind[0] == "ieee":
        return 1 + kind[1] + kind[2]
    return kind[1]


def kind_sign(kind):
    """the signedness class of a kind, or None where it is undetermined"""
    if kind is None or kind[0] == "width":
        return None
    return kind[0]


def kind_of_rep(rep):
    """the declared holder of the manifest as a kind: i32 -> ("signed", 32).
    Used ONLY to compare against what discovery found, never inside it."""
    if not rep:
        return None
    m = re.match(r"^([iuf])(\d+)$", rep)
    if m:
        w = int(m.group(2))
        if m.group(1) == "i":
            return ("signed", w)
        if m.group(1) == "u":
            return ("unsigned", w)
        e, mm = IEEE_BY_WIDTH.get(w, (None, None))
        return ("ieee", e, mm) if e else None
    if rep == "bool":
        return ("bool",)
    return None


# ------------------------------------------------- Sail's primitive vocabulary
# the names the RULE reads. Every one is a Sail or Lean primitive: none is an
# instruction mnemonic, none is an operator token.
SIGN_EXTEND = ("sign_extend", "Sail.BitVec.signExtend", "signExtend")
ZERO_EXTEND = ("zero_extend", "Sail.BitVec.zeroExtend", "zeroExtend")
EXTRACT = ("Sail.BitVec.extractLsb", "BitVec.extractLsb", "extractLsb")
TRUNCATE = ("to_bits_truncate", "to_bits", "to_bits_unsafe", "to_bits_checked")
READ_SIGNED = ("BitVec.toInt", "toInt")
READ_UNSIGNED = ("BitVec.toNatInt", "BitVec.toNat", "toNatInt")
BIT_OF_BOOL = ("bool_to_bit", "bool_bit_forwards")
BOOL_OF_BIT = ("bit_to_bool", "bool_bit_backwards")
SHIFT_LEFT = ("shift_bits_left", "Sail.shift_bits_left", "BitVec.shiftLeft")
SHIFT_RIGHT = ("shift_bits_right", "Sail.shift_bits_right", "BitVec.ushiftRight")
SHIFT_RIGHT_ARITH = ("shift_bits_right_arith", "Sail.shift_bits_right_arith",
                     "BitVec.sshiftRight")
EXACT_INT = ("Int.tdiv", "Int.tmod", "Int.ediv", "Int.emod", "Int.fdiv", "Int.fmod")
ZEROS = ("zeros", "BitVec.zero", "sail_zeros")
ONES = ("ones", "sail_ones")
NEGATE = ("Neg.neg",)
NOT_BOOL = ("not", "Bool.not")
LENGTH = ("Sail.BitVec.length", "BitVec.length")
COMPLEMENT = ("Complement.complement",)

RULE_VOCABULARY = set(SIGN_EXTEND + ZERO_EXTEND + EXTRACT + TRUNCATE
                      + READ_SIGNED + READ_UNSIGNED + BIT_OF_BOOL + BOOL_OF_BIT
                      + SHIFT_LEFT + SHIFT_RIGHT + SHIFT_RIGHT_ARITH
                      + EXACT_INT + ZEROS + ONES + NEGATE + NOT_BOOL
                      + LENGTH + COMPLEMENT)

# the Sail TYPE that marks a float edge: a function that consumes a rounding
# mode is reading IEEE values, whatever the function is called.
ROUNDING_TYPE = "rounding_mode"

COMPARE = ("<b", ">b", "≤b", "≥b", "==", "!=", "<", ">", "≤", "≥")
CONGRUENT_BITS = ("+", "-", "*", "&&&", "|||", "^^^", "+++")
CONGRUENT_INT = ("+i", "-i", "*i", "^i")
BOOL_JOIN = ("&&", "||")


# --------------------------------------------------------------- the parser
class Parser(LZ.Parser):
    """lean_tree's parser, with Sail's record literal `{ f := e, g := e }`
    (the multiply's operand settings ride in one)."""

    def atom(self):
        kind, val = self.peek()
        if kind == "op" and val == "{":
            self.take()
            fields = {}
            while True:
                k, v = self.peek()
                if k == "op" and v == "}":
                    self.take()
                    break
                name = self.take()[1]
                self.expect(":=")
                fields[name] = self.expr(0)
                if self.peek()[1] == ",":
                    self.take()
            return ("record", fields)
        return LZ.Parser.atom(self)

    def application(self):
        head = self.atom()
        args = []
        while True:
            kind, val = self.peek()
            if kind in ("num", "id") or (kind == "op" and val in ("(", "~~~", "{")):
                if kind == "id" and val in KEYWORDS:
                    break
                args.append(self.atom())
            else:
                break
        return ("app", head, args) if args else head


# a bare keyword never continues an application: `... | .Low => e let x := ...`
KEYWORDS = ("then", "else", "with", "let", "match", "if", "fun", "do", "in")

# Sail's emit writes equality as a bare `=`, which lean_tree's token set does
# not carry; `==` is the same relation and does tokenize.
BARE_EQUALS = re.compile(r"(?<![:=<>!≤≥])=(?![=>])")


def parse(text):
    return Parser(BARE_EQUALS.sub("==", text)).parse()


def bare(node):
    """a node with its ascriptions and named wrappers peeled off"""
    while node[0] in ("ascribe", "named"):
        node = node[1] if node[0] == "ascribe" else node[2]
    return node


NUM = re.compile(r"^(0x[0-9a-fA-F_]+|0b[01_]+|\d+)(?:#(\d+))?$")


def literal(text):
    """a Lean numeral: ("0x001#12") -> (1, 12); ("31") -> (31, None)"""
    m = NUM.match(text)
    if not m:
        return None
    body = m.group(1).replace("_", "")
    v = int(body, 0) if body[:2] in ("0x", "0b") else int(body)
    return (v, int(m.group(2)) if m.group(2) else None)


def lit(value, width=None):
    return ("lit", value, width)


def significant(value, width):
    """how many low bits carry a constant: 0 -> 0, 1 -> 1, -1 at 64 -> 64"""
    if value is None:
        return width
    if value < 0:
        return width
    return value.bit_length()


# ------------------------------------------------------------ the expansion
class Forms(object):
    """the pure forms of Sail's execute clauses (SailModel.strip's rule)
    plus the emitted definitions, so the expansion can unfold anything the
    rule has no rule for until it reaches Sail's primitive vocabulary."""

    def __init__(self, lean_dir):
        self.lean_dir = lean_dir
        self.forms = {}
        self.defs = ST.emitted_defs(lean_dir)
        self.consts = {}
        self.float_heads = set()
        for name, text in self.defs.items():
            m = re.search(r"^(?:abbrev|def)\s+%s\s*(?::[^:=]*)?:=\s*(-?\d+)\s*$"
                          % re.escape(name), text, re.M)
            if m:
                self.consts[name] = int(m.group(1))
            head = text.split(":=", 1)[0]
            if ROUNDING_TYPE in head:
                self.float_heads.add(name)
        for clause in ST.clauses_of(lean_dir):
            prop = ST.propose(clause)
            if prop.get("refused") or prop.get("shape") != "straight":
                continue
            short = clause["name"][len("execute_"):]
            params = [v for v, _ in prop["reads"]] + [n for n, _ in prop["others"]]
            types = ["(BitVec 64)" for _ in prop["reads"]] + [t for _, t in prop["others"]]
            self.forms[short] = {"params": params, "types": types,
                                 "lets": list(prop["lets"]), "value": prop["value"]}

    def body(self, name):
        """the right-hand side of an emitted definition, parsed, with its
        parameter names -- or None when the rule may not unfold it."""
        text = self.defs.get(name)
        if text is None:
            return None
        m = re.match(r"^(?:@\[[^\]]*\]\s*)?(?:protected\s+|noncomputable\s+|private\s+)*"
                     r"(?:def|abbrev)\s+\S+\s*(.*?):=\s*(.*)$", text, re.S)
        if not m:
            return None
        sig, rhs = m.group(1), m.group(2)
        if "SailM" in sig or "Id.run" in rhs or "←" in rhs or "for " in rhs:
            return None          # monadic or a loop: not an expression the rule reads
        if re.search(r"\b%s\b" % re.escape(name), rhs):
            return None          # recursive
        # split_params also picks up the parenthesised RETURN type; a real
        # parameter always carries `name : type`
        params = [(n, t) for n, t in ST.split_params(sig) if n and t and not n.startswith("{")]
        try:
            return (params, parse(joined(rhs)))
        except Exception:
            return None


def joined(text):
    """an emitted body on one line, its lines joined by a space (strip's
    one_line is for the pure forms and joins structure lines with commas)"""
    return " ".join(ln.strip() for ln in text.strip().split("\n") if ln.strip())


def expand(node, env, forms, depth=0):
    """Sail's own definitions applied: beta for a pure form's parameters,
    iota for its match arms, let-substitution, and constant folding of the
    numerals. Nothing is chosen by a name; a match arm is taken when the
    argument's text IS the arm's constructor."""
    if depth > 24:
        return node
    t = node[0]
    if t in ("lit", "num"):
        if t == "num":
            got = literal(node[1])
            return lit(got[0], got[1]) if got else node
        return node
    if t == "record":
        return ("record", dict((k, expand(v, env, forms, depth + 1))
                               for k, v in node[1].items()))
    if t == "id":
        name = node[1].lstrip(".")
        if name in env:
            return env[name]
        if "." in name:                                  # a field of a record argument
            head, _, rest = name.partition(".")
            got = env.get(head)
            if got and got[0] == "record" and rest in got[1]:
                return got[1][rest]
        if name in forms.consts:
            return lit(forms.consts[name])
        body = forms.body(name)                          # a nullary emitted definition
        if body is not None and not body[0] and name not in RULE_VOCABULARY:
            return expand(body[1], {}, forms, depth + 1)
        return node
    if t == "named":
        return ("named", node[1], expand(node[2], env, forms, depth + 1))
    if t == "ascribe":
        return ("ascribe", expand(node[1], env, forms, depth + 1), node[2])
    if t == "un":
        x = expand(node[2], env, forms, depth + 1)
        if node[1] == "-" and x[0] == "lit":
            return lit(-x[1], x[2])
        return ("un", node[1], x)
    if t == "let":
        env = dict(env)
        for name, value in node[1]:
            name = name.split(":")[0].strip()
            env[name] = expand(value, env, forms, depth + 1)
        return expand(node[2], env, forms, depth + 1)
    if t == "if":
        cond = expand(node[1], env, forms, depth + 1)
        folded = fold_bool(cond)
        if folded is True:
            return expand(node[2], env, forms, depth + 1)
        if folded is False:
            return expand(node[3], env, forms, depth + 1)
        return ("if", cond, expand(node[2], env, forms, depth + 1),
                expand(node[3], env, forms, depth + 1))
    if t == "match":
        s = expand(node[1], env, forms, depth + 1)
        tag = s[1].rsplit(".", 1)[-1] if s[0] == "id" else None
        for ctor, arm in node[2]:
            if tag is not None and ctor.rsplit(".", 1)[-1] == tag:
                return expand(arm, env, forms, depth + 1)
        return ("match", s, [(c, expand(a, env, forms, depth + 1)) for c, a in node[2]])
    if t == "bin":
        a = expand(node[2], env, forms, depth + 1)
        b = expand(node[3], env, forms, depth + 1)
        return fold_bin(node[1], a, b)
    if t == "app":
        head = node[1]
        args = [expand(x, env, forms, depth + 1) for x in node[2]]
        if head[0] != "id":
            return ("app", expand(head, env, forms, depth + 1), args)
        name = head[1].lstrip(".")
        if name in env:                                   # a bound function-valued name
            return ("app", env[name], args)
        if name.startswith("pure_") and name[len("pure_"):] in forms.forms:
            form = forms.forms[name[len("pure_"):]]
            positional = [x for x in args if x[0] != "named"]
            inner = {}
            for i, p in enumerate(form["params"]):
                if i < len(positional):
                    inner[p] = positional[i]
            for name_i, value in form["lets"]:
                key = name_i.split(":")[0].strip()
                ascription = name_i.partition(":")[2].strip()
                value_node = expand(parse(joined(value)), inner, forms, depth + 1)
                inner[key] = ("ascribe", value_node, ascription) if ascription else value_node
            return expand(parse(joined(form["value"])), inner, forms, depth + 1)
        folded = fold_app(name, args)
        if folded is not None:
            return folded
        if name not in RULE_VOCABULARY and name not in forms.float_heads:
            body = forms.body(name)                        # unfold until the rule's vocabulary
            if body is not None:
                params, rhs = body
                positional = [x for x in args if x[0] != "named"]
                inner = {}
                for i, (p, _t) in enumerate(params):
                    if i < len(positional):
                        inner[p] = positional[i]
                for x in args:
                    if x[0] == "named":
                        inner[x[1]] = x[2]
                return expand(rhs, inner, forms, depth + 1)
        return ("app", head, args)
    return node


def fold_bool(node):
    """true / false where the expansion has settled it, else None"""
    if node[0] == "id" and node[1].lstrip(".") in ("true", "false"):
        return node[1].lstrip(".") == "true"
    if node[0] == "ascribe":
        return fold_bool(node[1])
    if node[0] == "app" and node[1][0] == "id" and node[1][1] in NOT_BOOL and len(node[2]) == 1:
        inner = fold_bool(node[2][0])
        return None if inner is None else (not inner)
    if node[0] == "bin" and node[1] in BOOL_JOIN:
        a, b = fold_bool(node[2]), fold_bool(node[3])
        if node[1] == "&&":
            if a is False or b is False:
                return False
            return True if (a and b) else None
        if a is True or b is True:
            return True
        return False if (a is False and b is False) else None
    return None


def fold_bin(op, a, b):
    """the numeric identities the expansion needs so an immediate of zero
    does not hide the edge underneath it. Arithmetic, not a name rule."""
    la, lb = bare(a), bare(b)
    if la[0] == "lit" and lb[0] == "lit" and la[1] is not None and lb[1] is not None:
        if op in COMPARE:
            got = {"==": la[1] == lb[1], "!=": la[1] != lb[1], "<b": la[1] < lb[1],
                   ">b": la[1] > lb[1], "≤b": la[1] <= lb[1], "≥b": la[1] >= lb[1],
                   "<": la[1] < lb[1], ">": la[1] > lb[1],
                   "≤": la[1] <= lb[1], "≥": la[1] >= lb[1]}.get(op)
            if got is not None:
                return ("id", "true" if got else "false")
        w = la[2] or lb[2]
        if op in ("+", "+i"):
            return lit(la[1] + lb[1], w)
        if op in ("-", "-i"):
            return lit(la[1] - lb[1], w)
        if op in ("*", "*i"):
            return lit(la[1] * lb[1], w)
        if op == "^i":
            return lit(la[1] ** lb[1], w)
    if op in ("+", "-", "|||", "^^^", "+i", "-i", "<<<", ">>>") and lb[0] == "lit" and lb[1] == 0:
        return a
    if op in ("+", "|||", "^^^", "+i") and la[0] == "lit" and la[1] == 0:
        return b
    return ("bin", op, a, b)


def fold_app(name, args):
    positional = [bare(x) for x in args if x[0] != "named"]
    named = dict((x[1], bare(x[2])) for x in args if x[0] == "named")
    width = named.get("m") or named.get("n") or named.get("l")
    width = width[1] if (width is not None and width[0] == "lit") else None
    if name in ZEROS:
        return lit(0, width)
    if name in ONES and width:
        return lit(-1, width)
    if not positional or positional[0][0] != "lit":
        return None
    v, w = positional[0][1], positional[0][2]
    if name in SIGN_EXTEND and width:
        if w and v >= 0 and (v >> (w - 1)) & 1:
            v = v - (1 << w)
        return lit(v, width)
    if name in ZERO_EXTEND and width:
        return lit(v, width)
    if name in READ_SIGNED:
        if w and v >= 0 and (v >> (w - 1)) & 1:
            v = v - (1 << w)
        return lit(v)
    if name in READ_UNSIGNED:
        return lit(v if v >= 0 else v + (1 << (w or 64)), None)
    if name in TRUNCATE and width:
        return lit(v, width)
    return None


# ------------------------------------------------------------- the reading
BITVEC = re.compile(r"BitVec\s+(\d+)")
REGISTER_WIDTH = 64


class Val(object):
    """what a node's value IS: a vector of `width` bits whose value occupies
    the low `sig` of them, read as `sign`; or an integer; or a truth value."""

    def __init__(self, level="bits", width=None, sig=None, sign=None, ieee=None):
        self.level, self.width, self.sig, self.sign, self.ieee = level, width, sig, sign, ieee

    def kind(self):
        if self.ieee:
            return ("ieee", self.ieee[0], self.ieee[1])
        n = self.sig if self.sig is not None else self.width
        if n is None:
            return None
        if self.sign:
            return normalise((self.sign, n))
        return normalise(("width", n))


def join(a, b):
    """two arms of the same `if` or `match`: the wider view, the sign only
    where both arms agree"""
    return Val(a.level,
               max(a.width or 0, b.width or 0) or None,
               max(a.sig or 0, b.sig or 0) or None,
               a.sign if a.sign == b.sign else (a.sign or b.sign if not (a.sign and b.sign) else None),
               a.ieee or b.ieee)


def width_of(node):
    """the width a node's value has, read off its own shape"""
    t = node[0]
    if t == "lit":
        return node[2]
    if t == "ascribe":
        m = BITVEC.search(node[2])
        return int(m.group(1)) if m else width_of(node[1])
    if t == "named":
        return width_of(node[2])
    if t == "id":
        return REGISTER_WIDTH
    if t == "app" and node[1][0] == "id":
        name = node[1][1].lstrip(".")
        named = dict((x[1], x[2]) for x in node[2] if x[0] == "named")
        positional = [x for x in node[2] if x[0] != "named"]
        for key in ("m", "l", "n"):
            if key in named and named[key][0] == "lit":
                return named[key][1]
        if name in EXTRACT and len(positional) == 3:
            hi, lo = bare(positional[1]), bare(positional[2])
            if hi[0] == "lit" and lo[0] == "lit":
                return hi[1] - lo[1] + 1
        if name in BIT_OF_BOOL:
            return 1
        if positional:
            return width_of(positional[0])
    if t == "bin" and node[1] in CONGRUENT_BITS:
        return max(width_of(node[2]) or 0, width_of(node[3]) or 0) or None
    if t in ("if",):
        return max(width_of(node[2]) or 0, width_of(node[3]) or 0) or None
    return None


class Reading(object):
    """the walk that reads the edges and records what each argument met"""

    def __init__(self, args, forms):
        self.args = set(args)
        self.forms = forms
        self.facts = dict((v, []) for v in args)
        self.edges = []

    def note(self, name, fact, why):
        self.facts.setdefault(name, []).append(fact)
        self.edges.append({"name": name, "why": why})

    # ------------------------------------------------------------------
    def visit(self, node, want, sign, ic):
        """want: how many low bits the context reads; sign: how it reads the
        top one; ic: (truncation width, whether an exact operation is below)
        for the integer level."""
        t = node[0]
        if t == "lit":
            return Val("bits", node[2], significant(node[1], node[2] or 64), None)
        if t == "record":
            return Val("opaque")
        if t == "id":
            name = node[1].lstrip(".")
            if name in self.args:
                self.note(name, (min(want or REGISTER_WIDTH, REGISTER_WIDTH), sign),
                          "read in its low %d bits%s" % (min(want or REGISTER_WIDTH, REGISTER_WIDTH),
                                                         ", as %s" % sign if sign else ""))
                return Val("bits", REGISTER_WIDTH, REGISTER_WIDTH, None)
            if name in ("true", "false"):
                return Val("bool", 1, 1, "unsigned")
            return Val("opaque")
        if t == "named":
            return self.visit(node[2], want, sign, ic)
        if t == "ascribe":
            w = BITVEC.search(node[2])
            w = int(w.group(1)) if w else None
            got = self.visit(node[1], min(want, w) if (want and w) else want, sign, ic)
            if w:
                got.width = w
                got.sig = min(got.sig or w, w)
            return got
        if t == "un":
            got = self.visit(node[2], want, None, ic)
            return Val(got.level, got.width, got.width or got.sig, None)
        if t == "if":
            self.visit(node[1], REGISTER_WIDTH, None, (None, True))
            return join(self.visit(node[2], want, sign, ic),
                        self.visit(node[3], want, sign, ic))
        if t == "match":
            self.visit(node[1], REGISTER_WIDTH, None, (None, True))
            got = None
            for _ctor, arm in node[2]:
                v = self.visit(arm, want, sign, ic)
                got = v if got is None else join(got, v)
            return got or Val("opaque")
        if t == "bin":
            return self.binary(node, want, sign, ic)
        if t == "app":
            return self.application(node, want, sign, ic)
        return Val("opaque")

    # ------------------------------------------------------------------
    def binary(self, node, want, sign, ic):
        op, a, b = node[1], node[2], node[3]
        if op in COMPARE:
            if not self.truth_reading(op, a, b):
                self.visit(a, REGISTER_WIDTH, sign, (None, True))
                self.visit(b, REGISTER_WIDTH, sign, (None, True))
            return Val("bool", 1, 1, "unsigned")
        if op in BOOL_JOIN:
            self.visit(a, REGISTER_WIDTH, None, (None, True))
            self.visit(b, REGISTER_WIDTH, None, (None, True))
            return Val("bool", 1, 1, "unsigned")
        if op in CONGRUENT_INT:
            va = self.visit(a, want, sign, ic)
            vb = self.visit(b, want, sign, ic)
            return Val("int", None, None, va.sign if va.sign == vb.sign else (va.sign or vb.sign))
        if op in ("/", "%"):
            va = self.visit(a, want, sign, (None, True))
            vb = self.visit(b, want, sign, (None, True))
            return Val("int", None, None, va.sign if va.sign == vb.sign else (va.sign or vb.sign))
        # a congruent bit-vector operation: the low `want` bits of the answer
        # need only the low `want` bits of each side, and read no sign
        mask = self.mask_width(b) if op == "&&&" else None
        va = self.visit(a, min(want or REGISTER_WIDTH, mask) if mask else want, None, ic)
        mask_a = self.mask_width(a) if op == "&&&" else None
        vb = self.visit(b, min(want or REGISTER_WIDTH, mask_a) if mask_a else want, None, ic)
        sig = max(va.sig or 0, vb.sig or 0) or None
        if op == "&&&" and va.sig is not None and vb.sig is not None:
            sig = min(va.sig, vb.sig)          # an and cannot set a bit above either side's value
        if mask is not None:
            sig = min(sig or mask, mask)
        if mask_a is not None:
            sig = min(sig or mask_a, mask_a)
        both = va.sign if va.sign == vb.sign else None
        return Val("bits", max(va.width or 0, vb.width or 0) or None, sig, both)

    def mask_width(self, node):
        """`x &&& (2^k - 1)` reads only the low k bits of x -- a mask, read
        off the constant, not off any name"""
        node = bare(node)
        if node[0] == "lit" and node[1] is not None and node[1] > 0:
            v = node[1]
            if (v & (v + 1)) == 0:
                return v.bit_length()
        return None

    def truth_reading(self, op, a, b):
        """the meaning depends on this argument ONLY through `x == 0`: an
        unsigned comparison of a bare argument against 0 or 1. the owner's rule --
        `sltiu x 1`, `0 <u x`, a mask by 1 -- one bit of information, which
        is the owner's truth constraint (mant <= 1)."""
        for x, y, flip in ((a, b, False), (b, a, True)):
            name = self.bare_unsigned(bare(x))
            y = bare(y)
            if name is None or y[0] != "lit" or y[1] is None:
                continue
            test = op
            if flip:
                test = {"<b": ">b", ">b": "<b", "≤b": "≥b",
                        "≥b": "≤b"}.get(op, op)
            v = y[1]
            zero_test = ((test in ("<b",) and v == 1) or (test in ("≤b",) and v == 0)
                         or (test == "==" and v == 0))
            nonzero = ((test in (">b",) and v == 0) or (test in ("≥b",) and v == 1)
                       or (test == "!=" and v == 0))
            if zero_test or nonzero:
                self.note(name, ("truth",), "read only as zero / not zero")
                return True
        return False

    def bare_unsigned(self, node):
        """`BitVec.toNatInt a` over a bare argument, and nothing else"""
        if node[0] == "app" and node[1][0] == "id":
            name = node[1][1].lstrip(".")
            positional = [x for x in node[2] if x[0] != "named"]
            if name in READ_UNSIGNED and len(positional) == 1:
                inner = bare(positional[0])
                if inner[0] == "id" and inner[1].lstrip(".") in self.args:
                    return inner[1].lstrip(".")
        return None

    # ------------------------------------------------------------------
    def application(self, node, want, sign, ic):
        head = node[1]
        if head[0] != "id":
            for x in node[2]:
                self.visit(x, want, None, ic)
            return Val("opaque")
        name = head[1].lstrip(".")
        named = dict((x[1], x[2]) for x in node[2] if x[0] == "named")
        pos = [x for x in node[2] if x[0] != "named"]
        out = None
        for key in ("m", "l", "n"):
            if key in named and named[key][0] == "lit":
                out = named[key][1]

        if name in SIGN_EXTEND and pos:
            inner = width_of(pos[0]) or want
            self.visit(pos[0], inner, "signed", ic)
            return Val("bits", out or REGISTER_WIDTH, inner, "signed")
        if name in ZERO_EXTEND and pos:
            inner = width_of(pos[0]) or want
            self.visit(pos[0], inner, "unsigned", ic)
            return Val("bits", out or REGISTER_WIDTH, inner, "unsigned")
        if name in EXTRACT and len(pos) == 3:
            hi = bare(pos[1])[1] if bare(pos[1])[0] == "lit" else None
            lo = bare(pos[2])[1] if bare(pos[2])[0] == "lit" else None
            if hi is not None and lo is not None:
                # a slice of the low bits under a context that reads only `want`
                # of them demands only `want` of its operand
                if lo == 0:
                    self.visit(pos[0], min(hi + 1, want or hi + 1), sign, ic)
                    return Val("bits", hi + 1, min(hi + 1, want or hi + 1), sign)
                self.visit(pos[0], hi + 1, None, ic)
                return Val("bits", hi - lo + 1, hi - lo + 1, None)
        if name in TRUNCATE and pos:
            n = min(out or REGISTER_WIDTH, want or REGISTER_WIDTH)
            got = self.visit(pos[0], None, sign, (n, ic[1] if ic else False))
            return Val("bits", out or REGISTER_WIDTH, n, got.sign)
        if name in READ_SIGNED + READ_UNSIGNED and pos:
            reads = "signed" if name in READ_SIGNED else "unsigned"
            w = width_of(pos[0]) or REGISTER_WIDTH
            counts = bool(ic and (ic[1] or ic[0] is None or (ic[0] or 0) > w))
            self.visit(pos[0], w, reads if counts else None, ic)
            return Val("int", None, None, reads if counts else None)
        if name in BIT_OF_BOOL and pos:
            self.visit(pos[0], REGISTER_WIDTH, None, (None, True))
            return Val("bits", 1, 1, "unsigned")
        if name in BOOL_OF_BIT and pos:
            self.visit(pos[0], 1, None, ic)
            return Val("bool", 1, 1, "unsigned")
        if name in SHIFT_RIGHT_ARITH and len(pos) >= 1:
            v = self.visit(pos[0], want, "signed", ic)
            for x in pos[1:]:
                self.visit(x, width_of(x) or REGISTER_WIDTH, "unsigned", ic)
            return Val("bits", v.width, v.sig, "signed")
        if name in SHIFT_RIGHT and len(pos) >= 1:
            v = self.visit(pos[0], want, "unsigned", ic)
            for x in pos[1:]:
                self.visit(x, width_of(x) or REGISTER_WIDTH, "unsigned", ic)
            return Val("bits", v.width, v.sig, "unsigned")
        if name in SHIFT_LEFT and len(pos) >= 1:
            v = self.visit(pos[0], want, None, ic)
            for x in pos[1:]:
                self.visit(x, width_of(x) or REGISTER_WIDTH, "unsigned", ic)
            return Val("bits", v.width, v.width or v.sig, None)
        if name in EXACT_INT:
            got = None
            for x in pos:
                v = self.visit(x, want, sign, (None, True))
                got = v if got is None else Val("int", None, None,
                                                v.sign if v.sign == got.sign else (got.sign or v.sign))
            return got or Val("int")
        if name in NEGATE and pos:
            got = self.visit(pos[0], want, sign, ic)
            return Val(got.level, got.width, got.width or got.sig, got.sign)
        if name in NOT_BOOL and pos:
            self.visit(pos[0], REGISTER_WIDTH, None, (None, True))
            return Val("bool", 1, 1, "unsigned")
        if name in COMPLEMENT and pos:
            got = self.visit(pos[0], want, None, ic)
            return Val("bits", got.width, got.width or got.sig, None)
        if name in LENGTH:
            return Val("int")
        if name in self.forms.float_heads:
            # a Sail function that consumes a rounding mode is reading IEEE
            # values: the kind of each bit-vector operand is its own width's
            # binary format. Keyed by Sail's TYPE, never by the function.
            for x in pos:
                w = width_of(x) or REGISTER_WIDTH
                if x[0] == "id" and x[1].lstrip(".") in self.args:
                    e, m = IEEE_BY_WIDTH.get(w, (None, None))
                    if e:
                        self.note(x[1].lstrip("."), ("ieee", e, m),
                                  "an operand of a Sail function that takes a rounding mode")
                        continue
                self.visit(x, w, None, ic)
            w = width_of(node) or REGISTER_WIDTH
            e, m = IEEE_BY_WIDTH.get(w, (None, None))
            return Val("bits", w, w, None, (e, m) if e else None)
        # a function the rule has no rule for and could not unfold: its
        # arguments are read whole, with nothing said about their sign
        for x in pos:
            self.visit(x, width_of(x) or REGISTER_WIDTH, None, ic)
        return Val("opaque", width_of(node))

    # ------------------------------------------------------------------
    def kind_of(self, name):
        obs = self.facts.get(name) or []
        if not obs:
            return None
        ieee = [o for o in obs if o and o[0] == "ieee"]
        if ieee:
            return ieee[0]
        if all(o == ("truth",) for o in obs):
            return ("bool",)
        widths = [o[0] for o in obs if o != ("truth",)]
        if not widths:
            return ("bool",)
        w = max(widths)
        signs = set(o[1] for o in obs if o != ("truth",) and o[0] == w and o[1])
        if len(signs) == 1:
            return normalise((signs.pop(), w))
        return normalise(("width", w))


# ------------------------------------------------------------------ the rule
ARGUMENT_NAMES = ("a", "b", "c", "d")


def discover(meaning_text, pure_forms, detail=None):
    """The rule. Input: one arch-unit's meaning as Sail's Lean text, and the
    pure forms (a `Forms`, or a LeanIM directory). Output: the kind of each
    argument register the meaning names and the kind of its result.

    Nothing about the unit's declared holders, its language, its operator
    token or its instruction mnemonics is read."""
    if isinstance(pure_forms, str):
        pure_forms = Forms(pure_forms)
    text = joined(meaning_text.strip())
    args = [v for v in ARGUMENT_NAMES if re.search(r"\b%s\b" % v, text)]
    tree = expand(parse(text), {}, pure_forms)
    reading = Reading(args, pure_forms)
    value = reading.visit(tree, REGISTER_WIDTH, None, (REGISTER_WIDTH, False))
    out = dict((v, reading.kind_of(v)) for v in args)
    constant = not any(reading.facts.get(v) for v in args)
    out["result"] = None if constant else value.kind()
    if detail is not None:
        detail["expanded"] = to_text(tree)
        detail["edges"] = reading.edges
        detail["constant_meaning"] = constant
    return out


def to_text(node):
    t = node[0]
    if t == "lit":
        return "%d%s" % (node[1], "#%d" % node[2] if node[2] else "")
    if t == "num":
        return node[1]
    if t == "id":
        return node[1]
    if t == "named":
        return "(%s := %s)" % (node[1], to_text(node[2]))
    if t == "ascribe":
        return "(%s : %s)" % (to_text(node[1]), node[2])
    if t == "un":
        return "(%s %s)" % (node[1], to_text(node[2]))
    if t == "bin":
        return "(%s %s %s)" % (to_text(node[2]), node[1], to_text(node[3]))
    if t == "if":
        return "(if %s then %s else %s)" % (to_text(node[1]), to_text(node[2]), to_text(node[3]))
    if t == "match":
        return "(match %s with %s)" % (to_text(node[1]),
                                       " ".join("| %s => %s" % (c, to_text(a)) for c, a in node[2]))
    if t == "record":
        return "{ %s }" % ", ".join("%s := %s" % (k, to_text(v)) for k, v in sorted(node[1].items()))
    if t == "app":
        return "(%s %s)" % (to_text(node[1]), " ".join(to_text(x) for x in node[2]))
    return str(node)


# --------------------------------------------------------- the comparison
AGREE, DISAGREE, UNDETERMINED = "agree", "disagree", "undetermined"

# causes are codes (snake_case words, never a token); their sentences ride in meta
CAUSE_NEVER_READ = "never_read"
CAUSE_SIGN_UNTOUCHED = "sign_not_read"
CAUSE_WIDER = "reads_wider_than_holder"
CAUSE_NARROWER = "reads_narrower_than_holder"
CAUSE_SIGN_OPPOSITE = "sign_opposite"
CAUSE_IEEE_AS_BITS = "ieee_not_reached"
CAUSE_CONSTANT = "constant_meaning"
CAUSE_NO_DECLARATION = "no_declared_holder"

CAUSE_TEXT = {
    CAUSE_NEVER_READ: "the meaning never reads this parameter",
    CAUSE_SIGN_UNTOUCHED: "the width agrees and the meaning never reads the top bit as a sign",
    CAUSE_WIDER: "the meaning reads more bits than the holder has (it arrives already extended in the register)",
    CAUSE_NARROWER: "the meaning reads fewer bits than the holder has",
    CAUSE_SIGN_OPPOSITE: "the meaning reads a signedness the holder does not declare",
    CAUSE_IEEE_AS_BITS: ("the holder is an IEEE format and the meaning never reaches a float edge "
                         "(the walk's meaning is over the integer argument registers)"),
    CAUSE_CONSTANT: "the meaning is a constant and says nothing about the result",
    CAUSE_NO_DECLARATION: "no declared holder to compare against",
}


def compare(found, declared):
    """found against declared, in two coordinates: the width and the
    signedness class. Nothing is guessed: a width the meaning did not
    state is undetermined, not agreement."""
    if declared is None:
        return UNDETERMINED, CAUSE_NO_DECLARATION
    if found is None:
        return UNDETERMINED, CAUSE_NEVER_READ
    if found == declared:
        return AGREE, None
    fw, dw = kind_width(found), kind_width(declared)
    fs, ds = kind_sign(found), kind_sign(declared)
    if ds == "ieee" and fs != "ieee":
        # the walk's meaning is over the integer argument registers; a meaning
        # that never reaches a float edge has not determined an IEEE kind, and
        # has not contradicted one either
        return UNDETERMINED, CAUSE_IEEE_AS_BITS
    if fw == dw:
        if fs is None:
            return UNDETERMINED, CAUSE_SIGN_UNTOUCHED
        return DISAGREE, CAUSE_SIGN_OPPOSITE
    if fw > dw:
        return DISAGREE, CAUSE_WIDER
    return DISAGREE, CAUSE_NARROWER


# ------------------------------------------------------------- the command
DEFAULT_LEANIM = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "cache", "sail-riscv_6266b40c_sail_8eb1fb6b_all_modules", "LeanIM")


def type_to_rep(manifest_meta):
    """the manifest's own holder table read back as {declared type: rep},
    so a declared result type needs no table written here"""
    table = {}
    for h in (manifest_meta.get("meta") or {}).get("holders") or []:
        if h.get("type") and h.get("rep"):
            table[h["type"]] = h["rep"]
    return table


def cmd_kinds(argv, say, write_json):
    units_json, walk_jsons, out_json = argv[0], argv[1], argv[2]
    lean_dir = argv[3] if len(argv) > 3 else os.environ.get("LEANPATH_LEANIM", DEFAULT_LEANIM)
    forms = Forms(lean_dir)
    say("  pure forms read from the emit: %d" % len(forms.forms))

    units = json.load(open(units_json))
    by_name = dict((u["name"], u) for u in units)
    meta_path = os.path.join(os.path.dirname(os.path.abspath(units_json)), "manifest_meta.json")
    reps, result_of = {}, {}
    if os.path.exists(meta_path):
        meta = json.load(open(meta_path))
        reps = type_to_rep(meta)
        manifest = meta.get("manifest")
        if manifest and not os.path.isabs(manifest):
            # the probes command wrote the path relative to where it ran: the module root
            module_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            for base in (module_root, os.getcwd(), os.path.dirname(os.path.abspath(meta_path))):
                if os.path.exists(os.path.join(base, manifest)):
                    manifest = os.path.join(base, manifest)
                    break
        if manifest and os.path.exists(manifest):
            probes = json.load(open(manifest))["probes"]
            probes = list(probes.values()) if isinstance(probes, dict) else list(probes)
            for p in probes:
                result_of[p["n"]] = p.get("result_type")

    rows = []
    for wj in walk_jsons.split(","):
        rows += json.load(open(wj))["rows"]
    say("  walk rows: %d" % len(rows))

    out_units, tally = [], {}
    for w in rows:
        unit = by_name.get(w.get("unit"))
        if unit is None:
            continue
        lang = unit.get("lang")
        bucket = tally.setdefault(lang, blank_tally())
        bucket["units"] += 1
        probe = unit.get("probe") or {}
        declared = [kind_of_rep(probe.get("lhs_rep"))]
        if probe.get("rhs_rep"):
            declared.append(kind_of_rep(probe.get("rhs_rep")))
        declared_result = kind_of_rep(reps.get(result_of.get(probe.get("n"))))
        if w.get("verdict") != "CERTIFIED":
            bucket["units_without_a_meaning"] += 1
            continue
        bucket["units_with_a_meaning"] += 1
        detail = {}
        try:
            found = discover(w["proposal"], forms, detail)
        except Exception as ex:
            bucket["units_the_rule_could_not_read"] += 1
            out_units.append({"unit": w["unit"], "lang": lang, "display": w.get("cell_display"),
                              "refusal": "%s: %s" % (type(ex).__name__, ex)})
            continue
        params = []
        for i, name in enumerate(ARGUMENT_NAMES[:len(declared)]):
            verdict, cause = compare(found.get(name), declared[i])
            params.append({"name": name, "discovered": found.get(name),
                           "declared": declared[i], "verdict": verdict, "cause": cause})
            bucket["parameters"] += 1
            bucket["parameter_" + verdict] += 1
            if cause:
                bucket["parameter_causes"][cause] = bucket["parameter_causes"].get(cause, 0) + 1
        if any(k and k[0] == "ieee" for k in found.values()):
            bucket["units_with_an_ieee_edge"] += 1
        result_found = found.get("result")
        verdict, cause = compare(result_found, declared_result)
        if detail.get("constant_meaning") and declared_result is not None:
            verdict, cause = UNDETERMINED, CAUSE_CONSTANT
        bucket["results"] += 1
        bucket["result_" + verdict] += 1
        if cause:
            bucket["result_causes"][cause] = bucket["result_causes"].get(cause, 0) + 1
        out_units.append({"unit": w["unit"], "lang": lang, "display": w.get("cell_display"),
                          "meaning": w["proposal"], "expanded": detail.get("expanded"),
                          "parameters": params,
                          "result": {"discovered": result_found, "declared": declared_result,
                                     "verdict": verdict, "cause": cause}})
    doc = {"meta": {"what": "LeanExpr.kinds: the primitive kind of every parameter and result "
                            "DISCOVERED from the arch-unit's Lean expression alone, by rules over "
                            "the expression's edges; compared against the manifest's declared holders",
                    "units_json": units_json, "walk_json": walk_jsons, "lean_dir": lean_dir,
                    "pure_forms": len(forms.forms),
                    "sail_functions_taking_a_rounding_mode": len(forms.float_heads),
                    "cause_text": CAUSE_TEXT},
           "units": out_units, "languages": tally}
    write_json(out_json, doc)
    for lang in sorted(tally):
        t = tally[lang]
        say("  %-5s units %4d (meaning %4d); parameters %4d: agree %4d, disagree %4d, undetermined %4d"
            % (lang, t["units"], t["units_with_a_meaning"], t["parameters"],
               t["parameter_agree"], t["parameter_disagree"], t["parameter_undetermined"]))
    return 0


def blank_tally():
    return {"units": 0, "units_with_a_meaning": 0, "units_without_a_meaning": 0,
            "units_the_rule_could_not_read": 0, "units_with_an_ieee_edge": 0,
            "parameters": 0, "parameter_agree": 0, "parameter_disagree": 0,
            "parameter_undetermined": 0, "parameter_causes": {},
            "results": 0, "result_agree": 0, "result_disagree": 0,
            "result_undetermined": 0, "result_causes": {}}
