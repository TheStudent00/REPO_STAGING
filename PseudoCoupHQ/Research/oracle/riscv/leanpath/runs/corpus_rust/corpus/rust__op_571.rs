// probe 571 -- binary -
#[no_mangle]
pub fn op_571(a: i32, b: i64) -> <i32 as core::ops::Sub<i64>>::Output {
    a - b
}
