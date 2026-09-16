// probe 706 -- binary %
#[no_mangle]
pub fn op_706(a: f64, b: f64) -> <f64 as core::ops::Rem<f64>>::Output {
    a % b
}
