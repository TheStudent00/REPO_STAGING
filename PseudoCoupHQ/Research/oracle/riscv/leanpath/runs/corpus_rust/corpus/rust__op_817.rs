// probe 817 -- binary ..=
#[no_mangle]
pub fn op_817(a: bool, b: i64) -> core::ops::RangeInclusive<bool> {
    a ..= b
}
