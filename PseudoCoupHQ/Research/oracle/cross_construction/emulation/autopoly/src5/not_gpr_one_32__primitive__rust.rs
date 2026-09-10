// probe 12 -- unary !
#[no_mangle]
pub fn emu_not_gpr_one_32__primitive__rust(a: i32) -> <i32 as core::ops::Not>::Output {
    !a
}
