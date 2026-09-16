// probe 141 -- binary &
#[no_mangle]
pub fn op_141(a: i32, b: f32) -> <i32 as core::ops::BitAnd<f32>>::Output {
    a & b
}
