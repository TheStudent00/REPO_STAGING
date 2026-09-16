"""LeanExpr -- an expression in Lean over unknowns of fixed width, with
one question answerable of any two: are they the same function of their
unknowns. Plan leaf: lean_proof_path.lean_expr, with methods equals,
widen, normalize_integer_level, decide_fixed_width, primitives, and the
rule once_proved_theorems.

Every method here is a Lean file Lean checks against the built model
(the working copy of the cache under /persist on the tower). A
`LeanExpr` is what the harness printed after `simp` unfolded a run of
the model (`text`, LITERAL), together with the RUN that produced it
(`run`: a Lean term of type `SailM _` over the base state with the
argument registers left unknown) -- the run is what the theorems are
stated over, so the printed text is never re-parsed into a definition.

The runner (`_run_lean`) is the one place Lean is invoked: one `lean`
process per file, through `lake env` of the working copy, with a wall
budget; it returns the messages Lean printed. Python reads only the
markers the harness's own tactics log (LEANPATH_*), the `error:` lines,
and the profiler's seconds.
"""

import os
import re
import subprocess
import time

AWAITS_BUILT_MODEL = "AWAITS_BUILT_MODEL"

# the simp set every run is unfolded with: the model's definitions
# (leanpath_model), the run lemmas (leanpath_run), the support library's
# own set (simp_sail), the base facts (leanpath_base), plus the standard
# monad instance unfoldings of EStateM.
SIMP_SET = ("leanpath_model, leanpath_run, leanpath_base, simp_sail, "
            "Leanpath.decode, Leanpath.walk, Leanpath.results, Leanpath.answer, "
            "Leanpath.withRegs, Leanpath.stateOf, "
            "EStateM.bind, EStateM.pure, EStateM.get, EStateM.set, EStateM.modifyGet, "
            "EStateM.throw, EStateM.map, EStateM.seqRight, EStateM.instMonad, "
            "bind, pure, get, getThe, modify, modifyGet, set, throw, throwThe, "
            "MonadStateOf.get, MonadStateOf.set, MonadStateOf.modifyGet, "
            "MonadState.get, MonadState.set, MonadState.modifyGet, "
            "MonadExceptOf.throw, MonadExcept.throw, "
            "Functor.map, Seq.seq, SeqRight.seqRight, SeqLeft.seqLeft, "
            "ExceptT.run, ExceptT.mk, ExceptT.bind, ExceptT.pure, ExceptT.lift, "
            "ExceptT.bindCont, ExceptT.map, ExceptT.instMonad, "
            "monadLift, MonadLift.monadLift, MonadLiftT.monadLift, "
            "EStateM.instMonadStateOf, EStateM.instMonadExceptOf, EStateM.tryCatch, EStateM.instMonad, "
            "ite_true, ite_false, dite_true, dite_false, ite_self, if_true, if_false, "
            "Bool.false_eq_true, Bool.true_eq_false, Bool.and_true, Bool.and_false, Bool.true_and, Bool.false_and, "
            "Bool.or_true, Bool.or_false, Bool.true_or, Bool.false_or, Bool.not_true, Bool.not_false, Bool.not_not, "
            "and_true, true_and, and_false, false_and, or_true, true_or, or_false, false_or, not_true, not_false, "
            "not_true_eq_false, not_false_eq_true, decide_eq_true_eq, decide_true, decide_false, decide_True, decide_False, "
            "beq_iff_eq, beq_self_eq_true, bne_iff_ne, bne_self_eq_false, eq_self_iff_true, ne_eq, "
            "Option.some.injEq, Option.some_ne_none, List.mapM, List.mapM.loop, List.forM, Prod.mk.injEq, "
            "Function.comp, Function.comp_apply, id_eq, cast_eq")

# the hypothesis names of the run (the support library's axioms assumed
# state-preserving), set by the driver once the axioms are listed
EXTRA_SIMP = []


def simp_set():
    return SIMP_SET + ("".join(", " + h for h in EXTRA_SIMP))


HEADER = """import Leanpath
import LeanpathBase
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIM LeanIM.Functions Leanpath
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option pp.maxSteps 10000000
set_option pp.deepTerms true
set_option pp.proofs false
set_option format.width 1000000
set_option profiler true
set_option profiler.threshold 0
"""

HEADER_NOBASE = HEADER.replace("import LeanpathBase\n", "")


class LeanExpr:
    """attributes: text (the Lean expression as the harness printed it,
    LITERAL), unknowns (name -> width), run (the Lean term of the run it
    is the normal form of), hyps (the hypotheses the run is under)."""

    def __init__(self, text, unknowns, run=None, hyps=""):
        self.text = text
        self.unknowns = unknowns
        self.run = run
        self.hyps = hyps

    # ---------------------------------------------------------------- #
    # the runner
    # ---------------------------------------------------------------- #
    @staticmethod
    def _run_lean(project, path, timeout_s=1800):
        """one `lean` process on one file, under the working copy's lake
        environment; (rc, seconds, stdout+stderr as lines)."""
        t0 = time.time()
        try:
            p = subprocess.run(["lake", "env", "lean", path], cwd=project,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               timeout=timeout_s)
            rc, out = p.returncode, p.stdout.decode("utf-8", "replace")
        except subprocess.TimeoutExpired as exc:
            rc, out = 124, (exc.stdout or b"").decode("utf-8", "replace") + "\nTIMEOUT after %ds" % timeout_s
        return rc, time.time() - t0, out.splitlines()

    @staticmethod
    def _blocks(lines, tag):
        """every LEANPATH_<tag>_BEGIN .. _END block, joined, in order."""
        out = []
        cur = None
        for line in lines:
            if line.endswith("LEANPATH_%s_BEGIN" % tag):
                cur = []
            elif line.strip() == "LEANPATH_%s_END" % tag:
                if cur is not None:
                    out.append("\n".join(cur).strip())
                cur = None
            elif cur is not None:
                cur.append(line)
        return out

    @staticmethod
    def _errors(lines):
        return [l for l in lines if ": error:" in l or l.startswith("error:")]

    @staticmethod
    def _seconds(lines):
        """the profiler's 'took Xs' per line number, summed per declaration
        line; {line: seconds}."""
        out = {}
        for l in lines:
            m = re.match(r'.*?:(\d+):\d+: info: .* took ([0-9.]+)(m?s)\b', l)
            if m:
                v = float(m.group(2)) * (0.001 if m.group(3) == "ms" else 1.0)
                out[int(m.group(1))] = out.get(int(m.group(1)), 0.0) + v
        return out

    # ---------------------------------------------------------------- #
    # equals(left, right, budget) -> Proof | Differ | Undecided
    # ---------------------------------------------------------------- #
    @staticmethod
    def equals(left, right, budget_s, project, workdir, name, extra_hyps=""):
        """equals(left, right, budget) -> a checked Lean proof, a
        counterexample, or undecided with the stage it stopped at.

        Both sides are RUNS over the same base state with the same
        unknowns; the theorem is `left.run = right.run` after both are
        unfolded by `simp` with the model's definitions. Stages, in the
        plan's order, each announced by the harness's own tactic:
          1. integer level: the two simp normal forms coincide (`rfl`),
             else `grind` (ring normalization over Int, guards as cases)
          2. fixed width: `widen` (Lean's library facts on ofInt/toInt)
             then `bv_decide` with the budget
          3. the once-proved theorems: none exist yet (a closed set,
             empty for these languages; log 274 section 5.4)
          4. undecided, with the stage named
        A counterexample (`Differ`) comes from the point test the caller
        ran on the certified forms (decide_fixed_width) before this.
        """
        hyps = (left.hyps or "") + " " + (extra_hyps or "")
        thm = "theorem %s %s : %s = %s := by\n" % (name, hyps, left.run, right.run)
        thm += "  simp (config := {decide := true}) only [%s]\n" % simp_set()
        thm += "  first\n"
        thm += "    | (rfl; leanpath_stage \"integer-level: the two normal forms coincide (rfl)\")\n"
        thm += "    | (grind; leanpath_stage \"integer-level: grind\")\n"
        thm += "    | (leanpath_widen; bv_decide (config := {timeout := %d}); leanpath_stage \"fixed-width: widen then bv_decide\")\n" % int(budget_s)
        thm += "    | (bv_decide (config := {timeout := %d}); leanpath_stage \"fixed-width: bv_decide\")\n" % int(budget_s)
        thm += "    | (leanpath_show_goal; fail \"LEANPATH_UNDECIDED\")\n"
        path = os.path.join(workdir, name + ".lean")
        open(path, "w").write(HEADER + WIDEN + thm)
        rc, secs, lines = LeanExpr._run_lean(project, path, timeout_s=budget_s * 4 + 600)
        stages = [l.split("LEANPATH_STAGE ", 1)[1] for l in lines if "LEANPATH_STAGE " in l]
        errs = LeanExpr._errors(lines)
        goals = LeanExpr._blocks(lines, "GOAL")
        if rc == 0 and stages and not errs:
            return {"outcome": "Proof", "stage": stages[-1], "file": path, "seconds": secs}
        if rc == 124:
            return {"outcome": "Undecided", "stage": "budget: the lean process ran out at %ds" % (budget_s * 4 + 600), "file": path, "seconds": secs}
        return {"outcome": "Undecided", "stage": "undecided after every stage", "file": path, "seconds": secs,
                "residual_goal": goals[-1] if goals else "", "lean_errors": errs[:6]}

    @staticmethod
    def widen(expr):
        """widen(expr): the rule that rewrites width-free integer operations
        as fixed-width ones, citing Lean's own facts -- it is the tactic
        `leanpath_widen` (WIDEN below), applied inside `equals` at stage
        2; nothing per primitive is authored here."""
        return {"tactic": "leanpath_widen", "facts": WIDEN_FACTS}

    @staticmethod
    def normalize_integer_level(expr):
        """normalize_integer_level(expr) -> the simp normal form the harness
        printed (`text`): the model's definitions unfolded to Lean's own
        Int and BitVec operations with the guards kept as `if`; two runs
        whose forms coincide are equal by rfl, else grind's ring
        normalization decides at stage 1 of `equals`."""
        return expr.text

    @staticmethod
    def decide_fixed_width(left, right, project, workdir, name, points):
        """decide_fixed_width: the counterexample search at fixed width,
        by evaluation of the two CERTIFIED forms at the given points
        (kernel reduction, `decide`); a point where they differ is the
        `Differ` verdict with that input, LITERAL. The bit-blast itself
        (`bv_decide`) is stage 2 of `equals`."""
        src = HEADER
        for i, pt in enumerate(points):
            args = " ".join(pt)
            src += "example : (%s) %s = (%s) %s := by first | (decide; leanpath_stage \"point %d agree\") | (leanpath_show_goal; fail \"LEANPATH_POINT %d DIFFER\")\n" % (
                left.form_fn, args, right.form_fn, args, i, i)
        path = os.path.join(workdir, name + "_points.lean")
        open(path, "w").write(src)
        rc, secs, lines = LeanExpr._run_lean(project, path, timeout_s=600)
        differ = [l for l in lines if "LEANPATH_POINT" in l and "DIFFER" in l]
        agree = [l for l in lines if "LEANPATH_STAGE point" in l]
        goals = LeanExpr._blocks(lines, "GOAL")
        if differ:
            k = int(re.search(r'LEANPATH_POINT (\d+)', differ[0]).group(1))
            return {"outcome": "Differ", "input": " ".join(points[k]), "goal": goals[0] if goals else "", "seconds": secs}
        if len(agree) == len(points):
            return {"outcome": "agree", "points": len(points), "seconds": secs}
        return {"outcome": "Undecided", "stage": "point test did not evaluate", "lean_errors": LeanExpr._errors(lines)[:4], "seconds": secs}

    @staticmethod
    def primitives(expr):
        """primitives(expr) -> the atoms the printed form is made of: every
        dotted or plain identifier of Lean's Int/BitVec vocabulary and the
        support library's, with a count (a census over the LITERAL text,
        for the swap table's key and the report; no semantics read)."""
        toks = re.findall(r'[A-Za-z_][A-Za-z0-9_.]*|[+\-*/%^<>=&|]+|≥b|≤b|<b|>b|\+\+\+|&&&|\|\|\||\^\^\^|<<<|>>>', expr.text or "")
        out = {}
        for t in toks:
            if t in ("some", "none", "Option", "if", "then", "else", "match", "with", "fun", "let", "true", "false", "decide"):
                continue
            if re.match(r'^[a-z][0-9]$', t):
                continue                                    # an unknown a0..a7
            if t.startswith("BitVec") or t.startswith("Int") or t.startswith("Sail") or t.startswith("Nat") or not t[0].isalpha():
                out[t] = out.get(t, 0) + 1
        return out


# the widening facts: Lean's own, about its own Int and BitVec; tried as a
# simp set inside `equals` (stage 2). A name absent from this toolchain's
# library is skipped by the `first` combinator, never authored here.
WIDEN_FACTS = ["BitVec.ofInt_mul", "BitVec.ofInt_add", "BitVec.ofInt_sub", "BitVec.ofInt_neg",
               "BitVec.ofInt_toInt", "BitVec.ofInt_ofNat", "BitVec.signExtend_eq_setWidth_of_msb_false",
               "BitVec.toInt_signExtend", "BitVec.toNat_setWidth", "BitVec.ofNat_toNat",
               "Sail.BitVec.toNatInt", "Sail.get_slice_int"]
WIDEN = "macro \"leanpath_widen\" : tactic => `(tactic| first | (simp only [%s]) | skip)\n" % ", ".join(WIDEN_FACTS)
