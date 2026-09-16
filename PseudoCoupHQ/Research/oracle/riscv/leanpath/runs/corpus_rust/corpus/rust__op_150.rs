// probe 150 -- binary &
#[no_mangle]
pub fn op_150(a: u64, b: i32) -> <u64 as core::ops::BitAnd<i32>>::Output {
    a & b
}
