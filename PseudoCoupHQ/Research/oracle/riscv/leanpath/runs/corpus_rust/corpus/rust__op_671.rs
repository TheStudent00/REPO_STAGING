// probe 671 -- binary /
#[no_mangle]
pub fn op_671(a: f64, b: bool) -> <f64 as core::ops::Div<bool>>::Output {
    a / b
}
