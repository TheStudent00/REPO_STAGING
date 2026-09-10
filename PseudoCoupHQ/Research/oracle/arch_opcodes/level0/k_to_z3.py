#!/usr/bin/env python3
"""k_to_z3.py -- read ONE rule of the K-framework x86-64 semantics and leave
a z3 term in every place that rule writes.

WHAT THIS IS, in relation.  The K-framework x86-64 semantics (Dasgupta et
al., PLDI 2019) is a second reading of the same hardware our
`Research/op_pipeline/reference.py` reads: one file per instruction variant
(`addl_r32_r32.k`), each a K rule whose `<regstate>` update is a closed
expression saying what the instruction leaves in the destination register and
in each flag.  This program is the GRAMMAR over that expression language --
a lexer, a recursive-descent parser, and an evaluator into z3 -- so a rule
becomes the same kind of object our reference's builder leaves behind: one z3
term per written place.  It is written once over the ~30 functions the rule
language uses and never per file.  A function it does not know is REFUSED BY
CAUSE and counted; nothing is guessed.

WHERE THE SOURCE IS.  The rule files are read from `/sources/X86-64-semantics`
inside an Airlock lane (`Sources/X86-64-semantics` on the host),
under the University of Illinois/NCSA Open Source License
(`/sources/X86-64-semantics/LICENSE.md`).  Nothing from that tree is copied
into this repository: this file holds the grammar, not their text.

THE BIT-INDEX CONVENTION, stated before anything is compared.
    K's MInt indexes bits FROM THE MOST SIGNIFICANT END, and the range is
    half-open: `extractMInt(v, i, j)` of an n-bit v is the bits at
    most-significant positions i .. j-1, which in z3's least-significant
    numbering is `Extract(n - 1 - i, n - j, v)`.
  THE WORKED EXAMPLE, `addl_r32_r32`, their own text (LITERAL, one fragment,
  theirs):
      "CF" |-> extractMInt( addMInt( concatenateMInt( mi(1, 0),
               extractMInt( getParentValue(R1, RSMap), 32, 64)),
               concatenateMInt( mi(1, 0), extractMInt( getParentValue(R2,
               RSMap), 32, 64))), 0, 1)
  GLOSS, values in motion, with R1 = %esi = 0xFFFFFFFF and R2 = %edi = 1:
      extractMInt(getParentValue(R1), 32, 64)   the LOW 32 bits of the
                                                64-bit %rsi -> 0xFFFFFFFF
      concatenateMInt(mi(1,0), that)            a 33-bit 0x0FFFFFFFF
      the same for R2                           a 33-bit 0x000000001
      addMInt of the two                        0x100000000, 33 bits
      extractMInt(sum, 0, 1)                    position 0 counted from the
                                                MOST significant end of 33
                                                bits = the top bit = 1
      so CF = 1                                 the carry out, which is what
                                                the machine leaves
      and the destination is extractMInt(sum, 1, 33) = the low 32 bits = 0.
  THE SAME CONVENTION CHECKED A SECOND WAY, from their own `notl_r32`:
  `notl R1` writes `negMInt(extractMInt(getParentValue(R1), 32, 64))`, so
  `negMInt` is the BITWISE COMPLEMENT, and `negl R1` writes
  `addMInt(mi(32,1), negMInt(...))`, the two's complement.  Both readings
  agree only under the most-significant-first convention above.

WHAT UNDEFINED MEANS HERE.  Intel's manual leaves some flags undefined after
some instructions, and the rule files write `undefMInt` / `undefBool` there.
This program gives each occurrence A FRESH FREE SYMBOL, which is what
"undefined" is: unconstrained.  A place is then wholly undefined when its
term changes with that symbol on every input, and PARTIALLY undefined -- the
shifts, whose flags are undefined only when the count is out of range -- when
it changes with it on some inputs.  `undefined_region(term)` returns the
condition under which the place depends on a free undefined symbol, so a
comparison can be asked on the region where BOTH readings are defined and the
undefined region can be reported as itself.

usage:
    python3 k_to_z3.py <a .k file> [<a .k file> ...]
        parse each and print the places it writes with their z3 terms.
    python3 k_to_z3.py --vocabulary <folder>
        walk every .k file under the folder and print the function
        vocabulary with the ones this grammar does not know.
"""

import os
import re
import sys

import z3


# ==================================================================
# section 0: the refusal, and the sorts a K expression evaluates to
# ==================================================================


class Refused(Exception):
    """the parser could not read something, BY CAUSE.  `cause` is the
    short machine-form reason a report groups on; `detail` is the
    sentence a reader needs."""

    def __init__(self, cause, detail):
        Exception.__init__(self, "%s: %s" % (cause, detail))
        self.cause = cause
        self.detail = detail


UNDEF_PREFIX = "kundef_"
"""every free symbol this program makes for an `undefMInt` / `undefBool`
carries this prefix, so `undefined_region` can find them by nothing but
their names."""


class Val(object):
    """one evaluated K expression: a z3 term plus which K sort it came
    back as.

    kind is one of:
      "mint" -- a bit vector of `width` bits, K's MInt.
      "bool" -- a z3 Bool, K's Bool.
      "int"  -- K's unbounded Int, held here as a bit vector together
                with whether it was read signed; `as_mint` resizes it
                the way `mi(w, <an Int>)` does.
    """

    def __init__(self, kind, term, width=None, signed=False):
        self.kind = kind
        self.term = term
        self.width = width
        self.signed = signed

    def __repr__(self):
        return "Val(%s, %s)" % (self.kind, self.term)


def bool_of(value):
    if value.kind != "bool":
        raise Refused("a Bool was expected",
                      "the expression came back as the K sort %r"
                      % value.kind)
    return value.term


def mint_of(value):
    if value.kind != "mint":
        raise Refused("an MInt was expected",
                      "the expression came back as the K sort %r"
                      % value.kind)
    return value.term


def resize(term, width, signed):
    """the one resizing rule, used wherever K turns an Int into an MInt
    of a stated width: widen by sign or zero, narrow by taking the low
    bits, which is `mi(w, v)`'s own `v mod 2^w`."""
    have = term.size()
    if have == width:
        return term
    if have < width:
        if signed:
            return z3.SignExt(width - have, term)
        return z3.ZeroExt(width - have, term)
    return z3.Extract(width - 1, 0, term)


# ==================================================================
# section 1: the lexer
# ==================================================================


TOKEN_RE = re.compile(r"""
    (?P<space>\s+)
  | (?P<comment>//[^\n]*)
  | (?P<blockcomment>/\*.*?\*/)
  | (?P<string>"[^"]*")
  | (?P<arrow>\|->)
  | (?P<rewrite>=>)
  | (?P<eqbool>==Bool)
  | (?P<nebool>=/=Bool)
  | (?P<reg>%[A-Za-z0-9()]+)
  | (?P<hex>\$?0x[0-9a-fA-F]+)
  | (?P<number>-?\d+)
  | (?P<name>[#A-Za-z_][A-Za-z0-9_.]*)
  | (?P<punct>[(),:.<>])
  | (?P<other>.)
""", re.X | re.S)


class Token(object):
    def __init__(self, kind, text, position):
        self.kind = kind
        self.text = text
        self.position = position

    def __repr__(self):
        return "Token(%s, %r)" % (self.kind, self.text)


def tokenize(text):
    """every token of one rule file, in order.  Whitespace and comments
    are dropped; everything else keeps its text."""
    out = []
    at = 0
    end = len(text)
    while at < end:
        match = TOKEN_RE.match(text, at)
        if match is None:
            raise Refused("a character the lexer does not read",
                          "at offset %d: %r" % (at, text[at:at + 30]))
        at = match.end()
        kind = match.lastgroup
        if kind in ("space", "comment", "blockcomment"):
            continue
        out.append(Token(kind, match.group(), match.start()))
    return out


# ==================================================================
# section 2: the rule -- what one file says
# ==================================================================


SIZE_SORTS = {"R8": 8, "Rh": 8, "R16": 16, "R32": 32, "R64": 64,
              "Xmm": 128, "Ymm": 256}
"""the sort annotation a rule head puts on an operand variable, and the
width of the operand it stands for.  `Rh` is a high byte (%ah)."""

MEMORY_SORTS = frozenset(["Mem", "MemOffset", "MemLoadValue"])
"""the sorts a rule head puts on a MEMORY operand.  A memory variant's
head spells it `HOLE:Mem` on the `context` line and
`memOffset( MemOff:MInt):MemOffset` on the rule itself; both mean one
memory operand at the width the rule's own `loadFromMemory` /
`storeToMemory` states."""

KIND_OF_SORT = {"R8": "gpr", "R16": "gpr", "R32": "gpr", "R64": "gpr",
                "Rh": "high", "Xmm": "xmm", "Ymm": "ymm",
                "Imm": "imm"}
"""the operand KIND a head sort names, which is what an operand shape is
built out of.  A sort this table lacks makes the head unreadable, by
cause, rather than guessed at."""

THE_ORDER = ("the arch text's own order, source first and destination "
             "last, which is the order the rule HEAD spells -- their "
             "file NAME spells the reverse")


class Rule(object):
    """one instruction variant as this grammar reads it.

    mnem            the mnemonic the rule head spells, their spelling
                    (`addl`), kept in a field named `mnem`.
    operands        the rule head's operand list, in the arch text's own
                    order (AT&T: source first, destination last), each a
                    dict {"var", "sort", "width"} for a variable, or
                    {"literal"} for a register the head names outright
                    (`%cl`, `%rcx`).
    writes          place -> the parsed expression tree, in file order.
                    A place is either {"kind": "register", "var": ...}
                    for `convToRegKeys(R2)` or {"kind": "flag",
                    "name": "CF"} for a quoted flag key.
    """

    def __init__(self, mnem, operands, writes, path):
        self.mnem = mnem
        self.operands = operands
        self.writes = writes
        self.path = path
        self.immediate_widths = {}
        self.memory_width = None
        self.memory_values = {}


class Parser(object):
    """recursive descent over the token list of one rule file."""

    def __init__(self, tokens, path):
        self.tokens = tokens
        self.at = 0
        self.path = path

    # -- the token stream ------------------------------------------

    def peek(self, ahead=0):
        index = self.at + ahead
        if index >= len(self.tokens):
            return None
        return self.tokens[index]

    def next(self):
        token = self.peek()
        if token is None:
            raise Refused("the file ended inside an expression",
                          "in %s" % os.path.basename(self.path))
        self.at = self.at + 1
        return token

    def accept(self, kind, text=None):
        token = self.peek()
        if token is None:
            return None
        if token.kind != kind:
            return None
        if text is not None and token.text != text:
            return None
        return self.next()

    def expect(self, kind, text=None):
        token = self.accept(kind, text)
        if token is None:
            have = self.peek()
            raise Refused("the rule language has a shape this grammar "
                          "does not read",
                          "expected %s%s, found %r in %s"
                          % (kind, "" if text is None else " %r" % text,
                             None if have is None else have.text,
                             os.path.basename(self.path)))
        return token

    # -- the file --------------------------------------------------

    def parse_head(self):
        """`<mnem> <operands>, .Operands` -- the tokens between the
        parentheses of one `execinstr (...)`."""
        mnem_token = self.expect("name")
        mnem = mnem_token.text
        if self.accept("punct", ":") is not None:
            self.expect("name")          # `xorb:Opcode`, the Opcode sort
        operands = []
        while True:
            token = self.peek()
            if token is None:
                raise Refused("the rule head did not close",
                              "in %s" % os.path.basename(self.path))
            if token.kind == "punct" and token.text == ")":
                self.next()
                break
            if token.kind == "punct" and token.text == ",":
                self.next()
                continue
            if token.kind == "punct" and token.text == ".":
                self.next()
                self.expect("name")      # `.Operands`
                continue
            if token.kind == "reg":
                self.next()
                kind = "cl" if token.text == "%cl" else "register"
                operands.append({"literal": token.text, "kind": kind,
                                 "width": 8 if kind == "cl" else None})
                continue
            if token.kind == "name":
                self.next()
                if token.text == "memOffset":
                    # `memOffset( MemOff:MInt):MemOffset` -- one memory
                    # operand, written the long way on the rule itself.
                    self.expect("punct", "(")
                    depth = 1
                    while depth > 0:
                        inner = self.next()
                        if inner.kind == "punct" and inner.text == "(":
                            depth = depth + 1
                        elif inner.kind == "punct" and \
                                inner.text == ")":
                            depth = depth - 1
                    if self.accept("punct", ":") is not None:
                        self.expect("name")
                    operands.append({"var": None, "sort": "MemOffset",
                                     "kind": "mem", "width": None})
                    continue
                sort = None
                if self.accept("punct", ":") is not None:
                    sort = self.expect("name").text
                if sort is None:
                    raise Refused("an operand with no sort",
                                  "the head names %r with no `:Sort` in "
                                  "%s" % (token.text,
                                          os.path.basename(self.path)))
                if sort == "Opcode":
                    continue
                if sort in MEMORY_SORTS:
                    operands.append({"var": token.text, "sort": sort,
                                     "kind": "mem", "width": None})
                    continue
                kind = KIND_OF_SORT.get(sort)
                if kind is None:
                    raise Refused(
                        "an operand sort this grammar does not read",
                        "the head names %s:%s in %s"
                        % (token.text, sort,
                           os.path.basename(self.path)))
                operands.append({"var": token.text, "sort": sort,
                                 "kind": kind,
                                 "width": SIZE_SORTS.get(sort)})
                continue
            raise Refused("an operand shape this grammar does not read",
                          "the head carries %r in %s"
                          % (token.text, os.path.basename(self.path)))
        return mnem, operands

    def parse_regstate(self):
        """`RSMap:Map => updateMap(RSMap, <assignments>)` -- the tokens
        inside one `<regstate>` cell."""
        self.expect("name", "RSMap")
        self.expect("punct", ":")
        self.expect("name", "Map")
        self.expect("rewrite")
        self.expect("name", "updateMap")
        self.expect("punct", "(")
        self.expect("name", "RSMap")
        self.expect("punct", ",")
        writes = []
        while True:
            token = self.peek()
            if token is None:
                raise Refused("the regstate update did not close",
                              os.path.basename(self.path))
            if token.kind == "punct" and token.text == ")":
                self.next()
                break
            if token.kind == "punct" and token.text == ",":
                self.next()
                continue
            place = self.parse_place()
            self.expect("arrow")
            expression = self.parse_expression()
            writes.append((place, expression))
        return writes

    def parse_place(self):
        token = self.peek()
        if token is not None and token.kind == "string":
            self.next()
            return {"kind": "flag", "name": token.text.strip('"')}
        if token is not None and token.kind == "name" and \
                token.text == "convToRegKeys":
            self.next()
            self.expect("punct", "(")
            inner = self.next()
            if inner.kind == "reg":
                place = {"kind": "register", "literal": inner.text}
            elif inner.kind == "name":
                place = {"kind": "register", "var": inner.text}
            else:
                raise Refused("a written place this grammar does not "
                              "read",
                              "convToRegKeys(%r) in %s"
                              % (inner.text,
                                 os.path.basename(self.path)))
            self.expect("punct", ")")
            return place
        raise Refused("a written place this grammar does not read",
                      "the left of `|->` is %r in %s"
                      % (None if token is None else token.text,
                         os.path.basename(self.path)))

    # -- the expression grammar ------------------------------------
    #
    # One production per level, loosest binding first, which is the
    # order the rule files themselves parenthesise:
    #
    #   expression  ::= or_expression
    #   or_expression   ::= and_expression ( "orBool" and_expression )*
    #   and_expression  ::= eq_expression ( "andBool" eq_expression )*
    #   eq_expression   ::= xor_expression
    #                       ( ("==Bool" | "=/=Bool") xor_expression )*
    #   xor_expression  ::= unary ( "xorBool" unary )*
    #   unary       ::= "notBool" unary | primary
    #   primary     ::= "(" expression ")"
    #                 | "#ifMInt" expression "#then" expression
    #                   "#else" expression "#fi"
    #                 | name "(" arguments ")"
    #                 | name | register | number | string

    def parse_expression(self):
        return self.parse_or()

    def parse_or(self):
        left = self.parse_and()
        while True:
            token = self.peek()
            if token is None or token.kind != "name" or \
                    token.text != "orBool":
                return left
            self.next()
            right = self.parse_and()
            left = ("orBool", left, right)

    def parse_and(self):
        left = self.parse_eq()
        while True:
            token = self.peek()
            if token is None or token.kind != "name" or \
                    token.text != "andBool":
                return left
            self.next()
            right = self.parse_eq()
            left = ("andBool", left, right)

    def parse_eq(self):
        left = self.parse_xor()
        while True:
            token = self.peek()
            if token is None:
                return left
            if token.kind == "eqbool":
                self.next()
                left = ("==Bool", left, self.parse_xor())
                continue
            if token.kind == "nebool":
                self.next()
                left = ("=/=Bool", left, self.parse_xor())
                continue
            return left

    def parse_xor(self):
        left = self.parse_unary()
        while True:
            token = self.peek()
            if token is None or token.kind != "name" or \
                    token.text != "xorBool":
                return left
            self.next()
            right = self.parse_unary()
            left = ("xorBool", left, right)

    def parse_unary(self):
        token = self.peek()
        if token is not None and token.kind == "name" and \
                token.text == "notBool":
            self.next()
            return ("notBool", self.parse_unary())
        return self.parse_primary()

    def parse_primary(self):
        token = self.next()
        if token.kind == "punct" and token.text == "(":
            inner = self.parse_expression()
            self.expect("punct", ")")
            return inner
        if token.kind == "name" and token.text == "#ifMInt":
            condition = self.parse_expression()
            self.expect("name", "#then")
            taken = self.parse_expression()
            self.expect("name", "#else")
            otherwise = self.parse_expression()
            self.expect("name", "#fi")
            return ("#ifMInt", condition, taken, otherwise)
        if token.kind == "name" and token.text == "#ifBool":
            condition = self.parse_expression()
            self.expect("name", "#then")
            taken = self.parse_expression()
            self.expect("name", "#else")
            otherwise = self.parse_expression()
            self.expect("name", "#fi")
            return ("#ifMInt", condition, taken, otherwise)
        if token.kind == "reg":
            return ("register", token.text)
        if token.kind == "number":
            return ("number", int(token.text))
        if token.kind == "hex":
            return ("number", int(token.text.lstrip("$"), 16))
        if token.kind == "string":
            return ("string", token.text.strip('"'))
        if token.kind == "name":
            nxt = self.peek()
            if nxt is not None and nxt.kind == "punct" and \
                    nxt.text == "(":
                self.next()
                arguments = []
                if self.accept("punct", ")") is None:
                    while True:
                        arguments.append(self.parse_expression())
                        if self.accept("punct", ",") is not None:
                            continue
                        self.expect("punct", ")")
                        break
                return ("apply", token.text, arguments)
            return ("name", token.text)
        raise Refused("the rule language has a shape this grammar does "
                      "not read",
                      "the token %r in %s"
                      % (token.text, os.path.basename(self.path)))


EXECINSTR_RE = re.compile(r"\bexecinstr\s*\(")
REGSTATE_RE = re.compile(r"<regstate>(.*?)</regstate>", re.S)
OTHER_CELL_RE = re.compile(
    r"<(memory|sigsegv|sigfpe|sigbus|objects|nextLoc|freed|functargets"
    r"|mem|currModule)>")


def balanced_slice(text, open_at):
    """the text between `text[open_at]`, which must be an open paren,
    and its matching close paren."""
    depth = 0
    index = open_at
    while index < len(text):
        character = text[index]
        if character == "(":
            depth = depth + 1
        elif character == ")":
            depth = depth - 1
            if depth == 0:
                return text[open_at + 1:index]
        index = index + 1
    raise Refused("a parenthesis that never closes",
                  "from offset %d" % open_at)


IMMEDIATE_WIDTH_RE = re.compile(
    r"handleImmediateWithSignExtend\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*,"
    r"\s*(\d+)\s*,\s*(\d+)\s*\)")
LOAD_WIDTH_RE = re.compile(r"loadFromMemory\(\s*\w+\s*,\s*(\d+)\s*\)")
STORE_WIDTH_RE = re.compile(r",\s*MemOff\s*,\s*(\d+)\s*\)")
MEM_VALUE_RE = re.compile(r"\b(Mem(\d+))\s*:\s*MInt")


def slice_file(text, path):
    """the two slices this grammar reads: the operand list inside the
    FIRST `execinstr (...)` head, and the ONE `<regstate>` cell that
    carries an `updateMap`.

    Slicing rather than walking the whole file keeps K's module headers
    (`module ADDL-R32-R32`), its `requires` lines and its `<k>` cell out
    of the expression grammar entirely.

    A MEMORY VARIANT STATES THREE THINGS and only one of them updates
    the register state: a `context` line, a first rule that turns the
    memory operand into a `loadFromMemory`, and a second rule that
    computes.  Only the second carries `updateMap`, and the others
    carry a bare `<regstate> RSMap:Map </regstate>` pass-through, so
    taking the one cell WITH an update is what reads a memory variant
    at all.  A file with more than one such cell is refused by cause:
    which of two updates fires is decided by a side condition this
    grammar does not read.
    """
    heads = list(EXECINSTR_RE.finditer(text))
    if not heads:
        raise Refused("no execinstr head",
                      "%s states no `execinstr (...)` rule"
                      % os.path.basename(path))
    cells = [cell for cell in REGSTATE_RE.findall(text)
             if "updateMap" in cell]
    if not cells:
        other = OTHER_CELL_RE.search(text)
        if other is not None:
            raise Refused(
                "the rule updates a cell this grammar does not read",
                "%s updates <%s>, which is memory or a signal, not the "
                "register state"
                % (os.path.basename(path), other.group(1)))
        raise Refused("no regstate update",
                      "%s states no `<regstate>` update, so it writes "
                      "no register and no flag"
                      % os.path.basename(path))
    if len(cells) > 1:
        raise Refused(
            "the file states more than one register-state update",
            "%s carries %d, so which one fires is decided by a side "
            "condition this grammar does not read"
            % (os.path.basename(path), len(cells)))
    head = balanced_slice(text, heads[0].end() - 1)
    return head, cells[0]


def widths_of(text):
    """the widths a rule states for its own immediate and memory
    operands, from the rule's own text: `handleImmediateWithSignExtend`
    says the immediate's own width and the width it is extended to,
    `loadFromMemory` / `storeToMemory` say the memory operand's width,
    and a loaded value arrives as the variable `Mem<width>`."""
    immediates = {}
    for match in IMMEDIATE_WIDTH_RE.finditer(text):
        immediates[match.group(1)] = (int(match.group(2)),
                                      int(match.group(3)))
    memory = None
    match = LOAD_WIDTH_RE.search(text)
    if match is not None:
        memory = int(match.group(1))
    if memory is None:
        match = STORE_WIDTH_RE.search(text)
        if match is not None:
            memory = int(match.group(1))
    values = {}
    for match in MEM_VALUE_RE.finditer(text):
        values[match.group(1)] = int(match.group(2))
        if memory is None:
            memory = int(match.group(2))
    return immediates, memory, values


def parse_file(path):
    text = open(path).read()
    head_text, cell_text = slice_file(text, path)
    head = Parser(tokenize(head_text) + [Token("punct", ")", 0)],
                  path).parse_head()
    writes = Parser(tokenize(cell_text), path).parse_regstate()
    rule = Rule(head[0], head[1], writes, path)
    rule.immediate_widths, rule.memory_width, rule.memory_values = \
        widths_of(text)
    for operand in rule.operands:
        if operand.get("kind") == "imm":
            pair = rule.immediate_widths.get(operand.get("var"))
            if pair is not None:
                operand["width"] = pair[0]
                operand["extended_to"] = pair[1]
        elif operand.get("kind") == "mem":
            operand["width"] = rule.memory_width
    return rule


# ==================================================================
# section 3: the evaluator -- one K expression into one z3 term
# ==================================================================
#
# THE FUNCTION VOCABULARY, and each function's meaning, taken from the
# third-party source's own definitions (`x86-mint-wrapper.k`,
# `x86-abstract-semantics.k`) rather than guessed:
#
#   mi(w, v)                 the w-bit MInt whose value is v mod 2^w
#   extractMInt(v, i, j)     bits i .. j-1 counted from the MOST
#                            significant end, half open
#   concatenateMInt(a, b)    a in the high bits, b in the low
#   addMInt subMInt mulMInt  bit-vector + - * at one width
#   negMInt                  the BITWISE complement (their `notl` rule
#                            writes exactly negMInt, and their `negl`
#                            writes addMInt(mi(w,1), negMInt(...)))
#   andMInt orMInt xorMInt   bitwise & | ^
#   shiftLeftMInt(v, n)      << at v's own width
#   lshrMInt(v, n)           logical >> at v's own width
#   aShiftRightMInt(v, n)    arithmetic >> at v's own width
#   uremMInt(a, b)           unsigned remainder
#   eqMInt(a, b)             a == b, a Bool
#   ultMInt ugtMInt ugeMInt uleMInt   unsigned <, >, >=, <=
#   sltMInt sgtMInt          signed <, >
#   svalueMInt(v)            v read as a signed K Int
#   uvalueMInt(v)            v read as an unsigned K Int
#   bitwidthMInt(v)          v's width, a K Int
#   signExtend(v, n)         v sign-extended to n bits
#   #ifMInt c #then a #else b #fi        the conditional
#   andBool orBool notBool xorBool ==Bool =/=Bool
#   undefMInt undefBool      Intel's "undefined": a FRESH FREE SYMBOL
#   getParentValue(R, RSMap) the whole 64-bit register the operand
#                            belongs to
#   getFlag(F, RSMap)        the 1-bit flag F as it stood before
#   handleImmediateWithSignExtend(I, m, n)
#                            the immediate as an m-bit MInt, sign
#                            extended to n bits (their own rule)
#   shiftCountMask(v, n)     v & 0x3F when n is 64, else v & 0x1F


ARITHMETIC = {
    "addMInt": lambda a, b: a + b,
    "subMInt": lambda a, b: a - b,
    "mulMInt": lambda a, b: a * b,
    "andMInt": lambda a, b: a & b,
    "orMInt": lambda a, b: a | b,
    "xorMInt": lambda a, b: a ^ b,
}

COMPARISON = {
    "eqMInt": lambda a, b: a == b,
    "ultMInt": z3.ULT,
    "ugtMInt": z3.UGT,
    "ugeMInt": z3.UGE,
    "uleMInt": z3.ULE,
    "sltMInt": lambda a, b: a < b,
    "sgtMInt": lambda a, b: a > b,
    "sleMInt": lambda a, b: a <= b,
    "sgeMInt": lambda a, b: a >= b,
}

SHIFT = {
    "shiftLeftMInt": lambda a, n: a << n,
    "lshrMInt": z3.LShR,
    "aShiftRightMInt": lambda a, n: a >> n,
}

GRAMMAR_FORMS = frozenset(
    ["#ifMInt", "#ifBool", "#then", "#else", "#fi", "notBool",
     "andBool", "orBool", "xorBool", "==Bool", "=/=Bool", "updateMap",
     "convToRegKeys"])
"""the names the PARSER reads as forms of the rule language rather than
as functions to evaluate: the conditional's three keywords, the boolean
connectives, the map update the whole `<regstate>` rewrite is, and the
place spelling on the left of `|->`."""

KNOWN_FUNCTIONS = frozenset(
    list(ARITHMETIC) + list(COMPARISON) + list(SHIFT) +
    list(GRAMMAR_FORMS) +
    ["mi", "extractMInt", "concatenateMInt", "negMInt", "uremMInt",
     "sremMInt", "udivMInt", "sdivMInt", "svalueMInt", "uvalueMInt",
     "bitwidthMInt", "signExtend", "zeroExtend", "getParentValue",
     "getFlag", "getRegisterValue", "shiftCountMask",
     "handleImmediateWithSignExtend", "getSignBit", "getBitFromMInt"])


class Environment(object):
    """what the rule's free names stand for, in ONE comparison.

    register_of  a rule-head operand variable name, or a register the
                 head names outright, -> the 64-bit z3 symbol standing
                 for the whole register.  Both readings are given the
                 SAME symbol, so nothing has to be renamed afterwards.
    immediate_of a rule-head immediate variable name -> the z3 bit
                 vector standing for the immediate, at the width their
                 own `handleImmediateWithSignExtend` states.
    flag_of      a flag name ("CF") -> the 1-bit z3 term standing for
                 that flag as it stood before the instruction.
    """

    def __init__(self, register_of=None, immediate_of=None,
                 flag_of=None):
        self.register_of = register_of or {}
        self.immediate_of = immediate_of or {}
        self.flag_of = flag_of or {}
        self.undefined = []

    def fresh_undefined(self, kind, width=None):
        name = "%s%d" % (UNDEF_PREFIX, len(self.undefined))
        if kind == "bool":
            term = z3.Bool(name)
            value = Val("bool", term)
        else:
            term = z3.BitVec(name, width or 1)
            value = Val("mint", term, width or 1)
        self.undefined.append(term)
        return value


def evaluate(node, env):
    """one parsed K expression into one `Val`."""
    head = node[0]

    if head == "number":
        return Val("int", z3.BitVecVal(node[1], 65), 65, signed=True)

    if head == "string":
        raise Refused("a string in an expression position",
                      "the grammar reads a string only as a flag key")

    if head == "register":
        term = env.register_of.get(node[1])
        if term is None:
            raise Refused("a register the comparison did not bind",
                          "the rule reads %s, which the operand "
                          "binding does not name" % node[1])
        return Val("mint", term, term.size())

    if head == "name":
        name = node[1]
        if name == "undefMInt":
            return env.fresh_undefined("mint", 1)
        if name in ("undefMInt8", "undefMInt16", "undefMInt32",
                    "undefMInt64"):
            return env.fresh_undefined("mint", int(name[9:]))
        if name == "undefBool":
            return env.fresh_undefined("bool")
        if name == "RSMap":
            return Val("map", None)
        if name == "true":
            return Val("bool", z3.BoolVal(True))
        if name == "false":
            return Val("bool", z3.BoolVal(False))
        term = env.register_of.get(name)
        if term is not None:
            return Val("mint", term, term.size())
        term = env.immediate_of.get(name)
        if term is not None:
            return Val("mint", term, term.size())
        raise Refused("a bare name this grammar does not know",
                      "the rule reads %r" % name)

    if head in ("andBool", "orBool", "xorBool", "==Bool", "=/=Bool"):
        left = evaluate(node[1], env)
        right = evaluate(node[2], env)
        if head == "andBool":
            return Val("bool", z3.And(bool_of(left), bool_of(right)))
        if head == "orBool":
            return Val("bool", z3.Or(bool_of(left), bool_of(right)))
        if head == "xorBool":
            return Val("bool", z3.Xor(bool_of(left), bool_of(right)))
        if head == "==Bool":
            return Val("bool", bool_of(left) == bool_of(right))
        return Val("bool", z3.Not(bool_of(left) == bool_of(right)))

    if head == "notBool":
        return Val("bool", z3.Not(bool_of(evaluate(node[1], env))))

    if head == "#ifMInt":
        condition = bool_of(evaluate(node[1], env))
        taken = evaluate(node[2], env)
        otherwise = evaluate(node[3], env)
        if taken.kind == "bool" and otherwise.kind == "bool":
            return Val("bool", z3.If(condition, taken.term,
                                     otherwise.term))
        left = mint_of(taken)
        right = mint_of(otherwise)
        if left.size() != right.size():
            raise Refused("a conditional over two widths",
                          "the two sides are %d and %d bits"
                          % (left.size(), right.size()))
        return Val("mint", z3.If(condition, left, right), left.size())

    if head != "apply":
        raise Refused("an expression node this grammar does not read",
                      "the node head is %r" % head)

    name = node[1]
    arguments = node[2]
    return apply_function(name, arguments, env)


def apply_function(name, arguments, env):
    if name == "mi":
        width = literal_int(arguments[0], env)
        value = evaluate(arguments[1], env)
        if value.kind == "int":
            return Val("mint", resize(value.term, width, value.signed),
                       width)
        if value.kind == "mint":
            return Val("mint", resize(value.term, width, False), width)
        raise Refused("mi over a sort this grammar does not resize",
                      "mi(%d, <%s>)" % (width, value.kind))

    if name == "extractMInt":
        value = evaluate(arguments[0], env)
        term = mint_of(value)
        low_index = literal_int(arguments[1], env)
        high_index = literal_int(arguments[2], env)
        size = term.size()
        if not 0 <= low_index < high_index <= size:
            raise Refused(
                "an extract outside the value",
                "extractMInt(<%d bits>, %d, %d)"
                % (size, low_index, high_index))
        # MOST-SIGNIFICANT-FIRST, half open: positions low_index ..
        # high_index-1 counted from the top become z3's
        # Extract(size-1-low_index, size-high_index, term).
        return Val("mint",
                   z3.Extract(size - 1 - low_index, size - high_index,
                              term),
                   high_index - low_index)

    if name == "concatenateMInt":
        high = mint_of(evaluate(arguments[0], env))
        low = mint_of(evaluate(arguments[1], env))
        return Val("mint", z3.Concat(high, low),
                   high.size() + low.size())

    if name == "negMInt":
        # THEIR OWN `notl` RULE IS THE DEFINITION: `notl R1` writes
        # negMInt(<the operand>), so this is the bitwise complement,
        # and `negl` writes addMInt(mi(w,1), negMInt(...)).
        value = mint_of(evaluate(arguments[0], env))
        return Val("mint", ~value, value.size())

    if name in ARITHMETIC:
        left = mint_of(evaluate(arguments[0], env))
        right = mint_of(evaluate(arguments[1], env))
        if left.size() != right.size():
            raise Refused("an arithmetic over two widths",
                          "%s(<%d bits>, <%d bits>)"
                          % (name, left.size(), right.size()))
        return Val("mint", ARITHMETIC[name](left, right), left.size())

    if name in COMPARISON:
        left = mint_of(evaluate(arguments[0], env))
        right = mint_of(evaluate(arguments[1], env))
        if left.size() != right.size():
            raise Refused("a comparison over two widths",
                          "%s(<%d bits>, <%d bits>)"
                          % (name, left.size(), right.size()))
        return Val("bool", COMPARISON[name](left, right))

    if name in SHIFT:
        value = mint_of(evaluate(arguments[0], env))
        count = evaluate(arguments[1], env)
        if count.kind == "int":
            amount = resize(count.term, value.size(), False)
        else:
            amount = resize(mint_of(count), value.size(), False)
        return Val("mint", SHIFT[name](value, amount), value.size())

    if name in ("uremMInt", "sremMInt", "udivMInt", "sdivMInt"):
        left = mint_of(evaluate(arguments[0], env))
        right = mint_of(evaluate(arguments[1], env))
        if left.size() != right.size():
            raise Refused("a division over two widths",
                          "%s(<%d bits>, <%d bits>)"
                          % (name, left.size(), right.size()))
        table = {"uremMInt": z3.URem, "sremMInt": z3.SRem,
                 "udivMInt": z3.UDiv, "sdivMInt": lambda a, b: a / b}
        return Val("mint", table[name](left, right), left.size())

    if name == "svalueMInt":
        value = mint_of(evaluate(arguments[0], env))
        return Val("int", value, value.size(), signed=True)

    if name == "uvalueMInt":
        value = mint_of(evaluate(arguments[0], env))
        return Val("int", value, value.size(), signed=False)

    if name == "bitwidthMInt":
        value = mint_of(evaluate(arguments[0], env))
        return Val("int", z3.BitVecVal(value.size(), 65), 65,
                   signed=False)

    if name in ("signExtend", "zeroExtend"):
        value = mint_of(evaluate(arguments[0], env))
        width = literal_int(arguments[1], env)
        return Val("mint",
                   resize(value, width, name == "signExtend"), width)

    if name in ("getParentValue", "getRegisterValue"):
        target = arguments[0]
        key = None
        if target[0] == "register":
            key = target[1]
        elif target[0] == "name":
            key = target[1]
        if key is None:
            raise Refused("a register operand this grammar does not "
                          "read", "%s(%r, ...)" % (name, target))
        term = env.register_of.get(key)
        if term is None:
            raise Refused("a register the comparison did not bind",
                          "the rule reads %s, which the operand "
                          "binding does not name" % key)
        return Val("mint", term, term.size())

    if name == "getFlag":
        target = arguments[0]
        if target[0] != "string":
            raise Refused("a flag key this grammar does not read",
                          "getFlag(%r, ...)" % (target,))
        term = env.flag_of.get(target[1])
        if term is None:
            raise Refused(
                "the rule reads a flag the comparison did not bind",
                "getFlag(%r) -- this variant's mapping is a function "
                "of the flags a previous instruction left" % target[1])
        return Val("mint", term, term.size())

    if name == "handleImmediateWithSignExtend":
        target = arguments[0]
        if target[0] != "name":
            raise Refused("an immediate this grammar does not read",
                          "handleImmediateWithSignExtend(%r, ...)"
                          % (target,))
        own = literal_int(arguments[1], env)
        into = literal_int(arguments[2], env)
        term = env.immediate_of.get(target[1])
        if term is None:
            raise Refused("an immediate the comparison did not bind",
                          "the rule reads the immediate %s"
                          % target[1])
        # their own rule: signExtend(mi(own, I), into)
        narrow = resize(term, own, True)
        return Val("mint", resize(narrow, into, True), into)

    if name == "shiftCountMask":
        value = mint_of(evaluate(arguments[0], env))
        width = literal_int(arguments[1], env)
        mask = 0x3F if width == 64 else 0x1F
        return Val("mint", value & z3.BitVecVal(mask, value.size()),
                   value.size())

    if name == "getSignBit":
        value = mint_of(evaluate(arguments[0], env))
        top = value.size() - 1
        return Val("mint", z3.Extract(top, top, value), 1)

    if name == "getBitFromMInt":
        value = mint_of(evaluate(arguments[0], env))
        index = literal_int(arguments[1], env)
        return Val("mint", z3.Extract(index, index, value), 1)

    if name == "convToRegKeys":
        raise Refused("convToRegKeys in an expression position",
                      "this grammar reads it only as a written place")

    raise Refused("a function this grammar does not know",
                  "the rule applies %s/%d" % (name, len(arguments)))


def literal_int(node, env):
    """a K Int that must be a literal, because a width or a bit index
    cannot be symbolic."""
    if node[0] == "number":
        return node[1]
    value = evaluate(node, env)
    if value.kind == "int" and z3.is_bv_value(z3.simplify(value.term)):
        return z3.simplify(value.term).as_long()
    raise Refused("a width or a bit index that is not a literal",
                  "the rule computes it")


# ==================================================================
# section 4: what a place's undefined region is
# ==================================================================


def undefined_symbols(term):
    """every free symbol of a term whose name says it stands for one of
    Intel's undefined values."""
    out = {}
    seen = set()

    def walk(node):
        key = node.get_id()
        if key in seen:
            return
        seen.add(key)
        if node.num_args() == 0 and node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
            name = node.decl().name()
            if name.startswith(UNDEF_PREFIX):
                out[name] = node
            return
        for kid in node.children():
            walk(kid)

    walk(term)
    return [out[name] for name in sorted(out)]


def undefined_region(term):
    """the condition, over everything else the term reads, under which
    this place DEPENDS on an undefined value.

    Two copies of the term are made, one with every undefined symbol
    forced to zero (or false) and one with every undefined symbol
    forced to one (or true).  Where the two copies differ, the place is
    undefined; where they agree, the place is defined and the two
    copies are the same term, so either may be compared.

    Returns (the region as a z3 Bool, the term with the undefined
    symbols forced low).  A term with no undefined symbol comes back
    with the region `False` and itself.
    """
    symbols = undefined_symbols(term)
    if not symbols:
        return z3.BoolVal(False), term
    low = []
    high = []
    for symbol in symbols:
        if z3.is_bool(symbol):
            low.append((symbol, z3.BoolVal(False)))
            high.append((symbol, z3.BoolVal(True)))
        else:
            width = symbol.size()
            low.append((symbol, z3.BitVecVal(0, width)))
            high.append((symbol, z3.BitVecVal((1 << width) - 1, width)))
    forced_low = z3.substitute(term, *low)
    forced_high = z3.substitute(term, *high)
    if z3.is_bool(forced_low):
        region = z3.Xor(forced_low, forced_high)
    else:
        region = forced_low != forced_high
    return region, forced_low


# ==================================================================
# section 5: reading one rule with a stated binding
# ==================================================================


def places_of(rule, env):
    """every place the rule writes, as (place record, Val).  A place
    whose expression the grammar refuses carries the refusal instead of
    a value, so one unreadable flag does not lose the whole rule."""
    out = []
    for place, expression in rule.writes:
        try:
            value = evaluate(expression, env)
        except Refused as refusal:
            out.append((place, None, refusal))
            continue
        out.append((place, value, None))
    return out


# ==================================================================
# section 6: the command line
# ==================================================================


def vocabulary_of(folder):
    """every function name applied INSIDE a `<regstate>` cell of a rule
    file under the folder, with the ones this grammar does not know
    named.

    The scan is restricted to the regstate cells because that is the
    only text this grammar ever evaluates; counting the whole file would
    count K's own module machinery, the C-library models and the memory
    cells, none of which a register mapping reaches."""
    counts = {}
    files_by = {}
    unreadable = {}
    files = 0
    with_cell = 0
    for root, _dirs, names in os.walk(folder):
        for name in sorted(names):
            if not name.endswith(".k"):
                continue
            path = os.path.join(root, name)
            files = files + 1
            try:
                text = open(path).read()
            except (IOError, OSError) as problem:
                unreadable[str(problem)] = unreadable.get(
                    str(problem), 0) + 1
                continue
            cells = REGSTATE_RE.findall(text)
            if not cells:
                continue
            with_cell = with_cell + 1
            here = set()
            for cell in cells:
                for match in re.finditer(
                        r"([#A-Za-z_][A-Za-z0-9_]*)\s*\(", cell):
                    word = match.group(1)
                    counts[word] = counts.get(word, 0) + 1
                    here.add(word)
            for word in here:
                files_by[word] = files_by.get(word, 0) + 1
    return files, with_cell, counts, files_by, unreadable


def main(argv):
    if len(argv) > 2 and argv[1] == "--vocabulary":
        files, with_cell, counts, files_by, unreadable = \
            vocabulary_of(argv[2])
        print("%d .k files walked, %d of them carrying a regstate cell"
              % (files, with_cell))
        known = 0
        unknown = 0
        print("%9s %7s  %-34s %s"
              % ("uses", "files", "function", "this grammar"))
        for word in sorted(counts, key=lambda w: -counts[w]):
            if word in KNOWN_FUNCTIONS:
                known = known + 1
                mark = "known"
            else:
                unknown = unknown + 1
                mark = "NOT KNOWN"
            print("%9d %7d  %-34s %s"
                  % (counts[word], files_by.get(word, 0), word, mark))
        print("%d function names known, %d not known" % (known, unknown))
        for cause in sorted(unreadable):
            print("unreadable: %d x %s" % (unreadable[cause], cause))
        return 0
    if len(argv) < 2:
        print(__doc__)
        return 2
    for path in argv[1:]:
        print("=== %s" % path)
        try:
            rule = parse_file(path)
        except Refused as refusal:
            print("  REFUSED %s -- %s" % (refusal.cause, refusal.detail))
            continue
        print("  mnem %r operands %r" % (rule.mnem, rule.operands))
        env = Environment()
        for index, operand in enumerate(rule.operands):
            if "var" in operand:
                env.register_of[operand["var"]] = z3.BitVec(
                    "op%d" % index, 64)
                env.immediate_of[operand["var"]] = z3.BitVec(
                    "op%d" % index, 64)
            else:
                env.register_of[operand["literal"]] = z3.BitVec(
                    "op%d" % index, 64)
        for flag in ("CF", "PF", "AF", "ZF", "SF", "OF"):
            env.flag_of[flag] = z3.BitVec("flag_%s" % flag, 1)
        for place, value, refusal in places_of(rule, env):
            if refusal is not None:
                print("  %-24s REFUSED %s -- %s"
                      % (place, refusal.cause, refusal.detail))
                continue
            region, forced = undefined_region(value.term)
            print("  %-24s %s" % (place, z3.simplify(forced)))
            if not z3.is_false(z3.simplify(region)):
                print("      undefined where: %s" % z3.simplify(region))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
