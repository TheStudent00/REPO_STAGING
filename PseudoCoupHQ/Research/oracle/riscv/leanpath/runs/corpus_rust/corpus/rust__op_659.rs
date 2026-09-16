// probe 659 -- binary /
#[no_mangle]
pub fn op_659(a: u64, b: bool) -> <u64 as core::ops::Div<bool>>::Output {
    a / b
}
