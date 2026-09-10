// probe 577 -- binary -
#[no_mangle]
pub fn emu_sub_gpr_gpr_64__primitive__rust(a: i64, b: i64) -> <i64 as core::ops::Sub<i64>>::Output {
    a - b
}
