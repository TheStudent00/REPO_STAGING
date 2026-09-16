// probe 139 -- binary &
#[no_mangle]
pub fn op_139(a: i32, b: i64) -> <i32 as core::ops::BitAnd<i64>>::Output {
    a & b
}
