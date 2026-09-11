import Archproof.Model
import Std.Tactic.BVDecide

set_option maxRecDepth 40000
set_option linter.unusedVariables false

namespace Archproof

/-- rust single-opcode row 30, arch mnemonic 'sar', example unit rust/op_505, 14 members

    Left of the equals sign: the unit's own PROVED TERM, the one the pipeline
    stored as a printed line, put into Lean by term_to_lean.py.
    Right of it: the MODEL's operations, applied in the order this unit's own
    body spells them.  Every name on the right is a definition Model.lean got
    by running the reference simulator's builder for that one opcode.
    So this theorem is the two readings of one unit, and a failure is a
    discrepancy between them. -/
theorem ModelCheck_rust_30 (v0 : BitVec 64) (v1 : BitVec 64) :
    (v0.sshiftRight' ((0#58) ++ (v1.extractLsb 5 0)))
  = (model_sar_11 (model_mov_22 v0) (model_mov_22 v1)) := by
  simp only [model_mov_22, model_sar_11]
  bv_decide

#print axioms ModelCheck_rust_30

end Archproof
