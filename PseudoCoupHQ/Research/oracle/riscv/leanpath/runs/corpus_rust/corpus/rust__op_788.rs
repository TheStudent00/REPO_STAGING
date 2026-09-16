// probe 788 -- binary ..=
#[no_mangle]
pub fn op_788(a: i32, b: u64) -> core::ops::RangeInclusive<i32> {
    a ..= b
}
