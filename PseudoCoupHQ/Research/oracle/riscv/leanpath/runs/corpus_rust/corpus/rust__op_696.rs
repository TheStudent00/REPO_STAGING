// probe 696 -- binary %
#[no_mangle]
pub fn op_696(a: f32, b: i32) -> <f32 as core::ops::Rem<i32>>::Output {
    a % b
}
