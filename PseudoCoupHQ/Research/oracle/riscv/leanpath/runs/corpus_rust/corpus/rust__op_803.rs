// probe 803 -- binary ..=
#[no_mangle]
pub fn op_803(a: u64, b: bool) -> core::ops::RangeInclusive<u64> {
    a ..= b
}
