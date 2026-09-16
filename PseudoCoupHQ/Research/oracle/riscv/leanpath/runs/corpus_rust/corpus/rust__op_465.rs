// probe 465 -- binary <<
#[no_mangle]
pub fn op_465(a: i32, b: f32) -> <i32 as core::ops::Shl<f32>>::Output {
    a << b
}
