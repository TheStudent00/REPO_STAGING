// probe 501 -- binary >>
#[no_mangle]
pub fn op_501(a: i32, b: f32) -> <i32 as core::ops::Shr<f32>>::Output {
    a >> b
}
