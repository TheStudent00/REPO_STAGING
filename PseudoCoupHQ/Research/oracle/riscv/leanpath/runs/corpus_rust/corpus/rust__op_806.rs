// probe 806 -- binary ..=
#[no_mangle]
pub fn op_806(a: f32, b: u64) -> core::ops::RangeInclusive<f32> {
    a ..= b
}
