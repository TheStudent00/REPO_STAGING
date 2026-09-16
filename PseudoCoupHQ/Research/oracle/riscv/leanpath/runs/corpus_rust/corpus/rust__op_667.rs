// probe 667 -- binary /
#[no_mangle]
pub fn op_667(a: f64, b: i64) -> <f64 as core::ops::Div<i64>>::Output {
    a / b
}
