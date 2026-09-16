// probe 159 -- binary &
#[no_mangle]
pub fn op_159(a: f32, b: f32) -> <f32 as core::ops::BitAnd<f32>>::Output {
    a & b
}
