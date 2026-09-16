// probe 43 -- unary ..=
#[no_mangle]
pub fn op_43(a: i64) -> core::ops::RangeToInclusive<i64> {
    ..=a
}
