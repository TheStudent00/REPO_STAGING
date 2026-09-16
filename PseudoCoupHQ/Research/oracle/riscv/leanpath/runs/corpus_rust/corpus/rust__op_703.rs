// probe 703 -- binary %
#[no_mangle]
pub fn op_703(a: f64, b: i64) -> <f64 as core::ops::Rem<i64>>::Output {
    a % b
}
