// probe 606 -- binary *
#[no_mangle]
pub fn emu_imul_gpr_gpr_32__primitive__rust(a: i32, b: i32) -> <i32 as core::ops::Mul<i32>>::Output {
    a * b
}
