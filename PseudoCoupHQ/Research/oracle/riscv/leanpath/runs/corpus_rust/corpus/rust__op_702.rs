// probe 702 -- binary %
#[no_mangle]
pub fn op_702(a: f64, b: i32) -> <f64 as core::ops::Rem<i32>>::Output {
    a % b
}
