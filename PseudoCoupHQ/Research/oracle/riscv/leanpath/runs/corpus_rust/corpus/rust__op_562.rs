// probe 562 -- binary +
#[no_mangle]
pub fn op_562(a: f64, b: f64) -> <f64 as core::ops::Add<f64>>::Output {
    a + b
}
