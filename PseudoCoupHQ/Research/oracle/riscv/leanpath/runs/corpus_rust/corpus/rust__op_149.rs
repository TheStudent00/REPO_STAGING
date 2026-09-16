// probe 149 -- binary &
#[no_mangle]
pub fn op_149(a: i64, b: bool) -> <i64 as core::ops::BitAnd<bool>>::Output {
    a & b
}
