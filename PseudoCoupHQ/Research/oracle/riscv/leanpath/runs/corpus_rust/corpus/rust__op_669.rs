// probe 669 -- binary /
#[no_mangle]
pub fn op_669(a: f64, b: f32) -> <f64 as core::ops::Div<f32>>::Output {
    a / b
}
