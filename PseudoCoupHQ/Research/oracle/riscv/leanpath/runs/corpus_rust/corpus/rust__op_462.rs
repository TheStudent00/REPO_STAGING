// probe 462 -- binary <<
#[no_mangle]
pub fn op_462(a: i32, b: i32) -> <i32 as core::ops::Shl<i32>>::Output {
    a << b
}
