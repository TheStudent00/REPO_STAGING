// probe 697 -- binary %
#[no_mangle]
pub fn op_697(a: f32, b: i64) -> <f32 as core::ops::Rem<i64>>::Output {
    a % b
}
