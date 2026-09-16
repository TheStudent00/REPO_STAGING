// probe 656 -- binary /
#[no_mangle]
pub fn op_656(a: u64, b: u64) -> <u64 as core::ops::Div<u64>>::Output {
    a / b
}
