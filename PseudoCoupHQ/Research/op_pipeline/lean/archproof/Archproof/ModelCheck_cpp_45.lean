import Archproof.Model
import Std.Tactic.BVDecide

set_option maxRecDepth 40000
set_option linter.unusedVariables false

namespace Archproof

/-- cpp single-opcode row 45, arch mnemonic 'neg', example unit cpp/op_12, 16 members

    Left of the equals sign: the unit's own PROVED TERM, the one the pipeline
    stored as a printed line, put into Lean by term_to_lean.py.
    Right of it: the MODEL's operations, applied in the order this unit's own
    body spells them.  Every name on the right is a definition Model.lean got
    by running the reference simulator's builder for that one opcode.
    So this theorem is the two readings of one unit, and a failure is a
    discrepancy between them. -/
theorem ModelCheck_cpp_45 (v0 : BitVec 64) :
    ((v0.extractLsb 31 0) * (4294967295#32))
  = ((model_neg_14 (model_mov_15 v0)).extractLsb 31 0) := by
  simp only [model_mov_15, model_neg_14]
  bv_decide

#print axioms ModelCheck_cpp_45

end Archproof
