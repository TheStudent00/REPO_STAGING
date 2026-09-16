// probe 152 -- binary &
#[no_mangle]
pub fn op_152(a: u64, b: u64) -> <u64 as core::ops::BitAnd<u64>>::Output {
    a & b
}
