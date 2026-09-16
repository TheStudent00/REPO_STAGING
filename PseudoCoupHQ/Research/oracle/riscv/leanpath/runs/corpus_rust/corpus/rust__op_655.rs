// probe 655 -- binary /
#[no_mangle]
pub fn op_655(a: u64, b: i64) -> <u64 as core::ops::Div<i64>>::Output {
    a / b
}
