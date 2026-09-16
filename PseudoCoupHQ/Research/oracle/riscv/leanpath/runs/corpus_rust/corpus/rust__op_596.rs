// probe 596 -- binary -
#[no_mangle]
pub fn op_596(a: f64, b: u64) -> <f64 as core::ops::Sub<u64>>::Output {
    a - b
}
