// probe 493 -- binary <<
#[no_mangle]
pub fn op_493(a: bool, b: i64) -> <bool as core::ops::Shl<i64>>::Output {
    a << b
}
