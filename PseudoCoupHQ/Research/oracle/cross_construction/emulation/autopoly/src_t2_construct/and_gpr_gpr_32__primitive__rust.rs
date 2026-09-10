// probe 138 -- binary &
#[no_mangle]
pub fn emu_and_gpr_gpr_32__primitive__rust(a: i32, b: i32) -> <i32 as core::ops::BitAnd<i32>>::Output {
    a & b
}
