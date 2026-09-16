// probe 230 -- binary ^
#[no_mangle]
pub fn op_230(a: f32, b: u64) -> <f32 as core::ops::BitXor<u64>>::Output {
    a ^ b
}
