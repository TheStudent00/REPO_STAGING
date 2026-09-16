// probe 674 -- binary /
#[no_mangle]
pub fn op_674(a: bool, b: u64) -> <bool as core::ops::Div<u64>>::Output {
    a / b
}
