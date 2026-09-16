// probe 469 -- binary <<
#[no_mangle]
pub fn op_469(a: i64, b: i64) -> <i64 as core::ops::Shl<i64>>::Output {
    a << b
}
