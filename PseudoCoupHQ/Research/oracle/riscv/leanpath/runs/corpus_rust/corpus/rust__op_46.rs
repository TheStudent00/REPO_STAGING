// probe 46 -- unary ..=
#[no_mangle]
pub fn op_46(a: f64) -> core::ops::RangeToInclusive<f64> {
    ..=a
}
