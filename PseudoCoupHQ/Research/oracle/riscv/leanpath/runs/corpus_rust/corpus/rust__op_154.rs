// probe 154 -- binary &
#[no_mangle]
pub fn op_154(a: u64, b: f64) -> <u64 as core::ops::BitAnd<f64>>::Output {
    a & b
}
