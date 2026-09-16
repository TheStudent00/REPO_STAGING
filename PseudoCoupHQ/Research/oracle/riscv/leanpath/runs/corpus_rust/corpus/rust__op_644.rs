// probe 644 -- binary /
#[no_mangle]
pub fn op_644(a: i32, b: u64) -> <i32 as core::ops::Div<u64>>::Output {
    a / b
}
