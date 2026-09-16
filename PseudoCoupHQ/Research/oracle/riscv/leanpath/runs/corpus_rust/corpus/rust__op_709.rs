// probe 709 -- binary %
#[no_mangle]
pub fn op_709(a: bool, b: i64) -> <bool as core::ops::Rem<i64>>::Output {
    a % b
}
