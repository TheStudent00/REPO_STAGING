// probe 631 -- binary *
#[no_mangle]
pub fn op_631(a: f64, b: i64) -> <f64 as core::ops::Mul<i64>>::Output {
    a * b
}
