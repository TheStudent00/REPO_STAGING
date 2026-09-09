import Archproof.Model
import Std.Tactic.BVDecide

set_option maxRecDepth 40000
set_option linter.unusedVariables false

namespace Archproof

/-- c single-opcode row 74, arch mnemonic 'xor', example unit c/op_251, 38 members

    Left of the equals sign: the unit's own PROVED TERM, the one the pipeline
    stored as a printed line, put into Lean by term_to_lean.py.
    Right of it: the MODEL's operations, applied in the order this unit's own
    body spells them.  Every name on the right is a definition Model.lean got
    by running the reference simulator's builder for that one opcode.
    So this theorem is the two readings of one unit, and a failure is a
    discrepancy between them. -/
theorem ModelCheck_c_74 (v0 : BitVec 64) :
    (0#32)
  = ((model_xor_40 v0).extractLsb 31 0) := by
  simp only [model_xor_40]
  bv_decide

#print axioms ModelCheck_c_74

end Archproof
