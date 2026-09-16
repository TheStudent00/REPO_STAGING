// probe 692 -- binary %
#[no_mangle]
pub fn op_692(a: u64, b: u64) -> <u64 as core::ops::Rem<u64>>::Output {
    a % b
}
