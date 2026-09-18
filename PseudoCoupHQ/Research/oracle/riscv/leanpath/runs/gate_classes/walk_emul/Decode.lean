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

#eval IO.println ("emul_au_237_c_postdec_f64#0\t" ++ ((match (encdec_compressed_backwards (0x8082#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_198_c_sizeof_i64#0\t" ++ ((match (encdec_compressed_backwards (0x4521#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_348_c_bor_i64_i64#0\t" ++ ((match (encdec_compressed_backwards (0x8d4d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_364_c_bxor_i64_i64#0\t" ++ ((match (encdec_compressed_backwards (0x8d2d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_380_c_band_i64_i64#0\t" ++ ((match (encdec_compressed_backwards (0x8d6d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_316_c_lor_i64_i64#1\t" ++ ((match (encdec_backwards (0x00a03533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_332_c_land_i64_i64#1\t" ++ ((match (encdec_backwards (0x00b035b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_244_c_add_i64_i64#0\t" ++ ((match (encdec_compressed_backwards (0x952e#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_260_c_sub_i64_i64#0\t" ++ ((match (encdec_compressed_backwards (0x8d0d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_278_c_mul_bool_bool#1\t" ++ ((match (encdec_compressed_backwards (0x8905#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_396_c_eq_i64_i64#1\t" ++ ((match (encdec_backwards (0x00153513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_182_c_pos_i32#0\t" ++ ((match (encdec_compressed_backwards (0x9d71#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_192_c_preinc_bool#0\t" ++ ((match (encdec_compressed_backwards (0x4505#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#0\t" ++ ((match (encdec_compressed_backwards (0xc1a1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#1\t" ++ ((match (encdec_compressed_backwards (0x88aa#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#2\t" ++ ((match (encdec_compressed_backwards (0x4501#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#3\t" ++ ((match (encdec_compressed_backwards (0x4781#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#4\t" ++ ((match (encdec_backwards (0x03f00693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#5\t" ++ ((match (encdec_compressed_backwards (0x587d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#6\t" ++ ((match (encdec_backwards (0x00d8d733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#7\t" ++ ((match (encdec_backwards (0x0007a293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#8\t" ++ ((match (encdec_backwards (0x28d01333#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#9\t" ++ ((match (encdec_compressed_backwards (0x16fd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#10\t" ++ ((match (encdec_compressed_backwards (0x8b05#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#11\t" ++ ((match (encdec_backwards (0x20e7a733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#12\t" ++ ((match (encdec_backwards (0x00b737b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#13\t" ++ ((match (encdec_backwards (0x4057f7b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#14\t" ++ ((match (encdec_backwards (0x0ef5f633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#15\t" ++ ((match (encdec_backwards (0x0ef372b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#16\t" ++ ((match (encdec_backwards (0x40c707b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#17\t" ++ ((match (encdec_backwards (0x00a2e533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#18\t" ++ ((match (encdec_backwards (0xfd069ae3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_285_c_div_i64_u64#20\t" ++ ((match (encdec_compressed_backwards (0x557d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_301_c_rem_i64_u64#0\t" ++ ((match (encdec_compressed_backwards (0xc59d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_301_c_rem_i64_u64#1\t" ++ ((match (encdec_compressed_backwards (0x4601#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_301_c_rem_i64_u64#4\t" ++ ((match (encdec_backwards (0x00d557b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_301_c_rem_i64_u64#5\t" ++ ((match (encdec_backwards (0x00062713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_301_c_rem_i64_u64#6\t" ++ ((match (encdec_compressed_backwards (0x8b85#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_301_c_rem_i64_u64#7\t" ++ ((match (encdec_backwards (0x20f62633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_301_c_rem_i64_u64#8\t" ++ ((match (encdec_backwards (0x00b637b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_301_c_rem_i64_u64#9\t" ++ ((match (encdec_backwards (0x40e7f733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_301_c_rem_i64_u64#10\t" ++ ((match (encdec_backwards (0x0ee5f733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_301_c_rem_i64_u64#12\t" ++ ((match (encdec_compressed_backwards (0x8e19#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_301_c_rem_i64_u64#13\t" ++ ((match (encdec_backwards (0xff0691e3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_301_c_rem_i64_u64#14\t" ++ ((match (encdec_compressed_backwards (0x8532#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_312_c_lor_i32_i64#0\t" ++ ((match (encdec_compressed_backwards (0x2501#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_315_c_lor_i64_i32#0\t" ++ ((match (encdec_compressed_backwards (0x2581#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_318_c_lor_i64_bool#0\t" ++ ((match (encdec_compressed_backwards (0x8985#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_334_c_land_i64_bool#1\t" ++ ((match (encdec_backwards (0x0ea5d533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_340_c_land_bool_i64#1\t" ++ ((match (encdec_backwards (0x0eb55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_196_c_predec_bool#0\t" ++ ((match (encdec_compressed_backwards (0x4585#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_196_c_predec_bool#1\t" ++ ((match (encdec_backwards (0x40a5f533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_179_c_neg_i64#0\t" ++ ((match (encdec_backwards (0x40a00533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_197_c_sizeof_i32#0\t" ++ ((match (encdec_compressed_backwards (0x4511#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_190_c_preinc_i64#0\t" ++ ((match (encdec_compressed_backwards (0x0505#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_194_c_predec_i64#0\t" ++ ((match (encdec_compressed_backwards (0x157d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_178_c_neg_i32#0\t" ++ ((match (encdec_backwards (0x40a0053b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_255_c_sub_i32_i32#0\t" ++ ((match (encdec_compressed_backwards (0x9d0d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_271_c_mul_i32_i32#0\t" ++ ((match (encdec_compressed_backwards (0x9d4d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_355_c_bor_bool_i32#1\t" ++ ((match (encdec_compressed_backwards (0x9df1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_181_c_neg_bool#1\t" ++ ((match (encdec_compressed_backwards (0x55fd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_181_c_neg_bool#2\t" ++ ((match (encdec_compressed_backwards (0x9181#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#0\t" ++ ((match (encdec_backwards (0x02059613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#1\t" ++ ((match (encdec_compressed_backwards (0x52fd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#2\t" ++ ((match (encdec_compressed_backwards (0xc62d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#4\t" ++ ((match (encdec_compressed_backwards (0x4701#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#5\t" ++ ((match (encdec_backwards (0x0005081b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#6\t" ++ ((match (encdec_backwards (0x0005889b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#7\t" ++ ((match (encdec_backwards (0x41000533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#8\t" ++ ((match (encdec_backwards (0x411005b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#9\t" ++ ((match (encdec_backwards (0x0aa86333#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#10\t" ++ ((match (encdec_backwards (0x0ab8e3b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#11\t" ++ ((match (encdec_backwards (0x03f00593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#12\t" ++ ((match (encdec_backwards (0x00b356b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#13\t" ++ ((match (encdec_backwards (0x00072793#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#14\t" ++ ((match (encdec_backwards (0x28b01533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#15\t" ++ ((match (encdec_compressed_backwards (0x15fd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#16\t" ++ ((match (encdec_compressed_backwards (0x8a85#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#17\t" ++ ((match (encdec_backwards (0x20d726b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#18\t" ++ ((match (encdec_backwards (0x0076b733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#19\t" ++ ((match (encdec_backwards (0x40f77733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#20\t" ++ ((match (encdec_backwards (0x0ee3f7b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#21\t" ++ ((match (encdec_backwards (0x0ee57533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#22\t" ++ ((match (encdec_backwards (0x40f68733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#23\t" ++ ((match (encdec_compressed_backwards (0x8e49#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#24\t" ++ ((match (encdec_backwards (0xfc559be3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#25\t" ++ ((match (encdec_backwards (0x0108c533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#26\t" ++ ((match (encdec_backwards (0x40c005b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#27\t" ++ ((match (encdec_backwards (0x00052513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#28\t" ++ ((match (encdec_backwards (0x0ea5d5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#29\t" ++ ((match (encdec_backwards (0x0ea67533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_279_c_div_i32_i32#33\t" ++ ((match (encdec_backwards (0x0202d513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#0\t" ++ ((match (encdec_compressed_backwards (0xc1bd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#2\t" ++ ((match (encdec_compressed_backwards (0x4681#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#4\t" ++ ((match (encdec_backwards (0x40b007b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#5\t" ++ ((match (encdec_backwards (0x03f00713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#7\t" ++ ((match (encdec_backwards (0x0af5e333#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#8\t" ++ ((match (encdec_backwards (0x0aa862b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#9\t" ++ ((match (encdec_compressed_backwards (0x58fd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#10\t" ++ ((match (encdec_backwards (0x00e2d3b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#11\t" ++ ((match (encdec_backwards (0x0006ae13#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#12\t" ++ ((match (encdec_backwards (0x28e01eb3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#13\t" ++ ((match (encdec_compressed_backwards (0x177d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#14\t" ++ ((match (encdec_backwards (0x0013f793#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#15\t" ++ ((match (encdec_backwards (0x20f6a6b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#16\t" ++ ((match (encdec_backwards (0x0066b7b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#17\t" ++ ((match (encdec_backwards (0x41c7f7b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#18\t" ++ ((match (encdec_backwards (0x0ef37533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#19\t" ++ ((match (encdec_backwards (0x0efef7b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#20\t" ++ ((match (encdec_compressed_backwards (0x8e89#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#21\t" ++ ((match (encdec_compressed_backwards (0x8e5d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#22\t" ++ ((match (encdec_backwards (0xfd171be3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_280_c_div_i32_i64#23\t" ++ ((match (encdec_backwards (0x00b84533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_281_c_div_i32_u64#0\t" ++ ((match (encdec_compressed_backwards (0xc1b1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_281_c_div_i32_u64#1\t" ++ ((match (encdec_compressed_backwards (0x862a#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_281_c_div_i32_u64#4\t" ++ ((match (encdec_backwards (0x0006089b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#0\t" ++ ((match (encdec_backwards (0x02059693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#1\t" ++ ((match (encdec_compressed_backwards (0xca99#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#2\t" ++ ((match (encdec_backwards (0x2bf01613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#3\t" ++ ((match (encdec_backwards (0x00c51a63#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#4\t" ++ ((match (encdec_compressed_backwards (0x577d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#5\t" ++ ((match (encdec_compressed_backwards (0x1702#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#6\t" ++ ((match (encdec_backwards (0x00e69663#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#13\t" ++ ((match (encdec_backwards (0x0005881b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#14\t" ++ ((match (encdec_backwards (0x40a005b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#16\t" ++ ((match (encdec_backwards (0x0ab562b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#17\t" ++ ((match (encdec_backwards (0x410005b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#18\t" ++ ((match (encdec_backwards (0x0ab86333#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#20\t" ++ ((match (encdec_backwards (0x00e2d7b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#21\t" ++ ((match (encdec_backwards (0x0006a393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#22\t" ++ ((match (encdec_backwards (0x28e01e33#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#27\t" ++ ((match (encdec_backwards (0x4077f7b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#28\t" ++ ((match (encdec_backwards (0x0ef375b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#29\t" ++ ((match (encdec_backwards (0x0efe77b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#30\t" ++ ((match (encdec_compressed_backwards (0x8e8d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#32\t" ++ ((match (encdec_backwards (0xfd171ce3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#33\t" ++ ((match (encdec_backwards (0x00a84533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#37\t" ++ ((match (encdec_backwards (0x0ea67633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_283_c_div_i64_i32#38\t" ++ ((match (encdec_compressed_backwards (0x8e4d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_284_c_div_i64_i64#0\t" ++ ((match (encdec_compressed_backwards (0xc991#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_284_c_div_i64_i64#2\t" ++ ((match (encdec_backwards (0x00c51963#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_284_c_div_i64_i64#3\t" ++ ((match (encdec_compressed_backwards (0x56fd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_284_c_div_i64_i64#4\t" ++ ((match (encdec_backwards (0x00d59663#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_284_c_div_i64_i64#11\t" ++ ((match (encdec_backwards (0x40a00833#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_284_c_div_i64_i64#14\t" ++ ((match (encdec_backwards (0x0b056833#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_284_c_div_i64_i64#15\t" ++ ((match (encdec_backwards (0x0af5e2b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_284_c_div_i64_i64#17\t" ++ ((match (encdec_backwards (0x00e853b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_284_c_div_i64_i64#18\t" ++ ((match (encdec_backwards (0x0006a313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_284_c_div_i64_i64#23\t" ++ ((match (encdec_backwards (0x0056b7b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_284_c_div_i64_i64#24\t" ++ ((match (encdec_backwards (0x4067f7b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_284_c_div_i64_i64#25\t" ++ ((match (encdec_backwards (0x0ef2f333#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_284_c_div_i64_i64#27\t" ++ ((match (encdec_backwards (0x406686b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_284_c_div_i64_i64#29\t" ++ ((match (encdec_backwards (0xfd171ae3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_287_c_div_u64_i32#1\t" ++ ((match (encdec_compressed_backwards (0xc2a9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_287_c_div_u64_i32#5\t" ++ ((match (encdec_backwards (0x0005829b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_287_c_div_u64_i32#9\t" ++ ((match (encdec_backwards (0x0007a613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_287_c_div_u64_i32#10\t" ++ ((match (encdec_backwards (0x28d015b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_287_c_div_u64_i32#14\t" ++ ((match (encdec_backwards (0x005737b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_287_c_div_u64_i32#15\t" ++ ((match (encdec_backwards (0x40c7f633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_287_c_div_u64_i32#16\t" ++ ((match (encdec_backwards (0x0ec2f7b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_287_c_div_u64_i32#17\t" ++ ((match (encdec_backwards (0x0ec5f5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_287_c_div_u64_i32#18\t" ++ ((match (encdec_backwards (0x40f707b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_287_c_div_u64_i32#20\t" ++ ((match (encdec_backwards (0xfd069be3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#2\t" ++ ((match (encdec_compressed_backwards (0xce39#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#5\t" ++ ((match (encdec_backwards (0x00157293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#7\t" ++ ((match (encdec_backwards (0x41100733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#8\t" ++ ((match (encdec_backwards (0x0ae8e333#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#9\t" ++ ((match (encdec_backwards (0x03f00793#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#10\t" ++ ((match (encdec_backwards (0x00161593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#11\t" ++ ((match (encdec_backwards (0x00f2d533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#12\t" ++ ((match (encdec_backwards (0x00062613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#13\t" ++ ((match (encdec_backwards (0x28f01733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#14\t" ++ ((match (encdec_compressed_backwards (0x17fd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#16\t" ++ ((match (encdec_backwards (0x006535b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#17\t" ++ ((match (encdec_backwards (0x40c5f5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#18\t" ++ ((match (encdec_backwards (0x0eb37633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#19\t" ++ ((match (encdec_backwards (0x0eb775b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#20\t" ++ ((match (encdec_backwards (0x40c50633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#21\t" ++ ((match (encdec_compressed_backwards (0x8ecd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#22\t" ++ ((match (encdec_backwards (0xfd079be3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#23\t" ++ ((match (encdec_backwards (0x40d00533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#24\t" ++ ((match (encdec_backwards (0x0008a593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#25\t" ++ ((match (encdec_backwards (0x0eb6f633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#27\t" ++ ((match (encdec_compressed_backwards (0x8d51#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_291_c_div_bool_i32#30\t" ++ ((match (encdec_backwards (0x02085513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_292_c_div_bool_i64#0\t" ++ ((match (encdec_compressed_backwards (0xcdb9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_292_c_div_bool_i64#3\t" ++ ((match (encdec_backwards (0x00157893#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_292_c_div_bool_i64#4\t" ++ ((match (encdec_backwards (0x40b00733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_292_c_div_bool_i64#6\t" ++ ((match (encdec_backwards (0x0ae5e2b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_292_c_div_bool_i64#8\t" ++ ((match (encdec_backwards (0x00179313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_292_c_div_bool_i64#10\t" ++ ((match (encdec_backwards (0x0007a393#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_292_c_div_bool_i64#11\t" ++ ((match (encdec_backwards (0x28d01e33#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_292_c_div_bool_i64#13\t" ++ ((match (encdec_backwards (0x00e36733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_292_c_div_bool_i64#16\t" ++ ((match (encdec_backwards (0x0ef2f533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_292_c_div_bool_i64#17\t" ++ ((match (encdec_backwards (0x0efe7333#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_292_c_div_bool_i64#18\t" ++ ((match (encdec_backwards (0x40a707b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_292_c_div_bool_i64#19\t" ++ ((match (encdec_backwards (0x00c36633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_292_c_div_bool_i64#20\t" ++ ((match (encdec_backwards (0xfd0699e3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_292_c_div_bool_i64#21\t" ++ ((match (encdec_backwards (0x40c00533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_292_c_div_bool_i64#22\t" ++ ((match (encdec_backwards (0x0005a593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_292_c_div_bool_i64#23\t" ++ ((match (encdec_backwards (0x0eb67633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_293_c_div_bool_u64#0\t" ++ ((match (encdec_compressed_backwards (0xc1b9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_293_c_div_bool_u64#4\t" ++ ((match (encdec_backwards (0x00167893#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_293_c_div_bool_u64#7\t" ++ ((match (encdec_backwards (0x00179293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_293_c_div_bool_u64#8\t" ++ ((match (encdec_backwards (0x00d8d633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_293_c_div_bool_u64#9\t" ++ ((match (encdec_backwards (0x0007a313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_293_c_div_bool_u64#10\t" ++ ((match (encdec_backwards (0x28d013b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_293_c_div_bool_u64#12\t" ++ ((match (encdec_backwards (0x00c2e633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_293_c_div_bool_u64#15\t" ++ ((match (encdec_backwards (0x0ef5f733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_293_c_div_bool_u64#16\t" ++ ((match (encdec_backwards (0x0ef3f2b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_293_c_div_bool_u64#17\t" ++ ((match (encdec_backwards (0x40e607b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#1\t" ++ ((match (encdec_compressed_backwards (0xce21#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#2\t" ++ ((match (encdec_compressed_backwards (0x4581#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#4\t" ++ ((match (encdec_backwards (0x42065713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#5\t" ++ ((match (encdec_backwards (0x03f00613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#6\t" ++ ((match (encdec_backwards (0x410006b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#7\t" ++ ((match (encdec_backwards (0x40e007b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#8\t" ++ ((match (encdec_backwards (0x0ad866b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#9\t" ++ ((match (encdec_backwards (0x0af76733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#11\t" ++ ((match (encdec_backwards (0x00c6d533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#12\t" ++ ((match (encdec_backwards (0x0005a793#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#14\t" ++ ((match (encdec_backwards (0x20a5a533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#15\t" ++ ((match (encdec_backwards (0x00e535b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#16\t" ++ ((match (encdec_backwards (0x40f5f5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#18\t" ++ ((match (encdec_compressed_backwards (0x167d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#19\t" ++ ((match (encdec_backwards (0x40b505b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#20\t" ++ ((match (encdec_backwards (0xff1610e3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#21\t" ++ ((match (encdec_backwards (0x40b00533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#22\t" ++ ((match (encdec_backwards (0x00082613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#24\t" ++ ((match (encdec_backwards (0x0ec55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#26\t" ++ ((match (encdec_compressed_backwards (0x1502#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_295_c_rem_i32_i32#27\t" ++ ((match (encdec_compressed_backwards (0x9101#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_296_c_rem_i32_i64#1\t" ++ ((match (encdec_compressed_backwards (0xc5b9#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_296_c_rem_i32_i64#3\t" ++ ((match (encdec_backwards (0x40a00733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_296_c_rem_i32_i64#6\t" ++ ((match (encdec_backwards (0x0ae568b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_296_c_rem_i32_i64#7\t" ++ ((match (encdec_backwards (0x0af5e5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_296_c_rem_i32_i64#9\t" ++ ((match (encdec_backwards (0x00d8d7b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_297_c_rem_i32_u64#0\t" ++ ((match (encdec_backwards (0x0005061b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_297_c_rem_i32_u64#5\t" ++ ((match (encdec_backwards (0x00d657b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_297_c_rem_i32_u64#6\t" ++ ((match (encdec_backwards (0x00052713#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_297_c_rem_i32_u64#8\t" ++ ((match (encdec_backwards (0x20f52533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_297_c_rem_i32_u64#9\t" ++ ((match (encdec_backwards (0x00b537b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_297_c_rem_i32_u64#13\t" ++ ((match (encdec_compressed_backwards (0x8d19#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_299_c_rem_i64_i32#1\t" ++ ((match (encdec_compressed_backwards (0xc23d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_299_c_rem_i64_i32#2\t" ++ ((match (encdec_backwards (0x2bf01693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_299_c_rem_i64_i32#3\t" ++ ((match (encdec_backwards (0x00d51863#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_299_c_rem_i64_i32#5\t" ++ ((match (encdec_compressed_backwards (0x1682#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_299_c_rem_i64_i32#6\t" ++ ((match (encdec_backwards (0x00d61463#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_299_c_rem_i64_i32#10\t" ++ ((match (encdec_backwards (0x0005871b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_299_c_rem_i64_i32#11\t" ++ ((match (encdec_backwards (0x40a006b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_299_c_rem_i64_i32#13\t" ++ ((match (encdec_backwards (0x0ad568b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_299_c_rem_i64_i32#17\t" ++ ((match (encdec_backwards (0x00b8d7b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_299_c_rem_i64_i32#18\t" ++ ((match (encdec_backwards (0x00062693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_299_c_rem_i64_i32#21\t" ++ ((match (encdec_backwards (0x00e637b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_299_c_rem_i64_i32#22\t" ++ ((match (encdec_backwards (0x40d7f6b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_299_c_rem_i64_i32#23\t" ++ ((match (encdec_backwards (0x0ed776b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_299_c_rem_i64_i32#25\t" ++ ((match (encdec_compressed_backwards (0x8e15#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_299_c_rem_i64_i32#26\t" ++ ((match (encdec_backwards (0xff0591e3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_300_c_rem_i64_i64#0\t" ++ ((match (encdec_compressed_backwards (0xc1a5#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_300_c_rem_i64_i64#2\t" ++ ((match (encdec_backwards (0x00c51763#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_300_c_rem_i64_i64#3\t" ++ ((match (encdec_compressed_backwards (0x567d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_300_c_rem_i64_i64#4\t" ++ ((match (encdec_backwards (0x00c59463#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_303_c_rem_u64_i32#1\t" ++ ((match (encdec_compressed_backwards (0xca05#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_307_c_rem_bool_i32#2\t" ++ ((match (encdec_compressed_backwards (0xce1d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_307_c_rem_bool_i32#4\t" ++ ((match (encdec_backwards (0x42065693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_307_c_rem_bool_i32#6\t" ++ ((match (encdec_backwards (0x40d00733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_307_c_rem_bool_i32#7\t" ++ ((match (encdec_backwards (0x0ae6e6b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_307_c_rem_bool_i32#9\t" ++ ((match (encdec_backwards (0x00159793#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_307_c_rem_bool_i32#10\t" ++ ((match (encdec_backwards (0x00c55733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_307_c_rem_bool_i32#12\t" ++ ((match (encdec_compressed_backwards (0x8f5d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_307_c_rem_bool_i32#13\t" ++ ((match (encdec_backwards (0x00d737b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_307_c_rem_bool_i32#14\t" ++ ((match (encdec_backwards (0x40b7f5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_307_c_rem_bool_i32#15\t" ++ ((match (encdec_backwards (0x0eb6f5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_307_c_rem_bool_i32#17\t" ++ ((match (encdec_backwards (0x40b705b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_307_c_rem_bool_i32#18\t" ++ ((match (encdec_backwards (0xff0610e3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_307_c_rem_bool_i32#19\t" ++ ((match (encdec_backwards (0x0805853b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_308_c_rem_bool_i64#0\t" ++ ((match (encdec_backwards (0x00157613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_308_c_rem_bool_i64#1\t" ++ ((match (encdec_compressed_backwards (0xcd85#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_308_c_rem_bool_i64#5\t" ++ ((match (encdec_backwards (0x0ae5e5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_308_c_rem_bool_i64#7\t" ++ ((match (encdec_backwards (0x00151793#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_308_c_rem_bool_i64#8\t" ++ ((match (encdec_backwards (0x00d65733#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_308_c_rem_bool_i64#12\t" ++ ((match (encdec_backwards (0x40a7f533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_308_c_rem_bool_i64#13\t" ++ ((match (encdec_backwards (0x0ea5f533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_308_c_rem_bool_i64#15\t" ++ ((match (encdec_backwards (0x40a70533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_308_c_rem_bool_i64#16\t" ++ ((match (encdec_backwards (0xff0690e3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_309_c_rem_bool_u64#1\t" ++ ((match (encdec_compressed_backwards (0xc985#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_419_go_cmpl_i64#0\t" ++ ((match (encdec_compressed_backwards (0x9d75#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_439_go_shl_i64_u64#0\t" ++ ((match (encdec_backwards (0x00b51533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_439_go_shl_i64_u64#1\t" ++ ((match (encdec_backwards (0x0405b593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_456_go_andnot_i64_i64#0\t" ++ ((match (encdec_backwards (0x40b57533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_434_go_shl_i32_i32#0\t" ++ ((match (encdec_backwards (0x0065d61b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_434_go_shl_i32_i32#2\t" ++ ((match (encdec_compressed_backwards (0x061a#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_434_go_shl_i32_i32#4\t" ++ ((match (encdec_backwards (0x0ec57533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_443_go_shr_i32_i32#0\t" ++ ((match (encdec_backwards (0x0055d61b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_443_go_shr_i32_i32#1\t" ++ ((match (encdec_compressed_backwards (0x89fd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_443_go_shr_i32_i32#2\t" ++ ((match (encdec_compressed_backwards (0x46fd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_443_go_shr_i32_i32#3\t" ++ ((match (encdec_compressed_backwards (0x0616#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_443_go_shr_i32_i32#4\t" ++ ((match (encdec_backwards (0x0ec6d633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_443_go_shr_i32_i32#5\t" ++ ((match (encdec_backwards (0x080506bb#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_443_go_shr_i32_i32#6\t" ++ ((match (encdec_backwards (0x41f5551b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_443_go_shr_i32_i32#7\t" ++ ((match (encdec_compressed_backwards (0x8dd1#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_443_go_shr_i32_i32#8\t" ++ ((match (encdec_backwards (0x00b6d633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_443_go_shr_i32_i32#9\t" ++ ((match (encdec_backwards (0x01f5c593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_443_go_shr_i32_i32#11\t" ++ ((match (encdec_compressed_backwards (0x1506#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_444_go_shr_i32_i64#0\t" ++ ((match (encdec_compressed_backwards (0x467d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_444_go_shr_i32_i64#1\t" ++ ((match (encdec_backwards (0x0ac5d5b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_444_go_shr_i32_i64#2\t" ++ ((match (encdec_backwards (0x0805063b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_444_go_shr_i32_i64#4\t" ++ ((match (encdec_backwards (0x00b65633#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_446_go_shr_i64_i32#1\t" ++ ((match (encdec_backwards (0x03f5f593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_446_go_shr_i64_i32#5\t" ++ ((match (encdec_backwards (0x43f55693#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_446_go_shr_i64_i32#7\t" ++ ((match (encdec_backwards (0x00b55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_446_go_shr_i64_i32#8\t" ++ ((match (encdec_backwards (0x03f5c593#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_446_go_shr_i64_i32#9\t" ++ ((match (encdec_backwards (0x00b695b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_446_go_shr_i64_i32#10\t" ++ ((match (encdec_compressed_backwards (0x0586#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_447_go_shr_i64_i64#2\t" ++ ((match (encdec_backwards (0x43f55613#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_447_go_shr_i64_i64#5\t" ++ ((match (encdec_backwards (0x00b615b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_478_go_lt_i32_i32#1\t" ++ ((match (encdec_compressed_backwards (0x1582#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_478_go_lt_i32_i32#2\t" ++ ((match (encdec_backwards (0x00b52533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_480_go_lt_u64_u64#0\t" ++ ((match (encdec_backwards (0x00b53533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_481_go_le_i32_i32#2\t" ++ ((match (encdec_backwards (0x00a5a533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_481_go_le_i32_i32#3\t" ++ ((match (encdec_backwards (0x00154513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("emul_au_483_go_le_u64_u64#0\t" ++ ((match (encdec_backwards (0x00a5b533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
