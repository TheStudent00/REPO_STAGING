// probe 653 -- binary /
#[no_mangle]
pub fn op_653(a: i64, b: bool) -> <i64 as core::ops::Div<bool>>::Output {
    a / b
}
