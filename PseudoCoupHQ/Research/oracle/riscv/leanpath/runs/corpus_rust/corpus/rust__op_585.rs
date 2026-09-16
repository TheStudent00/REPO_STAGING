// probe 585 -- binary -
#[no_mangle]
pub fn op_585(a: u64, b: f32) -> <u64 as core::ops::Sub<f32>>::Output {
    a - b
}
