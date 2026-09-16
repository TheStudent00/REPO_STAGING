// probe 812 -- binary ..=
#[no_mangle]
pub fn op_812(a: f64, b: u64) -> core::ops::RangeInclusive<f64> {
    a ..= b
}
