// probe 38 -- unary ..
#[no_mangle]
pub fn op_38(a: u64) -> core::ops::RangeTo<u64> {
    ..a
}
