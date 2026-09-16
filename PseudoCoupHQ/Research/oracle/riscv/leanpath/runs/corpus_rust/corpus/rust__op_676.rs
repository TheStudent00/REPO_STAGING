// probe 676 -- binary /
#[no_mangle]
pub fn op_676(a: bool, b: f64) -> <bool as core::ops::Div<f64>>::Output {
    a / b
}
