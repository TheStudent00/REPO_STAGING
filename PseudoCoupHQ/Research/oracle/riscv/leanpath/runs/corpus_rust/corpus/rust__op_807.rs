// probe 807 -- binary ..=
#[no_mangle]
pub fn op_807(a: f32, b: f32) -> core::ops::RangeInclusive<f32> {
    a ..= b
}
