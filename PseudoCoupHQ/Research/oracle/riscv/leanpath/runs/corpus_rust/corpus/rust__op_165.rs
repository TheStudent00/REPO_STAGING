// probe 165 -- binary &
#[no_mangle]
pub fn op_165(a: f64, b: f32) -> <f64 as core::ops::BitAnd<f32>>::Output {
    a & b
}
