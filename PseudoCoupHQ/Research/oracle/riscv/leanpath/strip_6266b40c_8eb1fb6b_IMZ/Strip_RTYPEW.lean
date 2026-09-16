import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_RTYPEW (v_rs1 : BitVec 64) (v_rs2 : BitVec 64) (op : ropw) : BitVec 64 :=
  let rs1_val := (Sail.BitVec.extractLsb v_rs1 31 0)
  let rs2_val := (Sail.BitVec.extractLsb v_rs2 31 0)
  let result : (BitVec 32) := match op with
      | .ADDW => (rs1_val + rs2_val)
      | .SUBW => (rs1_val - rs2_val)
      | .SLLW => (shift_bits_left rs1_val (Sail.BitVec.extractLsb rs2_val 4 0))
      | .SRLW => (shift_bits_right rs1_val (Sail.BitVec.extractLsb rs2_val 4 0))
      | .SRAW => (shift_bits_right_arith rs1_val (Sail.BitVec.extractLsb rs2_val 4 0))
  sign_extend (m := 64) result

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_RTYPEW (rs2 : regidx) (rs1 : regidx) (rd : regidx) (op : ropw) :
    execute_RTYPEW rs2 rs1 rd op =
    (do
      let v_rs1 ← rX_bits rs1
      let v_rs2 ← rX_bits rs2
      wX_bits rd (pure_RTYPEW v_rs1 v_rs2 op)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_RTYPEW, pure_RTYPEW, bind_assoc, pure_bind]

end Leanpath
