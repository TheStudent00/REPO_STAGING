// probe 175 -- binary |
#[no_mangle]
pub fn op_175(a: i32, b: i64) -> <i32 as core::ops::BitOr<i64>>::Output {
    a | b
}
