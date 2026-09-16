// probe 603 -- binary -
#[no_mangle]
pub fn op_603(a: bool, b: f32) -> <bool as core::ops::Sub<f32>>::Output {
    a - b
}
