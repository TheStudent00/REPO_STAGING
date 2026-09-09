#!/usr/bin/env python3
"""canon37_gate.py -- THE GATE for the memory-wrapped form of task 47.

THE FORM is ledger47.py's; read that file's header first.  This file
holds only the proof machinery:

  * SIM47 -- canon33_gate.Sim33 whose designated-location model also
    covers the LEDGER ROW TEXTS (`IN-0`, `OUT-0`, ...), at the row's
    own width, so a 16-byte row is carried at 128 bits and a lane read
    of a vector arrival is ordinary rather than refused.
  * THE ARRIVAL BINDING -- input row i is bound to the same symbol as
    the argument the reference text reads in arrival register i.
  * THE PROOF OBLIGATION -- for every value of every input row, the
    value the wrapped text leaves in OUT-0 equals the value the
    reference text leaves in its own answer home.  The answer is read
    out of the ROW, never out of a register.
  * THE STRUCTURAL ROUTE -- a proof BY CONSTRUCTION for the units
    whose mnemonics the solver's own table cannot model.  Under this
    form it is much narrower than round 9's, because the form applies
    NO transformation to the body at all: the checks below verify only
    that the body is present character-for-character and that the
    plumbing cannot disturb it.

THE MONKEYPATCH SEAM, named rather than hidden.  canon33_gate's test
for "is this operand a designated location" is the module function
`G33.is_slot_text`, and its list of mnemonics that may touch one is
`G33.SLOT_MNEMONICS`.  This file WIDENS both, additively:
`-0xN(%rsp)` still tests true and still behaves exactly as before, so
no prior behaviour changes.

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

No operator token appears in this file.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                     # noqa: E402
import canon8_behaviour_check as BC8                             # noqa: E402
import canon10_behaviour_check as BC10                           # noqa: E402
import canon33_gate as G33                                       # noqa: E402
import ledger47 as L47                                           # noqa: E402
import region36 as R36                                           # noqa: E402
import z3                                                        # noqa: E402

_ORIGINAL_IS_SLOT_TEXT = G33.is_slot_text


def is_slot_text(text):
    if _ORIGINAL_IS_SLOT_TEXT(text):
        return True
    return L47.is_row_text(text)


G33.is_slot_text = is_slot_text
G33.SLOT_MNEMONICS = tuple(sorted(set(G33.SLOT_MNEMONICS) | set([
    "mov", "movd", "movq", "movl", "movb", "movw",
    "movss", "movsd", "movdqu", "movdqa", "movaps", "movapd",
])))

ROW_MNEMONIC_WIDTH = {
    "movss": 32,
    "movsd": 64,
    "movq": 64,
    "movd": 32,
    "movdqu": 128,
    "movdqa": 128,
    "movaps": 128,
    "movapd": 128,
}


class Sim47(G33.Sim33):
    """Sim33 whose designated-location model covers the ledger's rows
    at the row's own width."""

    def slot_value(self, slot_text, width):
        if slot_text in self.slots:
            value, stored_width = self.slots[slot_text]
            if stored_width == width:
                return value
            if stored_width > width:
                return z3.Extract(width - 1, 0, value)
            raise G33.NotModeled(
                "row %s was parked at %d bits and is read back at %d"
                % (slot_text, stored_width, width))
        key = "slot_%s" % slot_text
        if key not in self.shared_seed:
            self.shared_seed[key] = z3.BitVec(key, max(width, 64))
        seeded = self.shared_seed[key]
        if seeded.size() < width:
            raise G33.NotModeled(
                "row %s is seeded at %d bits and is read at %d"
                % (slot_text, seeded.size(), width))
        return z3.Extract(width - 1, 0, seeded)

    def exec_line(self, line):
        text = line.strip()
        parts = text.split(" ", 1)
        mnemonic = parts[0]
        width = ROW_MNEMONIC_WIDTH.get(mnemonic)
        if width is None:
            return G33.Sim33.exec_line(self, line)
        rest = parts[1] if len(parts) > 1 else ""
        operands = G33.split_operands(rest)
        if len(operands) != 2:
            return G33.Sim33.exec_line(self, line)
        source, destination = operands
        side = None
        if is_slot_text(destination):
            side = "store"
        if is_slot_text(source):
            side = "load"
        if side is None:
            return G33.Sim33.exec_line(self, line)
        if side == "load":
            value = self.slot_value(source, width)
            if self.is_xmm(destination):
                if width < 128:
                    value = self.zero_extend_to_128(value)
                self.write_xmm(destination, value)
                return None
            self.write(destination, value)
            return None
        if self.is_xmm(source):
            whole = self.read_xmm(source)
            if width >= 128:
                value = whole
            else:
                value = self.lane(whole, 0, width)
            self.slots[destination] = (value, width)
            return None
        value = self.read_at(source, width)
        self.slots[destination] = (value, width)
        return None

    def run_lines(self, text_lines):
        for line in text_lines:
            stripped = line.strip()
            if stripped == "":
                continue
            if stripped == "ret":
                continue
            self.exec_line(stripped)

    def out_row_value(self, out_row):
        if out_row not in self.slots:
            raise G33.NotModeled(
                "the wrapped text never wrote %s, so the answer has no "
                "row to be read from" % out_row)
        return self.slots[out_row]


def bind_arrival(shared_seed, ledger_rows, arrival_families):
    """THE ARRIVAL CONTRACT, bound before anything is proved.

    Input row i is bound to the same symbol as the argument the
    reference text reads in arrival register i.  A vector row is bound
    at its full 128 bits, which is what a 16-byte row holds."""
    made = []
    index = 0
    for row in ledger_rows:
        if row["block"] != "IN":
            continue
        family = arrival_families[index]
        index = index + 1
        if L47.is_vector_family(family):
            if family not in shared_seed:
                shared_seed[family] = z3.BitVec("seed_%s" % family, 128)
            value = shared_seed[family]
            shared_seed["slot_%s" % row["row"]] = value
        else:
            value = BC8.seed_family(shared_seed, family)
            shared_seed["slot_%s" % row["row"]] = value
        made.append({
            "row": row["row"],
            "size": row["size"],
            "bound_to_the_same_symbol_as": "%%%s" % family,
        })
    return made


def compare(reference_lines, wrapped_lines, shared_seed, home, width,
            out_row, what):
    """the one proof obligation, read off the row and never off a
    register."""
    sim_ref = Sim47(shared_seed, "reference")
    sim_wrapped = Sim47(shared_seed, "wrapped")
    sim_ref.answer_family = home
    sim_ref.answer_width = width
    sim_wrapped.answer_family = home
    sim_wrapped.answer_width = width
    try:
        val_ref, w_ref = sim_ref.answer_value(reference_lines)
        sim_wrapped.run_lines(wrapped_lines)
        val_out, w_out = sim_wrapped.out_row_value(out_row)
    except (BC10.NotModeled, G33.NotModeled, BC10.Trap) as bad:
        return "UNDECIDED", "%s: %s" % (what, bad)
    except Exception as bad:                       # noqa: BLE001
        return "UNDECIDED", "%s: %s: %s" % (what, type(bad).__name__, bad)
    bits = min(w_ref, w_out)
    left = z3.Extract(bits - 1, 0, val_ref)
    right = z3.Extract(bits - 1, 0, val_out)
    solver = z3.Solver()
    solver.set("timeout", 20000)
    solver.add(left != right)
    outcome = solver.check()
    if outcome == z3.unsat:
        return ("PROVED_EQUAL",
                "z3 proved the wrapped text's %s equal to %s at %d "
                "bits, for every value of every input row, with each "
                "input row bound to the same symbol as the argument "
                "the reference text reads in its arrival register"
                % (out_row, what, bits))
    if outcome == z3.sat:
        return ("DISPROVED",
                "z3 found a counterexample against %s: %s"
                % (what, solver.model()))
    return ("UNDECIDED",
            "z3 returned %r at a 20000ms timeout against %s"
            % (outcome, what))


def structural_route(fields):
    """A PROOF BY CONSTRUCTION.

    The form applies NO transformation to the body: it is present
    character-for-character.  So the whole obligation is that the
    plumbing cannot disturb it, and these are the checks that say so.
    Each is recorded by name; the route is claimed only when all hold.

    EVIDENCE CLASS: forced by construction over artifacts this lap
    built, except C2's statement about the prelude scratch, which
    rests on the arrival contract being exactly 'the families the body
    reads before it writes them' -- itself read off the body's own
    text, so also forced by construction."""
    checks = []
    body = fields["body_verbatim"]
    placed = L47.split_lines(fields["wrapped_text"])
    prelude = fields["prelude"]
    epilogue = fields["epilogue"]

    body_seen = []
    for line in placed:
        if line in prelude:
            continue
        if line in epilogue:
            continue
        body_seen.append(line)
    if body_seen != body:
        extra = []
        for line in body_seen:
            if line not in body:
                extra.append(line)
        return False, ("C1 fails: the wrapped text does not carry the "
                       "body character-for-character; unaccounted "
                       "lines %r" % extra[:4])
    checks.append("C1: the body appears in the wrapped text "
                  "character-for-character and in its own order -- no "
                  "register was renamed, no immediate was moved, no "
                  "stack address was rewritten")

    written = []
    for line in prelude:
        operands = L47.operands_of(line)
        if not operands:
            continue
        family = L47.family_of_operand(operands[-1])
        if family is None:
            continue
        written.append(family)
    wanted = set(fields["arrival_families"])
    scratch = fields.get("prelude_scratch")
    if scratch is not None:
        wanted.add(scratch)
    for family in written:
        if family not in wanted:
            return False, ("C2 fails: the prelude writes %s, which is "
                           "neither an arrival family nor the one "
                           "scratch the form allows" % family)
    if scratch is not None:
        if scratch not in fields["arrival_families"]:
            checks.append("C2b: the prelude's one scratch %%%s is not "
                          "an arrival family, so the body never reads "
                          "it before writing it" % scratch)
    checks.append("C2: the prelude writes only the registers the "
                  "arrival contract names, one two-step load per "
                  "input row")

    for index, line in enumerate(placed):
        if line != "ret":
            continue
        if index < len(epilogue):
            return False, "C3 fails: a `ret` has no epilogue before it"
        window = placed[index - len(epilogue):index]
        if window != epilogue:
            return False, ("C3 fails: a `ret` at line %d is not "
                           "immediately preceded by the epilogue"
                           % index)
    checks.append("C3: every one of the %d returns is immediately "
                  "preceded by the epilogue, which stores the "
                  "compiler's own result register into %s"
                  % (fields["returns"], fields["out_row"]))

    for line in body:
        if L47.LEDGER_SYMBOL in line:
            return False, ("C4 fails: a body line names the ledger "
                           "symbol: %r" % line)
        for operand in L47.operands_of(line):
            if L47.is_row_text(operand):
                return False, ("C4 fails: a body line names a ledger "
                               "row: %r" % line)
    checks.append("C4: no body line names the ledger symbol or any "
                  "ledger row, so the body and the plumbing touch "
                  "disjoint text")

    epilogue_scratch = fields.get("epilogue_scratch")
    if epilogue_scratch == fields["result_family"]:
        return False, ("C5 fails: the epilogue's pointer register is "
                       "the result register")
    checks.append("C5: the epilogue's pointer register %%%s is not the "
                  "result register %%%s, so loading the block base "
                  "cannot destroy the answer"
                  % (epilogue_scratch, fields["result_family"]))
    return True, checks


def answer_home_of(lang, n, canon4_docs, entry_contract, prior_text):
    """the unit's own answer home, read off its own ship text first."""
    real_text = BC8.real_text_of(lang, n, canon4_docs)
    if real_text is not None:
        lines_real = [ln.strip() for ln in real_text.split(";")]
        home, width = BC10.answer_home_from_real(lines_real)
        if home is not None:
            return home, width, "the unit's own real ship text"
    if prior_text:
        lines_prior = R36.split_lines(prior_text)
        home, width = BC10.answer_home_from_real(lines_prior)
        if home is not None:
            return (home, width,
                    "this unit's own canonical text (its ship code "
                    "names no answer home this checker can read)")
    if entry_contract.get("a") is not None:
        return (entry_contract.get("a"), 64,
                "the unit's own ship code writes no answer home, so "
                "the answer is the arriving value itself")
    return (entry_contract.get("result"), 64,
            "the recorded entry contract (the ship text names no "
            "answer home)")


def arrival_family_list(entry_contract):
    out = []
    for designation in ("a", "b", "c", "d", "e", "f", "g", "h"):
        family = entry_contract.get(designation)
        if family is None:
            continue
        out.append(family)
    return out


_ = canon


# ------------------------------------------------------------------
# THE ARRIVAL CONTRACT, READ OFF THE BODY, IN THE LANGUAGE'S OWN ABI
# ORDER
# ------------------------------------------------------------------
#
# Round 9 read every unit's arrival contract through ONE sequence, the
# System V one (%rdi, %rsi, %rdx, ...).  go does not use it: since go
# 1.17 the go compiler passes integer arguments in %rax, %rbx, %rcx,
# %rdi, %rsi, %r8, %r9, %r10, %r11.  Measured at first observation on
# this lap: go/op_319's body is `add %rbx,%rax; ret`, and the round-9
# contract for it names %rdi and %rsi -- registers the body never
# reads.  The prelude then filled two registers nothing read, and the
# gate's question became vacuous (both texts read %rax and %rbx as
# free symbols, so they agreed for no reason).
#
# So the sequence is chosen by the language, and the contract is read
# off the BODY: a family ARRIVES when the body reads it before it
# writes it.  The recorded contract is kept beside it and any
# disagreement is recorded rather than smoothed over.

GENERAL_SEQUENCE_SYSV = ("rdi", "rsi", "rdx", "rcx", "r8", "r9")
GENERAL_SEQUENCE_GO = ("rax", "rbx", "rcx", "rdi", "rsi", "r8", "r9",
                       "r10", "r11")
VECTOR_SEQUENCE_SYSV = tuple("xmm%d" % i for i in range(0, 8))
VECTOR_SEQUENCE_GO = tuple("xmm%d" % i for i in range(0, 15))

DESIGNATIONS = ("a", "b", "c", "d", "e", "f", "g", "h")


def sequences_for(lang):
    if lang == "go":
        return GENERAL_SEQUENCE_GO, VECTOR_SEQUENCE_GO
    return GENERAL_SEQUENCE_SYSV, VECTOR_SEQUENCE_SYSV


def arrival_contract(lang, text):
    """the arrival contract read off the body, in the language's own
    ABI order.  Machine-form evidence only."""
    general, vector = sequences_for(lang)
    candidates = tuple(general) + tuple(vector)
    arrives = {}
    written = {}
    for family in candidates:
        arrives[family] = False
        written[family] = False
    for raw in R36.split_lines(text):
        line = R36.strip_annotation(raw)
        mnemonic = L47.mnemonic_of(line)
        operands = L47.operands_of(line)
        for position, operand in enumerate(operands):
            if not operand.startswith("%"):
                # A REGISTER INSIDE A MEMORY OPERAND IS ALWAYS A READ:
                # it is part of the address computation, never a
                # destination.  Measured at first observation on this
                # lap: c/op_109's body is
                # `lea (%rdi,%rsi,1),%rax`, and reading only operands
                # that START with `%` found no arrivals at all, so the
                # unit was wrapped with an empty IN block.
                for token in L47.re.findall(r"%[a-z0-9]+", operand):
                    family = canon.FAMILY_OF.get(token[1:])
                    if family not in arrives:
                        continue
                    if not written[family]:
                        arrives[family] = True
                continue
            family = canon.FAMILY_OF.get(operand[1:])
            if family not in arrives:
                continue
            is_last = position == len(operands) - 1
            if is_last:
                if mnemonic in L47.PURE_WRITE_MNEMONICS:
                    written[family] = True
                    continue
            if not written[family]:
                arrives[family] = True
    ordered = []
    for family in general:
        if arrives[family]:
            ordered.append(family)
    for family in vector:
        if arrives[family]:
            ordered.append(family)
    out = {}
    for designation in DESIGNATIONS:
        out[designation] = None
    for index, family in enumerate(ordered):
        if index >= len(DESIGNATIONS):
            break
        out[DESIGNATIONS[index]] = family
    result = "rax"
    if "%rax" not in text:
        if "%eax" not in text:
            if "%al" not in text:
                if "%ax" not in text:
                    result = "xmm0"
    out["result"] = result
    return out


def contract_disagreement(recorded, read_off):
    """what the recorded contract said, where the body disagrees."""
    if not recorded:
        return None
    notes = []
    for designation in DESIGNATIONS:
        was = recorded.get(designation)
        now = read_off.get(designation)
        if was == now:
            continue
        notes.append({
            "designation": designation,
            "the_recorded_contract_said": was,
            "the_body_reads": now,
            "why_the_body_wins": "the recorded contract is human "
                                 "interpretation of stated design; the "
                                 "body is the artifact itself",
        })
    if not notes:
        return None
    return notes
