// probe 468 -- binary <<
#[no_mangle]
pub fn op_468(a: i64, b: i32) -> <i64 as core::ops::Shl<i32>>::Output {
    a << b
}
