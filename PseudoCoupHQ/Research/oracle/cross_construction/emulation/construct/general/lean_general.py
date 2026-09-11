#!/usr/bin/env python3
"""lean_general.py -- A z3 TERM PRINTED AS LEAN WITH ONE NAMED
INTERMEDIATE PER NODE, so a construction can be STATED as a theorem at
all.

Node: hq.research.compiler_graph.gate.lean (the proof system) and
hq.research.arch_unit_oracle.cross_construction.autopoly (the tier).
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_t4_brief.md`.

WHY THIS FILE EXISTS, and it is task t2's own owed item, written out in
`construct/lean/OWED.md` section 3: "a theorem's statement is the term
WRITTEN OUT, a printed term names no intermediate, and restoring
division reads its own previous remainder three times per step -- so the
statement grows like 3^width".  t2 recorded what was owed as "a way to
STATE it -- a translation to Lean that names intermediates (`let`),
which `op_pipeline/lean/term_to_lean.py` does not do today and which is
not this task's file to change".  This file is that translation, written
beside the tier it serves and touching nothing under `op_pipeline`.

THE OBJECTS, one sentence each, in relation.
  * A NAMED INTERMEDIATE is `let t17 : BitVec 64 := t16 ^^^ t9` -- one
    Lean binding per DISTINCT node of the term, so a node read three
    times is written once.
  * THE TWO FORMS a theorem may be stated in are `let` (the bindings
    inside the goal) and `written out` (the term printed whole, which is
    what task t2's lemmas do and what only small terms can carry); they
    are tried in that order and the row records which one the theorem
    was stated in.
  * THE LEAN SPELLINGS ARE THE PROJECT'S OWN, read off
    `op_pipeline/lean/term_to_lean.lean_of` -- `&&& ||| ^^^ ~~~`,
    `.extractLsb`, `.zeroExtend`, `.signExtend`, `++`, `.ult`, `.sle`,
    `.sdiv`, `.srem`, `.smod`, `.sshiftRight'` -- so a theorem here and
    a theorem there are in one language.  The difference is that this
    file walks the z3 NODE and that one parses printed text.

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

HOW THIS FILE OBEYS IT.  Every branch below is on a z3 DECLARATION KIND.
The Lean text it writes is the printed form of a node and is a display
label on it -- it keys nothing, groups nothing and selects nothing.

Coding discipline: no compound one-liner statements.
"""

import z3


class Refused(Exception):
    """this term cannot be stated in Lean by this file; `cause` names
    which node and why."""

    def __init__(self, cause, detail=""):
        Exception.__init__(self, "%s: %s" % (cause, detail))
        self.cause = cause
        self.detail = detail


CAUSE_NO_LEAN_FORM = "no Lean form is written here for a node of this kind"
CAUSE_FLOAT = ("a float node: Lean's `BitVec` carries no float "
               "operation, and the float obligations are z3's alone in "
               "this task")
CAUSE_SYMBOLIC_ROTATE = ("a rotate by a SYMBOLIC amount: Lean's "
                         "`BitVec.rotateLeft` takes a `Nat` and there "
                         "is no bit-vector-amount form to state it "
                         "against")


# ==================================================================
# section 1: one node, printed over its children's Lean texts
# ==================================================================

def is_a_leaf(node):
    kind = node.decl().kind()
    if z3.is_const(node) and kind == z3.Z3_OP_UNINTERPRETED:
        return True
    if kind in (z3.Z3_OP_BNUM, z3.Z3_OP_TRUE, z3.Z3_OP_FALSE):
        return True
    return False


def leaf_text(node):
    kind = node.decl().kind()
    if kind == z3.Z3_OP_BNUM:
        return "(%d#%d)" % (node.as_long(), node.size())
    if kind == z3.Z3_OP_TRUE:
        return "true"
    if kind == z3.Z3_OP_FALSE:
        return "false"
    return node.decl().name()


BINARY_INFIX = {
    z3.Z3_OP_BADD: "+",
    z3.Z3_OP_BSUB: "-",
    z3.Z3_OP_BMUL: "*",
    z3.Z3_OP_BAND: "&&&",
    z3.Z3_OP_BOR: "|||",
    z3.Z3_OP_BXOR: "^^^",
    z3.Z3_OP_BSHL: "<<<",
    z3.Z3_OP_BLSHR: ">>>",
    z3.Z3_OP_BUDIV: "/",
    z3.Z3_OP_BUDIV_I: "/",
    z3.Z3_OP_BUREM: "%",
    z3.Z3_OP_BUREM_I: "%",
}

METHOD_FORM = {
    z3.Z3_OP_BSDIV: "sdiv",
    z3.Z3_OP_BSDIV_I: "sdiv",
    z3.Z3_OP_BSREM: "srem",
    z3.Z3_OP_BSREM_I: "srem",
    z3.Z3_OP_BSMOD: "smod",
    z3.Z3_OP_BSMOD_I: "smod",
    z3.Z3_OP_BASHR: "sshiftRight'",
    z3.Z3_OP_ULT: "ult",
    z3.Z3_OP_ULEQ: "ule",
    z3.Z3_OP_SLT: "slt",
    z3.Z3_OP_SLEQ: "sle",
}

FLIPPED_METHOD = {
    z3.Z3_OP_UGT: "ult",
    z3.Z3_OP_UGEQ: "ule",
    z3.Z3_OP_SGT: "slt",
    z3.Z3_OP_SGEQ: "sle",
}


def node_text(node, children):
    """one node as Lean, over its children's own texts."""
    decl = node.decl()
    kind = decl.kind()
    if z3.is_fp(node) or z3.is_fprm(node):
        raise Refused(CAUSE_FLOAT, decl.name())
    if kind in BINARY_INFIX:
        text = children[0]
        for other in children[1:]:
            text = "(%s %s %s)" % (text, BINARY_INFIX[kind], other)
            continue
        return text
    if kind in METHOD_FORM:
        return "(%s.%s %s)" % (children[0], METHOD_FORM[kind],
                               children[1])
    if kind in FLIPPED_METHOD:
        return "(%s.%s %s)" % (children[1], FLIPPED_METHOD[kind],
                               children[0])
    if kind == z3.Z3_OP_BNOT:
        return "(~~~%s)" % children[0]
    if kind == z3.Z3_OP_BNEG:
        return "(-%s)" % children[0]
    if kind == z3.Z3_OP_NOT:
        return "(!%s)" % children[0]
    if kind == z3.Z3_OP_EQ:
        return "(%s == %s)" % (children[0], children[1])
    if kind == z3.Z3_OP_DISTINCT:
        return "(!(%s == %s))" % (children[0], children[1])
    if kind == z3.Z3_OP_IFF:
        return "(%s == %s)" % (children[0], children[1])
    if kind == z3.Z3_OP_AND:
        return "(" + " && ".join(children) + ")"
    if kind == z3.Z3_OP_OR:
        return "(" + " || ".join(children) + ")"
    if kind == z3.Z3_OP_XOR:
        return "(!(%s == %s))" % (children[0], children[1])
    if kind == z3.Z3_OP_IMPLIES:
        return "((!%s) || %s)" % (children[0], children[1])
    if kind == z3.Z3_OP_ITE:
        return "(if %s = true then %s else %s)" % (children[0],
                                                   children[1],
                                                   children[2])
    if kind == z3.Z3_OP_EXTRACT:
        high = decl.params()[0]
        low = decl.params()[1]
        return "(%s.extractLsb %d %d)" % (children[0], high, low)
    if kind == z3.Z3_OP_ZERO_EXT:
        return "(%s.zeroExtend %d)" % (children[0], node.size())
    if kind == z3.Z3_OP_SIGN_EXT:
        return "(%s.signExtend %d)" % (children[0], node.size())
    if kind == z3.Z3_OP_CONCAT:
        text = children[0]
        for other in children[1:]:
            text = "(%s ++ %s)" % (text, other)
            continue
        return text
    if kind == z3.Z3_OP_ROTATE_LEFT:
        return "(%s.rotateLeft %d)" % (children[0], decl.params()[0])
    if kind == z3.Z3_OP_ROTATE_RIGHT:
        return "(%s.rotateRight %d)" % (children[0], decl.params()[0])
    if kind in (z3.Z3_OP_EXT_ROTATE_LEFT, z3.Z3_OP_EXT_ROTATE_RIGHT):
        raise Refused(CAUSE_SYMBOLIC_ROTATE, decl.name())
    raise Refused(CAUSE_NO_LEAN_FORM,
                  "%s at %s" % (decl.name(), node.sort()))


# ==================================================================
# section 2: the whole term, in the two forms
# ==================================================================

def holder_of(node):
    sort = node.sort()
    if sort.kind() == z3.Z3_BV_SORT:
        return "BitVec %d" % node.size()
    if sort.kind() == z3.Z3_BOOL_SORT:
        return "Bool"
    raise Refused(CAUSE_NO_LEAN_FORM, "a node of sort %s" % sort)


def ordered_nodes(term):
    """every distinct node of the term, leaves first."""
    order = []
    seen = set()
    stack = [(term, False)]
    while stack:
        node, expanded = stack.pop()
        key = node.get_id()
        if expanded:
            order.append(node)
            continue
        if key in seen:
            continue
        seen.add(key)
        stack.append((node, True))
        for index in range(node.num_args()):
            stack.append((node.arg(index), False))
            continue
        continue
    return order


def free_symbols(term):
    """the term's own free symbols, with their Lean holders, in the
    order their names sort numerically."""
    found = {}
    for node in ordered_nodes(term):
        if not is_a_leaf(node):
            continue
        if node.decl().kind() != z3.Z3_OP_UNINTERPRETED:
            continue
        found[node.decl().name()] = holder_of(node)
        continue
    return found


def written_out(term):
    """the term as ONE Lean expression, every node printed where it is
    read -- task t2's own form, and the one whose size is the reason
    this file exists."""
    texts = {}
    for node in ordered_nodes(term):
        if is_a_leaf(node):
            texts[node.get_id()] = leaf_text(node)
            continue
        children = []
        for index in range(node.num_args()):
            children.append(texts[node.arg(index).get_id()])
            continue
        texts[node.get_id()] = node_text(node, children)
        continue
    return texts[term.get_id()]


def let_form(term, prefix="t"):
    """the term as a Lean `let` chain: one binding per distinct node,
    the last line the root's own name."""
    texts = {}
    lines = []
    counter = [0]

    def fresh():
        name = "%s%d" % (prefix, counter[0])
        counter[0] = counter[0] + 1
        return name

    for node in ordered_nodes(term):
        if is_a_leaf(node):
            texts[node.get_id()] = leaf_text(node)
            continue
        children = []
        for index in range(node.num_args()):
            children.append(texts[node.arg(index).get_id()])
            continue
        body = node_text(node, children)
        name = fresh()
        lines.append("let %s : %s := %s" % (name, holder_of(node), body))
        texts[node.get_id()] = name
        continue
    root = texts[term.get_id()]
    if not lines:
        return root, 0
    return "\n      ".join(lines + [root]), len(lines)


def theorem(name, term_left, term_right, form):
    """one theorem file's whole text.

    `form` is "let" or "written out"; the left side -- the operation --
    is always written out, because it is one node over its arguments."""
    widths = dict(free_symbols(term_left))
    widths.update(free_symbols(term_right))
    binders = []
    for symbol in sorted(widths, key=sort_key):
        binders.append("(%s : %s)" % (symbol, widths[symbol]))
        continue
    left = written_out(term_left)
    if form == "let":
        right, bindings = let_form(term_right)
        right = "(%s)" % right
    else:
        right = written_out(term_right)
        bindings = 0
    lines = ["-- generated by construct/general/run_lemmas_t4.py from "
             "construct/general/build.py itself",
             "import Std.Tactic.BVDecide", ""]
    lines.append("theorem %s %s :" % (name, " ".join(binders)))
    lines.append("    %s =" % left)
    lines.append("      %s := by" % right)
    lines.append("  bv_decide")
    return "\n".join(lines) + "\n", bindings


def sort_key(symbol):
    digits = "".join(letter for letter in symbol if letter.isdigit())
    if digits:
        return (0, int(digits), symbol)
    return (1, 0, symbol)
