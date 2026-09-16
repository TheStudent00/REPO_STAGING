// probe 492 -- binary <<
#[no_mangle]
pub fn op_492(a: bool, b: i32) -> <bool as core::ops::Shl<i32>>::Output {
    a << b
}
