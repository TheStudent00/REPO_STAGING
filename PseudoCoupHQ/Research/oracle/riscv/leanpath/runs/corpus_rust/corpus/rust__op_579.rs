// probe 579 -- binary -
#[no_mangle]
pub fn op_579(a: i64, b: f32) -> <i64 as core::ops::Sub<f32>>::Output {
    a - b
}
