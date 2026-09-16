// probe 519 -- binary >>
#[no_mangle]
pub fn op_519(a: f32, b: f32) -> <f32 as core::ops::Shr<f32>>::Output {
    a >> b
}
