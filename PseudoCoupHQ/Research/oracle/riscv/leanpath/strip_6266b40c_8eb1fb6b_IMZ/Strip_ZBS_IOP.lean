import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_ZBS_IOP (rs1_val : BitVec 64) (shamt : (BitVec 6)) (op : biop_zbs) : BitVec 64 :=
  let mask : xlenbits := (shift_bits_left (zero_extend (m := 64) 1#1) shamt)
  let result : xlenbits := match op with
      | .BCLRI => (rs1_val &&& (Complement.complement mask))
      | .BEXTI => (zero_extend (m := 64) (bool_to_bit ((rs1_val &&& mask) != (zeros (n := 64)))))
      | .BINVI => (rs1_val ^^^ mask)
      | .BSETI => (rs1_val ||| mask)
  result

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_ZBS_IOP (shamt : (BitVec 6)) (rs1 : regidx) (rd : regidx) (op : biop_zbs) :
    execute_ZBS_IOP shamt rs1 rd op =
    (do
      let rs1_val ← rX_bits rs1
      wX_bits rd (pure_ZBS_IOP rs1_val shamt op)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_ZBS_IOP, pure_ZBS_IOP, bind_assoc, pure_bind]

end Leanpath
