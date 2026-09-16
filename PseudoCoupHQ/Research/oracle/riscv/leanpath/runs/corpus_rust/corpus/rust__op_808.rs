// probe 808 -- binary ..=
#[no_mangle]
pub fn op_808(a: f32, b: f64) -> core::ops::RangeInclusive<f32> {
    a ..= b
}
