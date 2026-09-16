// probe 212 -- binary ^
#[no_mangle]
pub fn op_212(a: i32, b: u64) -> <i32 as core::ops::BitXor<u64>>::Output {
    a ^ b
}
