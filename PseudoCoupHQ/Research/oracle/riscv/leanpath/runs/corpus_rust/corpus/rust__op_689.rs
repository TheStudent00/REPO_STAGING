// probe 689 -- binary %
#[no_mangle]
pub fn op_689(a: i64, b: bool) -> <i64 as core::ops::Rem<bool>>::Output {
    a % b
}
