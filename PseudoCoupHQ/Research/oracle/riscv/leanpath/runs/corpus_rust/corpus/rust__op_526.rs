// probe 526 -- binary >>
#[no_mangle]
pub fn op_526(a: f64, b: f64) -> <f64 as core::ops::Shr<f64>>::Output {
    a >> b
}
