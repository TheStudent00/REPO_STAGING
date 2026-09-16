// probe 813 -- binary ..=
#[no_mangle]
pub fn op_813(a: f64, b: f32) -> core::ops::RangeInclusive<f64> {
    a ..= b
}
