// probe 819 -- binary ..=
#[no_mangle]
pub fn op_819(a: bool, b: f32) -> core::ops::RangeInclusive<bool> {
    a ..= b
}
