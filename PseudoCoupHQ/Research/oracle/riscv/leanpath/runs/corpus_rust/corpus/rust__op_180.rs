// probe 180 -- binary |
#[no_mangle]
pub fn op_180(a: i64, b: i32) -> <i64 as core::ops::BitOr<i32>>::Output {
    a | b
}
