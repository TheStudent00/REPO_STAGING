// probe 174 -- binary |
#[no_mangle]
pub fn emu_or_gpr_gpr_32__primitive__rust(a: i32, b: i32) -> <i32 as core::ops::BitOr<i32>>::Output {
    a | b
}
