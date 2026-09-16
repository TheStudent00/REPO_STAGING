// probe 642 -- binary /
#[no_mangle]
pub fn op_642(a: i32, b: i32) -> <i32 as core::ops::Div<i32>>::Output {
    a / b
}
