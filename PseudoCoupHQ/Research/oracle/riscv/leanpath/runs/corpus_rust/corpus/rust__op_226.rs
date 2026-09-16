// probe 226 -- binary ^
#[no_mangle]
pub fn op_226(a: u64, b: f64) -> <u64 as core::ops::BitXor<f64>>::Output {
    a ^ b
}
