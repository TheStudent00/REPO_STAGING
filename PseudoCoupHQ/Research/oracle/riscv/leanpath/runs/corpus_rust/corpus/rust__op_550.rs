// probe 550 -- binary +
#[no_mangle]
pub fn op_550(a: u64, b: f64) -> <u64 as core::ops::Add<f64>>::Output {
    a + b
}
