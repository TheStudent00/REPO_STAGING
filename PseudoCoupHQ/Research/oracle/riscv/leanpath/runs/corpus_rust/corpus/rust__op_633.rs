// probe 633 -- binary *
#[no_mangle]
pub fn op_633(a: f64, b: f32) -> <f64 as core::ops::Mul<f32>>::Output {
    a * b
}
