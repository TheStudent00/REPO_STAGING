// probe 708 -- binary %
#[no_mangle]
pub fn op_708(a: bool, b: i32) -> <bool as core::ops::Rem<i32>>::Output {
    a % b
}
