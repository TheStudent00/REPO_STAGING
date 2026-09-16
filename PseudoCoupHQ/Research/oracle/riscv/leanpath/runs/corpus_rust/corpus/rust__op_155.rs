// probe 155 -- binary &
#[no_mangle]
pub fn op_155(a: u64, b: bool) -> <u64 as core::ops::BitAnd<bool>>::Output {
    a & b
}
