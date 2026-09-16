// probe 548 -- binary +
#[no_mangle]
pub fn op_548(a: u64, b: u64) -> <u64 as core::ops::Add<u64>>::Output {
    a + b
}
