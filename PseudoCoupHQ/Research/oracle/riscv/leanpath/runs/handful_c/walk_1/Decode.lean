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

#eval IO.println ("c__op_1#0\t" ++ ((match (encdec_backwards (0x00153513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_1#1\t" ++ ((match (encdec_compressed_backwards (0x8082#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_5#0\t" ++ ((match (encdec_backwards (0x00154513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_13#0\t" ++ ((match (encdec_backwards (0x40a00533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_33#0\t" ++ ((match (encdec_compressed_backwards (0x1141#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_33#1\t" ++ ((match (encdec_compressed_backwards (0x0068#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_33#2\t" ++ ((match (encdec_backwards (0x00a12627#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_33#3\t" ++ ((match (encdec_compressed_backwards (0x0141#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_37#0\t" ++ ((match (encdec_compressed_backwards (0x0505#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_41#0\t" ++ ((match (encdec_compressed_backwards (0x4505#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_45#0\t" ++ ((match (encdec_backwards (0xf01007d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_45#1\t" ++ ((match (encdec_backwards (0x00f57553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_49#0\t" ++ ((match (encdec_compressed_backwards (0x4521#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_57#0\t" ++ ((match (encdec_compressed_backwards (0x4511#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_105#0\t" ++ ((match (encdec_backwards (0xd00577d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_109#0\t" ++ ((match (encdec_compressed_backwards (0x952e#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_117#0\t" ++ ((match (encdec_backwards (0xd03577d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_121#0\t" ++ ((match (encdec_backwards (0xd02577d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_125#0\t" ++ ((match (encdec_backwards (0xd01577d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_129#0\t" ++ ((match (encdec_backwards (0x420587d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_129#1\t" ++ ((match (encdec_backwards (0x02f57553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_141#1\t" ++ ((match (encdec_backwards (0x08a7f553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_145#0\t" ++ ((match (encdec_compressed_backwards (0x8d0d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_157#1\t" ++ ((match (encdec_backwards (0x08f57553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_165#1\t" ++ ((match (encdec_backwards (0x0af57553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_177#1\t" ++ ((match (encdec_backwards (0x10f57553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_181#0\t" ++ ((match (encdec_compressed_backwards (0x9d4d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_185#0\t" ++ ((match (encdec_backwards (0x0eb55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_201#1\t" ++ ((match (encdec_backwards (0x12f57553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_205#0\t" ++ ((match (encdec_backwards (0x0ea5d533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_209#0\t" ++ ((match (encdec_compressed_backwards (0x8d6d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_213#1\t" ++ ((match (encdec_backwards (0x18a7f553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_217#0\t" ++ ((match (encdec_backwards (0x02b54533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_229#1\t" ++ ((match (encdec_backwards (0x18f57553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_237#1\t" ++ ((match (encdec_backwards (0x1af57553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_253#0\t" ++ ((match (encdec_backwards (0x02b56533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_257#0\t" ++ ((match (encdec_compressed_backwards (0x4501#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_285#0\t" ++ ((match (encdec_backwards (0x00a03533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_285#1\t" ++ ((match (encdec_backwards (0xf00007d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_285#2\t" ++ ((match (encdec_backwards (0xa0f525d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_285#3\t" ++ ((match (encdec_backwards (0x0015c593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_285#4\t" ++ ((match (encdec_compressed_backwards (0x8d4d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_309#0\t" ++ ((match (encdec_backwards (0xf20007d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_309#1\t" ++ ((match (encdec_backwards (0xa2f52553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_309#3\t" ++ ((match (encdec_backwards (0xa0f5a5d3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_313#0\t" ++ ((match (encdec_backwards (0x00b035b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_337#3\t" ++ ((match (encdec_backwards (0x40b57533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_397#0\t" ++ ((match (encdec_compressed_backwards (0x8d2d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_465#1\t" ++ ((match (encdec_backwards (0xa0f52553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_537#1\t" ++ ((match (encdec_backwards (0xa0f51553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_541#0\t" ++ ((match (encdec_backwards (0x00a5a533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_553#1\t" ++ ((match (encdec_backwards (0xa0a79553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_561#1\t" ++ ((match (encdec_backwards (0xa2a79553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_573#1\t" ++ ((match (encdec_backwards (0xa0f50553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_577#0\t" ++ ((match (encdec_backwards (0x00b52533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_589#1\t" ++ ((match (encdec_backwards (0xa0a78553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_597#1\t" ++ ((match (encdec_backwards (0xa2a78553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_633#1\t" ++ ((match (encdec_backwards (0xa2f50553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_669#1\t" ++ ((match (encdec_backwards (0xa2f51553#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_685#0\t" ++ ((match (encdec_backwards (0x00b51533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_709#0\t" ++ ((match (encdec_backwards (0x00b5153b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_721#0\t" ++ ((match (encdec_backwards (0x40b55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("c__op_745#0\t" ++ ((match (encdec_backwards (0x00b5553b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
