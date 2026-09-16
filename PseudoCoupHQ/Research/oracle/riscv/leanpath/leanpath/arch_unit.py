"""ArchUnit -- the compiled machine code of one source operator at one
type pair, cut out of the binary at its function symbol, with its
meaning as a Lean expression computed by Sail's own definitions applied
in order. Plan leaf: lean_proof_path.arch_unit, with methods meaning,
decode, compose, branch_rule, memory_and_calls.

`meaning` knows Sail's decoder and `execute` and the shape of a
straight-line body; it knows no instruction. Every semantic step runs
inside Lean against the built model: `decode` is the harness's
`Leanpath.decode` (the model's own `encdec_backwards` for a 32-bit word,
`encdec_compressed_backwards` for a 16-bit one), `compose` is
`Leanpath.walk` (the model's own `execute`, word after word), and the
answer is the register the ABI names, read from the final state. The
harness prints the simp normal form of the run (LITERAL); Python reads
only whether every word retired and what the form's text is.
"""

import os
import re

from .lean_expr import LeanExpr, HEADER, simp_set

# the RISC-V psABI lp64d, as log 258 stated it: integer arguments in
# a0..a7 (x10..x17), the integer answer in a0 (x10). The harness sets
# every argument register to an unknown; a unit reads the ones it uses.
ARG_REGS = ["x10", "x11", "x12", "x13", "x14", "x15", "x16", "x17"]
ANSWER_REG = "x10"


class ArchUnit:
    """attributes: language, source, symbol, instructions (encoded words
    in address order, as hex strings of 4 or 8 digits), lean (LeanExpr,
    set by meaning)."""

    def __init__(self, language, source, symbol, instructions):
        self.language = language
        self.source = source
        self.symbol = symbol
        self.instructions = instructions
        self.lean = None

    # ---------------------------------------------------------------- #
    @staticmethod
    def words(instructions):
        """the carved body's words as Lean `Word`s: a 4-hex-digit word is
        a 16-bit encoding, an 8-digit one 32 bits (the carver's own
        column; the encoding's low two bits say the same)."""
        out = []
        for h in instructions:
            h = h.strip()
            if len(h) == 4:
                out.append(".w16 0x%s#16" % h)
            elif len(h) == 8:
                out.append(".w32 0x%s#32" % h)
            else:
                return None
        return out

    @staticmethod
    def state_term():
        """the base state with the argument registers set to unknowns."""
        pairs = ", ".join("⟨Register.%s, a%d⟩" % (r, i) for i, r in enumerate(ARG_REGS))
        return "(withRegs S0 [%s])" % pairs

    @staticmethod
    def binders():
        return " ".join("(a%d : BitVec 64)" % i for i in range(len(ARG_REGS)))

    @staticmethod
    def form_of(run, project, workdir, name, hyps, unknowns=None):
        """the simp normal form of a run: the pair (the ExecutionResults,
        the answer register's value) after the run on the base state with
        unknowns, printed by the harness's own tactic. Returns a LeanExpr
        with `text` (LITERAL) and `run`, or a refusal with the construct
        named:
          - a word whose ExecutionResult is not Retire_Success (Sail's own
            verdict on that word: Illegal_Instruction for an encoding the
            selected modules do not define, a Trap, ...)
          - a run that ends in the monad's error (a read of a register
            the base does not hold, an assertion)
          - a residual the unfolding does not reach (printed)"""
        unknowns = unknowns or {}
        extra = " ".join("(%s : %s)" % (k, v) for k, v in unknowns.items())
        st = ArchUnit.state_term()
        lhs = "(results %s %s, answer %s %s Register.%s)" % (run, st, run, st, ANSWER_REG)
        thm = "theorem %s %s %s %s : %s = %s := by\n" % (name, hyps, ArchUnit.binders(), extra, lhs, lhs)
        thm += "  conv => lhs; simp (config := {decide := true}) only [%s]\n" % simp_set()
        thm += "  leanpath_show_lhs\n  rfl\n"
        path = os.path.join(workdir, name + ".lean")
        open(path, "w").write(HEADER + thm)
        rc, secs, lines = LeanExpr._run_lean(project, path, timeout_s=1800)
        forms = LeanExpr._blocks(lines, "LHS")
        errs = LeanExpr._errors(lines)
        out = {"file": path, "seconds": secs, "rc": rc, "lean_errors": errs[:8]}
        if not forms:
            out["refusal"] = "the harness printed no form (lean rc=%d)" % rc
            return out
        text = forms[-1]
        out["text"] = text
        m = re.match(r'\(\s*(some\s*\[(.*?)\]|none)\s*,\s*(.*)\)\s*$', text, re.S)
        if not m:
            out["refusal"] = "the form is not a (results, answer) pair the reader knows"
            return out
        if m.group(1).strip() == "none":
            out["refusal"] = "the run ends in the monad's error (a read the base state does not serve, or an assertion); residual LITERAL in `text`"
            return out
        results = [r.strip() for r in re.split(r',\s*(?![^()]*\))', m.group(2)) if r.strip()]
        out["results"] = results
        bad = [(i, r) for i, r in enumerate(results) if not r.startswith("ExecutionResult.Retire_Success") and not r.startswith("Retire_Success")]
        if bad:
            out["refusal"] = "Sail's execute did not retire word %d: %s" % (bad[0][0], bad[0][1])
            return out
        ans = m.group(3).strip()
        out["answer"] = ans
        if ans == "none":
            out["refusal"] = "the answer register is unset after the run"
            return out
        if "readReg" in ans or "EStateM" in ans or "Leanpath.walk" in ans or "execute" in ans:
            out["refusal"] = "a residual the unfolding did not reach: " + ans[:200]
            return out
        out["expr"] = LeanExpr(ans, {"a%d" % i: 64 for i in range(len(ARG_REGS))}, run=("(answer %s %s Register.%s)" % (run, st, ANSWER_REG)), hyps=hyps)
        return out

    # ---------------------------------------------------------------- #
    @staticmethod
    def meaning(unit, project, workdir, name, hyps):
        """meaning(unit, defs) -> the expression the answering register
        holds, over the argument registers left unknown.
          1. decode every word with decode (in Lean, inside the walk)
          2. start a register file of unknowns named for the ABI argument
             registers (withRegs S0 [x10 := a0, ..., x17 := a7])
          3. walk the instructions in address order with compose (the
             harness's `walk`: decode, execute, next); the carve's last
             word is the return the carver stopped at and is not walked;
             at a branch branch_rule; at a load, store or call
             memory_and_calls (both refusals here, named by the run)
          4. return the answering register's expression; a refused walk
             returns the refusal with the construct named"""
        ws = ArchUnit.words(unit.instructions)
        if ws is None:
            return {"refusal": "a word that is neither 16 nor 32 bits wide: %r" % unit.instructions}
        body = ws[:-1] if len(ws) > 1 else ws
        run = "(walk [%s])" % ", ".join(body)
        out = ArchUnit.form_of(run, project, workdir, name, hyps)
        out["words_walked"] = len(body)
        out["boundary_word"] = ws[-1] if len(ws) > 1 else None
        if "expr" in out:
            unit.lean = out["expr"]
        return out

    @staticmethod
    def decode(word):
        """decode(word) -> the Sail `instruction` value as the model's own
        `encdec_backwards` (32 bits) or `encdec_compressed_backwards`
        (16 bits) gives it -- the harness's `Leanpath.decode`, run inside
        the walk; a word the model does not decode is the constructor
        ILLEGAL/C_ILLEGAL whose execute does not retire, a refusal."""
        return "Leanpath.decode (%s)" % word

    @staticmethod
    def decoded_display(unit, project, workdir, name, hyps):
        """the decoded instruction of each word, LITERAL (the model's own
        constructor and operands), for the log and for the immediate
        candidates of pass A (the literals the decoder itself produced)."""
        ws = ArchUnit.words(unit.instructions)
        st = ArchUnit.state_term()
        run = "(List.mapM Leanpath.decode [%s])" % ", ".join(ws)
        lhs = "results %s %s" % (run, st)
        thm = "theorem %s %s %s : %s = %s := by\n" % (name, hyps, ArchUnit.binders(), lhs, lhs)
        thm += "  conv => lhs; simp (config := {decide := true}) only [%s, List.mapM, List.mapM.loop]\n" % simp_set()
        thm += "  leanpath_show_lhs\n  rfl\n"
        path = os.path.join(workdir, name + ".lean")
        open(path, "w").write(HEADER + thm)
        rc, secs, lines = LeanExpr._run_lean(project, path, timeout_s=900)
        forms = LeanExpr._blocks(lines, "LHS")
        return {"file": path, "seconds": secs, "text": forms[-1] if forms else "", "lean_errors": LeanExpr._errors(lines)[:4]}

    @staticmethod
    def compose(state, instruction, defs):
        """compose(state, instruction, defs) -> the register file after
        it: the model's own `execute` dispatch finds the clause by the
        constructor, the reads take the current register expressions,
        the write lands in the destination -- `Leanpath.walk`, one
        step; nothing is dispatched by a name here."""
        return "Leanpath.walk"

    @staticmethod
    def branch_rule(state, branch, defs):
        """branch_rule: a body whose walk writes nextPC (a taken branch or
        a jump) is refused in this launch with the construct named -- the
        run's form carries the `if` on the condition where Sail put it,
        and the fork-and-join of the two sides is not implemented here
        (recorded; the plan's leaf stands)."""
        return {"refusal": "branch_rule: fork-and-join not implemented in lp1; the form shows the condition"}

    @staticmethod
    def memory_and_calls(state, instruction, defs):
        """memory_and_calls: a load or store goes through the model's own
        translation and memory; on the base state it does not retire
        (the run's error or residual names it); a call outside the unit
        is a jump, refused by branch_rule. Both are rows, named by the
        run, never a guess."""
        return {"refusal": "memory_and_calls: not modelled in lp1; the run names the construct"}
