// probe 630 -- binary *
#[no_mangle]
pub fn op_630(a: f64, b: i32) -> <f64 as core::ops::Mul<i32>>::Output {
    a * b
}
