// probe 163 -- binary &
#[no_mangle]
pub fn op_163(a: f64, b: i64) -> <f64 as core::ops::BitAnd<i64>>::Output {
    a & b
}
