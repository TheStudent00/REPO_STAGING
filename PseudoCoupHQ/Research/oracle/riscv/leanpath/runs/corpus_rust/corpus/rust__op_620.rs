// probe 620 -- binary *
#[no_mangle]
pub fn op_620(a: u64, b: u64) -> <u64 as core::ops::Mul<u64>>::Output {
    a * b
}
