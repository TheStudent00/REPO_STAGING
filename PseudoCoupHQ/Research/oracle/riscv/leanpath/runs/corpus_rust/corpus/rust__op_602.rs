// probe 602 -- binary -
#[no_mangle]
pub fn op_602(a: bool, b: u64) -> <bool as core::ops::Sub<u64>>::Output {
    a - b
}
