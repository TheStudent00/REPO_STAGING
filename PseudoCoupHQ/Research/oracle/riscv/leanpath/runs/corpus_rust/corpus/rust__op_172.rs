// probe 172 -- binary &
#[no_mangle]
pub fn op_172(a: bool, b: f64) -> <bool as core::ops::BitAnd<f64>>::Output {
    a & b
}
