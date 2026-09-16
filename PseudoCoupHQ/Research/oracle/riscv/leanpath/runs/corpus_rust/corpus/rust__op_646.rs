// probe 646 -- binary /
#[no_mangle]
pub fn op_646(a: i32, b: f64) -> <i32 as core::ops::Div<f64>>::Output {
    a / b
}
