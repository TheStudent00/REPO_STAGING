import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_CLMULH (v_rs1 : BitVec 64) (v_rs2 : BitVec 64) : BitVec 64 :=
  let prod := (carryless_mul v_rs1 v_rs2)
  Sail.BitVec.extractLsb prod ((2 *i xlen) -i 1) xlen

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_CLMULH (rs2 : regidx) (rs1 : regidx) (rd : regidx) :
    execute_CLMULH rs2 rs1 rd =
    (do
      let v_rs1 ← rX_bits rs1
      let v_rs2 ← rX_bits rs2
      wX_bits rd (pure_CLMULH v_rs1 v_rs2)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_CLMULH, pure_CLMULH, bind_assoc, pure_bind]

end Leanpath
