// probe 698 -- binary %
#[no_mangle]
pub fn op_698(a: f32, b: u64) -> <f32 as core::ops::Rem<u64>>::Output {
    a % b
}
