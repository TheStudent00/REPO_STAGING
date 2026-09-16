// probe 604 -- binary -
#[no_mangle]
pub fn op_604(a: bool, b: f64) -> <bool as core::ops::Sub<f64>>::Output {
    a - b
}
