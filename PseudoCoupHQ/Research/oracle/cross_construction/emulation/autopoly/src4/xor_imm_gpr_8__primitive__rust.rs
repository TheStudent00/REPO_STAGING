// probe 17 -- unary !
#[no_mangle]
pub fn emu_xor_imm_gpr_8__primitive__rust(a: bool) -> <bool as core::ops::Not>::Output {
    !a
}
