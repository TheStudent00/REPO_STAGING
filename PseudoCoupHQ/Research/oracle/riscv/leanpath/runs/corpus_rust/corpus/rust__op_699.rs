// probe 699 -- binary %
#[no_mangle]
pub fn op_699(a: f32, b: f32) -> <f32 as core::ops::Rem<f32>>::Output {
    a % b
}
