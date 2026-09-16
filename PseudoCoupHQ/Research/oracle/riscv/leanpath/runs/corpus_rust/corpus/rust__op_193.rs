// probe 193 -- binary |
#[no_mangle]
pub fn op_193(a: f32, b: i64) -> <f32 as core::ops::BitOr<i64>>::Output {
    a | b
}
