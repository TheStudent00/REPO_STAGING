// probe 487 -- binary <<
#[no_mangle]
pub fn op_487(a: f64, b: i64) -> <f64 as core::ops::Shl<i64>>::Output {
    a << b
}
