// probe 814 -- binary ..=
#[no_mangle]
pub fn op_814(a: f64, b: f64) -> core::ops::RangeInclusive<f64> {
    a ..= b
}
