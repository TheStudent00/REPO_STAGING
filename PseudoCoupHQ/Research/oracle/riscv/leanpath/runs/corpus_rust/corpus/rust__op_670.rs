// probe 670 -- binary /
#[no_mangle]
pub fn op_670(a: f64, b: f64) -> <f64 as core::ops::Div<f64>>::Output {
    a / b
}
