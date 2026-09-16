// probe 196 -- binary |
#[no_mangle]
pub fn op_196(a: f32, b: f64) -> <f32 as core::ops::BitOr<f64>>::Output {
    a | b
}
