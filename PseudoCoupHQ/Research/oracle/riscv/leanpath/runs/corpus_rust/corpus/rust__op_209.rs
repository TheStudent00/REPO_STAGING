// probe 209 -- binary |
#[no_mangle]
pub fn op_209(a: bool, b: bool) -> <bool as core::ops::BitOr<bool>>::Output {
    a | b
}
