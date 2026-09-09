// probe 511 -- binary >>
#[no_mangle]
pub fn emu_shr_cl_gpr_64__primitive__rust(a: u64, b: i64) -> <u64 as core::ops::Shr<i64>>::Output {
    a >> b
}
