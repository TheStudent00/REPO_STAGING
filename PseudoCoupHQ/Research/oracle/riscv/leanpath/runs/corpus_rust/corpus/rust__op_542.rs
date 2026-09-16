// probe 542 -- binary +
#[no_mangle]
pub fn op_542(a: i64, b: u64) -> <i64 as core::ops::Add<u64>>::Output {
    a + b
}
