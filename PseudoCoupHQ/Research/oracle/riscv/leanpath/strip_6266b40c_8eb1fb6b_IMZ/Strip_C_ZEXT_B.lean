import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_C_ZEXT_B (v_rsd : BitVec 64) (rsdc : cregidx) : BitVec 64 :=

  zero_extend (m := 64) (Sail.BitVec.extractLsb v_rsd 7 0)

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_C_ZEXT_B (rsdc : cregidx) :
    execute_C_ZEXT_B rsdc =
    (do
      let rsd := (creg2reg_idx rsdc)
      let v_rsd ← rX_bits rsd
      wX_bits rsd (pure_C_ZEXT_B v_rsd rsdc)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_C_ZEXT_B, pure_C_ZEXT_B, bind_assoc, pure_bind]

end Leanpath
