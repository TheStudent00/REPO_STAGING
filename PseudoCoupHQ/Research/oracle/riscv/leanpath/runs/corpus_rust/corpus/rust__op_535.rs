// probe 535 -- binary +
#[no_mangle]
pub fn op_535(a: i32, b: i64) -> <i32 as core::ops::Add<i64>>::Output {
    a + b
}
