// probe 595 -- binary -
#[no_mangle]
pub fn op_595(a: f64, b: i64) -> <f64 as core::ops::Sub<i64>>::Output {
    a - b
}
