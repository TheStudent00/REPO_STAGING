// probe 612 -- binary *
#[no_mangle]
pub fn op_612(a: i64, b: i32) -> <i64 as core::ops::Mul<i32>>::Output {
    a * b
}
