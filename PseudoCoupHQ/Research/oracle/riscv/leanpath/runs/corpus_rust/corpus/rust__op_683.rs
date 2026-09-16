// probe 683 -- binary %
#[no_mangle]
pub fn op_683(a: i32, b: bool) -> <i32 as core::ops::Rem<bool>>::Output {
    a % b
}
