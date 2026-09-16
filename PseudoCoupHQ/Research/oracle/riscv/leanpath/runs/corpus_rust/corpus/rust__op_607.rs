// probe 607 -- binary *
#[no_mangle]
pub fn op_607(a: i32, b: i64) -> <i32 as core::ops::Mul<i64>>::Output {
    a * b
}
