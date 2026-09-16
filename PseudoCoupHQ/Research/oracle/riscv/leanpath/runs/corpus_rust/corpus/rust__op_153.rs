// probe 153 -- binary &
#[no_mangle]
pub fn op_153(a: u64, b: f32) -> <u64 as core::ops::BitAnd<f32>>::Output {
    a & b
}
