import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_RORI (v_rs1 : BitVec 64) (shamt : (BitVec 6)) : BitVec 64 :=
  let shamt := (Sail.BitVec.extractLsb shamt (log2_xlen -i 1) 0)
  rotate_bits_right v_rs1 shamt

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_RORI (shamt : (BitVec 6)) (rs1 : regidx) (rd : regidx) :
    execute_RORI shamt rs1 rd =
    (do
      let v_rs1 ← rX_bits rs1
      wX_bits rd (pure_RORI v_rs1 shamt)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_RORI, pure_RORI, bind_assoc, pure_bind]

end Leanpath
