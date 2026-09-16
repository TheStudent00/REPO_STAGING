// probe 664 -- binary /
#[no_mangle]
pub fn op_664(a: f32, b: f64) -> <f32 as core::ops::Div<f64>>::Output {
    a / b
}
