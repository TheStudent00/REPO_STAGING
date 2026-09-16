// probe 572 -- binary -
#[no_mangle]
pub fn op_572(a: i32, b: u64) -> <i32 as core::ops::Sub<u64>>::Output {
    a - b
}
