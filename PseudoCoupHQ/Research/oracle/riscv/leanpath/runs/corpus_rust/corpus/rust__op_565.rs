// probe 565 -- binary +
#[no_mangle]
pub fn op_565(a: bool, b: i64) -> <bool as core::ops::Add<i64>>::Output {
    a + b
}
