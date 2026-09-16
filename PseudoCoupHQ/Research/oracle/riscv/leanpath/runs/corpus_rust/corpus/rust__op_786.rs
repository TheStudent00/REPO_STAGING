// probe 786 -- binary ..=
#[no_mangle]
pub fn op_786(a: i32, b: i32) -> core::ops::RangeInclusive<i32> {
    a ..= b
}
