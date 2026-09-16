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
/-- the alias: this clause re-dispatches to another instruction -/
def alias_C_AND (rsd : cregidx) (rs2 : cregidx) : instruction :=
  (RTYPE (((creg2reg_idx rs2)), ((creg2reg_idx rsd)), ((creg2reg_idx rsd)), AND))

theorem strip_C_AND (rsd : cregidx) (rs2 : cregidx) :
    execute_C_AND rsd rs2 = (ExecuteAs (alias_C_AND rsd rs2)) := by
  rfl

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

set_option linter.unusedVariables false

abbrev St := SequentialState RegisterType trivialChoiceSource

/-- the program ends in a state whose answering register holds v -/
def runsTo (m : SailM ExecutionResult) (s : St) (v : BitVec 64) : Prop :=
  match m s with
  | .ok _ s' => s'.regs.get? .x10 = some v
  | .error _ _ => False

/-- one instruction through the model's own execute; an ExecuteAs re-dispatches once -/
def step (i : instruction) : SailM ExecutionResult := do
  match (← execute i) with
  | .ExecuteAs j => execute j
  | r => pure r

def walk : List instruction → SailM ExecutionResult
  | [] => pure RETIRE_SUCCESS
  | i :: is => do let _ ← step i; walk is

/-- the unit's meaning: its proposal, certified -/
theorem meaning_cpp__op_335 (s : St) (a : BitVec 64) (b : BitVec 64) (h10 : s.regs.get? .x10 = some a) (h11 : s.regs.get? .x11 = some b) (hk0 : ∀ {α : Type} (x0 : α) (s : St), (plat_term_write x0) s = EStateM.Result.ok () s) (hk1 : ∀ (x0 : Arch.pa) (x1 : Nat) (s : St), (load_reservation x0 x1) s = EStateM.Result.ok () s) (hk2 : ∀ (x0 : Unit) (s : St), (cancel_reservation x0) s = EStateM.Result.ok () s) :
    runsTo (walk [LeanIM.instruction.RTYPE (LeanIM.regidx.Regidx 0x0a#5, LeanIM.regidx.Regidx 0x00#5, LeanIM.regidx.Regidx 0x0a#5, LeanIM.rop.SLTU), LeanIM.instruction.C_AND (LeanIM.cregidx.Cregidx 0x2#3, LeanIM.cregidx.Cregidx 0x3#3)]) s
      ((pure_RTYPE ((pure_RTYPE (zero_reg) (a) (LeanIM.rop.SLTU))) (b) (AND))) := by
  simp (config := {decide := true}) [runsTo, walk, step, execute, strip_C_AND, strip_RTYPE, alias_C_AND,
    rX_bits, rX, wX_bits, wX, regval_from_reg, regval_into_reg, PreSail.readReg, PreSail.writeReg,
    RETIRE_SUCCESS, reg_name_forwards, to_bits, zero_reg,
    csr_full_read_callback, csr_full_write_callback, csr_id_read_callback, csr_id_write_callback, csr_name_read_callback, csr_name_write_callback, fetch_callback, freg_write_callback, instret_callback, long_csr_write_callback, mem_exception_callback, mem_read_callback, mem_write_callback, pc_write_callback, ptw_fail_callback, ptw_start_callback, ptw_step_callback, ptw_success_callback, redirect_callback, tlb_add_callback, tlb_flush_begin_callback, tlb_flush_callback, tlb_flush_end_callback, trap_callback, vreg_write_callback, xreg_full_write_callback, xreg_write_callback, xret_callback, RETIRE_SUCCESS, creg2reg_idx, fregidx_to_regidx, rX_bits, ra, regidx_offset_range, sp, t0, wX_bits, zreg, zero_extend, trunc, SailM, rX, wX, RegisterType, readReg, regtype, regval_from_reg, zero_reg, regval_into_reg, to_bits, writeReg, xlenbits, zeros, Sail.BitVec.extractLsb, Sail.BitVec.zeroExtend, Sail.BitVec.truncate, Sail.ConcurrencyInterfaceV1.trivialChoiceSource, Sail.ConcurrencyInterfaceV1.PreSailM, Sail.get_slice_int,
    bind, pure, get, getThe, modify, modifyGet, set, throw,
    EStateM.bind, EStateM.pure, EStateM.get, EStateM.set, EStateM.modifyGet, EStateM.throw,
    EStateM.instMonad, EStateM.instMonadStateOf, MonadStateOf.get, MonadStateOf.set,
    MonadStateOf.modifyGet, MonadState.get, MonadState.set, MonadState.modifyGet,
    BitVec.toNatInt, Std.ExtDHashMap.get?_insert_self, Std.ExtDHashMap.get?_insert,
    h10, h11, hk0, hk1, hk2]

end Functions
end LeanIM
end
