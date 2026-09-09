// probe 499 -- binary >>
#[no_mangle]
pub fn emu_sar_cl_gpr_32__primitive__rust(a: i32, b: i64) -> <i32 as core::ops::Shr<i64>>::Output {
    a >> b
}
