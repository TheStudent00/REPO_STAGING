// probe 182 -- binary |
#[no_mangle]
pub fn op_182(a: i64, b: u64) -> <i64 as core::ops::BitOr<u64>>::Output {
    a | b
}
