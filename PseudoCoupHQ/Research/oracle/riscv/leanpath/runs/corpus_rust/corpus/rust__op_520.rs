// probe 520 -- binary >>
#[no_mangle]
pub fn op_520(a: f32, b: f64) -> <f32 as core::ops::Shr<f64>>::Output {
    a >> b
}
