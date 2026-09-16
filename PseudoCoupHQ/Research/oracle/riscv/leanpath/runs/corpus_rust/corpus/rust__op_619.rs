// probe 619 -- binary *
#[no_mangle]
pub fn op_619(a: u64, b: i64) -> <u64 as core::ops::Mul<i64>>::Output {
    a * b
}
