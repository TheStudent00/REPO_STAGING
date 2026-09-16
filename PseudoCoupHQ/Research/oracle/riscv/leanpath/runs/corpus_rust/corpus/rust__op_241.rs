// probe 241 -- binary ^
#[no_mangle]
pub fn op_241(a: bool, b: i64) -> <bool as core::ops::BitXor<i64>>::Output {
    a ^ b
}
