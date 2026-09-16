// probe 682 -- binary %
#[no_mangle]
pub fn op_682(a: i32, b: f64) -> <i32 as core::ops::Rem<f64>>::Output {
    a % b
}
