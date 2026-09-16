// probe 560 -- binary +
#[no_mangle]
pub fn op_560(a: f64, b: u64) -> <f64 as core::ops::Add<u64>>::Output {
    a + b
}
