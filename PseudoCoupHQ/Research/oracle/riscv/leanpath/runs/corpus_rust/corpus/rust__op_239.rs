// probe 239 -- binary ^
#[no_mangle]
pub fn op_239(a: f64, b: bool) -> <f64 as core::ops::BitXor<bool>>::Output {
    a ^ b
}
