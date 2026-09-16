// probe 205 -- binary |
#[no_mangle]
pub fn op_205(a: bool, b: i64) -> <bool as core::ops::BitOr<i64>>::Output {
    a | b
}
