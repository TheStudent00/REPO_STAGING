// probe 195 -- binary |
#[no_mangle]
pub fn op_195(a: f32, b: f32) -> <f32 as core::ops::BitOr<f32>>::Output {
    a | b
}
