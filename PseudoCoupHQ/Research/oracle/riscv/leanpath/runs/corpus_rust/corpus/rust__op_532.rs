// probe 532 -- binary >>
#[no_mangle]
pub fn op_532(a: bool, b: f64) -> <bool as core::ops::Shr<f64>>::Output {
    a >> b
}
