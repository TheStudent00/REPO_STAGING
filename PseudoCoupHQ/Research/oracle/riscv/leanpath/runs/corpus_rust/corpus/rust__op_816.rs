// probe 816 -- binary ..=
#[no_mangle]
pub fn op_816(a: bool, b: i32) -> core::ops::RangeInclusive<bool> {
    a ..= b
}
