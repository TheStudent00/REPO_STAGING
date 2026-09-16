// probe 791 -- binary ..=
#[no_mangle]
pub fn op_791(a: i32, b: bool) -> core::ops::RangeInclusive<i32> {
    a ..= b
}
