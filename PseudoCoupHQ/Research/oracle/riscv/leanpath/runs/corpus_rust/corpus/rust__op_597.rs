// probe 597 -- binary -
#[no_mangle]
pub fn op_597(a: f64, b: f32) -> <f64 as core::ops::Sub<f32>>::Output {
    a - b
}
