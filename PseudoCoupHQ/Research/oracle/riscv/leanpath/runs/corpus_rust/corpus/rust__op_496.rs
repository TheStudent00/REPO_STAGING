// probe 496 -- binary <<
#[no_mangle]
pub fn op_496(a: bool, b: f64) -> <bool as core::ops::Shl<f64>>::Output {
    a << b
}
