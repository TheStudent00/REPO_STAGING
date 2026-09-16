// probe 33 -- unary &raw mut
#[no_mangle]
pub fn op_33(a: f32) -> f32 {
    &raw mut a
}
