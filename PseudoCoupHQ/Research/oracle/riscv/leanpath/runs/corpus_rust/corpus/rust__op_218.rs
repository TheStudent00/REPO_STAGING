// probe 218 -- binary ^
#[no_mangle]
pub fn op_218(a: i64, b: u64) -> <i64 as core::ops::BitXor<u64>>::Output {
    a ^ b
}
