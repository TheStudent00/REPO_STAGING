// probe 700 -- binary %
#[no_mangle]
pub fn op_700(a: f32, b: f64) -> <f32 as core::ops::Rem<f64>>::Output {
    a % b
}
