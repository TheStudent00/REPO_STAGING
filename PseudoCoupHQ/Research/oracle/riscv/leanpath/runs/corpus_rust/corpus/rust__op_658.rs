// probe 658 -- binary /
#[no_mangle]
pub fn op_658(a: u64, b: f64) -> <u64 as core::ops::Div<f64>>::Output {
    a / b
}
