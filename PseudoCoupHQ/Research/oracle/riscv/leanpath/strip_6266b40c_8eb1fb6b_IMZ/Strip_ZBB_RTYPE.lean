import LeanIMZ
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMZ LeanIMZ.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option linter.unusedVariables false
noncomputable section
namespace Leanpath

/-- the proposal: the clause's pure form, by the one rule -/
def pure_ZBB_RTYPE (rs1_val : BitVec 64) (rs2_val : BitVec 64) (op : brop_zbb) : BitVec 64 :=
  let result : xlenbits := match op with
      | .ANDN => (rs1_val &&& (Complement.complement rs2_val))
      | .ORN => (rs1_val ||| (Complement.complement rs2_val))
      | .XNOR => (Complement.complement (rs1_val ^^^ rs2_val))
      | .MAX =>
        (if ((zopz0zK_s rs1_val rs2_val) : Bool)
        then rs1_val
        else rs2_val)
      | .MAXU =>
        (if ((zopz0zK_u rs1_val rs2_val) : Bool)
        then rs1_val
        else rs2_val)
      | .MIN =>
        (if ((zopz0zI_s rs1_val rs2_val) : Bool)
        then rs1_val
        else rs2_val)
      | .MINU =>
        (if ((zopz0zI_u rs1_val rs2_val) : Bool)
        then rs1_val
        else rs2_val)
      | .ROL => (rotate_bits_left rs1_val (Sail.BitVec.extractLsb rs2_val (log2_xlen -i 1) 0))
      | .ROR => (rotate_bits_right rs1_val (Sail.BitVec.extractLsb rs2_val (log2_xlen -i 1) 0))
  result

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_ZBB_RTYPE (rs2 : regidx) (rs1 : regidx) (rd : regidx) (op : brop_zbb) :
    execute_ZBB_RTYPE rs2 rs1 rd op =
    (do
      let rs1_val ← rX_bits rs1
      let rs2_val ← rX_bits rs2
      wX_bits rd (pure_ZBB_RTYPE rs1_val rs2_val op)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_ZBB_RTYPE, pure_ZBB_RTYPE, bind_assoc, pure_bind]

end Leanpath
