// probe 486 -- binary <<
#[no_mangle]
pub fn op_486(a: f64, b: i32) -> <f64 as core::ops::Shl<i32>>::Output {
    a << b
}
