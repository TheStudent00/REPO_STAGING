// probe 651 -- binary /
#[no_mangle]
pub fn op_651(a: i64, b: f32) -> <i64 as core::ops::Div<f32>>::Output {
    a / b
}
