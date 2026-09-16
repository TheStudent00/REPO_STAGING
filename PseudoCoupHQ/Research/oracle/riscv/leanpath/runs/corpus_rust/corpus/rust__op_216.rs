// probe 216 -- binary ^
#[no_mangle]
pub fn op_216(a: i64, b: i32) -> <i64 as core::ops::BitXor<i32>>::Output {
    a ^ b
}
