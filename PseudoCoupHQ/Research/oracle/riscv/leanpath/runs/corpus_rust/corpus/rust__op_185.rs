// probe 185 -- binary |
#[no_mangle]
pub fn op_185(a: i64, b: bool) -> <i64 as core::ops::BitOr<bool>>::Output {
    a | b
}
