// probe 635 -- binary *
#[no_mangle]
pub fn op_635(a: f64, b: bool) -> <f64 as core::ops::Mul<bool>>::Output {
    a * b
}
