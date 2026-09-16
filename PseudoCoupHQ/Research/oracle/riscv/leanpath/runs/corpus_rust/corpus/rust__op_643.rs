// probe 643 -- binary /
#[no_mangle]
pub fn op_643(a: i32, b: i64) -> <i32 as core::ops::Div<i64>>::Output {
    a / b
}
