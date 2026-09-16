// probe 145 -- binary &
#[no_mangle]
pub fn op_145(a: i64, b: i64) -> <i64 as core::ops::BitAnd<i64>>::Output {
    a & b
}
