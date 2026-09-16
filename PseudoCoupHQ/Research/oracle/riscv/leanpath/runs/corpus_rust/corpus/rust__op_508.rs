// probe 508 -- binary >>
#[no_mangle]
pub fn op_508(a: i64, b: f64) -> <i64 as core::ops::Shr<f64>>::Output {
    a >> b
}
