// probe 463 -- binary <<
#[no_mangle]
pub fn op_463(a: i32, b: i64) -> <i32 as core::ops::Shl<i64>>::Output {
    a << b
}
