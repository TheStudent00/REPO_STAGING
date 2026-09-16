// probe 521 -- binary >>
#[no_mangle]
pub fn op_521(a: f32, b: bool) -> <f32 as core::ops::Shr<bool>>::Output {
    a >> b
}
