import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_CTZW (v_rs1 : BitVec 64) : BitVec 64 :=

  to_bits (l := 64) (BitVec.countTrailingZeros (Sail.BitVec.extractLsb v_rs1 31 0))

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_CTZW (rs1 : regidx) (rd : regidx) :
    execute_CTZW rs1 rd =
    (do
      let v_rs1 ← rX_bits rs1
      wX_bits rd (pure_CTZW v_rs1)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_CTZW, pure_CTZW, bind_assoc, pure_bind]

end Leanpath
