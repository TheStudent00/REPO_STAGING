// probe 491 -- binary <<
#[no_mangle]
pub fn op_491(a: f64, b: bool) -> <f64 as core::ops::Shl<bool>>::Output {
    a << b
}
