// probe 498 -- binary >>
#[no_mangle]
pub fn emu_sar_cl_gpr_32__primitive__rust(a: i32, b: i32) -> <i32 as core::ops::Shr<i32>>::Output {
    a >> b
}
