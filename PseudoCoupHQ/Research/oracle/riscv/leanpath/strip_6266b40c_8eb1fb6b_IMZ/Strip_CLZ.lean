import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_CLZ (v_rs1 : BitVec 64) : BitVec 64 :=

  to_bits (l := 64) (BitVec.countLeadingZeros v_rs1)

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_CLZ (rs1 : regidx) (rd : regidx) :
    execute_CLZ rs1 rd =
    (do
      let v_rs1 ← rX_bits rs1
      wX_bits rd (pure_CLZ v_rs1)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_CLZ, pure_CLZ, bind_assoc, pure_bind]

end Leanpath
