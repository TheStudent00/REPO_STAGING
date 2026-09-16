// probe 231 -- binary ^
#[no_mangle]
pub fn op_231(a: f32, b: f32) -> <f32 as core::ops::BitXor<f32>>::Output {
    a ^ b
}
