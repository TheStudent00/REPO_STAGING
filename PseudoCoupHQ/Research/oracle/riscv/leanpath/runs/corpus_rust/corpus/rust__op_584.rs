// probe 584 -- binary -
#[no_mangle]
pub fn op_584(a: u64, b: u64) -> <u64 as core::ops::Sub<u64>>::Output {
    a - b
}
