// probe 569 -- binary +
#[no_mangle]
pub fn op_569(a: bool, b: bool) -> <bool as core::ops::Add<bool>>::Output {
    a + b
}
