// probe 471 -- binary <<
#[no_mangle]
pub fn op_471(a: i64, b: f32) -> <i64 as core::ops::Shl<f32>>::Output {
    a << b
}
