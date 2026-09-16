// probe 647 -- binary /
#[no_mangle]
pub fn op_647(a: i32, b: bool) -> <i32 as core::ops::Div<bool>>::Output {
    a / b
}
