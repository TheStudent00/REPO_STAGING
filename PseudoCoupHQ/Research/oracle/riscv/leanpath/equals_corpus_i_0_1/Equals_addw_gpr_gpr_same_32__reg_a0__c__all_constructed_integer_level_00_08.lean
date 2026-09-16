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
set_option linter.unusedVariables false

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
def pure_ZBA_RTYPEUW (v_rs1 : BitVec 64) (v_rs2 : BitVec 64) (shamt : (BitVec 2)) : BitVec 64 :=

  (shift_bits_left (zero_extend (m := 64) (Sail.BitVec.extractLsb v_rs1 31 0))
        shamt) + v_rs2

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_ZBA_RTYPEUW (rs2 : regidx) (rs1 : regidx) (rd : regidx) (shamt : (BitVec 2)) :
    execute_ZBA_RTYPEUW rs2 rs1 rd shamt =
    (do
      let v_rs1 ← rX_bits rs1
      let v_rs2 ← rX_bits rs2
      wX_bits rd (pure_ZBA_RTYPEUW v_rs1 v_rs2 shamt)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_ZBA_RTYPEUW, pure_ZBA_RTYPEUW, bind_assoc, pure_bind]

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
def pure_ZBA_RTYPE (v_rs1 : BitVec 64) (v_rs2 : BitVec 64) (shamt : (BitVec 2)) : BitVec 64 :=

  (shift_bits_left v_rs1 shamt) + v_rs2

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_ZBA_RTYPE (rs2 : regidx) (rs1 : regidx) (rd : regidx) (shamt : (BitVec 2)) :
    execute_ZBA_RTYPE rs2 rs1 rd shamt =
    (do
      let v_rs1 ← rX_bits rs1
      let v_rs2 ← rX_bits rs2
      wX_bits rd (pure_ZBA_RTYPE v_rs1 v_rs2 shamt)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_ZBA_RTYPE, pure_ZBA_RTYPE, bind_assoc, pure_bind]

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
def pure_BREV8 (v_rs1 : BitVec 64) : BitVec 64 :=

  brev8 v_rs1

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_BREV8 (rs1 : regidx) (rd : regidx) :
    execute_BREV8 rs1 rd =
    (do
      let v_rs1 ← rX_bits rs1
      wX_bits rd (pure_BREV8 v_rs1)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_BREV8, pure_BREV8, bind_assoc, pure_bind]

/-- the proposal: the clause's pure form, by the one rule -/
def pure_CLZ (v_rs1 : BitVec 64) : BitVec 64 :=

  to_bits (l := 64) (BitVec.countLeadingZeros v_rs1)

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_CLZ (rs1 : regidx) (rd : regidx) :
    execute_CLZ rs1 rd =
    (do
      let v_rs1 ← rX_bits rs1
      wX_bits rd (pure_CLZ v_rs1)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_CLZ, pure_CLZ, bind_assoc, pure_bind]

/-- the proposal: the clause's pure form, by the one rule -/
def pure_CLZW (v_rs1 : BitVec 64) : BitVec 64 :=

  to_bits (l := 64) (BitVec.countLeadingZeros (Sail.BitVec.extractLsb v_rs1 31 0))

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_CLZW (rs1 : regidx) (rd : regidx) :
    execute_CLZW rs1 rd =
    (do
      let v_rs1 ← rX_bits rs1
      wX_bits rd (pure_CLZW v_rs1)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_CLZW, pure_CLZW, bind_assoc, pure_bind]

/-- the proposal: the clause's pure form, by the one rule -/
def pure_CTZ (v_rs1 : BitVec 64) : BitVec 64 :=

  to_bits (l := 64) (BitVec.countTrailingZeros v_rs1)

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_CTZ (rs1 : regidx) (rd : regidx) :
    execute_CTZ rs1 rd =
    (do
      let v_rs1 ← rX_bits rs1
      wX_bits rd (pure_CTZ v_rs1)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_CTZ, pure_CTZ, bind_assoc, pure_bind]

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

/-- the proposal: the clause's pure form, by the one rule -/
def pure_REV8 (v_rs1 : BitVec 64) : BitVec 64 :=

  rev8 v_rs1

/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/
theorem strip_REV8 (rs1 : regidx) (rd : regidx) :
    execute_REV8 rs1 rd =
    (do
      let v_rs1 ← rX_bits rs1
      wX_bits rd (pure_REV8 v_rs1)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_REV8, pure_REV8, bind_assoc, pure_bind]

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


set_option maxHeartbeats 40000 in
theorem addw_gpr_gpr_same_32__reg_a0__c__all_constructed_00_integer_level (a : BitVec 64) :
    ((pure_ZBA_RTYPEUW ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((0x20#6)) (SLLI))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ITYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRAIW))) ((sign_extend (m := 12) (0x06#6))) (ANDI))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x21#6)) (SLLI))) (OR))) (0x0#2))) = (pure_BREV8 (a) ) := by
  try simp only [pure_RTYPE, pure_SHIFTIOP, pure_ZBA_RTYPEUW, pure_SHIFTIWOP, pure_ZBA_RTYPE, pure_ITYPE, pure_BREV8, brev8, reverse_bits, zeros, Sail.BitVec.length, Sail.BitVec.updateSubrange, Sail.BitVec.extractLsb]
  grind

set_option maxHeartbeats 40000 in
theorem addw_gpr_gpr_same_32__reg_a0__c__all_constructed_01_integer_level (a : BitVec 64) :
    ((pure_ZBA_RTYPEUW ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((0x20#6)) (SLLI))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ITYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRAIW))) ((sign_extend (m := 12) (0x06#6))) (ANDI))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x21#6)) (SLLI))) (OR))) (0x0#2))) = (pure_CLZ (a) ) := by
  try simp only [pure_RTYPE, pure_SHIFTIOP, pure_ZBA_RTYPEUW, pure_SHIFTIWOP, pure_ZBA_RTYPE, pure_ITYPE, pure_CLZ, to_bits]
  grind

set_option maxHeartbeats 40000 in
theorem addw_gpr_gpr_same_32__reg_a0__c__all_constructed_02_integer_level (a : BitVec 64) :
    ((pure_ZBA_RTYPEUW ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((0x20#6)) (SLLI))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ITYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRAIW))) ((sign_extend (m := 12) (0x06#6))) (ANDI))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x21#6)) (SLLI))) (OR))) (0x0#2))) = (pure_CLZW (a) ) := by
  try simp only [pure_RTYPE, pure_SHIFTIOP, pure_ZBA_RTYPEUW, pure_SHIFTIWOP, pure_ZBA_RTYPE, pure_ITYPE, pure_CLZW, to_bits]
  grind

set_option maxHeartbeats 40000 in
theorem addw_gpr_gpr_same_32__reg_a0__c__all_constructed_03_integer_level (a : BitVec 64) :
    ((pure_ZBA_RTYPEUW ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((0x20#6)) (SLLI))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ITYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRAIW))) ((sign_extend (m := 12) (0x06#6))) (ANDI))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x21#6)) (SLLI))) (OR))) (0x0#2))) = (pure_CTZ (a) ) := by
  try simp only [pure_RTYPE, pure_SHIFTIOP, pure_ZBA_RTYPEUW, pure_SHIFTIWOP, pure_ZBA_RTYPE, pure_ITYPE, pure_CTZ, to_bits]
  grind

set_option maxHeartbeats 40000 in
theorem addw_gpr_gpr_same_32__reg_a0__c__all_constructed_04_integer_level (a : BitVec 64) :
    ((pure_ZBA_RTYPEUW ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((0x20#6)) (SLLI))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ITYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRAIW))) ((sign_extend (m := 12) (0x06#6))) (ANDI))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x21#6)) (SLLI))) (OR))) (0x0#2))) = (pure_CTZW (a) ) := by
  try simp only [pure_RTYPE, pure_SHIFTIOP, pure_ZBA_RTYPEUW, pure_SHIFTIWOP, pure_ZBA_RTYPE, pure_ITYPE, pure_CTZW, to_bits]
  grind

set_option maxHeartbeats 40000 in
theorem addw_gpr_gpr_same_32__reg_a0__c__all_constructed_05_integer_level (a : BitVec 64) :
    ((pure_ZBA_RTYPEUW ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((0x20#6)) (SLLI))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ITYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRAIW))) ((sign_extend (m := 12) (0x06#6))) (ANDI))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x21#6)) (SLLI))) (OR))) (0x0#2))) = (pure_REV8 (a) ) := by
  try simp only [pure_RTYPE, pure_SHIFTIOP, pure_ZBA_RTYPEUW, pure_SHIFTIWOP, pure_ZBA_RTYPE, pure_ITYPE, pure_REV8, rev8, zeros, Sail.BitVec.length, Sail.BitVec.updateSubrange, Sail.BitVec.extractLsb]
  grind

set_option maxHeartbeats 40000 in
theorem addw_gpr_gpr_same_32__reg_a0__c__all_constructed_06_integer_level (a : BitVec 64) :
    ((pure_ZBA_RTYPEUW ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((0x20#6)) (SLLI))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ITYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRAIW))) ((sign_extend (m := 12) (0x06#6))) (ANDI))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x21#6)) (SLLI))) (OR))) (0x0#2))) = (pure_ZBB_EXTOP (a) (extop_zbb.SEXTB)) := by
  try simp only [pure_RTYPE, pure_SHIFTIOP, pure_ZBA_RTYPEUW, pure_SHIFTIWOP, pure_ZBA_RTYPE, pure_ITYPE, pure_ZBB_EXTOP, sign_extend, xlenbits, zero_extend, Sail.BitVec.signExtend, Sail.BitVec.zeroExtend]
  grind

set_option maxHeartbeats 40000 in
theorem addw_gpr_gpr_same_32__reg_a0__c__all_constructed_07_integer_level (a : BitVec 64) :
    ((pure_ZBA_RTYPEUW ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((0x20#6)) (SLLI))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ITYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRAIW))) ((sign_extend (m := 12) (0x06#6))) (ANDI))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x21#6)) (SLLI))) (OR))) (0x0#2))) = (pure_ZBB_EXTOP (a) (extop_zbb.SEXTH)) := by
  try simp only [pure_RTYPE, pure_SHIFTIOP, pure_ZBA_RTYPEUW, pure_SHIFTIWOP, pure_ZBA_RTYPE, pure_ITYPE, pure_ZBB_EXTOP, sign_extend, xlenbits, zero_extend, Sail.BitVec.signExtend, Sail.BitVec.zeroExtend]
  grind

set_option maxHeartbeats 40000 in
theorem addw_gpr_gpr_same_32__reg_a0__c__all_constructed_08_integer_level (a : BitVec 64) :
    ((pure_ZBA_RTYPEUW ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) ((pure_RTYPE ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((0x20#6)) (SLLI))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) ((pure_SHIFTIOP ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ZBA_RTYPE ((pure_RTYPE ((pure_ITYPE ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRAIW))) ((sign_extend (m := 12) (0x06#6))) (ANDI))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x02#6)) (SLLI))) (0x1#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((pure_SHIFTIOP ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (0x01#6) (LeanIM.sop.SLLI))) (0x2#2))) ((pure_SHIFTIWOP ((pure_SHIFTIOP (a) ((0x01#6)) (SLLI))) (0x1f#5) (LeanIM.sopw.SRLIW))) (OR))) ((0x21#6)) (SLLI))) (OR))) (0x0#2))) = (pure_ZBB_EXTOP (a) (extop_zbb.ZEXTH)) := by
  try simp only [pure_RTYPE, pure_SHIFTIOP, pure_ZBA_RTYPEUW, pure_SHIFTIWOP, pure_ZBA_RTYPE, pure_ITYPE, pure_ZBB_EXTOP, sign_extend, xlenbits, zero_extend, Sail.BitVec.signExtend, Sail.BitVec.zeroExtend]
  grind

end Functions
end LeanIM
end
