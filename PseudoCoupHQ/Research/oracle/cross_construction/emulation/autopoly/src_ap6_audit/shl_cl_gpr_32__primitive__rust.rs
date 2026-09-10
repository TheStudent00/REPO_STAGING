// probe 463 -- binary <<
#[no_mangle]
pub fn emu_shl_cl_gpr_32__primitive__rust(a: i32, b: i64) -> <i32 as core::ops::Shl<i64>>::Output {
    a << b
}
