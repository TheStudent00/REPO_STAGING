// probe 561 -- binary +
#[no_mangle]
pub fn op_561(a: f64, b: f32) -> <f64 as core::ops::Add<f32>>::Output {
    a + b
}
