// probe 787 -- binary ..=
#[no_mangle]
pub fn op_787(a: i32, b: i64) -> core::ops::RangeInclusive<i32> {
    a ..= b
}
