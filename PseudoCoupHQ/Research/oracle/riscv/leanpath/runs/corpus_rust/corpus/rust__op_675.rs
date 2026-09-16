// probe 675 -- binary /
#[no_mangle]
pub fn op_675(a: bool, b: f32) -> <bool as core::ops::Div<f32>>::Output {
    a / b
}
