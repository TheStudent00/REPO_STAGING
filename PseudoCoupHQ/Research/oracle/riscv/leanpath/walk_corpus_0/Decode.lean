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

#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_backwards (0x00a5f633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#1\t" ++ ((match (encdec_compressed_backwards (0x8d2d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#2\t" ++ ((match (encdec_backwards (0x00161593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#3\t" ++ ((match (encdec_backwards (0x00151693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#4\t" ++ ((match (encdec_compressed_backwards (0x8de9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#5\t" ++ ((match (encdec_compressed_backwards (0x8ee9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#6\t" ++ ((match (encdec_compressed_backwards (0x8dd1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#7\t" ++ ((match (encdec_backwards (0x00269613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#8\t" ++ ((match (encdec_backwards (0x00259713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#9\t" ++ ((match (encdec_compressed_backwards (0x8e75#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#10\t" ++ ((match (encdec_compressed_backwards (0x8ef9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#11\t" ++ ((match (encdec_backwards (0x00461713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#12\t" ++ ((match (encdec_compressed_backwards (0x8dd5#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#13\t" ++ ((match (encdec_compressed_backwards (0x8f71#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#14\t" ++ ((match (encdec_backwards (0x00459693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#16\t" ++ ((match (encdec_backwards (0x00871693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#19\t" ++ ((match (encdec_backwards (0x00859613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#20\t" ++ ((match (encdec_compressed_backwards (0x8e79#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#21\t" ++ ((match (encdec_backwards (0x01069713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#23\t" ++ ((match (encdec_backwards (0x01059613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#26\t" ++ ((match (encdec_backwards (0x02059613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#30\t" ++ ((match (encdec_compressed_backwards (0x0586#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__c__all_constructed#32\t" ++ ((match (encdec_compressed_backwards (0x8082#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#0\t" ++ ((match (encdec_backwards (0x00a5f2b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#1\t" ++ ((match (encdec_backwards (0x00129313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#2\t" ++ ((match (encdec_backwards (0x00a5c3b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#3\t" ++ ((match (encdec_backwards (0x0063f333#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#4\t" ++ ((match (encdec_backwards (0x005362b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#5\t" ++ ((match (encdec_backwards (0x00229313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#6\t" ++ ((match (encdec_backwards (0x00139413#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#7\t" ++ ((match (encdec_backwards (0x00747433#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#8\t" ++ ((match (encdec_backwards (0x00647333#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#9\t" ++ ((match (encdec_backwards (0x0062e2b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#10\t" ++ ((match (encdec_backwards (0x00429313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#11\t" ++ ((match (encdec_backwards (0x00241493#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#12\t" ++ ((match (encdec_compressed_backwards (0x8c65#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#13\t" ++ ((match (encdec_backwards (0x00837333#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#15\t" ++ ((match (encdec_backwards (0x00829313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#16\t" ++ ((match (encdec_backwards (0x00441493#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#20\t" ++ ((match (encdec_backwards (0x01029313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#21\t" ++ ((match (encdec_backwards (0x00841493#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#25\t" ++ ((match (encdec_backwards (0x02029313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#26\t" ++ ((match (encdec_backwards (0x01041493#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#30\t" ++ ((match (encdec_compressed_backwards (0x0286#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#31\t" ++ ((match (encdec_backwards (0x0072c533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#32\t" ++ ((match (encdec_backwards (0x00008067#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_gpr_64__reg_a0__go__all_constructed#33\t" ++ ((match (encdec_compressed_backwards (0x0000#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("add_gpr_gpr_same_64__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x0506#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_backwards (0x00357593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__c__all_constructed#1\t" ++ ((match (encdec_backwards (0x00354513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__c__all_constructed#2\t" ++ ((match (encdec_backwards (0x00159613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__c__all_constructed#4\t" ++ ((match (encdec_compressed_backwards (0x8e69#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__go__all_constructed#0\t" ++ ((match (encdec_backwards (0x00357293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__go__all_constructed#2\t" ++ ((match (encdec_backwards (0x00354393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__go__all_constructed#7\t" ++ ((match (encdec_backwards (0x007473b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__go__all_constructed#11\t" ++ ((match (encdec_backwards (0x00239413#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__go__all_constructed#13\t" ++ ((match (encdec_backwards (0x00737333#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__go__all_constructed#16\t" ++ ((match (encdec_backwards (0x00439413#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__go__all_constructed#21\t" ++ ((match (encdec_backwards (0x00839413#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__go__all_constructed#26\t" ++ ((match (encdec_backwards (0x01039413#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__go__all_constructed#31\t" ++ ((match (encdec_backwards (0x00a2c2b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addi_gpr_gpr_imm_64__reg_a0__go__all_constructed#32\t" ++ ((match (encdec_backwards (0x0032c513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__c__all_constructed#1\t" ++ ((match (encdec_backwards (0x01f5559b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__c__all_constructed#2\t" ++ ((match (encdec_backwards (0x41f5561b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__c__all_constructed#3\t" ++ ((match (encdec_backwards (0x00159693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__c__all_constructed#4\t" ++ ((match (encdec_compressed_backwards (0x8a19#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__c__all_constructed#5\t" ++ ((match (encdec_compressed_backwards (0x8e4d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__c__all_constructed#6\t" ++ ((match (encdec_backwards (0x20d64633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__c__all_constructed#10\t" ++ ((match (encdec_compressed_backwards (0x060a#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__c__all_constructed#11\t" ++ ((match (encdec_backwards (0x20c5a633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__c__all_constructed#40\t" ++ ((match (encdec_compressed_backwards (0x1606#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__c__all_constructed#41\t" ++ ((match (encdec_compressed_backwards (0x1582#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("addw_gpr_gpr_same_32__reg_a0__c__all_constructed#43\t" ++ ((match (encdec_backwards (0x08b5053b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("and_gpr_gpr_gpr_64__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x8d6d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("andi_gpr_gpr_imm_64__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x890d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("andi_gpr_gpr_imm_64__reg_a0__go__all_constructed#0\t" ++ ((match (encdec_backwards (0x0ff57293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("andi_gpr_gpr_imm_64__reg_a0__go__all_constructed#1\t" ++ ((match (encdec_backwards (0x0032f513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("auipc_gpr_imm_32__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x658d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("auipc_gpr_imm_32__reg_a0__c__all_constructed#1\t" ++ ((match (encdec_backwards (0x00b57633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("auipc_gpr_imm_32__reg_a0__go__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x6f8d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("auipc_gpr_imm_32__reg_a0__go__all_constructed#1\t" ++ ((match (encdec_backwards (0x01f572b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("auipc_gpr_imm_32__reg_a0__go__all_constructed#4\t" ++ ((match (encdec_backwards (0x01f543b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("auipc_gpr_imm_32__reg_a0__go__all_constructed#35\t" ++ ((match (encdec_backwards (0x01f2c533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__c__all_constructed#1\t" ++ ((match (encdec_backwards (0x00155593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__c__all_constructed#2\t" ++ ((match (encdec_compressed_backwards (0x8d4d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__c__all_constructed#3\t" ++ ((match (encdec_backwards (0x00255593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__c__all_constructed#5\t" ++ ((match (encdec_backwards (0x00455593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__c__all_constructed#7\t" ++ ((match (encdec_backwards (0x00855593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__c__all_constructed#9\t" ++ ((match (encdec_backwards (0x01055593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__c__all_constructed#11\t" ++ ((match (encdec_backwards (0x02055593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__c__all_constructed#13\t" ++ ((match (encdec_compressed_backwards (0x4585#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__c__all_constructed#14\t" ++ ((match (encdec_backwards (0x40a5f533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__go__all_constructed#0\t" ++ ((match (encdec_backwards (0x00b542b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__go__all_constructed#1\t" ++ ((match (encdec_backwards (0x0012d313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__go__all_constructed#3\t" ++ ((match (encdec_backwards (0x0022d313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__go__all_constructed#5\t" ++ ((match (encdec_backwards (0x0042d313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__go__all_constructed#7\t" ++ ((match (encdec_backwards (0x0082d313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__go__all_constructed#9\t" ++ ((match (encdec_backwards (0x0102d313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__go__all_constructed#11\t" ++ ((match (encdec_backwards (0x0202d313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__go__all_constructed#13\t" ++ ((match (encdec_backwards (0x0012f293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("beq_gpr_gpr_64__branch_condition__go__all_constructed#14\t" ++ ((match (encdec_backwards (0x0012b513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#0\t" ++ ((match (encdec_backwards (0x2bf01613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#1\t" ++ ((match (encdec_backwards (0x6bf51513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#2\t" ++ ((match (encdec_backwards (0x40c5c5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#3\t" ++ ((match (encdec_backwards (0x00a5c633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#5\t" ++ ((match (encdec_backwards (0x00167593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#6\t" ++ ((match (encdec_backwards (0x00161693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#8\t" ++ ((match (encdec_compressed_backwards (0x8ef1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#9\t" ++ ((match (encdec_backwards (0x00151593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#10\t" ++ ((match (encdec_compressed_backwards (0x8df1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#14\t" ++ ((match (encdec_backwards (0x00251593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#15\t" ++ ((match (encdec_compressed_backwards (0x8df5#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#16\t" ++ ((match (encdec_backwards (0x00461693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#19\t" ++ ((match (encdec_backwards (0x00451593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#21\t" ++ ((match (encdec_backwards (0x00869613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#24\t" ++ ((match (encdec_backwards (0x00851593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#26\t" ++ ((match (encdec_backwards (0x01061693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#28\t" ++ ((match (encdec_backwards (0x01051593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#31\t" ++ ((match (encdec_backwards (0x02051593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__c__all_constructed#35\t" ++ ((match (encdec_compressed_backwards (0x917d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x52fd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#1\t" ++ ((match (encdec_compressed_backwards (0x12fe#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#2\t" ++ ((match (encdec_backwards (0x00b2c333#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#3\t" ++ ((match (encdec_backwards (0xfff34313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#4\t" ++ ((match (encdec_backwards (0x00a2c3b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#5\t" ++ ((match (encdec_backwards (0x00a34433#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#6\t" ++ ((match (encdec_backwards (0x0082c2b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#7\t" ++ ((match (encdec_backwards (0x0012f413#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#9\t" ++ ((match (encdec_backwards (0x00646333#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#10\t" ++ ((match (encdec_backwards (0x00131393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#11\t" ++ ((match (encdec_backwards (0x0053f3b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#12\t" ++ ((match (encdec_backwards (0x0063e333#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#13\t" ++ ((match (encdec_backwards (0x00231393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#14\t" ++ ((match (encdec_backwards (0x00129413#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#15\t" ++ ((match (encdec_backwards (0x005472b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#16\t" ++ ((match (encdec_backwards (0x0072f3b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#17\t" ++ ((match (encdec_backwards (0x00736333#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#18\t" ++ ((match (encdec_backwards (0x00431393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#19\t" ++ ((match (encdec_backwards (0x00229413#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#23\t" ++ ((match (encdec_backwards (0x00831393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#24\t" ++ ((match (encdec_backwards (0x00429413#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#28\t" ++ ((match (encdec_backwards (0x01031393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#29\t" ++ ((match (encdec_backwards (0x00829413#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#33\t" ++ ((match (encdec_backwards (0x02031393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#34\t" ++ ((match (encdec_backwards (0x01029413#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#36\t" ++ ((match (encdec_backwards (0x0053f2b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#38\t" ++ ((match (encdec_backwards (0x03f2d293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bge_gpr_gpr_64__branch_condition__go__all_constructed#40\t" ++ ((match (encdec_backwards (0x00503533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bgeu_gpr_gpr_64__branch_condition__c__all_constructed#0\t" ++ ((match (encdec_backwards (0x40a5c633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bgeu_gpr_gpr_64__branch_condition__c__all_constructed#1\t" ++ ((match (encdec_backwards (0x40b57533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bgeu_gpr_gpr_64__branch_condition__go__all_constructed#1\t" ++ ((match (encdec_backwards (0xfff2c293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bgeu_gpr_gpr_64__branch_condition__go__all_constructed#2\t" ++ ((match (encdec_backwards (0x0012f313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bgeu_gpr_gpr_64__branch_condition__go__all_constructed#3\t" ++ ((match (encdec_backwards (0xfff5c393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bgeu_gpr_gpr_64__branch_condition__go__all_constructed#4\t" ++ ((match (encdec_backwards (0x007573b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("blt_gpr_gpr_64__branch_condition__c__all_constructed#35\t" ++ ((match (encdec_compressed_backwards (0x9d75#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("blt_gpr_gpr_64__branch_condition__go__all_constructed#41\t" ++ ((match (encdec_compressed_backwards (0x0001#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("bne_gpr_gpr_64__branch_condition__c__all_constructed#13\t" ++ ((match (encdec_compressed_backwards (0x8905#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_backwards (0x00155613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__c__all_constructed#1\t" ++ ((match (encdec_compressed_backwards (0x8d51#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__c__all_constructed#2\t" ++ ((match (encdec_backwards (0x00255613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__c__all_constructed#4\t" ++ ((match (encdec_backwards (0x00455613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__c__all_constructed#6\t" ++ ((match (encdec_backwards (0x00855613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__c__all_constructed#8\t" ++ ((match (encdec_backwards (0x01055613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__c__all_constructed#10\t" ++ ((match (encdec_compressed_backwards (0x4605#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__c__all_constructed#11\t" ++ ((match (encdec_backwards (0x2a061613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__c__all_constructed#12\t" ++ ((match (encdec_compressed_backwards (0x8d71#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__c__all_constructed#13\t" ++ ((match (encdec_backwards (0x0ea5d533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__go__all_constructed#0\t" ++ ((match (encdec_backwards (0x00155293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__go__all_constructed#1\t" ++ ((match (encdec_backwards (0x00a2e2b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__go__all_constructed#14\t" ++ ((match (encdec_backwards (0x00029363#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__go__all_constructed#15\t" ++ ((match (encdec_compressed_backwards (0x4581#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_gpr_64__reg_a0__go__all_constructed#16\t" ++ ((match (encdec_compressed_backwards (0x852e#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_same_64__reg_a0__c__all_constructed#1\t" ++ ((match (encdec_compressed_backwards (0x8dc9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_same_64__reg_a0__c__all_constructed#2\t" ++ ((match (encdec_backwards (0x0025d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_same_64__reg_a0__c__all_constructed#4\t" ++ ((match (encdec_backwards (0x0045d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_same_64__reg_a0__c__all_constructed#6\t" ++ ((match (encdec_backwards (0x0085d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_same_64__reg_a0__c__all_constructed#8\t" ++ ((match (encdec_backwards (0x0105d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_same_64__reg_a0__c__all_constructed#13\t" ++ ((match (encdec_backwards (0x0eb55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_eqz_gpr_gpr_same_64__reg_a0__go__all_constructed#15\t" ++ ((match (encdec_compressed_backwards (0x4501#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_nez_gpr_gpr_gpr_64__reg_a0__c__all_constructed#13\t" ++ ((match (encdec_backwards (0x0ea5f533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_nez_gpr_gpr_gpr_64__reg_a0__go__all_constructed#14\t" ++ ((match (encdec_backwards (0x00028363#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("czero_nez_gpr_gpr_same_64__reg_a0__c__all_constructed#13\t" ++ ((match (encdec_backwards (0x0eb57533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_d_fpr_fpr_fpr_64__freg_fa0__c__native_first#0\t" ++ ((match (encdec_backwards (0xf20587d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_d_fpr_fpr_fpr_64__freg_fa0__c__native_first#1\t" ++ ((match (encdec_backwards (0xf2050753#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_d_fpr_fpr_fpr_64__freg_fa0__c__native_first#2\t" ++ ((match (encdec_backwards (0x02f777d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_d_fpr_fpr_fpr_64__freg_fa0__c__native_first#3\t" ++ ((match (encdec_backwards (0xe2078553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__c__native_first#0\t" ++ ((match (encdec_backwards (0xf00587d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__c__native_first#1\t" ++ ((match (encdec_backwards (0xf0050753#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__c__native_first#2\t" ++ ((match (encdec_compressed_backwards (0x557d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__c__native_first#3\t" ++ ((match (encdec_backwards (0x00f777d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__c__native_first#4\t" ++ ((match (encdec_backwards (0xe00785d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fadd_s_fpr_fpr_fpr_32__freg_fa0__c__native_first#5\t" ++ ((match (encdec_compressed_backwards (0x1502#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_l_fpr_gpr_64__freg_fa0__c__native_first#0\t" ++ ((match (encdec_backwards (0xd22577d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_lu_fpr_gpr_64__freg_fa0__c__native_first#0\t" ++ ((match (encdec_backwards (0xd23577d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_s_fpr_fpr_64__freg_fa0__c__native_first#0\t" ++ ((match (encdec_backwards (0xf00507d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_s_fpr_fpr_64__freg_fa0__c__native_first#1\t" ++ ((match (encdec_backwards (0x420787d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_w_fpr_gpr_64__freg_fa0__c__native_first#0\t" ++ ((match (encdec_backwards (0xd20507d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_d_wu_fpr_gpr_64__freg_fa0__c__native_first#0\t" ++ ((match (encdec_backwards (0xd21507d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_d_fpr_fpr_32__freg_fa0__c__native_first#0\t" ++ ((match (encdec_backwards (0xf20507d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_d_fpr_fpr_32__freg_fa0__c__native_first#2\t" ++ ((match (encdec_backwards (0x4017f7d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_l_fpr_gpr_32__freg_fa0__c__native_first#0\t" ++ ((match (encdec_backwards (0xd02577d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_lu_fpr_gpr_32__freg_fa0__c__native_first#0\t" ++ ((match (encdec_backwards (0xd03577d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_w_fpr_gpr_32__freg_fa0__c__native_first#0\t" ++ ((match (encdec_backwards (0xd00577d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fcvt_s_wu_fpr_gpr_32__freg_fa0__c__native_first#0\t" ++ ((match (encdec_backwards (0xd01577d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fdiv_d_fpr_fpr_fpr_64__freg_fa0__c__native_first#2\t" ++ ((match (encdec_backwards (0x1af777d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fdiv_s_fpr_fpr_fpr_32__freg_fa0__c__native_first#2\t" ++ ((match (encdec_backwards (0x18f777d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("flw_fpr_fpr_32__freg_fa0__c__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x55fd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("flw_fpr_fpr_32__freg_fa0__go__all_constructed#0\t" ++ ((match (encdec_backwards (0x02051293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("flw_fpr_fpr_32__freg_fa0__go__all_constructed#1\t" ++ ((match (encdec_backwards (0x0202d293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("flw_fpr_fpr_32__freg_fa0__go__all_constructed#2\t" ++ ((match (encdec_compressed_backwards (0x537d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("flw_fpr_fpr_32__freg_fa0__go__all_constructed#3\t" ++ ((match (encdec_compressed_backwards (0x1302#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("flw_fpr_fpr_32__freg_fa0__go__all_constructed#4\t" ++ ((match (encdec_backwards (0x00536533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fmul_d_fpr_fpr_fpr_64__freg_fa0__c__native_first#2\t" ++ ((match (encdec_backwards (0x12f777d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fmul_s_fpr_fpr_fpr_32__freg_fa0__c__native_first#3\t" ++ ((match (encdec_backwards (0x10f777d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fmv_x_w_gpr_fpr_32__reg_a0__c__all_constructed#1\t" ++ ((match (encdec_backwards (0x01f55613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsub_d_fpr_fpr_fpr_64__freg_fa0__c__native_first#1\t" ++ ((match (encdec_backwards (0xf2058753#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsub_d_fpr_fpr_fpr_64__freg_fa0__c__native_first#2\t" ++ ((match (encdec_backwards (0x0ae7f7d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsub_s_fpr_fpr_fpr_32__freg_fa0__c__native_first#1\t" ++ ((match (encdec_backwards (0xf0058753#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsub_s_fpr_fpr_fpr_32__freg_fa0__c__native_first#3\t" ++ ((match (encdec_backwards (0x08e7f7d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsw_fpr_fpr_32__mem_MEM_fa1__c__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x9101#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsw_fpr_fpr_32__mem_MEM_fa1__c__all_constructed#2\t" ++ ((match (encdec_backwards (0x08a5853b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsw_fpr_fpr_32__mem_MEM_fa1__go__all_constructed#1\t" ++ ((match (encdec_compressed_backwards (0x1282#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsw_fpr_fpr_32__mem_MEM_fa1__go__all_constructed#2\t" ++ ((match (encdec_backwards (0x005572b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsw_fpr_fpr_32__mem_MEM_fa1__go__all_constructed#3\t" ++ ((match (encdec_backwards (0x02059313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsw_fpr_fpr_32__mem_MEM_fa1__go__all_constructed#4\t" ++ ((match (encdec_backwards (0x02035313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("fsw_fpr_fpr_32__mem_MEM_fa1__go__all_constructed#5\t" ++ ((match (encdec_backwards (0x0062e533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__c__all_constructed#1\t" ++ ((match (encdec_backwards (0x00454613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__c__all_constructed#2\t" ++ ((match (encdec_compressed_backwards (0x89a1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__c__all_constructed#4\t" ++ ((match (encdec_compressed_backwards (0x2591#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__c__all_constructed#7\t" ++ ((match (encdec_backwards (0x00269593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__c__all_constructed#8\t" ++ ((match (encdec_backwards (0x00251713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__c__all_constructed#11\t" ++ ((match (encdec_backwards (0x00459713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__c__all_constructed#12\t" ++ ((match (encdec_compressed_backwards (0x8d55#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__c__all_constructed#13\t" ++ ((match (encdec_compressed_backwards (0x8f6d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__c__all_constructed#14\t" ++ ((match (encdec_backwards (0x00451693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__c__all_constructed#20\t" ++ ((match (encdec_compressed_backwards (0x8df9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__c__all_constructed#31\t" ++ ((match (encdec_compressed_backwards (0x8d31#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__go__all_constructed#0\t" ++ ((match (encdec_backwards (0x00457293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__go__all_constructed#2\t" ++ ((match (encdec_backwards (0x00454393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("jal_gpr_fpr_64__reg_a0__go__all_constructed#32\t" ++ ((match (encdec_backwards (0x0042c513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lb_gpr_fpr_8__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_backwards (0x03851593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lb_gpr_fpr_8__reg_a0__c__all_constructed#1\t" ++ ((match (encdec_backwards (0x00755613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lb_gpr_fpr_8__reg_a0__c__all_constructed#2\t" ++ ((match (encdec_compressed_backwards (0x9585#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lb_gpr_fpr_8__reg_a0__c__all_constructed#3\t" ++ ((match (encdec_compressed_backwards (0x9181#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lb_gpr_fpr_8__reg_a0__c__all_constructed#5\t" ++ ((match (encdec_backwards (0x20d5c5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lb_gpr_fpr_8__reg_a0__c__all_constructed#29\t" ++ ((match (encdec_compressed_backwards (0x05a2#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lbu_gpr_fpr_8__reg_a0__go__all_constructed#0\t" ++ ((match (encdec_backwards (0x0ff57513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lh_gpr_fpr_16__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_backwards (0x03051593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lh_gpr_fpr_16__reg_a0__c__all_constructed#1\t" ++ ((match (encdec_backwards (0x00f55613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lh_gpr_fpr_16__reg_a0__c__all_constructed#21\t" ++ ((match (encdec_compressed_backwards (0x05c2#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lhu_gpr_fpr_16__reg_a0__go__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x1542#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lhu_gpr_fpr_16__reg_a0__go__all_constructed#1\t" ++ ((match (encdec_compressed_backwards (0x9141#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lui_gpr_imm_32__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x650d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("lwu_gpr_fpr_32__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x9d71#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("ori_gpr_gpr_imm_64__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_backwards (0x00356513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sb_gpr_fpr_8__mem_MEM_fa1__c__all_constructed#0\t" ++ ((match (encdec_backwards (0xf0057513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sb_gpr_fpr_8__mem_MEM_fa1__go__all_constructed#0\t" ++ ((match (encdec_backwards (0x0ff5f293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sb_gpr_fpr_8__mem_MEM_fa1__go__all_constructed#1\t" ++ ((match (encdec_backwards (0xf0057313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sh_gpr_fpr_16__mem_MEM_fa1__c__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x7641#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sh_gpr_fpr_16__mem_MEM_fa1__go__all_constructed#0\t" ++ ((match (encdec_backwards (0x03059293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sh_gpr_fpr_16__mem_MEM_fa1__go__all_constructed#1\t" ++ ((match (encdec_backwards (0x0302d293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sh_gpr_fpr_16__mem_MEM_fa1__go__all_constructed#2\t" ++ ((match (encdec_compressed_backwards (0x7fc1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sh_gpr_fpr_16__mem_MEM_fa1__go__all_constructed#3\t" ++ ((match (encdec_backwards (0x01f57333#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_gpr_64__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_backwards (0x0015f613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_gpr_64__reg_a0__c__all_constructed#1\t" ++ ((match (encdec_backwards (0x00c51533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_gpr_64__reg_a0__c__all_constructed#2\t" ++ ((match (encdec_backwards (0x0025f613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_gpr_64__reg_a0__c__all_constructed#4\t" ++ ((match (encdec_backwards (0x0045f613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_gpr_64__reg_a0__c__all_constructed#6\t" ++ ((match (encdec_backwards (0x0085f613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_gpr_64__reg_a0__c__all_constructed#8\t" ++ ((match (encdec_backwards (0x0105f613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_gpr_64__reg_a0__c__all_constructed#10\t" ++ ((match (encdec_backwards (0x0205f593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_gpr_64__reg_a0__c__all_constructed#11\t" ++ ((match (encdec_backwards (0x00b51533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_backwards (0x00157593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__c__all_constructed#1\t" ++ ((match (encdec_backwards (0x00257613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__c__all_constructed#2\t" ++ ((match (encdec_backwards (0x00b515b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__c__all_constructed#3\t" ++ ((match (encdec_backwards (0x00c595b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__c__all_constructed#4\t" ++ ((match (encdec_backwards (0x00457613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__c__all_constructed#6\t" ++ ((match (encdec_backwards (0x00857613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__c__all_constructed#8\t" ++ ((match (encdec_backwards (0x01057613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__c__all_constructed#10\t" ++ ((match (encdec_backwards (0x02057513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sll_gpr_gpr_same_64__reg_a0__c__all_constructed#11\t" ++ ((match (encdec_backwards (0x00a59533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slli_gpr_gpr_imm_64__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x050e#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slli_gpr_gpr_imm_64__reg_a0__go__all_constructed#1\t" ++ ((match (encdec_backwards (0x0032d293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slli_gpr_gpr_imm_64__reg_a0__go__all_constructed#3\t" ++ ((match (encdec_backwards (0x00329513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slliw_gpr_gpr_imm_32__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_backwards (0x0035151b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__c__all_constructed#1\t" ++ ((match (encdec_backwards (0x0025f693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__c__all_constructed#2\t" ++ ((match (encdec_backwards (0x00c5153b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__c__all_constructed#4\t" ++ ((match (encdec_backwards (0x00d5153b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__c__all_constructed#5\t" ++ ((match (encdec_backwards (0x0085f693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__c__all_constructed#6\t" ++ ((match (encdec_compressed_backwards (0x89c1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_gpr_32__reg_a0__c__all_constructed#9\t" ++ ((match (encdec_backwards (0x00b5153b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_same_32__reg_a0__c__all_constructed#2\t" ++ ((match (encdec_backwards (0x00457693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_same_32__reg_a0__c__all_constructed#3\t" ++ ((match (encdec_backwards (0x00b515bb#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_same_32__reg_a0__c__all_constructed#4\t" ++ ((match (encdec_backwards (0x00c595bb#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_same_32__reg_a0__c__all_constructed#6\t" ++ ((match (encdec_compressed_backwards (0x8941#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_same_32__reg_a0__c__all_constructed#7\t" ++ ((match (encdec_backwards (0x00d595bb#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sllw_gpr_gpr_same_32__reg_a0__c__all_constructed#9\t" ++ ((match (encdec_backwards (0x00a5953b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_backwards (0xffc54593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__c__all_constructed#1\t" ++ ((match (encdec_backwards (0x48151513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__c__all_constructed#2\t" ++ ((match (encdec_backwards (0x4bf51513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__c__all_constructed#5\t" ++ ((match (encdec_compressed_backwards (0x8e6d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__c__all_constructed#7\t" ++ ((match (encdec_backwards (0x00261693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__c__all_constructed#12\t" ++ ((match (encdec_backwards (0x00469613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__c__all_constructed#17\t" ++ ((match (encdec_backwards (0x00861693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__c__all_constructed#22\t" ++ ((match (encdec_backwards (0x01069613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#3\t" ++ ((match (encdec_backwards (0xffc54313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#4\t" ++ ((match (encdec_backwards (0x00137393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#5\t" ++ ((match (encdec_compressed_backwards (0x547d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#6\t" ++ ((match (encdec_compressed_backwards (0x040e#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#7\t" ++ ((match (encdec_compressed_backwards (0x8005#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#8\t" ++ ((match (encdec_backwards (0x0082f2b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#9\t" ++ ((match (encdec_backwards (0x0053e2b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#10\t" ++ ((match (encdec_backwards (0x00129393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#11\t" ++ ((match (encdec_backwards (0x0063f3b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#13\t" ++ ((match (encdec_backwards (0x00229393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#14\t" ++ ((match (encdec_backwards (0x00131413#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#16\t" ++ ((match (encdec_backwards (0x007373b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#17\t" ++ ((match (encdec_backwards (0x0072e2b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#18\t" ++ ((match (encdec_backwards (0x00429393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#19\t" ++ ((match (encdec_backwards (0x00231413#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#23\t" ++ ((match (encdec_backwards (0x00829393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#24\t" ++ ((match (encdec_backwards (0x00431413#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#28\t" ++ ((match (encdec_backwards (0x01029393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#29\t" ++ ((match (encdec_backwards (0x00831413#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#33\t" ++ ((match (encdec_backwards (0x02029393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("slti_gpr_gpr_imm_64__reg_a0__go__all_constructed#34\t" ++ ((match (encdec_backwards (0x01031413#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__c__all_constructed#1\t" ++ ((match (encdec_backwards (0x00355613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__c__all_constructed#4\t" ++ ((match (encdec_compressed_backwards (0x8189#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__c__all_constructed#15\t" ++ ((match (encdec_backwards (0xfff54613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__c__all_constructed#16\t" ++ ((match (encdec_compressed_backwards (0x8205#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__c__all_constructed#17\t" ++ ((match (encdec_backwards (0x0015b593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__c__all_constructed#18\t" ++ ((match (encdec_backwards (0x40a66533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#0\t" ++ ((match (encdec_backwards (0x00255293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#2\t" ++ ((match (encdec_backwards (0x00235313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#3\t" ++ ((match (encdec_backwards (0x005372b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#4\t" ++ ((match (encdec_backwards (0x0012d393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#7\t" ++ ((match (encdec_backwards (0x0062f2b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#8\t" ++ ((match (encdec_backwards (0x0042d393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#12\t" ++ ((match (encdec_backwards (0x0082d393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#16\t" ++ ((match (encdec_backwards (0x0102d393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#20\t" ++ ((match (encdec_backwards (0x0202d393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#22\t" ++ ((match (encdec_backwards (0x00357393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#23\t" ++ ((match (encdec_backwards (0x0033c393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#24\t" ++ ((match (encdec_backwards (0x0033f393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#25\t" ++ ((match (encdec_backwards (0x0013d41b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#26\t" ++ ((match (encdec_compressed_backwards (0x880d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#27\t" ++ ((match (encdec_backwards (0x0083e3b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#29\t" ++ ((match (encdec_backwards (0x0013f313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#30\t" ++ ((match (encdec_backwards (0x00030863#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#32\t" ++ ((match (encdec_backwards (0x005032b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#33\t" ++ ((match (encdec_backwards (0x0060006f#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed#34\t" ++ ((match (encdec_compressed_backwards (0x4285#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_backwards (0x03f55613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#1\t" ++ ((match (encdec_backwards (0x00155693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#2\t" ++ ((match (encdec_compressed_backwards (0x167e#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#3\t" ++ ((match (encdec_compressed_backwards (0x8e55#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#4\t" ++ ((match (encdec_backwards (0x0015f693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#5\t" ++ ((match (encdec_backwards (0x0ed57533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#6\t" ++ ((match (encdec_backwards (0x0ed65633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#8\t" ++ ((match (encdec_backwards (0x40155613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#9\t" ++ ((match (encdec_backwards (0x00255693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#10\t" ++ ((match (encdec_compressed_backwards (0x9279#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#11\t" ++ ((match (encdec_compressed_backwards (0x167a#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#17\t" ++ ((match (encdec_backwards (0x40355613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#18\t" ++ ((match (encdec_backwards (0x00455693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#19\t" ++ ((match (encdec_compressed_backwards (0x9271#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#20\t" ++ ((match (encdec_compressed_backwards (0x1672#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#22\t" ++ ((match (encdec_backwards (0x0045f693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#26\t" ++ ((match (encdec_backwards (0x40755613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#27\t" ++ ((match (encdec_backwards (0x00855693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#28\t" ++ ((match (encdec_compressed_backwards (0x9261#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#29\t" ++ ((match (encdec_compressed_backwards (0x1662#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#35\t" ++ ((match (encdec_backwards (0x40f55613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#36\t" ++ ((match (encdec_backwards (0x01055693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#37\t" ++ ((match (encdec_compressed_backwards (0x9241#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#38\t" ++ ((match (encdec_compressed_backwards (0x1642#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#40\t" ++ ((match (encdec_backwards (0x0105f693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#45\t" ++ ((match (encdec_backwards (0x41f55613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#46\t" ++ ((match (encdec_backwards (0x02055693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#47\t" ++ ((match (encdec_compressed_backwards (0x9201#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#48\t" ++ ((match (encdec_compressed_backwards (0x1602#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed#50\t" ++ ((match (encdec_backwards (0x0eb65633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#3\t" ++ ((match (encdec_backwards (0x00257713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#6\t" ++ ((match (encdec_backwards (0x0eb576b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#7\t" ++ ((match (encdec_backwards (0x0eb655b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#9\t" ++ ((match (encdec_backwards (0x4015d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#10\t" ++ ((match (encdec_backwards (0x0025d693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#15\t" ++ ((match (encdec_backwards (0x0ee5f5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#16\t" ++ ((match (encdec_backwards (0x0ee65633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#18\t" ++ ((match (encdec_backwards (0x4035d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#19\t" ++ ((match (encdec_backwards (0x0045d713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#22\t" ++ ((match (encdec_compressed_backwards (0x8e59#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#23\t" ++ ((match (encdec_backwards (0x00857713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#24\t" ++ ((match (encdec_backwards (0x0ed5f5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#27\t" ++ ((match (encdec_backwards (0x4075d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#28\t" ++ ((match (encdec_backwards (0x0085d693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#32\t" ++ ((match (encdec_backwards (0x01057693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#37\t" ++ ((match (encdec_backwards (0x40f5d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#38\t" ++ ((match (encdec_backwards (0x0105d713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#45\t" ++ ((match (encdec_backwards (0x41f5d613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#46\t" ++ ((match (encdec_backwards (0x0205d693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sra_gpr_gpr_same_64__reg_a0__c__all_constructed#50\t" ++ ((match (encdec_backwards (0x0ea65633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_backwards (0x40155593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__c__all_constructed#3\t" ++ ((match (encdec_compressed_backwards (0x91f9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__c__all_constructed#4\t" ++ ((match (encdec_compressed_backwards (0x1576#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__c__all_constructed#5\t" ++ ((match (encdec_compressed_backwards (0x15fa#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__go__all_constructed#0\t" ++ ((match (encdec_backwards (0x03f55293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__go__all_constructed#2\t" ++ ((match (encdec_backwards (0x00028563#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__go__all_constructed#5\t" ++ ((match (encdec_compressed_backwards (0x4281#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__go__all_constructed#7\t" ++ ((match (encdec_backwards (0x00155313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__go__all_constructed#9\t" ++ ((match (encdec_backwards (0x03f2d313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__go__all_constructed#10\t" ++ ((match (encdec_backwards (0x00137313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__go__all_constructed#11\t" ++ ((match (encdec_backwards (0x00030563#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__go__all_constructed#14\t" ++ ((match (encdec_compressed_backwards (0x4301#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__go__all_constructed#15\t" ++ ((match (encdec_compressed_backwards (0x137a#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srai_gpr_gpr_imm_64__reg_a0__go__all_constructed#16\t" ++ ((match (encdec_backwards (0x0022d293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#1\t" ++ ((match (encdec_backwards (0x0035561b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#2\t" ++ ((match (encdec_backwards (0x01f5551b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#3\t" ++ ((match (encdec_backwards (0x01e5d69b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#4\t" ++ ((match (encdec_backwards (0x01d51713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#5\t" ++ ((match (encdec_compressed_backwards (0x8f51#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#6\t" ++ ((match (encdec_backwards (0x00151613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#7\t" ++ ((match (encdec_backwards (0x01f5d793#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#8\t" ++ ((match (encdec_backwards (0x01e69593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#9\t" ++ ((match (encdec_compressed_backwards (0x8dd9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#10\t" ++ ((match (encdec_backwards (0x02051693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#11\t" ++ ((match (encdec_compressed_backwards (0x8b99#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#12\t" ++ ((match (encdec_compressed_backwards (0x8fc9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#13\t" ++ ((match (encdec_backwards (0x20c7c733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#14\t" ++ ((match (encdec_compressed_backwards (0x8f49#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#15\t" ++ ((match (encdec_backwards (0x20c74733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#17\t" ++ ((match (encdec_compressed_backwards (0x070a#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#18\t" ++ ((match (encdec_backwards (0x20e52733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#45\t" ++ ((match (encdec_backwards (0x20c74633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed#47\t" ++ ((match (encdec_compressed_backwards (0x1506#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srl_gpr_gpr_gpr_64__reg_a0__c__all_constructed#1\t" ++ ((match (encdec_backwards (0x00c55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srl_gpr_gpr_gpr_64__reg_a0__c__all_constructed#11\t" ++ ((match (encdec_backwards (0x00b55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srl_gpr_gpr_same_64__reg_a0__c__all_constructed#2\t" ++ ((match (encdec_backwards (0x00b555b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srl_gpr_gpr_same_64__reg_a0__c__all_constructed#3\t" ++ ((match (encdec_backwards (0x00c5d5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srl_gpr_gpr_same_64__reg_a0__c__all_constructed#11\t" ++ ((match (encdec_backwards (0x00a5d533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srli_gpr_gpr_imm_64__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_compressed_backwards (0x810d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srli_gpr_gpr_imm_64__reg_a0__go__all_constructed#0\t" ++ ((match (encdec_backwards (0x00355293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srli_gpr_gpr_imm_64__reg_a0__go__all_constructed#2\t" ++ ((match (encdec_backwards (0x00335313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srli_gpr_gpr_imm_64__reg_a0__go__all_constructed#3\t" ++ ((match (encdec_backwards (0x0062f533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srliw_gpr_gpr_imm_32__reg_a0__c__all_constructed#0\t" ++ ((match (encdec_backwards (0x0035551b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srliw_gpr_gpr_imm_32__reg_a0__go__all_constructed#0\t" ++ ((match (encdec_backwards (0x0035529b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srliw_gpr_gpr_imm_32__reg_a0__go__all_constructed#1\t" ++ ((match (encdec_backwards (0x20000fb7#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srliw_gpr_gpr_imm_32__reg_a0__go__all_constructed#2\t" ++ ((match (encdec_compressed_backwards (0x3ffd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srliw_gpr_gpr_imm_32__reg_a0__go__all_constructed#3\t" ++ ((match (encdec_backwards (0x01f2f533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_gpr_32__reg_a0__c__all_constructed#2\t" ++ ((match (encdec_backwards (0x00c5553b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_gpr_32__reg_a0__c__all_constructed#4\t" ++ ((match (encdec_backwards (0x00d5553b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_gpr_32__reg_a0__c__all_constructed#9\t" ++ ((match (encdec_backwards (0x00b5553b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_same_32__reg_a0__c__all_constructed#2\t" ++ ((match (encdec_backwards (0x00b555bb#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_same_32__reg_a0__c__all_constructed#3\t" ++ ((match (encdec_backwards (0x00c5d5bb#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_same_32__reg_a0__c__all_constructed#9\t" ++ ((match (encdec_backwards (0x00a5d63b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_same_32__reg_a0__c__all_constructed#10\t" ++ ((match (encdec_compressed_backwards (0x81fd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("srlw_gpr_gpr_same_32__reg_a0__c__all_constructed#13\t" ++ ((match (encdec_backwards (0x08a6053b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("xori_gpr_gpr_imm_64__reg_a0__go__all_constructed#2\t" ++ ((match (encdec_backwards (0x0032f293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("xori_gpr_gpr_imm_64__reg_a0__go__all_constructed#3\t" ++ ((match (encdec_backwards (0xffc57313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
