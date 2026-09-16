import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_DIV (rs1_bits : BitVec 64) (rs2_bits : BitVec 64) (is_unsigned : Bool) : BitVec 64 :=
  let rs1_int := if (is_unsigned : Bool)
      then (BitVec.toNatInt rs1_bits)
      else (BitVec.toInt rs1_bits)
  let rs2_int := if (is_unsigned : Bool)
      then (BitVec.toNatInt rs2_bits)
      else (BitVec.toInt rs2_bits)
  let quotient := if ((rs2_int == 0) : Bool)
      then (Neg.neg 1)
      else (Int.tdiv rs1_int rs2_int)
  let quotient := if (((not is_unsigned) && (quotient ≥b (2 ^i (xlen -i 1)))) : Bool)
      then (Neg.neg (2 ^i (xlen -i 1)))
      else quotient
  to_bits_truncate (l := 64) quotient

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_DIV (rs2 : regidx) (rs1 : regidx) (rd : regidx) (is_unsigned : Bool) :
    execute_DIV rs2 rs1 rd is_unsigned =
    (do
      let rs1_bits ← rX_bits rs1
      let rs2_bits ← rX_bits rs2
      wX_bits rd (pure_DIV rs1_bits rs2_bits is_unsigned)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_DIV, pure_DIV, bind_assoc, pure_bind]

end Leanpath
