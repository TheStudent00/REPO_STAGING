#!/usr/bin/env python3
"""bitblast.py -- THE BIT-BLAST ROUTE: a cell's term turned into an
and-or-not-xor CIRCUIT by z3 itself, and that circuit written out as one
named local per gate in c, cpp, go and rust.

Node: hq.research.arch_unit_oracle.cross_construction.riscv.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_bb1_brief.md`.

THE OBJECTS, one sentence each, in relation.
  * A CIRCUIT is what `blast` returns: a list of named gates over the
    INPUT BITS of the term's free symbols, every gate one of and, or,
    xor, not or a constant bit, with one name per output bit.  Nobody
    writes an adder, a multiplier or a divider: z3's own
    `Tactic('bit-blast')` does, after `Tactic('simplify')`, and z3 is
    the checker this line already trusts.
  * AN INPUT BIT is one bit of one arrival, `x<k>_<i>`: bit `i` of the
    k-th free symbol of the term the renderer walks.
  * A GATE is one boolean operation over two earlier names (or one, for
    not), named `g<n>`, and the gates are in an order in which every
    name is written before it is read.
  * THE GATE RENDER, `render_gates`, is the ONE thing this task adds to
    the driver: it writes the circuit as a sequence of named locals in
    the target's own spelling and hands back a source of exactly the
    shape `render_general.assemble` already writes, so the compile, the
    carve, the walk and the gate of `rv_general.py` are REUSED
    unchanged and not copied.

WHY A GATE IS A LOCAL OF THE TARGET'S OWN UNSIGNED WORD HOLDING 0 OR 1,
and not a local of the target's boolean holder.  This is a MEASURED
choice and it is recorded rather than assumed.  Go has no conversion
from `bool` to an integer: packing boolean gates into the answer would
need one `if` per output bit, and log_265's own flag says the RISC-V
walk still reads a compiled `if` in text order -- so a boolean-holder
render would have corrupted the very measurement this task exists to
take.  One bit per word, with the target's own `&`, `|`, `^` and `^ 1`,
is branchless in all four languages, is spelled identically in all four,
and is what makes the carved bodies comparable across languages, which
is the thing the owner asked this task to store.

Coding discipline: no compound one-liner statements.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

HOW THIS FILE OBEYS IT.  Nothing here reads a source token or a
mnemonic.  What a node becomes is decided by the z3 declaration KIND of
the blasted boolean node -- machine form -- and by nothing else; the
four operator texts below are OUTPUT SPELLINGS of the target language,
written into the source and never used as a key, a grouping or a
comparison scope.
"""

import os
import sys
import time

import z3

HERE = os.path.dirname(os.path.abspath(__file__))
CONSTRUCT = os.path.normpath(os.path.join(HERE, ".."))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
if CONSTRUCT not in sys.path:
    sys.path.insert(0, CONSTRUCT)

import build as B                                            # noqa: E402
import render_general as RG                                  # noqa: E402


CAUSE_NOT_BITS = ("the bit-blast route is a circuit over BITS and this "
                  "term is not a bit-vector term over bit-vector "
                  "arrivals: z3's bit-blast tactic has nothing to blast "
                  "here")
CAUSE_UNBLASTED = ("z3's bit-blast tactic left a node this file cannot "
                   "read as a gate or as an input bit")
CAUSE_GOAL_SHAPE = ("the blasted goal is not the one formula per output "
                    "bit this file poses")
CAUSE_TOO_MANY = ("the circuit is larger than the number of gates this "
                  "task states, measured before anything is written")
CAUSE_BIT_MISSING = ("an input bit of the circuit sits above the width "
                     "the target's own parameter plan gives that "
                     "arrival")

GATE_CEILING = 200000
"""how many gates one circuit may carry.  It is a MEASURED ceiling on
the thing that is actually written -- one statement per gate -- and it
sits beside `render_general.STATEMENT_CEILING` (400,000) for the same
reason: the cost of this route is the compile of the gate source, and a
source above this is a compile that the carve's own 300-second bound
would refuse anyway, with no row to read."""

OUT_PREFIX = "__bb_o"
"""the name of the boolean this file binds to output bit i before the
blast, so the blasted goal can be read back one output bit at a time."""


# ==================================================================
# section 1: the circuit
# ==================================================================

AND = "and"
OR = "or"
XOR = "xor"
NOT = "not"
CONST = "const"


class Circuit(object):
    """one term as gates over input bits.

    fields:
        width      how many output bits the term has
        symbols    the free symbols' names, in the term's own order
        inputs     (name, symbol index, bit) for every input bit read
        gates      (name, kind, argument names) in write order
        outputs    one name per output bit, low bit first
        gate_count how many gates, which is the task's headline cost
    """

    def __init__(self, width, symbols):
        self.width = width
        self.symbols = list(symbols)
        self.term = None
        self.seconds = None
        self.shape = None
        self.inputs = []
        self.gates = []
        self.outputs = []
        self.input_names = {}
        self.const_names = {}
        self.counter = 0

    def fresh(self):
        name = "g%d" % self.counter
        self.counter = self.counter + 1
        return name

    def input_bit(self, symbol_index, bit):
        key = (symbol_index, bit)
        got = self.input_names.get(key)
        if got is not None:
            return got
        name = "x%d_%d" % (symbol_index, bit)
        self.input_names[key] = name
        self.inputs.append((name, symbol_index, bit))
        return name

    def constant(self, value):
        got = self.const_names.get(value)
        if got is not None:
            return got
        name = "k%d" % value
        self.const_names[value] = name
        self.gates.append((name, CONST, [str(value)]))
        return name

    def gate(self, kind, arguments):
        if len(self.gates) >= GATE_CEILING:
            raise B.Refused(CAUSE_TOO_MANY,
                            "at or above %d gates" % GATE_CEILING)
        name = self.fresh()
        self.gates.append((name, kind, list(arguments)))
        return name

    def as_record(self):
        """the circuit without the z3 objects, for the store."""
        return {
            "width": self.width,
            "symbols": list(self.symbols),
            "gate_count": len(self.gates),
            "input_bits": len(self.inputs),
        }


# ==================================================================
# section 2: reading a blasted node
# ==================================================================

BIT_PREFIX = "x"
"""the name this file gives bit `i` of arrival `k` before the blast:
`x<k>_<i>`, which is also the name the rendered source gives the local
that unpacks it."""


def with_named_bits(term, symbols):
    """(the term with every arrival replaced by ITS OWN NAMED BITS, the
    bit names).

    WHY THE SUBSTITUTION IS HERE AND IS NOT OPTIONAL, measured in lane
    `bb1_l1_the_blast_read_back.sh` step [2/2] on z3 5.1.0.  Handed a
    bit-vector arrival, z3's blaster abstracts each of its bits into a
    FRESH BOOLEAN OF ITS OWN, spelled `k!<n>`, and which arrival and
    which bit that boolean stands for is carried in the goal's model
    CONVERTER and not in the formula.  The lane's own line, LITERAL:

        formula, LITERAL: (= __bb_o0 (not (= k!8 k!0)))

    Reading `k!8` as "bit 0 of the second arrival" would be a guess
    about z3's allocation order.  So the arrivals are handed to the
    blaster ALREADY DECOMPOSED, over booleans this file names, and the
    formula that comes back names them; a `k!` left anywhere in it is
    then a thing this file does not understand and is refused by name."""
    substitution = []
    inputs = {}
    for index, symbol in enumerate(symbols):
        pieces = []
        for bit in reversed(range(symbol.size())):
            name = "%s%d_%d" % (BIT_PREFIX, index, bit)
            inputs[name] = (index, bit)
            pieces.append(z3.If(z3.Bool(name), z3.BitVecVal(1, 1),
                                z3.BitVecVal(0, 1)))
            continue
        if len(pieces) == 1:
            replacement = pieces[0]
        else:
            replacement = z3.Concat(*pieces)
        substitution.append((symbol, replacement))
        continue
    if substitution:
        term = z3.substitute(term, *substitution)
    return term, inputs


def bit_atom(node, inputs):
    """(arrival index, bit) for a node that is one of the booleans this
    file handed the blaster; None where the node is not one."""
    if not z3.is_const(node):
        return None
    if node.decl().kind() != z3.Z3_OP_UNINTERPRETED:
        return None
    return inputs.get(node.decl().name())


def output_index(node):
    """the output bit this boolean names, or None."""
    if not z3.is_const(node):
        return None
    if node.decl().kind() != z3.Z3_OP_UNINTERPRETED:
        return None
    name = node.decl().name()
    if not name.startswith(OUT_PREFIX):
        return None
    return int(name[len(OUT_PREFIX):])


def gate_kind(node):
    """the gate this blasted boolean node is, as a (kind, arity) pair,
    or None where it is a leaf this file must read as an atom.

    Every test below is on the z3 DECLARATION KIND -- machine form."""
    if z3.is_true(node):
        return ("true", 0)
    if z3.is_false(node):
        return ("false", 0)
    kind = node.decl().kind()
    if kind == z3.Z3_OP_AND:
        return (AND, node.num_args())
    if kind == z3.Z3_OP_OR:
        return (OR, node.num_args())
    if kind == z3.Z3_OP_NOT:
        return (NOT, 1)
    if kind == z3.Z3_OP_XOR:
        return (XOR, node.num_args())
    if kind == z3.Z3_OP_IMPLIES:
        return ("implies", node.num_args())
    if kind == z3.Z3_OP_ITE:
        if node.sort().kind() == z3.Z3_BOOL_SORT:
            return ("ite", 3)
        return None
    if kind == z3.Z3_OP_EQ and node.num_args() == 2:
        if node.arg(0).sort().kind() == z3.Z3_BOOL_SORT:
            return ("iff", 2)
        return None
    if kind == z3.Z3_OP_DISTINCT and node.num_args() == 2:
        if node.arg(0).sort().kind() == z3.Z3_BOOL_SORT:
            return (XOR, 2)
        return None
    return None


# ==================================================================
# section 3: the blast
# ==================================================================

def free_symbols_in_order(term):
    """the term's free bit-vector symbols, in the order the pipeline's
    own `term.ordered_symbols` gives them, so an input bit's symbol
    index is the parameter index the renderer plans."""
    import term as T
    return T.ordered_symbols(term)


def refuse_if_not_bits(term):
    """the route's one precondition, stated rather than discovered: the
    term and every arrival are bit-vectors.  A float term is left
    untouched by `Tactic('bit-blast')` and would be refused a hundred
    nodes later with no cause worth reading."""
    if not z3.is_bv(term):
        raise B.Refused(CAUSE_NOT_BITS, "the term is %s" % term.sort())
    for symbol in free_symbols_in_order(term):
        if symbol.sort().kind() != z3.Z3_BV_SORT:
            raise B.Refused(CAUSE_NOT_BITS,
                            "the arrival %s is %s"
                            % (symbol.decl().name(), symbol.sort()))
    stack = [term]
    seen = set()
    while stack:
        node = stack.pop()
        key = node.get_id()
        if key in seen:
            continue
        seen.add(key)
        if z3.is_fp(node) or z3.is_fprm(node):
            raise B.Refused(CAUSE_NOT_BITS,
                            "a node of this term is %s" % node.sort())
        for index in range(node.num_args()):
            stack.append(node.arg(index))
            continue
    return


def blasted_definitions(term):
    """one blasted boolean per output bit of `term`, by z3 and by
    nothing written here.

    TWO SHAPES OF THE SAME QUESTION, in this order.  The first poses
    every output bit in ONE goal, which is one blast for the whole term
    and is what the cost sample measured.  If the goal that comes back
    is not one formula per output bit -- a shape of z3's simplifier and
    not of this task -- the second poses each output bit in a goal of
    its own, where the goal IS the definition and there is nothing to
    read back.  The fallback is exact and slower, never the other way
    round, and which of the two answered is on the circuit."""
    try:
        return whole_goal_definitions(term), "one goal"
    except B.Refused as refusal:
        if refusal.cause != CAUSE_GOAL_SHAPE:
            raise
        return per_bit_definitions(term), "one goal per output bit"


def per_bit_definitions(term):
    """the blast posed once per output bit, so the goal that comes back
    IS the bit's own boolean."""
    tactic = z3.Then(z3.Tactic("simplify"), z3.Tactic("bit-blast"))
    definitions = {}
    for index in range(term.size()):
        goal = z3.Goal()
        goal.add(z3.Extract(index, index, term) == z3.BitVecVal(1, 1))
        applied = tactic(goal)
        if len(applied) == 0:
            definitions[index] = z3.BoolVal(False)
            continue
        if len(applied) != 1:
            raise B.Refused(CAUSE_GOAL_SHAPE,
                            "output bit %d answered %d sub-goals"
                            % (index, len(applied)))
        formulas = list(applied[0])
        if not formulas:
            definitions[index] = z3.BoolVal(True)
            continue
        if len(formulas) == 1:
            definitions[index] = formulas[0]
            continue
        definitions[index] = z3.And(*formulas)
        continue
    return definitions


def whole_goal_definitions(term):
    """every output bit posed in one goal, each bound to a fresh
    boolean, and the blasted goal read back one formula at a time."""
    width = term.size()
    goal = z3.Goal()
    for index in range(width):
        marker = z3.Bool("%s%d" % (OUT_PREFIX, index))
        bit = z3.Extract(index, index, term) == z3.BitVecVal(1, 1)
        goal.add(marker == bit)
        continue
    tactic = z3.Then(z3.Tactic("simplify"), z3.Tactic("bit-blast"))
    applied = tactic(goal)
    if len(applied) != 1:
        raise B.Refused(CAUSE_GOAL_SHAPE,
                        "the tactic answered %d sub-goals" % len(applied))
    blasted = applied[0]
    definitions = {}
    for formula in blasted:
        index, body = one_definition(formula)
        if index in definitions:
            raise B.Refused(CAUSE_GOAL_SHAPE,
                            "output bit %d is bound twice" % index)
        definitions[index] = body
        continue
    for index in range(width):
        if index not in definitions:
            raise B.Refused(CAUSE_GOAL_SHAPE,
                            "output bit %d is bound by no formula"
                            % index)
        continue
    return definitions


def one_definition(formula):
    """(output bit, the boolean it is bound to) for one formula of the
    blasted goal."""
    index = output_index(formula)
    if index is not None:
        return index, z3.BoolVal(True)
    if formula.decl().kind() == z3.Z3_OP_NOT:
        index = output_index(formula.arg(0))
        if index is not None:
            return index, z3.BoolVal(False)
    if formula.decl().kind() == z3.Z3_OP_EQ and formula.num_args() == 2:
        left = output_index(formula.arg(0))
        right = output_index(formula.arg(1))
        if left is not None and right is None:
            return left, formula.arg(1)
        if right is not None and left is None:
            return right, formula.arg(0)
    raise B.Refused(CAUSE_GOAL_SHAPE,
                    "a formula of the blasted goal binds no output bit: "
                    "%s" % formula.sexpr()[:300])


def blast(term):
    """THE ROUTE: one term -> one circuit of named gates over the input
    bits, by z3's own bit-blast tactic after its own simplifier.

    Nothing arithmetic is written by a person anywhere below; the gates
    are z3's and this function only names them."""
    refuse_if_not_bits(term)
    symbols = free_symbols_in_order(term)
    names = []
    for symbol in symbols:
        names.append(symbol.decl().name())
        continue
    started = time.time()
    bitted, inputs = with_named_bits(term, symbols)
    definitions, shape = blasted_definitions(bitted)
    circuit = Circuit(term.size(), names)
    circuit.term = term
    circuit.shape = shape
    memo = {}
    for index in range(term.size()):
        circuit.outputs.append(name_of(circuit, definitions,
                                       definitions[index], memo, inputs))
        continue
    circuit.seconds = round(time.time() - started, 3)
    return circuit


def name_of(circuit, definitions, node, memo, inputs):
    """the circuit name of one blasted boolean, with every node it reads
    named first.  Iterative, because a blasted divide is thirteen
    thousand nodes deep and python's own recursion bound is a thousand."""
    stack = [(node, False)]
    while stack:
        current, expanded = stack.pop()
        key = current.get_id()
        if key in memo:
            continue
        if not expanded:
            alias = output_index(current)
            if alias is not None:
                body = definitions.get(alias)
                if body is None:
                    raise B.Refused(CAUSE_GOAL_SHAPE,
                                    "output bit %d is read and never "
                                    "bound" % alias)
                stack.append((current, True))
                stack.append((body, False))
                continue
            atom = bit_atom(current, inputs)
            if atom is not None:
                memo[key] = circuit.input_bit(atom[0], atom[1])
                continue
            shape = gate_kind(current)
            if shape is None:
                if z3.is_const(current):
                    raise B.Refused(CAUSE_UNBLASTED,
                                    "the blasted goal reads the leaf %s, "
                                    "which is neither a bit this file "
                                    "named nor a gate"
                                    % current.decl().name())
                raise B.Refused(CAUSE_UNBLASTED,
                                "%s" % current.sexpr()[:300])
            stack.append((current, True))
            for position in range(current.num_args()):
                stack.append((current.arg(position), False))
                continue
            continue
        alias = output_index(current)
        if alias is not None:
            memo[key] = memo[definitions[alias].get_id()]
            continue
        memo[key] = built(circuit, current, memo)
        continue
    return memo[node.get_id()]


def built(circuit, node, memo):
    """one blasted node turned into gates of and, or, xor, not and the
    constant bits, and nothing else."""
    shape = gate_kind(node)
    kind = shape[0]
    if kind == "true":
        return circuit.constant(1)
    if kind == "false":
        return circuit.constant(0)
    arguments = []
    for position in range(node.num_args()):
        arguments.append(memo[node.arg(position).get_id()])
        continue
    if kind == NOT:
        return circuit.gate(NOT, arguments)
    if kind in (AND, OR, XOR):
        return chained(circuit, kind, arguments)
    if kind == "implies":
        negated = circuit.gate(NOT, [arguments[0]])
        return chained(circuit, OR, [negated] + arguments[1:])
    if kind == "iff":
        differ = chained(circuit, XOR, arguments)
        return circuit.gate(NOT, [differ])
    if kind == "ite":
        condition = arguments[0]
        negated = circuit.gate(NOT, [condition])
        taken = circuit.gate(AND, [condition, arguments[1]])
        other = circuit.gate(AND, [negated, arguments[2]])
        return circuit.gate(OR, [taken, other])
    raise B.Refused(CAUSE_UNBLASTED, "%s" % node.sexpr()[:300])


def chained(circuit, kind, arguments):
    """an n-ary boolean node as a chain of two-input gates, so every
    gate of the circuit is one operation of the target language."""
    if not arguments:
        if kind == AND:
            return circuit.constant(1)
        return circuit.constant(0)
    running = arguments[0]
    for argument in arguments[1:]:
        running = circuit.gate(kind, [running, argument])
        continue
    return running


# ==================================================================
# section 4: the circuit put back to z3, so the route can be checked
# ==================================================================

def as_term(circuit, symbols):
    """the circuit read back as a z3 bit-vector term over the same
    arrivals.  Used by this file's `verify` command and by nothing in
    the run: the run's own answer is the COMPILED body's, gated against
    the cell's term by `rv_general`."""
    values = {}
    for name, symbol_index, bit in circuit.inputs:
        symbol = symbols[symbol_index]
        values[name] = z3.Extract(bit, bit, symbol) == z3.BitVecVal(1, 1)
        continue
    for name, kind, arguments in circuit.gates:
        if kind == CONST:
            values[name] = z3.BoolVal(arguments[0] == "1")
            continue
        if kind == NOT:
            values[name] = z3.Not(values[arguments[0]])
            continue
        left = values[arguments[0]]
        right = values[arguments[1]]
        if kind == AND:
            values[name] = z3.And(left, right)
        elif kind == OR:
            values[name] = z3.Or(left, right)
        else:
            values[name] = z3.Xor(left, right)
        continue
    pieces = []
    for index in range(circuit.width):
        driver = values[circuit.outputs[index]]
        pieces.append(z3.If(driver, z3.BitVecVal(1, 1),
                            z3.BitVecVal(0, 1)))
        continue
    pieces.reverse()
    if len(pieces) == 1:
        return pieces[0]
    return z3.Concat(*pieces)


def verify(term, milliseconds=10000):
    """(outcome, seconds, counterexample) for "the circuit computes the
    term".  z3's own answer about z3's own blast: it is a check of THIS
    FILE's reading of the blasted goal, not of the tactic."""
    circuit = blast(term)
    symbols = free_symbols_in_order(term)
    rebuilt = as_term(circuit, symbols)
    solver = z3.Solver()
    solver.set("timeout", milliseconds)
    solver.add(rebuilt != term)
    started = time.time()
    answer = solver.check()
    seconds = round(time.time() - started, 3)
    if answer == z3.unsat:
        return "PROVED", seconds, None, circuit
    if answer == z3.sat:
        return "DISPROVED", seconds, "%s" % solver.model(), circuit
    return "UNDECIDED", seconds, None, circuit


# ==================================================================
# section 5: the gate render
# ==================================================================
#
# THE FOUR OPERATOR TEXTS BELOW ARE OUTPUT SPELLINGS, written into the
# rendered source, and are never a key, a grouping or a comparison
# scope.  They are identical in c, cpp, go and rust, over a local of the
# target's own unsigned word holding 0 or 1, which is the whole reason
# this render has one shape and not four.

GATE_TEXT = {
    AND: "(%s & %s)",
    OR: "(%s | %s)",
    XOR: "(%s ^ %s)",
    NOT: "(%s ^ 1)",
}


def word_of(lang, bits):
    """(the target's own unsigned holder of the promoted width, the
    promoted width).  A width the target has no holder for raises the
    target's own refusal, which is the test this file wants."""
    import emulate as E
    promoted = E.promoted_bits(bits)
    if lang == "rust":
        import rust_render as RR
        if promoted not in RR.RU:
            raise E.Refused(E.CAUSE_WIDTH, "%d bits" % promoted)
        return RR.RU[promoted], promoted
    if lang == "go":
        import go_render as GR
        return GR.gu(promoted), promoted
    if promoted not in E.UNSIGNED:
        raise E.Refused(E.CAUSE_WIDTH, "%d bits" % promoted)
    return E.UNSIGNED[promoted], promoted


def local(lang, holder, name, text):
    """one named local of the target's own unsigned word."""
    if lang == "rust":
        return "let %s: %s = %s;" % (name, holder, text)
    if lang == "go":
        return "var %s %s = %s" % (name, holder, text)
    return "%s %s = %s;" % (holder, name, text)


def widened(lang, holder, text):
    """`text` read at the word the gates are held in, in the target's
    own spelling.  Go converts explicitly and never implicitly, so every
    step names its holder; c and rust say the same thing their own way."""
    if lang == "rust":
        return "((%s) as %s)" % (text, holder)
    if lang == "go":
        return "%s(%s)" % (holder, text)
    return "(%s)(%s)" % (holder, text)


def render_gates(circuit, lang, families, home, bits, label, text=""):
    """THE GATE RENDER: one circuit, one target, one source.

    The brief spells this `render_gates(circuit, target)`; the four
    arguments after the target are the PLACE'S OWN CONTRACT, exactly the
    ones `render_general.render` takes -- the arrival families in order,
    the answer home, the answer's width and the label the symbol is
    named after -- because a source with no contract compiles to a body
    no walk can read.

    Returns the record `rv_general.one_attempt` stores: the source, the
    symbol, the gate count, the source line count."""
    import handful as H
    renderer = H.renderer_for(lang, families, home, bits, label)
    renderer.plan_parameters(circuit.term)
    renderer.check_symbols(circuit.term)
    holder, promoted = word_of(lang, bits)
    statements = []

    # -- the arrivals, unpacked one bit at a time ------------------
    for name, symbol_index, bit in circuit.inputs:
        symbol_name = circuit.symbols[symbol_index]
        position = renderer.seed_names.get(symbol_name)
        if position is None:
            raise B.Refused(CAUSE_BIT_MISSING,
                            "%s is not a planned arrival" % symbol_name)
        param = renderer.params[position]
        if bit >= param["bits"]:
            raise B.Refused(CAUSE_BIT_MISSING,
                            "bit %d of %s, whose holder is %d bits"
                            % (bit, symbol_name, param["bits"]))
        read = "(%s >> %d) & 1" % (widened(lang, holder, param["name"]),
                                   bit)
        statements.append((name, local(lang, holder, name, read)))
        continue

    # -- the gates, one named local each ---------------------------
    for name, kind, arguments in circuit.gates:
        if kind == CONST:
            statements.append((name, local(lang, holder, name,
                                           arguments[0])))
            continue
        if kind == NOT:
            body = GATE_TEXT[NOT] % arguments[0]
        else:
            body = GATE_TEXT[kind] % (arguments[0], arguments[1])
        statements.append((name, local(lang, holder, name, body)))
        continue

    # -- the answer, the output bits packed into it ----------------
    packed = None
    counter = 0
    for index in range(circuit.width):
        driver = circuit.outputs[index]
        piece = "(%s << %d)" % (driver, index)
        name = "w%d" % counter
        counter = counter + 1
        if packed is None:
            statements.append((name, local(lang, holder, name, piece)))
        else:
            statements.append((name, local(lang, holder, name,
                                           "%s | %s" % (packed, piece))))
        packed = name
        continue
    if packed is None:
        packed = "w0"
        statements.append((packed, local(lang, holder, packed, "0")))
    made = renderer.answer(packed, "bv", bits)
    return_type = made[0]
    body = made[1]
    if isinstance(body, list):
        answer_lines = list(body)
    else:
        answer_lines = None
    source, symbol = RG.assemble(lang, renderer, label, return_type,
                                 statements, answer_lines, body, text)
    return {
        "source": source,
        "symbol": symbol,
        "renderer": renderer,
        "params": renderer.params,
        "gates": len(circuit.gates),
        "input_bits": len(circuit.inputs),
        "statements": len(statements),
        "source_lines": source.count("\n") + 1,
        "blast_seconds": getattr(circuit, "seconds", None),
    }


# ==================================================================
# section 6: this file run on its own, so the route can be read
# ==================================================================

def say(line):
    sys.stdout.write(line + "\n")
    sys.stdout.flush()


def probe_command():
    """what z3's bit-blast tactic actually hands back, printed, so the
    reading above is evidence and not an assumption."""
    first = z3.BitVec("seed_RDI", 4)
    second = z3.BitVec("seed_RSI", 4)
    whole = first + second
    bitted, named = with_named_bits(whole, [first, second])
    goal = z3.Goal()
    for index in range(4):
        marker = z3.Bool("%s%d" % (OUT_PREFIX, index))
        goal.add(marker == (z3.Extract(index, index, bitted)
                            == z3.BitVecVal(1, 1)))
        continue
    applied = z3.Then(z3.Tactic("simplify"), z3.Tactic("bit-blast"))(goal)
    say("an add at 4 bits, with the arrivals handed over as named bits.")
    say("sub-goals: %d" % len(applied))
    for formula in applied[0]:
        say("  formula, LITERAL: %s" % formula.sexpr()[:400])
        continue
    say("  the bits this file named: %s"
        % ", ".join(sorted(named, key=lambda n: named[n])))
    say("")
    say("THE CIRCUIT SIZES, and the check of this file's reading where "
        "the circuit is small enough to pose")
    say("| what | width | gates | input bits | goal shape | blast s | "
        "check | check s |")
    say("|---|---|---|---|---|---|---|---|")
    cases = []
    for width in (8, 32, 64):
        left = z3.BitVec("seed_RDI", width)
        right = z3.BitVec("seed_RSI", width)
        cases.append(("and", left & right))
        cases.append(("add", left + right))
        cases.append(("shift left", left << right))
        cases.append(("multiply", left * right))
        cases.append(("divide signed", left / right))
        continue
    a = z3.BitVec("seed_RDI", 64)
    b = z3.BitVec("seed_RSI", 64)
    ones = z3.BitVecVal((1 << 64) - 1, 64)
    lowest = z3.BitVecVal(1 << 63, 64)
    zero = z3.BitVecVal(0, 64)
    cases.append(("the lifter's own divide, with its cases",
                  z3.If(b == zero, ones,
                        z3.If(z3.And(a == lowest, b == ones), lowest,
                              a / b))))
    cases.append(("the lifter's own remainder, with its cases",
                  z3.If(b == zero, a,
                        z3.If(z3.And(a == lowest, b == ones), zero,
                              z3.SRem(a, b)))))
    cases.append(("the high half of the signed product",
                  z3.Extract(127, 64,
                             z3.SignExt(64, a) * z3.SignExt(64, b))))
    for name, term in cases:
        started = time.time()
        try:
            circuit = blast(term)
        except B.Refused as refusal:
            say("| %s | %d | refused | %s | | %.3f | | |"
                % (name, term.size(), refusal.detail[:80],
                   time.time() - started))
            continue
        outcome = "not posed"
        seconds = ""
        counter = None
        if len(circuit.gates) <= 2000:
            outcome, seconds, counter, _again = verify(term)
        say("| %s | %d | %d | %d | %s | %s | %s | %s |"
            % (name, term.size(), len(circuit.gates),
               len(circuit.inputs), circuit.shape, circuit.seconds,
               outcome, seconds))
        if counter is not None:
            say("|   counterexample, LITERAL | %s | | | | | | |"
                % counter[:200])
        continue
    return 0


def main():
    command = "probe"
    if len(sys.argv) > 1:
        command = sys.argv[1]
    if command == "probe":
        return probe_command()
    raise SystemExit("unknown command %r" % command)


if __name__ == "__main__":
    sys.exit(main())
