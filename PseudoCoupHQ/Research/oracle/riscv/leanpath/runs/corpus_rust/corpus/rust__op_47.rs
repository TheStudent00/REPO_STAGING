// probe 47 -- unary ..=
#[no_mangle]
pub fn op_47(a: bool) -> core::ops::RangeToInclusive<bool> {
    ..=a
}
