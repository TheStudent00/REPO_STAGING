// probe 28 -- unary &raw const
#[no_mangle]
pub fn op_28(a: f64) -> f64 {
    &raw const a
}
