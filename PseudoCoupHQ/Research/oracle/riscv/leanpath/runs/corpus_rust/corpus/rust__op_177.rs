// probe 177 -- binary |
#[no_mangle]
pub fn op_177(a: i32, b: f32) -> <i32 as core::ops::BitOr<f32>>::Output {
    a | b
}
