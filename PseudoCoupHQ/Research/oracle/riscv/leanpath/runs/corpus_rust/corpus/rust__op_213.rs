// probe 213 -- binary ^
#[no_mangle]
pub fn op_213(a: i32, b: f32) -> <i32 as core::ops::BitXor<f32>>::Output {
    a ^ b
}
