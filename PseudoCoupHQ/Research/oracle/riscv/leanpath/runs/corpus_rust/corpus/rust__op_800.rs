// probe 800 -- binary ..=
#[no_mangle]
pub fn op_800(a: u64, b: u64) -> core::ops::RangeInclusive<u64> {
    a ..= b
}
