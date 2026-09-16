// probe 484 -- binary <<
#[no_mangle]
pub fn op_484(a: f32, b: f64) -> <f32 as core::ops::Shl<f64>>::Output {
    a << b
}
