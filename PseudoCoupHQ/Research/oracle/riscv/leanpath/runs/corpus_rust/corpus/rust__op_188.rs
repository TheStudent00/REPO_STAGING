// probe 188 -- binary |
#[no_mangle]
pub fn op_188(a: u64, b: u64) -> <u64 as core::ops::BitOr<u64>>::Output {
    a | b
}
