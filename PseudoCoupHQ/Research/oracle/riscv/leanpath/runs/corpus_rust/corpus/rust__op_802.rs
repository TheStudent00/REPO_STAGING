// probe 802 -- binary ..=
#[no_mangle]
pub fn op_802(a: u64, b: f64) -> core::ops::RangeInclusive<u64> {
    a ..= b
}
