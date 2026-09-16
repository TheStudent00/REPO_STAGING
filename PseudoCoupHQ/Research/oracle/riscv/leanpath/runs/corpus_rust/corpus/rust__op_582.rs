// probe 582 -- binary -
#[no_mangle]
pub fn op_582(a: u64, b: i32) -> <u64 as core::ops::Sub<i32>>::Output {
    a - b
}
