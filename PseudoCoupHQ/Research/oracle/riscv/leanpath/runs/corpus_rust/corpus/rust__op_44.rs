// probe 44 -- unary ..=
#[no_mangle]
pub fn op_44(a: u64) -> core::ops::RangeToInclusive<u64> {
    ..=a
}
