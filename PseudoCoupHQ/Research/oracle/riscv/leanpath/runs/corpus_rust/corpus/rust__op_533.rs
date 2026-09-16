// probe 533 -- binary >>
#[no_mangle]
pub fn op_533(a: bool, b: bool) -> <bool as core::ops::Shr<bool>>::Output {
    a >> b
}
