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


theorem c_op_714__DIVW_true_integer_level (a : BitVec 64) (b : BitVec 64) :
    ((pure_RTYPEW (a) (b) (LeanIM.ropw.SRAW))) = (pure_DIVW (a) (b) (true)) := by
  simp only [pure_RTYPEW, pure_DIVW]
  grind

end Functions
end LeanIM
end
