import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_SLLIUW (v_rs1 : BitVec 64) (shamt : (BitVec 6)) : BitVec 64 :=

  shift_bits_left (zero_extend (m := 64) (Sail.BitVec.extractLsb v_rs1 31 0)) shamt

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_SLLIUW (shamt : (BitVec 6)) (rs1 : regidx) (rd : regidx) :
    execute_SLLIUW shamt rs1 rd =
    (do
      let v_rs1 ← rX_bits rs1
      wX_bits rd (pure_SLLIUW v_rs1 shamt)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_SLLIUW, pure_SLLIUW, bind_assoc, pure_bind]

end Leanpath
