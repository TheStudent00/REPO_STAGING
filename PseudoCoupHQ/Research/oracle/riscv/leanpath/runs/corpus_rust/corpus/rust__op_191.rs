// probe 191 -- binary |
#[no_mangle]
pub fn op_191(a: u64, b: bool) -> <u64 as core::ops::BitOr<bool>>::Output {
    a | b
}
