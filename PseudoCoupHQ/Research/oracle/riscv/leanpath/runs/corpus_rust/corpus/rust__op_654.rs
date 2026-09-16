// probe 654 -- binary /
#[no_mangle]
pub fn op_654(a: u64, b: i32) -> <u64 as core::ops::Div<i32>>::Output {
    a / b
}
