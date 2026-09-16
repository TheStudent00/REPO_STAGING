// probe 648 -- binary /
#[no_mangle]
pub fn op_648(a: i64, b: i32) -> <i64 as core::ops::Div<i32>>::Output {
    a / b
}
