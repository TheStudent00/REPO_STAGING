// probe 489 -- binary <<
#[no_mangle]
pub fn op_489(a: f64, b: f32) -> <f64 as core::ops::Shl<f32>>::Output {
    a << b
}
