// probe 192 -- binary |
#[no_mangle]
pub fn op_192(a: f32, b: i32) -> <f32 as core::ops::BitOr<i32>>::Output {
    a | b
}
