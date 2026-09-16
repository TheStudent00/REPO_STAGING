// probe 477 -- binary <<
#[no_mangle]
pub fn op_477(a: u64, b: f32) -> <u64 as core::ops::Shl<f32>>::Output {
    a << b
}
