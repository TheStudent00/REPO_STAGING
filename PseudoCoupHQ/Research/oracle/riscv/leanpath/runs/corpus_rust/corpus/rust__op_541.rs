// probe 541 -- binary +
#[no_mangle]
pub fn op_541(a: i64, b: i64) -> <i64 as core::ops::Add<i64>>::Output {
    a + b
}
