// probe 488 -- binary <<
#[no_mangle]
pub fn op_488(a: f64, b: u64) -> <f64 as core::ops::Shl<u64>>::Output {
    a << b
}
