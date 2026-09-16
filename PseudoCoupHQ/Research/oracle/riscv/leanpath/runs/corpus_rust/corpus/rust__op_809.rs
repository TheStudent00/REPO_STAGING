// probe 809 -- binary ..=
#[no_mangle]
pub fn op_809(a: f32, b: bool) -> core::ops::RangeInclusive<f32> {
    a ..= b
}
