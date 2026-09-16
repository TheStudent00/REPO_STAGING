// probe 695 -- binary %
#[no_mangle]
pub fn op_695(a: u64, b: bool) -> <u64 as core::ops::Rem<bool>>::Output {
    a % b
}
