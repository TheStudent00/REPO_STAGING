// probe 578 -- binary -
#[no_mangle]
pub fn op_578(a: i64, b: u64) -> <i64 as core::ops::Sub<u64>>::Output {
    a - b
}
