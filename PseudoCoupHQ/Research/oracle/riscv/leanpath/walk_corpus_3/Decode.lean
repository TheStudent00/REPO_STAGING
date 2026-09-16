import LeanIMPrExecutable
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIMPrExecutable LeanIMPrExecutable.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000

/-- a blank machine state, as the emulator's own main starts from -/
def blank : SequentialState RegisterType trivialChoiceSource :=
  { regs := ∅, choiceState := (), mem := ∅, tags := (), cycleCount := 0, sailOutput := #[] }
/-- every register present, with a default value (the emulator's own first step) -/
def filled : SequentialState RegisterType trivialChoiceSource :=
  match ((do
      PreSail.writeReg Register.hart_state default
      PreSail.writeReg Register.mhpmcounter default
      PreSail.writeReg Register.mhpmevent default
      PreSail.writeReg Register.ssp default
      PreSail.writeReg Register.srmcfg default
      PreSail.writeReg Register.satp default
      PreSail.writeReg Register.tlb default
      PreSail.writeReg Register.pma_regions default
      PreSail.writeReg Register.htif_payload_writes default
      PreSail.writeReg Register.htif_cmd_write default
      PreSail.writeReg Register.htif_exit_code default
      PreSail.writeReg Register.htif_done default
      PreSail.writeReg Register.htif_tohost default
      PreSail.writeReg Register.stimecmp default
      PreSail.writeReg Register.mtimecmp default
      PreSail.writeReg Register.htif_tohost_base default
      PreSail.writeReg Register.pc_reset_address default
      PreSail.writeReg Register.elp default
      PreSail.writeReg Register.minstretcfg default
      PreSail.writeReg Register.mcyclecfg default
      PreSail.writeReg Register.vcsr default
      PreSail.writeReg Register.vtype default
      PreSail.writeReg Register.vl default
      PreSail.writeReg Register.vstart default
      PreSail.writeReg Register.vr31 default
      PreSail.writeReg Register.vr30 default
      PreSail.writeReg Register.vr29 default
      PreSail.writeReg Register.vr28 default
      PreSail.writeReg Register.vr27 default
      PreSail.writeReg Register.vr26 default
      PreSail.writeReg Register.vr25 default
      PreSail.writeReg Register.vr24 default
      PreSail.writeReg Register.vr23 default
      PreSail.writeReg Register.vr22 default
      PreSail.writeReg Register.vr21 default
      PreSail.writeReg Register.vr20 default
      PreSail.writeReg Register.vr19 default
      PreSail.writeReg Register.vr18 default
      PreSail.writeReg Register.vr17 default
      PreSail.writeReg Register.vr16 default
      PreSail.writeReg Register.vr15 default
      PreSail.writeReg Register.vr14 default
      PreSail.writeReg Register.vr13 default
      PreSail.writeReg Register.vr12 default
      PreSail.writeReg Register.vr11 default
      PreSail.writeReg Register.vr10 default
      PreSail.writeReg Register.vr9 default
      PreSail.writeReg Register.vr8 default
      PreSail.writeReg Register.vr7 default
      PreSail.writeReg Register.vr6 default
      PreSail.writeReg Register.vr5 default
      PreSail.writeReg Register.vr4 default
      PreSail.writeReg Register.vr3 default
      PreSail.writeReg Register.vr2 default
      PreSail.writeReg Register.vr1 default
      PreSail.writeReg Register.vr0 default
      PreSail.writeReg Register.fcsr default
      PreSail.writeReg Register.f31 default
      PreSail.writeReg Register.f30 default
      PreSail.writeReg Register.f29 default
      PreSail.writeReg Register.f28 default
      PreSail.writeReg Register.f27 default
      PreSail.writeReg Register.f26 default
      PreSail.writeReg Register.f25 default
      PreSail.writeReg Register.f24 default
      PreSail.writeReg Register.f23 default
      PreSail.writeReg Register.f22 default
      PreSail.writeReg Register.f21 default
      PreSail.writeReg Register.f20 default
      PreSail.writeReg Register.f19 default
      PreSail.writeReg Register.f18 default
      PreSail.writeReg Register.f17 default
      PreSail.writeReg Register.f16 default
      PreSail.writeReg Register.f15 default
      PreSail.writeReg Register.f14 default
      PreSail.writeReg Register.f13 default
      PreSail.writeReg Register.f12 default
      PreSail.writeReg Register.f11 default
      PreSail.writeReg Register.f10 default
      PreSail.writeReg Register.f9 default
      PreSail.writeReg Register.f8 default
      PreSail.writeReg Register.f7 default
      PreSail.writeReg Register.f6 default
      PreSail.writeReg Register.f5 default
      PreSail.writeReg Register.f4 default
      PreSail.writeReg Register.f3 default
      PreSail.writeReg Register.f2 default
      PreSail.writeReg Register.f1 default
      PreSail.writeReg Register.f0 default
      PreSail.writeReg Register.pmpaddr_n default
      PreSail.writeReg Register.pmpcfg_n default
      PreSail.writeReg Register.sig_seip default
      PreSail.writeReg Register.sig_meip default
      PreSail.writeReg Register.mideleg default
      PreSail.writeReg Register.medeleg default
      PreSail.writeReg Register.mip default
      PreSail.writeReg Register.mie default
      PreSail.writeReg Register.tselect default
      PreSail.writeReg Register.stval default
      PreSail.writeReg Register.scause default
      PreSail.writeReg Register.sepc default
      PreSail.writeReg Register.sscratch default
      PreSail.writeReg Register.stvec default
      PreSail.writeReg Register.mconfigptr default
      PreSail.writeReg Register.mhartid default
      PreSail.writeReg Register.marchid default
      PreSail.writeReg Register.mimpid default
      PreSail.writeReg Register.mvendorid default
      PreSail.writeReg Register.minstret_increment default
      PreSail.writeReg Register.minstret default
      PreSail.writeReg Register.mtime default
      PreSail.writeReg Register.mcycle default
      PreSail.writeReg Register.mcountinhibit default
      PreSail.writeReg Register.mcounteren default
      PreSail.writeReg Register.scounteren default
      PreSail.writeReg Register.mscratch default
      PreSail.writeReg Register.mtval default
      PreSail.writeReg Register.mepc default
      PreSail.writeReg Register.mcause default
      PreSail.writeReg Register.mtvec default
      PreSail.writeReg Register.cur_inst default
      PreSail.writeReg Register.x31 default
      PreSail.writeReg Register.x30 default
      PreSail.writeReg Register.x29 default
      PreSail.writeReg Register.x28 default
      PreSail.writeReg Register.x27 default
      PreSail.writeReg Register.x26 default
      PreSail.writeReg Register.x25 default
      PreSail.writeReg Register.x24 default
      PreSail.writeReg Register.x23 default
      PreSail.writeReg Register.x22 default
      PreSail.writeReg Register.x21 default
      PreSail.writeReg Register.x20 default
      PreSail.writeReg Register.x19 default
      PreSail.writeReg Register.x18 default
      PreSail.writeReg Register.x17 default
      PreSail.writeReg Register.x16 default
      PreSail.writeReg Register.x15 default
      PreSail.writeReg Register.x14 default
      PreSail.writeReg Register.x13 default
      PreSail.writeReg Register.x12 default
      PreSail.writeReg Register.x11 default
      PreSail.writeReg Register.x10 default
      PreSail.writeReg Register.x9 default
      PreSail.writeReg Register.x8 default
      PreSail.writeReg Register.x7 default
      PreSail.writeReg Register.x6 default
      PreSail.writeReg Register.x5 default
      PreSail.writeReg Register.x4 default
      PreSail.writeReg Register.x3 default
      PreSail.writeReg Register.x2 default
      PreSail.writeReg Register.x1 default
      PreSail.writeReg Register.nextPC default
      PreSail.writeReg Register.PC default
      PreSail.writeReg Register.menvcfg default
      PreSail.writeReg Register.mseccfg default
      PreSail.writeReg Register.senvcfg default
      PreSail.writeReg Register.sstateen3 default
      PreSail.writeReg Register.sstateen2 default
      PreSail.writeReg Register.sstateen1 default
      PreSail.writeReg Register.sstateen0 default
      PreSail.writeReg Register.mstateen3 default
      PreSail.writeReg Register.mstateen2 default
      PreSail.writeReg Register.mstateen1 default
      PreSail.writeReg Register.mstateen0 default
      PreSail.writeReg Register.hstateen3 default
      PreSail.writeReg Register.hstateen2 default
      PreSail.writeReg Register.hstateen1 default
      PreSail.writeReg Register.hstateen0 default
      PreSail.writeReg Register.mstatus default
      PreSail.writeReg Register.misa default
      PreSail.writeReg Register.cur_privilege default
      PreSail.writeReg Register.rvfi_mem_data_present default
      PreSail.writeReg Register.rvfi_mem_data default
      PreSail.writeReg Register.rvfi_int_data_present default
      PreSail.writeReg Register.rvfi_int_data default
      PreSail.writeReg Register.rvfi_pc_data default
      PreSail.writeReg Register.rvfi_inst_data default
      PreSail.writeReg Register.rvfi_instruction default
      PreSail.writeReg Register.fp_rounding_global default
      pure ()) : SailM Unit) blank with | .ok _ s => s | .error _ s => s
/-- then the model's own init and reset -/
def s0 : SequentialState RegisterType trivialChoiceSource :=
  match ((do sail_model_init (); init_model "") : SailM Unit) filled with | .ok _ s => s | .error _ s => s

#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x952e#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__native_first#1\t" ++ ((match (encdec_compressed_backwards (0x8082#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_same_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x0506#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x050d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("and_gpr_gpr_gpr_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x8d6d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("andi_gpr_gpr_imm_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x890d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("auipc_gpr_imm_32__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x658d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x8d2d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__cpp__native_first#1\t" ++ ((match (encdec_backwards (0x00153513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x00b52533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__native_first#1\t" ++ ((match (encdec_backwards (0x00154513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bgeu_gpr_gpr_64__branch_condition__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x00b53533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bne_gpr_gpr_64__branch_condition__cpp__native_first#1\t" ++ ((match (encdec_backwards (0x00a03533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x0ea5d533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__rust__native_first#1\t" ++ ((match (encdec_compressed_backwards (0x157d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_nez_gpr_gpr_gpr_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x0ea5f533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_nez_gpr_gpr_same_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x4501#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("div_gpr_gpr_gpr_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x02a5c633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("div_gpr_gpr_gpr_64__reg_a0__cpp__native_first#1\t" ++ ((match (encdec_backwards (0x6bf59593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("div_gpr_gpr_gpr_64__reg_a0__cpp__native_first#2\t" ++ ((match (encdec_backwards (0x40a5e533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("div_gpr_gpr_gpr_64__reg_a0__cpp__native_first#3\t" ++ ((match (encdec_backwards (0x2bf01593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("div_gpr_gpr_gpr_64__reg_a0__cpp__native_first#4\t" ++ ((match (encdec_backwards (0x0ea65633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("div_gpr_gpr_gpr_64__reg_a0__cpp__native_first#6\t" ++ ((match (encdec_compressed_backwards (0x8d51#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("div_gpr_gpr_gpr_64__reg_a0__rust__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x862a#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("div_gpr_gpr_gpr_64__reg_a0__rust__native_first#1\t" ++ ((match (encdec_compressed_backwards (0x557d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("div_gpr_gpr_gpr_64__reg_a0__rust__native_first#2\t" ++ ((match (encdec_compressed_backwards (0x157e#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("div_gpr_gpr_gpr_64__reg_a0__rust__native_first#3\t" ++ ((match (encdec_backwards (0x00a5c6b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("div_gpr_gpr_gpr_64__reg_a0__rust__native_first#4\t" ++ ((match (encdec_backwards (0xfff64713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("div_gpr_gpr_gpr_64__reg_a0__rust__native_first#5\t" ++ ((match (encdec_compressed_backwards (0x8ed9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("div_gpr_gpr_gpr_64__reg_a0__rust__native_first#6\t" ++ ((match (encdec_compressed_backwards (0xc299#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("div_gpr_gpr_gpr_64__reg_a0__rust__native_first#7\t" ++ ((match (encdec_backwards (0x02c5c533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("div_gpr_gpr_same_64__reg_a0__cpp__native_first#2\t" ++ ((match (encdec_backwards (0x00156513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("div_gpr_gpr_same_64__reg_a0__rust__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x4505#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("divu_gpr_gpr_gpr_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x02a5d533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_d_fpr_fpr_fpr_64__freg_fa0__rust__native_first#0\t" ++ ((match (encdec_backwards (0xf20587d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_d_fpr_fpr_fpr_64__freg_fa0__rust__native_first#1\t" ++ ((match (encdec_backwards (0xf2050753#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_d_fpr_fpr_fpr_64__freg_fa0__rust__native_first#2\t" ++ ((match (encdec_backwards (0x02f777d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_d_fpr_fpr_fpr_64__freg_fa0__rust__native_first#3\t" ++ ((match (encdec_backwards (0xe2078553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__rust__native_first#0\t" ++ ((match (encdec_backwards (0xf00587d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__rust__native_first#1\t" ++ ((match (encdec_backwards (0xf0050753#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__rust__native_first#3\t" ++ ((match (encdec_backwards (0x00f777d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__rust__native_first#4\t" ++ ((match (encdec_backwards (0xe00785d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__rust__native_first#5\t" ++ ((match (encdec_compressed_backwards (0x1502#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__rust__native_first#6\t" ++ ((match (encdec_compressed_backwards (0x8d4d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_l_fpr_gpr_64__freg_fa0__rust__native_first#0\t" ++ ((match (encdec_backwards (0xd22577d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_lu_fpr_gpr_64__freg_fa0__rust__native_first#0\t" ++ ((match (encdec_backwards (0xd23577d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_s_fpr_fpr_64__freg_fa0__rust__native_first#0\t" ++ ((match (encdec_backwards (0xf00507d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_s_fpr_fpr_64__freg_fa0__rust__native_first#1\t" ++ ((match (encdec_backwards (0x420787d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_w_fpr_gpr_64__freg_fa0__rust__native_first#0\t" ++ ((match (encdec_backwards (0xd20507d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_wu_fpr_gpr_64__freg_fa0__rust__native_first#0\t" ++ ((match (encdec_backwards (0xd21507d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_d_fpr_fpr_32__freg_fa0__rust__native_first#0\t" ++ ((match (encdec_backwards (0xf20507d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_d_fpr_fpr_32__freg_fa0__rust__native_first#2\t" ++ ((match (encdec_backwards (0x4017f7d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_l_fpr_gpr_32__freg_fa0__rust__native_first#0\t" ++ ((match (encdec_backwards (0xd02577d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_lu_fpr_gpr_32__freg_fa0__rust__native_first#0\t" ++ ((match (encdec_backwards (0xd03577d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_w_fpr_gpr_32__freg_fa0__rust__native_first#0\t" ++ ((match (encdec_backwards (0xd00577d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_wu_fpr_gpr_32__freg_fa0__rust__native_first#0\t" ++ ((match (encdec_backwards (0xd01577d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fdiv_d_fpr_fpr_fpr_64__freg_fa0__rust__native_first#2\t" ++ ((match (encdec_backwards (0x1af777d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fdiv_s_fpr_fpr_fpr_32__freg_fa0__rust__native_first#2\t" ++ ((match (encdec_backwards (0x18f777d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("feq_d_gpr_fpr_fpr_64__reg_a0__cpp__native_first#2\t" ++ ((match (encdec_backwards (0xa2f72553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("feq_s_gpr_fpr_fpr_32__reg_a0__cpp__native_first#2\t" ++ ((match (encdec_backwards (0xa0f72553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fle_d_gpr_fpr_fpr_64__reg_a0__cpp__native_first#2\t" ++ ((match (encdec_backwards (0xa2f70553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fle_s_gpr_fpr_fpr_32__reg_a0__cpp__native_first#2\t" ++ ((match (encdec_backwards (0xa0f70553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("flt_d_gpr_fpr_fpr_64__reg_a0__cpp__native_first#2\t" ++ ((match (encdec_backwards (0xa2f71553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("flt_s_gpr_fpr_fpr_32__reg_a0__cpp__native_first#2\t" ++ ((match (encdec_backwards (0xa0f71553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("flw_fpr_fpr_32__freg_fa0__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x55fd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("flw_fpr_fpr_32__freg_fa0__cpp__native_first#1\t" ++ ((match (encdec_compressed_backwards (0x1582#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fmul_d_fpr_fpr_fpr_64__freg_fa0__rust__native_first#2\t" ++ ((match (encdec_backwards (0x12f777d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fmul_s_fpr_fpr_fpr_32__freg_fa0__rust__native_first#3\t" ++ ((match (encdec_backwards (0x10f777d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsub_d_fpr_fpr_fpr_64__freg_fa0__rust__native_first#1\t" ++ ((match (encdec_backwards (0xf2058753#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsub_d_fpr_fpr_fpr_64__freg_fa0__rust__native_first#2\t" ++ ((match (encdec_backwards (0x0ae7f7d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsub_s_fpr_fpr_fpr_32__freg_fa0__rust__native_first#1\t" ++ ((match (encdec_backwards (0xf0058753#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsub_s_fpr_fpr_fpr_32__freg_fa0__rust__native_first#3\t" ++ ((match (encdec_backwards (0x08e7f7d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsw_fpr_fpr_32__mem_MEM_fa1__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x9101#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsw_fpr_fpr_32__mem_MEM_fa1__cpp__native_first#2\t" ++ ((match (encdec_backwards (0x08a5853b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsw_fpr_fpr_32__mem_MEM_fa1__rust__native_first#3\t" ++ ((match (encdec_compressed_backwards (0x9181#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x0511#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lui_gpr_imm_32__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x650d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lwu_gpr_fpr_32__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x9d71#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("mul_gpr_gpr_gpr_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x9d4d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("mul_gpr_gpr_gpr_64__reg_a0__rust__native_first#0\t" ++ ((match (encdec_backwards (0x02a58533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("mul_gpr_gpr_same_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x9d49#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("mul_gpr_gpr_same_64__reg_a0__rust__native_first#0\t" ++ ((match (encdec_backwards (0x02a50533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("mulhu_gpr_gpr_gpr_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x02a5b533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("mulhu_gpr_gpr_same_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x02a53533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("ori_gpr_gpr_imm_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x00356513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("rem_gpr_gpr_gpr_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x02a5e633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("rem_gpr_gpr_gpr_64__reg_a0__cpp__native_first#3\t" ++ ((match (encdec_backwards (0x0ea65533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("rem_gpr_gpr_gpr_64__reg_a0__rust__native_first#1\t" ++ ((match (encdec_compressed_backwards (0x56fd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("rem_gpr_gpr_gpr_64__reg_a0__rust__native_first#2\t" ++ ((match (encdec_compressed_backwards (0x16fe#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("rem_gpr_gpr_gpr_64__reg_a0__rust__native_first#3\t" ++ ((match (encdec_compressed_backwards (0x8db5#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("rem_gpr_gpr_gpr_64__reg_a0__rust__native_first#4\t" ++ ((match (encdec_backwards (0xfff54513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("rem_gpr_gpr_gpr_64__reg_a0__rust__native_first#8\t" ++ ((match (encdec_compressed_backwards (0x8d71#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("remu_gpr_gpr_gpr_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x02a5f533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sb_gpr_fpr_8__mem_MEM_fa1__cpp__native_first#0\t" ++ ((match (encdec_backwards (0xf0057513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sh_gpr_fpr_16__mem_MEM_fa1__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x7641#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_gpr_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x00b51533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x00a51533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slli_gpr_gpr_imm_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x050e#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x00352513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x00353513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x40b55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x40a55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x850d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srl_gpr_gpr_gpr_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x00b55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srl_gpr_gpr_same_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x00a55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srli_gpr_gpr_imm_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x810d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srliw_gpr_gpr_imm_32__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x0035551b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sub_gpr_gpr_gpr_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x8d0d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("xori_gpr_gpr_imm_64__reg_a0__cpp__native_first#0\t" ++ ((match (encdec_backwards (0x00354513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
