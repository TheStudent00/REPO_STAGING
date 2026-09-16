// probe 641 -- binary *
#[no_mangle]
pub fn op_641(a: bool, b: bool) -> <bool as core::ops::Mul<bool>>::Output {
    a * b
}
