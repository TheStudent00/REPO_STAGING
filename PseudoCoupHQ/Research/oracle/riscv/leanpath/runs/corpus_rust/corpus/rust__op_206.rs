// probe 206 -- binary |
#[no_mangle]
pub fn op_206(a: bool, b: u64) -> <bool as core::ops::BitOr<u64>>::Output {
    a | b
}
