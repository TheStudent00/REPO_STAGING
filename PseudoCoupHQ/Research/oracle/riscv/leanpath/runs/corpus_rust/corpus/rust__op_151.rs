// probe 151 -- binary &
#[no_mangle]
pub fn op_151(a: u64, b: i64) -> <u64 as core::ops::BitAnd<i64>>::Output {
    a & b
}
