// probe 636 -- binary *
#[no_mangle]
pub fn op_636(a: bool, b: i32) -> <bool as core::ops::Mul<i32>>::Output {
    a * b
}
