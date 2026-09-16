// probe 36 -- unary ..
#[no_mangle]
pub fn op_36(a: i32) -> core::ops::RangeTo<i32> {
    ..a
}
