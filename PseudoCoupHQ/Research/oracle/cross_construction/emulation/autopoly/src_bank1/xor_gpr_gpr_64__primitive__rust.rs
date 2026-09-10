// probe 217 -- binary ^
#[no_mangle]
pub fn emu_xor_gpr_gpr_64__primitive__rust(a: i64, b: i64) -> <i64 as core::ops::BitXor<i64>>::Output {
    a ^ b
}
