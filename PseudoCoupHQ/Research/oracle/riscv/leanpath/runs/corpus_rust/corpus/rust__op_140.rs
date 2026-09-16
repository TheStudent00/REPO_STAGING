// probe 140 -- binary &
#[no_mangle]
pub fn op_140(a: i32, b: u64) -> <i32 as core::ops::BitAnd<u64>>::Output {
    a & b
}
