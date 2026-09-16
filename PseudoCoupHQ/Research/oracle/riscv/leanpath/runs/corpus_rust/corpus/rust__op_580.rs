// probe 580 -- binary -
#[no_mangle]
pub fn op_580(a: i64, b: f64) -> <i64 as core::ops::Sub<f64>>::Output {
    a - b
}
