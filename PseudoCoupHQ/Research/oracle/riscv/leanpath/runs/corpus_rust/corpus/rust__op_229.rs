// probe 229 -- binary ^
#[no_mangle]
pub fn op_229(a: f32, b: i64) -> <f32 as core::ops::BitXor<i64>>::Output {
    a ^ b
}
