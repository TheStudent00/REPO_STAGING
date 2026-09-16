// probe 538 -- binary +
#[no_mangle]
pub fn op_538(a: i32, b: f64) -> <i32 as core::ops::Add<f64>>::Output {
    a + b
}
