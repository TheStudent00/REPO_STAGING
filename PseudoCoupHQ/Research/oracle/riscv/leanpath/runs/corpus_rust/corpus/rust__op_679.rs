// probe 679 -- binary %
#[no_mangle]
pub fn op_679(a: i32, b: i64) -> <i32 as core::ops::Rem<i64>>::Output {
    a % b
}
