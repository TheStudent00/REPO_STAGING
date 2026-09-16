// probe 179 -- binary |
#[no_mangle]
pub fn op_179(a: i32, b: bool) -> <i32 as core::ops::BitOr<bool>>::Output {
    a | b
}
