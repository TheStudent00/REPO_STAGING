// probe 225 -- binary ^
#[no_mangle]
pub fn op_225(a: u64, b: f32) -> <u64 as core::ops::BitXor<f32>>::Output {
    a ^ b
}
