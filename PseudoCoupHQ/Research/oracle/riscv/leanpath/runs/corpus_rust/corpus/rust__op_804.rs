// probe 804 -- binary ..=
#[no_mangle]
pub fn op_804(a: f32, b: i32) -> core::ops::RangeInclusive<f32> {
    a ..= b
}
