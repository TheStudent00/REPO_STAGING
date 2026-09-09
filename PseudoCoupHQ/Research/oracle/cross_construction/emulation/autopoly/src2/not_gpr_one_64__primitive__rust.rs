// probe 13 -- unary !
#[no_mangle]
pub fn emu_not_gpr_one_64__primitive__rust(a: i64) -> <i64 as core::ops::Not>::Output {
    !a
}
