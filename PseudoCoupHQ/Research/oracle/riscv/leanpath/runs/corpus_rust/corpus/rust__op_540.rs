// probe 540 -- binary +
#[no_mangle]
pub fn op_540(a: i64, b: i32) -> <i64 as core::ops::Add<i32>>::Output {
    a + b
}
