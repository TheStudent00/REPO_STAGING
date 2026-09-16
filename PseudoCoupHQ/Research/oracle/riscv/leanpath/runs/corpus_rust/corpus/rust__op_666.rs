// probe 666 -- binary /
#[no_mangle]
pub fn op_666(a: f64, b: i32) -> <f64 as core::ops::Div<i32>>::Output {
    a / b
}
