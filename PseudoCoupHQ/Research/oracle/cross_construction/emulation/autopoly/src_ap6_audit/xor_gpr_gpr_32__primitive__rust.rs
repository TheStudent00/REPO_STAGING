// probe 210 -- binary ^
#[no_mangle]
pub fn emu_xor_gpr_gpr_32__primitive__rust(a: i32, b: i32) -> <i32 as core::ops::BitXor<i32>>::Output {
    a ^ b
}
