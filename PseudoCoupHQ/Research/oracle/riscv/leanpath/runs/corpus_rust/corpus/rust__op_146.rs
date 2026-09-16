// probe 146 -- binary &
#[no_mangle]
pub fn op_146(a: i64, b: u64) -> <i64 as core::ops::BitAnd<u64>>::Output {
    a & b
}
