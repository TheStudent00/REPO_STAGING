// probe 701 -- binary %
#[no_mangle]
pub fn op_701(a: f32, b: bool) -> <f32 as core::ops::Rem<bool>>::Output {
    a % b
}
