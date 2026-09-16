// probe 687 -- binary %
#[no_mangle]
pub fn op_687(a: i64, b: f32) -> <i64 as core::ops::Rem<f32>>::Output {
    a % b
}
