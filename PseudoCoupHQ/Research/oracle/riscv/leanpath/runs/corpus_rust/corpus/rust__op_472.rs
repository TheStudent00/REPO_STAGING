// probe 472 -- binary <<
#[no_mangle]
pub fn op_472(a: i64, b: f64) -> <i64 as core::ops::Shl<f64>>::Output {
    a << b
}
