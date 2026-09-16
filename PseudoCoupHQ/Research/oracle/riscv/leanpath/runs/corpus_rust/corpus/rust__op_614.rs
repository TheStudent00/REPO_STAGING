// probe 614 -- binary *
#[no_mangle]
pub fn op_614(a: i64, b: u64) -> <i64 as core::ops::Mul<u64>>::Output {
    a * b
}
