// probe 590 -- binary -
#[no_mangle]
pub fn op_590(a: f32, b: u64) -> <f32 as core::ops::Sub<u64>>::Output {
    a - b
}
