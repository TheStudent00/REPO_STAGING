// probe 204 -- binary |
#[no_mangle]
pub fn op_204(a: bool, b: i32) -> <bool as core::ops::BitOr<i32>>::Output {
    a | b
}
