import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_CLMUL (v_rs1 : BitVec 64) (v_rs2 : BitVec 64) : BitVec 64 :=
  let prod := (carryless_mul v_rs1 v_rs2)
  Sail.BitVec.extractLsb prod (xlen -i 1) 0

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_CLMUL (rs2 : regidx) (rs1 : regidx) (rd : regidx) :
    execute_CLMUL rs2 rs1 rd =
    (do
      let v_rs1 ← rX_bits rs1
      let v_rs2 ← rX_bits rs2
      wX_bits rd (pure_CLMUL v_rs1 v_rs2)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_CLMUL, pure_CLMUL, bind_assoc, pure_bind]

end Leanpath
