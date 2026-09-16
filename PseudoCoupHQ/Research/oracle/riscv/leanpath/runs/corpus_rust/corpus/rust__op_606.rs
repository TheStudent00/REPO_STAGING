// probe 606 -- binary *
#[no_mangle]
pub fn op_606(a: i32, b: i32) -> <i32 as core::ops::Mul<i32>>::Output {
    a * b
}
