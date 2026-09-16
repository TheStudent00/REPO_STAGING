// probe 713 -- binary %
#[no_mangle]
pub fn op_713(a: bool, b: bool) -> <bool as core::ops::Rem<bool>>::Output {
    a % b
}
