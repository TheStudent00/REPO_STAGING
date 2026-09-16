// probe 686 -- binary %
#[no_mangle]
pub fn op_686(a: i64, b: u64) -> <i64 as core::ops::Rem<u64>>::Output {
    a % b
}
