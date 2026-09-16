// probe 688 -- binary %
#[no_mangle]
pub fn op_688(a: i64, b: f64) -> <i64 as core::ops::Rem<f64>>::Output {
    a % b
}
