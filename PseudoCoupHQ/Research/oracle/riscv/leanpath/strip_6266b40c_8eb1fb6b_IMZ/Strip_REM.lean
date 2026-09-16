import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_REM (rs1_bits : BitVec 64) (rs2_bits : BitVec 64) (is_unsigned : Bool) : BitVec 64 :=
  let rs1_int := if (is_unsigned : Bool)
      then (BitVec.toNatInt rs1_bits)
      else (BitVec.toInt rs1_bits)
  let rs2_int := if (is_unsigned : Bool)
      then (BitVec.toNatInt rs2_bits)
      else (BitVec.toInt rs2_bits)
  let remainder := if ((rs2_int == 0) : Bool)
      then rs1_int
      else (Int.tmod rs1_int rs2_int)
  to_bits_truncate (l := 64) remainder

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_REM (rs2 : regidx) (rs1 : regidx) (rd : regidx) (is_unsigned : Bool) :
    execute_REM rs2 rs1 rd is_unsigned =
    (do
      let rs1_bits ← rX_bits rs1
      let rs2_bits ← rX_bits rs2
      wX_bits rd (pure_REM rs1_bits rs2_bits is_unsigned)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_REM, pure_REM, bind_assoc, pure_bind]

end Leanpath
