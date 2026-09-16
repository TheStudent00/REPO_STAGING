// probe 494 -- binary <<
#[no_mangle]
pub fn op_494(a: bool, b: u64) -> <bool as core::ops::Shl<u64>>::Output {
    a << b
}
