import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_C_NOT (v_r : BitVec 64) (rsdc : cregidx) : BitVec 64 :=

  Complement.complement v_r

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_C_NOT (rsdc : cregidx) :
    execute_C_NOT rsdc =
    (do
      let r := (creg2reg_idx rsdc)
      let v_r ← rX_bits r
      wX_bits r (pure_C_NOT v_r rsdc)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_C_NOT, pure_C_NOT, bind_assoc, pure_bind]

end Leanpath
