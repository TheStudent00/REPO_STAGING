// probe 792 -- binary ..=
#[no_mangle]
pub fn op_792(a: i64, b: i32) -> core::ops::RangeInclusive<i64> {
    a ..= b
}
