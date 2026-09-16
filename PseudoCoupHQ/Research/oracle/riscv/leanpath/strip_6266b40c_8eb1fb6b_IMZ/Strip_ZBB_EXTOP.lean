import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_ZBB_EXTOP (rs1_val : BitVec 64) (op : extop_zbb) : BitVec 64 :=
  let result : xlenbits := match op with
      | .SEXTB => (sign_extend (m := 64) (Sail.BitVec.extractLsb rs1_val 7 0))
      | .SEXTH => (sign_extend (m := 64) (Sail.BitVec.extractLsb rs1_val 15 0))
      | .ZEXTH => (zero_extend (m := 64) (Sail.BitVec.extractLsb rs1_val 15 0))
  result

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_ZBB_EXTOP (rs1 : regidx) (rd : regidx) (op : extop_zbb) :
    execute_ZBB_EXTOP rs1 rd op =
    (do
      let rs1_val ← rX_bits rs1
      wX_bits rd (pure_ZBB_EXTOP rs1_val op)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_ZBB_EXTOP, pure_ZBB_EXTOP, bind_assoc, pure_bind]

end Leanpath
