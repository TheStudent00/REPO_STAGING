// probe 690 -- binary %
#[no_mangle]
pub fn op_690(a: u64, b: i32) -> <u64 as core::ops::Rem<i32>>::Output {
    a % b
}
