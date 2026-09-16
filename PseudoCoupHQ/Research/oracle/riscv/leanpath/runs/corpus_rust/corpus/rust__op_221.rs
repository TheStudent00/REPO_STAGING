// probe 221 -- binary ^
#[no_mangle]
pub fn op_221(a: i64, b: bool) -> <i64 as core::ops::BitXor<bool>>::Output {
    a ^ b
}
