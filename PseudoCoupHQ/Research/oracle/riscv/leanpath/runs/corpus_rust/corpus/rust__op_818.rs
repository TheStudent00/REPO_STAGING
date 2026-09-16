// probe 818 -- binary ..=
#[no_mangle]
pub fn op_818(a: bool, b: u64) -> core::ops::RangeInclusive<bool> {
    a ..= b
}
