// probe 657 -- binary /
#[no_mangle]
pub fn op_657(a: u64, b: f32) -> <u64 as core::ops::Div<f32>>::Output {
    a / b
}
