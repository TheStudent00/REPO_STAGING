import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_ITYPE (v_rs1 : BitVec 64) (imm : (BitVec 12)) (op : iop) : BitVec 64 :=
  let immext : xlenbits := (sign_extend (m := 64) imm)
  match op with
    | .ADDI => (v_rs1 + immext)
    | .SLTI => (zero_extend (m := 64) (bool_to_bit (zopz0zI_s v_rs1 immext)))
    | .SLTIU => (zero_extend (m := 64) (bool_to_bit (zopz0zI_u v_rs1 immext)))
    | .ANDI => (v_rs1 &&& immext)
    | .ORI => (v_rs1 ||| immext)
    | .XORI => (v_rs1 ^^^ immext)

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_ITYPE (imm : (BitVec 12)) (rs1 : regidx) (rd : regidx) (op : iop) :
    execute_ITYPE imm rs1 rd op =
    (do
      let v_rs1 ← rX_bits rs1
      wX_bits rd (pure_ITYPE v_rs1 imm op)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | (cases op <;> simp only [execute_ITYPE, pure_ITYPE, bind_assoc, pure_bind])
  | simp only [execute_ITYPE, pure_ITYPE, bind_assoc, pure_bind]

end Leanpath
