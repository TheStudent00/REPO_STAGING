// probe 201 -- binary |
#[no_mangle]
pub fn op_201(a: f64, b: f32) -> <f64 as core::ops::BitOr<f32>>::Output {
    a | b
}
