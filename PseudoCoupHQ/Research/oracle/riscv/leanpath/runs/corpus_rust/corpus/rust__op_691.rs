// probe 691 -- binary %
#[no_mangle]
pub fn op_691(a: u64, b: i64) -> <u64 as core::ops::Rem<i64>>::Output {
    a % b
}
