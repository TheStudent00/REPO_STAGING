// probe 566 -- binary +
#[no_mangle]
pub fn op_566(a: bool, b: u64) -> <bool as core::ops::Add<u64>>::Output {
    a + b
}
