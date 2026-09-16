// probe 483 -- binary <<
#[no_mangle]
pub fn op_483(a: f32, b: f32) -> <f32 as core::ops::Shl<f32>>::Output {
    a << b
}
