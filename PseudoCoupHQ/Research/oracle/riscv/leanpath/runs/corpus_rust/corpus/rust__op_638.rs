// probe 638 -- binary *
#[no_mangle]
pub fn op_638(a: bool, b: u64) -> <bool as core::ops::Mul<u64>>::Output {
    a * b
}
