// probe 663 -- binary /
#[no_mangle]
pub fn op_663(a: f32, b: f32) -> <f32 as core::ops::Div<f32>>::Output {
    a / b
}
