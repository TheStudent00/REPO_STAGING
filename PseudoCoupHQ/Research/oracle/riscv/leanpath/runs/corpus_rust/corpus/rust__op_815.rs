// probe 815 -- binary ..=
#[no_mangle]
pub fn op_815(a: f64, b: bool) -> core::ops::RangeInclusive<f64> {
    a ..= b
}
