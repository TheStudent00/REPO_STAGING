// probe 799 -- binary ..=
#[no_mangle]
pub fn op_799(a: u64, b: i64) -> core::ops::RangeInclusive<u64> {
    a ..= b
}
