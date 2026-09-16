// probe 45 -- unary ..=
#[no_mangle]
pub fn op_45(a: f32) -> core::ops::RangeToInclusive<f32> {
    ..=a
}
