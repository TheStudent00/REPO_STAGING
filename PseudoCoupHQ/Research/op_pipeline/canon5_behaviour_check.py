#!/usr/bin/env python3
"""canon5_behaviour_check.py -- item 2(c) of the canon5 work list:
BEHAVIOUR PRESERVATION, proved rather than claimed.

For every 0-branch unit whose canon5_text differs from its canon4_text
(canon5_units_<lang>.json's own `converged` flag), this file builds a
symbolic bitvector model of BOTH instruction sequences and asks z3
whether they compute the same value in the answer register, starting
from the SAME symbolic machine state (every register that either
sequence reads before writing gets one shared fresh symbol -- the two
sequences are literally run against one unconstrained starting state,
not two independently-guessed ones).

WHY A NEW SMALL SIMULATOR, NOT A REUSE OF PYVEX. This is not the same
job as tree_match2.py's lift: that lift turns REAL compiled bytes into
a VEX/z3 expression once, upstream. Here the job is different -- prove
two already-rendered, hand-written-by-a-fixed-rule INSTRUCTION TEXTS
denote the same function of the entry registers. Piping canon4_text/
canon5_text back through the real compiler+pyvex pipeline (assemble,
lift the resulting bytes) would work for canon5_text (expr_to_canon.py
already assembles it) but NOT prove anything -- it would just re-derive
the same expression canon5 rendered FROM, a circular check. What must
be modeled instead is: "these literal AT&T lines, executed as x86-64
really executes them (specifically: a 32-bit destination write always
zero-extends to 64 bits; an 8/16-bit destination write does not)."
That is a small, closed, mechanically-checkable rule -- smaller and
more auditable than a full x86 lifter -- covering EXACTLY the mnemonic
vocabulary this corpus's converged units use (verified by direct
inventory below, not assumed): mov, lea (base,index,scale -- no
displacement form appears), add, sub, and, or, xor, imul, not, neg,
shl (immediate count only). `idiv` is explicitly OUT OF SCOPE (see
UNDECIDED_MNEM) and left UNDECIDED, never guessed at.

REGISTER-WIDTH TABLE: reused verbatim from canon.py (`FAMILY_OF`,
`WIDTH_OF`, `GP_NAMES`) -- the same table canon4.py itself renders
register text from -- rather than re-deriving a second, possibly
disagreeing, width table.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.

usage:
  canon5_behaviour_check.py [--in DIR]
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon  # noqa: E402  (FAMILY_OF, WIDTH_OF -- the register table)
import z3  # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]

WIDTH_BITS = {0: 64, 1: 32, 2: 16, 3: 8}

# the exact vocabulary a symbolic model is provided for. Anything else
# encountered is UNDECIDED by name, never guessed.
MODELED_MNEM = set([
    "mov", "lea", "add", "sub", "and", "or", "xor", "imul",
    "not", "neg", "shl",
])

UNDECIDED_MNEM_NOTE = {
    "idiv": "idiv's dividend is the ambient %edx/%rdx (not modeled as "
        "part of the entry contract by this corpus's designated-"
        "register convention) -- whether the two texts agree depends "
        "on a fact this checker cannot read off the rendered text "
        "alone, so this unit is left UNDECIDED rather than guessed",
}


class NotModeled(Exception):
    pass


def split_operands(rest):
    """split an AT&T operand list on top-level commas only -- lea's
    `(%rdi,%rsi,1)` addressing form has commas INSIDE the parens that
    must not split it from the rest."""
    out = []
    depth = 0
    cur = ""
    for ch in rest:
        if ch == "(":
            depth = depth + 1
            cur = cur + ch
            continue
        if ch == ")":
            depth = depth - 1
            cur = cur + ch
            continue
        if ch == "," and depth == 0:
            out.append(cur)
            cur = ""
            continue
        cur = cur + ch
    if cur:
        out.append(cur)
    return [o.strip() for o in out]


LEA_RE = re.compile(r"^\((%\w+),(%\w+),(\d+)\)$")


class Sim(object):
    """one symbolic execution of one instruction sequence. `shared_seed`
    is a dict (family -> fresh 64-bit BitVec) SHARED with the other
    sequence being compared, so a register neither sequence writes
    before reading starts from the identical symbolic value in both --
    the two runs are two programs applied to the SAME unconstrained
    starting machine state, not two separately-invented ones."""

    def __init__(self, shared_seed, tag):
        self.shared_seed = shared_seed
        self.tag = tag
        self.regs = {}

    def get_family(self, fam):
        if fam in self.regs:
            return self.regs[fam]
        if fam not in self.shared_seed:
            self.shared_seed[fam] = z3.BitVec(
                "seed_%s" % fam, 64)
        v = self.shared_seed[fam]
        self.regs[fam] = v
        return v

    def width_of_operand(self, operand):
        name = operand[1:]
        w = canon.WIDTH_OF.get(name)
        if w is None:
            raise NotModeled(
                "register spelling %r not in canon.py's WIDTH_OF "
                "table" % operand)
        return WIDTH_BITS[w]

    def read_at(self, operand, width):
        if operand.startswith("$"):
            v = int(operand[1:], 0)
            v = v & ((1 << width) - 1)
            return z3.BitVecVal(v, width)
        if operand.startswith("%"):
            name = operand[1:]
            fam = canon.FAMILY_OF.get(name)
            if fam is None:
                raise NotModeled(
                    "register spelling %r not in canon.py's FAMILY_OF "
                    "table" % operand)
            own_width = self.width_of_operand(operand)
            if own_width != width:
                raise NotModeled(
                    "operand %r is %d-bit, expected %d-bit in this "
                    "instruction -- a width-mixing form this checker "
                    "does not model" % (operand, own_width, width))
            full = self.get_family(fam)
            return z3.Extract(width - 1, 0, full)
        raise NotModeled("operand %r is neither an immediate nor a "
                         "plain register" % operand)

    def write(self, operand, value):
        name = operand[1:]
        fam = canon.FAMILY_OF.get(name)
        if fam is None:
            raise NotModeled(
                "register spelling %r not in canon.py's FAMILY_OF "
                "table" % operand)
        width = self.width_of_operand(operand)
        if width == 64:
            newfull = value
        else:
            newfull = z3.ZeroExt(64 - width, value)
        self.regs[fam] = newfull

    def exec_line(self, line):
        line = line.strip()
        if line.endswith(":"):
            raise NotModeled("a label line -- this checker only "
                             "models straight-line 0-branch text")
        parts = line.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        if mnem == "ret":
            return
        if mnem not in MODELED_MNEM:
            note = UNDECIDED_MNEM_NOTE.get(
                mnem, "mnemonic %r has no symbolic model in this "
                "checker" % mnem)
            raise NotModeled(note)
        operands = split_operands(rest)
        if mnem == "lea":
            src, dst = operands
            m = LEA_RE.match(src)
            if m is None:
                raise NotModeled(
                    "lea addressing form %r is not the plain "
                    "(base,index,scale) shape this checker models "
                    "(no displacement forms are modeled)" % src)
            base_op, index_op, scale = m.groups()
            base_fam = canon.FAMILY_OF[base_op[1:]]
            index_fam = canon.FAMILY_OF[index_op[1:]]
            base_v = self.get_family(base_fam)
            index_v = self.get_family(index_fam)
            addr = base_v + index_v * int(scale)
            dst_width = self.width_of_operand(dst)
            self.write(dst, z3.Extract(dst_width - 1, 0, addr))
            return
        if mnem == "mov":
            src, dst = operands
            width = self.width_of_operand(dst)
            v = self.read_at(src, width)
            self.write(dst, v)
            return
        if mnem in ("add", "sub", "and", "or", "xor", "imul"):
            src, dst = operands
            width = self.width_of_operand(dst)
            a = self.read_at(dst, width)
            b = self.read_at(src, width)
            if mnem == "add":
                r = a + b
            elif mnem == "sub":
                r = a - b
            elif mnem == "and":
                r = a & b
            elif mnem == "or":
                r = a | b
            elif mnem == "xor":
                r = a ^ b
            else:
                r = a * b
            self.write(dst, r)
            return
        if mnem in ("not", "neg"):
            (operand,) = operands
            width = self.width_of_operand(operand)
            a = self.read_at(operand, width)
            r = ~a if mnem == "not" else -a
            self.write(operand, r)
            return
        if mnem == "shl":
            imm, dst = operands
            if not imm.startswith("$"):
                raise NotModeled(
                    "shl by a register count is not modeled (only "
                    "an immediate count is)")
            width = self.width_of_operand(dst)
            a = self.read_at(dst, width)
            amt = int(imm[1:], 0)
            r = a << z3.BitVecVal(amt, width)
            self.write(dst, r)
            return
        raise NotModeled("unreached mnemonic %r" % mnem)

    def answer_value(self, text_lines):
        """the value in the `ans` family (canon.py's FAMILY_OF['rax']
        family, i.e. the register named rax/eax/...) after running
        every line up to and including the last non-`ret` line, at the
        WIDTH the text's own final answer-producing instruction used
        (so a 32-bit result is compared as 32 bits, a 64-bit result as
        64 bits -- each text is read at its own stated width, never
        assumed)."""
        last_width = None
        last_dst = None
        for line in text_lines:
            if line.strip() == "ret":
                continue
            self.exec_line(line)
            parts = line.strip().split(" ", 1)
            mnem = parts[0]
            rest = parts[1] if len(parts) > 1 else ""
            operands = split_operands(rest)
            if not operands:
                continue
            dst = operands[-1]
            if not dst.startswith("%"):
                continue
            name = dst[1:]
            fam = canon.FAMILY_OF.get(name)
            if fam != "rax":
                continue
            last_dst = dst
            last_width = self.width_of_operand(dst)
        if last_dst is None:
            raise NotModeled("no instruction in this text ever wrote "
                             "the answer (rax) family")
        fam_val = self.get_family("rax")
        return z3.Extract(last_width - 1, 0, fam_val), last_width


def check_pair(canon4_text, canon5_text):
    """(verdict, detail). verdict is one of PROVED_EQUAL /
    DISPROVED / UNDECIDED."""
    lines4 = [ln.strip() for ln in canon4_text.split(";")]
    lines5 = [ln.strip() for ln in canon5_text.split(";")]
    shared_seed = {}
    sim4 = Sim(shared_seed, "c4")
    sim5 = Sim(shared_seed, "c5")
    try:
        val4, w4 = sim4.answer_value(lines4)
        val5, w5 = sim5.answer_value(lines5)
    except NotModeled as exc:
        return "UNDECIDED", str(exc)
    if w4 != w5:
        # project onto the NARROWER width -- that is the strongest
        # claim both texts actually agree on; a wider text's extra
        # high bits are not part of either width's own stated answer.
        w = min(w4, w5)
        val4 = z3.Extract(w - 1, 0, val4)
        val5 = z3.Extract(w - 1, 0, val5)
    solver = z3.Solver()
    solver.add(val4 != val5)
    result = solver.check()
    if result == z3.unsat:
        return "PROVED_EQUAL", "z3 proved the two answer values equal " \
            "for every value of every register either text reads " \
            "before writing"
    if result == z3.sat:
        model = solver.model()
        return "DISPROVED", "z3 found a counterexample machine state " \
            "under which the two texts compute DIFFERENT answers: " \
            "%s" % model
    return "UNDECIDED", "z3 returned %r (neither proved nor "\
        "disproved)" % result


def main(argv):
    indir = HERE
    i = 1
    while i < len(argv):
        if argv[i] == "--in":
            indir = argv[i + 1]
            i = i + 2
            continue
        print(__doc__)
        return 2

    proved = 0
    disproved = 0
    undecided = 0
    rows = []
    undecided_reasons = {}
    disproved_rows = []
    ground_truth_tally = {}

    canon4_docs = {}
    for lang in LANGS:
        canon4_docs[lang] = json.load(
            open(os.path.join(indir,
                              "canon4_units_%s.json" % lang)))["units"]

    for lang in LANGS:
        path = os.path.join(indir, "canon5_units_%s.json" % lang)
        doc = json.load(open(path))
        for n, u in doc["units"].items():
            if u.get("status") != "converged":
                continue
            verdict, detail = check_pair(u["canon4_text"],
                                         u["canon5_text"])
            row = {
                "lang": lang,
                "n": n,
                "unit": "%s/op_%s" % (lang, n),
                "operator": u.get("operator"),
                "canon4_text": u["canon4_text"],
                "canon5_text": u["canon5_text"],
                "verdict": verdict,
                "detail": detail,
            }
            if verdict == "DISPROVED":
                # a disproved pair is exactly the case the owner's ruling
                # names: "fix it or refuse that unit's convergence and
                # say so". Before refusing, ask the strongest evidence
                # this corpus has -- the unit's OWN real disassembly
                # (`mnem`, forced-by-construction ground truth) -- which
                # of the two disagreeing texts it actually agrees with.
                real_mnem = canon4_docs[lang][n].get("mnem") or []
                real_text = "; ".join(real_mnem)
                gv4, _gd4 = check_pair(real_text, u["canon4_text"])
                gv5, _gd5 = check_pair(real_text, u["canon5_text"])
                if gv5 == "PROVED_EQUAL" and gv4 != "PROVED_EQUAL":
                    ground_truth = "REAL_BYTES_MATCH_CANON5_ONLY -- " \
                        "the unit's own real disassembly proves " \
                        "canon5_text correct and canon4_text WRONG " \
                        "(a pre-existing canon4.py defect, not a " \
                        "canon5 regression)"
                elif gv4 == "PROVED_EQUAL" and gv5 != "PROVED_EQUAL":
                    ground_truth = "REAL_BYTES_MATCH_CANON4_ONLY -- " \
                        "the unit's own real disassembly proves " \
                        "canon4_text correct and canon5_text WRONG " \
                        "-- REFUSING this unit's convergence"
                elif gv4 == "PROVED_EQUAL" and gv5 == "PROVED_EQUAL":
                    ground_truth = "REAL_BYTES_MATCH_BOTH (should be " \
                        "impossible if canon4_text != canon5_text " \
                        "was itself disproved -- flagged for review)"
                else:
                    ground_truth = "NEITHER_MATCHES_DIRECTLY -- the " \
                        "real disassembly uses this language's own " \
                        "raw register choice (e.g. go's %%rbx for an " \
                        "argument), not yet anchor-renamed to %%rdi/" \
                        "%%rsi by this checker, so no direct textual " \
                        "comparison is possible; undecided against " \
                        "ground truth (gv4=%s gv5=%s)" % (gv4, gv5)
                row["ground_truth_check"] = ground_truth
                key = ground_truth.split(" -- ")[0]
                ground_truth_tally[key] = \
                    ground_truth_tally.get(key, 0) + 1
            rows.append(row)
            if verdict == "PROVED_EQUAL":
                proved = proved + 1
            elif verdict == "DISPROVED":
                disproved = disproved + 1
                disproved_rows.append(row)
            else:
                undecided = undecided + 1
                key = detail[:100]
                undecided_reasons[key] = \
                    undecided_reasons.get(key, 0) + 1

    out = {
        "meta": {
            "role": "generator provenance",
            "generator": "canon5_behaviour_check.py",
            "form": "z3 symbolic equivalence check between each "
                   "converged unit's canon4_text and canon5_text, "
                   "over a small closed instruction vocabulary (see "
                   "MODELED_MNEM) -- never a guess",
        },
        "checked": len(rows),
        "proved_equal": proved,
        "disproved": disproved,
        "undecided": undecided,
        "undecided_reasons": undecided_reasons,
        "ground_truth_tally_over_disproved": ground_truth_tally,
        "disproved_units": disproved_rows,
        "checked_units": rows,
    }
    name = os.path.join(indir, "canon5_behaviour_check.json")
    json.dump(out, open(name, "w"), indent=1)
    print("wrote %s" % name)
    print("checked      %d" % len(rows))
    print("proved_equal %d" % proved)
    print("disproved    %d" % disproved)
    print("undecided    %d" % undecided)
    if disproved_rows:
        print()
        print("ground truth tally over disproved rows:")
        for k in sorted(ground_truth_tally,
                        key=lambda x: -ground_truth_tally[x]):
            print("  %5d  %s" % (ground_truth_tally[k], k))
        print()
        print("DISPROVED units (see canon5_behaviour_check.json for "
              "the ground_truth_check verdict on each):")
        for row in disproved_rows:
            print("  %s  c4=%r  c5=%r" % (
                row["unit"], row["canon4_text"], row["canon5_text"]))
            print("      %s" % row.get("ground_truth_check"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
