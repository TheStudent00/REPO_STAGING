// probe 227 -- binary ^
#[no_mangle]
pub fn op_227(a: u64, b: bool) -> <u64 as core::ops::BitXor<bool>>::Output {
    a ^ b
}
