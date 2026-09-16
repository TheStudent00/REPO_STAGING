// probe 478 -- binary <<
#[no_mangle]
pub fn op_478(a: u64, b: f64) -> <u64 as core::ops::Shl<f64>>::Output {
    a << b
}
