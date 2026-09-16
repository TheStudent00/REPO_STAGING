import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_MULW (v_rs1 : BitVec 64) (v_rs2 : BitVec 64) : BitVec 64 :=
  let rs1_bits := (Sail.BitVec.extractLsb v_rs1 31 0)
  let rs2_bits := (Sail.BitVec.extractLsb v_rs2 31 0)
  let rs1_int := (BitVec.toInt rs1_bits)
  let rs2_int := (BitVec.toInt rs2_bits)
  let result32 : (BitVec 32) := (to_bits_truncate (l := 32) (rs1_int *i rs2_int))
  sign_extend (m := 64) result32

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_MULW (rs2 : regidx) (rs1 : regidx) (rd : regidx) :
    execute_MULW rs2 rs1 rd =
    (do
      let v_rs1 ← rX_bits rs1
      let v_rs2 ← rX_bits rs2
      wX_bits rd (pure_MULW v_rs1 v_rs2)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_MULW, pure_MULW, bind_assoc, pure_bind]

end Leanpath
