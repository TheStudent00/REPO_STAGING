// probe 568 -- binary +
#[no_mangle]
pub fn op_568(a: bool, b: f64) -> <bool as core::ops::Add<f64>>::Output {
    a + b
}
