// probe 142 -- binary &
#[no_mangle]
pub fn op_142(a: i32, b: f64) -> <i32 as core::ops::BitAnd<f64>>::Output {
    a & b
}
