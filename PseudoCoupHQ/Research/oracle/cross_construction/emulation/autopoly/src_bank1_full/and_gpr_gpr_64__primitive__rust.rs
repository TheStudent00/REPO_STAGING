// probe 145 -- binary &
#[no_mangle]
pub fn emu_and_gpr_gpr_64__primitive__rust(a: i64, b: i64) -> <i64 as core::ops::BitAnd<i64>>::Output {
    a & b
}
