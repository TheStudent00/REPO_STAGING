// probe 466 -- binary <<
#[no_mangle]
pub fn op_466(a: i32, b: f64) -> <i32 as core::ops::Shl<f64>>::Output {
    a << b
}
