// probe 531 -- binary >>
#[no_mangle]
pub fn op_531(a: bool, b: f32) -> <bool as core::ops::Shr<f32>>::Output {
    a >> b
}
