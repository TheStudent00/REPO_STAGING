// probe 223 -- binary ^
#[no_mangle]
pub fn op_223(a: u64, b: i64) -> <u64 as core::ops::BitXor<i64>>::Output {
    a ^ b
}
