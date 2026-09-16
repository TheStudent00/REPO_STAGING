// probe 632 -- binary *
#[no_mangle]
pub fn op_632(a: f64, b: u64) -> <f64 as core::ops::Mul<u64>>::Output {
    a * b
}
