#!/usr/bin/env python3
"""canon6_behaviour_check.py -- BEHAVIOUR PRESERVATION for canon6.

AgentMemory's op_pipeline lap, 2026-08-28, step 6 of the work order:
"for every unit whose text changed: z3-check old vs new lifted
forms; report proved/disproved/undecided ... cross-check any
disproved against the unit's own real disassembly."

REUSES canon5_behaviour_check.py's Sim/check_pair/ground-truth-cross-
check MACHINERY UNCHANGED (imported, not copied) -- that file is not
modified. This file only EXTENDS the modeled mnemonic vocabulary,
because canon6's renderer introduces mnemonics canon5's simulator
never had to model: `cmp`/`test` (flag-setting) and `set<cc>`/
`cmov<cc>` (flag-reading) from CAUSE 1's condition substitution, plus
`shr`/`sar`/`movzx`/`movsx`/`movsxd` from CAUSE 4's block-aware
renderer reusing the same general codegen. The flag semantics are
NOT re-invented here: `ExtSim.cond_to_z3` calls are the SAME proved
(against angr's ccall) predicate table condition_table.py already
carries, applied to whichever two operands the immediately preceding
`cmp`/`test` compared (real x86 semantics: flags persist until the
next flag-setting instruction).

SCOPE, stated honestly: straight-line unit pairs (canon5_text vs
canon6_text) are checked directly, the same way canon5_behaviour_
check.py already does. For a BRANCHING (guarded) unit, this file
does NOT attempt whole-program control-flow equivalence (a materially
bigger proof); instead it checks EVERY BLOCK CAUSE 4's renderer
actually changed, old canon4 block text vs new rendered block text,
as its own straight-line pair (both are guaranteed to be closed --
compute-then-`ret` -- straight-line sequences by construction, since
guard/dispatch/trap/call blocks are never touched). Every OTHER
block (control flow, guards) is byte-identical to canon4's own,
already independently verified by real `as`/`objdump` in
render_branching_unit -- there is nothing new to prove behaviourally
about a block this pass did not rewrite.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.

usage:
  canon6_behaviour_check.py [--in DIR]
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                   # noqa: E402
import condition_table as CT                                   # noqa: E402
import canon5_behaviour_check as BC                             # noqa: E402
import z3                                                       # noqa: E402

LANGS = BC.LANGS
split_operands = BC.split_operands
NotModeled = BC.NotModeled


class ExtSim(BC.Sim):
    """canon5_behaviour_check.Sim, plus cmp/test/setcc/cmov/shr/sar/
    movzx/movsx/movsxd. Falls back to the base class for everything
    already modeled there."""

    def __init__(self, shared_seed, tag):
        BC.Sim.__init__(self, shared_seed, tag)
        self.last_cmp = None   # (L, R) z3 expressions, same width

    def exec_line(self, line):
        line = line.strip()
        if line.endswith(":"):
            raise NotModeled("a label line -- block-level checks "
                             "strip labels before calling this")
        parts = line.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        if mnem == "ret":
            return
        if mnem in ("cmp", "test"):
            operands = split_operands(rest)
            src, dst = operands
            width = self.width_of_operand(dst)
            dst_v = self.read_at(dst, width)
            src_v = self.read_at(src, width)
            if mnem == "cmp":
                self.last_cmp = (dst_v, src_v)
            else:
                self.last_cmp = (dst_v & src_v,
                                 z3.BitVecVal(0, width))
            return
        if mnem.startswith("set") and mnem[3:] in CT.SUFFIX_TO_COND:
            (dst,) = split_operands(rest)
            if self.last_cmp is None:
                raise NotModeled(
                    "setcc with no preceding cmp/test in this text "
                    "-- flags carried in from outside this sequence, "
                    "not modeled")
            cond = CT.SUFFIX_TO_COND[mnem[3:]]
            L, R = self.last_cmp
            pred = CT.cond_to_z3(cond, L, R, z3)
            bit = z3.If(pred, z3.BitVecVal(1, 8), z3.BitVecVal(0, 8))
            self.write(dst, bit)
            return
        if mnem.startswith("cmov") and mnem[4:] in CT.SUFFIX_TO_COND:
            operands = split_operands(rest)
            src, dst = operands
            if self.last_cmp is None:
                raise NotModeled(
                    "cmov with no preceding cmp/test in this text "
                    "-- flags carried in from outside this sequence, "
                    "not modeled")
            cond = CT.SUFFIX_TO_COND[mnem[4:]]
            L, R = self.last_cmp
            pred = CT.cond_to_z3(cond, L, R, z3)
            width = self.width_of_operand(dst)
            old_v = self.read_at(dst, width)
            new_v = self.read_at(src, width)
            self.write(dst, z3.If(pred, new_v, old_v))
            return
        if mnem in ("shr", "sar", "shl") and \
                split_operands(rest)[0] == "%cl":
            cl_op, dst = split_operands(rest)
            width = self.width_of_operand(dst)
            a = self.read_at(dst, width)
            amt = z3.Extract(width - 1, 0,
                             z3.ZeroExt(width - 8, self.read_at(cl_op, 8)))
            if mnem == "shl":
                r = a << amt
            elif mnem == "shr":
                r = z3.LShR(a, amt)
            else:
                r = a >> amt
            self.write(dst, r)
            return
        if mnem in ("shr", "sar"):
            operands = split_operands(rest)
            imm, dst = operands
            if not imm.startswith("$"):
                raise NotModeled(
                    "%s by a register count is not modeled" % mnem)
            width = self.width_of_operand(dst)
            a = self.read_at(dst, width)
            amt = int(imm[1:], 0)
            r = z3.LShR(a, amt) if mnem == "shr" else a >> amt
            self.write(dst, r)
            return
        # AT&T's SIZE-SUFFIXED mov spellings (movzbl, movzwq, movsbl,
        # movslq, ...) are the SAME zero/sign-extend operation as
        # movzx/movsx/movsxd -- the suffix names widths the operands
        # already state, so a bare alias is exact, not a guess.
        zero_ext_mnem = ("movzx", "movzbl", "movzbw", "movzbq",
                         "movzwl", "movzwq")
        sign_ext_mnem = ("movsx", "movsxd", "movsbl", "movsbw",
                         "movsbq", "movswl", "movswq", "movslq")
        if mnem in zero_ext_mnem or mnem in sign_ext_mnem:
            operands = split_operands(rest)
            src, dst = operands
            src_w = self.width_of_operand(src)
            dst_w = self.width_of_operand(dst)
            v = self.read_at(src, src_w)
            if mnem in zero_ext_mnem:
                r = z3.ZeroExt(dst_w - src_w, v)
            else:
                r = z3.SignExt(dst_w - src_w, v)
            self.write(dst, r)
            return
        BC.Sim.exec_line(self, line)


def check_pair(text_a, text_b):
    lines_a = [ln.strip() for ln in text_a.split(";")]
    lines_b = [ln.strip() for ln in text_b.split(";")]
    shared_seed = {}
    sim_a = ExtSim(shared_seed, "a")
    sim_b = ExtSim(shared_seed, "b")
    try:
        val_a, w_a = sim_a.answer_value(lines_a)
        val_b, w_b = sim_b.answer_value(lines_b)
    except NotModeled as exc:
        return "UNDECIDED", str(exc)
    if w_a != w_b:
        w = min(w_a, w_b)
        val_a = z3.Extract(w - 1, 0, val_a)
        val_b = z3.Extract(w - 1, 0, val_b)
    solver = z3.Solver()
    solver.add(val_a != val_b)
    result = solver.check()
    if result == z3.unsat:
        return "PROVED_EQUAL", "z3 proved the two answer values " \
            "equal for every value of every register either text " \
            "reads before writing"
    if result == z3.sat:
        model = solver.model()
        return "DISPROVED", "z3 found a counterexample machine " \
            "state under which the two texts compute DIFFERENT " \
            "answers: %s" % model
    return "UNDECIDED", "z3 returned %r" % result


def strip_block_labels(steps):
    return [s for s in steps if not s.strip().endswith(":")]


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

    canon4_docs = {}
    for lang in LANGS:
        canon4_docs[lang] = json.load(open(
            os.path.join(indir, "canon4_units_%s.json" % lang)
        ))["units"]

    canon5_docs = {}
    canon6_docs = {}
    for lang in LANGS:
        canon5_docs[lang] = json.load(open(
            os.path.join(indir, "canon5_units_%s.json" % lang)
        ))["units"]
        canon6_docs[lang] = json.load(open(
            os.path.join(indir, "canon6_units_%s.json" % lang)
        ))["units"]

    rows = []
    tally = {"PROVED_EQUAL": 0, "DISPROVED": 0, "UNDECIDED": 0}
    undecided_reasons = {}
    ground_truth_tally = {}

    for lang in LANGS:
        for n, u6 in canon6_docs[lang].items():
            u5 = canon5_docs[lang].get(n)
            old_text = u5.get("canon5_text") if u5 else None
            new_text = u6.get("canon6_text")

            if u6.get("branch_kind") == "branching":
                per_block = u6.get("per_block_report") or []
                for b in per_block:
                    if b.get("source") != "rerendered" or \
                            not b.get("changed"):
                        continue
                    label = b["label"]
                    c4rec = canon4_docs[lang][n]
                    old_block = None
                    for db in c4rec.get("derived_blocks", []):
                        if db["label"] == label:
                            old_block = db["steps"]
                            break
                    new_block_lines = None
                    if isinstance(new_text, str):
                        lines = new_text.split("; ")
                        try:
                            idx = lines.index(label + ":")
                            j = idx + 1
                            grabbed = []
                            while j < len(lines) and not lines[j] \
                                    .strip().endswith(":"):
                                grabbed.append(lines[j].strip())
                                j += 1
                            new_block_lines = grabbed
                        except ValueError:
                            new_block_lines = None
                    if old_block is None or new_block_lines is None:
                        verdict, detail = "UNDECIDED", \
                            "could not isolate block %r's old/new " \
                            "text for a standalone comparison" % label
                    else:
                        verdict, detail = check_pair(
                            "; ".join(old_block),
                            "; ".join(new_block_lines))
                    rows.append(dict(
                        lang=lang, n=n, unit="%s/op_%s block %s"
                        % (lang, n, label),
                        operator=u6.get("operator"),
                        old_text="; ".join(old_block or []),
                        new_text="; ".join(new_block_lines or []),
                        verdict=verdict, detail=detail))
                    tally[verdict] = tally.get(verdict, 0) + 1
                    if verdict == "UNDECIDED":
                        key = detail[:100]
                        undecided_reasons[key] = \
                            undecided_reasons.get(key, 0) + 1
                continue

            if old_text == new_text:
                continue
            if old_text is None or new_text is None:
                continue
            verdict, detail = check_pair(old_text, new_text)
            row = dict(lang=lang, n=n, unit="%s/op_%s" % (lang, n),
                       operator=u6.get("operator"),
                       old_text=old_text, new_text=new_text,
                       verdict=verdict, detail=detail)
            if verdict == "DISPROVED":
                real_mnem = canon4_docs[lang][n].get("mnem") or []
                real_text = "; ".join(real_mnem)
                gv_old, _ = check_pair(real_text, old_text)
                gv_new, _ = check_pair(real_text, new_text)
                if gv_new == "PROVED_EQUAL" and gv_old != "PROVED_EQUAL":
                    gt = "REAL_BYTES_MATCH_NEW_ONLY -- the unit's own " \
                        "real disassembly proves canon6_text correct " \
                        "and canon5_text WRONG (a pre-existing defect, " \
                        "not a canon6 regression)"
                elif gv_old == "PROVED_EQUAL" and gv_new != "PROVED_EQUAL":
                    gt = "REAL_BYTES_MATCH_OLD_ONLY -- the unit's own " \
                        "real disassembly proves canon5_text correct " \
                        "and canon6_text WRONG -- REFUSING this " \
                        "unit's convergence"
                elif gv_old == "PROVED_EQUAL" and gv_new == "PROVED_EQUAL":
                    gt = "REAL_BYTES_MATCH_BOTH (should be impossible " \
                        "-- flagged for review)"
                else:
                    gt = "NEITHER_MATCHES_DIRECTLY (gv_old=%s gv_new=%s)" \
                        % (gv_old, gv_new)
                row["ground_truth_check"] = gt
                key = gt.split(" -- ")[0]
                ground_truth_tally[key] = \
                    ground_truth_tally.get(key, 0) + 1
            rows.append(row)
            tally[verdict] = tally.get(verdict, 0) + 1
            if verdict == "UNDECIDED":
                key = detail[:100]
                undecided_reasons[key] = \
                    undecided_reasons.get(key, 0) + 1

    out = {
        "meta": {
            "role": "generator provenance",
            "generator": "canon6_behaviour_check.py",
            "form": "z3 symbolic equivalence check, canon5_text vs "
                   "canon6_text (whole units) and, for branching "
                   "units, per-block for every block CAUSE 4's "
                   "renderer actually changed",
        },
        "tally": tally,
        "undecided_reasons": undecided_reasons,
        "ground_truth_tally": ground_truth_tally,
        "rows": rows,
    }
    out_path = os.path.join(indir, "canon6_behaviour_check.json")
    json.dump(out, open(out_path, "w"), indent=1)
    print("wrote", out_path)
    print("tally:", tally)
    print("undecided reasons:")
    for k, v in sorted(undecided_reasons.items(), key=lambda x: -x[1]):
        print(" %4d  %s" % (v, k))
    print("ground truth tally (disproved only):", ground_truth_tally)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
