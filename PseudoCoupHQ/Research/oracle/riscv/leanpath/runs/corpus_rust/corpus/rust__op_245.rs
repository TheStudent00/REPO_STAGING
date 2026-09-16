// probe 245 -- binary ^
#[no_mangle]
pub fn op_245(a: bool, b: bool) -> <bool as core::ops::BitXor<bool>>::Output {
    a ^ b
}
