// probe 525 -- binary >>
#[no_mangle]
pub fn op_525(a: f64, b: f32) -> <f64 as core::ops::Shr<f32>>::Output {
    a >> b
}
