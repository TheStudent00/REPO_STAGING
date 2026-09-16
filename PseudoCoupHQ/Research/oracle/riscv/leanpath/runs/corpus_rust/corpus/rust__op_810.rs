// probe 810 -- binary ..=
#[no_mangle]
pub fn op_810(a: f64, b: i32) -> core::ops::RangeInclusive<f64> {
    a ..= b
}
