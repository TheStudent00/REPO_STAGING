// probe 242 -- binary ^
#[no_mangle]
pub fn op_242(a: bool, b: u64) -> <bool as core::ops::BitXor<u64>>::Output {
    a ^ b
}
