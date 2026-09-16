// probe 611 -- binary *
#[no_mangle]
pub fn op_611(a: i32, b: bool) -> <i32 as core::ops::Mul<bool>>::Output {
    a * b
}
