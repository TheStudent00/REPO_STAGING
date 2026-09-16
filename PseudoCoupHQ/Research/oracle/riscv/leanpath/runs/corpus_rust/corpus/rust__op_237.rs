// probe 237 -- binary ^
#[no_mangle]
pub fn op_237(a: f64, b: f32) -> <f64 as core::ops::BitXor<f32>>::Output {
    a ^ b
}
