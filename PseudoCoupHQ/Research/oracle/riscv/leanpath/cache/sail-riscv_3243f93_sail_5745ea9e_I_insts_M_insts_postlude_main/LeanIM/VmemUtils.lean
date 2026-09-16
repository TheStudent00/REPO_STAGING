import LeanIM.Flow
import LeanIM.Prelude
import LeanIM.Xlen
import LeanIM.MemAddrtype
import LeanIM.PlatformConfig
import LeanIM.Types
import LeanIM.VmemTypes
import LeanIM.AddrChecks
import LeanIM.SyncException
import LeanIM.PmUtils
import LeanIM.SysControl
import LeanIM.SplitAccessUtils
import LeanIM.Mem
import LeanIM.Vmem
import LeanIM.InstsBegin

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

open xRET_type
open wxfunct6
open wvxfunct6
open wvvfunct6
open wvfunct6
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
open extension
open exception
open cregidx
open cfregidx
open cbop_zicbop
open cbop_zicbom
open cacheop
open breakpoint_cause
open bop
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
open TranslationStage
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
open HGATPMode
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

/-- Type quantifiers: k_ex555858_ : Bool -/
def plat_misaligned_exception (access : (MemoryAccessType mem_payload)) (res : Bool) : (Option misaligned_exception) :=
  if ((is_amo_access access) : Bool)
  then plat_misaligned_access.amo
  else
    (if (res : Bool)
    then plat_misaligned_access.lrsc
    else
      (if ((is_vector_access access) : Bool)
      then plat_misaligned_access.vector
      else plat_misaligned_access.load_store))

def offset_virtaddr_by (typ_0 : virtaddr) (typ_1 : physaddr) (typ_2 : physaddr) : virtaddr :=
  let .Virtaddr base_vaddr : virtaddr := typ_0
  let .Physaddr base_paddr : physaddr := typ_1
  let .Physaddr exc_paddr : physaddr := typ_2
  let offset := (Sail.BitVec.extractLsb (exc_paddr - base_paddr) (xlen -i 1) 0)
  let reconstructed := (base_vaddr + offset)
  let masked := (reconstructed &&& (zero_extend (m := 64) (ones (n := physaddr_bits))))
  (Virtaddr masked)

/-- Type quantifiers: pmlen : Nat, pmlen ∈ {0, 7, 16} -/
def transform_effective_address (vaddr : virtaddr) (eff_privilege : Privilege) (pmlen : Nat) : SailM virtaddr := do
  let mode ← do
    if (((eff_privilege == VirtualSupervisor) || (eff_privilege == VirtualUser)) : Bool)
    then (vsatp_mode ())
    else (satp_mode eff_privilege)
  if ((mode == Bare) : Bool)
  then (pure (pm_transform_PA vaddr pmlen))
  else (pure (pm_transform_VA vaddr pmlen))

def access_is_gva (access : (MemoryAccessType mem_payload)) : SailM Bool := do
  (pure (privLevel_is_virtual
      (← (effectivePrivilege access (← readReg mstatus) (← readReg cur_privilege)))))

def mem_exception_context (e : ExceptionType) (excinfo : (BitVec 64)) (access : (MemoryAccessType mem_payload)) : SailM ExceptionContext := do
  (pure (make_exception_context e excinfo (← (access_is_gva access)) none))

def memory_exception (e : ExceptionType) (excinfo : (BitVec 64)) (access : (MemoryAccessType mem_payload)) : SailM ExecutionResult := do
  (trap (← (mem_exception_context e excinfo access)))

/-- Type quantifiers: k_ex555862_ : Bool, k_ex555861_ : Bool, k_ex555860_ : Bool, width : Nat, width
  ≥ 0, 0 < width ∧ width ≤ max_mem_access -/
def translate_and_read_value (vaddr : virtaddr) (width : Nat) (eff_priv : Privilege) (access : (MemoryAccessType mem_payload)) (aq : Bool) (rl : Bool) (res : Bool) : SailM (Result (physaddr × (BitVec (8 * width))) ExecutionResult) := do
  match (← (translateAddr vaddr access eff_priv)) with
  | .Err (e, _) => (pure (Err (← (trap e))))
  | .Ok (paddr, pbmt, _) =>
    (do
      match (← (mem_read access pbmt eff_priv paddr width aq rl res)) with
      | .Err (exc_paddr, e) =>
        (do
          let exc_vaddr := (offset_virtaddr_by vaddr paddr exc_paddr)
          (pure (Err (← (memory_exception e (bits_of_virtaddr exc_vaddr) access)))))
      | .Ok v => (pure (Ok (paddr, v))))

/-- Type quantifiers: k_ex555868_ : Bool, k_ex555867_ : Bool, k_ex555866_ : Bool, width : Nat, width
  ≥ 0, is_mem_width(width) -/
def vmem_read_addr (vaddr : virtaddr) (width : Nat) (access : (MemoryAccessType mem_payload)) (eff_priv : Privilege) (aq : Bool) (rl : Bool) (res : Bool) : SailM (Result (BitVec (8 * width)) ExecutionResult) := SailME.run do
  assert (res == (is_load_reserved access)) "sys/vmem_utils.sail:108.40-108.41"
  if ((not (is_aligned_vaddr vaddr width)) : Bool)
  then
    (do
      match (plat_misaligned_exception access res) with
      | .some .AccessFault =>
        SailME.throw (← do
            (pure (Err
                (← (memory_exception (E_Load_Access_Fault ()) (bits_of_virtaddr vaddr) access)))))
      | .some .AlignmentException =>
        SailME.throw (← do
            (pure (Err
                (← (memory_exception (E_Load_Addr_Align ()) (bits_of_virtaddr vaddr) access)))))
      | none => (pure ()))
  else (pure ())
  let vaddr_bits := (bits_of_virtaddr vaddr)
  let (in_page_bytes, next_page_bytes) ← do (split_on_page_boundary vaddr_bits width)
  let data := (zeros (n := (8 *i width)))
  let vmem_active ← (( do
    if ((privLevel_is_virtual eff_priv) : Bool)
    then (pure ((bne (← (vsatp_mode ())) Bare) || (bne (← (hgatp_mode ())) HBare)))
    else (pure (bne (← (satp_mode eff_priv)) Bare)) ) : SailME
    (Result (BitVec (8 * width)) ExecutionResult) Bool )
  let do_split_access := (vmem_active && ((next_page_bytes >b 0) && (not res)))
  let data ← (( do
    if ((sys_misaligned_order_decreasing && do_split_access) : Bool)
    then
      (do
        let access_addr := (Virtaddr (BitVec.addInt vaddr_bits in_page_bytes))
        match (← (translate_and_read_value access_addr next_page_bytes eff_priv access aq rl res)) with
        | .Err e => SailME.throw ((Err e) : (Result (BitVec (8 * width)) ExecutionResult))
        | .Ok (_, v) =>
          (pure (Sail.BitVec.updateSubrange data ((8 *i width) -i 1) (8 *i in_page_bytes) v)))
    else (pure data) ) : SailME (Result (BitVec (8 * width)) ExecutionResult) (BitVec (8 * width)) )
  let access_width :=
    if (do_split_access : Bool)
    then in_page_bytes
    else width
  let data ← (( do
    match (← (translate_and_read_value vaddr access_width eff_priv access aq rl res)) with
    | .Err e => SailME.throw ((Err e) : (Result (BitVec (8 * width)) ExecutionResult))
    | .Ok (paddr, v) =>
      (do
        if (res : Bool)
        then
          (do
            assert (width == access_width) "sys/vmem_utils.sail:155.36-155.37"
            (load_reservation (bits_of_physaddr paddr) width))
        else (pure ())
        (pure (Sail.BitVec.updateSubrange data ((8 *i access_width) -i 1) 0 v))) ) : SailME
    (Result (BitVec (8 * width)) ExecutionResult) (BitVec (8 * width)) )
  let data ← (( do
    if (((not sys_misaligned_order_decreasing) && do_split_access) : Bool)
    then
      (do
        let access_addr := (Virtaddr (BitVec.addInt vaddr_bits in_page_bytes))
        match (← (translate_and_read_value access_addr next_page_bytes eff_priv access aq rl res)) with
        | .Err e => SailME.throw ((Err e) : (Result (BitVec (8 * width)) ExecutionResult))
        | .Ok (_, v) =>
          (pure (Sail.BitVec.updateSubrange data ((8 *i width) -i 1) (8 *i in_page_bytes) v)))
    else (pure data) ) : SailME (Result (BitVec (8 * width)) ExecutionResult) (BitVec (8 * width)) )
  (pure (Ok data))

/-- Type quantifiers: k_ex555873_ : Bool, k_ex555872_ : Bool, k_ex555871_ : Bool, width : Nat, width
  ≥ 0, 0 < width ∧ width ≤ max_mem_access -/
def translate_and_write_value (vaddr : virtaddr) (width : Nat) (value : (BitVec (8 * width))) (eff_priv : Privilege) (access : (MemoryAccessType mem_payload)) (aq : Bool) (rl : Bool) (res : Bool) : SailM (Result Bool ExecutionResult) := do
  match (← (translateAddr vaddr access eff_priv)) with
  | .Err (e, _) => (pure (Err (← (trap e))))
  | .Ok (paddr, pbmt, _) =>
    (do
      match (← (mem_write_ea paddr width eff_priv access pbmt aq rl res)) with
      | .Err (exc_paddr, e) =>
        (do
          let exc_vaddr := (offset_virtaddr_by vaddr paddr exc_paddr)
          (pure (Err (← (memory_exception e (bits_of_virtaddr exc_vaddr) access)))))
      | .Ok () =>
        (do
          match (← (mem_write_value paddr width value eff_priv access pbmt aq rl res)) with
          | .Err (exc_paddr, e) =>
            (do
              let exc_vaddr := (offset_virtaddr_by vaddr paddr exc_paddr)
              (pure (Err (← (memory_exception e (bits_of_virtaddr exc_vaddr) access)))))
          | .Ok s => (pure (Ok s))))

/-- Type quantifiers: k_ex555879_ : Bool, k_ex555878_ : Bool, k_ex555877_ : Bool, width : Nat, width
  ≥ 0, is_mem_width(width) -/
def vmem_write_addr (vaddr : virtaddr) (width : Nat) (data : (BitVec (8 * width))) (access : (MemoryAccessType mem_payload)) (eff_priv : Privilege) (aq : Bool) (rl : Bool) (res : Bool) : SailM (Result Bool ExecutionResult) := SailME.run do
  assert (res == (is_store_conditional access)) "sys/vmem_utils.sail:205.44-205.45"
  if ((not (is_aligned_vaddr vaddr width)) : Bool)
  then
    (do
      match (plat_misaligned_exception access res) with
      | .some .AccessFault =>
        SailME.throw (← do
            (pure (Err
                (← (memory_exception (E_SAMO_Access_Fault ()) (bits_of_virtaddr vaddr) access)))))
      | .some .AlignmentException =>
        SailME.throw (← do
            (pure (Err
                (← (memory_exception (E_SAMO_Addr_Align ()) (bits_of_virtaddr vaddr) access)))))
      | none => (pure ()))
  else (pure ())
  let vaddr_bits := (bits_of_virtaddr vaddr)
  let write_success : Bool := true
  let (in_page_bytes, next_page_bytes) ← do (split_on_page_boundary vaddr_bits width)
  let vmem_active ← (( do
    if ((privLevel_is_virtual eff_priv) : Bool)
    then (pure ((bne (← (vsatp_mode ())) Bare) || (bne (← (hgatp_mode ())) HBare)))
    else (pure (bne (← (satp_mode eff_priv)) Bare)) ) : SailME (Result Bool ExecutionResult) Bool
    )
  let do_split_access := (vmem_active && ((next_page_bytes >b 0) && (not res)))
  let write_success ← (( do
    if ((sys_misaligned_order_decreasing && do_split_access) : Bool)
    then
      (do
        let access_addr := (Virtaddr (BitVec.addInt vaddr_bits in_page_bytes))
        let write_value := (Sail.BitVec.extractLsb data ((8 *i width) -i 1) (8 *i in_page_bytes))
        match (← (translate_and_write_value access_addr next_page_bytes write_value eff_priv
            access aq rl res)) with
        | .Err e => SailME.throw ((Err e) : (Result Bool ExecutionResult))
        | .Ok s => (pure (write_success && s)))
    else (pure write_success) ) : SailME (Result Bool ExecutionResult) Bool )
  let access_width :=
    if (do_split_access : Bool)
    then in_page_bytes
    else width
  let write_success ← (( do
    match (← (translateAddr vaddr access eff_priv)) with
    | .Err (e, _) =>
      SailME.throw (← do
          (pure (Err (← (trap e)))))
    | .Ok (paddr, pbmt, _) =>
      (do
        if ((res && (not (match_reservation (bits_of_physaddr paddr)))) : Bool)
        then
          (do
            match (← (phys_access_check access pbmt eff_priv paddr access_width true)) with
            | .Err e =>
              SailME.throw (← do
                  (pure (Err (← (memory_exception e (bits_of_virtaddr vaddr) access)))))
            | .Ok _ => (pure false))
        else
          (do
            match (← (mem_write_ea paddr access_width eff_priv access pbmt aq rl res)) with
            | .Err (exc_paddr, e) =>
              SailME.throw (← do
                  let exc_vaddr := (offset_virtaddr_by vaddr paddr exc_paddr)
                  (pure (Err (← (memory_exception e (bits_of_virtaddr exc_vaddr) access)))))
            | .Ok () =>
              (do
                let write_value := (Sail.BitVec.extractLsb data ((8 *i access_width) -i 1) 0)
                match (← (mem_write_value paddr access_width write_value eff_priv access pbmt aq
                    rl res)) with
                | .Err (exc_paddr, e) =>
                  SailME.throw (← do
                      let exc_vaddr := (offset_virtaddr_by vaddr paddr exc_paddr)
                      (pure (Err (← (memory_exception e (bits_of_virtaddr exc_vaddr) access)))))
                | .Ok s => (pure (write_success && s))))) ) : SailME (Result Bool ExecutionResult)
    Bool )
  let write_success ← (( do
    if (((not sys_misaligned_order_decreasing) && do_split_access) : Bool)
    then
      (do
        let access_addr := (Virtaddr (BitVec.addInt vaddr_bits in_page_bytes))
        let write_value := (Sail.BitVec.extractLsb data ((8 *i width) -i 1) (8 *i in_page_bytes))
        match (← (translate_and_write_value access_addr next_page_bytes write_value eff_priv
            access aq rl res)) with
        | .Err e => SailME.throw ((Err e) : (Result Bool ExecutionResult))
        | .Ok s => (pure (write_success && s)))
    else (pure write_success) ) : SailME (Result Bool ExecutionResult) Bool )
  (pure (Ok write_success))

/-- Type quantifiers: width : Nat, pmlen : Nat, pmlen ∈ {0, 7, 16}, 1 ≤ width ∧ width ≤ 4096 -/
def get_transformed_data_addr (base : regidx) (offset : (BitVec 64)) (access : (MemoryAccessType mem_payload)) (eff_priv : Privilege) (pmlen : Nat) (width : Nat) : SailM (Ext_DataAddr_Check Unit) := do
  match (← (ext_data_get_addr base offset access width)) with
  | .Ext_DataAddr_Error e => (pure (Ext_DataAddr_Error e))
  | .Ext_DataAddr_OK vaddr =>
    (do
      let vaddr ← do (transform_effective_address vaddr eff_priv pmlen)
      (pure (Ext_DataAddr_OK vaddr)))

/-- Type quantifiers: k_ex555889_ : Bool, k_ex555888_ : Bool, k_ex555887_ : Bool, width : Nat, width
  ≥ 0, is_mem_width(width) -/
def vmem_read (rs : regidx) (offset : (BitVec 64)) (width : Nat) (access : (MemoryAccessType mem_payload)) (aq : Bool) (rl : Bool) (res : Bool) : SailM (Result (BitVec (8 * width)) ExecutionResult) := SailME.run do
  let eff_priv ← do (effectivePrivilege access (← readReg mstatus) (← readReg cur_privilege))
  let pmlen ← do (get_pmlen access eff_priv)
  let vaddr ← (( do
    match (← (get_transformed_data_addr rs offset access eff_priv pmlen width)) with
    | .Ext_DataAddr_OK vaddr => (pure vaddr)
    | .Ext_DataAddr_Error e =>
      SailME.throw ((Err (Ext_DataAddr_Check_Failure e)) : (Result (BitVec (8 * width)) ExecutionResult))
    ) : SailME (Result (BitVec (8 * width)) ExecutionResult) virtaddr )
  (vmem_read_addr vaddr width access eff_priv aq rl res)

/-- Type quantifiers: k_ex555897_ : Bool, k_ex555896_ : Bool, k_ex555895_ : Bool, width : Nat, width
  ≥ 0, is_mem_width(width) -/
def vmem_write (rs_addr : regidx) (offset : (BitVec 64)) (width : Nat) (data : (BitVec (8 * width))) (access : (MemoryAccessType mem_payload)) (aq : Bool) (rl : Bool) (res : Bool) : SailM (Result Bool ExecutionResult) := SailME.run do
  let eff_priv ← do (effectivePrivilege access (← readReg mstatus) (← readReg cur_privilege))
  let pmlen ← do (get_pmlen access eff_priv)
  let vaddr ← (( do
    match (← (get_transformed_data_addr rs_addr offset access eff_priv pmlen width)) with
    | .Ext_DataAddr_OK vaddr => (pure vaddr)
    | .Ext_DataAddr_Error e =>
      SailME.throw ((Err (Ext_DataAddr_Check_Failure e)) : (Result Bool ExecutionResult)) ) : SailME
    (Result Bool ExecutionResult) virtaddr )
  (vmem_write_addr vaddr width data access eff_priv aq rl res)

