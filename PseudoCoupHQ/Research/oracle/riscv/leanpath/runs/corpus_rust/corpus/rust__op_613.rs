// probe 613 -- binary *
#[no_mangle]
pub fn op_613(a: i64, b: i64) -> <i64 as core::ops::Mul<i64>>::Output {
    a * b
}
