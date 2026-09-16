// probe 160 -- binary &
#[no_mangle]
pub fn op_160(a: f32, b: f64) -> <f32 as core::ops::BitAnd<f64>>::Output {
    a & b
}
