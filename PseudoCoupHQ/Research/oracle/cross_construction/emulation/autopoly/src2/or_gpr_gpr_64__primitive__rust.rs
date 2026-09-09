// probe 181 -- binary |
#[no_mangle]
pub fn emu_or_gpr_gpr_64__primitive__rust(a: i64, b: i64) -> <i64 as core::ops::BitOr<i64>>::Output {
    a | b
}
