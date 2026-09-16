// probe 490 -- binary <<
#[no_mangle]
pub fn op_490(a: f64, b: f64) -> <f64 as core::ops::Shl<f64>>::Output {
    a << b
}
