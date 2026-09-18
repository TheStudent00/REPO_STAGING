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

#eval IO.println ("arch_au_237_c_postdec_f64#0\t" ++ ((match (encdec_compressed_backwards (0x8082#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_198_c_sizeof_i64#0\t" ++ ((match (encdec_compressed_backwards (0x4521#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_348_c_bor_i64_i64#0\t" ++ ((match (encdec_compressed_backwards (0x8d4d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_364_c_bxor_i64_i64#0\t" ++ ((match (encdec_compressed_backwards (0x8d2d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_380_c_band_i64_i64#0\t" ++ ((match (encdec_compressed_backwards (0x8d6d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_316_c_lor_i64_i64#1\t" ++ ((match (encdec_backwards (0x00a03533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_332_c_land_i64_i64#1\t" ++ ((match (encdec_backwards (0x00b035b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_244_c_add_i64_i64#0\t" ++ ((match (encdec_compressed_backwards (0x952e#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_260_c_sub_i64_i64#0\t" ++ ((match (encdec_compressed_backwards (0x8d0d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_396_c_eq_i64_i64#1\t" ++ ((match (encdec_backwards (0x00153513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_192_c_preinc_bool#0\t" ++ ((match (encdec_compressed_backwards (0x4505#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_285_c_div_i64_u64#0\t" ++ ((match (encdec_backwards (0x02b55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_301_c_rem_i64_u64#0\t" ++ ((match (encdec_backwards (0x02b57533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_196_c_predec_bool#0\t" ++ ((match (encdec_backwards (0x00154513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_179_c_neg_i64#0\t" ++ ((match (encdec_backwards (0x40a00533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_197_c_sizeof_i32#0\t" ++ ((match (encdec_compressed_backwards (0x4511#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_190_c_preinc_i64#0\t" ++ ((match (encdec_compressed_backwards (0x0505#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_194_c_predec_i64#0\t" ++ ((match (encdec_compressed_backwards (0x157d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_273_c_mul_i64_bool#0\t" ++ ((match (encdec_backwards (0x0eb55533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_276_c_mul_bool_i64#0\t" ++ ((match (encdec_backwards (0x0ea5d533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_302_c_rem_i64_bool#0\t" ++ ((match (encdec_compressed_backwards (0x4501#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_178_c_neg_i32#0\t" ++ ((match (encdec_backwards (0x40a0053b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_239_c_add_i32_i32#0\t" ++ ((match (encdec_compressed_backwards (0x9d2d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_255_c_sub_i32_i32#0\t" ++ ((match (encdec_compressed_backwards (0x9d0d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_271_c_mul_i32_i32#0\t" ++ ((match (encdec_backwards (0x02a5853b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_410_go_pos_i64#0\t" ++ ((match (encdec_backwards (0x00008067#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_189_c_preinc_i32#0\t" ++ ((match (encdec_compressed_backwards (0x2505#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_193_c_predec_i32#0\t" ++ ((match (encdec_compressed_backwards (0x357d#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_279_c_div_i32_i32#0\t" ++ ((match (encdec_backwards (0x02b5453b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_280_c_div_i32_i64#0\t" ++ ((match (encdec_backwards (0x02b54533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_295_c_rem_i32_i32#0\t" ++ ((match (encdec_backwards (0x02b5653b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_296_c_rem_i32_i64#0\t" ++ ((match (encdec_backwards (0x02b56533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_419_go_cmpl_i64#0\t" ++ ((match (encdec_backwards (0xfff54513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_426_go_mul_i64_i64#0\t" ++ ((match (encdec_backwards (0x02b50533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_439_go_shl_i64_u64#0\t" ++ ((match (encdec_backwards (0x00b512b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_439_go_shl_i64_u64#1\t" ++ ((match (encdec_backwards (0x0405b313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_439_go_shl_i64_u64#2\t" ++ ((match (encdec_backwards (0x40600333#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_439_go_shl_i64_u64#3\t" ++ ((match (encdec_backwards (0x0062f533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_456_go_andnot_i64_i64#0\t" ++ ((match (encdec_backwards (0xfff5cf93#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_456_go_andnot_i64_i64#1\t" ++ ((match (encdec_backwards (0x01f57533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_471_go_eq_i64_i64#0\t" ++ ((match (encdec_backwards (0x40b502b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_471_go_eq_i64_i64#1\t" ++ ((match (encdec_backwards (0x0012b513#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_475_go_ne_i64_i64#1\t" ++ ((match (encdec_backwards (0x00503533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_425_go_mul_i32_i32#0\t" ++ ((match (encdec_backwards (0x02b5053b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_428_go_div_i32_i32#0\t" ++ ((match (encdec_backwards (0x010db303#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_428_go_div_i32_i32#1\t" ++ ((match (encdec_backwards (0x00236a63#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_428_go_div_i32_i32#2\t" ++ ((match (encdec_compressed_backwards (0xc42a#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_428_go_div_i32_i32#3\t" ++ ((match (encdec_compressed_backwards (0xc62e#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_428_go_div_i32_i32#4\t" ++ ((match (encdec_backwards (0x864fe2ef#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_428_go_div_i32_i32#5\t" ++ ((match (encdec_compressed_backwards (0x4522#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_428_go_div_i32_i32#6\t" ++ ((match (encdec_compressed_backwards (0x45b2#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_428_go_div_i32_i32#7\t" ++ ((match (encdec_backwards (0xfedff06f#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_428_go_div_i32_i32#8\t" ++ ((match (encdec_backwards (0xfe113c23#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_428_go_div_i32_i32#9\t" ++ ((match (encdec_compressed_backwards (0x1161#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_428_go_div_i32_i32#10\t" ++ ((match (encdec_compressed_backwards (0xe006#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_428_go_div_i32_i32#11\t" ++ ((match (encdec_backwards (0x0005829b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_428_go_div_i32_i32#12\t" ++ ((match (encdec_backwards (0x00028863#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_428_go_div_i32_i32#14\t" ++ ((match (encdec_compressed_backwards (0x6082#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_428_go_div_i32_i32#15\t" ++ ((match (encdec_compressed_backwards (0x0121#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_428_go_div_i32_i32#17\t" ++ ((match (encdec_backwards (0x984d40ef#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_428_go_div_i32_i32#18\t" ++ ((match (encdec_compressed_backwards (0x0001#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_429_go_div_i64_i64#2\t" ++ ((match (encdec_compressed_backwards (0xe42a#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_429_go_div_i64_i64#3\t" ++ ((match (encdec_compressed_backwards (0xe82e#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_429_go_div_i64_i64#5\t" ++ ((match (encdec_compressed_backwards (0x6522#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_429_go_div_i64_i64#6\t" ++ ((match (encdec_compressed_backwards (0x65c2#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_429_go_div_i64_i64#11\t" ++ ((match (encdec_backwards (0x00058863#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_429_go_div_i64_i64#16\t" ++ ((match (encdec_backwards (0x928d40ef#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_434_go_shl_i32_i32#12\t" ++ ((match (encdec_backwards (0x0202c263#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_434_go_shl_i32_i32#14\t" ++ ((match (encdec_backwards (0x02059313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_434_go_shl_i32_i32#15\t" ++ ((match (encdec_backwards (0x02035313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_434_go_shl_i32_i32#16\t" ++ ((match (encdec_backwards (0x04033313#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_435_go_shl_i32_i64#11\t" ++ ((match (encdec_backwards (0x0005ce63#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_435_go_shl_i32_i64#19\t" ++ ((match (encdec_backwards (0x934d40ef#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_437_go_shl_i64_i32#3\t" ++ ((match (encdec_compressed_backwards (0xc82e#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_437_go_shl_i64_i32#6\t" ++ ((match (encdec_compressed_backwards (0x45c2#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_437_go_shl_i64_i32#22\t" ++ ((match (encdec_backwards (0x8c8d40ef#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_438_go_shl_i64_i64#19\t" ++ ((match (encdec_backwards (0x8d4d40ef#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_443_go_shr_i32_i32#12\t" ++ ((match (encdec_backwards (0x0202c163#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_443_go_shr_i32_i32#13\t" ++ ((match (encdec_backwards (0x02059293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_443_go_shr_i32_i32#14\t" ++ ((match (encdec_backwards (0x0202d293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_443_go_shr_i32_i32#15\t" ++ ((match (encdec_backwards (0x0202b293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_443_go_shr_i32_i32#16\t" ++ ((match (encdec_compressed_backwards (0x12fd#16)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_443_go_shr_i32_i32#17\t" ++ ((match (encdec_backwards (0x0055e2b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_443_go_shr_i32_i32#18\t" ++ ((match (encdec_backwards (0x4055553b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_443_go_shr_i32_i32#22\t" ++ ((match (encdec_backwards (0x92ad40ef#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_444_go_shr_i32_i64#11\t" ++ ((match (encdec_backwards (0x0005cd63#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_444_go_shr_i32_i64#12\t" ++ ((match (encdec_backwards (0x0205b293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_444_go_shr_i32_i64#19\t" ++ ((match (encdec_backwards (0x936d40ef#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_446_go_shr_i64_i32#15\t" ++ ((match (encdec_backwards (0x0402b293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_446_go_shr_i64_i32#18\t" ++ ((match (encdec_backwards (0x40555533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_446_go_shr_i64_i32#22\t" ++ ((match (encdec_backwards (0x8cad40ef#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_447_go_shr_i64_i64#12\t" ++ ((match (encdec_backwards (0x0405b293#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_447_go_shr_i64_i64#19\t" ++ ((match (encdec_backwards (0x8d6d40ef#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_449_go_shr_u64_i32#13\t" ++ ((match (encdec_backwards (0x00b552b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_470_go_eq_i32_i32#0\t" ++ ((match (encdec_backwards (0x0005029b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_470_go_eq_i32_i32#1\t" ++ ((match (encdec_backwards (0x0005831b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_470_go_eq_i32_i32#2\t" ++ ((match (encdec_backwards (0x406282b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_478_go_lt_i32_i32#2\t" ++ ((match (encdec_backwards (0x0062a533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_479_go_lt_i64_i64#0\t" ++ ((match (encdec_backwards (0x00b52533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_480_go_lt_u64_u64#0\t" ++ ((match (encdec_backwards (0x00b53533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_481_go_le_i32_i32#1\t" ++ ((match (encdec_backwards (0x0005031b#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_481_go_le_i32_i32#2\t" ++ ((match (encdec_backwards (0x0062a2b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_482_go_le_i64_i64#0\t" ++ ((match (encdec_backwards (0x00a5a2b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_483_go_le_u64_u64#0\t" ++ ((match (encdec_backwards (0x00a5b2b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_485_go_gt_i64_i64#0\t" ++ ((match (encdec_backwards (0x00a5a533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_486_go_gt_u64_u64#0\t" ++ ((match (encdec_backwards (0x00a5b533#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_488_go_ge_i64_i64#0\t" ++ ((match (encdec_backwards (0x00b522b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
#eval IO.println ("arch_au_489_go_ge_u64_u64#0\t" ++ ((match (encdec_backwards (0x00b532b3#32)) (s0) with | .ok i _ => toString (repr i) | .error _ _ => "ERROR")))
