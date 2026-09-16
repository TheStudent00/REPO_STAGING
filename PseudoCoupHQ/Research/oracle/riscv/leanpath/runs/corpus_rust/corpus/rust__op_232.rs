// probe 232 -- binary ^
#[no_mangle]
pub fn op_232(a: f32, b: f64) -> <f32 as core::ops::BitXor<f64>>::Output {
    a ^ b
}
