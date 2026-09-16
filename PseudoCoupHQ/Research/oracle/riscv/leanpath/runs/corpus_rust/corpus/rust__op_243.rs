// probe 243 -- binary ^
#[no_mangle]
pub fn op_243(a: bool, b: f32) -> <bool as core::ops::BitXor<f32>>::Output {
    a ^ b
}
