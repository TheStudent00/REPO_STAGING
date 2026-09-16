// probe 233 -- binary ^
#[no_mangle]
pub fn op_233(a: f32, b: bool) -> <f32 as core::ops::BitXor<bool>>::Output {
    a ^ b
}
