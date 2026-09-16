// probe 544 -- binary +
#[no_mangle]
pub fn op_544(a: i64, b: f64) -> <i64 as core::ops::Add<f64>>::Output {
    a + b
}
