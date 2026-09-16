// probe 485 -- binary <<
#[no_mangle]
pub fn op_485(a: f32, b: bool) -> <f32 as core::ops::Shl<bool>>::Output {
    a << b
}
