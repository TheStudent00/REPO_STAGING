import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_SHIFTIWOP (v_rs1 : BitVec 64) (shamt : (BitVec 5)) (op : sopw) : BitVec 64 :=
  let rs1_val := (Sail.BitVec.extractLsb v_rs1 31 0)
  let result : (BitVec 32) := match op with
      | .SLLIW => (shift_bits_left rs1_val shamt)
      | .SRLIW => (shift_bits_right rs1_val shamt)
      | .SRAIW => (shift_bits_right_arith rs1_val shamt)
  sign_extend (m := 64) result

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_SHIFTIWOP (shamt : (BitVec 5)) (rs1 : regidx) (rd : regidx) (op : sopw) :
    execute_SHIFTIWOP shamt rs1 rd op =
    (do
      let v_rs1 ← rX_bits rs1
      wX_bits rd (pure_SHIFTIWOP v_rs1 shamt op)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_SHIFTIWOP, pure_SHIFTIWOP, bind_assoc, pure_bind]

end Leanpath
