// probe 586 -- binary -
#[no_mangle]
pub fn op_586(a: u64, b: f64) -> <u64 as core::ops::Sub<f64>>::Output {
    a - b
}
