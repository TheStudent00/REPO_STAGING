// probe 623 -- binary *
#[no_mangle]
pub fn op_623(a: u64, b: bool) -> <u64 as core::ops::Mul<bool>>::Output {
    a * b
}
