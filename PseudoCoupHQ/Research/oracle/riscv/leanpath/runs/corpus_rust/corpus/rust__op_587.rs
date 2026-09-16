// probe 587 -- binary -
#[no_mangle]
pub fn op_587(a: u64, b: bool) -> <u64 as core::ops::Sub<bool>>::Output {
    a - b
}
