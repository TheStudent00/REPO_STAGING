// probe 678 -- binary %
#[no_mangle]
pub fn op_678(a: i32, b: i32) -> <i32 as core::ops::Rem<i32>>::Output {
    a % b
}
