// probe 170 -- binary &
#[no_mangle]
pub fn op_170(a: bool, b: u64) -> <bool as core::ops::BitAnd<u64>>::Output {
    a & b
}
