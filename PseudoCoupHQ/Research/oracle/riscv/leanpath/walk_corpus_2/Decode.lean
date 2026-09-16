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

#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_backwards (0x00a5f633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#1\t" ++ ((match (encdec_compressed_backwards (0x8d2d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#2\t" ++ ((match (encdec_backwards (0x00161593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#3\t" ++ ((match (encdec_backwards (0x00151693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#4\t" ++ ((match (encdec_compressed_backwards (0x8de9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#5\t" ++ ((match (encdec_compressed_backwards (0x8ee9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#6\t" ++ ((match (encdec_compressed_backwards (0x8dd1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#7\t" ++ ((match (encdec_backwards (0x00269613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#8\t" ++ ((match (encdec_backwards (0x00259713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#9\t" ++ ((match (encdec_compressed_backwards (0x8e75#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#10\t" ++ ((match (encdec_compressed_backwards (0x8ef9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#11\t" ++ ((match (encdec_backwards (0x00461713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#12\t" ++ ((match (encdec_compressed_backwards (0x8dd5#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#13\t" ++ ((match (encdec_compressed_backwards (0x8f71#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#14\t" ++ ((match (encdec_backwards (0x00459693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#16\t" ++ ((match (encdec_backwards (0x00871693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#19\t" ++ ((match (encdec_backwards (0x00859613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#20\t" ++ ((match (encdec_compressed_backwards (0x8e79#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#21\t" ++ ((match (encdec_backwards (0x01069713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#23\t" ++ ((match (encdec_backwards (0x01059613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#26\t" ++ ((match (encdec_backwards (0x02059613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#30\t" ++ ((match (encdec_compressed_backwards (0x0586#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#32\t" ++ ((match (encdec_compressed_backwards (0x8082#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_same_64__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x0506#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_backwards (0x00357593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#1\t" ++ ((match (encdec_backwards (0x00354513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#2\t" ++ ((match (encdec_backwards (0x00159613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#4\t" ++ ((match (encdec_compressed_backwards (0x8e69#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#1\t" ++ ((match (encdec_backwards (0x01f5559b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#2\t" ++ ((match (encdec_backwards (0x41f5561b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#3\t" ++ ((match (encdec_backwards (0x00159693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#4\t" ++ ((match (encdec_compressed_backwards (0x8a19#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#5\t" ++ ((match (encdec_compressed_backwards (0x8e4d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#6\t" ++ ((match (encdec_backwards (0x20d64633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#10\t" ++ ((match (encdec_compressed_backwards (0x060a#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#11\t" ++ ((match (encdec_backwards (0x20c5a633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#40\t" ++ ((match (encdec_compressed_backwards (0x1606#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#41\t" ++ ((match (encdec_compressed_backwards (0x1582#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#43\t" ++ ((match (encdec_backwards (0x08b5053b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__rust__all_constructed#3\t" ++ ((match (encdec_compressed_backwards (0x1502#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__rust__all_constructed#7\t" ++ ((match (encdec_compressed_backwards (0x8ecd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__rust__all_constructed#9\t" ++ ((match (encdec_compressed_backwards (0x9101#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__rust__all_constructed#11\t" ++ ((match (encdec_compressed_backwards (0x8e55#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__rust__all_constructed#39\t" ++ ((match (encdec_compressed_backwards (0x8d4d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__rust__all_constructed#40\t" ++ ((match (encdec_compressed_backwards (0x8d51#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("and_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x8d6d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("andi_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x890d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("auipc_gpr_imm_32__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x658d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("auipc_gpr_imm_32__reg_a0__cpp__all_constructed#1\t" ++ ((match (encdec_backwards (0x00b57633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__cpp__all_constructed#1\t" ++ ((match (encdec_backwards (0x00155593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__cpp__all_constructed#3\t" ++ ((match (encdec_backwards (0x00255593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__cpp__all_constructed#5\t" ++ ((match (encdec_backwards (0x00455593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__cpp__all_constructed#7\t" ++ ((match (encdec_backwards (0x00855593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__cpp__all_constructed#9\t" ++ ((match (encdec_backwards (0x01055593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__cpp__all_constructed#11\t" ++ ((match (encdec_backwards (0x02055593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__cpp__all_constructed#13\t" ++ ((match (encdec_compressed_backwards (0x4585#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__cpp__all_constructed#14\t" ++ ((match (encdec_backwards (0x40a5f533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__rust__all_constructed#13\t" ++ ((match (encdec_backwards (0xfff54513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__rust__all_constructed#14\t" ++ ((match (encdec_compressed_backwards (0x8905#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#0\t" ++ ((match (encdec_backwards (0x2bf01613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#1\t" ++ ((match (encdec_backwards (0x6bf51513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#2\t" ++ ((match (encdec_backwards (0x40c5c5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#3\t" ++ ((match (encdec_backwards (0x00a5c633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#5\t" ++ ((match (encdec_backwards (0x00167593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#6\t" ++ ((match (encdec_backwards (0x00161693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#8\t" ++ ((match (encdec_compressed_backwards (0x8ef1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#9\t" ++ ((match (encdec_backwards (0x00151593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#10\t" ++ ((match (encdec_compressed_backwards (0x8df1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#14\t" ++ ((match (encdec_backwards (0x00251593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#15\t" ++ ((match (encdec_compressed_backwards (0x8df5#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#16\t" ++ ((match (encdec_backwards (0x00461693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#19\t" ++ ((match (encdec_backwards (0x00451593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#21\t" ++ ((match (encdec_backwards (0x00869613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#24\t" ++ ((match (encdec_backwards (0x00851593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#26\t" ++ ((match (encdec_backwards (0x01061693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#28\t" ++ ((match (encdec_backwards (0x01051593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#31\t" ++ ((match (encdec_backwards (0x02051593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__cpp__all_constructed#35\t" ++ ((match (encdec_compressed_backwards (0x917d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__rust__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x567d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__rust__all_constructed#1\t" ++ ((match (encdec_compressed_backwards (0x8205#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__rust__all_constructed#2\t" ++ ((match (encdec_compressed_backwards (0x8db1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__rust__all_constructed#3\t" ++ ((match (encdec_compressed_backwards (0x0605#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__rust__all_constructed#4\t" ++ ((match (encdec_compressed_backwards (0x8d31#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bgeu_gpr_gpr_64__branch_condition__cpp__all_constructed#0\t" ++ ((match (encdec_backwards (0x40a5c633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bgeu_gpr_gpr_64__branch_condition__cpp__all_constructed#1\t" ++ ((match (encdec_backwards (0x40b57533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bgeu_gpr_gpr_64__branch_condition__rust__all_constructed#0\t" ++ ((match (encdec_backwards (0xfff5c593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bgeu_gpr_gpr_64__branch_condition__rust__all_constructed#1\t" ++ ((match (encdec_backwards (0x00b54633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("blt_gpr_gpr_64__branch_condition__cpp__all_constructed#35\t" ++ ((match (encdec_compressed_backwards (0x9d75#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_backwards (0x00155613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#2\t" ++ ((match (encdec_backwards (0x00255613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#4\t" ++ ((match (encdec_backwards (0x00455613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#6\t" ++ ((match (encdec_backwards (0x00855613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#8\t" ++ ((match (encdec_backwards (0x01055613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#10\t" ++ ((match (encdec_compressed_backwards (0x4605#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#11\t" ++ ((match (encdec_backwards (0x2a061613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#12\t" ++ ((match (encdec_compressed_backwards (0x8d71#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#13\t" ++ ((match (encdec_backwards (0x0ea5d533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#11\t" ++ ((match (encdec_compressed_backwards (0x1602#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#14\t" ++ ((match (encdec_backwards (0x00153513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#15\t" ++ ((match (encdec_compressed_backwards (0x157d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_same_64__reg_a0__cpp__all_constructed#1\t" ++ ((match (encdec_compressed_backwards (0x8dc9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_same_64__reg_a0__cpp__all_constructed#2\t" ++ ((match (encdec_backwards (0x0025d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_same_64__reg_a0__cpp__all_constructed#4\t" ++ ((match (encdec_backwards (0x0045d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_same_64__reg_a0__cpp__all_constructed#6\t" ++ ((match (encdec_backwards (0x0085d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_same_64__reg_a0__cpp__all_constructed#8\t" ++ ((match (encdec_backwards (0x0105d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_same_64__reg_a0__cpp__all_constructed#13\t" ++ ((match (encdec_backwards (0x0eb55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_same_64__reg_a0__rust__all_constructed#14\t" ++ ((match (encdec_backwards (0x0015b593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_same_64__reg_a0__rust__all_constructed#15\t" ++ ((match (encdec_compressed_backwards (0x15fd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_nez_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#13\t" ++ ((match (encdec_backwards (0x0ea5f533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_nez_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#14\t" ++ ((match (encdec_backwards (0x00a03533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_nez_gpr_gpr_same_64__reg_a0__cpp__all_constructed#13\t" ++ ((match (encdec_backwards (0x0eb57533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_nez_gpr_gpr_same_64__reg_a0__rust__all_constructed#14\t" ++ ((match (encdec_backwards (0x00b035b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_d_fpr_fpr_fpr_64__freg_fa0__go__native_first#0\t" ++ ((match (encdec_compressed_backwards (0x0001#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_d_fpr_fpr_fpr_64__freg_fa0__go__native_first#1\t" ++ ((match (encdec_backwards (0xf2058053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_d_fpr_fpr_fpr_64__freg_fa0__go__native_first#2\t" ++ ((match (encdec_backwards (0xf20500d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_d_fpr_fpr_fpr_64__freg_fa0__go__native_first#3\t" ++ ((match (encdec_backwards (0x02008053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_d_fpr_fpr_fpr_64__freg_fa0__go__native_first#4\t" ++ ((match (encdec_backwards (0xe2000553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_d_fpr_fpr_fpr_64__freg_fa0__go__native_first#8\t" ++ ((match (encdec_backwards (0x00008067#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_d_fpr_fpr_fpr_64__freg_fa0__go__native_first#9\t" ++ ((match (encdec_compressed_backwards (0x0000#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__go__native_first#1\t" ++ ((match (encdec_backwards (0xf0058053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__go__native_first#2\t" ++ ((match (encdec_backwards (0xf00500d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__go__native_first#3\t" ++ ((match (encdec_backwards (0x00008053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__go__native_first#4\t" ++ ((match (encdec_backwards (0xe00002d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__go__native_first#5\t" ++ ((match (encdec_compressed_backwards (0x1282#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__go__native_first#6\t" ++ ((match (encdec_backwards (0x0202d293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__go__native_first#7\t" ++ ((match (encdec_compressed_backwards (0x537d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__go__native_first#8\t" ++ ((match (encdec_compressed_backwards (0x1302#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__go__native_first#9\t" ++ ((match (encdec_backwards (0x00536533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_l_fpr_gpr_64__freg_fa0__go__native_first#0\t" ++ ((match (encdec_backwards (0xd2250053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_lu_fpr_gpr_64__freg_fa0__go__native_first#0\t" ++ ((match (encdec_backwards (0x00054663#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_lu_fpr_gpr_64__freg_fa0__go__native_first#2\t" ++ ((match (encdec_backwards (0x0180006f#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_lu_fpr_gpr_64__freg_fa0__go__native_first#3\t" ++ ((match (encdec_backwards (0x00157293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_lu_fpr_gpr_64__freg_fa0__go__native_first#4\t" ++ ((match (encdec_backwards (0x00155313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_lu_fpr_gpr_64__freg_fa0__go__native_first#5\t" ++ ((match (encdec_backwards (0x005362b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_lu_fpr_gpr_64__freg_fa0__go__native_first#6\t" ++ ((match (encdec_backwards (0xd22280d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_lu_fpr_gpr_64__freg_fa0__go__native_first#7\t" ++ ((match (encdec_backwards (0x02108053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_s_fpr_fpr_64__freg_fa0__go__native_first#1\t" ++ ((match (encdec_backwards (0xf0050053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_s_fpr_fpr_64__freg_fa0__go__native_first#2\t" ++ ((match (encdec_backwards (0x42000053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_w_fpr_gpr_64__freg_fa0__go__native_first#0\t" ++ ((match (encdec_backwards (0xd2050053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_wu_fpr_gpr_64__freg_fa0__go__native_first#0\t" ++ ((match (encdec_backwards (0x02051293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_wu_fpr_gpr_64__freg_fa0__go__native_first#2\t" ++ ((match (encdec_backwards (0xd2228053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_d_fpr_fpr_32__freg_fa0__go__native_first#1\t" ++ ((match (encdec_backwards (0xf2050053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_d_fpr_fpr_32__freg_fa0__go__native_first#2\t" ++ ((match (encdec_backwards (0x40100053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_l_fpr_gpr_32__freg_fa0__go__native_first#0\t" ++ ((match (encdec_backwards (0xd0250053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_lu_fpr_gpr_32__freg_fa0__go__native_first#6\t" ++ ((match (encdec_backwards (0xd02280d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_lu_fpr_gpr_32__freg_fa0__go__native_first#7\t" ++ ((match (encdec_backwards (0x00108053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_lu_fpr_gpr_32__freg_fa0__go__native_first#13\t" ++ ((match (encdec_backwards (0x0062e533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_w_fpr_gpr_32__freg_fa0__go__native_first#0\t" ++ ((match (encdec_backwards (0xd0050053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_wu_fpr_gpr_32__freg_fa0__go__native_first#2\t" ++ ((match (encdec_backwards (0xd0228053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fdiv_d_fpr_fpr_fpr_64__freg_fa0__go__native_first#3\t" ++ ((match (encdec_backwards (0x1a008053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fdiv_s_fpr_fpr_fpr_32__freg_fa0__go__native_first#3\t" ++ ((match (encdec_backwards (0x18008053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("flw_fpr_fpr_32__freg_fa0__cpp__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x55fd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fmul_d_fpr_fpr_fpr_64__freg_fa0__go__native_first#3\t" ++ ((match (encdec_backwards (0x12008053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fmul_s_fpr_fpr_fpr_32__freg_fa0__go__native_first#3\t" ++ ((match (encdec_backwards (0x10008053#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fmv_x_w_gpr_fpr_32__reg_a0__cpp__all_constructed#1\t" ++ ((match (encdec_backwards (0x01f55613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsub_d_fpr_fpr_fpr_64__freg_fa0__go__native_first#2\t" ++ ((match (encdec_backwards (0xf20580d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsub_d_fpr_fpr_fpr_64__freg_fa0__go__native_first#3\t" ++ ((match (encdec_backwards (0x221090d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsub_s_fpr_fpr_fpr_32__freg_fa0__go__native_first#2\t" ++ ((match (encdec_backwards (0xf00580d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsub_s_fpr_fpr_fpr_32__freg_fa0__go__native_first#3\t" ++ ((match (encdec_backwards (0x201090d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsw_fpr_fpr_32__mem_MEM_fa1__cpp__all_constructed#2\t" ++ ((match (encdec_backwards (0x08a5853b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsw_fpr_fpr_32__mem_MEM_fa1__rust__all_constructed#3\t" ++ ((match (encdec_compressed_backwards (0x9181#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__cpp__all_constructed#1\t" ++ ((match (encdec_backwards (0x00454613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__cpp__all_constructed#2\t" ++ ((match (encdec_compressed_backwards (0x89a1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__cpp__all_constructed#4\t" ++ ((match (encdec_compressed_backwards (0x2591#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__cpp__all_constructed#7\t" ++ ((match (encdec_backwards (0x00269593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__cpp__all_constructed#8\t" ++ ((match (encdec_backwards (0x00251713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__cpp__all_constructed#11\t" ++ ((match (encdec_backwards (0x00459713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__cpp__all_constructed#12\t" ++ ((match (encdec_compressed_backwards (0x8d55#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__cpp__all_constructed#13\t" ++ ((match (encdec_compressed_backwards (0x8f6d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__cpp__all_constructed#14\t" ++ ((match (encdec_backwards (0x00451693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__cpp__all_constructed#20\t" ++ ((match (encdec_compressed_backwards (0x8df9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lb_gpr_fpr_8__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_backwards (0x03851593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lb_gpr_fpr_8__reg_a0__cpp__all_constructed#1\t" ++ ((match (encdec_backwards (0x00755613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lb_gpr_fpr_8__reg_a0__cpp__all_constructed#2\t" ++ ((match (encdec_compressed_backwards (0x9585#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lb_gpr_fpr_8__reg_a0__cpp__all_constructed#5\t" ++ ((match (encdec_backwards (0x20d5c5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lb_gpr_fpr_8__reg_a0__cpp__all_constructed#29\t" ++ ((match (encdec_compressed_backwards (0x05a2#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lb_gpr_fpr_8__reg_a0__rust__all_constructed#5\t" ++ ((match (encdec_compressed_backwards (0x058a#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lh_gpr_fpr_16__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_backwards (0x03051593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lh_gpr_fpr_16__reg_a0__cpp__all_constructed#1\t" ++ ((match (encdec_backwards (0x00f55613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lh_gpr_fpr_16__reg_a0__cpp__all_constructed#21\t" ++ ((match (encdec_compressed_backwards (0x05c2#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lui_gpr_imm_32__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x650d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lwu_gpr_fpr_32__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x9d71#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("ori_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_backwards (0x00356513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sb_gpr_fpr_8__mem_MEM_fa1__cpp__all_constructed#0\t" ++ ((match (encdec_backwards (0xf0057513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sh_gpr_fpr_16__mem_MEM_fa1__cpp__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x7641#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_backwards (0x0015f613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#1\t" ++ ((match (encdec_backwards (0x00c51533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#2\t" ++ ((match (encdec_backwards (0x0025f613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#4\t" ++ ((match (encdec_backwards (0x0045f613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#6\t" ++ ((match (encdec_backwards (0x0085f613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#8\t" ++ ((match (encdec_backwards (0x0105f613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#10\t" ++ ((match (encdec_backwards (0x0205f593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#11\t" ++ ((match (encdec_backwards (0x00b51533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_backwards (0x00157593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__cpp__all_constructed#1\t" ++ ((match (encdec_backwards (0x00257613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__cpp__all_constructed#2\t" ++ ((match (encdec_backwards (0x00b515b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__cpp__all_constructed#3\t" ++ ((match (encdec_backwards (0x00c595b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__cpp__all_constructed#4\t" ++ ((match (encdec_backwards (0x00457613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__cpp__all_constructed#6\t" ++ ((match (encdec_backwards (0x00857613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__cpp__all_constructed#8\t" ++ ((match (encdec_backwards (0x01057613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__cpp__all_constructed#10\t" ++ ((match (encdec_backwards (0x02057513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__cpp__all_constructed#11\t" ++ ((match (encdec_backwards (0x00a59533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__rust__all_constructed#0\t" ++ ((match (encdec_backwards (0x02057813#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__rust__all_constructed#2\t" ++ ((match (encdec_backwards (0x00857693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__rust__all_constructed#3\t" ++ ((match (encdec_backwards (0x00457713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__rust__all_constructed#4\t" ++ ((match (encdec_backwards (0x00257793#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__rust__all_constructed#7\t" ++ ((match (encdec_backwards (0x00f51533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__rust__all_constructed#8\t" ++ ((match (encdec_backwards (0x00e51533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__rust__all_constructed#9\t" ++ ((match (encdec_backwards (0x00d51533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__rust__all_constructed#11\t" ++ ((match (encdec_backwards (0x01051533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slli_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x050e#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slliw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_backwards (0x0035151b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed#1\t" ++ ((match (encdec_backwards (0x0025f693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed#2\t" ++ ((match (encdec_backwards (0x00c5153b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed#4\t" ++ ((match (encdec_backwards (0x00d5153b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed#5\t" ++ ((match (encdec_backwards (0x0085f693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed#6\t" ++ ((match (encdec_compressed_backwards (0x89c1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed#9\t" ++ ((match (encdec_backwards (0x00b5153b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed#1\t" ++ ((match (encdec_backwards (0x0045f693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed#2\t" ++ ((match (encdec_backwards (0x0025f713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed#3\t" ++ ((match (encdec_backwards (0x0015f793#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed#5\t" ++ ((match (encdec_backwards (0x00f5153b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed#6\t" ++ ((match (encdec_backwards (0x00e5153b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed#15\t" ++ ((match (encdec_backwards (0x02059713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed#47\t" ++ ((match (encdec_compressed_backwards (0x1586#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed#48\t" ++ ((match (encdec_compressed_backwards (0x8d59#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#2\t" ++ ((match (encdec_backwards (0x00457693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#3\t" ++ ((match (encdec_backwards (0x00b515bb#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#4\t" ++ ((match (encdec_backwards (0x00c595bb#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#6\t" ++ ((match (encdec_compressed_backwards (0x8941#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#7\t" ++ ((match (encdec_backwards (0x00d595bb#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#9\t" ++ ((match (encdec_backwards (0x00a5953b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slt_gpr_gpr_same_64__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x4501#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_backwards (0xffc54593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#1\t" ++ ((match (encdec_backwards (0x48151513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#2\t" ++ ((match (encdec_backwards (0x4bf51513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#5\t" ++ ((match (encdec_compressed_backwards (0x8e6d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#7\t" ++ ((match (encdec_backwards (0x00261693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#12\t" ++ ((match (encdec_backwards (0x00469613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#17\t" ++ ((match (encdec_backwards (0x00861693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#22\t" ++ ((match (encdec_backwards (0x01069613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__rust__all_constructed#1\t" ++ ((match (encdec_compressed_backwards (0x566d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__rust__all_constructed#5\t" ++ ((match (encdec_compressed_backwards (0x8eed#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__rust__all_constructed#6\t" ++ ((match (encdec_backwards (0x00151613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#1\t" ++ ((match (encdec_backwards (0x00355613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#4\t" ++ ((match (encdec_compressed_backwards (0x8189#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#15\t" ++ ((match (encdec_backwards (0xfff54613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#18\t" ++ ((match (encdec_backwards (0x40a66533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_backwards (0x03f55613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#1\t" ++ ((match (encdec_backwards (0x00155693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#2\t" ++ ((match (encdec_compressed_backwards (0x167e#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#4\t" ++ ((match (encdec_backwards (0x0015f693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#5\t" ++ ((match (encdec_backwards (0x0ed57533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#6\t" ++ ((match (encdec_backwards (0x0ed65633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#8\t" ++ ((match (encdec_backwards (0x40155613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#9\t" ++ ((match (encdec_backwards (0x00255693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#10\t" ++ ((match (encdec_compressed_backwards (0x9279#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#11\t" ++ ((match (encdec_compressed_backwards (0x167a#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#17\t" ++ ((match (encdec_backwards (0x40355613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#18\t" ++ ((match (encdec_backwards (0x00455693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#19\t" ++ ((match (encdec_compressed_backwards (0x9271#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#20\t" ++ ((match (encdec_compressed_backwards (0x1672#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#26\t" ++ ((match (encdec_backwards (0x40755613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#27\t" ++ ((match (encdec_backwards (0x00855693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#28\t" ++ ((match (encdec_compressed_backwards (0x9261#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#29\t" ++ ((match (encdec_compressed_backwards (0x1662#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#35\t" ++ ((match (encdec_backwards (0x40f55613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#36\t" ++ ((match (encdec_backwards (0x01055693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#37\t" ++ ((match (encdec_compressed_backwards (0x9241#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#38\t" ++ ((match (encdec_compressed_backwards (0x1642#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#40\t" ++ ((match (encdec_backwards (0x0105f693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#45\t" ++ ((match (encdec_backwards (0x41f55613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#46\t" ++ ((match (encdec_backwards (0x02055693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#47\t" ++ ((match (encdec_compressed_backwards (0x9201#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#50\t" ++ ((match (encdec_backwards (0x0eb65633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#2\t" ++ ((match (encdec_compressed_backwards (0xee19#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#4\t" ++ ((match (encdec_compressed_backwards (0xe685#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#6\t" ++ ((match (encdec_compressed_backwards (0xea15#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#8\t" ++ ((match (encdec_compressed_backwards (0xe2a1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#10\t" ++ ((match (encdec_compressed_backwards (0xe631#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#11\t" ++ ((match (encdec_compressed_backwards (0xeda1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#15\t" ++ ((match (encdec_compressed_backwards (0x8105#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#18\t" ++ ((match (encdec_compressed_backwards (0xdef1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#19\t" ++ ((match (encdec_backwards (0x40155693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#20\t" ++ ((match (encdec_compressed_backwards (0x92f9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#21\t" ++ ((match (encdec_compressed_backwards (0x16fa#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#22\t" ++ ((match (encdec_compressed_backwards (0x8109#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#25\t" ++ ((match (encdec_compressed_backwards (0xda61#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#29\t" ++ ((match (encdec_compressed_backwards (0x8111#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#32\t" ++ ((match (encdec_compressed_backwards (0xd2f1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#33\t" ++ ((match (encdec_backwards (0x40755693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#34\t" ++ ((match (encdec_compressed_backwards (0x92e1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#35\t" ++ ((match (encdec_compressed_backwards (0x16e2#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#36\t" ++ ((match (encdec_compressed_backwards (0x8121#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#39\t" ++ ((match (encdec_compressed_backwards (0xde45#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#43\t" ++ ((match (encdec_compressed_backwards (0x8141#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#45\t" ++ ((match (encdec_compressed_backwards (0xd5d5#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed#46\t" ++ ((match (encdec_backwards (0x41f55593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#3\t" ++ ((match (encdec_backwards (0x00257713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#6\t" ++ ((match (encdec_backwards (0x0eb576b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#7\t" ++ ((match (encdec_backwards (0x0eb655b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#9\t" ++ ((match (encdec_backwards (0x4015d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#10\t" ++ ((match (encdec_backwards (0x0025d693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#15\t" ++ ((match (encdec_backwards (0x0ee5f5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#16\t" ++ ((match (encdec_backwards (0x0ee65633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#18\t" ++ ((match (encdec_backwards (0x4035d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#19\t" ++ ((match (encdec_backwards (0x0045d713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#22\t" ++ ((match (encdec_compressed_backwards (0x8e59#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#23\t" ++ ((match (encdec_backwards (0x00857713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#24\t" ++ ((match (encdec_backwards (0x0ed5f5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#27\t" ++ ((match (encdec_backwards (0x4075d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#28\t" ++ ((match (encdec_backwards (0x0085d693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#32\t" ++ ((match (encdec_backwards (0x01057693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#37\t" ++ ((match (encdec_backwards (0x40f5d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#38\t" ++ ((match (encdec_backwards (0x0105d713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#45\t" ++ ((match (encdec_backwards (0x41f5d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#46\t" ++ ((match (encdec_backwards (0x0205d693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed#50\t" ++ ((match (encdec_backwards (0x0ea65633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__rust__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x85aa#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__rust__all_constructed#1\t" ++ ((match (encdec_backwards (0x00157613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__rust__all_constructed#2\t" ++ ((match (encdec_backwards (0x00257693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__rust__all_constructed#5\t" ++ ((match (encdec_compressed_backwards (0xe68d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__rust__all_constructed#7\t" ++ ((match (encdec_compressed_backwards (0xea1d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__rust__all_constructed#9\t" ++ ((match (encdec_compressed_backwards (0xe2a9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__rust__all_constructed#11\t" ++ ((match (encdec_compressed_backwards (0xe639#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__rust__all_constructed#12\t" ++ ((match (encdec_compressed_backwards (0xeda9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__rust__all_constructed#14\t" ++ ((match (encdec_backwards (0x03f5d513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__rust__all_constructed#15\t" ++ ((match (encdec_compressed_backwards (0x157e#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__rust__all_constructed#16\t" ++ ((match (encdec_backwards (0x0015d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__rust__all_constructed#19\t" ++ ((match (encdec_compressed_backwards (0xdee9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__rust__all_constructed#26\t" ++ ((match (encdec_compressed_backwards (0xd679#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__rust__all_constructed#33\t" ++ ((match (encdec_compressed_backwards (0xd2e9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__rust__all_constructed#40\t" ++ ((match (encdec_compressed_backwards (0xda5d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__rust__all_constructed#46\t" ++ ((match (encdec_compressed_backwards (0xd5cd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_backwards (0x40155593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#3\t" ++ ((match (encdec_compressed_backwards (0x91f9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#4\t" ++ ((match (encdec_compressed_backwards (0x1576#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#5\t" ++ ((match (encdec_compressed_backwards (0x15fa#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#1\t" ++ ((match (encdec_backwards (0x0035561b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#2\t" ++ ((match (encdec_backwards (0x01f5551b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#3\t" ++ ((match (encdec_backwards (0x01e5d69b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#4\t" ++ ((match (encdec_backwards (0x01d51713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#5\t" ++ ((match (encdec_compressed_backwards (0x8f51#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#7\t" ++ ((match (encdec_backwards (0x01f5d793#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#8\t" ++ ((match (encdec_backwards (0x01e69593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#9\t" ++ ((match (encdec_compressed_backwards (0x8dd9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#10\t" ++ ((match (encdec_backwards (0x02051693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#11\t" ++ ((match (encdec_compressed_backwards (0x8b99#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#12\t" ++ ((match (encdec_compressed_backwards (0x8fc9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#13\t" ++ ((match (encdec_backwards (0x20c7c733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#14\t" ++ ((match (encdec_compressed_backwards (0x8f49#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#15\t" ++ ((match (encdec_backwards (0x20c74733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#17\t" ++ ((match (encdec_compressed_backwards (0x070a#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#18\t" ++ ((match (encdec_backwards (0x20e52733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#45\t" ++ ((match (encdec_backwards (0x20c74633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#47\t" ++ ((match (encdec_compressed_backwards (0x1506#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__rust__all_constructed#2\t" ++ ((match (encdec_backwards (0x01f5569b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__rust__all_constructed#3\t" ++ ((match (encdec_backwards (0x01e5d51b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__rust__all_constructed#4\t" ++ ((match (encdec_backwards (0x01d69713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__rust__all_constructed#6\t" ++ ((match (encdec_backwards (0x00169713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__rust__all_constructed#7\t" ++ ((match (encdec_compressed_backwards (0x81fd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__rust__all_constructed#8\t" ++ ((match (encdec_compressed_backwards (0x057a#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__rust__all_constructed#10\t" ++ ((match (encdec_backwards (0x02069613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__rust__all_constructed#11\t" ++ ((match (encdec_compressed_backwards (0x8999#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__rust__all_constructed#12\t" ++ ((match (encdec_compressed_backwards (0x8f55#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srl_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#1\t" ++ ((match (encdec_backwards (0x00c55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srl_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed#11\t" ++ ((match (encdec_backwards (0x00b55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srl_gpr_gpr_same_64__reg_a0__cpp__all_constructed#2\t" ++ ((match (encdec_backwards (0x00b555b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srl_gpr_gpr_same_64__reg_a0__cpp__all_constructed#3\t" ++ ((match (encdec_backwards (0x00c5d5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srl_gpr_gpr_same_64__reg_a0__cpp__all_constructed#11\t" ++ ((match (encdec_backwards (0x00a5d533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srl_gpr_gpr_same_64__reg_a0__rust__all_constructed#7\t" ++ ((match (encdec_backwards (0x00f55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srl_gpr_gpr_same_64__reg_a0__rust__all_constructed#8\t" ++ ((match (encdec_backwards (0x00e55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srl_gpr_gpr_same_64__reg_a0__rust__all_constructed#9\t" ++ ((match (encdec_backwards (0x00d55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srl_gpr_gpr_same_64__reg_a0__rust__all_constructed#11\t" ++ ((match (encdec_backwards (0x01055533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srli_gpr_gpr_imm_64__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x810d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srliw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed#0\t" ++ ((match (encdec_backwards (0x0035551b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed#2\t" ++ ((match (encdec_backwards (0x00c5553b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed#4\t" ++ ((match (encdec_backwards (0x00d5553b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed#9\t" ++ ((match (encdec_backwards (0x00b5553b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed#5\t" ++ ((match (encdec_backwards (0x00f5553b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed#6\t" ++ ((match (encdec_backwards (0x00e5553b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#2\t" ++ ((match (encdec_backwards (0x00b555bb#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#3\t" ++ ((match (encdec_backwards (0x00c5d5bb#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#9\t" ++ ((match (encdec_backwards (0x00a5d63b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_same_32__reg_a0__cpp__all_constructed#13\t" ++ ((match (encdec_backwards (0x08a6053b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_same_32__reg_a0__rust__all_constructed#7\t" ++ ((match (encdec_backwards (0x00d5d5bb#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_same_32__reg_a0__rust__all_constructed#9\t" ++ ((match (encdec_backwards (0x00a5d53b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
