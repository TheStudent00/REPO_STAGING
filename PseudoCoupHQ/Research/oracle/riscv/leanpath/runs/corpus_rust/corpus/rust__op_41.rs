// probe 41 -- unary ..
#[no_mangle]
pub fn op_41(a: bool) -> core::ops::RangeTo<bool> {
    ..a
}
