// probe 637 -- binary *
#[no_mangle]
pub fn op_637(a: bool, b: i64) -> <bool as core::ops::Mul<i64>>::Output {
    a * b
}
