// probe 34 -- unary &raw mut
#[no_mangle]
pub fn op_34(a: f64) -> f64 {
    &raw mut a
}
