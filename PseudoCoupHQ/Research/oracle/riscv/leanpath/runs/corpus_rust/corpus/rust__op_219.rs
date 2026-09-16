// probe 219 -- binary ^
#[no_mangle]
pub fn op_219(a: i64, b: f32) -> <i64 as core::ops::BitXor<f32>>::Output {
    a ^ b
}
