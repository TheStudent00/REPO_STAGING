// probe 224 -- binary ^
#[no_mangle]
pub fn op_224(a: u64, b: u64) -> <u64 as core::ops::BitXor<u64>>::Output {
    a ^ b
}
