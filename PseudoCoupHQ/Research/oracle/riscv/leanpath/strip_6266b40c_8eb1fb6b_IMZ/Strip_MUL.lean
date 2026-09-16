import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_MUL (rs1_bits : BitVec 64) (rs2_bits : BitVec 64) (mul_op : mul_op) : BitVec 64 :=

  mult_to_bits_half (l := xlen) mul_op.signed_rs1 mul_op.signed_rs2 rs1_bits rs2_bits
      mul_op.result_part

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_MUL (rs2 : regidx) (rs1 : regidx) (rd : regidx) (mul_op : mul_op) :
    execute_MUL rs2 rs1 rd mul_op =
    (do
      let rs1_bits ← rX_bits rs1
      let rs2_bits ← rX_bits rs2
      wX_bits rd (pure_MUL rs1_bits rs2_bits mul_op)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_MUL, pure_MUL, bind_assoc, pure_bind]

end Leanpath
