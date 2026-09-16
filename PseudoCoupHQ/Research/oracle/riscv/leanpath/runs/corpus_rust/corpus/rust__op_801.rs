// probe 801 -- binary ..=
#[no_mangle]
pub fn op_801(a: u64, b: f32) -> core::ops::RangeInclusive<u64> {
    a ..= b
}
