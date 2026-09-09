#!/usr/bin/env python3
"""model_translate.py -- the reference simulator's opcode semantics, to Lean 4
definitions over `BitVec`.

WHAT THIS PROGRAM IS, in relation to the two things it sits between.
  On one side: `reference.py`, THE one symbolic simulator of the machine.  Its
  `opcode_table` holds, per arch mnemonic, a BUILDER -- a python function that
  applies that opcode's meaning to a symbolic machine state, producing z3
  terms.  On the other side: Lean 4, whose kernel checks proofs.  This program
  RUNS the reference's own builders on a fresh symbolic state and writes what
  comes back as Lean definitions.  Nothing about an opcode's meaning is typed
  here.  A meaning this program cannot carry across is a REFUSAL by cause, and
  a refusal is never patched by writing the definition by hand.

WHY DERIVED RATHER THAN WRITTEN (log_229 section 4.1).  A Lean model written
beside the reference would be a SECOND reading of the hardware, and two
readings can disagree without anyone noticing.  Derived, there is one reading;
the single-opcode check then tests the TRANSLATOR, and a discrepancy is
located rather than diffuse.

THE FOUR STAGES
  1. RUN.  One body line on a fresh `reference.MachineState`.  A fresh state
     seeds every register family it is asked for as a free symbol, so what the
     builder leaves behind is already the opcode's GENERIC form: a function of
     free symbols and nothing else.
  2. READ WHAT CHANGED.  A family whose new value is not its own seed was
     written.  The flag triple (setter name, L, R) is read the same way.
  3. TRANSLATE.  The free symbols are renamed positionally v0, v1, ... and the
     term is printed by `layer5.one_line` -- the pipeline's own fixed print
     rule.  That one line goes through `term_to_lean.translate`, which parses
     it, infers widths, REBUILDS IT IN Z3 AND DEMANDS Z3'S PRINTER REPRODUCE
     THE LINE, and only then emits Lean.  So the bit-vector rule table lives in
     exactly one place: `term_to_lean.OPERATOR_TABLE` / `term_to_lean.lean_of`.
  4. NAME AND DEDUPE.  Two lines whose generic Lean bodies are the same string
     under positional parameter names are ONE definition.  So a definition is
     one distinct mapping, not one line.

THE FLOATING-POINT LAYER, and why it is not a hand-written model.
  `term_to_lean.py` refuses every floating-point node, because Lean's
  `bv_decide` bit-blasts to a SAT solver and has no floating-point theory.  The
  brief's rule is that a float opcode is still TRANSLATED and its CHECK marked
  unavailable.  So the float nodes of a reference term are carried across as
  UNINTERPRETED Lean constants -- `opaque` declarations over `BitVec`, one per
  distinct (float operation, widths) this program actually meets, generated
  from the z3 declaration kinds encountered and never typed.  Two of z3's
  float nodes are not arithmetic and are carried as the identity, with the
  seam named on the record:
    * `fpToFP(bv)` with one argument is IEEE bit-pattern REINTERPRETATION;
    * `fp.to_ieee_bv(f)` is its inverse.
  Both are the identity on bit patterns EXCEPT that SMT-LIB leaves
  `fp.to_ieee_bv` unspecified on a NaN, so a NaN payload may differ.  That is
  recorded as the cause NAN_PAYLOAD_SEAM on every definition that carries one.
  An `opaque` constant is a function symbol with no equations, so nothing can
  be proved about it -- which is the honest state of the float model until the
  lean node's `float_model` sub-node is built.

THE REFUSAL CAUSES this program uses (it refuses by cause; it never guesses)
  NOT_MODELLED_BY_THE_REFERENCE  the reference's own builder raised
                                 `NotModeled` on this line, with its words
  NO_BUILDER                     the opcode is a census row in the table: an
                                 entry with no builder, which the opcode_table
                                 CORE requires be counted, not hidden
  NOTHING_WRITTEN                the builder ran and changed no register and
                                 no flag at this operand shape
  UNKNOWN_Z3_KIND                a z3 declaration kind with no rule here
  plus every cause `term_to_lean.translate` raises: FLOATING_POINT,
  UNKNOWN_NODE, WIDTH_UNRESOLVED, ROUNDTRIP_MISMATCH, PARSE_ERROR,
  UNGUARDED_DIVISION.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a second
violation). No operator token may appear in ANY key, grouping, pairing, row
structure, candidate selection, or comparison scope, anywhere in this line --
not in matching, not in "which pairs get compared", not in report rows, not in
dropdowns. The candidate set for comparison comes from machine-form evidence
(clusters, connections, type pairs) or from ratified intention -- never from
the token. The token appears exactly once per unit: as a display label on the
member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2) verdicts.py's
row pairing (caught by the owner 2026-08-25 -- the fix brief itself reintroduced it
as "same-operator pairs"). MECHANICAL GUARD REQUIRED: every pipeline stage
that groups or pairs units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on failure.
A brief handed to any subagent for this line MUST paste this paragraph
verbatim."

No source operator token appears in this file or in what it writes.  Every key
here is an ARCH MNEMONIC read off a disassembled body, or a WIDTH, or a
machine-form signature; the arch mnemonic is carried in a field named `mnem`,
which the guard treats as machine form.  No candidate set is formed here at
all: the population is the single-opcode rows task o2 fixed from the machine
form, and the model's population is the opcode table's own inventory.

usage:
  model_translate.py table            print the two rule tables
  model_translate.py five             the five opcodes the brief names, end to end
  model_translate.py model            sweep the table, write Model.lean + the json
  model_translate.py check            the 243 rows, write ModelCheck/*.lean + the json
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OP = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, OP)

sys.setrecursionlimit(30000)
"""A vector opcode's term nests deeply -- `punpcklqdq` and the packed float
family build one `Concat` per lane -- and both the emitter here and
`term_to_lean.py`'s parser walk a term by recursion.  30,000 frames is well
above the deepest term this corpus holds; a term that still passes it is
REFUSED by the cause DEEP_TERM rather than stopping the run."""

import z3                                                        # noqa: E402
import layer5                                                    # noqa: E402
import reference as R                                            # noqa: E402
import term_to_lean as TTL                                       # noqa: E402


# ==================================================================
# section 0: the two rule tables
# ==================================================================

# TABLE ONE -- the bit-vector rules.  NOT restated here: they are
# `term_to_lean.OPERATOR_TABLE`, and this program reaches them by handing
# `term_to_lean.translate` a printed line.  `model_translate.py table` prints
# that table so the log carries it LITERAL.

# TABLE TWO -- the floating-point rules, keyed by the z3 DECLARATION KIND the
# reference's own term carries, never by a printed name (z3 prints several
# different conversions all as `fpToFP`).  Right-hand side: how this program
# writes the node in Lean, where every float value is its IEEE bit pattern as a
# `BitVec`.  `opaque` = an uninterpreted Lean constant this program declares.
FLOAT_RULES = [
    ("Z3_OP_FPA_TO_IEEE_BV", "identity on the bit pattern (NAN_PAYLOAD_SEAM)"),
    ("Z3_OP_FPA_TO_FP, one bit-vector argument",
     "identity on the bit pattern (NAN_PAYLOAD_SEAM)"),
    ("Z3_OP_FPA_TO_FP, a rounding mode and a bit-vector",
     "opaque ieeeOfSIntW<src>ToF<dst>Rne"),
    ("Z3_OP_FPA_TO_FP, a rounding mode and a float",
     "opaque ieeeConvertF<src>ToF<dst>Rne"),
    ("Z3_OP_FPA_ADD", "opaque ieeeAddF<w>Rne"),
    ("Z3_OP_FPA_SUB", "opaque ieeeSubF<w>Rne"),
    ("Z3_OP_FPA_MUL", "opaque ieeeMulF<w>Rne"),
    ("Z3_OP_FPA_DIV", "opaque ieeeDivF<w>Rne"),
    ("Z3_OP_FPA_NEG", "opaque ieeeNegF<w>"),
    ("Z3_OP_FPA_ABS", "opaque ieeeAbsF<w>"),
    ("Z3_OP_FPA_EQ", "opaque ieeeEqF<w> : ... -> Bool"),
    ("Z3_OP_FPA_LT", "opaque ieeeLtF<w> : ... -> Bool"),
    ("Z3_OP_FPA_LE", "opaque ieeeLeF<w> : ... -> Bool"),
    ("Z3_OP_FPA_GT", "opaque ieeeGtF<w> : ... -> Bool"),
    ("Z3_OP_FPA_GE", "opaque ieeeGeF<w> : ... -> Bool"),
    ("Z3_OP_FPA_IS_NAN", "opaque ieeeIsNanF<w> : ... -> Bool"),
    ("Z3_OP_FPA_IS_INF", "opaque ieeeIsInfF<w> : ... -> Bool"),
    ("Z3_OP_FPA_IS_ZERO", "opaque ieeeIsZeroF<w> : ... -> Bool"),
    ("Z3_OP_FPA_RM_NEAREST_TIES_TO_EVEN",
     "absorbed into the Rne suffix of the operation above it"),
]

FLOAT_BINARY_KINDS = {
    "Z3_OP_FPA_ADD": "ieeeAddF%dRne",
    "Z3_OP_FPA_SUB": "ieeeSubF%dRne",
    "Z3_OP_FPA_MUL": "ieeeMulF%dRne",
    "Z3_OP_FPA_DIV": "ieeeDivF%dRne",
}
FLOAT_UNARY_KINDS = {
    "Z3_OP_FPA_NEG": "ieeeNegF%d",
    "Z3_OP_FPA_ABS": "ieeeAbsF%d",
}
FLOAT_PREDICATE_KINDS = {
    "Z3_OP_FPA_EQ": "ieeeEqF%d",
    "Z3_OP_FPA_LT": "ieeeLtF%d",
    "Z3_OP_FPA_LE": "ieeeLeF%d",
    "Z3_OP_FPA_GT": "ieeeGtF%d",
    "Z3_OP_FPA_GE": "ieeeGeF%d",
}
FLOAT_ONE_PREDICATE_KINDS = {
    "Z3_OP_FPA_IS_NAN": "ieeeIsNanF%d",
    "Z3_OP_FPA_IS_INF": "ieeeIsInfF%d",
    "Z3_OP_FPA_IS_ZERO": "ieeeIsZeroF%d",
}

NAN_SEAM = "NAN_PAYLOAD_SEAM"


class Refused(Exception):
    def __init__(self, cause, detail):
        Exception.__init__(self, "%s: %s" % (cause, detail))
        self.cause = cause
        self.detail = detail


# ==================================================================
# section 1: the operand shapes the sweep tries
# ==================================================================
#
# These are PROBES, not semantics: each is one legal way to spell an
# instruction's operands, and the reference's own builder decides whether it
# models that shape.  Nothing about what an opcode MEANS is decided here.

GPR_A = {8: "%dil", 16: "%di", 32: "%edi", 64: "%rdi"}
GPR_B = {8: "%sil", 16: "%si", 32: "%esi", 64: "%rsi"}
GPR_C = {8: "%r8b", 16: "%r8w", 32: "%r8d", 64: "%r8"}
XMM_A = "%xmm0"
XMM_B = "%xmm1"

SWEEP_WIDTHS = (8, 16, 32, 64)


def shapes_for(width):
    """every operand spelling this sweep tries at one operand width, as
    (shape name, operand texts in the arch text's own order)."""
    a = GPR_A[width]
    b = GPR_B[width]
    c = GPR_C[width]
    out = [
        ("gpr_gpr", [b, a]),
        ("gpr_same", [a, a]),
        ("gpr_one", [a]),
        ("imm_gpr", ["$0x3", a]),
        ("cl_gpr", ["%cl", a]),
        ("mem_gpr", ["(%rsi)", a]),
        ("gpr_mem", [b, "(%rax)"]),
        ("lea_mem", ["(%rsi,%rcx,1)", GPR_A[64]]),
        ("imm_gpr_gpr", ["$0x3", b, a]),
        ("cl_gpr_gpr", ["%cl", b, a]),
        ("xmm_xmm", [XMM_B, XMM_A]),
        ("xmm_same", [XMM_A, XMM_A]),
        ("gpr_xmm", [a, XMM_A]),
        ("xmm_gpr", [XMM_B, a]),
        ("mem_xmm", ["(%rsi)", XMM_A]),
        ("xmm_mem", [XMM_B, "(%rax)"]),
        ("mem_one", ["(%rsi)"]),
        ("imm_xmm_gpr", ["$0x1", XMM_B, a]),
        ("imm_gpr_xmm", ["$0x1", b, XMM_A]),
        ("none", []),
        # THE X87 REGISTER STACK, added 2026-09-08 by task m1b, whose
        # brief authorises exactly these three and nothing else.  The
        # x87 stack is the one place the reference models that this
        # list had no spelling for, so `faddp %st,%st(1)` -- 1,259
        # ledger rows of the corpus -- had no shape to be classified
        # into and every x87 mnemonic's attestation collapsed onto
        # `mem_one`.  These three carry no width of their own: an x87
        # register is 80 bits whatever the loop variable says, and the
        # operand texts are the same at all four widths.  `st_none` is
        # spelled apart from `none` because an x87 opcode with no
        # operand (`fldz`, `faddp`) reads and writes the stack, which
        # a general opcode with no operand does not.
        ("st_st", ["%st", "%st(1)"]),
        ("st_one", ["%st(1)"]),
        ("st_none", []),
    ]
    return out


def widening_pair(mnemonic):
    """the (source width, destination width) the reference's OWN extension
    tables give this mnemonic, or nothing."""
    pair = R.SIGN_EXTEND.get(mnemonic)
    if pair is None:
        pair = R.ZERO_EXTEND.get(mnemonic)
    return pair


def widening_shapes(mnemonic):
    pair = widening_pair(mnemonic)
    if pair is None:
        return []
    source, destination = pair
    return [("widen_gpr_gpr", [GPR_B[source], GPR_A[destination]]),
            ("widen_mem_gpr", ["(%rsi)", GPR_A[destination]])]


# ==================================================================
# section 2: RUN one line on a fresh state, and read what changed
# ==================================================================


X87_SORT = z3.FPSort(15, 64)
"""the x87 register stack's own width, the shape the machine_state CORE
states: an 80-bit extended float, `z3.FPSort(15, 64)`."""


def preseeded_state(width, setter):
    """a state whose FLAGS, MACHINE STACK and X87 STACK already hold free
    symbols.

    An opcode that READS one of those places leaves nothing behind on a state
    where the place is empty -- the reference refuses by name, which is
    correct for a body but wrong for a MODEL, since the mapping is a function
    OF that place.  So the second sweep pass hands the builder a state in
    which every place it might read is a free symbol, and those symbols become
    the definition's parameters like any other."""
    state = R.MachineState()
    if setter is not None:
        state.flags = (setter, z3.BitVec("seed_FLAG_L", width),
                       z3.BitVec("seed_FLAG_R", width))
    state.push_value(z3.BitVec("seed_STACK_0", 64))
    state.x87_push(z3.FP("seed_X87_1", X87_SORT))
    state.x87_push(z3.FP("seed_X87_0", X87_SORT))
    return state


def snapshot(state):
    places = {}
    for family, term in state.registers.items():
        places["reg_%s" % family] = term
    for index, term in enumerate(state.x87["slots"]):
        places["x87_%d" % index] = term
    for offset, term in state.stack["cells"].items():
        places["stack_%d" % offset] = term
    for text, term in state.memory.items():
        places["mem_%s" % R.mangle(text)] = term
    return places


def run_line(mnemonic, texts, state=None):
    """one body line, on a fresh MachineState unless one is handed in.

    Returns (written places -> term, flag triple or None, the state, the line
    as the reference is handed it).  A fresh state seeds every place the
    builder asks for as a free symbol, so what it leaves behind is already the
    opcode's generic mapping."""
    line = mnemonic
    if texts:
        line = "%s %s" % (mnemonic, ",".join(texts))
    if state is None:
        state = R.MachineState()
    before = snapshot(state)
    R.REFERENCE.step(state, line)
    after = snapshot(state)
    written = {}
    for place, term in after.items():
        if term is None:
            continue
        was = before.get(place)
        if was is not None and was.sexpr() == term.sexpr():
            continue
        if place.startswith("reg_"):
            seed = state.shared_seed.get(place[4:])
            if seed is not None and term.sexpr() == seed.sexpr():
                continue
        written[place] = as_bits(term)
    return written, state.flags, state, line


def free_symbols_ordered(term):
    """every free symbol of a term, in the order the pipeline's own layer-5
    rule meets them, so the parameter order is the print order."""
    return layer5.ordered_symbols(term)


def positional(term):
    """(the term with its free symbols renamed v0, v1, ..., the original
    symbols in that order)."""
    symbols = free_symbols_ordered(term)
    substitution = []
    for index, symbol in enumerate(symbols):
        if symbol.sort().kind() == z3.Z3_BV_SORT:
            fresh = z3.BitVec("v%d" % index, symbol.size())
        else:
            fresh = z3.Const("v%d" % index, symbol.sort())
        substitution.append((symbol, fresh))
    if substitution:
        term = z3.substitute(term, *substitution)
    return term, symbols


# ==================================================================
# section 3: TRANSLATE a z3 term to one Lean expression
# ==================================================================


def ieee_width(sort):
    """the width of the IEEE bit pattern a z3 float sort holds."""
    return sort.ebits() + sort.sbits()


def sort_width(term):
    sort = term.sort()
    if sort.kind() == z3.Z3_BV_SORT:
        return sort.size()
    if sort.kind() == z3.Z3_FLOATING_POINT_SORT:
        return ieee_width(sort)
    return None


KIND_NAMES = {}
for _name in dir(z3.z3consts):
    if _name.startswith("Z3_OP_"):
        KIND_NAMES.setdefault(getattr(z3.z3consts, _name), _name)


def _kind_name(term):
    """the z3 declaration kind of a node, as its own enum name."""
    number = term.decl().kind()
    return KIND_NAMES.get(number, "Z3_OP_UNKNOWN_%d" % number)


def carries_float(term):
    if term.sort().kind() == z3.Z3_FLOATING_POINT_SORT:
        return True
    if term.sort().kind() == z3.Z3_ROUNDING_MODE_SORT:
        return True
    for kid in term.children():
        if carries_float(kid):
            return True
    return False


class LeanOut(object):
    """what one translation produced: the Lean text, the opaque float
    constants it needs declared, and the seams it carries."""

    def __init__(self):
        self.opaques = {}
        self.seams = set()


def lean_of_term(term, out):
    """one z3 term -> one Lean expression string.

    Bit-vector and boolean nodes are handed to `term_to_lean.lean_of`, which
    holds the ONE bit-vector rule table; this function's own rules are the
    float ones of FLOAT_RULES and nothing else."""
    sort_kind = term.sort().kind()
    name = _kind_name(term)

    if sort_kind == z3.Z3_ROUNDING_MODE_SORT:
        raise Refused("UNKNOWN_Z3_KIND",
                      "a rounding mode reached the emitter on its own: %s"
                      % name)

    if name == "Z3_OP_FPA_TO_IEEE_BV":
        out.seams.add(NAN_SEAM)
        return lean_of_term(term.arg(0), out)

    if name == "Z3_OP_FPA_TO_FP":
        return float_conversion(term, out)

    if name in FLOAT_BINARY_KINDS:
        width = ieee_width(term.sort())
        symbol = FLOAT_BINARY_KINDS[name] % width
        declare(out, symbol, [width, width], width, "bv")
        return "(%s %s %s)" % (symbol, lean_of_term(term.arg(1), out),
                               lean_of_term(term.arg(2), out))

    if name in FLOAT_UNARY_KINDS:
        width = ieee_width(term.sort())
        symbol = FLOAT_UNARY_KINDS[name] % width
        declare(out, symbol, [width], width, "bv")
        return "(%s %s)" % (symbol, lean_of_term(term.arg(0), out))

    if name in FLOAT_PREDICATE_KINDS:
        width = ieee_width(term.arg(0).sort())
        symbol = FLOAT_PREDICATE_KINDS[name] % width
        declare(out, symbol, [width, width], None, "bool")
        return "(%s %s %s)" % (symbol, lean_of_term(term.arg(0), out),
                               lean_of_term(term.arg(1), out))

    if name in FLOAT_ONE_PREDICATE_KINDS:
        width = ieee_width(term.arg(0).sort())
        symbol = FLOAT_ONE_PREDICATE_KINDS[name] % width
        declare(out, symbol, [width], None, "bool")
        return "(%s %s)" % (symbol, lean_of_term(term.arg(0), out))

    if sort_kind == z3.Z3_FLOATING_POINT_SORT:
        if name == "Z3_OP_UNINTERPRETED":
            # a free float symbol -- an x87 position this body did not write,
            # or a lane that arrived.  In this model a float value IS its IEEE
            # bit pattern, so the symbol is a bit-vector parameter and its
            # name is what stands here.
            return term.decl().name()
        if name in FLOAT_LITERAL_KINDS:
            # a float CONSTANT the builder wrote (`fldz` pushes +0.0).  Its
            # IEEE encoding is computed by z3 itself rather than typed.
            bits = z3.simplify(z3.fpToIEEEBV(term))
            node = TTL.Node("num", value=bits.as_long())
            node.width = bits.size()
            return TTL.lean_of(node, False)
        raise Refused("UNKNOWN_Z3_KIND",
                      "a float-valued node with no rule: %s" % name)

    return bitvector_node(term, name, out)


FLOAT_LITERAL_KINDS = frozenset([
    "Z3_OP_FPA_PLUS_ZERO", "Z3_OP_FPA_MINUS_ZERO", "Z3_OP_FPA_PLUS_INF",
    "Z3_OP_FPA_MINUS_INF", "Z3_OP_FPA_NAN", "Z3_OP_FPA_NUM",
    "Z3_OP_FPA_FP",
])


def float_conversion(term, out):
    """z3 prints every one of these `fpToFP`; they are told apart by their
    argument sorts, which is machine form and not a name."""
    args = [term.arg(i) for i in range(term.num_args())]
    if len(args) == 1 and args[0].sort().kind() == z3.Z3_BV_SORT:
        out.seams.add(NAN_SEAM)
        return lean_of_term(args[0], out)
    if len(args) == 2 and \
            args[0].sort().kind() == z3.Z3_ROUNDING_MODE_SORT:
        source = args[1]
        destination = ieee_width(term.sort())
        if source.sort().kind() == z3.Z3_BV_SORT:
            symbol = "ieeeOfSIntW%dToF%dRne" % (source.sort().size(),
                                                destination)
            declare(out, symbol, [source.sort().size()], destination, "bv")
            return "(%s %s)" % (symbol, lean_of_term(source, out))
        if source.sort().kind() == z3.Z3_FLOATING_POINT_SORT:
            symbol = "ieeeConvertF%dToF%dRne" % (ieee_width(source.sort()),
                                                 destination)
            declare(out, symbol, [ieee_width(source.sort())], destination,
                    "bv")
            return "(%s %s)" % (symbol, lean_of_term(source, out))
    raise Refused("UNKNOWN_Z3_KIND",
                  "a float conversion this program has no rule for: %d "
                  "argument(s)" % len(args))


def declare(out, symbol, argument_widths, result_width, result_kind):
    """record that the Lean file must carry this uninterpreted constant."""
    pieces = ["BitVec %d" % w for w in argument_widths]
    if result_kind == "bool":
        pieces.append("Bool")
    else:
        pieces.append("BitVec %d" % result_width)
    out.opaques[symbol] = "opaque %s : %s" % (symbol, " → ".join(pieces))


def bitvector_node(term, name, out):
    """a bit-vector or boolean node, written through `term_to_lean.lean_of`
    so the bit-vector rule table has one home.

    The children are emitted first and handed in as `var` nodes carrying their
    finished Lean text; `term_to_lean.lean_of` returns a `var`'s name
    verbatim, so this substitutes text into that table's own forms rather than
    restating them."""
    if z3.is_const(term) and \
            term.decl().kind() == z3.Z3_OP_UNINTERPRETED:
        return term.decl().name()
    if name == "Z3_OP_BNUM":
        node = TTL.Node("num", value=term.as_long())
        node.width = term.sort().size()
        return TTL.lean_of(node, False)
    if name == "Z3_OP_TRUE":
        return "true"
    if name == "Z3_OP_FALSE":
        return "false"

    if name == "Z3_OP_EXTRACT":
        high, low = term.params()
        kid = TTL.Node("var", name=lean_of_term(term.arg(0), out))
        node = TTL.Node("app", "Extract",
                        [TTL.Node("num", value=high),
                         TTL.Node("num", value=low), kid])
        node.width = term.sort().size()
        return TTL.lean_of(node, False)

    if name in ("Z3_OP_ZERO_EXT", "Z3_OP_SIGN_EXT"):
        added = term.params()[0]
        kid = TTL.Node("var", name=lean_of_term(term.arg(0), out))
        head = "ZeroExt" if name == "Z3_OP_ZERO_EXT" else "SignExt"
        node = TTL.Node("app", head, [TTL.Node("num", value=added), kid])
        node.width = term.sort().size()
        return TTL.lean_of(node, False)

    head = BV_KIND_TO_NODE.get(name)
    if head is None:
        raise Refused("UNKNOWN_Z3_KIND", "no rule for %s" % name)
    if head in ("bvudiv_i", "bvsdiv_i", "bvurem_i", "bvsrem_i", "bvsmod_i"):
        raise Refused("UNGUARDED_DIVISION",
                      "z3's %s has no specified value at a zero divisor, and "
                      "Lean's own answers zero there" % head)
    kids = []
    for index in range(term.num_args()):
        kids.append(TTL.Node("var",
                             name=lean_of_term(term.arg(index), out)))
    node = TTL.Node("app", head, kids)
    node.width = sort_width(term)
    return TTL.lean_of(node, False)


# z3 declaration kind -> the node name `term_to_lean.lean_of` knows.  This is
# a NAMING table only: what each name MEANS in Lean is stated once, in
# `term_to_lean.OPERATOR_TABLE`.
BV_KIND_TO_NODE = {
    "Z3_OP_BADD": "+", "Z3_OP_BSUB": "-", "Z3_OP_BMUL": "*",
    "Z3_OP_BAND": "&", "Z3_OP_BOR": "|", "Z3_OP_BXOR": "^",
    "Z3_OP_BNOT": "u~", "Z3_OP_BNEG": "u-",
    "Z3_OP_BSHL": "<<", "Z3_OP_BLSHR": "LShR", "Z3_OP_BASHR": ">>",
    "Z3_OP_CONCAT": "Concat", "Z3_OP_ITE": "If",
    "Z3_OP_EQ": "==", "Z3_OP_DISTINCT": "!=",
    "Z3_OP_SLEQ": "<=", "Z3_OP_SLT": "<",
    "Z3_OP_SGEQ": ">=", "Z3_OP_SGT": ">",
    "Z3_OP_ULEQ": "ULE", "Z3_OP_ULT": "ULT",
    "Z3_OP_UGEQ": "UGE", "Z3_OP_UGT": "UGT",
    "Z3_OP_AND": "And", "Z3_OP_OR": "Or", "Z3_OP_NOT": "u!",
    "Z3_OP_BUDIV": "UDiv", "Z3_OP_BUREM": "URem",
    "Z3_OP_BSDIV": "SDiv", "Z3_OP_BSREM": "SRem", "Z3_OP_BSMOD": "SMod",
    "Z3_OP_BUDIV_I": "bvudiv_i", "Z3_OP_BSDIV_I": "bvsdiv_i",
    "Z3_OP_BUREM_I": "bvurem_i", "Z3_OP_BSREM_I": "bvsrem_i",
    "Z3_OP_BSMOD_I": "bvsmod_i",
}


def translate_term(term):
    """one z3 term -> {lean, params, widths, opaques, seams} or a refusal.

    The free symbols become the definition's parameters, in the pipeline's own
    print order.  A float-free term is ALSO translated a second way -- printed
    by layer5's fixed rule and put through `term_to_lean.translate`, which
    round-trips the parse against z3's own printer -- and the two must agree
    character for character.  A disagreement is a refusal, not a warning."""
    renamed, symbols = positional(term)
    record = {
        "params": [s.decl().name() for s in symbols],
        "param_widths": [sort_width(s) for s in symbols],
        "result_width": sort_width(term),
        "float": carries_float(term),
    }
    out = LeanOut()
    try:
        record["lean"] = lean_of_term(renamed, out)
    except Refused as refusal:
        record["lean"] = None
        record["refused"] = [refusal.cause, refusal.detail]
        return record
    except TTL.Refused as refusal:
        record["lean"] = None
        record["refused"] = [refusal.cause, refusal.detail]
        return record
    except RecursionError:
        record["lean"] = None
        record["refused"] = ["DEEP_TERM",
                             "the term nests past this program's recursion "
                             "ceiling"]
        return record
    record["opaques"] = sorted(out.opaques.values())
    record["seams"] = sorted(out.seams)
    record["refused"] = None
    if not record["float"]:
        free_widths = {}
        for index, width in enumerate(record["param_widths"]):
            free_widths["v%d" % index] = width
        printed = layer5.one_line(renamed)
        record["printed"] = printed
        try:
            second = TTL.translate(printed, free_widths,
                                   record["result_width"])
        except RecursionError:
            record["cross_check"] = ("UNAVAILABLE: DEEP_TERM the printed "
                                     "line nests past the parser's "
                                     "recursion ceiling")
            return record
        record["cross_check"] = "AGREES"
        record["roundtrip_ok"] = second.get("roundtrip_ok")
        if second.get("refused") is not None:
            # THE CROSS-CHECK COULD NOT RUN.  The term route walks the z3
            # object and parses nothing, so a printed-text route that cannot
            # read the line does not make the definition wrong -- it makes the
            # second opinion unavailable, and that is what is recorded.
            record["cross_check"] = "UNAVAILABLE: %s %s" % (
                second["refused"][0], second["refused"][1])
            return record
        if second["lean"] != record["lean"]:
            record["lean_from_printed_text"] = second["lean"]
            record["lean"] = None
            record["refused"] = [
                "TRANSLATOR_DISAGREEMENT",
                "the term route and the printed-text route wrote different "
                "Lean"]
            return record
    return record


# ==================================================================
# section 4: the model -- one definition per distinct mapping
# ==================================================================

FLAGS_STRUCTURE = """\
/-- The reference's flag model, its own shape: the (setter, L, R) triple the
    last flag-setting instruction left.  `setter` is the arch mnemonic that
    wrote them, which is what `condition_table.predicate_of` reads to choose
    between the integer route, the float route and the carry route -- so a
    record that dropped it would answer a later condition by the wrong rule. -/
structure Flags (w : Nat) where
  setter : String
  L : BitVec w
  R : BitVec w
"""


class Model(object):
    """the growing set of Lean definitions: one per distinct mapping, named
    `model_<mnem>_<serial>`, with the body lines that produced it recorded
    beside it so the definition can be read against the instruction."""

    def __init__(self):
        self.by_signature = {}
        self.definitions = []
        self.opaques = {}
        self.serial = {}
        self.lines_of = {}

    def name_for(self, mnemonic):
        self.serial[mnemonic] = self.serial.get(mnemonic, -1) + 1
        return "model_%s_%d" % (mnemonic, self.serial[mnemonic])


def add_definition(model, mnemonic, translated, is_flags=False,
                   setter=None, note=None):
    """one translated term becomes one Lean definition, or joins the one an
    identical mapping already has.

    Two lines whose generic Lean bodies are the same string under positional
    parameter names are ONE definition, so a definition is one distinct
    mapping rather than one spelling."""
    body = translated["lean"]
    if isinstance(body, list):
        body = tuple(body)
    signature = (mnemonic, tuple(translated["param_widths"]),
                 translated["result_width"], body, bool(is_flags), setter)
    if signature in model.by_signature:
        name = model.by_signature[signature]
        if note:
            model.lines_of.setdefault(name, set()).add(note)
        return name
    width = translated["result_width"]
    name = model.name_for(mnemonic)
    if is_flags:
        name = name + "_flags"
    if note:
        model.lines_of.setdefault(name, set()).add(note)
    binders = []
    for index, param_width in enumerate(translated["param_widths"]):
        binders.append("(v%d : BitVec %d)" % (index, param_width))
    head = "def %s %s" % (name, " ".join(binders)) if binders \
        else "def %s" % name
    if is_flags:
        body = ("{ setter := %s, L := %s, R := %s }"
                % (json.dumps(setter), translated["lean"][0],
                   translated["lean"][1]))
        text = "%s : Flags %d :=\n  %s" % (head, width, body)
    else:
        text = "%s : BitVec %d :=\n  %s" % (head, width, translated["lean"])
    model.definitions.append((name, text))
    for line in translated.get("opaques", []):
        symbol = line.split()[1]
        model.opaques[symbol] = line
    model.by_signature[signature] = name
    return name


def attempts_for(mnemonic):
    out = []
    for width in SWEEP_WIDTHS:
        for shape_name, texts in shapes_for(width):
            out.append((shape_name, width, texts))
    for shape_name, texts in widening_shapes(mnemonic):
        out.append((shape_name, None, texts))
    return out


def sweep(model):
    """every mnemonic the table models, at every operand shape this program
    spells, recorded by outcome.

    TWO PASSES.  Pass one hands each builder a fresh state.  Pass two is run
    only over the mnemonics pass one left with no definition at all, and hands
    them a state whose flags, machine stack and x87 stack already hold free
    symbols -- because an opcode that READS one of those is a function of it,
    and a state where the place is empty makes the reference refuse by name.
    The flag setters pass two tries are not typed here: they are the setter
    names pass one's own flag definitions carried."""
    table = R.REFERENCE.opcode_table
    rows = []
    translated = set()
    setters = set()
    for mnemonic in sorted(table.entries):
        entry = table.entries[mnemonic]
        if entry.build is None:
            rows.append({"mnem": mnemonic, "shape": None, "width": None,
                         "outcome": "NO_BUILDER",
                         "cause": entry.cause or
                         "an entry with no builder: a census row"})
            continue
        for shape_name, width, texts in attempts_for(mnemonic):
            row = one_attempt(model, mnemonic, shape_name, width, texts)
            rows.append(row)
            if row["outcome"] == "TRANSLATED":
                translated.add(mnemonic)
            if row.get("flag_setter"):
                setters.add(row["flag_setter"])
    empty = []
    for mnemonic in sorted(table.entries):
        entry = table.entries[mnemonic]
        if entry.build is None:
            continue
        if mnemonic in translated:
            continue
        empty.append(mnemonic)
    for mnemonic in empty:
        entry = table.entries[mnemonic]
        reads_flags = R.FLAGS in entry.reads
        wanted = sorted(setters) if reads_flags else [None]
        for setter in wanted:
            for shape_name, width, texts in attempts_for(mnemonic):
                rows.append(one_attempt(model, mnemonic, shape_name, width,
                                        texts, setter, True))
    return rows


def one_attempt(model, mnemonic, shape_name, width, texts, setter=None,
                preseeded=False):
    row = {"mnem": mnemonic, "shape": shape_name, "width": width,
           "operands": list(texts), "preseeded": preseeded,
           "flags_in_setter": setter}
    state = None
    if preseeded:
        state = preseeded_state(width or 64, setter)
    try:
        written, flags, _state, line = run_line(mnemonic, texts, state)
    except R.NotModeled as refusal:
        row["outcome"] = "NOT_MODELLED_BY_THE_REFERENCE"
        row["cause"] = str(refusal)
        return row
    except Exception as failure:
        row["outcome"] = "NOT_MODELLED_BY_THE_REFERENCE"
        row["cause"] = "%s: %s" % (type(failure).__name__, failure)
        return row
    row["line"] = line
    if not written and flags is None:
        row["outcome"] = "NOTHING_WRITTEN"
        row["cause"] = "the builder ran and changed no register and no flag"
        return row
    row["defs"] = []
    causes = []
    for family in sorted(written):
        try:
            translated = translate_term(written[family])
        except Exception as failure:
            causes.append("%s: TRANSLATOR_ERROR %s"
                          % (family, type(failure).__name__))
            continue
        if translated["refused"] is not None:
            causes.append("%s: %s %s" % (family, translated["refused"][0],
                                         translated["refused"][1]))
            continue
        name = add_definition(model, mnemonic, translated, note=line)
        row["defs"].append({"writes": family, "name": name,
                            "float": translated["float"],
                            "cross_check": translated.get("cross_check"),
                            "seams": translated.get("seams", [])})
    if flags is not None:
        row["flag_setter"] = flags[0]
        try:
            translated = translate_flags(flags)
        except Exception as failure:
            translated = {"refused": ["TRANSLATOR_ERROR",
                                      type(failure).__name__]}
        if translated["refused"] is not None:
            causes.append("flags: %s" % translated["refused"][0])
        else:
            name = add_definition(model, mnemonic, translated, True,
                                  flags[0], note=line)
            row["defs"].append({"writes": "flags", "name": name,
                                "float": translated["float"],
                                "cross_check": translated.get("cross_check"),
                                "seams": translated.get("seams", [])})
    if row["defs"]:
        row["outcome"] = "TRANSLATED"
    else:
        row["outcome"] = "REFUSED"
    if causes:
        row["cause"] = "; ".join(causes)
    return row


def translate_flags(flags):
    """the (setter, L, R) triple, as one record's two bit-vector fields.  L
    and R are translated together so their free symbols share one parameter
    numbering."""
    setter, left, right = flags
    width = sort_width(left)
    pair = z3.Concat(as_bits(left), as_bits(right))
    renamed, symbols = positional(pair)
    record = {
        "params": [s.decl().name() for s in symbols],
        "param_widths": [sort_width(s) for s in symbols],
        "result_width": width,
        "float": carries_float(pair),
        "setter": setter,
    }
    out = LeanOut()
    try:
        whole = renamed
        left_lean = lean_of_term(z3.simplify(
            z3.Extract(2 * width - 1, width, whole)), out)
        right_lean = lean_of_term(z3.simplify(
            z3.Extract(width - 1, 0, whole)), out)
    except (Refused, TTL.Refused) as refusal:
        record["lean"] = None
        record["refused"] = [refusal.cause, refusal.detail]
        return record
    record["lean"] = [left_lean, right_lean]
    record["opaques"] = sorted(out.opaques.values())
    record["seams"] = sorted(out.seams)
    record["refused"] = None
    return record


def as_bits(term):
    """a term as its bit pattern: a float value is its IEEE encoding, which is
    how this whole model holds a float."""
    if term.sort().kind() == z3.Z3_FLOATING_POINT_SORT:
        return z3.fpToIEEEBV(term)
    return term


# ==================================================================
# section 5: the check -- the single-opcode units, against the model
# ==================================================================
#
# THE SHAPE OF ONE CHECK, said before the code.
#   Left of the equals sign: the unit's own PROVED TERM, which the pipeline
#   stored as one printed line (`layer5_normalized_text`) and which
#   `term_to_lean.py` turns into Lean.  That line is the LEDGER route's
#   reading of the unit -- how the term walk wired the unit's own recorded
#   rows together.
#   Right of it: the MODEL's operations, applied in the order the unit's own
#   body spells them.  Every operation is a definition the sweep generated
#   from the reference's builder; this side states no meaning of its own.
#   So the theorem is the two readings of one unit, and a failure is a
#   DISCREPANCY between them rather than a Lean problem.

FLAGS_READ = R.FLAGS
STACK_READ = (R.MACHINE_STACK, R.X87_STACK, R.MEMORY)


def bound_variables(unit_term):
    """the theorem's bound variables, taken from the SAME rule that produced
    the stored text: layer 5 renames free symbols positionally in the order
    its own print meets them, so v0 is whichever symbol the stored line calls
    v0."""
    symbols = free_symbols_ordered(z3.simplify(unit_term))
    names = {}
    widths = []
    for index, symbol in enumerate(symbols):
        names[symbol.decl().name()] = "v%d" % index
        widths.append(sort_width(symbol))
    return names, widths


def argument_lean(symbol_name, names, held, extra):
    """the Lean expression standing where one model parameter goes.

    A parameter of a step's model is a free symbol of that step's generic
    form, named after what the step READ: a register family, a memory cell,
    or a rip-relative constant.  If an earlier step wrote it, its Lean text
    is what that step's model application returned; otherwise it is a value
    the unit received, so it is a bound variable of the theorem."""
    if symbol_name in held:
        return held[symbol_name]
    if symbol_name in names:
        return names[symbol_name]
    fresh = "v%d" % (len(names) + len(extra))
    extra[symbol_name] = fresh
    names[symbol_name] = fresh
    return fresh


def refuse_unwalkable(mnemonic, entry, line):
    """the two shapes this composition cannot carry, refused by name.

    A step that READS THE FLAGS reads state this composition does not carry
    (the flag triple is not a register), and a step that touches memory or a
    stack reads state a later step could have written.  Neither is a Lean
    limitation and neither is guessed at."""
    for place in entry.reads:
        if place == FLAGS_READ:
            raise Refused("FLAGS_READ_NOT_COMPOSED",
                          "line %r reads the flag triple, which this "
                          "composition does not carry" % line)
        if place in STACK_READ:
            raise Refused("STATEFUL_PLACE_NOT_COMPOSED",
                          "line %r reads %s" % (line, place))
    for place in entry.writes:
        if place in STACK_READ:
            raise Refused("STATEFUL_PLACE_NOT_COMPOSED",
                          "line %r writes %s" % (line, place))


def compose_body(model, record, names):
    """walk one unit's body, building the Lean composition of model
    applications beside the reference's own symbolic walk.

    Each line is run TWICE by `reference.step`: once on a fresh state, whose
    result is that opcode's generic mapping and therefore its model
    definition; once on the real state, which carries the values forward."""
    lines = R.REFERENCE.body_lines(record.get("body_verbatim"))
    state = R.MachineState()
    R.REFERENCE.apply_arrival_contract(
        state, record.get("arrival_contract_bindings"))
    held = {}
    extra = {}
    used = []
    for line in lines:
        mnemonic, rest = R.REFERENCE.split_line(line)
        entry = R.REFERENCE.opcode_table.entry_for(mnemonic)
        if entry is None:
            raise Refused("NO_ENTRY",
                          "line %r: no entry in the opcode table" % line)
        if entry.build is None:
            raise Refused("NO_BUILDER",
                          "line %r: %s"
                          % (line, entry.cause or "a census row"))
        refuse_unwalkable(mnemonic, entry, line)
        texts = R.split_operands(rest)
        try:
            written, flags, _fresh, _line = run_line(mnemonic, texts)
        except R.NotModeled as refusal:
            raise Refused("NOT_MODELLED_BY_THE_REFERENCE", str(refusal))
        new_held = {}
        for place in sorted(written):
            if not place.startswith("reg_"):
                raise Refused("STATEFUL_PLACE_NOT_COMPOSED",
                              "line %r writes %s, which this composition "
                              "does not carry" % (line, place))
            family = place[4:]
            translated = translate_term(written[place])
            if translated["refused"] is not None:
                raise Refused(translated["refused"][0],
                              "line %r writing %s: %s"
                              % (line, family, translated["refused"][1]))
            for parameter in translated["params"]:
                if parameter.startswith("ripconst_"):
                    raise Refused(
                        "RIP_CONSTANT_POSITIONAL",
                        "line %r reads a rip-relative constant, whose name "
                        "is its position in the body, so a step run on its "
                        "own does not name the same one" % line)
            name = add_definition(model, mnemonic, translated, note=line)
            arguments = []
            for parameter in translated["params"]:
                arguments.append(argument_lean(parameter, names, held,
                                               extra))
            application = name
            if arguments:
                application = "(%s %s)" % (name, " ".join(arguments))
            new_held["seed_%s" % family] = application
            used.append({"line": line, "writes": family, "name": name})
        held.update(new_held)
        R.REFERENCE.step(state, line)
    return state, held, used, extra


def check_one(model, record, stored_text, unit_term):
    """one row -> one theorem, or a refusal by cause."""
    out = {"unit": record.get("unit")}
    names, widths = bound_variables(unit_term)
    free_widths = {}
    for index, width in enumerate(widths):
        free_widths["v%d" % index] = width
    result_width = record.get("result_width")
    left = TTL.translate(stored_text, free_widths, result_width)
    out["roundtrip_ok"] = left.get("roundtrip_ok")
    if left["refused"] is not None:
        out["outcome"] = "REFUSED"
        out["cause"] = left["refused"][0]
        out["detail"] = left["refused"][1]
        return out
    try:
        _state, held, used, extra = compose_body(model, record, names)
    except Refused as refusal:
        out["outcome"] = "REFUSED"
        out["cause"] = refusal.cause
        out["detail"] = refusal.detail
        return out
    except R.NotModeled as refusal:
        out["outcome"] = "REFUSED"
        out["cause"] = "NOT_MODELLED_BY_THE_REFERENCE"
        out["detail"] = str(refusal)
        return out
    family = record.get("result_family")
    key = "seed_%s" % family
    if key in held:
        answer = held[key]
        answer_width = 128 if family in R.XMM_NAMES else 64
    else:
        answer = argument_lean(key, names, held, extra)
        answer_width = 128 if family in R.XMM_NAMES else 64
    if result_width < answer_width:
        answer = "(%s.extractLsb %d 0)" % (answer, result_width - 1)
    binders = []
    for index, width in enumerate(widths):
        binders.append("(v%d : BitVec %d)" % (index, width))
    for symbol_name in sorted(extra, key=lambda s: extra[s]):
        width = 128 if symbol_name[5:] in R.XMM_NAMES else 64
        binders.append("(%s : BitVec %d)" % (extra[symbol_name], width))
    out["outcome"] = "STATED"
    out["binders"] = binders
    out["left"] = left["lean"]
    out["right"] = answer
    out["steps"] = used
    out["extra_binders"] = sorted(extra.items())
    return out


THEOREM = """\
import Archproof.Model
import Std.Tactic.BVDecide

set_option maxRecDepth 40000
set_option linter.unusedVariables false

namespace Archproof

/-- %s

    Left of the equals sign: the unit's own PROVED TERM, the one the pipeline
    stored as a printed line, put into Lean by term_to_lean.py.
    Right of it: the MODEL's operations, applied in the order this unit's own
    body spells them.  Every name on the right is a definition Model.lean got
    by running the reference simulator's builder for that one opcode.
    So this theorem is the two readings of one unit, and a failure is a
    discrepancy between them. -/
theorem %s %s :
    %s
  = %s := by
  %s

#print axioms %s

end Archproof
"""


def theorem_text(label, name, row, tactic):
    return THEOREM % (label, name, " ".join(row["binders"]), row["left"],
                      row["right"], tactic, name)


def tactic_for(row, which):
    """the two tactics this task tries, in order.

    `rfl` closes a goal the two sides reduce to one form on -- definitional
    agreement, the cheapest of the three obligations log_228 section 4.1
    names.  Where they do not, the model definitions are unfolded and the
    goal is bit-blasted, with the SAT solver's certificate checked in Lean's
    kernel."""
    if which == "rfl":
        return "rfl"
    names = []
    for step in row.get("steps", []):
        if step["name"] not in names:
            names.append(step["name"])
    if not names:
        return "bv_decide"
    return "simp only [%s]\n  bv_decide" % ", ".join(names)


# ==================================================================
# section 6: what the driver writes
# ==================================================================

MODEL_HEADER = """\
/-
  Archproof/Model.lean -- GENERATED by
  PseudoCoupHQ/Research/op_pipeline/lean/model_translate.py
  from the builders of PseudoCoupHQ/Research/op_pipeline/reference.py.

  DO NOT EDIT.  Every definition here was produced by RUNNING the reference
  simulator's own builder for one arch opcode on a fresh symbolic machine
  state and translating what it left behind.  A meaning this file lacks is a
  meaning the reference refused or the translator could not carry, and it is
  recorded by cause in model_L2.json -- never repaired by hand.

  Floating point: every float value here is its IEEE bit pattern as a
  `BitVec`, and every float OPERATION is an `opaque` constant -- an
  uninterpreted function symbol.  Nothing can be proved about an opaque
  constant, which is the honest state of the float model until the lean
  node's `float_model` sub-node is built.  Two of z3's float nodes are
  carried as the identity on bit patterns: `fpToFP` with one bit-vector
  argument, and `fp.to_ieee_bv`.  Those are IEEE reinterpretation and its
  inverse, and they agree except that SMT-LIB leaves `fp.to_ieee_bv`
  unspecified on a NaN, so a NaN payload may differ.  Every definition
  carrying one is marked NAN_PAYLOAD_SEAM in the json.
-/

-- A vector opcode's definition is one term per lane joined by `++`, which
-- elaborates deeply; and the linter's unused-variable warning fires on a
-- definition whose operand shape names a register the mapping does not read
-- (`xorps %xmm0,%xmm0` reads one register twice, so its second parameter is
-- absent).  Both are properties of the generated text, not of the model.
set_option maxRecDepth 40000
set_option linter.unusedVariables false

namespace Archproof

"""


def write_model(directory, model):
    lines = [MODEL_HEADER]
    if model.opaques:
        lines.append("-- the uninterpreted float primitives this model "
                     "needed, one per\n-- (operation, widths) the "
                     "reference's own terms carried\n")
        for symbol in sorted(model.opaques):
            lines.append(model.opaques[symbol])
        lines.append("")
    lines.append(FLAGS_STRUCTURE)
    lines.append("")
    for name, text in model.definitions:
        spellings = sorted(model.lines_of.get(name, []))
        if spellings:
            shown = spellings[:4]
            lines.append("/-- the mapping the reference's own builder leaves "
                         "for: %s%s -/"
                         % ("; ".join(shown),
                            " (and %d more spelling(s))"
                            % (len(spellings) - len(shown))
                            if len(spellings) > len(shown) else ""))
        lines.append(text)
        lines.append("")
    lines.append("end Archproof")
    lines.append("")
    handle = open(os.path.join(directory, "Model.lean"), "w")
    handle.write("\n".join(lines))
    handle.close()


def load_rows():
    """the single-opcode rows, recomputed from task o2's own product: the
    narrow rule, the five compiled languages."""
    source = os.path.join(os.path.dirname(OP), "oracle", "arch_opcodes",
                          "single_opcode_units.json")
    document = json.load(open(source))
    rows = []
    for language in ("c", "cpp", "go", "rust", "swift"):
        group = document["single_opcode_groups"][language]["narrow"]
        for index, row in enumerate(group):
            rows.append({"lang": language, "row_index": index,
                         # task mn1 renamed this field to `mnem`;
                         # `mnemonic` is task o2's older artifact,
                         # accepted as a fallback (task ap3).
                         "mnem": row.get("mnem",
                                         row.get("mnemonic")),
                         "row_body_text": row["body_text"],
                         "unit": row["example_unit_id"],
                         "member_count": row["member_count"]})
    return rows, source


def model_command(out_directory, lean_directory):
    model = Model()
    rows = sweep(model)
    write_model(lean_directory, model)
    per_mnemonic = {}
    for row in rows:
        slot = per_mnemonic.setdefault(row["mnem"],
                                       {"attempts": 0, "translated": 0,
                                        "refused": 0, "no_builder": 0,
                                        "not_modelled": 0, "nothing": 0,
                                        "causes": {}})
        slot["attempts"] += 1
        outcome = row["outcome"]
        if outcome == "TRANSLATED":
            slot["translated"] += 1
        elif outcome == "NO_BUILDER":
            slot["no_builder"] += 1
        elif outcome == "NOT_MODELLED_BY_THE_REFERENCE":
            slot["not_modelled"] += 1
        elif outcome == "NOTHING_WRITTEN":
            slot["nothing"] += 1
        else:
            slot["refused"] += 1
            cause = row.get("cause", "?")
            slot["causes"][cause] = slot["causes"].get(cause, 0) + 1
    document = {
        "what": "every arch mnemonic the reference's opcode table holds, "
                "swept over the operand shapes model_translate.py spells, "
                "with the Lean definitions the reference's own builders "
                "produced",
        "source_of_the_meanings": os.path.join(OP, "reference.py"),
        "definitions": len(model.definitions),
        "opaque_float_primitives": sorted(model.opaques),
        "mnemonics_in_the_table": len(R.REFERENCE.opcode_table.entries),
        "per_mnemonic": per_mnemonic,
        "rows": rows,
    }
    handle = open(os.path.join(out_directory, "model_L2.json"), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    modelled = [m for m in per_mnemonic if per_mnemonic[m]["translated"]]
    print("definitions written: %d" % len(model.definitions))
    print("mnemonics in the table: %d"
          % len(R.REFERENCE.opcode_table.entries))
    print("mnemonics with at least one translated shape: %d" % len(modelled))
    print("opaque float primitives declared: %d -- %s"
          % (len(model.opaques), " ".join(sorted(model.opaques))))
    return model


def five_command():
    """the five opcodes the brief names, end to end and LITERAL."""
    model = Model()
    show = [("add", "gpr_gpr", 64), ("add", "gpr_gpr", 32),
            ("sar", "cl_gpr", 64), ("sar", "imm_gpr", 32),
            ("imul", "gpr_gpr", 64), ("imul", "gpr_one", 64),
            ("ucomiss", "xmm_xmm", 32), ("cvtsi2sd", "gpr_xmm", 32)]
    for mnemonic, wanted, width in show:
        for shape_name, texts in shapes_for(width):
            if shape_name != wanted:
                continue
            row = one_attempt(model, mnemonic, shape_name, width, texts)
            print("=== %s   shape %s   operand width %d"
                  % (mnemonic, shape_name, width))
            print("    line, as the reference is handed it: %r"
                  % row.get("line"))
            print("    outcome: %s" % row["outcome"])
            if row.get("cause"):
                print("    cause  : %s" % row["cause"])
            for one in row.get("defs", []):
                print("    writes %-6s -> %s%s"
                      % (one["writes"], one["name"],
                         "   seams: %s" % ",".join(one["seams"])
                         if one["seams"] else ""))
    print("")
    print("--- Model.lean definitions these produced, LITERAL")
    for name, text in model.definitions:
        spellings = sorted(model.lines_of.get(name, []))
        if spellings:
            print("-- for: %s" % "; ".join(spellings))
        print(text)
        print("")
    if model.opaques:
        print("--- and the uninterpreted float primitives they needed")
        for symbol in sorted(model.opaques):
            print(model.opaques[symbol])
    return 0


def main(argv):
    if len(argv) < 2:
        sys.stderr.write(__doc__)
        return 2
    command = argv[1]
    if command == "table":
        TTL.print_operator_table()
        print("")
        print("| z3 declaration kind | how this program writes it in Lean |")
        print("|---|---|")
        for kind, form in FLOAT_RULES:
            print("| `%s` | `%s` |" % (kind, form))
        print("")
        print("| z3 declaration kind | the node name whose Lean form "
              "`term_to_lean.OPERATOR_TABLE` states |")
        print("|---|---|")
        for kind in sorted(BV_KIND_TO_NODE):
            print("| `%s` | `%s` |" % (kind, BV_KIND_TO_NODE[kind]))
        return 0
    if command == "five":
        return five_command()
    if command == "model":
        model_command(HERE, os.path.join(HERE, "archproof", "Archproof"))
        return 0
    if command == "check":
        return check_command()
    if command == "run":
        return run_command()
    if command == "imports":
        return imports_command()
    if command == "axioms_gap":
        return axioms_gap_command("gap")
    if command == "axioms_refresh":
        return axioms_gap_command("all")
    sys.stderr.write("unknown command %r\n" % command)
    return 2


def check_command():
    """the 243 rows: state each theorem, write it, and record the outcome.

    The Lean run itself is a separate step -- this writes the files and the
    json; a lane builds them and records wall clock and peak memory."""
    import term97_walk as TW
    maker, _gate, _attached, _readings = TW.build()
    model = Model()
    sweep(model)
    rows, source = load_rows()
    held, terms = stream_store(set(row["unit"] for row in rows))
    directory = os.path.join(HERE, "archproof", "Archproof")
    results = []
    for row in rows:
        results.append(one_row(model, maker, row, held, terms, directory))
    write_model(os.path.join(HERE, "archproof", "Archproof"), model)
    document = {
        "what": "every single-opcode row of the five compiled languages, "
                "its own proved term against the model's operations",
        "population_source": source,
        "rows": results,
    }
    handle = open(os.path.join(HERE, "check_L2.json"), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    tally = {}
    for one in results:
        tally[one["outcome"]] = tally.get(one["outcome"], 0) + 1
    print("rows: %d" % len(results))
    for outcome in sorted(tally):
        print("  %-24s %d" % (outcome, tally[outcome]))
    print("definitions after the check: %d" % len(model.definitions))
    return 0


# ==================================================================
# section 7: running the theorems, one `lean` process each
# ==================================================================


def lean_once(path):
    """one theorem file through `lake env lean`, with ITS OWN wall clock and
    ITS OWN peak resident memory.

    `os.wait4` returns the rusage of that one process, so the numbers are per
    theorem rather than a running maximum over every child."""
    import subprocess
    import time
    project = os.path.join(HERE, "archproof")
    relative = os.path.relpath(path, project)
    start = time.time()
    process = subprocess.Popen(["lake", "env", "lean", relative],
                               cwd=project, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    output = process.stdout.read()
    _pid, status, usage = os.wait4(process.pid, 0)
    process.stdout.close()
    wall = time.time() - start
    code = os.waitstatus_to_exitcode(status)
    return {"exit": code, "wall_seconds": round(wall, 3),
            "peak_kb": usage.ru_maxrss,
            "output": output.decode("utf-8", "replace")}


DISCREPANCY_MARKS = ("counter-example", "counterexample")


def classify(result):
    """what a failed `lean` run means, by cause.

    A `bv_decide` that comes back with a counterexample has DECIDED the two
    readings differ -- that is a DISCREPANCY and the counterexample is the
    evidence.  Any other failure is the check being unavailable, and the
    message says which."""
    if result["exit"] == 0:
        return "PROVED", None
    text = result["output"].lower()
    for mark in DISCREPANCY_MARKS:
        if mark in text:
            return "DISCREPANCY", "bv_decide returned a counterexample"
    first = ""
    for line in result["output"].splitlines():
        if "error" in line.lower():
            first = line.strip()
            break
    return "LEAN_REFUSED", first or result["output"].strip()[:400]


def run_command():
    """every stated theorem: `rfl` first, then the model definitions unfolded
    and the goal bit-blasted, recording which closed it and at what cost."""
    document = json.load(open(os.path.join(HERE, "check_L2.json")))
    directory = os.path.join(HERE, "archproof", "Archproof")
    total = 0
    for row in document["rows"]:
        if row.get("outcome") == "STATED":
            total = total + 1
    index = 0
    for row in document["rows"]:
        if row.get("outcome") != "STATED":
            continue
        index = index + 1
        label = "%s single-opcode row %d, arch mnemonic %r, example unit " \
                "%s, %d members" % (row["lang"], row["row_index"],
                                    row["mnem"], row["unit"],
                                    row["member_count"])
        name = row["theorem_name"]
        path = row["file"]
        handle = open(path, "w")
        handle.write(theorem_text(label, name, row, tactic_for(row, "rfl")))
        handle.close()
        result = lean_once(path)
        outcome, detail = classify(result)
        row["rfl"] = {"outcome": outcome, "wall_seconds":
                      result["wall_seconds"], "peak_kb": result["peak_kb"]}
        if outcome == "PROVED":
            row["closed_by"] = "rfl"
            row["wall_seconds"] = result["wall_seconds"]
            row["peak_kb"] = result["peak_kb"]
            row["axioms"] = axiom_line(result["output"])
            print("[%d/%d] %-28s rfl        %6.2f s  %7d kB"
                  % (index, total, name, result["wall_seconds"],
                     result["peak_kb"]))
            continue
        handle = open(path, "w")
        handle.write(theorem_text(label, name, row,
                                  tactic_for(row, "bv_decide")))
        handle.close()
        second = lean_once(path)
        outcome, detail = classify(second)
        row["bv_decide"] = {"outcome": outcome, "wall_seconds":
                            second["wall_seconds"],
                            "peak_kb": second["peak_kb"]}
        row["closed_by"] = "bv_decide" if outcome == "PROVED" else None
        row["wall_seconds"] = second["wall_seconds"]
        row["peak_kb"] = second["peak_kb"]
        if outcome == "PROVED":
            row["axioms"] = axiom_line(second["output"])
        else:
            row["outcome"] = outcome
            row["cause"] = detail
            row["lean_output"] = second["output"][:4000]
        print("[%d/%d] %-28s %-10s %6.2f s  %7d kB  %s"
              % (index, total, name,
                 "bv_decide" if row["closed_by"] else outcome,
                 second["wall_seconds"], second["peak_kb"], detail or ""))
    handle = open(os.path.join(HERE, "check_L2.json"), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    tally = {}
    for row in document["rows"]:
        key = row.get("closed_by") or row.get("outcome")
        tally[key] = tally.get(key, 0) + 1
    print("")
    for key in sorted(tally, key=str):
        print("  %-24s %d" % (key, tally[key]))
    return 0


def axioms_gap_command(scope="gap"):
    """some proved theorem files' first `lean_once` run closed the goal
    (exit 0) but the `#print axioms` info trace that same run's output
    should carry was not found by `axiom_line` -- so `row["axioms"]` is
    None even though `row["closed_by"]` names a tactic that succeeded.
    This re-runs `lake env lean` on exactly those already-written files
    (unchanged on disk since the winning tactic was chosen; nothing here
    edits a theorem or writes a new one) and records what the trace
    actually says, so every proved row states its axioms rather than
    leaving the gap silent.

    scope="gap" (the default) touches only rows with no axioms line yet.
    scope="all" re-runs every proved row -- used once, after lane 17's
    probe showed `axiom_line`'s first version silently truncated a
    wrapped multi-line axiom list (61 `bv_decide`-closed rows lost
    `Lean.ofReduceBool` and `Lean.trustCompiler` this way), to refresh
    rows that already held a (truncated) line and so were never in the
    "gap"."""
    document = json.load(open(os.path.join(HERE, "check_L2.json")))
    if scope == "all":
        gap = [row for row in document["rows"] if row.get("closed_by")]
    else:
        gap = [row for row in document["rows"]
               if row.get("closed_by") and not row.get("axioms")]
    total = len(gap)
    print("gap: %d proved theorem(s) missing an axioms line" % total)
    still_missing = 0
    sorry_found = 0
    for index, row in enumerate(gap, 1):
        result = lean_once(row["file"])
        line = axiom_line(result["output"])
        print("[%d/%d] %-28s exit %d  %6.2f s  axioms=%s"
              % (index, total, row["theorem_name"], result["exit"],
                 result["wall_seconds"], line or "STILL MISSING"))
        if result["exit"] != 0:
            print("    re-run did not exit 0 -- full output follows")
            print(result["output"])
        if line:
            row["axioms"] = line
            if "sorryAx" in line:
                sorry_found = sorry_found + 1
        else:
            still_missing = still_missing + 1
    handle = open(os.path.join(HERE, "check_L2.json"), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    print("")
    print("still missing after the re-run: %d" % still_missing)
    print("carrying sorryAx after the re-run: %d" % sorry_found)
    return 0 if (still_missing == 0 and sorry_found == 0) else 1


def axiom_line(output):
    """`#print axioms NAME` prints one of two shapes: "'NAME' depends on
    axioms: [...]" when the proof used at least one, or "'NAME' does not
    depend on any axioms" when it used none at all (a zero-axiom proof --
    the strongest outcome, not a gap). Lane 15's probe of ModelCheck_c_21
    found the second shape on disk and showed the first regex alone was
    why 20 proved rows came back with no axioms line: `rfl` closed those
    theorems with no axiom dependency whatsoever, so the "depends on"
    substring never appeared.

    When the axiom LIST is long -- lane 17's probe of ModelCheck_c_9
    found `bv_decide`-closed theorems naming five axioms, including
    `Lean.ofReduceBool` and `Lean.trustCompiler` alongside the ordinary
    propext/Classical.choice/Quot.sound trio -- Lean wraps it over
    several lines, each continuation indented and ending the block at
    the line holding `]`. Returning only the opening line silently
    dropped `Lean.ofReduceBool` and `Lean.trustCompiler` from 61 rows'
    recorded axioms, which is exactly the kind of gap `#print axioms`
    exists to surface, so this joins every wrapped line up to the
    closing bracket."""
    lines = output.splitlines()
    for index, line in enumerate(lines):
        if "does not depend on any axioms" in line:
            return line.strip()
        if "depends on axioms" in line:
            parts = [line.strip()]
            if "]" not in line:
                cursor = index + 1
                while cursor < len(lines):
                    parts.append(lines[cursor].strip())
                    if "]" in lines[cursor]:
                        break
                    cursor = cursor + 1
            return " ".join(parts)
    return None


def imports_command():
    """the project root file: every module that CLOSED, so `lake build` is a
    build of the proofs rather than of the attempts."""
    document = json.load(open(os.path.join(HERE, "check_L2.json")))
    lines = ["import Archproof.Basic", "import Archproof.Model",
             "import Archproof.Render"]
    kept = 0
    for row in document["rows"]:
        if not row.get("closed_by"):
            continue
        lines.append("import %s" % row["module"])
        kept = kept + 1
    handle = open(os.path.join(HERE, "archproof", "Archproof.lean"), "w")
    handle.write("\n".join(lines) + "\n")
    handle.close()
    print("Archproof.lean imports %d proved check modules" % kept)
    return 0


def one_row(model, maker, row, held, terms, directory):
    out = {"lang": row["lang"], "unit": row["unit"], "mnem": row["mnem"],
           "row_index": row["row_index"],
           "member_count": row["member_count"]}
    record = held.get(row["unit"])
    term_record = terms.get(row["unit"])
    if record is None or term_record is None:
        out["outcome"] = "REFUSED"
        out["cause"] = "NO_STORE_RECORD"
        return out
    if term_record.get("outcome") != "PROVED_ON_SHIP":
        out["outcome"] = "REFUSED"
        out["cause"] = "NO_PROVED_TERM"
        out["detail"] = "term66_store outcome is %r" % \
            term_record.get("outcome")
        return out
    stored = term_record.get("layer5_normalized_text")
    if not stored:
        out["outcome"] = "REFUSED"
        out["cause"] = "NO_LAYER5_TEXT"
        return out
    unit = dict(record)
    unit["unit"] = row["unit"]
    walked = maker.transcribe(unit)
    if walked.refused is not None or walked.out_term is None:
        out["outcome"] = "REFUSED"
        out["cause"] = "NO_TERM_ON_RETRANSCRIPTION"
        out["detail"] = str(walked.refused)
        return out
    reprinted = maker.normalize(walked.out_term)
    if reprinted != stored:
        out["outcome"] = "REFUSED"
        out["cause"] = "LAYER5_REPRINT_MISMATCH"
        out["detail"] = reprinted
        return out
    unit["result_width"] = record.get("result_width")
    unit["result_family"] = record.get("result_family")
    stated = check_one(model, unit, stored, walked.out_term)
    out.update(stated)
    out["unit"] = row["unit"]
    if stated["outcome"] != "STATED":
        return out
    label = ("%s single-opcode row %d, arch mnemonic %r, example unit %s, "
             "%d members" % (row["lang"], row["row_index"], row["mnem"],
                             row["unit"], row["member_count"]))
    stem = "ModelCheck_%s_%d" % (row["lang"], row["row_index"])
    out["theorem_name"] = stem
    out["module"] = "Archproof.%s" % stem
    out["file"] = os.path.join(directory, stem + ".lean")
    handle = open(out["file"], "w")
    handle.write(theorem_text(label, stem, stated, tactic_for(stated, "rfl")))
    handle.close()
    return out


MEMORY_CEILING_KB = 6 * 1024 * 1024
"""THE MEMORY BOUND, and the named abort at it.  This task holds two records
per unit for 259 units and nothing else; the stores themselves are streamed
one shard at a time and dropped.  6 GB is the ceiling at which this process
aborts by name rather than swapping the host, and it is far above what the
sample measured -- the number is a guard, not an expectation."""


def peak_kb():
    import resource
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory():
    peak = peak_kb()
    if peak > MEMORY_CEILING_KB:
        raise SystemExit("ABORT_MEMORY_L2: peak %d kB passed the stated "
                         "ceiling %d kB" % (peak, MEMORY_CEILING_KB))
    return peak


def term66_shard_path(canon40_path):
    """the term66_store counterpart of one canon40 shard path: the same
    basename, prefixed `canon40_regen_store__` for a shard that sits under
    the `canon40_regen_store/` sub-folder."""
    base = os.path.basename(canon40_path)
    parent = os.path.basename(os.path.dirname(canon40_path))
    if parent == "canon40_regen_store":
        base = "canon40_regen_store__" + base
    return os.path.join(OP, "term66_store", base)


def stream_store(needed):
    """the canon40 record and the term66 record for each unit this task
    needs, streaming one shard at a time so no whole store is ever held."""
    import term66_run as TR
    held = {}
    terms = {}
    for path in TR.shards():
        document = json.load(open(path))
        for name, record in document["units"].items():
            if name in needed:
                held[name] = record
        del document
        term_path = term66_shard_path(path)
        if os.path.exists(term_path):
            term_document = json.load(open(term_path))
            for name, record in term_document["units"].items():
                if name in needed:
                    terms[name] = record
            del term_document
        check_memory()
    return held, terms


if __name__ == "__main__":
    sys.exit(main(sys.argv))
