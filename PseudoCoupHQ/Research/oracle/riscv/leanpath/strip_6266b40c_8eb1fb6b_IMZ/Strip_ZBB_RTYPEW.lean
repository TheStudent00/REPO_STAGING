import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_ZBB_RTYPEW (v_rs1 : BitVec 64) (v_rs2 : BitVec 64) (op : bropw_zbb) : BitVec 64 :=
  let rs1_val := (Sail.BitVec.extractLsb v_rs1 31 0)
  let shamt := (Sail.BitVec.extractLsb v_rs2 4 0)
  let result : (BitVec 32) := match op with
      | .ROLW => (rotate_bits_left rs1_val shamt)
      | .RORW => (rotate_bits_right rs1_val shamt)
  sign_extend (m := 64) result

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_ZBB_RTYPEW (rs2 : regidx) (rs1 : regidx) (rd : regidx) (op : bropw_zbb) :
    execute_ZBB_RTYPEW rs2 rs1 rd op =
    (do
      let v_rs1 ← rX_bits rs1
      let v_rs2 ← rX_bits rs2
      wX_bits rd (pure_ZBB_RTYPEW v_rs1 v_rs2 op)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_ZBB_RTYPEW, pure_ZBB_RTYPEW, bind_assoc, pure_bind]

end Leanpath
