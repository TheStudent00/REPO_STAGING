// probe 684 -- binary %
#[no_mangle]
pub fn op_684(a: i64, b: i32) -> <i64 as core::ops::Rem<i32>>::Output {
    a % b
}
