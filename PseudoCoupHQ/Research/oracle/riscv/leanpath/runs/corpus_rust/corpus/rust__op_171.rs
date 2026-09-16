// probe 171 -- binary &
#[no_mangle]
pub fn op_171(a: bool, b: f32) -> <bool as core::ops::BitAnd<f32>>::Output {
    a & b
}
