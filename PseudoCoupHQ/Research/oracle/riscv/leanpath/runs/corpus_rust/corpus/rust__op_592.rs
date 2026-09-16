// probe 592 -- binary -
#[no_mangle]
pub fn op_592(a: f32, b: f64) -> <f32 as core::ops::Sub<f64>>::Output {
    a - b
}
