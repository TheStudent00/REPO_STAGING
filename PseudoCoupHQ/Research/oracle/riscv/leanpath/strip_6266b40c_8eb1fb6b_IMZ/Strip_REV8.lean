import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_REV8 (v_rs1 : BitVec 64) : BitVec 64 :=

  rev8 v_rs1

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_REV8 (rs1 : regidx) (rd : regidx) :
    execute_REV8 rs1 rd =
    (do
      let v_rs1 ← rX_bits rs1
      wX_bits rd (pure_REV8 v_rs1)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_REV8, pure_REV8, bind_assoc, pure_bind]

end Leanpath
