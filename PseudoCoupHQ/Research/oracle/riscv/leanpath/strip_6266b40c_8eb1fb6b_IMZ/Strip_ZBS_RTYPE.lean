import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_ZBS_RTYPE (rs1_val : BitVec 64) (rs2_val : BitVec 64) (op : brop_zbs) : BitVec 64 :=
  let mask : xlenbits := (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb rs2_val 5 0))
  let result : xlenbits := match op with
      | .BCLR => (rs1_val &&& (Complement.complement mask))
      | .BEXT => (zero_extend (m := 64) (bool_to_bit ((rs1_val &&& mask) != (zeros (n := 64)))))
      | .BINV => (rs1_val ^^^ mask)
      | .BSET => (rs1_val ||| mask)
  result

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_ZBS_RTYPE (rs2 : regidx) (rs1 : regidx) (rd : regidx) (op : brop_zbs) :
    execute_ZBS_RTYPE rs2 rs1 rd op =
    (do
      let rs1_val ← rX_bits rs1
      let rs2_val ← rX_bits rs2
      wX_bits rd (pure_ZBS_RTYPE rs1_val rs2_val op)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_ZBS_RTYPE, pure_ZBS_RTYPE, bind_assoc, pure_bind]

end Leanpath
