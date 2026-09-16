// probe 514 -- binary >>
#[no_mangle]
pub fn op_514(a: u64, b: f64) -> <u64 as core::ops::Shr<f64>>::Output {
    a >> b
}
