// probe 685 -- binary %
#[no_mangle]
pub fn op_685(a: i64, b: i64) -> <i64 as core::ops::Rem<i64>>::Output {
    a % b
}
