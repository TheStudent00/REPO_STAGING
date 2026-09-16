// probe 811 -- binary ..=
#[no_mangle]
pub fn op_811(a: f64, b: i64) -> core::ops::RangeInclusive<f64> {
    a ..= b
}
