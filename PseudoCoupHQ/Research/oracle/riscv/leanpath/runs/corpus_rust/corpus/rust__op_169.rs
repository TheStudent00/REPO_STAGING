// probe 169 -- binary &
#[no_mangle]
pub fn op_169(a: bool, b: i64) -> <bool as core::ops::BitAnd<i64>>::Output {
    a & b
}
