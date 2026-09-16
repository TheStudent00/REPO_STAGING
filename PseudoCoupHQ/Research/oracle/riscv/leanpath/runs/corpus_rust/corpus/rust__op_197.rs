// probe 197 -- binary |
#[no_mangle]
pub fn op_197(a: f32, b: bool) -> <f32 as core::ops::BitOr<bool>>::Output {
    a | b
}
