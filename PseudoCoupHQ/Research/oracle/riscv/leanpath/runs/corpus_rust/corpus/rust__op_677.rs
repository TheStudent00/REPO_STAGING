// probe 677 -- binary /
#[no_mangle]
pub fn op_677(a: bool, b: bool) -> <bool as core::ops::Div<bool>>::Output {
    a / b
}
