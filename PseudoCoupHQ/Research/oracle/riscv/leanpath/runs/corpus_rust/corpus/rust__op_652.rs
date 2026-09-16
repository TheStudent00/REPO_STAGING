// probe 652 -- binary /
#[no_mangle]
pub fn op_652(a: i64, b: f64) -> <i64 as core::ops::Div<f64>>::Output {
    a / b
}
