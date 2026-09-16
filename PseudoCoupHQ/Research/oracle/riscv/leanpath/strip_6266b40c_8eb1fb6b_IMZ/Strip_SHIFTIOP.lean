import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_SHIFTIOP (v_rs1 : BitVec 64) (shamt : (BitVec 6)) (op : sop) : BitVec 64 :=
  let shamt := (Sail.BitVec.extractLsb shamt (log2_xlen -i 1) 0)
  match op with
    | .SLLI => (shift_bits_left v_rs1 shamt)
    | .SRLI => (shift_bits_right v_rs1 shamt)
    | .SRAI => (shift_bits_right_arith v_rs1 shamt)

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_SHIFTIOP (shamt : (BitVec 6)) (rs1 : regidx) (rd : regidx) (op : sop) :
    execute_SHIFTIOP shamt rs1 rd op =
    (do
      let v_rs1 ← rX_bits rs1
      wX_bits rd (pure_SHIFTIOP v_rs1 shamt op)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | (cases op <;> simp only [execute_SHIFTIOP, pure_SHIFTIOP, bind_assoc, pure_bind])
  | simp only [execute_SHIFTIOP, pure_SHIFTIOP, bind_assoc, pure_bind]

end Leanpath
