// probe 605 -- binary -
#[no_mangle]
pub fn op_605(a: bool, b: bool) -> <bool as core::ops::Sub<bool>>::Output {
    a - b
}
