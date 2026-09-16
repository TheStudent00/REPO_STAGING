// probe 217 -- binary ^
#[no_mangle]
pub fn op_217(a: i64, b: i64) -> <i64 as core::ops::BitXor<i64>>::Output {
    a ^ b
}
