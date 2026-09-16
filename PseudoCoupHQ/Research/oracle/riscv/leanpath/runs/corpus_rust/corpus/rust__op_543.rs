// probe 543 -- binary +
#[no_mangle]
pub fn op_543(a: i64, b: f32) -> <i64 as core::ops::Add<f32>>::Output {
    a + b
}
