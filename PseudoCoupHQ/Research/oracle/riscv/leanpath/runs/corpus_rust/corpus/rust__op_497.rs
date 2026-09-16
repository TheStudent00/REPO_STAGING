// probe 497 -- binary <<
#[no_mangle]
pub fn op_497(a: bool, b: bool) -> <bool as core::ops::Shl<bool>>::Output {
    a << b
}
