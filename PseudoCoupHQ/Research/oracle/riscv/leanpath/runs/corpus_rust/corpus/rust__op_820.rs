// probe 820 -- binary ..=
#[no_mangle]
pub fn op_820(a: bool, b: f64) -> core::ops::RangeInclusive<bool> {
    a ..= b
}
