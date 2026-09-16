// probe 467 -- binary <<
#[no_mangle]
pub fn op_467(a: i32, b: bool) -> <i32 as core::ops::Shl<bool>>::Output {
    a << b
}
