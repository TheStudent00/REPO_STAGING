// probe 181 -- binary |
#[no_mangle]
pub fn op_181(a: i64, b: i64) -> <i64 as core::ops::BitOr<i64>>::Output {
    a | b
}
