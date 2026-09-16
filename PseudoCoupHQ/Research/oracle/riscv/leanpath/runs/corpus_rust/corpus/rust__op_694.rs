// probe 694 -- binary %
#[no_mangle]
pub fn op_694(a: u64, b: f64) -> <u64 as core::ops::Rem<f64>>::Output {
    a % b
}
