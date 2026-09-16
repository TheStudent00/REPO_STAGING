// probe 27 -- unary &raw const
#[no_mangle]
pub fn op_27(a: f32) -> f32 {
    &raw const a
}
