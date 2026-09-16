// probe 473 -- binary <<
#[no_mangle]
pub fn op_473(a: i64, b: bool) -> <i64 as core::ops::Shl<bool>>::Output {
    a << b
}
