// probe 549 -- binary +
#[no_mangle]
pub fn op_549(a: u64, b: f32) -> <u64 as core::ops::Add<f32>>::Output {
    a + b
}
