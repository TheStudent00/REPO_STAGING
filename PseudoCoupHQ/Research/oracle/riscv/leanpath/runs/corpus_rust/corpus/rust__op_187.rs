// probe 187 -- binary |
#[no_mangle]
pub fn op_187(a: u64, b: i64) -> <u64 as core::ops::BitOr<i64>>::Output {
    a | b
}
