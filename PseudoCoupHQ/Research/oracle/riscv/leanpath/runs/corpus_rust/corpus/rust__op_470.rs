// probe 470 -- binary <<
#[no_mangle]
pub fn op_470(a: i64, b: u64) -> <i64 as core::ops::Shl<u64>>::Output {
    a << b
}
