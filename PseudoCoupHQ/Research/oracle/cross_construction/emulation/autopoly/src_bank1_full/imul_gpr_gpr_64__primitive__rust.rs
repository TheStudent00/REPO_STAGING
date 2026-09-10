// probe 613 -- binary *
#[no_mangle]
pub fn emu_imul_gpr_gpr_64__primitive__rust(a: i64, b: i64) -> <i64 as core::ops::Mul<i64>>::Output {
    a * b
}
