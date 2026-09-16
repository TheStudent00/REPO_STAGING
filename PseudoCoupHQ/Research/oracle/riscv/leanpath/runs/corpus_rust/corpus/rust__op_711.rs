// probe 711 -- binary %
#[no_mangle]
pub fn op_711(a: bool, b: f32) -> <bool as core::ops::Rem<f32>>::Output {
    a % b
}
