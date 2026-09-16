// probe 575 -- binary -
#[no_mangle]
pub fn op_575(a: i32, b: bool) -> <i32 as core::ops::Sub<bool>>::Output {
    a - b
}
