// probe 598 -- binary -
#[no_mangle]
pub fn op_598(a: f64, b: f64) -> <f64 as core::ops::Sub<f64>>::Output {
    a - b
}
