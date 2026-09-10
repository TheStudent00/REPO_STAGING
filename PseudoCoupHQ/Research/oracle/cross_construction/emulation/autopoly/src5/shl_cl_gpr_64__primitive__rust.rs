// probe 469 -- binary <<
#[no_mangle]
pub fn emu_shl_cl_gpr_64__primitive__rust(a: i64, b: i64) -> <i64 as core::ops::Shl<i64>>::Output {
    a << b
}
