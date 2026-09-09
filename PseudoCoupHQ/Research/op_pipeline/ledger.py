#!/usr/bin/env python3
"""ledger.py -- THE PROVENANCE LEDGER.

Node: `hq.research.compiler_graph.ledger`
CORE: Planning/node_0_3_research/node_0_3_5_compiler_graph/
      node_0_3_5_3_ledger/CORE_0_3_5_3_ledger.md
Sub-nodes realized here: `row` (class Row), `producer` (class
Producer), `destination_rules` (DESTINATION_RULES), `flag_rules`
(FLAG_RULES); the unrealized entries `rows` and `walk_dataflow` are the
attribute and the method of class Ledger, as the CORE's register says.

TASK 59, round 12 (log_158).  Binding rule 1 of the round: the code
carries the node's name.  This module therefore IMPORTS NOTHING FROM
`ledger47.py` OR `ledger48.py`.  Those two are superseded records: they
are never edited and never imported.  EVERY PART OF THEM THAT IS
UNCHANGED IS COPIED HERE VERBATIM, and every copied part carries a
header line saying which file it was copied from and that it is
unchanged.  What is NOT copied is listed at the end of this docstring.

--------------------------------------------------------------------
WHAT IS NEW HERE, AND NOTHING ELSE
--------------------------------------------------------------------

(a) `sbb` and `adc` ARE MODELLED AS FLAG SETTERS (FLAG_RULES rule 7).

    Until now these two opcodes took the ordinary rule: one value row,
    and `last_flag_row` pointed AT THAT VALUE ROW.  A following `setl`
    or `jb` therefore linked to a row typed `8-byte general value`,
    which carries no flag state at all, and the reference had nothing
    to read.  That is the hole log_153 §4.2 measured -- 699 units moved
    from proved to no-term when the flag link was made honest.

    The model, stated: `sbb` and `adc` are BOTH a flag READER and a
    flag SETTER.  They read the CARRY the previous setter left, and
    they set flags from their own arithmetic.  So each one now writes
    TWO rows, exactly as the destination table's two-destination
    opcodes do:

        the value row   type `8-byte general value` (or the operand's
                        own width), written_half "the difference" for
                        `sbb` and "the sum" for `adc`
        the flags row   type `flags only`, written_half "the flags",
                        and it is this row that becomes the flag state
                        a following flag reader links to

    Both rows read the SAME operands, and the carry-in row -- the row
    that set the flags this opcode reads -- is their FIRST operand,
    which is the same shape flag_rules rule 4 already gives a reader.
    Where no flag-setting opcode precedes, the walk records a hole by
    name rather than pretending a carry-in exists.

    The ledger's job here is the LINEAGE, not the term: with the flags
    row present and its operands named, `reference.py` (node
    0_3_5_4, task 57) has something to build a term from.  Whether a
    given unit then proves is task 58's answer, not this file's claim.

    Recorded in the tree first, as round 12's binding rule 2 requires:
    CORE_0_3_5_3_4_flag_rules.md `## design` rule 7 and its settled
    rules, 2026-09-03, with this file named as the realization.

(b) `call` INTO THE COMPILER'S OWN RUNTIME IS A DESTINATION RULE, and
    the producer kind `runtime_callee` is real.

    the owner, 2026-09-03: "if its within the compiler, its not a library
    call.  if the compiler is importing something as a standard
    feature, also not a library call."  That ruling supersedes the
    verdict in `out_of_scope_library_calls.json` (its list of 308
    units stands; the supersession is written as the NEW file
    `out_of_scope_library_calls_superseded.json`, and the recorded
    file is not edited).  So the destination table gains the rule
    log_152 §9.2 put to the owner and log_153 §3.4 declined to invent: a
    transfer to a routine of the compiler's own runtime WRITES THE
    ACCUMULATOR, and the row it writes is produced by
    `{"kind": "runtime_callee", "callee": ...}`.

    WHICH names are runtime routines is not a list this file believes
    in.  It is machine-form evidence: `runtime_callee.py` asks each
    toolchain where its own archive is and reads that archive's own
    symbol index.  This file takes the answer as a set handed in, and
    when none is handed in the rule does not fire and a `call` is left
    exactly as it was.

(c) EVERYTHING ELSE IS COPIED UNCHANGED, section by section, with the
    source named on each section.

WHAT IS NOT COPIED, and why:
  * ledger47's six-block `BLOCK_ORDER`, its `walk_dataflow`, its
    last-named-operand destination rule, its `jmp`-as-flag-reader and
    its bare-string producers.  All superseded by ledger48 (log_152),
    and the superseding forms are what is copied.
  * ledger48's module-level `import ledger47 as L47` re-export block.
    Its twenty names are DEFINED here instead, which is what "imports
    nothing from ledger47/48" means.

--------------------------------------------------------------------
THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation).  No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns.  The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label
on the member.  HISTORY OF VIOLATIONS, so the pattern is visible: (1)
the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25
-- the fix brief itself reintroduced it as "same-operator pairs").
MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste
this paragraph verbatim."

No operator token appears in this file as a key, a grouping, a pairing
or a row structure.  Every mnemonic sits under `mnem` and every
runtime routine name under `callee`, which are this codebase's
ratified machine-form fields.

Coding discipline: no compound one-liner statements.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                     # noqa: E402
import canon33_gate as G33                                       # noqa: E402
import region36 as R36                                           # noqa: E402


# ==================================================================
# COPIED UNCHANGED from ledger47.py -- the refusal, the fixed pool,
# the ledger symbol and the entry size.
# ==================================================================

LEDGER_SYMBOL = "ledger"
LEDGER_ENTRY_SIZE = 8

SCRATCH_POOL = ["r11", "r10", "rax", "rcx", "rdx", "rsi", "rdi",
                "r8", "r9", "rbx", "r12", "r13", "r14", "r15"]


class Refusal(Exception):
    """refused BY NAME, never silently."""

    def __init__(self, cause, detail):
        Exception.__init__(self, detail)
        self.cause = cause
        self.detail = detail


# ==================================================================
# COPIED UNCHANGED from ledger47.py -- reading a body, register
# families, scratch selection, alignment, immediates.
# ==================================================================

PURE_WRITE_MNEMONICS = frozenset([
    "mov", "movl", "movq", "movb", "movw", "movabs",
    "movzbl", "movzwl", "movzbq", "movzwq", "movsbl", "movswl",
    "movsbq", "movswq", "movslq", "movsbw", "movzbw",
    "lea", "movss", "movsd", "movaps", "movapd", "movdqa", "movdqu",
    "movd", "set", "xorps", "pxor",
])

SIZE_SUFFIX = ("b", "w", "l", "q")

IMMEDIATE = re.compile(r"^\$(-?0x[0-9a-fA-F]+|-?\d+)$")
SETCC = re.compile(r"^set[a-z]+$")
JCC = re.compile(r"^j[a-z]+$")
CMOVCC = re.compile(r"^cmov[a-z]+$")


def split_lines(text):
    return R36.split_lines(text)


def operands_of(line):
    return R36.operands_of(line, G33.split_operands)


def mnemonic_of(line):
    return R36.mnemonic_of(line)


def family_of_operand(operand):
    if not operand.startswith("%"):
        return None
    return canon.FAMILY_OF.get(operand[1:])


def is_vector_family(family):
    if family is None:
        return False
    return family.startswith("xmm")


def register_text(family, width):
    """the spelling of `family` at `width` bits."""
    if is_vector_family(family):
        return "%" + family
    index = {64: 0, 32: 1, 16: 2, 8: 3}.get(width)
    if index is None:
        index = 0
    return "%" + R36.widened(family, index)


def pick_scratch(reserved):
    for family in SCRATCH_POOL:
        if family in reserved:
            continue
        return family
    raise Refusal(
        "no scratch register",
        "every family of the fixed pool is reserved by this unit, so "
        "the form has no register to hold a block base in")


def align_up(value, alignment):
    if alignment <= 1:
        return value
    remainder = value % alignment
    if remainder == 0:
        return value
    return value + (alignment - remainder)


def immediate_value(operand):
    hit = IMMEDIATE.match(operand)
    if hit is None:
        return None
    text = hit.group(1)
    if text.startswith("-0x"):
        return -int(text[3:], 16)
    if text.startswith("0x"):
        return int(text, 16)
    return int(text, 10)


def weave(body, prelude, epilogue):
    """COPIED UNCHANGED from ledger47.py.  The wrapped text: the
    prelude ahead of the first executable instruction, the epilogue
    immediately before every `ret`."""
    first = None
    for index, line in enumerate(body):
        if line.endswith(":"):
            continue
        first = index
        break
    if first is None:
        raise Refusal("no executable instruction",
                      "the body carries no executable instruction")
    returns = 0
    for line in body:
        if line == "ret":
            returns = returns + 1
    if returns == 0:
        raise Refusal("never returns",
                      "the body never returns, so the answer has no "
                      "place to be stored")
    out = []
    for index, line in enumerate(body):
        if index == first:
            out.extend(prelude)
        if line == "ret":
            out.extend(epilogue)
        out.append(line)
    return out, returns


# ==================================================================
# COPIED UNCHANGED from ledger48.py -- the eight-block order and the
# ledger's own two-step addressing.
# ==================================================================

BLOCK_ORDER = ("IN", "CONST", "TEMP", "OWN", "STACK", "X87", "GUARD",
               "OUT")
LEDGER_ENTRIES = len(BLOCK_ORDER)
LEDGER_BYTES = LEDGER_ENTRY_SIZE * LEDGER_ENTRIES

ROW_TEXT = re.compile(r"^(IN|CONST|TEMP|OWN|STACK|X87|GUARD|OUT)-(\d+)$")


def ledger_entry_index(block):
    return BLOCK_ORDER.index(block)


def ledger_entry_offset(block):
    return LEDGER_ENTRY_SIZE * ledger_entry_index(block)


def ledger_entry_text(block):
    return "%s+0x%02x(%%rip)" % (LEDGER_SYMBOL, ledger_entry_offset(block))


def row_text(block, index):
    return "%s-%d" % (block, index)


def is_row_text(text):
    return ROW_TEXT.match(text) is not None


def parse_row_text(text):
    hit = ROW_TEXT.match(text)
    if hit is None:
        return None
    return hit.group(1), int(hit.group(2))


# ==================================================================
# THE `producer` SUB-NODE -- class Producer
#
# COPIED from ledger48.py's `producer_object` / `opcode_producer` and
# given the class shape the CORE names, plus ONE new kind:
# `runtime_callee`, whose second field is `callee` rather than `mnem`
# because what produced the value is a ROUTINE, not a mnemonic.  That
# third field is written into
# CORE_0_3_5_3_2_producer.md before it is written here (round 12
# binding rule 2), with log_158 TASK 59 as the provenance.
# ==================================================================

NON_OPCODE_PHRASES = (
    "arrival",
    "the body's own immediate operand",
    "the body's own stack displacement",
    "the body's last write to",
    "a value the machine stack held before this unit was entered",
    "an x87 stack position this unit did not itself load",
)

PRODUCER_KINDS = ("arch_opcode", "flag_pair", "non_opcode_phrase",
                  "runtime_callee")


class Producer(object):
    """what made a row's value: a TYPED OBJECT, never a bare string.

    attributes:
        kind    arch_opcode / flag_pair / non_opcode_phrase /
                runtime_callee
        mnem    the machine mnemonic, or for a flag_pair the two
                mnemonics of setter and reader; absent for the two
                kinds that name no mnemonic
    """

    def __init__(self, kind, mnem=None, phrase=None, callee=None,
                 writes_which_half=None):
        if kind not in PRODUCER_KINDS:
            raise Refusal("unknown producer kind",
                          "the ledger was handed the producer kind %r"
                          % kind)
        self.kind = kind
        self.mnem = mnem
        self.phrase = phrase
        self.callee = callee
        self.writes_which_half = writes_which_half

    def as_dict(self):
        out = {"kind": self.kind}
        if self.mnem is not None:
            out["mnem"] = self.mnem
        if self.phrase is not None:
            out["phrase"] = self.phrase
        if self.callee is not None:
            out["callee"] = self.callee
        if self.writes_which_half is not None:
            out["writes_which_half"] = self.writes_which_half
        return out

    # ---- the four kinds, each built by name -----------------------
    @classmethod
    def arch_opcode(cls, mnemonic, writes_which_half=None):
        return cls("arch_opcode", mnem=str(mnemonic),
                   writes_which_half=writes_which_half)

    @classmethod
    def flag_pair(cls, setter, reader):
        return cls("flag_pair", mnem=[str(setter), str(reader)])

    @classmethod
    def non_opcode_phrase(cls, phrase):
        return cls("non_opcode_phrase", phrase=str(phrase))

    @classmethod
    def runtime_callee(cls, callee):
        return cls("runtime_callee", callee=str(callee))

    @classmethod
    def of(cls, producer):
        """COPIED from ledger48.producer_object: anything already
        shaped is passed through, a list becomes the flag pair, a
        recorded phrase becomes the phrase kind, anything else is a
        mnemonic."""
        if isinstance(producer, Producer):
            return producer
        if isinstance(producer, dict):
            kind = producer.get("kind")
            return cls(kind,
                       mnem=producer.get("mnem"),
                       phrase=producer.get("phrase"),
                       callee=producer.get("callee"),
                       writes_which_half=producer.get(
                           "writes_which_half"))
        if isinstance(producer, list):
            return cls("flag_pair",
                       mnem=[str(one) for one in producer])
        text = str(producer)
        for phrase in NON_OPCODE_PHRASES:
            if text.startswith(phrase):
                return cls("non_opcode_phrase", phrase=text)
        return cls("arch_opcode", mnem=text)


def producer_object(producer):
    """the producer as the machine-form dict the artifacts carry."""
    return Producer.of(producer).as_dict()


# ==================================================================
# THE `destination_rules` SUB-NODE -- DESTINATION_RULES
#
# COPIED UNCHANGED from ledger48.py, with ONE entry added: the
# transfer into the compiler's own runtime (see the module docstring,
# (b)).  ACCUMULATOR is the %rax family, DATA REGISTER the %rdx family.
# ==================================================================

ACCUMULATOR = "rax"
DATA_REGISTER = "rdx"

DESTINATION_RULES = {
    "idiv": {
        "writes": [(ACCUMULATOR, "quotient"),
                   (DATA_REGISTER, "remainder")],
        "reads_implicitly": [ACCUMULATOR, DATA_REGISTER],
        "named_operands_are": "all read",
        "only_when_operand_count_is": None,
        "why": "this opcode divides the value held in the data "
               "register and the accumulator together by the operand "
               "it names, and leaves the quotient in the accumulator "
               "and the remainder in the data register; it names "
               "neither destination",
    },
    "div": {
        "writes": [(ACCUMULATOR, "quotient"),
                   (DATA_REGISTER, "remainder")],
        "reads_implicitly": [ACCUMULATOR, DATA_REGISTER],
        "named_operands_are": "all read",
        "only_when_operand_count_is": None,
        "why": "as idiv, without the sign",
    },
    "mul": {
        "writes": [(ACCUMULATOR, "low half"),
                   (DATA_REGISTER, "high half")],
        "reads_implicitly": [ACCUMULATOR],
        "named_operands_are": "all read",
        "only_when_operand_count_is": 1,
        "why": "the one-operand form multiplies the accumulator by "
               "the operand it names and leaves the low half in the "
               "accumulator and the high half in the data register",
    },
    "imul": {
        "writes": [(ACCUMULATOR, "low half"),
                   (DATA_REGISTER, "high half")],
        "reads_implicitly": [ACCUMULATOR],
        "named_operands_are": "all read",
        "only_when_operand_count_is": 1,
        "why": "the ONE-OPERAND form only: the two- and three-operand "
               "forms name their destination and are left to the "
               "ordinary rule",
    },
    "cltd": {
        "writes": [(DATA_REGISTER, "the sign of the accumulator")],
        "reads_implicitly": [ACCUMULATOR],
        "named_operands_are": "all read",
        "only_when_operand_count_is": 0,
        "why": "spreads the sign of the accumulator's low 32 bits "
               "through the data register; it names no operand at "
               "all, so ledger47's walk skipped it entirely",
    },
    "cqto": {
        "writes": [(DATA_REGISTER, "the sign of the accumulator")],
        "reads_implicitly": [ACCUMULATOR],
        "named_operands_are": "all read",
        "only_when_operand_count_is": 0,
        "why": "as cltd, at 64 bits",
    },
    "cwtl": {
        "writes": [(ACCUMULATOR, "the widened accumulator")],
        "reads_implicitly": [ACCUMULATOR],
        "named_operands_are": "all read",
        "only_when_operand_count_is": 0,
        "why": "widens the accumulator's low 16 bits to 32, in place",
    },
    "cltq": {
        "writes": [(ACCUMULATOR, "the widened accumulator")],
        "reads_implicitly": [ACCUMULATOR],
        "named_operands_are": "all read",
        "only_when_operand_count_is": 0,
        "why": "widens the accumulator's low 32 bits to 64, in place",
    },
    "cbtw": {
        "writes": [(ACCUMULATOR, "the widened accumulator")],
        "reads_implicitly": [ACCUMULATOR],
        "named_operands_are": "all read",
        "only_when_operand_count_is": 0,
        "why": "widens the accumulator's low 8 bits to 16, in place",
    },
}

# The one entry ADDED this lap.  It is not keyed by the transfer's
# mnemonic in the table above, because it applies only when the callee
# is a routine the toolchain's OWN archive defines -- machine-form
# evidence, decided by `runtime_callee.py`, never by the name's
# spelling.
RUNTIME_TRANSFER_RULE = {
    "writes": "every register family the ATTACHED CALLEE's own body "
              "changes, one row per family, read off that body by "
              "`answer_registers_of_body`",
    "reads_implicitly": [],
    "named_operands_are": "the callee",
    "why": "a transfer into a routine the compiler ships as its own "
           "lowering leaves that routine's answers where the "
           "routine's own body puts them; the body is attached as a "
           "further arch unit the caller references (node "
           "arch_unit.runtime_callee) and it is READ, never asserted",
    "ruling": "the owner, 2026-09-03: \"if its within the compiler, its not "
              "a library call.\"  log_158 TASK 59.  The register and "
              "the row COUNT corrected by task 78 against log_168 "
              "§5.3's 2,862 units; CORE_0_3_5_3_3_destination_rules "
              "`## design` rule 4 and its settled rule.",
    "superseded_wording": "a transfer into the compiler's OWN runtime "
                          "writes the accumulator, and the row it "
                          "writes is produced by {\"kind\": "
                          "\"runtime_callee\", \"callee\": ...} -- one "
                          "row, on %rax.  Wrong twice: wrong register "
                          "for every float lowering, and one row "
                          "where the body writes several places.",
}

TRANSFER_STEMS = frozenset(["call", "callq"])

# the positional branch labels the label pass writes (ruling 4)
POSITIONAL_LABEL = re.compile(r"^L\d+$")


# ==================================================================
# THE ATTACHED CALLEE'S OWN ANSWER REGISTERS, READ OFF ITS BODY
#
# Written into CORE_0_3_5_3_3_destination_rules.md first (the settled
# rule "THE ANSWER REGISTERS ARE READ OFF THE ATTACHED CALLEE'S BODY",
# 2026-09-03, task 78), then here.  The six steps of that rule are the
# six things this section does, in its order.
# ==================================================================

# %rsp, %rbp and %rip are excluded from the answer set for the same
# reason the walk never makes rows for them.
ANSWER_EXCLUDED = canon.NEVER_RENAME

MOVE_LIKE = frozenset([
    "mov", "movq", "movd", "movl", "movb", "movw", "movabs",
    "movaps", "movapd", "movdqa", "movdqu", "movups", "movupd",
    "movss", "movsd",
])

X87_PUSHERS = ("fld", "fild", "fbld")
X87_POPPERS = ("fstp", "fistp", "fbstp", "fucompp", "faddp", "fsubp",
               "fsubrp", "fmulp", "fdivp", "fdivrp", "fucomip",
               "fcomip", "fcompp")

RETURN_STEMS = frozenset(["ret", "retq", "repz", "repz retq"])


def _memory_slot(operand, delta):
    """the tracked stack slot an operand names, or None.

    Only stack-pointer-relative memory is tracked, and only while the
    depth is still known.  Anything else is memory this reading does
    not model, which is why a load from it yields a fresh token."""
    if "(" not in operand:
        return None
    head, _, tail = operand.partition("(")
    base = tail.rstrip(")")
    if base != "%rsp":
        return None
    if head == "":
        displacement = 0
    else:
        displacement = immediate_value(head)
        if displacement is None:
            try:
                displacement = int(head, 0)
            except ValueError:
                return None
    return delta + displacement


def answer_registers_of_body(lines, resolve=None, seen=None):
    """the register families an attached callee's OWN body changes.

    Returns a dict with `families` (a list of family names in the
    order of their last change), `x87` (True when the body leaves a
    value on the x87 stack), `tail_transfer`, `unresolved_transfers`
    and `how`; or a dict with `refuse` naming why the reading cannot
    be made.

    `resolve` is called with a routine name and returns that routine's
    own reading, so a body that ends in an unconditional transfer to
    another routine of the same archive takes that routine's families
    as well.  `seen` is the cycle guard.
    """
    if seen is None:
        seen = set()
    state = {}
    slots = {}
    delta = 0
    depth_known = True
    order = {}
    step = 0
    x87_depth = 0
    saw_return = False
    tail_transfer = None
    unresolved = []
    last_executable = None

    def token_of(operand):
        family = family_of_operand(operand)
        if family is not None:
            return state.get(family, ("entry", family))
        slot = _memory_slot(operand, delta)
        if slot is None:
            return ("computed", step)
        if not depth_known:
            return ("computed", step)
        return slots.get(slot, ("computed", step))

    saved_entry = set()
    x87_at_returns = []

    def park(token):
        """a value put on the machine stack.  Remembering that a
        family's ARRIVAL value was parked is what lets a later `pop`
        this one-line reading cannot place be read as the restore it
        is: a body with one `push %rbx` and two `pop %rbx`, one per
        return path, is `clang/__eqtf2`, measured."""
        if isinstance(token, tuple):
            if token[0] == "entry":
                saved_entry.add(token[1])

    def write_family(family, token):
        if family is None:
            return
        if family in ANSWER_EXCLUDED:
            return
        state[family] = token
        order[family] = step

    for raw in lines:
        line = R36.strip_annotation(raw).strip()
        if not line:
            continue
        if line.endswith(":"):
            continue
        step = step + 1
        mnemonic = mnemonic_of(line)
        if mnemonic is None:
            continue
        operands = operands_of(line)
        last_executable = mnemonic
        if mnemonic in RETURN_STEMS:
            saw_return = True
            x87_at_returns.append(x87_depth)
            continue
        if mnemonic.startswith("nop"):
            continue
        if mnemonic in ("endbr64", "hlt", "ud2", "int3", "cld", "std"):
            continue
        # ------------------------------------------- the machine stack
        if mnemonic.startswith("push"):
            delta = delta - 8
            if operands:
                parked = token_of(operands[0])
                slots[delta] = parked
                park(parked)
            continue
        if mnemonic.startswith("pop"):
            token = slots.pop(delta, None)
            delta = delta + 8
            if not operands:
                continue
            family = family_of_operand(operands[0])
            if token is None:
                token = ("computed", step)
                if family in saved_entry:
                    token = ("entry", family)
            write_family(family, token)
            continue
        # ------------------------------------------------------ x87
        if x87_base(mnemonic) is not None:
            if mnemonic.startswith(X87_PUSHERS):
                x87_depth = x87_depth + 1
                continue
            if mnemonic.startswith(X87_POPPERS):
                if x87_depth > 0:
                    x87_depth = x87_depth - 1
                continue
            continue
        # ------------------------------------------------- transfers
        if is_transfer(mnemonic):
            callee = transfer_callee(mnemonic, operands, raw)
            if callee is None:
                callee = reloc_callee(raw)
            if mnemonic in TRANSFER_STEMS:
                if callee is None:
                    unresolved.append(line)
                    continue
                inner = None
                if resolve is not None:
                    inner = resolve(callee, seen)
                if inner is None:
                    unresolved.append(callee)
                    continue
                if inner.get("refuse"):
                    unresolved.append(callee)
                    continue
                for family in inner.get("families", []):
                    write_family(family, ("computed", step))
                continue
            if mnemonic == "jmp":
                if callee is not None:
                    tail_transfer = callee
            continue
        # ------------------------------ the per-opcode destination table
        stem, rule = destination_rule(mnemonic, len(operands))
        if rule is not None:
            for family, _half in rule["writes"]:
                write_family(family, ("computed", step))
            continue
        # ----------------------------------------------- comparisons
        if comparison_stem(mnemonic) is not None:
            continue
        # ------------------------------------------- the ordinary rule
        if not operands:
            continue
        destination = operands[-1]
        source_token = ("computed", step)
        base = mnemonic
        while len(base) > 3:
            if base in MOVE_LIKE:
                break
            if base[-1] not in SIZE_SUFFIX:
                break
            base = base[:-1]
        if base in MOVE_LIKE:
            if len(operands) == 2:
                source_token = token_of(operands[0])
        family = family_of_operand(destination)
        if family is not None:
            if mnemonic.startswith(("add", "sub")):
                if family in ANSWER_EXCLUDED:
                    if destination == "%rsp":
                        amount = immediate_value(operands[0]) \
                            if operands else None
                        if amount is None:
                            depth_known = False
                        elif mnemonic.startswith("add"):
                            delta = delta + amount
                        else:
                            delta = delta - amount
                        continue
            write_family(family, source_token)
            continue
        slot = _memory_slot(destination, delta)
        if slot is not None:
            if depth_known:
                slots[slot] = source_token
        continue

    changed = []
    for family, token in state.items():
        if token == ("entry", family):
            continue
        changed.append(family)
    changed.sort(key=lambda name: (order.get(name, 0), name))

    leaves_x87 = False
    for depth in x87_at_returns:
        if depth > 0:
            leaves_x87 = True
    if not x87_at_returns:
        leaves_x87 = x87_depth > 0

    reading = {
        "families": changed,
        "x87": leaves_x87,
        "saved_and_restored": sorted(saved_entry),
        "tail_transfer": tail_transfer,
        "unresolved_transfers": unresolved,
        "saw_return": saw_return,
        "stack_depth_tracked": depth_known,
        "how": "the families whose token is no longer their own entry "
               "token after one text-order walk of the callee's body, "
               "with the machine stack tracked so a save-and-restore "
               "ends unchanged",
    }
    if tail_transfer is not None:
        if resolve is None:
            reading["refuse"] = (
                "this body ends in an unconditional transfer to %r and "
                "no resolver was handed in, so the routine it hands "
                "its answer to cannot be read" % tail_transfer)
            return reading
        inner = resolve(tail_transfer, seen)
        if inner is None or inner.get("refuse"):
            reading["refuse"] = (
                "this body ends in an unconditional transfer to %r, "
                "whose own body could not be read" % tail_transfer)
            return reading
        for family in inner.get("families", []):
            if family not in reading["families"]:
                reading["families"].append(family)
        if inner.get("x87"):
            reading["x87"] = True
        reading["saw_return"] = reading["saw_return"] or \
            inner.get("saw_return", False)
        reading["how"] = reading["how"] + \
            ", plus the families of the routine this body tail-transfers to"
    if not reading["saw_return"]:
        reading["refuse"] = (
            "this body carries no return and no resolvable tail "
            "transfer, so where it leaves its answer cannot be read")
        return reading
    if not depth_known:
        reading["refuse"] = (
            "the tracked stack depth was lost inside this body, so a "
            "save-and-restore cannot be told from a change")
        return reading
    if not reading["families"]:
        if not reading["x87"]:
            reading["refuse"] = (
                "this body changes no register family and leaves "
                "nothing on the x87 stack, so it names no answer")
            return reading
    return reading


def answer_row_half(family):
    """what a runtime-callee row's `written_half` says."""
    return "the value the attached callee leaves in %%%s" % family


def destination_rule(mnemonic, operand_count):
    """COPIED UNCHANGED from ledger48.py.  The table row for
    `mnemonic`, or None when the ordinary rule ('the destination is
    the last named operand') applies."""
    stem = mnemonic
    if stem not in DESTINATION_RULES:
        if len(mnemonic) > 3:
            if mnemonic[-1] in SIZE_SUFFIX:
                stem = mnemonic[:-1]
    rule = DESTINATION_RULES.get(stem)
    if rule is None:
        return None, None
    wanted = rule["only_when_operand_count_is"]
    if wanted is not None:
        if operand_count != wanted:
            return None, None
    return stem, rule


CALLEE_TEXT = re.compile(r"^x_(\w+)$")


def transfer_callee(mnemonic, operands, annotation=""):
    """the routine a transfer names, or None when this line is not a
    transfer to a named routine.

    TWO places carry the name, and both are machine form:
      * the assembler identifier the positional-label pass leaves
        behind on a transfer out of the unit (`call x___divti3`);
      * the RELOCATION the unit's own object file carries
        (`!!reloc=R_X86_64_PLT32:__divti3-0x4`).  A `call` whose
        displacement is not yet linked disassembles as a transfer to
        an address inside the unit, so the label pass writes `call L0`
        and only the relocation still says where it really goes.  The
        relocation is read here for exactly that reason.
    """
    if mnemonic not in TRANSFER_STEMS:
        return None
    if annotation:
        named = reloc_callee(annotation)
        if named is not None:
            return named
    if not operands:
        return None
    hit = CALLEE_TEXT.match(operands[0].strip())
    if hit is None:
        return None
    return hit.group(1)


# ==================================================================
# THE `flag_rules` SUB-NODE -- FLAG_RULES
#
# The setter stems are COPIED UNCHANGED from ledger47.py; the
# comparison stems and the unconditional-transfer rule are COPIED
# UNCHANGED from ledger48.py.  WHAT IS NEW is the `carry_in_setters`
# entry and the two-row model it names -- rule 7, written into
# CORE_0_3_5_3_4_flag_rules.md first.
# ==================================================================

FLAG_SETTER_STEMS = frozenset([
    "cmp", "test",
    "add", "sub", "and", "or", "xor", "inc", "dec", "neg",
    "shl", "shr", "sar", "sal", "rol", "ror", "rcl", "rcr",
    "shld", "shrd",
    "adc", "sbb", "imul", "mul", "div", "idiv",
    "bt", "bts", "btr", "btc", "bsf", "bsr", "popcnt", "lzcnt",
    "tzcnt", "xadd", "cmpxchg",
    "ucomiss", "ucomisd", "comiss", "comisd",
    "vucomiss", "vucomisd", "vcomiss", "vcomisd",
    "fucomi", "fucomip", "fcomi", "fcomip", "fucom", "fucomp",
    "fcom", "fcomp", "ftst",
    "ptest", "vptest",
    "cmpeqss", "cmpeqsd", "cmpss", "cmpsd",
])

COMPARISON_STEMS = frozenset([
    "cmp", "test",
    "ucomiss", "ucomisd", "comiss", "comisd",
    "vucomiss", "vucomisd", "vcomiss", "vcomisd",
    "ptest", "vptest",
    "bt",
    "fucomi", "fucomip", "fcomi", "fcomip",
    "fucom", "fucomp", "fcom", "fcomp", "ftst",
])

UNCONDITIONAL_TRANSFERS = frozenset(["jmp", "jmpq"])

# RULE 7, the model this lap writes.  A stem here reads the carry the
# previous setter left AND sets flags from its own arithmetic, so it
# writes two rows: the value it computed, and the flag state it left.
CARRY_IN_SETTERS = {
    "sbb": {
        "value_half": "the difference",
        "flags_half": "the flags",
        "reads": "the carry the previous flag-setting opcode left, "
                 "and both of its own named operands",
        "why": "this opcode subtracts its source and the carry from "
               "its destination, so its answer depends on the flag "
               "state as well as on its operands, and the flags it "
               "leaves are its own",
    },
    "adc": {
        "value_half": "the sum",
        "flags_half": "the flags",
        "reads": "the carry the previous flag-setting opcode left, "
                 "and both of its own named operands",
        "why": "this opcode adds its source and the carry to its "
               "destination, so its answer depends on the flag state "
               "as well as on its operands, and the flags it leaves "
               "are its own",
    },
}

FLAG_RULES = {
    "setters": {
        "stems": sorted(FLAG_SETTER_STEMS),
        "how_matched": "by mnemonic stem, with ONE operand-size "
                       "suffix removed before the test, so cmpl and "
                       "cmpq are both cmp",
        "count": len(FLAG_SETTER_STEMS),
    },
    "comparison_setters": {
        "stems": sorted(COMPARISON_STEMS),
        "row": "a comparison writes a row typed `flags only` and does "
               "NOT repoint its named destination register",
    },
    "carry_in_setters": CARRY_IN_SETTERS,
    "readers": {
        "conditional_set": "set<condition>",
        "conditional_move": "cmov<condition>",
        "conditional_transfer": "j<condition>",
        "carry_in_arithmetic": sorted(CARRY_IN_SETTERS),
        "how_linked": "a reader's row carries, as its FIRST operand, "
                      "the ROW that set the flags it reads -- never a "
                      "running 'last flags' variable",
    },
    "never_a_reader": sorted(UNCONDITIONAL_TRANSFERS),
    "producer_of_a_flag_derived_row": "the PAIR (flag-setting opcode, "
                                      "flag-reading opcode); a "
                                      "lifter's helper name never "
                                      "enters the ledger",
}


def flag_setter_stem(mnemonic):
    """COPIED UNCHANGED from ledger47.py."""
    if mnemonic in FLAG_SETTER_STEMS:
        return mnemonic
    if len(mnemonic) < 2:
        return None
    if mnemonic[-1] in SIZE_SUFFIX:
        stem = mnemonic[:-1]
        if stem in FLAG_SETTER_STEMS:
            return stem
    return None


def sets_the_flags(mnemonic):
    return flag_setter_stem(mnemonic) is not None


def comparison_stem(mnemonic):
    """COPIED UNCHANGED from ledger48.py."""
    if mnemonic in COMPARISON_STEMS:
        return mnemonic
    if len(mnemonic) > 2:
        if mnemonic[-1] in SIZE_SUFFIX:
            stem = mnemonic[:-1]
            if stem in COMPARISON_STEMS:
                return stem
    return None


def carry_in_stem(mnemonic):
    """RULE 7: the stem of a mnemonic that reads the carry and sets its
    own flags, or None."""
    if mnemonic in CARRY_IN_SETTERS:
        return mnemonic
    if len(mnemonic) > 2:
        if mnemonic[-1] in SIZE_SUFFIX:
            stem = mnemonic[:-1]
            if stem in CARRY_IN_SETTERS:
                return stem
    return None


def is_flag_reading_transfer(mnemonic):
    """COPIED UNCHANGED from ledger48.py."""
    if JCC.match(mnemonic) is None:
        return False
    if mnemonic in UNCONDITIONAL_TRANSFERS:
        return False
    return True


# ==================================================================
# COPIED UNCHANGED from ledger48.py -- the machine stack and the x87
# register stack.
# ==================================================================

PUSH_STEMS = frozenset(["push", "pushq", "pushl", "pushw"])
POP_STEMS = frozenset(["pop", "popq", "popl", "popw"])

X87_LOADS = frozenset(["fld", "fild", "fldz", "fld1", "fldpi",
                       "fldl2e", "fldl2t", "fldlg2", "fldln2"])
X87_STORES_POP = frozenset(["fstp", "fistp", "fisttp"])
X87_STORES_KEEP = frozenset(["fst", "fist"])
X87_ARITH_POP = frozenset(["faddp", "fsubp", "fsubrp", "fmulp",
                           "fdivp", "fdivrp"])
X87_ARITH_KEEP = frozenset(["fadd", "fsub", "fsubr", "fmul", "fdiv",
                            "fdivr",
                            "fiadd", "fisub", "fisubr", "fimul",
                            "fidiv", "fidivr"])
X87_ONE_PLACE = frozenset(["fchs", "fabs", "fsqrt", "frndint", "f2xm1",
                           "fcos", "fsin", "fptan", "fyl2x"])
X87_EXCHANGE = frozenset(["fxch"])
X87_COMPARE_POP = frozenset(["fucomip", "fcomip", "fucomp", "fcomp"])
X87_COMPARE_KEEP = frozenset(["fucomi", "fcomi", "fucom", "fcom",
                              "ftst"])

X87_BASES = (X87_LOADS | X87_STORES_POP | X87_STORES_KEEP
             | X87_ARITH_POP | X87_ARITH_KEEP | X87_ONE_PLACE
             | X87_EXCHANGE | X87_COMPARE_POP | X87_COMPARE_KEEP)

X87_SIZE_LETTERS = ("s", "l", "t", "q", "b", "w")

X87_POSITION = re.compile(r"^%st(?:\((\d)\))?$")

X87_POSITIONS = 8


def x87_base(mnemonic):
    """COPIED UNCHANGED from ledger48.py."""
    if not mnemonic.startswith("f"):
        return None
    text = mnemonic
    while True:
        if text in X87_BASES:
            return text
        if len(text) <= 3:
            return None
        if text[-1] not in X87_SIZE_LETTERS:
            return None
        text = text[:-1]


def x87_position_of(operand):
    """COPIED UNCHANGED from ledger48.py."""
    hit = X87_POSITION.match(operand)
    if hit is None:
        return None
    if hit.group(1) is None:
        return 0
    return int(hit.group(1))


# ==================================================================
# COPIED UNCHANGED from ledger48.py -- RULING 4, positional branch
# labels.
# ==================================================================

TRANSFER_TARGET = re.compile(r"^([0-9a-f]+)\s*(?:<([^>]*)>)?$")
INNER_OFFSET = re.compile(r"\+0x([0-9a-f]+)$")
EXTERNAL_NAME = re.compile(r"[^A-Za-z0-9_]")
TRANSFER_MNEMONIC = re.compile(r"^(j[a-z]+|call|callq|loop[a-z]*)$")


def is_transfer(mnemonic):
    return TRANSFER_MNEMONIC.match(mnemonic) is not None


def external_symbol(inner):
    """COPIED UNCHANGED from ledger48.py."""
    head = inner.split("@")[0]
    head = head.split("+")[0]
    head = head.split("-")[0]
    return "x_" + EXTERNAL_NAME.sub("_", head)


def instruction_offsets(byte_text):
    """COPIED UNCHANGED from ledger48.py."""
    if not byte_text:
        return None
    try:
        import capstone
    except ImportError:
        return None
    cleaned = byte_text.replace(" ", "").replace("\n", "")
    try:
        blob = bytes.fromhex(cleaned)
    except ValueError:
        return None
    engine = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    offsets = []
    for instruction in engine.disasm(blob, 0):
        offsets.append(instruction.address)
    return offsets


def split_off_annotation(line):
    """COPIED UNCHANGED from ledger48.py."""
    if "!!" not in line:
        return line, ""
    head, tail = line.split("!!", 1)
    return head.strip(), "!!" + tail


def reloc_callee(annotation):
    """COPIED UNCHANGED from ledger48.py."""
    if "reloc=" not in annotation:
        return None
    piece = annotation.split("reloc=", 1)[1]
    if ":" not in piece:
        return None
    name = piece.split(":", 1)[1]
    name = name.split("-")[0]
    name = name.split("+")[0]
    name = name.strip()
    if not name:
        return None
    return name


def positional_labels(body_lines, byte_text):
    """COPIED UNCHANGED from ledger48.py.  RULING 4, applied to one
    body.  Returns (new_body_lines, record)."""
    offsets = instruction_offsets(byte_text)
    by_offset = {}
    if offsets is not None:
        if len(offsets) == len(body_lines):
            for index, offset in enumerate(offsets):
                by_offset[offset] = index
    found = []
    for index, raw in enumerate(body_lines):
        text, annotation = split_off_annotation(raw)
        parts = text.split(" ", 1)
        if len(parts) != 2:
            continue
        mnemonic = parts[0]
        if not is_transfer(mnemonic):
            continue
        hit = TRANSFER_TARGET.match(parts[1].strip())
        if hit is None:
            continue
        address = int(hit.group(1), 16)
        inner = hit.group(2)
        inside = None
        if inner is not None:
            offset_hit = INNER_OFFSET.search(inner)
            if offset_hit is not None:
                candidate = int(offset_hit.group(1), 16)
                if candidate in by_offset:
                    inside = candidate
        if inside is None:
            if address in by_offset:
                inside = address
        found.append({
            "line_index": index,
            "mnem": mnemonic,
            "address": address,
            "inner": inner,
            "inside_at_offset": inside,
            "annotation": annotation,
        })
    inside_targets = []
    for entry in found:
        if entry["inside_at_offset"] is None:
            continue
        if entry["inside_at_offset"] in inside_targets:
            continue
        inside_targets.append(entry["inside_at_offset"])
    inside_targets.sort()
    label_of_offset = {}
    for rank, offset in enumerate(inside_targets):
        label_of_offset[offset] = "L%d" % rank
    outside_addresses = []
    for entry in found:
        if entry["inside_at_offset"] is not None:
            continue
        if entry["address"] in outside_addresses:
            continue
        outside_addresses.append(entry["address"])
    outside_addresses.sort()
    label_of_outside = {}
    for rank, address in enumerate(outside_addresses):
        label_of_outside[address] = "L%d" % (len(inside_targets) + rank)

    rewrites = []
    replaced = {}
    for entry in found:
        text, annotation = split_off_annotation(body_lines[
            entry["line_index"]])
        was = text
        if entry["inside_at_offset"] is not None:
            label = label_of_offset[entry["inside_at_offset"]]
            now = "%s %s" % (entry["mnem"], label)
            how = "a transfer to an instruction inside this unit"
        else:
            callee = None
            if entry["annotation"]:
                callee = reloc_callee(entry["annotation"])
            if callee is None:
                if entry["inner"]:
                    callee = entry["inner"]
            if callee is None:
                label = label_of_outside[entry["address"]]
                now = "%s %s" % (entry["mnem"], label)
                how = ("a transfer this file could not place: neither "
                       "the bytes nor a symbol comment says where it "
                       "goes, so the target is a positional label and "
                       "the address is dropped")
            else:
                now = "%s %s" % (entry["mnem"], external_symbol(callee))
                how = "a transfer out of this unit, to a named callee"
        if annotation:
            now = "%s %s" % (now, annotation)
        replaced[entry["line_index"]] = now
        rewrites.append({
            "line_index": entry["line_index"],
            "was": was,
            "now": now,
            "how": how,
        })

    out = []
    label_lines = []
    for index, raw in enumerate(body_lines):
        offset_here = None
        if offsets is not None:
            if len(offsets) == len(body_lines):
                offset_here = offsets[index]
        if offset_here is not None:
            if offset_here in label_of_offset:
                name = label_of_offset[offset_here]
                out.append("%s:" % name)
                label_lines.append({"label": name,
                                    "before_line_index": index})
        if index in replaced:
            out.append(replaced[index])
            continue
        out.append(raw)
    record = {
        "transfers_seen": len(found),
        "labels_defined": label_lines,
        "rewrites": rewrites,
        "bytes_were_read": offsets is not None and len(by_offset) > 0,
        "how": "targets inside the unit become L0.. in address order "
               "and the label is defined on the instruction it names; "
               "a transfer out of the unit keeps its callee and loses "
               "its address; the objdump symbol comment is dropped "
               "either way",
    }
    return out, record


# ==================================================================
# THE `row` SUB-NODE -- class Row
#
# The record ledger48's LedgerTable.add built as a dict, given the
# class shape the CORE names.  The dict form is what every artifact
# carries, so `as_dict` is what is written down and the field names
# are unchanged.
# ==================================================================

class Row(object):
    """one value that moves through a unit, written down as one line of
    the ledger.  Its name is its block plus its index."""

    def __init__(self, block, index, offset, size, type_name,
                 produced_by, operands, note=None, resident=None):
        self.block = block
        self.index = index
        self.offset = offset
        self.size = size
        self.type = type_name
        self.produced_by = Producer.of(produced_by)
        self.operands = list(operands)
        self.written_half = None
        self.value_at_run = None
        self.note = note
        self.resident = resident
        self.extra = {}

    def name(self):
        return row_text(self.block, self.index)

    def as_dict(self):
        out = {
            "row": self.name(),
            "block": self.block,
            "index": self.index,
            "offset": self.offset,
            "size": self.size,
            "type": self.type,
            "produced_by": self.produced_by.as_dict(),
            "operands": list(self.operands),
            "value_at_run": self.value_at_run,
            "ledger_entry": ledger_entry_index(self.block),
            "ledger_entry_text": ledger_entry_text(self.block),
        }
        if self.note is not None:
            out["note"] = self.note
        if self.resident is not None:
            out["resident"] = self.resident
        if self.written_half is not None:
            out["written_half"] = self.written_half
        for key in sorted(self.extra):
            out[key] = self.extra[key]
        return out


# ==================================================================
# THE NODE ITSELF -- class Ledger
#
# attributes: rows       (the CORE's unrealized sub-node `rows`)
# methods:    walk_dataflow, wrap_unit
# ==================================================================

class Ledger(object):
    """the provenance ledger of one unit, over the eight blocks.

    `runtime_routines` is the set of routine names the compiler's own
    archives DEFINE, handed in by `runtime_callee.py`.  When it is
    empty the runtime transfer rule does not fire, and a `call` is
    left exactly as it was.
    """

    def __init__(self, runtime_routines=None, runtime_answers=None,
                 toolchain=None):
        self.rows = []
        self.by_row = {}
        self.next_offset = {}
        self.counts = {}
        self.notes = []
        self.runtime_routines = frozenset(runtime_routines or [])
        self.runtime_answers = dict(runtime_answers or {})
        self.toolchain = toolchain
        self.transfer_shapes = []
        for block in BLOCK_ORDER:
            self.next_offset[block] = 0
            self.counts[block] = 0

    # ------------------------------- the attached callee's own answer
    def runtime_answer(self, callee):
        """the reading of the ATTACHED callee's own body, from the
        archive of the toolchain that built this caller.

        Keyed `toolchain/name` first, because one routine's body
        differs between compiler versions (swift's `__extendhfsf2` is
        33 instructions where clang 21's is 40 -- log_167 §5.3).  Where
        this caller's toolchain is not known, the readings of every
        toolchain that defines the name must AGREE, or the answer is
        not read at all."""
        if self.toolchain is not None:
            key = "%s/%s" % (self.toolchain, callee)
            if key in self.runtime_answers:
                return self.runtime_answers[key]
        if callee in self.runtime_answers:
            return self.runtime_answers[callee]
        offered = []
        for key, reading in self.runtime_answers.items():
            if not key.endswith("/" + callee):
                continue
            offered.append(reading)
        if not offered:
            return None
        first = offered[0]
        for other in offered[1:]:
            if other.get("families") != first.get("families"):
                return {"refuse":
                        "this caller's own toolchain is not known and "
                        "the toolchains that define %r do not agree "
                        "on the families its body changes" % callee}
            if other.get("x87") != first.get("x87"):
                return {"refuse":
                        "this caller's own toolchain is not known and "
                        "the toolchains that define %r do not agree "
                        "on whether it answers on the x87 stack"
                        % callee}
        return first

    # ------------------- a transfer no archive index defines (the 196)
    def record_transfer_shape(self, callee, body, line_index):
        """the shape a transfer gets when no archive index defines its
        target: `guard_exit` when the transfer is the last instruction
        of its block, `unread_runtime_routine` when the body carries on
        after it.  Neither makes a row.  The shapes are the proposal in
        CORE_0_3_5_1_8_runtime_callee.md, FLAGGED for the owner."""
        own_label = None
        line = R36.strip_annotation(body[line_index]).strip()
        operands = operands_of(line)
        if operands:
            candidate = operands[0].strip()
            if POSITIONAL_LABEL.match(candidate):
                own_label = candidate
        ends = True
        for later in body[line_index + 1:]:
            text = R36.strip_annotation(later).strip()
            if not text:
                continue
            if text.endswith(":"):
                # AN UNLINKED `call` DISASSEMBLES AS A TRANSFER TO ITS
                # OWN NEXT ADDRESS, and the positional-label pass then
                # defines that label on the very next instruction.  So
                # a label here is the transfer's OWN RETURN POINT when
                # it is the label the transfer names, and a different
                # block's entry otherwise.
                if own_label is not None:
                    if text[:-1] == own_label:
                        ends = False
                break
            if text.split()[0].startswith("nop"):
                continue
            ends = False
            break
        if ends:
            kind = "guard_exit"
            why = ("nothing follows this transfer on its own path "
                   "-- the body ends, or the next line defines a "
                   "label that is NOT this transfer's own return "
                   "point -- so the compiler emitted no continuation "
                   "and the routine does not come back: it produces "
                   "no value and the ledger makes no row")
        else:
            kind = "unread_runtime_routine"
            why = ("the routine comes back -- an instruction of the "
                   "same block follows the transfer, or the label the "
                   "transfer itself names does -- but no archive "
                   "index on this machine defines it, so the families "
                   "it changes cannot be read and no row is guessed")
        self.transfer_shapes.append({
            "kind": kind,
            "callee": callee,
            "why": why,
        })
        self.notes.append({
            "transfer_shape": kind,
            "callee": callee,
            "why": why,
        })

    # ------------------------------------------------------- rows
    def add(self, block, size, type_name, produced_by, operands,
            note=None, resident=None):
        if block not in BLOCK_ORDER:
            raise Refusal("unknown block",
                          "the ledger was asked for block %r" % block)
        index = self.counts[block]
        offset = align_up(self.next_offset[block], size)
        row = Row(block, index, offset, size, type_name, produced_by,
                  operands, note=note, resident=resident)
        self.counts[block] = index + 1
        self.next_offset[block] = offset + size
        self.rows.append(row)
        self.by_row[row.name()] = row
        return row

    def block_bytes(self):
        out = {}
        for block in BLOCK_ORDER:
            out[block] = self.next_offset[block]
        return out

    def as_list(self):
        out = []
        for row in self.rows:
            out.append(row.as_dict())
        return out

    # --------------------------------------------- the two wrappers
    def build_prelude(self, arrival_families):
        """COPIED UNCHANGED from ledger48.py, reading its rows off this
        ledger."""
        literal = []
        resolved = []
        rows = []
        general = []
        vector = []
        for family in arrival_families:
            if is_vector_family(family):
                vector.append(family)
            else:
                general.append(family)
        scratch = None
        if vector:
            scratch = pick_scratch(set(general) | set(canon.NEVER_RENAME))
        order = vector + general
        for family in order:
            if is_vector_family(family):
                size = 16
                type_name = "16-byte vector value"
            else:
                size = 8
                type_name = "8-byte general value"
            row = self.add("IN", size, type_name, "arrival", [],
                           note="the runner fills this row before the "
                                "unit is entered")
            rows.append(row)
            if is_vector_family(family):
                pointer = register_text(scratch, 64)
                literal.append("mov %s,%s" % (ledger_entry_text("IN"),
                                              pointer))
                literal.append("movdqu 0x%x(%s),%%%s"
                               % (row.offset, pointer, family))
                resolved.append("movdqu %s,%%%s" % (row.name(), family))
            else:
                pointer = register_text(family, 64)
                literal.append("mov %s,%s" % (ledger_entry_text("IN"),
                                              pointer))
                literal.append("mov 0x%x(%s),%s"
                               % (row.offset, pointer, pointer))
                resolved.append("mov %s,%s" % (row.name(), pointer))
        return literal, resolved, rows, scratch

    def build_epilogue(self, result_family, result_width, producer,
                       operands):
        """COPIED UNCHANGED from ledger48.py."""
        if result_family is None:
            raise Refusal(
                "no answer home",
                "this unit's own code names no register the answer is "
                "left in, so there is nothing to store into OUT-0")
        if is_vector_family(result_family):
            if result_width > 64:
                size = 16
                mnemonic = "movdqu"
                source = "%" + result_family
                type_name = "16-byte vector value"
            else:
                size = 8
                mnemonic = "movq"
                source = "%" + result_family
                type_name = "8-byte vector-held value"
        else:
            size = max(1, result_width // 8)
            if size not in (1, 2, 4, 8):
                size = 8
            mnemonic = "mov"
            source = register_text(result_family, size * 8)
            type_name = "%d-byte general value" % size
        row = self.add("OUT", size, type_name, producer, operands,
                       note="the answer; the runner reads this row "
                            "when the unit returns")
        scratch = pick_scratch(set([result_family])
                               | set(canon.NEVER_RENAME))
        pointer = register_text(scratch, 64)
        literal = []
        literal.append("mov %s,%s" % (ledger_entry_text("OUT"), pointer))
        literal.append("%s %s,0x%x(%s)"
                       % (mnemonic, source, row.offset, pointer))
        resolved = ["%s %s,%s" % (mnemonic, source, row.name())]
        return literal, resolved, row, scratch

    # ------------------------------------------------ walk_dataflow
    def walk_dataflow(self, body, arrival_rows, arrival_families):
        """body_text -> rows.  ONE PASS IN PROGRAM ORDER keeping a
        register-family -> row map; each instruction's destination(s)
        per DESTINATION_RULES; each flag reader linked to the row that
        set the flags per FLAG_RULES.

        COPIED from ledger48.walk_dataflow with ONE branch added: the
        carry-in setters of FLAG_RULES rule 7, and the runtime transfer
        rule.  Returns (where, notes).
        """
        where = {}
        for index, family in enumerate(arrival_families):
            where[family] = arrival_rows[index].name()
        literals = {}
        own = {}
        stack = []                 # the machine stack, newest first
        x87 = []                   # the x87 stack, position 0 first
        last_flag_setter = None
        last_flag_row = None
        notes = self.notes

        def read_operand_rows(operands, mnemonic, treat_last_as_read):
            """COPIED UNCHANGED from ledger48.py."""
            rows_read = []
            for position, operand in enumerate(operands):
                value = immediate_value(operand)
                if value is not None:
                    if operand not in literals:
                        made = self.add(
                            "CONST", 8, "literal",
                            "the body's own immediate operand", [],
                            note="not materialized: the body is kept "
                                 "verbatim, so the literal stays an "
                                 "immediate in the text")
                        made.value_at_run = value
                        literals[operand] = made.name()
                    rows_read.append(literals[operand])
                    continue
                if x87_position_of(operand) is not None:
                    continue
                if operand.startswith("%"):
                    family = family_of_operand(operand)
                    if family is None:
                        continue
                    is_last = position == len(operands) - 1
                    if is_last:
                        if not treat_last_as_read:
                            if mnemonic in PURE_WRITE_MNEMONICS:
                                continue
                    if family in where:
                        rows_read.append(where[family])
                    continue
                for token in re.findall(r"%[a-z0-9]+", operand):
                    family = canon.FAMILY_OF.get(token[1:])
                    if family is None:
                        continue
                    if family in where:
                        rows_read.append(where[family])
                for hit in R36.RSP_DISP.finditer(operand):
                    displacement = int(hit.group(1), 16)
                    key = "-0x%x(%%rsp)" % displacement
                    if key not in own:
                        made = self.add(
                            "OWN", 8, "the unit's own stack address",
                            "the body's own stack displacement", [],
                            note="the body is kept verbatim, so this "
                                 "row records the address the body "
                                 "itself spells: %%rsp - 0x%x"
                                 % displacement)
                        made.extra["displacement"] = displacement
                        made.extra["address_is"] = ("%%rsp - 0x%x"
                                                    % displacement)
                        own[key] = made.name()
                    rows_read.append(own[key])
            return rows_read

        def x87_row_at(position, mnemonic):
            """COPIED UNCHANGED from ledger48.py."""
            while len(x87) <= position:
                made = self.add(
                    "X87", 16, "x87 stack value",
                    "an x87 stack position this unit did not itself "
                    "load", [],
                    note="the body reads x87 stack position %d without "
                         "having loaded it inside this body, so the "
                         "row stands for what was there when the unit "
                         "was entered" % len(x87),
                    resident="x87 stack position %d" % len(x87))
                made.extra["x87_position"] = len(x87)
                x87.append(made.name())
                notes.append({
                    "row_producer_hole": mnemonic,
                    "why": "an x87 stack position was read before this "
                           "body loaded it; the row records that it "
                           "came from outside the body",
                })
            return x87[position]

        for line_index, raw in enumerate(body):
            line, annotation = split_off_annotation(raw)
            line = R36.strip_annotation(raw)
            if line.endswith(":"):
                continue
            if line == "ret":
                continue
            mnemonic = mnemonic_of(line)
            operands = operands_of(line)

            # ---------------------------------------------- x87
            base = x87_base(mnemonic)
            if base is not None:
                named = []
                for operand in operands:
                    position = x87_position_of(operand)
                    if position is not None:
                        named.append(position)
                memory_rows = read_operand_rows(operands, mnemonic, True)
                if base in X87_LOADS:
                    made = self.add(
                        "X87", 16, "x87 stack value",
                        Producer.arch_opcode(mnemonic), memory_rows,
                        note="this opcode pushed a value onto the x87 "
                             "register stack; it becomes position 0 "
                             "and every other position moves down one",
                        resident="x87 stack position 0")
                    made.extra["x87_position"] = 0
                    x87.insert(0, made.name())
                    if len(x87) > X87_POSITIONS:
                        notes.append({
                            "row_producer_hole": mnemonic,
                            "why": "the x87 register stack has eight "
                                   "positions and this body pushed "
                                   "past the eighth",
                        })
                    continue
                if base in X87_STORES_POP or base in X87_STORES_KEEP:
                    top = x87_row_at(0, mnemonic)
                    destination = operands[-1] if operands else None
                    if destination is not None:
                        family = family_of_operand(destination)
                        if family is not None:
                            if family not in canon.NEVER_RENAME:
                                where[family] = top
                    if base in X87_STORES_POP:
                        if x87:
                            x87.pop(0)
                    continue
                if base in X87_COMPARE_POP or base in X87_COMPARE_KEEP:
                    sides = []
                    if named:
                        for position in named:
                            sides.append(x87_row_at(position, mnemonic))
                    else:
                        sides.append(x87_row_at(0, mnemonic))
                    made = self.add(
                        "TEMP", 8, "flags only",
                        Producer.arch_opcode(mnemonic),
                        sides + memory_rows,
                        note="a comparison writes the flags and no "
                             "register: this row is the flag state the "
                             "next flag-reading opcode picks up")
                    last_flag_setter = mnemonic
                    last_flag_row = made.name()
                    if base in X87_COMPARE_POP:
                        if x87:
                            x87.pop(0)
                    continue
                if base in X87_EXCHANGE:
                    other = 1
                    if named:
                        other = named[0]
                    if other == 0:
                        continue
                    x87_row_at(other, mnemonic)
                    first = x87[0]
                    x87[0] = x87[other]
                    x87[other] = first
                    continue
                sides = []
                for position in named:
                    sides.append(x87_row_at(position, mnemonic))
                if not sides:
                    sides.append(x87_row_at(0, mnemonic))
                made = self.add(
                    "X87", 16, "x87 stack value",
                    Producer.arch_opcode(mnemonic), sides + memory_rows,
                    note="this opcode wrote an x87 stack position",
                    resident="an x87 stack position")
                destination_position = 0
                if base in X87_ARITH_POP:
                    destination_position = 1
                    if named:
                        destination_position = named[-1]
                elif named:
                    destination_position = named[-1]
                x87_row_at(destination_position, mnemonic)
                made.extra["x87_position"] = destination_position
                x87[destination_position] = made.name()
                if base in X87_ARITH_POP:
                    if x87:
                        x87.pop(0)
                continue

            # -------------------------------------------- the stack
            if mnemonic in PUSH_STEMS:
                read_rows = read_operand_rows(operands, mnemonic, True)
                made = self.add(
                    "STACK", 8, "8-byte value on the machine stack",
                    Producer.arch_opcode(mnemonic), read_rows,
                    note="this opcode moved a value onto the machine "
                         "stack; the row holds the value it moved",
                    resident="the machine stack, newest entry")
                stack.insert(0, made.name())
                continue
            if mnemonic in POP_STEMS:
                if stack:
                    taken = stack.pop(0)
                else:
                    made = self.add(
                        "STACK", 8, "8-byte value on the machine stack",
                        "a value the machine stack held before this "
                        "unit was entered", [],
                        note="this opcode took a value off the machine "
                             "stack that no opcode in this body put "
                             "there",
                        resident="the machine stack, before entry")
                    taken = made.name()
                destination = operands[-1] if operands else None
                if destination is not None:
                    family = family_of_operand(destination)
                    if family is not None:
                        where[family] = taken
                continue

            # ------------- FLAG_RULES rule 7: the carry-in setters
            carry_stem = carry_in_stem(mnemonic)
            if carry_stem is not None:
                rule = CARRY_IN_SETTERS[carry_stem]
                read_rows = read_operand_rows(operands, mnemonic, True)
                all_read = list(read_rows)
                if last_flag_row is not None:
                    all_read = [last_flag_row] + all_read
                else:
                    notes.append({
                        "row_producer_hole": mnemonic,
                        "why": "this opcode reads the carry the "
                               "previous flag-setting opcode left, and "
                               "no flag-setting arch opcode precedes "
                               "it in this body, so the carry it reads "
                               "came from outside the body",
                    })
                destination = operands[-1] if operands else None
                family = None
                if destination is not None:
                    family = family_of_operand(destination)
                size = 8
                type_name = "8-byte general value"
                if is_vector_family(family):
                    size = 16
                    type_name = "16-byte vector value"
                value_row = None
                if family is not None:
                    if family not in canon.NEVER_RENAME:
                        value_row = self.add(
                            "TEMP", size, type_name,
                            Producer.arch_opcode(mnemonic,
                                                 rule["value_half"]),
                            all_read,
                            note="FLAG_RULES rule 7: %s.  This row is "
                                 "the value half; the flag state this "
                                 "opcode leaves is the row after it"
                                 % rule["why"],
                            resident="register %%%s" % family)
                        value_row.written_half = rule["value_half"]
                        where[family] = value_row.name()
                flags_row = self.add(
                    "TEMP", 8, "flags only",
                    Producer.arch_opcode(mnemonic, rule["flags_half"]),
                    all_read,
                    note="FLAG_RULES rule 7: this opcode sets the "
                         "flags from its own arithmetic, so the flag "
                         "state a following flag-reading opcode picks "
                         "up is THIS row and not the value row and not "
                         "the earlier comparison")
                flags_row.written_half = rule["flags_half"]
                if value_row is not None:
                    flags_row.extra["value_half_row"] = value_row.name()
                last_flag_setter = mnemonic
                last_flag_row = flags_row.name()
                continue

            # ---------------------------- the destination table
            stem, rule = destination_rule(mnemonic, len(operands))
            if rule is not None:
                read_rows = read_operand_rows(operands, mnemonic, True)
                implicit = []
                for family in rule["reads_implicitly"]:
                    if family in where:
                        implicit.append(where[family])
                all_read = implicit + read_rows
                made_rows = []
                for family, half in rule["writes"]:
                    made = self.add(
                        "TEMP", 8, "8-byte general value",
                        Producer.arch_opcode(mnemonic, half), all_read,
                        note="the per-opcode destination rule: %s"
                             % rule["why"],
                        resident="register %%%s" % family)
                    made.written_half = half
                    made_rows.append((family, made))
                for family, made in made_rows:
                    where[family] = made.name()
                if sets_the_flags(mnemonic):
                    last_flag_setter = mnemonic
                    last_flag_row = made_rows[0][1].name()
                continue

            # ------------- the transfer into the compiler's runtime
            callee = transfer_callee(mnemonic, operands, annotation)
            if callee is not None:
                if callee in self.runtime_routines:
                    reading = self.runtime_answer(callee)
                    if reading is None:
                        raise Refusal(
                            "the attached callee's answer register "
                            "cannot be read",
                            "the transfer names %r, which one of this "
                            "machine's archives defines, but no "
                            "reading of that body was handed to the "
                            "ledger" % callee)
                    if reading.get("refuse"):
                        raise Refusal(
                            "the attached callee's answer register "
                            "cannot be read",
                            "the transfer names %r and its own body "
                            "was read: %s"
                            % (callee, reading["refuse"]))
                    implicit = []
                    for family in ("rdi", "rsi", "rdx", "rcx",
                                   "xmm0", "xmm1"):
                        if family in where:
                            implicit.append(where[family])
                    for family in reading["families"]:
                        size = 8
                        type_name = "8-byte general value"
                        if is_vector_family(family):
                            size = 16
                            type_name = "16-byte vector value"
                        made = self.add(
                            "TEMP", size, type_name,
                            Producer.runtime_callee(callee), implicit,
                            note="the runtime transfer rule: %s"
                                 % RUNTIME_TRANSFER_RULE["why"],
                            resident="register %%%s" % family)
                        made.written_half = answer_row_half(family)
                        where[family] = made.name()
                    if reading.get("x87"):
                        made = self.add(
                            "X87", 16, "x87 stack value",
                            Producer.runtime_callee(callee), implicit,
                            note="the attached callee leaves its "
                                 "answer on the x87 stack: its own "
                                 "body pushes more than it pops on "
                                 "the path to its return",
                            resident="x87 stack position 0")
                        made.extra["x87_position"] = 0
                        made.written_half = (
                            "the value the attached callee leaves on "
                            "the x87 stack")
                        x87.insert(0, made.name())
                    continue
                self.record_transfer_shape(callee, body, line_index)

            # ----------------------------------- comparisons
            if comparison_stem(mnemonic) is not None:
                read_rows = read_operand_rows(operands, mnemonic, True)
                made = self.add(
                    "TEMP", 8, "flags only",
                    Producer.arch_opcode(mnemonic), read_rows,
                    note="a comparison writes the flags and no "
                         "register: this row is the flag state the "
                         "next flag-reading opcode picks up, and the "
                         "destination operand keeps the value it had")
                last_flag_setter = mnemonic
                last_flag_row = made.name()
                continue

            # ----------------------------------- flag readers
            read_rows = read_operand_rows(operands, mnemonic, False)
            flag_reader = None
            if SETCC.match(mnemonic):
                flag_reader = mnemonic
            if CMOVCC.match(mnemonic):
                flag_reader = mnemonic
            if is_flag_reading_transfer(mnemonic):
                flag_reader = mnemonic
            if flag_reader is not None:
                producer = [last_flag_setter, flag_reader]
                operands_of_row = list(read_rows)
                if last_flag_row is not None:
                    operands_of_row = [last_flag_row] + operands_of_row
                if last_flag_setter is None:
                    notes.append({
                        "row_producer_hole": flag_reader,
                        "why": "no flag-setting arch opcode precedes "
                               "this flag-reading opcode in the body, "
                               "so the pair the ledger records is "
                               "incomplete",
                    })
                made = self.add("GUARD", 8, "flag-derived value",
                                producer, operands_of_row,
                                note="the producer is the pair "
                                     "(flag-setting opcode, "
                                     "flag-reading opcode), and the "
                                     "first operand is the row holding "
                                     "the flag state that pair reads")
                if JCC.match(mnemonic):
                    continue
                destination = operands[-1] if operands else None
                if destination is not None:
                    family = family_of_operand(destination)
                    if family is not None:
                        where[family] = made.name()
                continue

            if mnemonic in UNCONDITIONAL_TRANSFERS:
                continue
            if not operands:
                continue
            destination = operands[-1]
            family = family_of_operand(destination)
            if family is None:
                continue
            if family in canon.NEVER_RENAME:
                continue
            size = 16 if is_vector_family(family) else 8
            if size == 16:
                type_name = "16-byte vector value"
            else:
                type_name = "8-byte general value"
            made = self.add("TEMP", size, type_name,
                            Producer.arch_opcode(mnemonic), read_rows,
                            resident="register %%%s" % family)
            where[family] = made.name()
            if sets_the_flags(mnemonic):
                last_flag_setter = mnemonic
                last_flag_row = made.name()
        return where, notes

    # ---------------------------------------------------- wrap_unit
    def wrap_unit(self, body_text, arrival_families, result_family,
                  result_width, body_bytes=None):
        """COPIED from ledger48.wrap_unit, reading its ledger off this
        object.  (fields)."""
        if not body_text:
            raise Refusal("no text",
                          "no text exists for this unit, so there is "
                          "no body to wrap")
        body_as_read = split_lines(body_text)
        for raw in body_as_read:
            line = R36.strip_annotation(raw)
            if LEDGER_SYMBOL in line:
                raise Refusal(
                    "the body names the ledger symbol",
                    "the body spells %r, which would collide with the "
                    "form's own symbol" % LEDGER_SYMBOL)
        body, label_record = positional_labels(body_as_read, body_bytes)
        prelude_literal, prelude_resolved, arrival_rows, \
            prelude_scratch = self.build_prelude(arrival_families)
        where, holes = self.walk_dataflow(body, arrival_rows,
                                          arrival_families)
        producer = "the body's last write to %%%s" % result_family
        operands = []
        if result_family in where:
            answer_row = where[result_family]
            operands = [answer_row]
            source_row = self.by_row.get(answer_row)
            if source_row is not None:
                producer = source_row.produced_by
        epilogue_literal, epilogue_resolved, out_row, epilogue_scratch \
            = self.build_epilogue(result_family, result_width, producer,
                                  operands)
        literal_lines, returns = weave(body, prelude_literal,
                                       epilogue_literal)
        resolved_lines, _ = weave(body, prelude_resolved,
                                  epilogue_resolved)
        fields = {
            "wrapped_text": "; ".join(literal_lines),
            "wrapped_text_resolved": "; ".join(resolved_lines),
            "body_verbatim": list(body),
            "body_as_read": list(body_as_read),
            "branch_labels": label_record,
            "prelude": prelude_literal,
            "prelude_resolved": prelude_resolved,
            "epilogue": epilogue_literal,
            "epilogue_resolved": epilogue_resolved,
            "prelude_scratch": prelude_scratch,
            "epilogue_scratch": epilogue_scratch,
            "returns": returns,
            "ledger": self.as_list(),
            "ledger_block_bytes": self.block_bytes(),
            "ledger_symbol": LEDGER_SYMBOL,
            "ledger_entries": list(BLOCK_ORDER),
            "out_row": out_row.name(),
            "arrival_families": list(arrival_families),
            "result_family": result_family,
            "result_width": result_width,
            "producer_holes": holes,
            "form": "ledger",
            "addressing": "two steps: read the block's base out of the "
                          "ledger at an absolute address "
                          "(rip-relative), then read the row inside "
                          "that block",
        }
        return fields


# ------------------------------------------------------------------
# the module-level entry every consumer uses
# ------------------------------------------------------------------

def wrap_unit(body_text, arrival_families, result_family, result_width,
              body_bytes=None, runtime_routines=None,
              runtime_answers=None, toolchain=None):
    """one unit -> its wrapped form and its ledger.  This is what
    `canonical_form.py` (node 0_3_5_2, task 60) calls."""
    ledger = Ledger(runtime_routines=runtime_routines,
                    runtime_answers=runtime_answers,
                    toolchain=toolchain)
    return ledger.wrap_unit(body_text, arrival_families, result_family,
                            result_width, body_bytes=body_bytes)
