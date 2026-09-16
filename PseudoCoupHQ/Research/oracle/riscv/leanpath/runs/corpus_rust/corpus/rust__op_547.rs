// probe 547 -- binary +
#[no_mangle]
pub fn op_547(a: u64, b: i64) -> <u64 as core::ops::Add<i64>>::Output {
    a + b
}
