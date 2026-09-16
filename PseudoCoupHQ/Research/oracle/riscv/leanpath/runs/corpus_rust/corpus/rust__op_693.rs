// probe 693 -- binary %
#[no_mangle]
pub fn op_693(a: u64, b: f32) -> <u64 as core::ops::Rem<f32>>::Output {
    a % b
}
