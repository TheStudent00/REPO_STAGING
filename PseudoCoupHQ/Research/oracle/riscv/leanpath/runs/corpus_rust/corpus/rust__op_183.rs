// probe 183 -- binary |
#[no_mangle]
pub fn op_183(a: i64, b: f32) -> <i64 as core::ops::BitOr<f32>>::Output {
    a | b
}
