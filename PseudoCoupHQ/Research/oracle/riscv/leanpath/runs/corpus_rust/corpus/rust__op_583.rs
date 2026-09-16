// probe 583 -- binary -
#[no_mangle]
pub fn op_583(a: u64, b: i64) -> <u64 as core::ops::Sub<i64>>::Output {
    a - b
}
