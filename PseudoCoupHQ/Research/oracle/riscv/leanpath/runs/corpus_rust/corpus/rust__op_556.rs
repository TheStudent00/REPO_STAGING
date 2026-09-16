// probe 556 -- binary +
#[no_mangle]
pub fn op_556(a: f32, b: f64) -> <f32 as core::ops::Add<f64>>::Output {
    a + b
}
