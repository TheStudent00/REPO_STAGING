// probe 222 -- binary ^
#[no_mangle]
pub fn op_222(a: u64, b: i32) -> <u64 as core::ops::BitXor<i32>>::Output {
    a ^ b
}
