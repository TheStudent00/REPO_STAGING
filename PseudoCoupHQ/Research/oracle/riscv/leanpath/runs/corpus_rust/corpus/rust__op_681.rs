// probe 681 -- binary %
#[no_mangle]
pub fn op_681(a: i32, b: f32) -> <i32 as core::ops::Rem<f32>>::Output {
    a % b
}
