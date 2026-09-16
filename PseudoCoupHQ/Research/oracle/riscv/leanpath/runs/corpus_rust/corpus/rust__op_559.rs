// probe 559 -- binary +
#[no_mangle]
pub fn op_559(a: f64, b: i64) -> <f64 as core::ops::Add<i64>>::Output {
    a + b
}
