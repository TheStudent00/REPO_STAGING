// probe 660 -- binary /
#[no_mangle]
pub fn op_660(a: f32, b: i32) -> <f32 as core::ops::Div<i32>>::Output {
    a / b
}
