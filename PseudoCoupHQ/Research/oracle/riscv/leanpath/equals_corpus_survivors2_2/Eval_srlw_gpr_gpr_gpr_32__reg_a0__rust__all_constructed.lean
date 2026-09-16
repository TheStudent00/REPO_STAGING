import LeanIM
set_option maxHeartbeats 1_000_000_000
set_option maxRecDepth 1_000_000
set_option linter.unusedVariables false
set_option match.ignoreUnusedAlts true
open Sail
open Sail.ConcurrencyInterfaceV1
noncomputable section
namespace LeanIM
open ConcurrencyInterfaceV1
namespace Functions
open zvk_vsm4r_funct6
open zvk_vsha2_funct6
open zvk_vaesem_funct6
open zvk_vaesef_funct6
open zvk_vaesdm_funct6
open zvk_vaesdf_funct6
open zvabd_vwabda_func6
open zvabd_vabd_func6
open zicondop
open xRET_type
open wxfunct6
open wvxfunct6
open wvvfunct6
open wvfunct6
open wrsop
open write_kind
open wmvxfunct6
open wmvvfunct6
open vxsgfunct6
open vxmsfunct6
open vxmfunct6
open vxmcfunct6
open vxfunct6
open vxcmpfunct6
open vvmsfunct6
open vvmfunct6
open vvmcfunct6
open vvfunct6
open vvcmpfunct6
open vstart_class
open vregno
open vregidx
open vmlsop
open vlewidth
open visgfunct6
open virtaddr
open vimsfunct6
open vimfunct6
open vimcfunct6
open vifunct6
open vicmpfunct6
open vfwunary0
open vfunary1
open vfunary0
open vfnunary0
open vextfunct6
open vector_support
open uop
open stateen_bit
open sopw
open sop
open seed_opst
open rounding_mode
open ropw
open rop
open rmvvfunct6
open rivvfunct6
open rfwvvfunct6
open rfvvfunct6
open regno
open regidx
open read_kind
open pte_check_failure
open pmpAddrMatch
open physaddr
open page_based_mem_type
open option
open nxsfunct6
open nxfunct6
open nvsfunct6
open nvfunct6
open ntl_type
open nisfunct6
open nifunct6
open mvxmafunct6
open mvxfunct6
open mvvmafunct6
open mvvfunct6
open mmfunct6
open misaligned_exception
open mem_payload
open maskfunct3
open landing_pad_expectation
open iop
open instruction
open indexed_mop
open fwvvmafunct6
open fwvvfunct6
open fwvfunct6
open fwvfmafunct6
open fwvffunct6
open fwffunct6
open fvvmfunct6
open fvvmafunct6
open fvvfunct6
open fvfmfunct6
open fvfmafunct6
open fvffunct6
open fregno
open fregidx
open float_class
open f_un_x_op_H
open f_un_x_op_D
open f_un_rm_xf_op_S
open f_un_rm_xf_op_H
open f_un_rm_xf_op_D
open f_un_rm_fx_op_S
open f_un_rm_fx_op_H
open f_un_rm_fx_op_D
open f_un_rm_ff_op_S
open f_un_rm_ff_op_H
open f_un_rm_ff_op_D
open f_un_op_x_S
open f_un_op_f_S
open f_un_f_op_H
open f_un_f_op_D
open f_madd_op_S
open f_madd_op_H
open f_madd_op_D
open f_bin_x_op_H
open f_bin_x_op_D
open f_bin_rm_op_S
open f_bin_rm_op_H
open f_bin_rm_op_D
open f_bin_op_x_S
open f_bin_op_f_S
open f_bin_f_op_H
open f_bin_f_op_D
open extop_zbb
open extension
open exception
open csrop
open cregidx
open checked_cbop
open cfregidx
open cbop_zicbop
open cbop_zicbom
open cbie
open cacheop
open bropw_zbb
open brop_zbs
open brop_zbkb
open brop_zbb
open breakpoint_cause
open bop
open biop_zbs
open biop
open barrier_kind
open amoop
open agtype
open XtvecModeReservedBehavior
open XipReadType
open XenvcfgCbieReservedBehavior
open WaitReason
open VectorHalf
open TrapVectorMode
open TrapCause
open Step
open Splittability
open Software_Check_Code
open Signedness
open SWCheckCodes
open SATPMode
open Reservability
open Register
open RV32ZdinxOddRegisterReservedBehavior
open Privileged_ISA_Version
open Privilege
open PointerMaskingMode
open PmpWriteOnlyReservedBehavior
open PmpAddrMatchType
open PTW_Error
open PTE_Check
open PM_Ext
open OOBVstartReservedBehavior
open MemoryRegionType
open MemoryAccessType
open InterruptType
open IllegalVtypeReservedBehavior
open ISA_Format
open HartState
open FflagsDirtyPolicy
open FetchResult
open FetchBytes_Result
open FeatureEnabledResult
open FcsrRmReservedBehavior
open Ext_DataAddr_Check
open ExtStatus
open ExtContextPolicy
open ExecutionResult
open ExceptionType
open CSRCheckResult
open CSRAccessType
open AtomicSupport
open Architecture
open AmocasOddRegisterReservedBehavior

/-- the proposal: the clause's pure form, by the one rule -/
def pure_SHIFTIWOP (v_rs1 : BitVec 64) (shamt : (BitVec 5)) (op : sopw) : BitVec 64 :=
  let rs1_val := (Sail.BitVec.extractLsb v_rs1 31 0)
  let result : (BitVec 32) := match op with
      | .SLLIW => (shift_bits_left rs1_val shamt)
      | .SRLIW => (shift_bits_right rs1_val shamt)
      | .SRAIW => (shift_bits_right_arith rs1_val shamt)
  sign_extend (m := 64) result

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_SHIFTIWOP (shamt : (BitVec 5)) (rs1 : regidx) (rd : regidx) (op : sopw) :
    execute_SHIFTIWOP shamt rs1 rd op =
    (do
      let v_rs1 ← rX_bits rs1
      wX_bits rd (pure_SHIFTIWOP v_rs1 shamt op)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_SHIFTIWOP, pure_SHIFTIWOP, bind_assoc, pure_bind]

/-- the proposal: the clause's pure form, by the one rule -/
def pure_SHIFTIOP (v_rs1 : BitVec 64) (shamt : (BitVec 6)) (op : sop) : BitVec 64 :=
  let shamt := (Sail.BitVec.extractLsb shamt (log2_xlen -i 1) 0)
  match op with
    | .SLLI => (shift_bits_left v_rs1 shamt)
    | .SRLI => (shift_bits_right v_rs1 shamt)
    | .SRAI => (shift_bits_right_arith v_rs1 shamt)

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_SHIFTIOP (shamt : (BitVec 6)) (rs1 : regidx) (rd : regidx) (op : sop) :
    execute_SHIFTIOP shamt rs1 rd op =
    (do
      let v_rs1 ← rX_bits rs1
      wX_bits rd (pure_SHIFTIOP v_rs1 shamt op)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | (cases op <;> simp only [execute_SHIFTIOP, pure_SHIFTIOP, bind_assoc, pure_bind])
  | simp only [execute_SHIFTIOP, pure_SHIFTIOP, bind_assoc, pure_bind]

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

/-- the proposal: the clause's pure form, by the one rule -/
def pure_RTYPEW (v_rs1 : BitVec 64) (v_rs2 : BitVec 64) (op : ropw) : BitVec 64 :=
  let rs1_val := (Sail.BitVec.extractLsb v_rs1 31 0)
  let rs2_val := (Sail.BitVec.extractLsb v_rs2 31 0)
  let result : (BitVec 32) := match op with
      | .ADDW => (rs1_val + rs2_val)
      | .SUBW => (rs1_val - rs2_val)
      | .SLLW => (shift_bits_left rs1_val (Sail.BitVec.extractLsb rs2_val 4 0))
      | .SRLW => (shift_bits_right rs1_val (Sail.BitVec.extractLsb rs2_val 4 0))
      | .SRAW => (shift_bits_right_arith rs1_val (Sail.BitVec.extractLsb rs2_val 4 0))
  sign_extend (m := 64) result

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_RTYPEW (rs2 : regidx) (rs1 : regidx) (rd : regidx) (op : ropw) :
    execute_RTYPEW rs2 rs1 rd op =
    (do
      let v_rs1 ← rX_bits rs1
      let v_rs2 ← rX_bits rs2
      wX_bits rd (pure_RTYPEW v_rs1 v_rs2 op)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_RTYPEW, pure_RTYPEW, bind_assoc, pure_bind]

/-- the proposal: the clause's pure form, by the one rule -/
def pure_RTYPE (v_rs1 : BitVec 64) (v_rs2 : BitVec 64) (op : rop) : BitVec 64 :=

  match op with
    | .ADD => (v_rs1 + v_rs2)
    | .SLT => (zero_extend (m := 64)
            (bool_to_bit (zopz0zI_s v_rs1 v_rs2)))
    | .SLTU => (zero_extend (m := 64)
            (bool_to_bit (zopz0zI_u v_rs1 v_rs2)))
    | .AND => (v_rs1 &&& v_rs2)
    | .OR => (v_rs1 ||| v_rs2)
    | .XOR => (v_rs1 ^^^ v_rs2)
    | .SLL => (shift_bits_left v_rs1
            (Sail.BitVec.extractLsb v_rs2 (log2_xlen -i 1) 0))
    | .SRL => (shift_bits_right v_rs1
            (Sail.BitVec.extractLsb v_rs2 (log2_xlen -i 1) 0))
    | .SUB => (v_rs1 - v_rs2)
    | .SRA => (shift_bits_right_arith v_rs1
            (Sail.BitVec.extractLsb v_rs2 (log2_xlen -i 1) 0))

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_RTYPE (rs2 : regidx) (rs1 : regidx) (rd : regidx) (op : rop) :
    execute_RTYPE rs2 rs1 rd op =
    (do
      let v_rs1 ← rX_bits rs1
      let v_rs2 ← rX_bits rs2
      wX_bits rd (pure_RTYPE v_rs1 v_rs2 op)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | (cases op <;> simp only [execute_RTYPE, pure_RTYPE, bind_assoc, pure_bind])
  | simp only [execute_RTYPE, pure_RTYPE, bind_assoc, pure_bind]

/-- the proposal: the clause's pure form, by the one rule -/
def pure_CLMUL (v_rs1 : BitVec 64) (v_rs2 : BitVec 64) : BitVec 64 :=
  let prod := (carryless_mul v_rs1 v_rs2)
  Sail.BitVec.extractLsb prod (xlen -i 1) 0

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_CLMUL (rs2 : regidx) (rs1 : regidx) (rd : regidx) :
    execute_CLMUL rs2 rs1 rd =
    (do
      let v_rs1 ← rX_bits rs1
      let v_rs2 ← rX_bits rs2
      wX_bits rd (pure_CLMUL v_rs1 v_rs2)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_CLMUL, pure_CLMUL, bind_assoc, pure_bind]

/-- the proposal: the clause's pure form, by the one rule -/
def pure_CLMULH (v_rs1 : BitVec 64) (v_rs2 : BitVec 64) : BitVec 64 :=
  let prod := (carryless_mul v_rs1 v_rs2)
  Sail.BitVec.extractLsb prod ((2 *i xlen) -i 1) xlen

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_CLMULH (rs2 : regidx) (rs1 : regidx) (rd : regidx) :
    execute_CLMULH rs2 rs1 rd =
    (do
      let v_rs1 ← rX_bits rs1
      let v_rs2 ← rX_bits rs2
      wX_bits rd (pure_CLMULH v_rs1 v_rs2)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_CLMULH, pure_CLMULH, bind_assoc, pure_bind]

/-- the proposal: the clause's pure form, by the one rule -/
def pure_CLMULR (v_rs1 : BitVec 64) (v_rs2 : BitVec 64) : BitVec 64 :=

  carryless_mulr v_rs1 v_rs2

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_CLMULR (rs2 : regidx) (rs1 : regidx) (rd : regidx) :
    execute_CLMULR rs2 rs1 rd =
    (do
      let v_rs1 ← rX_bits rs1
      let v_rs2 ← rX_bits rs2
      wX_bits rd (pure_CLMULR v_rs1 v_rs2)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_CLMULR, pure_CLMULR, bind_assoc, pure_bind]

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

/-- the proposal: the clause's pure form, by the one rule -/
def pure_DIVW (v_rs1 : BitVec 64) (v_rs2 : BitVec 64) (is_unsigned : Bool) : BitVec 64 :=
  let rs1_bits := (Sail.BitVec.extractLsb v_rs1 31 0)
  let rs2_bits := (Sail.BitVec.extractLsb v_rs2 31 0)
  let rs1_int := if (is_unsigned : Bool)
      then (BitVec.toNatInt rs1_bits)
      else (BitVec.toInt rs1_bits)
  let rs2_int := if (is_unsigned : Bool)
      then (BitVec.toNatInt rs2_bits)
      else (BitVec.toInt rs2_bits)
  let quotient := if ((rs2_int == 0) : Bool)
      then (Neg.neg 1)
      else (Int.tdiv rs1_int rs2_int)
  let quotient := if (((not is_unsigned) && (quotient ≥b (2 ^i 31))) : Bool)
      then (Neg.neg (2 ^i 31))
      else quotient
  sign_extend (m := 64) (to_bits_truncate (l := 32) quotient)

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_DIVW (rs2 : regidx) (rs1 : regidx) (rd : regidx) (is_unsigned : Bool) :
    execute_DIVW rs2 rs1 rd is_unsigned =
    (do
      let v_rs1 ← rX_bits rs1
      let v_rs2 ← rX_bits rs2
      wX_bits rd (pure_DIVW v_rs1 v_rs2 is_unsigned)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_DIVW, pure_DIVW, bind_assoc, pure_bind]

/-- the proposal: the clause's pure form, by the one rule -/
def pure_MUL (rs1_bits : BitVec 64) (rs2_bits : BitVec 64) (mul_op : mul_op) : BitVec 64 :=

  mult_to_bits_half (l := xlen) mul_op.signed_rs1 mul_op.signed_rs2 rs1_bits rs2_bits
      mul_op.result_part

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_MUL (rs2 : regidx) (rs1 : regidx) (rd : regidx) (mul_op : mul_op) :
    execute_MUL rs2 rs1 rd mul_op =
    (do
      let rs1_bits ← rX_bits rs1
      let rs2_bits ← rX_bits rs2
      wX_bits rd (pure_MUL rs1_bits rs2_bits mul_op)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_MUL, pure_MUL, bind_assoc, pure_bind]

/-- the proposal: the clause's pure form, by the one rule -/
def pure_MULW (v_rs1 : BitVec 64) (v_rs2 : BitVec 64) : BitVec 64 :=
  let rs1_bits := (Sail.BitVec.extractLsb v_rs1 31 0)
  let rs2_bits := (Sail.BitVec.extractLsb v_rs2 31 0)
  let rs1_int := (BitVec.toInt rs1_bits)
  let rs2_int := (BitVec.toInt rs2_bits)
  let result32 : (BitVec 32) := (to_bits_truncate (l := 32) (rs1_int *i rs2_int))
  sign_extend (m := 64) result32

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_MULW (rs2 : regidx) (rs1 : regidx) (rd : regidx) :
    execute_MULW rs2 rs1 rd =
    (do
      let v_rs1 ← rX_bits rs1
      let v_rs2 ← rX_bits rs2
      wX_bits rd (pure_MULW v_rs1 v_rs2)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_MULW, pure_MULW, bind_assoc, pure_bind]

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

/-- the proposal: the clause's pure form, by the one rule -/
def pure_REMW (v_rs1 : BitVec 64) (v_rs2 : BitVec 64) (is_unsigned : Bool) : BitVec 64 :=
  let rs1_bits := (Sail.BitVec.extractLsb v_rs1 31 0)
  let rs2_bits := (Sail.BitVec.extractLsb v_rs2 31 0)
  let rs1_int := if (is_unsigned : Bool)
      then (BitVec.toNatInt rs1_bits)
      else (BitVec.toInt rs1_bits)
  let rs2_int := if (is_unsigned : Bool)
      then (BitVec.toNatInt rs2_bits)
      else (BitVec.toInt rs2_bits)
  let remainder := if ((rs2_int == 0) : Bool)
      then rs1_int
      else (Int.tmod rs1_int rs2_int)
  sign_extend (m := 64) (to_bits_truncate (l := 32) remainder)

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_REMW (rs2 : regidx) (rs1 : regidx) (rd : regidx) (is_unsigned : Bool) :
    execute_REMW rs2 rs1 rd is_unsigned =
    (do
      let v_rs1 ← rX_bits rs1
      let v_rs2 ← rX_bits rs2
      wX_bits rd (pure_REMW v_rs1 v_rs2 is_unsigned)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_REMW, pure_REMW, bind_assoc, pure_bind]

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

/-- the proposal: the clause's pure form, by the one rule -/
def pure_ZBB_RTYPEW (v_rs1 : BitVec 64) (v_rs2 : BitVec 64) (op : bropw_zbb) : BitVec 64 :=
  let rs1_val := (Sail.BitVec.extractLsb v_rs1 31 0)
  let shamt := (Sail.BitVec.extractLsb v_rs2 4 0)
  let result : (BitVec 32) := match op with
      | .ROLW => (rotate_bits_left rs1_val shamt)
      | .RORW => (rotate_bits_right rs1_val shamt)
  sign_extend (m := 64) result

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_ZBB_RTYPEW (rs2 : regidx) (rs1 : regidx) (rd : regidx) (op : bropw_zbb) :
    execute_ZBB_RTYPEW rs2 rs1 rd op =
    (do
      let v_rs1 ← rX_bits rs1
      let v_rs2 ← rX_bits rs2
      wX_bits rd (pure_ZBB_RTYPEW v_rs1 v_rs2 op)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_ZBB_RTYPEW, pure_ZBB_RTYPEW, bind_assoc, pure_bind]

/-- the proposal: the clause's pure form, by the one rule -/
def pure_ZBKB_RTYPE (rs1_val : BitVec 64) (rs2_val : BitVec 64) (op : brop_zbkb) : BitVec 64 :=
  let result : xlenbits := match op with
      | .PACK =>
        ((Sail.BitVec.extractLsb rs2_val ((xlen_bytes *i 4) -i 1) 0) +++ (Sail.BitVec.extractLsb
            rs1_val ((xlen_bytes *i 4) -i 1) 0))
      | .PACKH =>
        (zero_extend (m := 64)
          ((Sail.BitVec.extractLsb rs2_val 7 0) +++ (Sail.BitVec.extractLsb rs1_val 7 0)))
  result

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_ZBKB_RTYPE (rs2 : regidx) (rs1 : regidx) (rd : regidx) (op : brop_zbkb) :
    execute_ZBKB_RTYPE rs2 rs1 rd op =
    (do
      let rs1_val ← rX_bits rs1
      let rs2_val ← rX_bits rs2
      wX_bits rd (pure_ZBKB_RTYPE rs1_val rs2_val op)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_ZBKB_RTYPE, pure_ZBKB_RTYPE, bind_assoc, pure_bind]

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


#eval IO.println s!"E {0} [{String.intercalate ", " (([(fun (a : BitVec 64) (b : BitVec 64) => ((pure_RTYPE ((pure_RTYPE ((pure_SHIFTIOP ((pure_SHIFTIOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) ((0x20#6)) (SLLI))) ((0x20#6)) (SRLI))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x20#6) (LeanIM.sop.SLLI))) (OR))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_ITYPE ((pure_SHIFTIOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#6) (LeanIM.sop.SRLI))) ((sign_extend (m := 12) (0x06#6))) (ANDI))) ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) (OR))) ((0x21#6)) (SLLI))) (OR)))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.ADD))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SUB))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SLL))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SLT))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SLTU))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.XOR))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SRL))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SRA))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.OR))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.AND))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.ADDW))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.SUBW))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.SLLW))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.SRLW))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.SRAW))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_CLMUL (a) (b) )) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_CLMULH (a) (b) )) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_CLMULR (a) (b) )) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_DIV (a) (b) (false))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_DIV (a) (b) (true))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_DIVW (a) (b) (false))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_DIVW (a) (b) (true))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.High, signed_rs1 := Signedness.Signed, signed_rs2 := Signedness.Signed }))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.High, signed_rs1 := Signedness.Signed, signed_rs2 := Signedness.Unsigned }))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.High, signed_rs1 := Signedness.Unsigned, signed_rs2 := Signedness.Signed }))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.High, signed_rs1 := Signedness.Unsigned, signed_rs2 := Signedness.Unsigned }))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.Low, signed_rs1 := Signedness.Signed, signed_rs2 := Signedness.Signed }))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.Low, signed_rs1 := Signedness.Signed, signed_rs2 := Signedness.Unsigned }))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.Low, signed_rs1 := Signedness.Unsigned, signed_rs2 := Signedness.Signed }))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.Low, signed_rs1 := Signedness.Unsigned, signed_rs2 := Signedness.Unsigned }))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MULW (a) (b) )) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_REM (a) (b) (false))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_REM (a) (b) (true))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_REMW (a) (b) (false))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_REMW (a) (b) (true))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.ANDN))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.ORN))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.XNOR))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.MAX))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.MAXU))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.MIN))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.MINU))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.ROL))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.ROR))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPEW (a) (b) (bropw_zbb.ROLW))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPEW (a) (b) (bropw_zbb.RORW))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBKB_RTYPE (a) (b) (brop_zbkb.PACK))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBKB_RTYPE (a) (b) (brop_zbkb.PACKH))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBS_RTYPE (a) (b) (brop_zbs.BCLR))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBS_RTYPE (a) (b) (brop_zbs.BEXT))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBS_RTYPE (a) (b) (brop_zbs.BINV))) (0x0123456789abcdef#64) (0xfedcba9876543210#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBS_RTYPE (a) (b) (brop_zbs.BSET))) (0x0123456789abcdef#64) (0xfedcba9876543210#64)] : List (BitVec 64)).map (fun x => toString x.toNat))}]"
#eval IO.println s!"E {1} [{String.intercalate ", " (([(fun (a : BitVec 64) (b : BitVec 64) => ((pure_RTYPE ((pure_RTYPE ((pure_SHIFTIOP ((pure_SHIFTIOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) ((0x20#6)) (SLLI))) ((0x20#6)) (SRLI))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x20#6) (LeanIM.sop.SLLI))) (OR))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_ITYPE ((pure_SHIFTIOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#6) (LeanIM.sop.SRLI))) ((sign_extend (m := 12) (0x06#6))) (ANDI))) ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) (OR))) ((0x21#6)) (SLLI))) (OR)))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.ADD))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SUB))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SLL))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SLT))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SLTU))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.XOR))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SRL))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SRA))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.OR))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.AND))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.ADDW))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.SUBW))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.SLLW))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.SRLW))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.SRAW))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_CLMUL (a) (b) )) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_CLMULH (a) (b) )) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_CLMULR (a) (b) )) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_DIV (a) (b) (false))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_DIV (a) (b) (true))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_DIVW (a) (b) (false))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_DIVW (a) (b) (true))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.High, signed_rs1 := Signedness.Signed, signed_rs2 := Signedness.Signed }))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.High, signed_rs1 := Signedness.Signed, signed_rs2 := Signedness.Unsigned }))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.High, signed_rs1 := Signedness.Unsigned, signed_rs2 := Signedness.Signed }))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.High, signed_rs1 := Signedness.Unsigned, signed_rs2 := Signedness.Unsigned }))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.Low, signed_rs1 := Signedness.Signed, signed_rs2 := Signedness.Signed }))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.Low, signed_rs1 := Signedness.Signed, signed_rs2 := Signedness.Unsigned }))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.Low, signed_rs1 := Signedness.Unsigned, signed_rs2 := Signedness.Signed }))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.Low, signed_rs1 := Signedness.Unsigned, signed_rs2 := Signedness.Unsigned }))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MULW (a) (b) )) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_REM (a) (b) (false))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_REM (a) (b) (true))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_REMW (a) (b) (false))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_REMW (a) (b) (true))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.ANDN))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.ORN))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.XNOR))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.MAX))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.MAXU))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.MIN))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.MINU))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.ROL))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.ROR))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPEW (a) (b) (bropw_zbb.ROLW))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPEW (a) (b) (bropw_zbb.RORW))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBKB_RTYPE (a) (b) (brop_zbkb.PACK))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBKB_RTYPE (a) (b) (brop_zbkb.PACKH))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBS_RTYPE (a) (b) (brop_zbs.BCLR))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBS_RTYPE (a) (b) (brop_zbs.BEXT))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBS_RTYPE (a) (b) (brop_zbs.BINV))) (0xffffffffffffffff#64) (0x1#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBS_RTYPE (a) (b) (brop_zbs.BSET))) (0xffffffffffffffff#64) (0x1#64)] : List (BitVec 64)).map (fun x => toString x.toNat))}]"
#eval IO.println s!"E {2} [{String.intercalate ", " (([(fun (a : BitVec 64) (b : BitVec 64) => ((pure_RTYPE ((pure_RTYPE ((pure_SHIFTIOP ((pure_SHIFTIOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) ((0x20#6)) (SLLI))) ((0x20#6)) (SRLI))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x20#6) (LeanIM.sop.SLLI))) (OR))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_ITYPE ((pure_SHIFTIOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#6) (LeanIM.sop.SRLI))) ((sign_extend (m := 12) (0x06#6))) (ANDI))) ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) (OR))) ((0x21#6)) (SLLI))) (OR)))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.ADD))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SUB))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SLL))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SLT))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SLTU))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.XOR))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SRL))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SRA))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.OR))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.AND))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.ADDW))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.SUBW))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.SLLW))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.SRLW))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.SRAW))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_CLMUL (a) (b) )) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_CLMULH (a) (b) )) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_CLMULR (a) (b) )) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_DIV (a) (b) (false))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_DIV (a) (b) (true))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_DIVW (a) (b) (false))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_DIVW (a) (b) (true))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.High, signed_rs1 := Signedness.Signed, signed_rs2 := Signedness.Signed }))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.High, signed_rs1 := Signedness.Signed, signed_rs2 := Signedness.Unsigned }))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.High, signed_rs1 := Signedness.Unsigned, signed_rs2 := Signedness.Signed }))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.High, signed_rs1 := Signedness.Unsigned, signed_rs2 := Signedness.Unsigned }))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.Low, signed_rs1 := Signedness.Signed, signed_rs2 := Signedness.Signed }))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.Low, signed_rs1 := Signedness.Signed, signed_rs2 := Signedness.Unsigned }))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.Low, signed_rs1 := Signedness.Unsigned, signed_rs2 := Signedness.Signed }))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.Low, signed_rs1 := Signedness.Unsigned, signed_rs2 := Signedness.Unsigned }))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MULW (a) (b) )) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_REM (a) (b) (false))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_REM (a) (b) (true))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_REMW (a) (b) (false))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_REMW (a) (b) (true))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.ANDN))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.ORN))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.XNOR))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.MAX))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.MAXU))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.MIN))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.MINU))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.ROL))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.ROR))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPEW (a) (b) (bropw_zbb.ROLW))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPEW (a) (b) (bropw_zbb.RORW))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBKB_RTYPE (a) (b) (brop_zbkb.PACK))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBKB_RTYPE (a) (b) (brop_zbkb.PACKH))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBS_RTYPE (a) (b) (brop_zbs.BCLR))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBS_RTYPE (a) (b) (brop_zbs.BEXT))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBS_RTYPE (a) (b) (brop_zbs.BINV))) (0x8000000000000000#64) (0x7fffffffffffffff#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBS_RTYPE (a) (b) (brop_zbs.BSET))) (0x8000000000000000#64) (0x7fffffffffffffff#64)] : List (BitVec 64)).map (fun x => toString x.toNat))}]"
#eval IO.println s!"E {3} [{String.intercalate ", " (([(fun (a : BitVec 64) (b : BitVec 64) => ((pure_RTYPE ((pure_RTYPE ((pure_SHIFTIOP ((pure_SHIFTIOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) ((0x20#6)) (SLLI))) ((0x20#6)) (SRLI))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x20#6) (LeanIM.sop.SLLI))) (OR))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_SHIFTIOP ((pure_RTYPE ((pure_ITYPE ((pure_SHIFTIOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#6) (LeanIM.sop.SRLI))) ((sign_extend (m := 12) (0x06#6))) (ANDI))) ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW ((pure_RTYPEW (a) ((pure_ITYPE (b) (0x001#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x002#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x004#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) (0x008#12) (LeanIM.iop.ANDI))) (LeanIM.ropw.SRLW))) ((pure_ITYPE (b) ((sign_extend (m := 12) (0x10#6))) (ANDI))) (LeanIM.ropw.SRLW))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (OR))) (OR))) ((0x02#6)) (SLLI))) (OR))) ((0x21#6)) (SLLI))) (OR)))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.ADD))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SUB))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SLL))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SLT))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SLTU))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.XOR))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SRL))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.SRA))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.OR))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPE (a) (b) (rop.AND))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.ADDW))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.SUBW))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.SLLW))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.SRLW))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_RTYPEW (a) (b) (ropw.SRAW))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_CLMUL (a) (b) )) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_CLMULH (a) (b) )) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_CLMULR (a) (b) )) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_DIV (a) (b) (false))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_DIV (a) (b) (true))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_DIVW (a) (b) (false))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_DIVW (a) (b) (true))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.High, signed_rs1 := Signedness.Signed, signed_rs2 := Signedness.Signed }))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.High, signed_rs1 := Signedness.Signed, signed_rs2 := Signedness.Unsigned }))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.High, signed_rs1 := Signedness.Unsigned, signed_rs2 := Signedness.Signed }))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.High, signed_rs1 := Signedness.Unsigned, signed_rs2 := Signedness.Unsigned }))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.Low, signed_rs1 := Signedness.Signed, signed_rs2 := Signedness.Signed }))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.Low, signed_rs1 := Signedness.Signed, signed_rs2 := Signedness.Unsigned }))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.Low, signed_rs1 := Signedness.Unsigned, signed_rs2 := Signedness.Signed }))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MUL (a) (b) ({ result_part := VectorHalf.Low, signed_rs1 := Signedness.Unsigned, signed_rs2 := Signedness.Unsigned }))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_MULW (a) (b) )) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_REM (a) (b) (false))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_REM (a) (b) (true))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_REMW (a) (b) (false))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_REMW (a) (b) (true))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.ANDN))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.ORN))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.XNOR))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.MAX))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.MAXU))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.MIN))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.MINU))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.ROL))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPE (a) (b) (brop_zbb.ROR))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPEW (a) (b) (bropw_zbb.ROLW))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBB_RTYPEW (a) (b) (bropw_zbb.RORW))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBKB_RTYPE (a) (b) (brop_zbkb.PACK))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBKB_RTYPE (a) (b) (brop_zbkb.PACKH))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBS_RTYPE (a) (b) (brop_zbs.BCLR))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBS_RTYPE (a) (b) (brop_zbs.BEXT))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBS_RTYPE (a) (b) (brop_zbs.BINV))) (0x5#64) (0x3#64), (fun (a : BitVec 64) (b : BitVec 64) => (pure_ZBS_RTYPE (a) (b) (brop_zbs.BSET))) (0x5#64) (0x3#64)] : List (BitVec 64)).map (fun x => toString x.toNat))}]"
end Functions
end LeanIM
end
