// probe 244 -- binary ^
#[no_mangle]
pub fn op_244(a: bool, b: f64) -> <bool as core::ops::BitXor<f64>>::Output {
    a ^ b
}
