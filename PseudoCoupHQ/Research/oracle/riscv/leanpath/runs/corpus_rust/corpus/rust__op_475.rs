// probe 475 -- binary <<
#[no_mangle]
pub fn op_475(a: u64, b: i64) -> <u64 as core::ops::Shl<i64>>::Output {
    a << b
}
