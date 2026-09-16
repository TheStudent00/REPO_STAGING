// probe 707 -- binary %
#[no_mangle]
pub fn op_707(a: f64, b: bool) -> <f64 as core::ops::Rem<bool>>::Output {
    a % b
}
