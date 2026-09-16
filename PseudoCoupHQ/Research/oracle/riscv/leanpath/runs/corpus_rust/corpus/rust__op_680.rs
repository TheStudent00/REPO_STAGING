// probe 680 -- binary %
#[no_mangle]
pub fn op_680(a: i32, b: u64) -> <i32 as core::ops::Rem<u64>>::Output {
    a % b
}
