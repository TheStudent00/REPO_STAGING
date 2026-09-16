import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_ADDIW (v_rs1 : BitVec 64) (imm : (BitVec 12)) : BitVec 64 :=
  let result := (v_rs1 + (sign_extend (m := 64) imm))
  sign_extend (m := 64) (Sail.BitVec.extractLsb result 31 0)

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_ADDIW (imm : (BitVec 12)) (rs1 : regidx) (rd : regidx) :
    execute_ADDIW imm rs1 rd =
    (do
      let v_rs1 ← rX_bits rs1
      wX_bits rd (pure_ADDIW v_rs1 imm)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_ADDIW, pure_ADDIW, bind_assoc, pure_bind]

end Leanpath
