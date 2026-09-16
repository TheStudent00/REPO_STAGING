// probe 42 -- unary ..=
#[no_mangle]
pub fn op_42(a: i32) -> core::ops::RangeToInclusive<i32> {
    ..=a
}
