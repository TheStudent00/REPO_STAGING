// probe 164 -- binary &
#[no_mangle]
pub fn op_164(a: f64, b: u64) -> <f64 as core::ops::BitAnd<u64>>::Output {
    a & b
}
