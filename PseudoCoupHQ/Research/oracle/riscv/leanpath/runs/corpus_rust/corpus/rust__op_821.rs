// probe 821 -- binary ..=
#[no_mangle]
pub fn op_821(a: bool, b: bool) -> core::ops::RangeInclusive<bool> {
    a ..= b
}
