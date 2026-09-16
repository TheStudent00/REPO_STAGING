// probe 704 -- binary %
#[no_mangle]
pub fn op_704(a: f64, b: u64) -> <f64 as core::ops::Rem<u64>>::Output {
    a % b
}
