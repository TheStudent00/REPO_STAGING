// probe 574 -- binary -
#[no_mangle]
pub fn op_574(a: i32, b: f64) -> <i32 as core::ops::Sub<f64>>::Output {
    a - b
}
