// probe 238 -- binary ^
#[no_mangle]
pub fn op_238(a: f64, b: f64) -> <f64 as core::ops::BitXor<f64>>::Output {
    a ^ b
}
