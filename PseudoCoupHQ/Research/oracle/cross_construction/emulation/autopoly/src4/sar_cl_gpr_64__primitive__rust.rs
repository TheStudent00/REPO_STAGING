// probe 505 -- binary >>
#[no_mangle]
pub fn emu_sar_cl_gpr_64__primitive__rust(a: i64, b: i64) -> <i64 as core::ops::Shr<i64>>::Output {
    a >> b
}
