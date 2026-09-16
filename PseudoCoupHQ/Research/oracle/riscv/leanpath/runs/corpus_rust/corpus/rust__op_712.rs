// probe 712 -- binary %
#[no_mangle]
pub fn op_712(a: bool, b: f64) -> <bool as core::ops::Rem<f64>>::Output {
    a % b
}
