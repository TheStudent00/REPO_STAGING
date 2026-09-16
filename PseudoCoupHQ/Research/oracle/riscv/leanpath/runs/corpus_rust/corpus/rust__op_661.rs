// probe 661 -- binary /
#[no_mangle]
pub fn op_661(a: f32, b: i64) -> <f32 as core::ops::Div<i64>>::Output {
    a / b
}
