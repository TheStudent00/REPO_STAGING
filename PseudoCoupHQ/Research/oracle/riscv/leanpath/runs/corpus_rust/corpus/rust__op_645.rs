// probe 645 -- binary /
#[no_mangle]
pub fn op_645(a: i32, b: f32) -> <i32 as core::ops::Div<f32>>::Output {
    a / b
}
