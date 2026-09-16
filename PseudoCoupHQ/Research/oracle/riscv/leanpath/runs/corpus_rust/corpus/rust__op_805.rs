// probe 805 -- binary ..=
#[no_mangle]
pub fn op_805(a: f32, b: i64) -> core::ops::RangeInclusive<f32> {
    a ..= b
}
