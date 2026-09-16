import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_ZBA_RTYPE (v_rs1 : BitVec 64) (v_rs2 : BitVec 64) (shamt : (BitVec 2)) : BitVec 64 :=

  (shift_bits_left v_rs1 shamt) + v_rs2

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_ZBA_RTYPE (rs2 : regidx) (rs1 : regidx) (rd : regidx) (shamt : (BitVec 2)) :
    execute_ZBA_RTYPE rs2 rs1 rd shamt =
    (do
      let v_rs1 ← rX_bits rs1
      let v_rs2 ← rX_bits rs2
      wX_bits rd (pure_ZBA_RTYPE v_rs1 v_rs2 shamt)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_ZBA_RTYPE, pure_ZBA_RTYPE, bind_assoc, pure_bind]

end Leanpath
