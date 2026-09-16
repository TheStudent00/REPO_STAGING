// probe 710 -- binary %
#[no_mangle]
pub fn op_710(a: bool, b: u64) -> <bool as core::ops::Rem<u64>>::Output {
    a % b
}
