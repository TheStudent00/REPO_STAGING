// probe 576 -- binary -
#[no_mangle]
pub fn op_576(a: i64, b: i32) -> <i64 as core::ops::Sub<i32>>::Output {
    a - b
}
