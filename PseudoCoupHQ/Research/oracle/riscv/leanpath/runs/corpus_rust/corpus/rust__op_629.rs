// probe 629 -- binary *
#[no_mangle]
pub fn op_629(a: f32, b: bool) -> <f32 as core::ops::Mul<bool>>::Output {
    a * b
}
