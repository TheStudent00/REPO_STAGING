// probe 207 -- binary |
#[no_mangle]
pub fn op_207(a: bool, b: f32) -> <bool as core::ops::BitOr<f32>>::Output {
    a | b
}
