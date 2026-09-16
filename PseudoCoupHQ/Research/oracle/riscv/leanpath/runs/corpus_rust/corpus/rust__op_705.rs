// probe 705 -- binary %
#[no_mangle]
pub fn op_705(a: f64, b: f32) -> <f64 as core::ops::Rem<f32>>::Output {
    a % b
}
