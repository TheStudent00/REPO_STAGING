// probe 524 -- binary >>
#[no_mangle]
pub fn op_524(a: f64, b: u64) -> <f64 as core::ops::Shr<u64>>::Output {
    a >> b
}
