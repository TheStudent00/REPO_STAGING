// probe 228 -- binary ^
#[no_mangle]
pub fn op_228(a: f32, b: i32) -> <f32 as core::ops::BitXor<i32>>::Output {
    a ^ b
}
