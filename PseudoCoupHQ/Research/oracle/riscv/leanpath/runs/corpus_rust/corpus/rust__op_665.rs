// probe 665 -- binary /
#[no_mangle]
pub fn op_665(a: f32, b: bool) -> <f32 as core::ops::Div<bool>>::Output {
    a / b
}
