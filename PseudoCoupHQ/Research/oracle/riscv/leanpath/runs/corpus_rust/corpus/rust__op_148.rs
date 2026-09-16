// probe 148 -- binary &
#[no_mangle]
pub fn op_148(a: i64, b: f64) -> <i64 as core::ops::BitAnd<f64>>::Output {
    a & b
}
